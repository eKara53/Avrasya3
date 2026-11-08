# -*- coding: ascii -*-
"""Avrasya2 Live Runtime Telemetry, Native AC Dumper & RPC Bridge -- sitecustomize.py (v3.2.0)

Rascal-Stealth & Freeze-Free Python 2.7.3 ctypes + pure built-in runtime bridge:
  1. Ensures HKCU AppCompatFlags\Layers (~ RUNASINVOKER) and __COMPAT_LAYER=RunAsInvoker
     without spawning child processes, modifying binaries at runtime, or mutating tokens.
  2. Uses official Python 2.7.3 _ctypes.pyd (RWX-free, zero redundant LoadLibraryA) and
     cloaks _ctypes.pyd's PEB LDR_DATA_TABLE_ENTRY FullDllName/BaseDllName in writable
     heap memory to a Microsoft-signed system DLL (ws2_32.dll) so Rascal's unsigned DLL
     scanner (+0x0E07F0 -> +0x0E8890) sees 0 unsigned modules.
  3. Hooks site.execusercustomize to scrub 'sitecustomize'/'usercustomize' from sys.modules,
     remove AppData\Roaming from sys.path, disable site.ENABLE_USER_SITE, and set
     Py_NoSiteFlag=1 & Py_NoUserSiteDirectory=1 in python27.dll .data BEFORE Py_Initialize()
     returns, neutralizing Rascal's C-API Python startup check (+0x0DE120 / 0x4ECA).
  4. Sets rascal.dll .data flag (+0x295605 = 1) in writable memory to neutralize the
     background process scanner (+0x0E0310 / 0x4EC1) without calling VirtualProtect.
  5. Dumps decrypted EterPack scripts, Python/C-API modules, native ml_meth addresses,
     client singletons, RascalGate, and runs the live RPC execution bridge.
"""

import os
import sys
import time
import __builtin__

VERSION = "3.2.0"
PROJECT_ROOT = r"C:\Users\erenk\Desktop\Avrasya2"
CLIENT_DIR = r"C:\Program Files (x86)\Avrasya2"
SOURCE_DIR = r"C:\Users\erenk\Desktop\Avrasya2\source"
TOOLS_DIR = r"C:\Users\erenk\Desktop\Avrasya2\tools"
BACKUP_DIR = r"C:\Users\erenk\Desktop\Avrasya2\yedek"
LOG_DIR = r"C:\Users\erenk\Desktop\Avrasya2\logs"
PACK_DUMP_DIR = r"C:\Users\erenk\Desktop\Avrasya2\logs\pack_dump"
RUNTIME_LOG = r"C:\Users\erenk\Desktop\Avrasya2\logs\runtime_system.log"
RASCAL_DUMP_BIN = r"C:\Users\erenk\Desktop\Avrasya2\logs\rascal_unpacked.bin"
RPC_CMD_FILE = r"C:\Users\erenk\Desktop\Avrasya2\logs\rpc_cmd.py"
RPC_OUT_FILE = r"C:\Users\erenk\Desktop\Avrasya2\logs\rpc_out.txt"

RASCAL_EXPORTS = (
    ("InitializeRascal", 0x000BD4C0),
    ("FunctionProtect", 0x000B7FA0),
    ("RascalCallback", 0x000B8290),
    ("RascalProtectRTypes", 0x000B83E0),
    ("RascalSessionRespond", 0x00036720),
    ("RascalSessionRespondEx", 0x000366F0),
    ("GetRascalThreadID", 0x000B8080),
    ("getunknown", 0x000B81B0),
    ("WLog", 0x000B80D0),
    ("GetClientCount", 0x000BA400),
    ("GetDiscordName", 0x000BA4F0),
)


class _RuntimeState(object):
    def __init__(self):
        self.bridge_attached = (1 == 0)
        self.import_hooked = (1 == 0)
        self.compile_hooked = (1 == 0)
        self.module_do_hooked = (1 == 0)
        self.window_patched = (1 == 0)
        self.native_dumped = (1 == 0)
        self.peb_cloaked = (1 == 0)
        self.site_scrubbed = (1 == 0)
        self.rascal_data_patched = (1 == 0)
        self.in_hook = (1 == 0)
        self.self_mod = None
        self.user_mod = None
        self.held_mods = {}
        self.orig_execusercustomize = None
        self.ctypes_mod = None
        self.orig_import = getattr(__builtin__, "__import__", None)
        self.orig_compile = getattr(__builtin__, "compile", None)
        self.orig_open = getattr(__builtin__, "open", None)
        self.orig_win_init = None
        self.patched_win_cls = None
        self.system_globals = None
        self.orig_module_do = None
        self.last_gate = ""
        self.dumped_files = set()
        self.dumped_modules = set()
        self.bridge_win = None
        self.last_rpc_check_t = 0.0
        self.last_heartbeat_t = 0.0
        self.last_mod_scan_t = 0.0
        self.last_live_snap = None
        self.frame_count = 0
        self.exe_base = 0x00400000
        self.rascal_base = 0
        self.offshop_tool_ns = None
        self.offshop_tool_failed = (1 == 0)
        self.offshop_tool_mtime = 0.0
        self.last_offshop_mtime_check_t = 0.0
        self.rpc_ns = {
            "__name__": "__avr_rpc__",
            "sys": sys,
            "os": os,
            "time": time,
            "__builtin__": __builtin__,
            "_state": self,
        }


_state = _RuntimeState()


def _safe_ascii(text):
    if text is None:
        return ""
    s = str(text)
    out = []
    for ch in s:
        o = ord(ch)
        if 32 <= o <= 126 or ch in ("\t", "\n"):
            out.append(ch)
        else:
            out.append("\\x%02x" % o)
    return "".join(out)


def _log(msg):
    try:
        open_fn = _state.orig_open or open
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        path = os.path.join(LOG_DIR, "bootstrap.log")
        stamp = time.strftime("%H:%M:%S")
        f = open_fn(path, "a")
        try:
            f.write("%s %s\n" % (stamp, _safe_ascii(msg)))
        finally:
            f.close()
    except Exception:
        pass


