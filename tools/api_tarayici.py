# -*- coding: utf-8 -*-
"""Avrasya2 metin2client.bin statik native API ve modul tarayicisi.

Calistirma:
    python tools/api_tarayici.py
"""

import json
import os
import re
import struct

CLIENT_DIR = r"C:\Program Files (x86)\Avrasya2"
BIN_PATH = os.path.join(CLIENT_DIR, "metin2client.bin")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "cikti")


def load_pe(path):
    with open(path, "rb") as f:
        b = f.read()
    pe_off = struct.unpack_from("<I", b, 0x3C)[0]
    image_base = struct.unpack_from("<I", b, pe_off + 0x34)[0]
    num_secs = struct.unpack_from("<H", b, pe_off + 6)[0]
    opt_size = struct.unpack_from("<H", b, pe_off + 20)[0]
    sec_off = pe_off + 24 + opt_size
    secs = []
    for i in range(num_secs):
        name, vsz, sva, rsz, rptr = struct.unpack_from("<8sIIII", b, sec_off + i * 40)
        secs.append((name.rstrip(b"\x00").decode("ascii", "replace"), vsz, sva, rsz, rptr))
    return b, image_base, secs


def va_to_off(va, image_base, secs):
    rva = va - image_base
    for _, vsz, sva, rsz, rptr in secs:
        if sva <= rva < sva + rsz:
            return rptr + (rva - sva)
    return None


def off_to_va(off, image_base, secs):
    for _, vsz, sva, rsz, rptr in secs:
        if rptr <= off < rptr + rsz:
            return image_base + sva + (off - rptr)
    return 0


def read_cstr(b, va, image_base, secs, max_len=128):
    off = va_to_off(va, image_base, secs)
    if off is None or off < 0 or off >= len(b):
        return None
    end = b.find(b"\x00", off, off + max_len)
    if end == -1 or end == off:
        return None
    s = b[off:end]
    if all(32 <= c < 127 for c in s):
        return s.decode("ascii")
    return None


def find_module_init_info(b, tva, image_base, secs):
    """Tablo VA'sina referans veren init fonksiyonunu ve modul adini bulur."""
    text_rptr, text_rsz = secs[0][4], secs[0][3]
    pat = b"\x68" + struct.pack("<I", tva)
    pos = b.find(pat, text_rptr, text_rptr + text_rsz)
    if pos == -1:
        return "?", None, []

    # Py_InitModule4 cagrisindaki modul adini bul (push tva etrafindaki push <str>)
    mod_name = "?"
    window = b[max(text_rptr, pos - 24):min(text_rptr + text_rsz, pos + 24)]
    for k in range(len(window) - 5):
        if window[k] == 0x68:
            cand_va = struct.unpack_from("<I", window, k + 1)[0]
            if cand_va != tva:
                s = read_cstr(b, cand_va, image_base, secs)
                if s and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", s):
                    mod_name = s
                    break

    # Init fonksiyonunun sonuna kadar PyModule_AddIntConstant / AddStringConstant sabitlerini tara
    # Fonksiyon sonu: ret (0xC3) veya int3 (0xCC padding)
    func_end = pos + 64
    while func_end < min(text_rptr + text_rsz, pos + 0x4000):
        if b[func_end] == 0xC3 and b[func_end + 1:func_end + 3] in (b"\xCC\xCC", b"\x90\x90", b"\x55\x8B"):
            break
        func_end += 1

    constants = []
    chunk = b[pos:func_end]
    # Kalip: push <int_val> (68 imm32 veya 6A imm8), push <str_va> (68 va), push <mod>, call PyModule_AddIntConstant
    i = 0
    while i < len(chunk) - 12:
        # push imm8 (6A xx) + push str_va (68 xxxx)
        if chunk[i] == 0x6A and chunk[i + 2] == 0x68:
            val = struct.unpack_from("<b", chunk, i + 1)[0]
            sva = struct.unpack_from("<I", chunk, i + 3)[0]
            cname = read_cstr(b, sva, image_base, secs)
            if cname and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", cname):
                constants.append((cname, val))
                i += 7
                continue
        # push imm32 (68 xxxx) + push str_va (68 xxxx)
        if chunk[i] == 0x68 and chunk[i + 5] == 0x68:
            val = struct.unpack_from("<i", chunk, i + 1)[0]
            sva = struct.unpack_from("<I", chunk, i + 6)[0]
            cname = read_cstr(b, sva, image_base, secs)
            if cname and cname != mod_name and re.match(r"^[A-Z_][A-Z0-9_]{2,}$", cname):
                constants.append((cname, val))
                i += 10
                continue
        i += 1

    return mod_name, off_to_va(pos, image_base, secs), constants


