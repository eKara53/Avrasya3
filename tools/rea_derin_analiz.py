# -*- coding: utf-8 -*-
"""Avrasya2 REA + Capstone + PEFile Derin Tersine Muhendislik Araci.

Incelenen hedefler:
  1. metin2client.bin <-> rascal.dll entegrasyonu ve tum XREF/cagri noktalari
  2. FunctionProtect / RascalProtectRTypes / InitializeRascal / RascalCallback analizi
  3. .text icindeki tum VMProtect (.rdataa0) kancalari ve hangi Python API'lerinin
     alt katmaninda tetiklendikleri (Return Address Check analizi)
  4. CInstanceBase / CPythonPlayer sifreli bellek erisimcileri (0x6dbd90, 0x6dbe10, 0x6dc0a0)
  5. 37 Python C++ modulunun tam yetenek ve guvenlik siniflandirmasi
"""

import collections
import json
import os
import struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

CLIENT_DIR = r"C:\Program Files (x86)\Avrasya2"
BIN_PATH = os.path.join(CLIENT_DIR, "metin2client.bin")
RASCAL_PATH = os.path.join(CLIENT_DIR, "rascal.dll")
API_JSON = r"C:\Users\erenk\Desktop\Avrasya2\tools\cikti\native_apiler.json"
OUT_REPORT = r"C:\Users\erenk\Desktop\Avrasya2\tools\cikti\rea_derin_rapor.txt"


class BinaryAnalyzer(object):
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as f:
            self.data = f.read()
        self.pe = pefile.PE(data=self.data, fast_load=False)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.md = Cs(CS_ARCH_X86, CS_MODE_32)
        self.sections = []
        for s in self.pe.sections:
            name = s.Name.rstrip(b"\x00").decode("latin-1", errors="replace")
            va_start = self.base + s.VirtualAddress
            va_end = va_start + max(s.Misc_VirtualSize, s.SizeOfRawData)
            self.sections.append((name, va_start, va_end, s.PointerToRawData, s.SizeOfRawData))
        self.rel_xrefs = collections.defaultdict(list)
        self._build_rel_index()

    def _build_rel_index(self):
        for name, va_start, _va_end, raw_ptr, raw_size in self.sections:
            if name != ".text":
                continue
            chunk = self.data[raw_ptr:raw_ptr + raw_size]
            for opcode, label in ((0xE8, "rel_call"), (0xE9, "rel_jmp")):
                b_op = bytes([opcode])
                pos = 0
                limit = len(chunk) - 5
                while True:
                    idx = chunk.find(b_op, pos, limit)
                    if idx == -1:
                        break
                    rel = struct.unpack_from("<i", chunk, idx + 1)[0]
                    insn_va = va_start + idx
                    dest = (insn_va + 5 + rel) & 0xFFFFFFFF
                    self.rel_xrefs[dest].append((label, ".text", insn_va))
                    pos = idx + 1

    def va_to_offset(self, va):
        rva = va - self.base
        if rva < 0:
            return None
        try:
            return self.pe.get_offset_from_rva(rva)
        except Exception:
            return None

    def offset_to_va(self, off):
        try:
            return self.base + self.pe.get_rva_from_offset(off)
        except Exception:
            return None

    def section_of(self, va):
        for name, start, end, _, _ in self.sections:
            if start <= va < end:
                return name
        return "?"

    def read_bytes(self, va, size):
        off = self.va_to_offset(va)
        if off is None or off + size > len(self.data):
            return b""
        return self.data[off:off + size]

    def read_u32(self, va):
        b = self.read_bytes(va, 4)
        return struct.unpack("<I", b)[0] if len(b) == 4 else None

    def read_cstr(self, va, max_len=256):
        off = self.va_to_offset(va)
        if off is None or off >= len(self.data):
            return ""
        end = self.data.find(b"\x00", off, off + max_len)
        if end == -1:
            end = off + max_len
        raw = self.data[off:end]
        try:
            return raw.decode("ascii")
        except Exception:
            return raw.decode("latin-1", errors="replace")

    def disasm_func(self, va, max_insns=90, stop_on_ret=True):
        code = self.read_bytes(va, max_insns * 8)
        lines = []
        rets = 0
        for insn in self.md.disasm(code, va):
            comment = ""
            if insn.mnemonic in ("push", "mov") and "0x" in insn.op_str:
                for part in insn.op_str.replace("[", " ").replace("]", " ").replace(",", " ").split():
                    if part.startswith("0x"):
                        try:
                            val = int(part, 16)
                            sec = self.section_of(val)
                            if sec == ".rdata":
                                s = self.read_cstr(val, 80)
                                if len(s) >= 3 and all(32 <= ord(c) < 127 for c in s):
                                    comment = ' ; "%s"' % s
                        except Exception:
                            pass
            lines.append((insn.address, insn.mnemonic, insn.op_str, comment))
            if insn.mnemonic in ("ret", "retn"):
                rets += 1
                if stop_on_ret and rets >= 1:
                    break
            if insn.mnemonic == "jmp" and insn.op_str.startswith("0x"):
                try:
                    t = int(insn.op_str, 16)
                    if self.section_of(t) == ".rdataa0":
                        lines[-1] = (insn.address, insn.mnemonic, insn.op_str, " ; [VMPROTECT .rdataa0]")
                        break
                except Exception:
                    pass
        return lines

    def find_string_vas(self, needle_bytes):
        vas = []
        start = 0
        while True:
            idx = self.data.find(needle_bytes, start)
            if idx == -1:
                break
            va = self.offset_to_va(idx)
            if va is not None:
                vas.append(va)
            start = idx + 1
        return vas

    def find_xrefs_to_va(self, target_va):
        xrefs = list(self.rel_xrefs.get(target_va, []))
        packed = struct.pack("<I", target_va)
        for name, va_start, _va_end, raw_ptr, raw_size in self.sections:
            if name not in (".text", ".rdata", ".data"):
                continue
            chunk = self.data[raw_ptr:raw_ptr + raw_size]
            pos = 0
            while True:
                idx = chunk.find(packed, pos)
                if idx == -1:
                    break
                ref_va = va_start + idx
                xrefs.append(("imm32", name, ref_va))
                pos = idx + 1
        return xrefs