def _rt_log(msg):
    try:
        open_fn = _state.orig_open or open
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        stamp = time.strftime("%H:%M:%S")
        f = open_fn(RUNTIME_LOG, "a")
        try:
            f.write("%s %s\n" % (stamp, _safe_ascii(msg)))
        finally:
            f.close()
    except Exception:
        pass


def _read_u32(ct, addr):
    try:
        return int(ct.c_uint32.from_address(int(addr) & 0xFFFFFFFF).value) & 0xFFFFFFFF
    except Exception:
        return 0


def _write_u32(ct, addr, val):
    try:
        ct.c_uint32.from_address(int(addr) & 0xFFFFFFFF).value = int(val) & 0xFFFFFFFF
        return (1 == 1)
    except Exception:
        return (1 == 0)


def _write_u8(ct, addr, val):
    try:
        ct.c_ubyte.from_address(int(addr) & 0xFFFFFFFF).value = int(val) & 0xFF
        return (1 == 1)
    except Exception:
        return (1 == 0)


def _read_f32(ct, addr):
    try:
        return float(ct.c_float.from_address(int(addr) & 0xFFFFFFFF).value)
    except Exception:
        return 0.0


def _read_bytes_hex(ct, addr, size=16):
    try:
        raw = ct.string_at(int(addr) & 0xFFFFFFFF, int(size))
        return "".join("%02x" % ord(b) for b in raw)
    except Exception:
        return ""


def _cloak_ctypes_in_peb(ct):
    """Cloaks _ctypes.pyd in PEB->Ldr->InLoadOrderModuleList by copying the UNICODE_STRING
    FullDllName (+0x24) and BaseDllName (+0x2C) of a Microsoft-signed system DLL (ws2_32.dll)
    into _ctypes.pyd's LDR_DATA_TABLE_ENTRY in writable heap memory (zero VirtualProtect)."""
    if ct is None or _state.peb_cloaked:
        return
    try:
        k32 = ct.windll.kernel32
        ntdll = ct.windll.ntdll
        k32.GetModuleHandleA.argtypes = [ct.c_char_p]
        k32.GetModuleHandleA.restype = ct.c_uint32
        ntdll.NtCurrentTeb.argtypes = []
        ntdll.NtCurrentTeb.restype = ct.c_uint32

        ctypes_base = int(k32.GetModuleHandleA("_ctypes.pyd") or 0) & 0xFFFFFFFF
        donor_base = int(
            k32.GetModuleHandleA("ws2_32.dll")
            or k32.GetModuleHandleA("kernelbase.dll")
            or k32.GetModuleHandleA("kernel32.dll")
            or 0
        ) & 0xFFFFFFFF
        if ctypes_base < 0x10000 or donor_base < 0x10000:
            return

        teb = int(ntdll.NtCurrentTeb() or 0) & 0xFFFFFFFF
        if teb < 0x10000:
            return
        peb = _read_u32(ct, teb + 0x30)
        if peb < 0x10000:
            return
        ldr = _read_u32(ct, peb + 0x0C)
        if ldr < 0x10000:
            return

        # PEB_LDR_DATA.InLoadOrderModuleList head is at ldr + 0x0C
        head = (ldr + 0x0C) & 0xFFFFFFFF
        curr = _read_u32(ct, head)
        ctypes_entry = 0
        donor_entry = 0
        steps = 0
        while curr and curr != head and steps < 256:
            steps += 1
            dll_base = _read_u32(ct, curr + 0x18)
            if dll_base == ctypes_base:
                ctypes_entry = curr
            elif dll_base == donor_base:
                donor_entry = curr
            if ctypes_entry and donor_entry:
                break
            curr = _read_u32(ct, curr)

        if ctypes_entry and donor_entry:
            # Copy FullDllName (8 bytes at +0x24) and BaseDllName (8 bytes at +0x2C)
            for off in (0x24, 0x28, 0x2C, 0x30):
                _write_u32(ct, ctypes_entry + off, _read_u32(ct, donor_entry + off))
            _state.peb_cloaked = (1 == 1)
            _rt_log(
                "[STEALTH:PEB_LDR] Cloaked _ctypes.pyd (base=0x%08X entry=0x%08X) -> donor=0x%08X"
                % (ctypes_base, ctypes_entry, donor_base)
            )
    except Exception as e:
        _rt_log("[STEALTH:PEB_ERR] %s" % str(e))


def _neutralize_rascal_data_flags(ct):
    """Neutralizes writable .data scanner flags inside rascal.dll without touching .text/.rdata."""
    if ct is None:
        return
    try:
        k32 = ct.windll.kernel32
        k32.GetModuleHandleA.argtypes = [ct.c_char_p]
        k32.GetModuleHandleA.restype = ct.c_uint32
        k32.IsBadWritePtr.argtypes = [ct.c_uint32, ct.c_uint32]
        k32.IsBadWritePtr.restype = ct.c_int32

        rascal_base = int(k32.GetModuleHandleA("rascal.dll") or 0) & 0xFFFFFFFF
        if rascal_base < 0x10000:
            return
        _state.rascal_base = rascal_base

        # 1) +0x295605: writable .data boolean flag checked at +0x0E033B and +0x0E056B:
        #    movzx eax, byte ptr [rascal_base + 0x295605]; test eax, eax; jne skip
        #    Setting to 1 disables the CreateToolhelp32Snapshot / Process32NextW scanner.
        # 2) +0x293916: writable .data boolean flag checked at +0x0C7EAE:
        #    movzx ecx, byte ptr [rascal_base + 0x293916]; test ecx, ecx; je 0x0C8359
        #    Setting to 0 skips 11 integrity/debugger/hook checks (0x4e68..0x4e72) while
        #    preserving the watchdog counter increment at +0x0C8403 (+0x29399C).
        # 3) +0x29394E, +0x29394F: secondary scanner flags read at +0x0F5370 / +0x0F5380.
        patches = (
            (0x295605, 1, "proc_scan_skip"),
            (0x293916, 0, "integrity_block_4e68_4e72_skip"),
            (0x29394E, 0, "aux_flag_4e"),
            (0x29394F, 0, "aux_flag_4f"),
        )
        patched_any = (1 == 0)
        for rva, target_val, label in patches:
            addr = (rascal_base + rva) & 0xFFFFFFFF
            if k32.IsBadWritePtr(addr, 1) == 0:
                cur_v = int(ct.c_ubyte.from_address(addr).value)
                if cur_v != target_val:
                    _write_u8(ct, addr, target_val)
                    patched_any = (1 == 1)
                    _rt_log(
                        "[STEALTH:RASCAL_DATA] %s at 0x%08X (+0x%06X): %d -> %d"
                        % (label, addr, rva, cur_v, target_val)
                    )
        if patched_any:
            _state.rascal_data_patched = (1 == 1)
    except Exception as e:
        _rt_log("[STEALTH:RASCAL_DATA_ERR] %s" % str(e))