def inspect_function_returns(b, func_va, image_base, secs):
    """Fonksiyon govdesindeki Py_BuildValue format dizgelerini cikarir."""
    off = va_to_off(func_va, image_base, secs)
    if off is None:
        return []
    # Fonksiyon govdesini 512 bayta kadar veya C3 + CC/55'e kadar tara
    end = off
    limit = min(len(b) - 4, off + 768)
    while end < limit:
        if b[end] == 0xC3 and b[end + 1] in (0xCC, 0x90, 0x55):
            end += 1
            break
        end += 1
    body = b[off:end]
    formats = []
    for k in range(len(body) - 5):
        if body[k] == 0x68:
            sva = struct.unpack_from("<I", body, k + 1)[0]
            s = read_cstr(b, sva, image_base, secs, max_len=32)
            if s is not None and len(s) <= 16 and re.match(r"^[idfsObhHBIlLkK()\[\]{}]+$", s):
                if s not in formats:
                    formats.append(s)
    return formats


def scan():
    b, image_base, secs = load_pe(BIN_PATH)
    text_start = image_base + secs[0][2]
    text_end = text_start + secs[0][1]

    modules = {}
    for sname, vsz, sva, rsz, rptr in secs[1:4]:
        i = rptr
        end = rptr + rsz - 16
        while i < end:
            name_va, meth_va, flags, doc_va = struct.unpack_from("<IIII", b, i)
            if flags in (0, 1, 2, 3) and (text_start <= meth_va < text_end):
                fn_name = read_cstr(b, name_va, image_base, secs)
                if fn_name and fn_name[0].isalpha():
                    entries = []
                    j = i
                    while j < end:
                        nva, mva, flg, dva = struct.unpack_from("<IIII", b, j)
                        if nva == 0 and mva == 0:
                            break
                        fn = read_cstr(b, nva, image_base, secs)
                        if not fn or not (text_start <= mva < text_end) or flg not in (0, 1, 2, 3, 4, 8):
                            entries = []
                            break
                        rets = inspect_function_returns(b, mva, image_base, secs)
                        entries.append({
                            "name": fn,
                            "va": hex(mva),
                            "flags": flg,
                            "returns": rets,
                        })
                        j += 16
                    if len(entries) >= 2:
                        tva = image_base + sva + (i - rptr)
                        mod_name, init_va, constants = find_module_init_info(b, tva, image_base, secs)
                        modules[mod_name] = {
                            "table_va": hex(tva),
                            "init_va": hex(init_va) if init_va else None,
                            "function_count": len(entries),
                            "constant_count": len(constants),
                            "functions": entries,
                            "constants": constants,
                        }
                        i = j + 16
                        continue
            i += 4

    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)

    json_path = os.path.join(OUT_DIR, "native_apiler.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(modules, f, indent=2, ensure_ascii=False)

    txt_path = os.path.join(OUT_DIR, "native_apiler.txt")
    total_fn = sum(m["function_count"] for m in modules.values())
    total_const = sum(m["constant_count"] for m in modules.values())
    with open(txt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Avrasya2 Native Python Modulleri ve API Imzalari\n")
        f.write("# Kaynak: %s\n" % BIN_PATH)
        f.write("# Toplam: %d modul, %d fonksiyon, %d sabit\n\n" % (len(modules), total_fn, total_const))
        for mod_name in sorted(modules.keys()):
            m = modules[mod_name]
            f.write("[%s] (tablo=%s, fonksiyon=%d, sabit=%d)\n" % (
                mod_name, m["table_va"], m["function_count"], m["constant_count"]))
            for fn in m["functions"]:
                ret_str = (" -> " + "|".join(fn["returns"])) if fn["returns"] else ""
                f.write("  %s()%s  @ %s\n" % (fn["name"], ret_str, fn["va"]))
            if m["constants"]:
                f.write("  # Sabitler:\n")
                for cname, cval in m["constants"]:
                    f.write("  const %s = %d\n" % (cname, cval))
            f.write("\n")

    print("Tarama tamamlandi: %d modul, %d fonksiyon, %d sabit" % (len(modules), total_fn, total_const))
    print("Ciktilar:\n  %s\n  %s" % (txt_path, json_path))


if __name__ == "__main__":
    scan()