def main():
    out = []
    def w(line=""):
        out.append(line)

    b = BinaryAnalyzer(BIN_PATH)
    w("=" * 88)
    w("AVRASYA2 REA DERIN MIMARI, ANTI-CHEAT (RASCAL + VMPROTECT) VE YETENEK ANALIZI")
    w("=" * 88)

    # 1. PE Imports of metin2client.bin
    w("\n[BOLUM 1] METIN2CLIENT.BIN ITHAL EDILEN (IMPORT) DLL VE FONKSIYONLAR")
    imports_map = {}
    if hasattr(b.pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in b.pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode("latin-1", errors="replace")
            funcs = []
            for imp in entry.imports:
                fname = imp.name.decode("latin-1", errors="replace") if imp.name else ("ord_%s" % imp.ordinal)
                funcs.append((imp.address, fname))
                imports_map[imp.address] = "%s!%s" % (dll, fname)
            w("  - %-22s : %d fonksiyon" % (dll, len(funcs)))
            if "rascal" in dll.lower() or "python" in dll.lower() or "artp" in dll.lower():
                for addr, fn in funcs:
                    w("      0x%08x -> %s" % (addr, fn))

    # 2. Search for rascal strings and export names inside metin2client.bin
    w("\n[BOLUM 2] RASCAL.DLL ENTEGRASYONU VE CAGRI NOKTALARI (XREF)")
    rascal_terms = [
        b"rascal.dll", b"rascal", b"Rascal",
        b"FunctionProtect", b"GetClientCount", b"GetDiscordName",
        b"GetRascalThreadID", b"InitializeRascal", b"RascalCallback",
        b"RascalProtectRTypes", b"RascalSessionRespond", b"RascalSessionRespondEx",
        b"WLog", b"getunknown", b"artpclnt"
    ]
    seen_vas = set()
    for term in rascal_terms:
        vas = b.find_string_vas(term)
        for va in vas:
            if va in seen_vas:
                continue
            seen_vas.add(va)
            s = b.read_cstr(va, 120)
            sec = b.section_of(va)
            xrefs = b.find_xrefs_to_va(va)
            w("  Dize @ 0x%08x (%s): %r -> %d XREF" % (va, sec, s, len(xrefs)))
            for xtype, xsec, xva in xrefs[:10]:
                w("    -> XREF [%s] @ 0x%08x (%s)" % (xtype, xva, xsec))
                if xsec == ".text":
                    start_va = max(0x401000, xva - 32)
                    for a, m, op, c in b.disasm_func(start_va, max_insns=28, stop_on_ret=False):
                        marker = "  <<<" if abs(a - xva) <= 5 else ""
                        w("         0x%08x: %-8s %-28s%s%s" % (a, m, op, c, marker))

    # 3. Check all jumps from .text into .rdataa0 (VMProtect section)
    w("\n[BOLUM 3] .text -> .rdataa0 (VMPROTECT) KANCALARININ TAM HARITASI")
    text_sec = [s for s in b.sections if s[0] == ".text"][0]
    vmp_sec = [s for s in b.sections if s[0] == ".rdataa0"][0]
    _, t_start, t_end, t_raw, t_size = text_sec
    _, v_start, v_end, _, _ = vmp_sec
    t_bytes = b.data[t_raw:t_raw + t_size]

    vmp_jumps = []
    for opcode, kind in ((0xE8, "CALL"), (0xE9, "JMP")):
        b_op = bytes([opcode])
        pos = 0
        limit = len(t_bytes) - 5
        while True:
            i = t_bytes.find(b_op, pos, limit)
            if i == -1:
                break
            rel = struct.unpack_from("<i", t_bytes, i + 1)[0]
            src_va = t_start + i
            dst_va = (src_va + 5 + rel) & 0xFFFFFFFF
            if v_start <= dst_va < v_end:
                prev_b = t_bytes[i - 1] if i > 0 else 0xCC
                is_prologue = prev_b in (0xCC, 0xC3, 0x90) or (i >= 3 and t_bytes[i - 3] == 0xC2)
                vmp_jumps.append((src_va, kind, dst_va, is_prologue))
            pos = i + 1
    vmp_jumps.sort(key=lambda x: x[0])

    w("  Toplam .text -> .rdataa0 gecisi : %d (Fonksiyon baslangici olanlar: %d)" % (
        len(vmp_jumps), sum(1 for x in vmp_jumps if x[3])))
    for src_va, kind, dst_va, is_pro in vmp_jumps:
        if is_pro:
            callers = b.rel_xrefs.get(src_va, [])
            caller_str = ", ".join("0x%08x" % c[2] for c in callers[:8])
            w("    0x%08x: %s 0x%08x [PROLOGUE] <- Cagiranlar (%d): %s" % (
                src_va, kind, dst_va, len(callers), caller_str))

    # 4. Cross-reference all 1,291 Python C functions and their direct callees with VMProtect
    w("\n[BOLUM 4] 37 PYTHON MODULUNDE VMPROTECT KANCALI FONKSIYONLAR (1. VE 2. SEVIYE)")
    with open(API_JSON, "r", encoding="utf-8") as f:
        api_data = json.load(f)

    vmp_prologues = set(x[0] for x in vmp_jumps if x[3])
    direct_vmp_apis = []
    second_level_vmp_apis = []
    clean_apis = []

    for mod_name, mod_info in sorted(api_data.items()):
        if not isinstance(mod_info, dict) or "functions" not in mod_info:
            continue
        for fn in mod_info["functions"]:
            fn_name = fn["name"]
            fn_va = int(fn["va"], 16)
            if fn_va in vmp_prologues or b.section_of(fn_va) == ".rdataa0":
                direct_vmp_apis.append((mod_name, fn_name, fn_va))
                continue
            insns = b.disasm_func(fn_va, max_insns=80, stop_on_ret=False)
            hit_vmp = []
            for a, m, op, _ in insns:
                if m in ("call", "jmp") and op.startswith("0x"):
                    try:
                        callee = int(op, 16)
                        if callee in vmp_prologues or b.section_of(callee) == ".rdataa0":
                            hit_vmp.append(callee)
                        else:
                            c_bytes = b.read_bytes(callee, 5)
                            if len(c_bytes) == 5 and c_bytes[0] == 0xE9:
                                rel = struct.unpack("<i", c_bytes[1:5])[0]
                                target = (callee + 5 + rel) & 0xFFFFFFFF
                                if v_start <= target < v_end:
                                    hit_vmp.append(callee)
                    except Exception:
                        pass
            if hit_vmp:
                second_level_vmp_apis.append((mod_name, fn_name, fn_va, hit_vmp))
            else:
                clean_apis.append((mod_name, fn_name, fn_va))

    w("  - Dogrudan VMProtect girisli Python C API sayisi     : %d" % len(direct_vmp_apis))
    for m, fn, va in direct_vmp_apis:
        w("      * %-16s . %-32s @ 0x%08x" % (m, fn, va))

    w("\n  - Alt C++ motor fonksiyonu VMProtect'li Python API   : %d" % len(second_level_vmp_apis))
    for m, fn, va, callees in second_level_vmp_apis:
        c_str = ", ".join("0x%08x" % c for c in callees)
        w("      * %-16s . %-32s @ 0x%08x -> Alt C++ VMP: %s" % (m, fn, va, c_str))

    w("\n  - Tamamen Acik (.text) Python C API sayisi           : %d" % len(clean_apis))

    # 5. Disassemble Memory Encryption Helpers (0x6dbd90, 0x6dbe10, 0x6dc0a0)
    w("\n[BOLUM 5] BELLEK SIFRELEME / XOR YARDIMCILARI (ANTI-CHEATENGINE KORUMASI)")
    for helper_va, label in [
        (0x006dbd90, "EncryptedField_Read_U32 (0x6dbd90)"),
        (0x006dbe10, "EncryptedField_Write_U32 (0x6dbe10)"),
        (0x006dc0a0, "EncryptedField_Write_U8 (0x6dc0a0)"),
    ]:
        w("  === %s ===" % label)
        for a, m, op, c in b.disasm_func(helper_va, max_insns=45, stop_on_ret=True):
            w("    0x%08x: %-8s %-28s%s" % (a, m, op, c))

    # 6. Disassemble Important Combat / Movement / Entity / Nav Functions
    w("\n[BOLUM 6] KRITIK OYUN MEKANIGI FONKSIYONLARI (SALDIRI, HAREKET, VARLIK, NAV)")
    targets = [
        ("player", "SetMouseState"),
        ("player", "SetMouseButtonState"),
        ("player", "GetMouseFunc"),
        ("player", "SetMouseMiddleButtonState"),
        ("player", "SetSingleDIKKeyState"),
        ("player", "SetAttackKeyState"),
        ("player", "GetMainCharacterIndex"),
        ("player", "GetTargetVID"),
        ("player", "IsMountingHorse"),
        ("player", "GetStatus"),
        ("player", "GetItemIndex"),
        ("player", "GetItemCount"),
        ("player", "GetItemMetinSocket"),
        ("player", "GetItemAttribute"),
        ("chr", "GetProjectPosition"),
        ("chr", "GetRotation"),
        ("chr", "SetRotation"),
        ("chr", "SetDirection"),
        ("chr", "LookAt"),
        ("chr", "GetNameByVID"),
        ("chr", "GetRace"),
        ("chrmgr", "SelectVID"),
        ("chrmgr", "IsPossibleEmoticon"),
        ("chrmgr", "GetPickedVID"),
        ("chrmgr", "GetVIDInfo"),
        ("net", "SendBattlePacket"),
        ("net", "SendCharacterPositionPacket"),
        ("net", "SendWhisperPacket"),
        ("net", "SendGiveItemPacket"),
        ("net", "SendRefinePacket"),
        ("background", "GetCurrentMapName"),
        ("background", "GlobalPositionToMapInfo"),
    ]
    for mod_name, fn_name in targets:
        mod_obj = api_data.get(mod_name)
        if not mod_obj:
            continue
        matches = [f for f in mod_obj["functions"] if f["name"] == fn_name]
        if not matches:
            w("  === %s.%s : YOK ===" % (mod_name, fn_name))
            continue
        fn_va = int(matches[0]["va"], 16)
        w("  === %s.%s @ 0x%08x ===" % (mod_name, fn_name, fn_va))
        for a, m, op, c in b.disasm_func(fn_va, max_insns=45, stop_on_ret=False):
            w("    0x%08x: %-8s %-28s%s" % (a, m, op, c))

    # 7. List all functions in nav, player, chr, chrmgr, net, item, nonplayer
    w("\n[BOLUM 7] TEMEL MODULLERIN TUM FONKSIYON ENVANTERI")
    for mod_name in ("nav", "player", "chr", "chrmgr", "net", "nonplayer", "item", "background"):
        mod_obj = api_data.get(mod_name, {})
        funcs = mod_obj.get("functions", [])
        w("\n  --- Modul: %s (%d fonksiyon) ---" % (mod_name, len(funcs)))
        for fn in funcs:
            w("    %-38s @ %s" % (fn["name"], fn["va"]))

    os.makedirs(os.path.dirname(OUT_REPORT), exist_ok=True)
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Rapor yazildi:", OUT_REPORT, "satir:", len(out))


if __name__ == "__main__":
    main()