def _ensure_ctypes():
    if _state.ctypes_mod is not None:
        return _state.ctypes_mod
    ct = sys.modules.get("ctypes")
    if ct is None:
        try:
            imp_fn = _state.orig_import or __import__
            ct = imp_fn("ctypes")
            _log("ctypes yuklendi (RWX-free, PEB-stealth)")
        except Exception as e:
            _log("ctypes yukleme hatasi: %s" % str(e))
            _rt_log("[CTYPES_ERR] %s" % str(e))
            return None
    _state.ctypes_mod = ct
    _state.rpc_ns["ctypes"] = ct
    # Sanitize __file__ metadata on ctypes and _ctypes so no AppData path is exposed
    for m_key in ("ctypes", "ctypes._endian", "_ctypes"):
        m_obj = sys.modules.get(m_key)
        if m_obj is not None and hasattr(m_obj, "__file__"):
            try:
                m_obj.__file__ = os.path.join(CLIENT_DIR, "lib", m_key.replace(".", "\\") + ".pyc")
            except Exception:
                pass
    _cloak_ctypes_in_peb(ct)
    _neutralize_rascal_data_flags(ct)
    return ct


def _scrub_sitecustomize_traces():
    """Scrubs sitecustomize/usercustomize/ctypes/_ctypes from sys.modules, cleans AppData
    paths from sys.path and sys.path_importer_cache, and sets Py_NoSiteFlag=1 &
    Py_NoUserSiteDirectory=1 in python27.dll .data."""
    if _state.site_scrubbed:
        return
    try:
        # Hold strong references in _state so CPython _PyModule_Clear never wipes globals!
        if _state.self_mod is None:
            _state.self_mod = sys.modules.get("sitecustomize")
        if _state.user_mod is None:
            _state.user_mod = sys.modules.get("usercustomize")

        ct = _ensure_ctypes()
        for hidden_key in ("sitecustomize", "usercustomize", "ctypes", "_ctypes", "ctypes._endian"):
            m_ref = sys.modules.get(hidden_key)
            if m_ref is not None:
                _state.held_mods[hidden_key] = m_ref
            sys.modules.pop(hidden_key, None)

        # Clean sys.path of any AppData / Roaming / Python27\site-packages directory
        clean_paths = []
        for p in list(sys.path):
            p_low = str(p).lower()
            if "appdata" in p_low or "roaming" in p_low or "users" in p_low:
                continue
            clean_paths.append(p)
        sys.path[:] = clean_paths

        # Clean sys.path_importer_cache of any AppData / Roaming / Users keys
        pic = getattr(sys, "path_importer_cache", None)
        if isinstance(pic, dict):
            for k in list(pic.keys()):
                k_low = str(k).lower()
                if "appdata" in k_low or "roaming" in k_low or "users" in k_low:
                    pic.pop(k, None)

        # Clean 'site' module attributes inspected by anti-cheat
        site_mod = sys.modules.get("site")
        if site_mod is not None:
            try:
                site_mod.ENABLE_USER_SITE = (1 == 0)
                site_mod.USER_SITE = None
                site_mod.USER_BASE = None
                if _state.orig_execusercustomize is not None:
                    site_mod.execusercustomize = _state.orig_execusercustomize
            except Exception:
                pass

        # Set Py_NoSiteFlag = 1 and Py_NoUserSiteDirectory = 1 in python27.dll writable .data
        if ct is not None:
            try:
                ct.c_int.in_dll(ct.pythonapi, "Py_NoSiteFlag").value = 1
                ct.c_int.in_dll(ct.pythonapi, "Py_NoUserSiteDirectory").value = 1
            except Exception:
                pass

        _state.site_scrubbed = (1 == 1)
        _rt_log(
            "[STEALTH:SITE_SCRUB] Scrubbed sitecustomize/usercustomize/ctypes/_ctypes from sys.modules & path_importer_cache, sys.path=%s, Py_NoSiteFlag=1, Py_NoUserSiteDirectory=1"
            % repr(sys.path)
        )
    except Exception as e:
        _rt_log("[STEALTH:SITE_SCRUB_ERR] %s" % str(e))


def _post_sitecustomize_hook(*args, **kwargs):
    """Hooked onto site.execusercustomize so it runs immediately AFTER site.execsitecustomize()
    completes inside site.main(), BEFORE Py_Initialize() returns to the host process."""
    _scrub_sitecustomize_traces()


def _install_post_site_scrub_hook():
    if _state.self_mod is None:
        _state.self_mod = sys.modules.get("sitecustomize")
    site_mod = sys.modules.get("site")
    if site_mod is not None and hasattr(site_mod, "execusercustomize"):
        orig_eu = getattr(site_mod, "execusercustomize", None)
        if orig_eu is not _post_sitecustomize_hook:
            _state.orig_execusercustomize = orig_eu
            site_mod.execusercustomize = _post_sitecustomize_hook
            site_mod.ENABLE_USER_SITE = (1 == 1)
    else:
        _scrub_sitecustomize_traces()


def _revoke_admin_privileges():
    """Ensures HKCU AppCompatFlags ~ RUNASINVOKER and __COMPAT_LAYER=RunAsInvoker.
    Does not spawn child processes, write to EXE files at runtime, or mutate process tokens."""
    try:
        import _winreg
        key_path = r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
        k = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, key_path)
        for target_bin in ("metin2client.bin", "AvrasyaMt2.exe", "config.exe"):
            full_p = os.path.join(CLIENT_DIR, target_bin)
            _winreg.SetValueEx(k, full_p, 0, _winreg.REG_SZ, "~ RUNASINVOKER")
        _winreg.CloseKey(k)

        ek = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Environment", 0, _winreg.KEY_SET_VALUE)
        _winreg.SetValueEx(ek, "__COMPAT_LAYER", 0, _winreg.REG_SZ, "RunAsInvoker")
        _winreg.CloseKey(ek)
        os.environ["__COMPAT_LAYER"] = "RunAsInvoker"
        _rt_log("[ADMIN_REVOKE:REG] HKCU AppCompatFlags ~ RUNASINVOKER active (AvrasyaMt2.exe IsUserAdmin=patched, Users ACL=M)")
    except Exception as e:
        _rt_log("[ADMIN_REVOKE:REG_ERR] %s" % str(e))


def _get_pycfunction_native_addr(ct, fn_obj):
    """Reads PyCFunctionObject.m_ml->ml_meth (native C++ function pointer) using ctypes."""
    if ct is None or fn_obj is None:
        return 0
    try:
        if type(fn_obj).__name__ != "builtin_function_or_method":
            return 0
        obj_addr = id(fn_obj) & 0xFFFFFFFF
        ml_ptr = _read_u32(ct, obj_addr + 0x08)
        if ml_ptr < 0x10000:
            return 0
        return _read_u32(ct, ml_ptr + 0x04)
    except Exception:
        return 0


def _dump_native_ac_and_client_state(trigger):
    ct = _ensure_ctypes()
    if ct is None:
        return
    try:
        _neutralize_rascal_data_flags(ct)
        k32 = ct.windll.kernel32
        k32.GetModuleHandleA.argtypes = [ct.c_char_p]
        k32.GetModuleHandleA.restype = ct.c_uint32
        k32.IsBadReadPtr.argtypes = [ct.c_uint32, ct.c_uint32]
        k32.IsBadReadPtr.restype = ct.c_int32

        exe_base = int(k32.GetModuleHandleA(None) or 0) & 0xFFFFFFFF
        rascal_base = int(k32.GetModuleHandleA("rascal.dll") or 0) & 0xFFFFFFFF
        py_base = int(getattr(sys, "dllhandle", 0) or k32.GetModuleHandleA("python27.dll") or 0) & 0xFFFFFFFF
        ntdll_base = int(k32.GetModuleHandleA("ntdll.dll") or 0) & 0xFFFFFFFF
        k32_base = int(k32.GetModuleHandleA("kernel32.dll") or 0) & 0xFFFFFFFF

        if exe_base >= 0x10000:
            _state.exe_base = exe_base
        _state.rascal_base = rascal_base
        slide = (_state.exe_base - 0x00400000) & 0xFFFFFFFF

        _rt_log("======================================================================")
        _rt_log("[NATIVE_AC_DUMP:%s] exe=0x%08X (slide=+0x%X) rascal.dll=0x%08X python27.dll=0x%08X kernel32=0x%08X ntdll=0x%08X" % (
            trigger, _state.exe_base, slide, rascal_base, py_base, k32_base, ntdll_base
        ))

        def _va(static_va):
            return (_state.exe_base + (int(static_va) - 0x00400000)) & 0xFFFFFFFF

        def _can_read(addr, sz=16):
            return addr >= 0x10000 and k32.IsBadReadPtr(int(addr) & 0xFFFFFFFF, int(sz)) == 0

        # 1. Dump metin2client.bin RascalGate (0x006ccc90) & AC globals (0x009c7800..0x009c7810) & Singletons
        gate_va = _va(0x006CCC90)
        gate_bytes = _read_bytes_hex(ct, gate_va, 24) if _can_read(gate_va, 24) else "UNMAPPED"
        g_9c7800 = _read_u32(ct, _va(0x009C7800)) if _can_read(_va(0x009C7800), 16) else 0
        g_9c7804 = _read_u32(ct, _va(0x009C7804)) if _can_read(_va(0x009C7804), 16) else 0
        g_9c7808 = _read_u32(ct, _va(0x009C7808)) if _can_read(_va(0x009C7808), 16) else 0
        g_9c780c_u = _read_u32(ct, _va(0x009C780C)) if _can_read(_va(0x009C780C), 16) else 0
        g_9c780c_f = _read_f32(ct, _va(0x009C780C)) if _can_read(_va(0x009C780C), 16) else 0.0

        _rt_log("[RASCAL_GATE:0x%08X] bytes=%s | globals: [0x9c7800]=0x%08X [0x9c7804]=0x%08X [0x9c7808]=0x%08X [0x9c780c]=0x%08X(%.4f)" % (
            gate_va, gate_bytes, g_9c7800, g_9c7804, g_9c7808, g_9c780c_u, g_9c780c_f
        ))

        s_player = _read_u32(ct, _va(0x009C47BC)) if _can_read(_va(0x009C47BC), 4) else 0
        s_chrmgr = _read_u32(ct, _va(0x009C1590)) if _can_read(_va(0x009C1590), 4) else 0
        s_net = _read_u32(ct, _va(0x009C4794)) if _can_read(_va(0x009C4794), 4) else 0
        s_item = _read_u32(ct, _va(0x009BD4C0)) if _can_read(_va(0x009BD4C0), 4) else 0
        s_app = _read_u32(ct, _va(0x009C5600)) if _can_read(_va(0x009C5600), 4) else 0
        _rt_log("[CLIENT_SINGLETONS] CPythonPlayer=0x%08X CPythonCharacterManager=0x%08X CPythonNetworkStream=0x%08X CPythonItem=0x%08X CPythonApplication=0x%08X" % (
            s_player, s_chrmgr, s_net, s_item, s_app
        ))

        # 2. Dump rascal.dll 11 exported entry points & live RAM prologues
        if rascal_base >= 0x10000:
            for exp_name, exp_rva in RASCAL_EXPORTS:
                exp_va = (rascal_base + exp_rva) & 0xFFFFFFFF
                b_hex = _read_bytes_hex(ct, exp_va, 24) if _can_read(exp_va, 24) else "UNMAPPED"
                _rt_log("[RASCAL_EXPORT:%s] va=0x%08X (rva=+0x%06X) bytes=%s" % (
                    exp_name, exp_va, exp_rva, b_hex
                ))
        else:
            _rt_log("[RASCAL_EXPORT] rascal.dll not mapped in process")

        # 3. Check ntdll hooks placed by Rascal AC & trace JMP rel32 targets
        if ntdll_base >= 0x10000:
            k32.GetProcAddress.argtypes = [ct.c_uint32, ct.c_char_p]
            k32.GetProcAddress.restype = ct.c_uint32
            for nt_fn in (
                "LdrLoadDll",
                "NtOpenProcess",
                "NtReadVirtualMemory",
                "NtWriteVirtualMemory",
                "NtProtectVirtualMemory",
                "NtAllocateVirtualMemory",
                "NtQueryInformationProcess",
                "NtQuerySystemInformation",
                "RtlCreateUserThread",
            ):
                fn_va = int(k32.GetProcAddress(ntdll_base, nt_fn) or 0) & 0xFFFFFFFF
                if fn_va and _can_read(fn_va, 16):
                    b_hex = _read_bytes_hex(ct, fn_va, 16)
                    extra = ""
                    if b_hex.startswith("e9"):
                        rel_u = _read_u32(ct, fn_va + 1)
                        rel_s = int(rel_u - 0x100000000) if rel_u >= 0x80000000 else int(rel_u)
                        jmp_tgt = (fn_va + 5 + rel_s) & 0xFFFFFFFF
                        tgt_bytes = _read_bytes_hex(ct, jmp_tgt, 32) if _can_read(jmp_tgt, 32) else "UNMAPPED"
                        if rascal_base >= 0x10000 and rascal_base <= jmp_tgt < (rascal_base + 0x500000):
                            extra = " -> JMP 0x%08X (rascal.dll+0x%06X) tgt_bytes=%s" % (
                                jmp_tgt, jmp_tgt - rascal_base, tgt_bytes
                            )
                        else:
                            extra = " -> JMP 0x%08X (trampoline) tgt_bytes=%s" % (jmp_tgt, tgt_bytes)
                    _rt_log("[NTDLL_HOOK_CHECK:%s] va=0x%08X bytes=%s%s" % (
                        nt_fn, fn_va, b_hex, extra
                    ))

        _rt_log("======================================================================")
        _state.native_dumped = (1 == 1)
    except Exception as e:
        _rt_log("[NATIVE_AC_DUMP_ERR] %s" % str(e))


def _dump_compiled_source(source, filename):
    try:
        if not source:
            return
        fn_str = str(filename or "unknown.py")
        if fn_str in _state.dumped_files:
            return
        _state.dumped_files.add(fn_str)

        open_fn = _state.orig_open or open
        if not os.path.isdir(PACK_DUMP_DIR):
            os.makedirs(PACK_DUMP_DIR)

        clean_name = fn_str.replace(":", "_").replace("\\", "__").replace("/", "__").replace("<", "").replace(">", "")
        if not clean_name.endswith(".py"):
            clean_name = clean_name + ".py"
        out_path = os.path.join(PACK_DUMP_DIR, clean_name)

        raw_bytes = source if isinstance(source, str) else str(source)
        f = open_fn(out_path, "wb")
        try:
            f.write("# DUMPED FROM LIVE COMPILE: %s (len=%d)\n" % (fn_str, len(raw_bytes)))
            f.write(raw_bytes)
        finally:
            f.close()
        _rt_log("[PACK_COMPILE_DUMP] file=%s bytes=%d -> %s" % (fn_str, len(raw_bytes), clean_name))
    except Exception as e:
        _rt_log("[PACK_COMPILE_ERR] %s: %s" % (str(filename), str(e)))


def _inspect_and_dump_module(mod_name, mod_obj):
    if mod_obj is None or mod_name in _state.dumped_modules:
        return
    if mod_name in ("sitecustomize", "usercustomize"):
        return
    _state.dumped_modules.add(mod_name)
    ct = _state.ctypes_mod
    try:
        attrs = dir(mod_obj)
        funcs = []
        consts = []
        classes = []
        others = []
        for a in attrs:
            if a.startswith("__") and a.endswith("__"):
                continue
            try:
                val = getattr(mod_obj, a)
                tname = type(val).__name__
                if tname in ("builtin_function_or_method", "function", "method", "method_descriptor"):
                    c_ptr = _get_pycfunction_native_addr(ct, val) if ct is not None else 0
                    if c_ptr:
                        funcs.append("%s@0x%08X(c=0x%08X)" % (a, id(val) & 0xFFFFFFFF, c_ptr))
                    else:
                        funcs.append("%s@0x%08X" % (a, id(val) & 0xFFFFFFFF))
                elif isinstance(val, (int, long, float, str)):
                    sval = repr(val)
                    if len(sval) > 36:
                        sval = sval[:36] + "..."
                    consts.append("%s=%s" % (a, sval))
                elif tname in ("type", "classobj"):
                    classes.append("%s@0x%08X" % (a, id(val) & 0xFFFFFFFF))
                else:
                    others.append("%s(%s)" % (a, tname))
            except Exception:
                others.append("%s(?)" % a)

        mod_file = getattr(mod_obj, "__file__", "<builtin/pack>")
        _rt_log(
            "[MODULE_DUMP:%s] id=0x%08X file=%s funcs(%d)=[%s] classes(%d)=[%s] consts(%d)=[%s] others(%d)=[%s]"
            % (
                mod_name,
                id(mod_obj) & 0xFFFFFFFF,
                str(mod_file),
                len(funcs),
                ", ".join(funcs[:160]),
                len(classes),
                ", ".join(classes[:60]),
                len(consts),
                ", ".join(consts[:120]),
                len(others),
                ", ".join(others[:60]),
            )
        )
    except Exception as e:
        _rt_log("[MODULE_DUMP_ERR:%s] %s" % (mod_name, str(e)))


def _scan_new_modules():
    try:
        for mname, mobj in list(sys.modules.items()):
            if mobj is not None and mname not in _state.dumped_modules:
                _inspect_and_dump_module(mname, mobj)
    except Exception:
        pass


def _dump_initial_process_state():
    try:
        pid = os.getpid() if hasattr(os, "getpid") else -1
        cwd = os.getcwd() if hasattr(os, "getcwd") else "?"
        _rt_log("======================================================================")
        _rt_log("=== AVRASYA2 LIVE RUNTIME SYSTEM TELEMETRY v%s (PID=%d) ===" % (VERSION, pid))
        _rt_log("sys.version = %s" % repr(sys.version))
        _rt_log("sys.executable = %s" % repr(getattr(sys, "executable", None)))
        _rt_log("sys.prefix = %s | sys.exec_prefix = %s" % (repr(sys.prefix), repr(sys.exec_prefix)))
        _rt_log("sys.path = %s" % repr(sys.path))
        _rt_log("sys.argv = %s" % repr(getattr(sys, "argv", None)))
        _rt_log("cwd = %s" % repr(cwd))
        _rt_log("sys.builtin_module_names (%d) = %s" % (
            len(sys.builtin_module_names), ", ".join(sys.builtin_module_names)
        ))
        _rt_log("initial sys.modules (%d) = %s" % (
            len(sys.modules), ", ".join(sorted(sys.modules.keys()))
        ))
        _revoke_admin_privileges()
        _dump_native_ac_and_client_state("BOOT")
        _scan_new_modules()
    except Exception as e:
        _rt_log("[INIT_DUMP_ERR] %s" % str(e))


def _poll_rpc_command():
    try:
        if not os.path.isfile(RPC_CMD_FILE):
            return
        open_fn = _state.orig_open or open
        compile_fn = _state.orig_compile or compile
        f = open_fn(RPC_CMD_FILE, "rb")
        try:
            cmd_src = f.read()
        finally:
            f.close()
        try:
            os.remove(RPC_CMD_FILE)
        except Exception:
            pass

        clean_src = cmd_src.replace("\r\n", "\n").replace("\r", "\n")
        _rt_log("[RPC_EXEC] executing %d bytes from rpc_cmd.py" % len(clean_src))

        out_lines = []
        def _rpc_write(val):
            out_lines.append(str(val))

        _state.rpc_ns["OUT"] = _rpc_write
        _state.rpc_ns["MODULES"] = sys.modules
        _state.rpc_ns["ctypes"] = _ensure_ctypes()
        try:
            code_obj = compile_fn(clean_src, "<rpc_cmd>", "exec")
            exec code_obj in _state.rpc_ns
            if "_result" in _state.rpc_ns:
                out_lines.append("RESULT: " + repr(_state.rpc_ns.pop("_result")))
            status = "OK"
        except Exception:
            import traceback
            out_lines.append(traceback.format_exc())
            status = "ERR"

        fout = open_fn(RPC_OUT_FILE, "wb")
        try:
            fout.write("=== RPC %s (%s) ===\n" % (status, time.strftime("%H:%M:%S")))
            fout.write("\n".join(out_lines) + "\n")
        finally:
            fout.close()
        _rt_log("[RPC_DONE] status=%s lines=%d" % (status, len(out_lines)))
    except Exception as e:
        _rt_log("[RPC_POLL_ERR] %s" % str(e))


def _tick_offlineshop_tool():
    now = time.clock() if hasattr(time, "clock") else time.time()
    tool_path = os.path.join(SOURCE_DIR, "offlineshop_tool.py")
    if (now - getattr(_state, "last_offshop_mtime_check_t", 0.0)) >= 2.0:
        _state.last_offshop_mtime_check_t = now
        try:
            if os.path.isfile(tool_path):
                cur_mt = float(os.path.getmtime(tool_path))
                if cur_mt > getattr(_state, "offshop_tool_mtime", 0.0):
                    if _state.offshop_tool_ns is not None or _state.offshop_tool_failed:
                        _rt_log("[OFFSHOP_TOOL] Hot-reloading modified source/offlineshop_tool.py")
                    _state.offshop_tool_failed = (1 == 0)
                    _state.offshop_tool_mtime = cur_mt
                    prev_ns = _state.offshop_tool_ns
                    _state.offshop_tool_ns = None
                    _state._prev_offshop_ns = prev_ns
        except Exception:
            pass

    if _state.offshop_tool_failed:
        return
    try:
        if _state.offshop_tool_ns is None:
            if not os.path.isfile(tool_path):
                return
            try:
                _state.offshop_tool_mtime = float(os.path.getmtime(tool_path))
            except Exception:
                pass
            open_fn = _state.orig_open or open
            compile_fn = _state.orig_compile or compile
            f = open_fn(tool_path, "rb")
            try:
                src = f.read()
            finally:
                f.close()
            clean_src = src.replace("\r\n", "\n").replace("\r", "\n")
            ns = {
                "__name__": "__avr_offshop_tool__",
                "__file__": tool_path,
                "__builtin__": __builtin__,
                "__prev_offshop_ns__": getattr(_state, "_prev_offshop_ns", None),
            }
            code_obj = compile_fn(clean_src, tool_path, "exec")
            exec code_obj in ns
            _state.offshop_tool_ns = ns
            _state._prev_offshop_ns = None
            _state.rpc_ns["offshop_tool"] = ns
            _rt_log("[OFFSHOP_TOOL] Loaded source/offlineshop_tool.py (%d bytes)" % len(clean_src))
        tick_fn = _state.offshop_tool_ns.get("tick_suite")
        if tick_fn is not None:
            tick_fn(ct_mod=_ensure_ctypes())
    except Exception as e:
        _state.offshop_tool_failed = (1 == 1)
        _rt_log("[OFFSHOP_TOOL_ERR] %s" % str(e))


def _step_live_runtime_tick():
    _state.frame_count += 1
    now = time.clock() if hasattr(time, "clock") else time.time()

    if not _state.site_scrubbed:
        _scrub_sitecustomize_traces()

    _tick_offlineshop_tool()

    # 1. Poll RPC command every 0.15s
    if now - _state.last_rpc_check_t >= 0.15:
        _state.last_rpc_check_t = now
        _poll_rpc_command()

    # 2. Scan for any newly loaded modules every 0.50s
    if now - _state.last_mod_scan_t >= 0.50:
        _state.last_mod_scan_t = now
        _scan_new_modules()

    # 3. Watch live player / target / picked VID / position transitions
    pl = sys.modules.get("player")
    cm = sys.modules.get("chrmgr")
    if pl is not None:
        try:
            my_vid = int(pl.GetMainCharacterIndex()) if hasattr(pl, "GetMainCharacterIndex") else 0
            if my_vid <= 0 and cm is not None and hasattr(cm, "GetMainVID"):
                my_vid = int(cm.GetMainVID())
            tgt_vid = int(pl.GetTargetVID()) if hasattr(pl, "GetTargetVID") else 0
            pick_vid = int(cm.GetPickedVID()) if (cm is not None and hasattr(cm, "GetPickedVID")) else -1
            snap = (my_vid, tgt_vid, pick_vid)
            if snap != _state.last_live_snap:
                prev_vid = _state.last_live_snap[0] if _state.last_live_snap else 0
                _state.last_live_snap = snap
                pos_s = "(0,0,0)"
                if hasattr(pl, "GetMainCharacterPosition"):
                    p = pl.GetMainCharacterPosition()
                    if p and len(p) >= 3:
                        pos_s = "(%.1f,%.1f,%.1f)" % (float(p[0]), float(p[1]), float(p[2]))
                _rt_log(
                    "[LIVE_STATE_CHANGE] frame=%d my_vid=%d tgt_vid=%d pick_vid=%d pos=%s"
                    % (_state.frame_count, my_vid, tgt_vid, pick_vid, pos_s)
                )
                if prev_vid <= 0 and my_vid > 0:
                    _dump_native_ac_and_client_state("WORLD_ENTER_VID_%d" % my_vid)
        except Exception:
            pass

    # 4. Periodic 5.0s heartbeat
    if now - _state.last_heartbeat_t >= 5.0:
        _state.last_heartbeat_t = now
        try:
            if _state.ctypes_mod is not None and not _state.rascal_data_patched:
                _neutralize_rascal_data_flags(_state.ctypes_mod)
            my_vid = int(pl.GetMainCharacterIndex()) if (pl is not None and hasattr(pl, "GetMainCharacterIndex")) else 0
            pos_s = "(0,0)"
            if pl is not None and hasattr(pl, "GetMainCharacterPosition"):
                p = pl.GetMainCharacterPosition()
                if p and len(p) >= 2:
                    pos_s = "(%.0f,%.0f)" % (float(p[0]), float(p[1]))
            _rt_log(
                "[HEARTBEAT] frame=%d mods=%d packed_files=%d ctypes=%s peb_cloaked=%s site_scrubbed=%s my_vid=%d pos=%s"
                % (
                    _state.frame_count,
                    len(sys.modules),
                    len(_state.dumped_files),
                    bool(_state.ctypes_mod),
                    bool(_state.peb_cloaked),
                    bool(_state.site_scrubbed),
                    my_vid,
                    pos_s,
                )
            )
        except Exception:
            pass


def _is_ui_ready():
    ui_mod = sys.modules.get("ui")
    if ui_mod is None or not hasattr(ui_mod, "Window"):
        return (1 == 0), "ui.Window bekleniyor"
    wnd_mod = sys.modules.get("wndMgr")
    if wnd_mod is None or not hasattr(wnd_mod, "GetScreenWidth"):
        return (1 == 0), "wndMgr bekleniyor"
    try:
        w = int(wnd_mod.GetScreenWidth())
        h = int(wnd_mod.GetScreenHeight()) if hasattr(wnd_mod, "GetScreenHeight") else 600
    except Exception as e:
        return (1 == 0), "GetScreenWidth hata: %s" % e
    if w < 320 or w > 7680 or h < 240 or h > 4320:
        return (1 == 0), "ekran hazir degil (%dx%d)" % (w, h)
    return (1 == 1), "hazir (%dx%d)" % (w, h)


def _attach_runtime_bridge(trigger):
    if _state.bridge_attached:
        return
    ready, reason = _is_ui_ready()
    if reason != _state.last_gate:
        _state.last_gate = reason
        _log("kapi [%s]: %s" % (trigger, reason))
    if not ready:
        _try_patch_window()
        return

    _state.bridge_attached = (1 == 1)
    _ensure_ctypes()
    _scrub_sitecustomize_traces()
    for c_mod in ("app", "net", "chr", "chrmgr", "player", "item", "nonplayer", "background", "textTail", "wndMgr", "grp", "pack", "system", "offlineshop", "ime", "snd", "effect", "event", "quest", "skill", "chat", "messenger", "guild", "safebox", "shop", "exchange", "miniMap"):
        m_name = c_mod.strip()
        if m_name in sys.modules:
            _state.dumped_modules.discard(m_name)
    _scan_new_modules()
    _dump_native_ac_and_client_state("UI_READY_%s" % trigger)

    try:
        ui_mod = sys.modules.get("ui")
        win_base = getattr(ui_mod, "Window", object)

        class _RuntimeBridgeWindow(win_base):
            def __init__(self):
                win_base.__init__(self, "TOP_MOST")
                self.SetSize(0, 0)
                self.SetPosition(0, 0)
                self.Show()

            def OnUpdate(self):
                _step_live_runtime_tick()

        bw = _RuntimeBridgeWindow()
        _state.bridge_win = bw
        _log("canli runtime koprusu kuruldu (%s, ctypes=%s)" % (trigger, bool(_state.ctypes_mod)))
        _rt_log("[BRIDGE_ATTACHED] trigger=%s ctypes=%s peb_cloaked=%s site_scrubbed=%s" % (
            trigger, bool(_state.ctypes_mod), bool(_state.peb_cloaked), bool(_state.site_scrubbed)
        ))
    except Exception as e:
        _log("kopru kurulum hatasi: %s" % e)
        _rt_log("[BRIDGE_ATTACH_ERR] %s" % str(e))


def _window_init_hook(self, *args, **kwargs):
    orig = _state.orig_win_init
    if orig is not None:
        orig(self, *args, **kwargs)
    if not _state.bridge_attached:
        _attach_runtime_bridge("ui.Window.__init__")


def _try_patch_window():
    if _state.window_patched or _state.bridge_attached:
        return
    ui_mod = sys.modules.get("ui")
    if ui_mod is None:
        return
    win_cls = getattr(ui_mod, "Window", None)
    if win_cls is None:
        return
    orig_init = getattr(win_cls, "__init__", None)
    orig_fn = getattr(orig_init, "im_func", orig_init)
    if orig_fn is None or orig_fn is _window_init_hook:
        return
    try:
        _state.orig_win_init = orig_fn
        _state.patched_win_cls = win_cls
        win_cls.__init__ = _window_init_hook
        _state.window_patched = (1 == 1)
        _log("ui.Window.__init__ kancasi kuruldu")
    except Exception as e:
        _log("ui.Window kanca hatasi: %s" % e)


def _try_hook_system_globals(gdict):
    if _state.module_do_hooked or not isinstance(gdict, dict):
        return
    if "module_do" in gdict and "__hybrid_import" in gdict:
        orig_md = gdict.get("module_do")
        if orig_md is not None and orig_md is not _module_do_hook:
            _state.system_globals = gdict
            _state.orig_module_do = orig_md
            gdict["module_do"] = _module_do_hook
            _state.module_do_hooked = (1 == 1)
            _state.rpc_ns["SYSTEM_GLOBALS"] = gdict
            _log("system.module_do kancasi kuruldu")
            _rt_log("[SYSTEM_GLOBALS_HOOKED] keys=%s" % (", ".join(sorted(gdict.keys()))))
            for k, v in sorted(gdict.items()):
                if not k.startswith("__"):
                    _rt_log("  [SYSTEM_GLOBAL] %s = %s (type=%s, id=0x%08X)" % (
                        k, _safe_ascii(repr(v))[:80], type(v).__name__, id(v) & 0xFFFFFFFF
                    ))
            pf = gdict.get("pack_file")
            if pf is not None:
                for target_py in ("system.py", "prototype.py", "localeInfo.py", "constInfo.py", "playersettingmodule.py"):
                    try:
                        fp = pf(target_py, "r")
                        raw = fp.read()
                        if raw:
                            _dump_compiled_source(raw, target_py)
                    except Exception:
                        pass


def _module_do_hook(newmodule):
    orig_md = _state.orig_module_do
    if orig_md is not None:
        try:
            orig_md(newmodule)
        except Exception:
            pass
    try:
        mname = getattr(newmodule, "__name__", None)
        if mname:
            _inspect_and_dump_module(str(mname), newmodule)
    except Exception:
        pass
    if not _state.bridge_attached:
        _try_patch_window()


def _compile_hook(source, filename, mode, *args, **kwargs):
    if not _state.site_scrubbed:
        _scrub_sitecustomize_traces()
    _dump_compiled_source(source, filename)
    res = _state.orig_compile(source, filename, mode, *args, **kwargs)
    if not _state.in_hook:
        _state.in_hook = (1 == 1)
        try:
            _poll_rpc_command()
            if not _state.module_do_hooked:
                for depth in (1, 2, 3):
                    try:
                        caller_globals = sys._getframe(depth).f_globals
                        _try_hook_system_globals(caller_globals)
                    except Exception:
                        break
            if not _state.bridge_attached and "ui" in sys.modules:
                _try_patch_window()
        finally:
            _state.in_hook = (1 == 0)
    return res


def _import_hook(name, *args, **kwargs):
    if not _state.site_scrubbed:
        _scrub_sitecustomize_traces()
    if name in ("sitecustomize", "usercustomize"):
        raise ImportError("No module named %s" % name)
    res = _state.orig_import(name, *args, **kwargs)
    if not _state.in_hook:
        _state.in_hook = (1 == 1)
        try:
            _poll_rpc_command()
            if res is not None and str(name) not in _state.dumped_modules:
                _inspect_and_dump_module(str(name), res)
            if not _state.module_do_hooked:
                for depth in (1, 2, 3):
                    try:
                        caller_globals = sys._getframe(depth).f_globals
                        _try_hook_system_globals(caller_globals)
                    except Exception:
                        break
            if not _state.bridge_attached:
                _try_patch_window()
        finally:
            _state.in_hook = (1 == 0)
    return res


def _bootstrap():
    if getattr(__builtin__.__import__, "_avr_active", (1 == 0)):
        return

    _state.self_mod = sys.modules.get("sitecustomize")
    _log("=== Avrasya2 Live Runtime Bridge v%s ===" % VERSION)
    _dump_initial_process_state()
    _install_post_site_scrub_hook()

    ready, _ = _is_ui_ready()
    if ready:
        _attach_runtime_bridge("dogrudan")
        return

    if _state.orig_import is not None and not _state.import_hooked:
        try:
            _import_hook._avr_active = (1 == 1)
        except Exception:
            pass
        __builtin__.__import__ = _import_hook
        _state.import_hooked = (1 == 1)

    if _state.orig_compile is not None and not _state.compile_hooked:
        __builtin__.compile = _compile_hook
        _state.compile_hooked = (1 == 1)

    _try_patch_window()
    _log("canli runtime izleyici kuruldu (__import__ + compile + module_do + ctypes + PEB-stealth + RPC)")


_bootstrap()
