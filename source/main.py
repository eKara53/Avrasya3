# c:/Users/erenk/Desktop/Avrasya2/source/main.py
# -*- coding: ascii -*-
# Avrasya2 Internal Suite v4.6 (Python 2.7 / x86)
# ASLR-Aware Native __cdecl Encrypted Field & Map Bridge + Differential Offset Dumper + [INSERT] GUI

import sys
import os
import time
import math
import re
import struct

try:
    import ctypes
except Exception:
    ctypes = sys.modules.get("ctypes", None)

if not hasattr(time, "clock"):
    time.clock = getattr(time, "perf_counter", time.time)

SUITE_VERSION = "v4.6"

BASE_DIR = r"c:\Users\erenk\Desktop\Avrasya2"
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "avrasya.log")


def _ascii_safe_log(text):
    if text is None:
        return ""
    s = str(text)
    out = []
    for ch in s:
        o = ord(ch)
        if 32 <= o <= 126 or ch in ("\t", "\n"):
            out.append(ch)
        elif ch in _TR_CHAR_MAP:
            out.append(_TR_CHAR_MAP[ch])
        else:
            out.append("?")
    return "".join(out)


def log_msg(text, level="INFO"):
    try:
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        ts = time.strftime("%H:%M:%S")
        with open(LOG_FILE, "a") as fp:
            fp.write("%s [%s] %s\n" % (ts, level, _ascii_safe_log(text)))
    except Exception:
        pass


_CAPI_IMPORTABLE_MODS = set([
    "app", "chr", "chrmgr", "player", "net", "nonplayer", "background",
    "textTail", "grp", "wndMgr", "ui", "chat", "item", "shop", "safebox",
    "exchange", "offlineshop", "event", "effect", "skill", "quest", "ime",
    "miniMap", "systemSetting", "constInfo",
])


def get_mod(name):
    mod = sys.modules.get(name, None)
    if mod is not None:
        return mod
    if "app" in sys.modules and name in _CAPI_IMPORTABLE_MODS:
        try:
            return __import__(name)
        except Exception:
            return None
    return None


_TR_CHAR_MAP = {
    "\xdd": "i", "\xfd": "i", "\xfe": "s", "\xde": "s",
    "\xf0": "g", "\xd0": "g", "\xfc": "u", "\xdc": "u",
    "\xf6": "o", "\xd6": "o", "\xe7": "c", "\xc7": "c",
}


def normalize_tr_ascii(text):
    if not text:
        return ""
    s = str(text)
    out = []
    for ch in s:
        if ch in _TR_CHAR_MAP:
            out.append(_TR_CHAR_MAP[ch])
        elif "A" <= ch <= "Z":
            out.append(chr(ord(ch) + 32))
        else:
            out.append(ch)
    return "".join(out)


def get_item_meta(vnum):
    """Returns (name_ascii, item_type, item_subtype, buy_price, sell_price) using C-API item module."""
    if vnum <= 0:
        return ("", -1, -1, 0, 0)
    item_mod = get_mod("item")
    if item_mod is None or not hasattr(item_mod, "SelectItem"):
        return ("", -1, -1, 0, 0)
    try:
        item_mod.SelectItem(int(vnum))
        nm = ""
        if hasattr(item_mod, "GetItemName"):
            nm = normalize_tr_ascii(item_mod.GetItemName())
        it = int(item_mod.GetItemType()) if hasattr(item_mod, "GetItemType") else -1
        st = int(item_mod.GetItemSubType()) if hasattr(item_mod, "GetItemSubType") else -1
        bp = int(item_mod.GetIBuyItemPrice()) if hasattr(item_mod, "GetIBuyItemPrice") else 0
        sp = int(item_mod.GetISellItemPrice()) if hasattr(item_mod, "GetISellItemPrice") else 0
        return (nm, it, st, bp, sp)
    except Exception:
        return ("", -1, -1, 0, 0)


def scan_inventory_for_item(match_fn, max_slot=1000):
    """
    Scans standard + K-Special inventory (0..999) and special inventory windows (1..11)
    returning (win_type, slot_idx, vnum, item_name) or (None, -1, 0, '').
    """
    player = get_mod("player")
    if player is None or not hasattr(player, "GetItemIndex"):
        return (None, -1, 0, "")
    get_vnum = player.GetItemIndex

    # 1. Standard 1-arg GetItemIndex(slot) covering Inventory (0..179) and Special Inventory (180..999)
    for slot in range(max_slot):
        if 90 <= slot <= 118:
            # Skip equipment range during inventory scan
            continue
        try:
            vnum = int(get_vnum(slot))
            if vnum > 0:
                nm, it, st, bp, sp = get_item_meta(vnum)
                if match_fn(vnum, nm, it, st):
                    return (None, slot, vnum, nm)
        except Exception:
            pass

    # 2. 2-arg GetItemIndex(win_type, slot) for special inventories (Dragon Soul / Special Storage)
    for win_type in (1, 3, 4, 5, 6, 7, 8, 9, 10, 11):
        for slot in range(225):
            if win_type == 1 and 90 <= slot <= 118:
                continue
            try:
                vnum = int(get_vnum(win_type, slot))
                if vnum > 0:
                    nm, it, st, bp, sp = get_item_meta(vnum)
                    if match_fn(vnum, nm, it, st):
                        return (win_type, slot, vnum, nm)
            except Exception:
                break
    return (None, -1, 0, "")


def use_inventory_item(win_type, slot_idx):
    net = get_mod("net")
    if net is None or not hasattr(net, "SendItemUsePacket") or slot_idx < 0:
        return False
    try:
        if win_type is not None:
            try:
                net.SendItemUsePacket(int(win_type), int(slot_idx))
                return True
            except TypeError:
                pass
        net.SendItemUsePacket(int(slot_idx))
        return True
    except Exception:
        return False


def chat_notice(text):
    log_msg("CHAT: " + str(text))
    chat = get_mod("chat")
    if chat is not None:
        try:
            mode = getattr(chat, "CHAT_TYPE_INFO", 1)
            chat.AppendChat(mode, "[Avrasya2] " + str(text))
        except Exception:
            pass


# ============================================================================
# VNUM & ENTITY CLASSIFICATION TABLES
# ============================================================================

AVRASYA_METIN_VNUMS = set(range(8001, 8400)) | set([
    8051, 8052, 8053, 8054, 8055, 8056, 8057, 8058, 8059, 8060,
    8061, 8062, 8063, 8064, 8065, 8066, 8067, 8070, 8071, 8072,
    8073, 8074, 8075, 8076, 8077, 8101, 8102, 8103, 8104, 8105,
    8106, 8107, 8108, 8109, 8110, 8111, 8112, 8113, 8114, 8115,
    8201, 8202, 8203, 8204, 8205, 8206, 8301, 8302, 8303, 8304,
])

AVRASYA_BOSS_VNUMS = set([
    191, 192, 193, 194,
    491, 492, 493, 494,
    591, 691, 692, 693,
    791, 792, 991, 992, 993,
    1091, 1092, 1093, 1094, 1095,
    1191, 1192, 1304, 1306, 1307,
    1401, 1402, 1403, 1901, 1902,
    2091, 2092, 2093, 2094, 2191, 2192,
    2206, 2207, 2291, 2306, 2307,
    2491, 2492, 2493, 2494, 2495,
    2591, 2595, 2596, 2597, 2598,
    3090, 3091, 3190, 3191, 3290, 3291,
    3390, 3391, 3490, 3491, 3590, 3591,
    3595, 3596, 3690, 3691, 3790, 3791,
    3890, 3891, 3970, 3971, 3972,
    4091, 4191, 4291, 6091, 6191, 6192,
])

HP_POTION_VNUMS = set([27001, 27002, 27003, 27007, 27051, 27201, 27202, 27203, 72723, 72724, 72725, 72726])
SP_POTION_VNUMS = set([27004, 27005, 27006, 27008, 27052, 27204, 27205, 27206, 72727, 72728, 72729, 72730])
ELIXIR_DEW_VNUMS = set([
    27100, 27101, 27102, 27103, 27104, 27105,
    27207, 27208, 27209, 27210, 27211, 27212,
    50821, 50822, 50823, 50824, 50825, 50826,
    71027, 71028, 71029, 71030, 71044, 71045,
    39017, 39018, 39019, 39020, 39024, 39025,
])
BRAVERY_CAPE_VNUMS = set([70038, 70057, 76007])

BIYOLOG_MATERIAL_VNUMS = set([
    30006, 30047, 30015, 30050, 30066, 30165, 30166, 30167, 30168,
    30220, 30221, 30222, 30223, 30224, 30225, 30226, 30227, 30228,
    30251, 30252, 30253,
])

ORE_VEIN_VNUMS = set(range(20047, 20060)) | set([30301, 30302, 30303, 30304, 30305])
EFSUN_ITEM_VNUMS = set([71084, 71151, 76014])

VALUABLE_ATTRIBUTE_MIN = {
    1: 1500,   # Max HP
    9: 15,     # Cast Speed
    15: 10,    # Crit
    16: 10,    # Penetrate
    17: 10,    # Half-human
    43: 15,    # Double drop
    44: 15,    # Double yang
    71: 12,    # Skill dmg
    72: 35,    # Avg dmg
}


def is_metin_stone(vnum, name_str, nonplayer_mod):
    if vnum in AVRASYA_METIN_VNUMS:
        return True
    if nonplayer_mod is not None:
        fn_stone = getattr(nonplayer_mod, "IsMonsterStone", None)
        if fn_stone is not None:
            try:
                if int(fn_stone(int(vnum))) == 1:
                    return True
            except Exception:
                pass
    if 8000 <= vnum <= 8999:
        low = (name_str or "").lower()
        if "metin" in low or "tas" in low or low == "" or low.startswith("id_"):
            return True
    if name_str:
        low = name_str.lower()
        if "metin" in low and vnum >= 8000:
            return True
    return False


def is_non_combat_vnum(vnum, event_type):
    # CAutoNav (0x4e1b30) + mob_proto non-combat ranges:
    # event_type: 0=NONE, 1=BATTLE, 2=SHOP, 3=TALK, 4=VEHICLE
    if event_type in (2, 3, 4):
        return True
    if 9001 <= vnum <= 9099:
        return True
    if 10000 <= vnum <= 20999:
        return True
    if 29000 <= vnum <= 35999:
        return True
    return False


# ============================================================================
# 0. NATIVE ENGINE BRIDGE (__cdecl ENCRYPTED FIELD & MAP HELPERS + OFFSET DUMP)
# ============================================================================

class NativeEngineBridge(object):
    """
    Direct ctypes bindings for Avrasya2 (metin2client.bin, ImageBase 0x00400000)
    __cdecl encrypted field & alive-instance map helpers discovered via REA + Capstone:
      - 0x006dbd90: EncRead_A(void* field_addr, void* out_buf, uint32_t size)
      - 0x006dbe10: EncWrite_A(void* field_addr, const void* in_buf, uint32_t size)
      - 0x006dbf70: EncRead_B(void* field_addr, void* out_buf, uint32_t size)
      - 0x006dc0a0: EncWrite_B(void* field_addr, const void* in_buf, uint32_t size)
      - 0x006dc310: EncMapCount(void* map_handle)
      - 0x006dc240: EncMapByIdx(void* map_h, int idx, void* out_p, uint32_t sz, uint32_t* out_sz)
      - 0x006dc470: EncMapFind(void* map_h, uint32_t vid, void* out_p, uint32_t sz, uint32_t* out_sz)
    """

    STATIC_BASE = 0x00400000

    ADDR_PYTHON_PLAYER = 0x009C47BC
    ADDR_CHAR_MGR = 0x009C47C0
    ADDR_NET_STREAM = 0x009C53C8
    ADDR_PYTHON_ITEM = 0x009C54C8
    ADDR_TEXT_TAIL = 0x009C47D0
    ADDR_AUTO_NAV = 0x009C54DC
    ADDR_NON_PLAYER = 0x009C47B4

    FN_ENC_READ_A = 0x006DBD90
    FN_ENC_WRITE_A = 0x006DBE10
    FN_ENC_READ_B = 0x006DBF70
    FN_ENC_WRITE_B = 0x006DC0A0
    FN_ENC_MAP_COUNT = 0x006DC310
    FN_ENC_MAP_BY_IDX = 0x006DC240
    FN_ENC_MAP_FIND = 0x006DC470

    def __init__(self):
        self.ready = False
        self.base_addr = self.STATIC_BASE
        self.k32_bad_read = None
        self.k32_bad_write = None
        self.fn_read_a = None
        self.fn_write_a = None
        self.fn_read_b = None
        self.fn_write_b = None
        self.fn_map_count = None
        self.fn_map_by_idx = None
        self.fn_map_find = None
        self._init_bindings()

    def _u32(self, val):
        return int(val) & 0xFFFFFFFF

    def _s32(self, val):
        u = int(val) & 0xFFFFFFFF
        return int(u - 0x100000000) if u >= 0x80000000 else int(u)

    def va(self, static_va):
        return (self.base_addr + (int(static_va) - self.STATIC_BASE)) & 0xFFFFFFFF

    def _init_bindings(self):
        if ctypes is None or getattr(ctypes, "sizeof", lambda x: 0)(ctypes.c_void_p) != 4:
            return
        try:
            k32 = ctypes.windll.kernel32
            c_u32 = ctypes.c_uint32
            c_i32 = ctypes.c_int32
            c_vp = ctypes.c_void_p

            k32.GetModuleHandleA.argtypes = [c_vp]
            k32.GetModuleHandleA.restype = c_u32
            self.k32_bad_read = k32.IsBadReadPtr
            self.k32_bad_read.argtypes = [c_u32, c_u32]
            self.k32_bad_read.restype = c_i32
            self.k32_bad_write = k32.IsBadWritePtr
            self.k32_bad_write.argtypes = [c_u32, c_u32]
            self.k32_bad_write.restype = c_i32

            exe_b = int(k32.GetModuleHandleA(None) or 0) & 0xFFFFFFFF
            if exe_b >= 0x00010000:
                self.base_addr = exe_b

            # Verify metin2client.bin __cdecl helper code page is mapped and non-zero at FN_ENC_READ_A
            fn_a_va = self.va(self.FN_ENC_READ_A)
            if self.k32_bad_read(fn_a_va, 5) != 0:
                return
            sig_byte = int(ctypes.c_uint8.from_address(self._s32(fn_a_va)).value)
            if sig_byte in (0x00, 0xCC):
                return

            t_rw = ctypes.CFUNCTYPE(None, c_u32, c_vp, c_u32)
            t_cnt = ctypes.CFUNCTYPE(c_i32, c_u32)
            t_idx = ctypes.CFUNCTYPE(c_i32, c_u32, c_i32, c_vp, c_u32, c_vp)
            t_fnd = ctypes.CFUNCTYPE(c_i32, c_u32, c_u32, c_vp, c_u32, c_vp)

            self.fn_read_a = t_rw(self.va(self.FN_ENC_READ_A))
            self.fn_write_a = t_rw(self.va(self.FN_ENC_WRITE_A))
            self.fn_read_b = t_rw(self.va(self.FN_ENC_READ_B))
            self.fn_write_b = t_rw(self.va(self.FN_ENC_WRITE_B))
            self.fn_map_count = t_cnt(self.va(self.FN_ENC_MAP_COUNT))
            self.fn_map_by_idx = t_idx(self.va(self.FN_ENC_MAP_BY_IDX))
            self.fn_map_find = t_fnd(self.va(self.FN_ENC_MAP_FIND))
            self.ready = True
        except Exception as e:
            log_msg("NativeEngineBridge init err: " + str(e), "ERROR")
            self.ready = False

    def ensure_ready(self):
        if not self.ready and ctypes is not None:
            self._init_bindings()
        return self.ready

    def _valid_ptr(self, ptr, size=4):
        u = int(ptr) & 0xFFFFFFFF
        if u < 0x00010000 or u > 0xFFFE0000:
            return False
        if self.k32_bad_read is not None:
            try:
                return int(self.k32_bad_read(u, int(size))) == 0
            except Exception:
                return False
        return u <= 0x7FFF0000

    def _valid_write_ptr(self, ptr, size=4):
        u = int(ptr) & 0xFFFFFFFF
        if u < 0x00010000 or u > 0xFFFE0000:
            return False
        if self.k32_bad_write is not None:
            try:
                return int(self.k32_bad_write(u, int(size))) == 0
            except Exception:
                return False
        return u <= 0x7FFF0000

    def read_u32_plain(self, addr):
        if not self._valid_ptr(addr, 4):
            return 0
        try:
            return int(ctypes.c_uint32.from_address(self._s32(addr)).value) & 0xFFFFFFFF
        except Exception:
            return 0

    def write_u32_plain(self, addr, val):
        if not self._valid_write_ptr(addr, 4):
            return False
        try:
            ctypes.c_uint32.from_address(self._s32(addr)).value = int(val) & 0xFFFFFFFF
            return True
        except Exception:
            return False

    def read_f32_plain(self, addr):
        if not self._valid_ptr(addr, 4):
            return 0.0
        try:
            return float(ctypes.c_float.from_address(self._s32(addr)).value)
        except Exception:
            return 0.0

    def write_f32_plain(self, addr, val):
        if not self._valid_write_ptr(addr, 4):
            return False
        try:
            ctypes.c_float.from_address(self._s32(addr)).value = float(val)
            return True
        except Exception:
            return False

    def read_u8_plain(self, addr):
        if not self._valid_ptr(addr, 1):
            return 0
        try:
            return int(ctypes.c_uint8.from_address(self._s32(addr)).value) & 0xFF
        except Exception:
            return 0

    def write_u8_plain(self, addr, val):
        if not self._valid_write_ptr(addr, 1):
            return False
        try:
            ctypes.c_uint8.from_address(self._s32(addr)).value = int(val) & 0xFF
            return True
        except Exception:
            return False

    def get_player_ptr(self):
        if not self.ensure_ready():
            return 0
        p = self.read_u32_plain(self.va(self.ADDR_PYTHON_PLAYER))
        return p if self._valid_ptr(p, 64) else 0

    def get_chrmgr_ptr(self):
        if not self.ensure_ready():
            return 0
        p = self.read_u32_plain(self.va(self.ADDR_CHAR_MGR))
        return p if self._valid_ptr(p, 48) else 0

    def get_item_ptr(self):
        if not self.ensure_ready():
            return 0
        p = self.read_u32_plain(self.va(self.ADDR_PYTHON_ITEM))
        return p if self._valid_ptr(p, 16) else 0

    def enc_read_a_u32(self, field_addr):
        if not self.ensure_ready() or not self._valid_ptr(field_addr, 4):
            return 0
        try:
            out = ctypes.c_uint32(0)
            self.fn_read_a(self._u32(field_addr), ctypes.byref(out), 4)
            return int(out.value) & 0xFFFFFFFF
        except Exception:
            return 0

    def enc_write_a_u32(self, field_addr, val):
        if not self.ensure_ready() or not self._valid_write_ptr(field_addr, 4):
            return False
        try:
            inp = ctypes.c_uint32(int(val) & 0xFFFFFFFF)
            self.fn_write_a(self._u32(field_addr), ctypes.byref(inp), 4)
            return True
        except Exception:
            return False

    def enc_read_a_f32(self, field_addr):
        if not self.ensure_ready() or not self._valid_ptr(field_addr, 4):
            return 0.0
        try:
            out = ctypes.c_float(0.0)
            self.fn_read_a(self._u32(field_addr), ctypes.byref(out), 4)
            return float(out.value)
        except Exception:
            return 0.0

    def enc_read_b_u32(self, field_addr):
        if not self.ensure_ready() or not self._valid_ptr(field_addr, 4):
            return 0
        try:
            out = ctypes.c_uint32(0)
            self.fn_read_b(self._u32(field_addr), ctypes.byref(out), 4)
            return int(out.value) & 0xFFFFFFFF
        except Exception:
            return 0

    def enc_write_b_u32(self, field_addr, val):
        if not self.ensure_ready() or not self._valid_write_ptr(field_addr, 4):
            return False
        try:
            inp = ctypes.c_uint32(int(val) & 0xFFFFFFFF)
            self.fn_write_b(self._u32(field_addr), ctypes.byref(inp), 4)
            return True
        except Exception:
            return False

    def enc_read_b_u8(self, field_addr):
        if not self.ensure_ready() or not self._valid_ptr(field_addr, 1):
            return 0
        try:
            out = ctypes.c_uint8(0)
            self.fn_read_b(self._u32(field_addr), ctypes.byref(out), 1)
            return int(out.value) & 0xFF
        except Exception:
            return 0

    def enc_write_b_u8(self, field_addr, val):
        if not self.ensure_ready() or not self._valid_write_ptr(field_addr, 1):
            return False
        try:
            inp = ctypes.c_uint8(int(val) & 0xFF)
            self.fn_write_b(self._u32(field_addr), ctypes.byref(inp), 1)
            return True
        except Exception:
            return False

    def enc_read_b_f32(self, field_addr):
        if not self.ensure_ready() or not self._valid_ptr(field_addr, 4):
            return 0.0
        try:
            out = ctypes.c_float(0.0)
            self.fn_read_b(self._u32(field_addr), ctypes.byref(out), 4)
            return float(out.value)
        except Exception:
            return 0.0

    def enc_write_b_f32(self, field_addr, val):
        if not self.ensure_ready() or not self._valid_write_ptr(field_addr, 4):
            return False
        try:
            inp = ctypes.c_float(float(val))
            self.fn_write_b(self._u32(field_addr), ctypes.byref(inp), 4)
            return True
        except Exception:
            return False

    def get_main_inst_ptr(self):
        cm = self.get_chrmgr_ptr()
        if not cm:
            return 0
        inst = self.enc_read_a_u32(cm + 0x0C)
        return inst if self._valid_ptr(inst, 0x800) else 0

    def find_inst_ptr(self, vid):
        if vid <= 0 or not self.ensure_ready():
            return 0
        cm = self.get_chrmgr_ptr()
        if not cm:
            return 0
        map_h = self.read_u32_plain(cm + 0x20)
        if not self._valid_ptr(map_h, 8):
            return 0
        try:
            inst = ctypes.c_uint32(0)
            out_sz = ctypes.c_uint32(0)
            ok = int(self.fn_map_find(self._u32(map_h), self._u32(vid), ctypes.byref(inst), 4, ctypes.byref(out_sz)))
            if ok and int(out_sz.value) == 4 and self._valid_ptr(inst.value, 0x800):
                return int(inst.value) & 0xFFFFFFFF
        except Exception:
            pass
        return 0

    def read_inst_fields(self, inst_ptr):
        """
        Reads decrypted (vid, vnum, actor_type, x, y, z) directly from CInstanceBase*
        using EncRead_A (0x006dbd90), bypassing chr.GetPixelPosition's main_vid anti-bot check!
        """
        if not self._valid_ptr(inst_ptr):
            return None
        try:
            vid = self.enc_read_a_u32(inst_ptr + 0x75C)
            if vid <= 0:
                return None
            vnum = self.enc_read_a_u32(inst_ptr + 0x170)
            actor_type = self.enc_read_a_u32(inst_ptr + 0x5E8)
            fx = self.enc_read_a_f32(inst_ptr + 0x654)
            fy_neg = self.enc_read_a_f32(inst_ptr + 0x658)
            fz = self.enc_read_a_f32(inst_ptr + 0x65C)
            fy = abs(fy_neg) if fy_neg < 0.0 else -fy_neg
            return {
                "inst_ptr": int(inst_ptr),
                "vid": int(vid),
                "vnum": int(vnum),
                "actor_type": int(actor_type),
                "x": float(fx),
                "y": float(fy),
                "z": float(fz),
            }
        except Exception:
            return None

    def enumerate_alive_instances(self):
        """
        Iterates m_kAliveInstMap (*(DWORD*)(chrmgr_ptr + 0x20)) via EncMapCount (0x006dc310)
        and EncMapByIdx (0x006dc240) in O(N) (< 0.05ms) without scanning 300,000 VIDs!
        """
        if not self.ensure_ready():
            return []
        cm = self.get_chrmgr_ptr()
        if not cm:
            return []
        map_h = self.read_u32_plain(cm + 0x20)
        if not self._valid_ptr(map_h, 8):
            return []
        out_list = []
        try:
            cnt = int(self.fn_map_count(self._u32(map_h)))
            if cnt <= 0 or cnt > 2048:
                return []
            inst = ctypes.c_uint32(0)
            out_sz = ctypes.c_uint32(0)
            for idx in range(cnt):
                inst.value = 0
                out_sz.value = 0
                ok = int(self.fn_map_by_idx(self._u32(map_h), int(idx), ctypes.byref(inst), 4, ctypes.byref(out_sz)))
                if ok and int(out_sz.value) == 4 and self._valid_ptr(inst.value, 0x800):
                    data = self.read_inst_fields(int(inst.value) & 0xFFFFFFFF)
                    if data is not None:
                        out_list.append(data)
        except Exception:
            pass
        return out_list

    def set_attack_key_direct(self, state):
        """
        Writes CPythonPlayer + 0xB8 (m_isAtkKey) directly via EncWrite_B (0x006dc0a0),
        executing 0x004fbc45..0x004fbc5a while completely skipping 0x004fbc0e (RascalGate)!
        """
        pl = self.get_player_ptr()
        if pl:
            return self.enc_write_b_u8(pl + 0xB8, 1 if state else 0)
        return False

    def reserve_click_actor_native(self, target_vid, inst_ptr=0):
        """
        Triggers 100% native CPythonPlayer::__ReserveClickActor (0x004fb590) +
        m_pkInstPick (chrmgr + 0x10) so CPythonPlayer::Update() walks to and attacks target_vid!
        """
        if target_vid <= 0 or not self.ensure_ready():
            return False
        pl = self.get_player_ptr()
        cm = self.get_chrmgr_ptr()
        if not pl:
            return False
        try:
            if inst_ptr <= 0:
                inst_ptr = self.find_inst_ptr(target_vid)
            if cm and self._valid_ptr(inst_ptr):
                # Set m_pkInstPick (chrmgr + 0x10) and m_pkInstBind (chrmgr + 0x14)
                self.enc_write_a_u32(cm + 0x10, inst_ptr)
            # Set m_dwVIDReserved (+0xF7E0), m_dwAutoAttackTargetVID (+0xF878), m_dwTargetVID (+0xF88C)
            self.enc_write_a_u32(pl + 0xF7E0, int(target_vid))
            self.enc_write_a_u32(pl + 0xF878, int(target_vid))
            self.enc_write_a_u32(pl + 0xF88C, int(target_vid))
            # m_fReservedDelayTime (+0x70) = 0.02f, m_eReservedMode (+0x60) = 3 (MODE_CLICK_ACTOR)
            self.write_f32_plain(pl + 0x70, 0.02)
            self.enc_write_b_u32(pl + 0x60, 3)
            return True
        except Exception:
            return False

    def reserve_click_ground_native(self, tx, ty, tz=0.0):
        """
        Triggers 100% native CPythonPlayer::__ReserveClickGround (0x004fb5d0):
        writes (tx, ty, tz) to player_ptr + 0xF800 (m_kPPosReserved) and sets
        m_eReservedMode = 1 (MODE_CLICK_POSITION).
        """
        pl = self.get_player_ptr()
        if not pl:
            return False
        try:
            self.write_f32_plain(pl + 0xF800, float(tx))
            self.write_f32_plain(pl + 0xF804, float(abs(ty)))
            self.write_f32_plain(pl + 0xF808, float(tz))
            self.write_f32_plain(pl + 0x70, 0.02)
            self.enc_write_b_u32(pl + 0x60, 1)
            return True
        except Exception:
            return False

    def set_actor_speeds_native(self, atk_spd=1.35, mov_spd=1.35):
        """
        Directly executes CActorInstance::SetAttackSpeed (0x005ffc30 -> inst + 0x674)
        and CActorInstance::SetMoveSpeed (0x005ffb50 -> inst + 0x684) via EncWrite_B (0x006dc0a0),
        bypassing the Py_BuildNone (0x00684680) NO-OP stubs on chr.SetAttackSpeed / chr.SetMoveSpeed!
        """
        main_inst = self.get_main_inst_ptr()
        if not main_inst:
            return False
        ok1 = self.enc_write_b_f32(main_inst + 0x674, float(atk_spd))
        ok2 = self.enc_write_b_f32(main_inst + 0x684, float(mov_spd))
        return ok1 and ok2

    def set_cooltime_check(self, enabled=False):
        """
        CPythonPlayer + 0xF854 = m_isCoolTime (0x004f9680 ToggleCoolTime).
        Writing 0 disables client-side skill cooldown blocking.
        """
        pl = self.get_player_ptr()
        if not pl:
            return False
        return self.write_u8_plain(pl + 0xF854, 1 if enabled else 0)

    def scan_ground_items(self, mx, my, max_dist=550.0):
        """
        Traverses CPythonItem::m_GroundItemInstanceMap (MSVC std::_Tree at [item_ptr + 0x04])
        discovered at 0x004c0590, returning [(dist, item_vid, ix, iy), ...].
        """
        item_ptr = self.get_item_ptr()
        if not item_ptr:
            return []
        head = self.read_u32_plain(item_ptr + 0x04)
        if not self._valid_ptr(head):
            return []
        results = []
        try:
            node = self.read_u32_plain(head + 0x00)  # leftmost node
            steps = 0
            while self._valid_ptr(node) and node != head and steps < 128:
                steps += 1
                is_nil = self.read_u8_plain(node + 0x19)
                if is_nil != 0:
                    break
                item_vid = self.read_u32_plain(node + 0x10)
                p_inst = self.read_u32_plain(node + 0x14)
                if item_vid > 0 and self._valid_ptr(p_inst):
                    ix = self.read_f32_plain(p_inst + 0x08)
                    iy_neg = self.read_f32_plain(p_inst + 0x0C)
                    iy = abs(iy_neg) if iy_neg < 0.0 else -iy_neg
                    d = math.hypot(ix - mx, iy - my) if (mx != 0.0 or my != 0.0) else 0.0
                    if d <= max_dist:
                        results.append((d, int(item_vid), ix, iy))
                # In-order successor in MSVC std::_Tree (0x004c19a0)
                right = self.read_u32_plain(node + 0x08)
                if self._valid_ptr(right) and self.read_u8_plain(right + 0x19) == 0:
                    node = right
                    while True:
                        left = self.read_u32_plain(node + 0x00)
                        if self._valid_ptr(left) and self.read_u8_plain(left + 0x19) == 0:
                            node = left
                        else:
                            break
                else:
                    parent = self.read_u32_plain(node + 0x04)
                    while self._valid_ptr(parent) and self.read_u8_plain(parent + 0x19) == 0 and node == self.read_u32_plain(parent + 0x08):
                        node = parent
                        parent = self.read_u32_plain(parent + 0x04)
                    node = parent
        except Exception:
            pass
        results.sort(key=lambda t: t[0])
        return results

    def read_bytes_hex(self, addr, length=12):
        if not self._valid_ptr(addr, length):
            return ""
        try:
            buf = (ctypes.c_uint8 * int(length)).from_address(self._s32(addr))
            return "".join(["%02X" % int(b) for b in buf])
        except Exception:
            return ""

    def log_pid_and_gate_state(self, phase="BOOT"):
        """
        Passively logs PID, module base addresses (metin2client.bin, rascal.dll, python27.dll),
        ASLR slide, singleton pointers, and C-API gate state.
        Does NOT write any memory or load any external DLL!
        """
        pid = os.getpid() if hasattr(os, "getpid") else -1
        if ctypes is None or getattr(ctypes, "sizeof", lambda x: 0)(ctypes.c_void_p) != 4:
            pl_mod = get_mod("player")
            cm_mod = get_mod("chrmgr")
            my_vid = 0
            tgt_vid = 0
            pick_vid = 0
            pos_s = "(0,0,0)"
            try:
                if pl_mod is not None and hasattr(pl_mod, "GetMainCharacterIndex"):
                    my_vid = int(pl_mod.GetMainCharacterIndex())
                if my_vid <= 0 and cm_mod is not None and hasattr(cm_mod, "GetMainVID"):
                    my_vid = int(cm_mod.GetMainVID())
                if pl_mod is not None and hasattr(pl_mod, "GetTargetVID"):
                    tgt_vid = int(pl_mod.GetTargetVID())
                if cm_mod is not None and hasattr(cm_mod, "GetPickedVID"):
                    pick_vid = int(cm_mod.GetPickedVID())
                if pl_mod is not None and hasattr(pl_mod, "GetMainCharacterPosition"):
                    p = pl_mod.GetMainCharacterPosition()
                    if p and len(p) >= 2:
                        pos_s = "(%.0f,%.0f)" % (float(p[0]), float(p[1]))
            except Exception:
                pass
            capi_loaded = [m for m in ("app", "player", "chr", "chrmgr", "net", "nonplayer", "item", "textTail", "background", "wndMgr", "grp", "nav") if m in sys.modules]
            log_msg("[AC_GATE_TRACE:%s] pid=%d mode=PURE_CAPI_NO_DLL my_vid=%d tgt_vid=%d pick_vid=%d pos=%s mods=%s" % (
                phase, pid, my_vid, tgt_vid, pick_vid, pos_s, ",".join(capi_loaded)
            ))
            return
        try:
            self.ensure_ready()
            k32 = ctypes.windll.kernel32
            exe_b = int(k32.GetModuleHandleA(None) or 0) & 0xFFFFFFFF
            if exe_b >= 0x00010000:
                self.base_addr = exe_b
            ras_b = int(k32.GetModuleHandleA("rascal.dll") or 0) & 0xFFFFFFFF
            py_b = int(k32.GetModuleHandleA("python27.dll") or 0) & 0xFFFFFFFF
            tid = int(k32.GetCurrentThreadId() or 0) & 0xFFFFFFFF
            slide = (self.base_addr - self.STATIC_BASE) & 0xFFFFFFFF

            pl = self.read_u32_plain(self.va(self.ADDR_PYTHON_PLAYER))
            cm = self.read_u32_plain(self.va(self.ADDR_CHAR_MGR))
            net_p = self.read_u32_plain(self.va(self.ADDR_NET_STREAM))
            item_p = self.read_u32_plain(self.va(self.ADDR_PYTHON_ITEM))
            bg_rdy = self.read_u8_plain(self.va(0x009C54D8))

            b_gate = self.read_bytes_hex(self.va(0x006CCC90), 12)
            b_login = self.read_bytes_hex(self.va(0x00542718), 12)
            b_atk = self.read_bytes_hex(self.va(0x004FBC0C), 12)
            b_enc_a = self.read_bytes_hex(self.va(self.FN_ENC_READ_A), 8)

            log_msg(
                "[AC_GATE_TRACE:%s] pid=%d tid=%d ready=%s exe=0x%08X(slide=+0x%X) rascal=0x%08X py27=0x%08X | pl=0x%08X cm=0x%08X net=0x%08X item=0x%08X bgRdy=%d | encA=%s gate(6ccc90)=%s login(542718)=%s atk(4fbc0c)=%s"
                % (
                    phase, pid, tid, str(self.ready), exe_b, slide, ras_b, py_b,
                    pl, cm, net_p, item_p, bg_rdy,
                    b_enc_a, b_gate, b_login, b_atk,
                )
            )
        except Exception as e:
            log_msg("log_pid_and_gate_state err: " + str(e), "ERROR")

    def watch_live_transitions(self, tag="WATCH"):
        """
        Detects any frame-to-frame change in player/target/pick state and logs [OFFSET_CHANGE].
        """
        if not self.ensure_ready():
            pl_mod = get_mod("player")
            cm_mod = get_mod("chrmgr")
            if pl_mod is None:
                return
            try:
                tgt_vid = int(pl_mod.GetTargetVID()) if hasattr(pl_mod, "GetTargetVID") else 0
                pick_vid = int(cm_mod.GetPickedVID()) if (cm_mod is not None and hasattr(cm_mod, "GetPickedVID")) else 0
                snap = (tgt_vid, pick_vid)
                prev = getattr(self, "_last_capi_snap", None)
                if snap != prev:
                    self._last_capi_snap = snap
                    log_msg("[OFFSET_CHANGE:%s] mode=CAPI vidTgt=%d pickVID=%d" % (tag, tgt_vid, pick_vid))
            except Exception:
                pass
            return
        pl = self.get_player_ptr()
        cm = self.get_chrmgr_ptr()
        if not pl or not cm:
            return
        try:
            res_mode = self.enc_read_b_u32(pl + 0x60)
            atk_key = self.enc_read_b_u8(pl + 0xB8)
            dir_key = self.enc_read_b_u8(pl + 0xC8)
            smt_mov = self.enc_read_b_u8(pl + 0x78)
            dir_mov = self.enc_read_b_u8(pl + 0x88)
            vid_res = self.enc_read_a_u32(pl + 0xF7E0)
            vid_auto = self.enc_read_a_u32(pl + 0xF878)
            vid_tgt = self.enc_read_a_u32(pl + 0xF88C)
            mbf_l = self.read_u32_plain(pl + 0x54)
            pick_inst = self.enc_read_a_u32(cm + 0x10)
            pick_vid = self.enc_read_a_u32(pick_inst + 0x75C) if self._valid_ptr(pick_inst) else 0

            snap = (res_mode, atk_key, dir_key, smt_mov, dir_mov, vid_res, vid_auto, vid_tgt, mbf_l, pick_vid)
            prev = getattr(self, "_last_watch_snap", None)
            if snap != prev:
                self._last_watch_snap = snap
                log_msg(
                    "[OFFSET_CHANGE:%s] mode=%d atkKey=%d dirKey=%d smtMov=%d dirMov=%d mbfL=%d | vidRes=%d vidAuto=%d vidTgt=%d pickVID=%d"
                    % (tag, res_mode, atk_key, dir_key, smt_mov, dir_mov, mbf_l, vid_res, vid_auto, vid_tgt, pick_vid)
                )
        except Exception:
            pass

    def dump_live_offsets(self, tag="STATE"):
        """
        Logs a differential snapshot of CPythonPlayer / CPythonCharacterManager state to logs/avrasya.log.
        """
        if not self.ensure_ready():
            pl_mod = get_mod("player")
            cm_mod = get_mod("chrmgr")
            chr_mod = get_mod("chr")
            if pl_mod is None:
                return
            try:
                my_vid = int(pl_mod.GetMainCharacterIndex()) if hasattr(pl_mod, "GetMainCharacterIndex") else 0
                tgt_vid = int(pl_mod.GetTargetVID()) if hasattr(pl_mod, "GetTargetVID") else 0
                pick_vid = int(cm_mod.GetPickedVID()) if (cm_mod is not None and hasattr(cm_mod, "GetPickedVID")) else 0
                px, py = 0.0, 0.0
                if hasattr(pl_mod, "GetMainCharacterPosition"):
                    p = pl_mod.GetMainCharacterPosition()
                    if p and len(p) >= 2:
                        px, py = float(p[0]), float(p[1])
                rot = float(chr_mod.GetRotation()) if (chr_mod is not None and hasattr(chr_mod, "GetRotation")) else 0.0
                log_msg("[OFFSET_DUMP:%s] mode=CAPI myVID=%d vidTgt=%d pickVID=%d pos=(%.0f,%.0f) rot=%.1f" % (
                    tag, my_vid, tgt_vid, pick_vid, px, py, rot
                ))
            except Exception:
                pass
            return
        pl = self.get_player_ptr()
        cm = self.get_chrmgr_ptr()
        main_inst = self.get_main_inst_ptr()
        if not pl or not cm:
            return
        try:
            res_mode = self.enc_read_b_u32(pl + 0x60)
            smt_mov = self.enc_read_b_u8(pl + 0x78)
            dir_mov = self.enc_read_b_u8(pl + 0x88)
            atk_key = self.enc_read_b_u8(pl + 0xB8)
            dir_key = self.enc_read_b_u8(pl + 0xC8)
            vid_res = self.enc_read_a_u32(pl + 0xF7E0)
            vid_auto = self.enc_read_a_u32(pl + 0xF878)
            vid_tgt = self.enc_read_a_u32(pl + 0xF88C)
            cool_chk = self.read_u8_plain(pl + 0xF854)
            mbf_l = self.read_u32_plain(pl + 0x54)

            pick_inst = self.enc_read_a_u32(cm + 0x10)
            pick_vid = self.enc_read_a_u32(pick_inst + 0x75C) if self._valid_ptr(pick_inst) else 0
            map_h = self.read_u32_plain(cm + 0x20)
            alive_cnt = int(self.fn_map_count(self._u32(map_h))) if self._valid_ptr(map_h, 8) else -1

            atk_spd = self.enc_read_b_f32(main_inst + 0x674) if main_inst else 0.0
            mov_spd = self.enc_read_b_f32(main_inst + 0x684) if main_inst else 0.0
            px = self.enc_read_a_f32(main_inst + 0x654) if main_inst else 0.0
            py = -self.enc_read_a_f32(main_inst + 0x658) if main_inst else 0.0

            log_msg(
                "[OFFSET_DUMP:%s] pl=0x%X cm=0x%X main=0x%X | mode=%d atkKey=%d dirKey=%d smtMov=%d dirMov=%d mbfL=%d cool=%d | vidRes=%d vidAuto=%d vidTgt=%d pickVID=%d | aliveCnt=%d pos=(%.0f,%.0f) spd=(atk:%.2f,mov:%.2f)"
                % (
                    tag, pl, cm, main_inst,
                    res_mode, atk_key, dir_key, smt_mov, dir_mov, mbf_l, cool_chk,
                    vid_res, vid_auto, vid_tgt, pick_vid,
                    alive_cnt, px, py, atk_spd, mov_spd,
                )
            )
        except Exception as e:
            log_msg("dump_live_offsets err: " + str(e), "ERROR")


_NATIVE_BRIDGE = NativeEngineBridge()


# ============================================================================
# 1. ENTITY RADAR + NATIVE m_kAliveInstMap SCANNER + 3D CAMERA W2S PROJECTION
# ============================================================================

class EntityRadar(object):
    FILTER_MODES = [
        ("all", "Tumu"),
        ("metin_boss", "Metin+Boss"),
        ("metin", "Sadece Metin"),
        ("boss", "Sadece Boss"),
        ("monster", "Canavar"),
        ("ore", "Maden Damari"),
    ]

    def __init__(self):
        self.entities = {}
        self.near_cursor = -35000
        self.band_cursor = 0
        self.global_cursor = 1
        self.min_seen_vid = 0
        self.max_seen_vid = 0
        self.filter_idx = 0
        self.last_prune_t = 0.0
        self.last_trilat_t = 0.0
        self.last_w2s_t = 0.0
        self.last_minimap_t = 0.0
        self.pinned_vids = set()
        self.cam_dir_x = 0.0
        self.cam_dir_y = -1.0

    def get_filter_mode(self):
        return self.FILTER_MODES[self.filter_idx][0]

    def get_filter_label(self):
        return self.FILTER_MODES[self.filter_idx][1]

    def cycle_filter(self):
        self.filter_idx = (self.filter_idx + 1) % len(self.FILTER_MODES)
        return self.get_filter_label()

    def get_player_state(self):
        player = get_mod("player")
        if player is None:
            return 0, 0.0, 0.0, 0.0
        my_vid = 0
        try:
            my_vid = int(player.GetMainCharacterIndex())
        except Exception:
            my_vid = 0
        if my_vid <= 0:
            chrmgr = get_mod("chrmgr")
            if chrmgr is not None:
                try:
                    my_vid = int(chrmgr.GetMainVID())
                except Exception:
                    my_vid = 0
        mx, my, mz = 0.0, 0.0, 0.0
        try:
            pos = player.GetMainCharacterPosition()
            if pos and len(pos) >= 3:
                mx, my, mz = float(pos[0]), float(pos[1]), float(pos[2])
            elif pos and len(pos) >= 2:
                mx, my = float(pos[0]), float(pos[1])
        except Exception:
            pass
        return my_vid, mx, my, mz

    def classify_vid(self, vid, my_vid, chr_mod, nonplayer_mod, player_mod):
        if vid <= 0 or vid == my_vid:
            return None
        try:
            if not chr_mod.HasInstance(vid):
                return None
        except Exception:
            return None

        vnum = 0
        try:
            vnum = int(chr_mod.GetVirtualNumber(vid))
        except Exception:
            vnum = 0
        if vnum <= 0 and nonplayer_mod is not None:
            try:
                rv = int(nonplayer_mod.GetRaceNumByVID(vid))
                if rv > 0:
                    vnum = rv
            except Exception:
                pass

        name_str = ""
        try:
            nm = chr_mod.GetNameByVID(vid)
            if nm and nm != "None":
                name_str = str(nm)
        except Exception:
            pass
        if not name_str and vnum > 0 and nonplayer_mod is not None:
            try:
                mn = nonplayer_mod.GetMonsterName(vnum)
                if mn and mn != "None":
                    name_str = str(mn)
            except Exception:
                pass

        event_type = -1
        grade = 0
        max_hp = 0
        if nonplayer_mod is not None:
            try:
                event_type = int(nonplayer_mod.GetEventTypeByVID(vid))
            except Exception:
                try:
                    if vnum > 0:
                        event_type = int(nonplayer_mod.GetEventType(vnum))
                except Exception:
                    event_type = -1
            try:
                grade = int(nonplayer_mod.GetGradeByVID(vid))
            except Exception:
                grade = 0
            if vnum > 0:
                try:
                    max_hp = int(nonplayer_mod.GetMonsterMaxHP(vnum))
                except Exception:
                    max_hp = 0

        # 1. Metin Stone check (IsMonsterStone checks pMobTable->bType == 2 directly)
        if is_metin_stone(vnum, name_str, nonplayer_mod):
            kind = "metin"
        # 1B. Ore Vein check (20047..20059)
        elif vnum in ORE_VEIN_VNUMS:
            kind = "ore"
        # 2. Player check (races 0..8 have max_hp == 0 in mob_proto and event_type == 0)
        elif 0 <= vnum <= 8 and max_hp <= 0 and event_type <= 0:
            if not name_str:
                return None
            kind = "player"
        # 3. Non-combat NPC / Shop / Horse / Mount / Pet / Portal filter
        elif is_non_combat_vnum(vnum, event_type):
            kind = "npc"
        else:
            # 4. Boss / Monster check
            can_atk = False
            if event_type == 1:
                can_atk = True
            elif player_mod is not None:
                try:
                    can_atk = bool(player_mod.CanAttackInstance(vid))
                except Exception:
                    can_atk = False
            if not can_atk and 101 <= vnum <= 7999 and max_hp > 0:
                can_atk = True

            if can_atk:
                if grade >= 4 or vnum in AVRASYA_BOSS_VNUMS:
                    kind = "boss"
                else:
                    kind = "monster"
            else:
                kind = "npc"

        dist = -1.0
        if player_mod is not None:
            try:
                dist = float(player_mod.GetCharacterDistance(vid))
            except Exception:
                dist = -1.0
        if dist < 0.0 or dist > 25000.0:
            return None

        if not name_str:
            name_str = "ID_%d" % vnum

        return {
            "vid": vid,
            "vnum": vnum,
            "name": name_str,
            "kind": kind,
            "grade": grade,
            "dist": dist,
            "x": 0.0,
            "y": 0.0,
            "has_world_pos": False,
            "static_locked": False,
            "pos_t": 0.0,
            "sx": 0.0,
            "sy": 0.0,
            "on_screen": False,
            "seen_t": time.clock(),
        }

    def _merge_entity(self, vid, info, now):
        if vid > 1000:
            if self.min_seen_vid <= 0 or vid < self.min_seen_vid:
                self.min_seen_vid = vid
            if vid > self.max_seen_vid:
                self.max_seen_vid = vid
        old = self.entities.get(vid)
        if old is not None:
            old["dist"] = info["dist"]
            old["seen_t"] = now
            if info["name"] and not info["name"].startswith("ID_"):
                old["name"] = info["name"]
            if info["vnum"] > 0:
                old["vnum"] = info["vnum"]
            old["kind"] = info["kind"]
            if info.get("has_world_pos", False):
                old["x"] = info["x"]
                old["y"] = info["y"]
                old["has_world_pos"] = True
                old["pos_t"] = info.get("pos_t", now)
            if info.get("inst_ptr", 0) > 0:
                old["inst_ptr"] = info["inst_ptr"]
        else:
            self.entities[vid] = info

    def step_scan(self, my_vid, now):
        chr_mod = get_mod("chr")
        nonplayer_mod = get_mod("nonplayer")
        player_mod = get_mod("player")
        if chr_mod is None or player_mod is None or my_vid <= 0:
            return

        # 0. Native O(N) m_kAliveInstMap enumeration via EncMapCount (0x006dc310) + EncMapByIdx (0x006dc240)
        if _NATIVE_BRIDGE.ensure_ready():
            alive_list = _NATIVE_BRIDGE.enumerate_alive_instances()
            if alive_list:
                for raw in alive_list:
                    r_vid = int(raw["vid"])
                    if r_vid <= 0 or r_vid == my_vid:
                        continue
                    old_inf = self.entities.get(r_vid)
                    if old_inf is not None and (now - old_inf.get("seen_t", 0.0) < 1.2):
                        old_inf["x"] = raw["x"]
                        old_inf["y"] = raw["y"]
                        old_inf["has_world_pos"] = True
                        old_inf["pos_t"] = now
                        old_inf["inst_ptr"] = raw["inst_ptr"]
                        old_inf["seen_t"] = now
                        try:
                            d = float(player_mod.GetCharacterDistance(r_vid))
                            if d >= 0.0:
                                old_inf["dist"] = d
                        except Exception:
                            pass
                        continue
                    info = self.classify_vid(r_vid, my_vid, chr_mod, nonplayer_mod, player_mod)
                    if info is not None:
                        info["x"] = raw["x"]
                        info["y"] = raw["y"]
                        info["has_world_pos"] = True
                        info["pos_t"] = now
                        info["inst_ptr"] = raw["inst_ptr"]
                        self._merge_entity(r_vid, info, now)
                return

        has_inst = getattr(chr_mod, "HasInstance", None)
        if has_inst is None:
            return

        # 1. Picked VID under mouse
        chrmgr = get_mod("chrmgr")
        if chrmgr is not None:
            try:
                pvid = int(chrmgr.GetPickedVID())
                if pvid > 0 and pvid != my_vid:
                    info = self.classify_vid(pvid, my_vid, chr_mod, nonplayer_mod, player_mod)
                    if info is not None:
                        self._merge_entity(pvid, info, now)
            except Exception:
                pass

        # 2. Fast Near-VID Window (my_vid - 35000 .. my_vid + 35000), 0.7 ms budget
        t_limit1 = time.clock() + 0.0007
        checked = 0
        while checked < 1000 and time.clock() < t_limit1:
            vid = my_vid + self.near_cursor
            self.near_cursor += 1
            if self.near_cursor > 35000:
                self.near_cursor = -35000
            checked += 1
            if vid <= 0 or vid == my_vid:
                continue
            try:
                if not has_inst(vid):
                    continue
            except Exception:
                continue
            info = self.classify_vid(vid, my_vid, chr_mod, nonplayer_mod, player_mod)
            if info is not None:
                self._merge_entity(vid, info, now)

        # 3. Dynamic Active-Band Sweep around [min_seen_vid - 110000 .. max_seen_vid + 45000], 0.65 ms budget
        # Covers Avrasya2 high VIDs (~6,940,000 .. 7,100,000) without wasting 98% of scans on 1..6,900,000
        base_lo = self.min_seen_vid if self.min_seen_vid > 1000 else my_vid
        base_hi = self.max_seen_vid if self.max_seen_vid > my_vid else my_vid
        band_lo = max(1, base_lo - 110000)
        band_hi = max(band_lo + 20000, base_hi + 45000)
        if self.band_cursor < band_lo or self.band_cursor > band_hi:
            self.band_cursor = band_lo

        t_limit2 = time.clock() + 0.00065
        b_checked = 0
        while b_checked < 1000 and time.clock() < t_limit2:
            vid = self.band_cursor
            self.band_cursor += 1
            if self.band_cursor > band_hi:
                self.band_cursor = band_lo
            b_checked += 1
            if vid <= 0 or vid == my_vid:
                continue
            try:
                if not has_inst(vid):
                    continue
            except Exception:
                continue
            info = self.classify_vid(vid, my_vid, chr_mod, nonplayer_mod, player_mod)
            if info is not None:
                self._merge_entity(vid, info, now)

        # 4. Low-VID Sweep (1 .. 150000) for static/low-VID instances, 0.25 ms budget
        t_limit3 = time.clock() + 0.00025
        g_checked = 0
        while g_checked < 350 and time.clock() < t_limit3:
            vid = self.global_cursor
            self.global_cursor += 1
            if self.global_cursor > 150000:
                self.global_cursor = 1
            g_checked += 1
            if vid == my_vid:
                continue
            try:
                if not has_inst(vid):
                    continue
            except Exception:
                continue
            info = self.classify_vid(vid, my_vid, chr_mod, nonplayer_mod, player_mod)
            if info is not None:
                self._merge_entity(vid, info, now)

    def step_prune_and_distances(self, my_vid, now):
        if now - self.last_prune_t < 0.20:
            return
        self.last_prune_t = now
        chr_mod = get_mod("chr")
        player_mod = get_mod("player")
        if chr_mod is None or player_mod is None:
            return
        has_inst = getattr(chr_mod, "HasInstance", None)
        get_dist = getattr(player_mod, "GetCharacterDistance", None)
        if has_inst is None or get_dist is None:
            return

        dead_vids = []
        for vid, info in list(self.entities.items()):
            if vid == my_vid:
                dead_vids.append(vid)
                continue
            try:
                if not has_inst(vid):
                    dead_vids.append(vid)
                    continue
                d = float(get_dist(vid))
                if d < 0.0 or d > 25000.0:
                    dead_vids.append(vid)
                    continue
                info["dist"] = d
                info["seen_t"] = now
            except Exception:
                dead_vids.append(vid)

        for vid in dead_vids:
            self.entities.pop(vid, None)

    def step_trilaterate(self, my_vid, mx, my, mz, now, priority_vid=0, farm_active=False, in_melee=False):
        if my_vid <= 0 or (mx == 0.0 and my == 0.0):
            return

        # In Live Client: read exact decrypted (x, y, z) directly from CInstanceBase + 0x654..0x65C
        # via EncRead_A (0x006dbd90), NEVER calling chr.SetPixelPosition on my_vid!
        if _NATIVE_BRIDGE.ensure_ready():
            for vid, info in list(self.entities.items()):
                if vid != priority_vid and info.get("has_world_pos", False) and (now - info.get("pos_t", 0.0) < 0.25):
                    continue
                iptr = info.get("inst_ptr", 0)
                if not _NATIVE_BRIDGE._valid_ptr(iptr):
                    iptr = _NATIVE_BRIDGE.find_inst_ptr(vid)
                if _NATIVE_BRIDGE._valid_ptr(iptr):
                    raw = _NATIVE_BRIDGE.read_inst_fields(iptr)
                    if raw is not None and (raw["x"] != 0.0 or raw["y"] != 0.0):
                        info["inst_ptr"] = iptr
                        info["x"] = raw["x"]
                        info["y"] = raw["y"]
                        info["has_world_pos"] = True
                        info["pos_t"] = now
            return

        prio_info = self.entities.get(priority_vid) if priority_vid > 0 else None
        prio_age = (now - prio_info.get("pos_t", 0.0)) if prio_info is not None else 999.0
        need_urgent = prio_info is not None and (
            not prio_info.get("has_world_pos", False)
            or (prio_info.get("kind") != "metin" and prio_age >= 0.70)
        )

        # Keep trilateration throttled during walking/combat so movement & attack frames stay smooth
        if not need_urgent:
            if farm_active and in_melee:
                if now - self.last_trilat_t < 0.75:
                    return
            elif farm_active and not in_melee:
                if now - self.last_trilat_t < 0.95:
                    return
            elif now - self.last_trilat_t < 0.35:
                return
        self.last_trilat_t = now

        chr_mod = get_mod("chr")
        player_mod = get_mod("player")
        if chr_mod is None or player_mod is None:
            return

        # Select candidates needing (tx, ty)
        candidates = []
        for vid, info in self.entities.items():
            if info.get("static_locked", False) and info.get("has_world_pos", False):
                continue
            kind = info.get("kind", "npc")
            age = now - info.get("pos_t", 0.0)
            if not info.get("has_world_pos", False):
                pr = -1 if vid == priority_vid else (0 if kind == "metin" else (1 if kind == "boss" else (2 if kind == "monster" else 3)))
                candidates.append((pr, info.get("dist", 99999.0), vid))
            elif vid == priority_vid and age >= 0.45:
                candidates.append((-1, 0.0, vid))
            elif kind in ("boss", "monster", "player") and age >= 0.90:
                candidates.append((2, info.get("dist", 99999.0), vid))

        if not candidates:
            return

        candidates.sort(key=lambda item: (item[0], item[1]))
        batch_vids = [item[2] for item in candidates[:28]]

        get_dist = player_mod.GetCharacterDistance
        d0_map = {}
        for vid in batch_vids:
            try:
                d0 = float(get_dist(vid))
                if 0.0 <= d0 <= 25000.0:
                    d0_map[vid] = d0
            except Exception:
                pass

        if not d0_map:
            return

        ix = int(round(mx))
        iy = int(round(my))
        iz = int(round(mz))
        step = 500
        step_sq = float(step * step)
        inv_2s = 1.0 / float(2 * step)

        d1_map = {}
        d2_map = {}
        try:
            chr_mod.SelectInstance(int(my_vid))
            chr_mod.SetPixelPosition(ix + step, iy, iz)
            for vid in d0_map:
                try:
                    d1_map[vid] = float(get_dist(vid))
                except Exception:
                    pass

            chr_mod.SelectInstance(int(my_vid))
            chr_mod.SetPixelPosition(ix, iy + step, iz)
            for vid in d0_map:
                try:
                    d2_map[vid] = float(get_dist(vid))
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            try:
                chr_mod.SelectInstance(int(my_vid))
                chr_mod.SetPixelPosition(ix, iy, iz)
            except Exception:
                pass

        for vid, d0 in d0_map.items():
            d1 = d1_map.get(vid, -1.0)
            d2 = d2_map.get(vid, -1.0)
            info = self.entities.get(vid)
            if info is None:
                continue
            info["dist"] = d0
            if d1 < 0.0 or d2 < 0.0:
                continue
            dx = (d0 * d0 - d1 * d1 + step_sq) * inv_2s
            dy = (d0 * d0 - d2 * d2 + step_sq) * inv_2s
            tx = float(ix) + dx
            ty = float(iy) + dy
            info["x"] = tx
            info["y"] = ty
            info["has_world_pos"] = True
            info["pos_t"] = now
            if info.get("kind") in ("metin", "npc") and d0 > 5.0:
                info["static_locked"] = True

    def step_screen_projection(self, my_vid, mx, my, mz, now):
        # Combines exact 3D Camera Matrix W2S (grp.GetCameraPosition / GetTargetPosition)
        # with textTail height refinement for on-screen entities
        if now - self.last_w2s_t < 0.04:
            return
        self.last_w2s_t = now

        grp = get_mod("grp")
        wndMgr = get_mod("wndMgr")
        textTail = get_mod("textTail")
        if grp is None:
            return

        wnd_w, wnd_h = 1024, 768
        if wndMgr is not None:
            try:
                wnd_w = max(320, int(wndMgr.GetScreenWidth()))
                wnd_h = max(240, int(wndMgr.GetScreenHeight()))
            except Exception:
                pass

        # Read 3D camera eye and look-at target (0x5e9e10 & 0x5e9ed0)
        ex, ey, ez = 0.0, 0.0, 0.0
        ax, ay, az = 0.0, 0.0, 0.0
        has_cam = False
        try:
            cpos = grp.GetCameraPosition()
            tpos = grp.GetTargetPosition()
            if cpos and tpos and len(cpos) >= 3 and len(tpos) >= 3:
                ex, ey, ez = float(cpos[0]), float(cpos[1]), float(cpos[2])
                ax, ay, az = float(tpos[0]), float(tpos[1]), float(tpos[2])
                has_cam = True
        except Exception:
            has_cam = False

        # Refresh textTail for on-screen height refinement
        tt_pos_fn = getattr(textTail, "GetPosition", None) if textTail is not None else None
        msx, msy = -9999.0, -9999.0
        if textTail is not None and tt_pos_fn is not None:
            try:
                if hasattr(textTail, "UpdateAllTextTail"):
                    textTail.UpdateAllTextTail()
                if hasattr(textTail, "ShowCharacterTextTail"):
                    for vid, info in self.entities.items():
                        if info.get("dist", 99999.0) <= 4500.0 and info.get("kind") != "npc":
                            try:
                                textTail.ShowCharacterTextTail(int(vid))
                            except Exception:
                                pass
                if hasattr(textTail, "UpdateShowingTextTail"):
                    textTail.UpdateShowingTextTail()
                mp = tt_pos_fn(int(my_vid))
                if mp and len(mp) >= 2:
                    msx, msy = float(mp[0]), float(mp[1])
            except Exception:
                pass

        if not has_cam:
            for info in self.entities.values():
                info["on_screen"] = False
            return

        # D3D World Y sign detection: in Metin2 D3D space, wy = -my
        sign_y = 1.0 if abs(ay - my) < abs(ay + my) else -1.0

        # Camera basis vectors (Right-Handed D3D world space: wx=East, wy=North, wz=Up)
        fx = ax - ex
        fy = ay - ey
        fz = az - ez
        flen = math.sqrt(fx * fx + fy * fy + fz * fz)
        if flen < 1e-4:
            return
        fx /= flen
        fy /= flen
        fz /= flen

        # Store 2D map camera forward direction for Radar View Cone
        f2d = math.sqrt(fx * fx + fy * fy)
        if f2d > 1e-4:
            self.cam_dir_x = fx / f2d
            self.cam_dir_y = (fy * sign_y) / f2d

        # Right = normalize(F x Up) where Up = (0, 0, 1) -> (fy, -fx, 0)
        rx = fy
        ry = -fx
        rz = 0.0
        rlen = math.sqrt(rx * rx + ry * ry)
        if rlen < 1e-4:
            return
        rx /= rlen
        ry /= rlen

        # True Up = R x F
        ux = ry * fz - rz * fy
        uy = rz * fx - rx * fz
        uz = rx * fy - ry * fx

        # Metin2 SetPerspective uses fovy = 30.0 deg -> tan(15 deg) = 0.26794919
        tan_half_fov = 0.26794919
        aspect = float(wnd_w) / float(max(1, wnd_h))
        half_w = float(wnd_w) * 0.5
        half_h = float(wnd_h) * 0.5

        for vid, info in self.entities.items():
            # 1. Query native C++ textTail.GetPosition(vid) (0x00530350 -> 0x0052da00), which has ZERO main_vid restriction
            #    and projects pCharacterInstance ([edi + 0x1c]) directly via CScreen::ProjectPosition (0x0059cb60)!
            tt_valid = False
            tsx, tsy, tsz = 0.0, 0.0, 0.0
            if tt_pos_fn is not None:
                try:
                    tp = tt_pos_fn(int(vid))
                    if tp and len(tp) >= 2:
                        tsx, tsy = float(tp[0]), float(tp[1])
                        tsz = float(tp[2]) if len(tp) >= 3 else 0.5
                        if 5.0 < tsx < (wnd_w - 5.0) and 5.0 < tsy < (wnd_h - 5.0) and 0.0 <= tsz <= 1.0:
                            if not (abs(tsx - msx) < 2.5 and abs(tsy - msy) < 2.5 and info.get("dist", 0.0) > 80.0):
                                tt_valid = True
                except Exception:
                    tt_valid = False

            # 2. If entity is on screen in textTail and needs world coordinates (or is a moving monster),
            #    ray-cast (tsx, tsy) onto ground plane + combine with GetCharacterDistance(vid) for zero-SetPixelPosition (x, y)!
            if tt_valid and (not info.get("has_world_pos", False) or (info.get("kind") != "metin" and (now - info.get("pos_t", 0.0) >= 0.35))):
                d0 = float(info.get("dist", 0.0))
                if d0 > 1.0 and (mx != 0.0 or my != 0.0):
                    ndc_tx = (tsx / half_w) - 1.0
                    ndc_ty = 1.0 - (tsy / half_h)
                    ray_x = fx + rx * (ndc_tx * tan_half_fov * aspect) + ux * (ndc_ty * tan_half_fov)
                    ray_y = fy + ry * (ndc_tx * tan_half_fov * aspect) + uy * (ndc_ty * tan_half_fov)
                    ray_z = fz + rz * (ndc_tx * tan_half_fov * aspect) + uz * (ndc_ty * tan_half_fov)
                    wz_est = mz + 100.0
                    if abs(ray_z) > 0.04:
                        t_hit = (wz_est - ez) / ray_z
                        if 50.0 < t_hit < 30000.0:
                            wx_hit = ex + ray_x * t_hit
                            wy_hit = (ey + ray_y * t_hit) * sign_y
                            dx_r = wx_hit - mx
                            dy_r = wy_hit - my
                            r_2d = math.hypot(dx_r, dy_r)
                            if r_2d > 5.0:
                                info["x"] = mx + (dx_r / r_2d) * d0
                                info["y"] = my + (dy_r / r_2d) * d0
                                info["has_world_pos"] = True
                                info["pos_t"] = now

            if not info.get("has_world_pos", False):
                if tt_valid and 16.0 <= tsx <= (wnd_w - 16.0) and 16.0 <= tsy <= (wnd_h - 16.0):
                    info["sx"] = tsx
                    info["sy"] = tsy
                    info["on_screen"] = True
                else:
                    info["on_screen"] = False
                continue

            wx = info["x"]
            wy = sign_y * info["y"]
            wz = mz + (135.0 if info.get("kind") in ("metin", "boss") else 95.0)

            vx = wx - ex
            vy = wy - ey
            vz = wz - ez

            z_cam = vx * fx + vy * fy + vz * fz
            if z_cam <= 60.0:
                info["on_screen"] = False
                continue

            x_cam = vx * rx + vy * ry + vz * rz
            y_cam = vx * ux + vy * uy + vz * uz

            ndc_x = x_cam / (z_cam * tan_half_fov * aspect)
            ndc_y = y_cam / (z_cam * tan_half_fov)

            sx = half_w * (1.0 + ndc_x)
            sy = half_h * (1.0 - ndc_y)

            if tt_valid and abs(tsx - sx) < 180.0 and abs(tsy - sy) < 200.0:
                sx = tsx
                sy = tsy

            if 16.0 <= sx <= (wnd_w - 16.0) and 16.0 <= sy <= (wnd_h - 16.0):
                info["sx"] = sx
                info["sy"] = sy
                info["on_screen"] = True
            else:
                info["on_screen"] = False

    def sync_minimap_waypoints(self, now, enabled=True):
        if now - self.last_minimap_t < 1.0:
            return
        self.last_minimap_t = now
        miniMap = get_mod("miniMap")
        if miniMap is None:
            return
        add_wp = getattr(miniMap, "AddWayPoint", None)
        rem_wp = getattr(miniMap, "RemoveWayPoint", None)
        reg_atlas = getattr(miniMap, "RegisterAtlasWindow", None)
        if add_wp is None or rem_wp is None:
            return
        try:
            if reg_atlas is not None:
                reg_atlas(None)
        except Exception:
            pass

        for old_vid in list(self.pinned_vids):
            try:
                rem_wp(int(old_vid))
            except Exception:
                pass
        self.pinned_vids.clear()

        if not enabled:
            return

        wp_type = getattr(miniMap, "TYPE_TARGET", 1)
        targets = []
        for vid, info in self.entities.items():
            if info.get("kind") in ("metin", "boss") and info.get("has_world_pos", False):
                targets.append((0 if info["kind"] == "metin" else 1, info.get("dist", 99999.0), vid, info))
        targets.sort(key=lambda t: (t[0], t[1]))

        for _, _, vid, info in targets[:10]:
            try:
                add_wp(int(wp_type), str(info["name"]), float(info["x"]), float(info["y"]), "", int(vid))
                self.pinned_vids.add(int(vid))
            except Exception:
                pass

    def step(self, esp_enabled=True, priority_vid=0, farm_active=False, in_melee=False):
        now = time.clock()
        my_vid, mx, my, mz = self.get_player_state()
        if my_vid <= 0:
            return 0, 0.0, 0.0, 0.0
        self.step_scan(my_vid, now)
        self.step_prune_and_distances(my_vid, now)
        self.step_trilaterate(
            my_vid,
            mx,
            my,
            mz,
            now,
            priority_vid=priority_vid,
            farm_active=farm_active,
            in_melee=in_melee,
        )
        if esp_enabled:
            self.step_screen_projection(my_vid, mx, my, mz, now)
        self.sync_minimap_waypoints(now, enabled=esp_enabled)
        return my_vid, mx, my, mz

    def get_counts(self):
        c = {"metin": 0, "boss": 0, "monster": 0, "player": 0, "ore": 0, "npc": 0}
        for info in self.entities.values():
            k = info.get("kind", "npc")
            if k in c:
                c[k] += 1
        return c

    def get_filtered_list(self, mode=None):
        if mode is None:
            mode = self.get_filter_mode()
        res = []
        for info in self.entities.values():
            k = info.get("kind", "npc")
            if mode == "all":
                if k in ("metin", "boss", "monster", "player", "ore"):
                    res.append(info)
            elif mode == "metin_boss":
                if k in ("metin", "boss"):
                    res.append(info)
            elif mode == "metin":
                if k == "metin":
                    res.append(info)
            elif mode == "boss":
                if k == "boss":
                    res.append(info)
            elif mode == "monster":
                if k == "monster":
                    res.append(info)
            elif mode == "ore":
                if k == "ore":
                    res.append(info)
        res.sort(key=lambda item: (
            0 if item["kind"] == "metin" else (1 if item["kind"] == "boss" else (2 if item["kind"] == "ore" else (3 if item["kind"] == "monster" else 4))),
            item.get("dist", 99999.0),
        ))
        return res

    def pick_target(self, farm_mode="all", blacklist=None):
        if blacklist is None:
            blacklist = {}
        now = time.clock()
        best_key = None
        best_info = None
        for vid, info in self.entities.items():
            if blacklist.get(vid, 0.0) > now:
                continue
            k = info.get("kind", "npc")
            if farm_mode == "metin" and k != "metin":
                continue
            if farm_mode == "boss" and k != "boss":
                continue
            if farm_mode == "metin_boss" and k not in ("metin", "boss"):
                continue
            if farm_mode == "ore" and k != "ore":
                continue
            if farm_mode == "all" and k not in ("metin", "boss", "monster"):
                continue
            d = info.get("dist", 99999.0)
            if d < 0.0 or d > 16000.0:
                continue
            prio = 0 if k == "metin" else (1 if k == "boss" else 2)
            key = (prio, d)
            if best_key is None or key < best_key:
                best_key = key
                best_info = info
        return best_info


# ============================================================================
# 2. AUTO-FARM + 360 MELEE CLEAVE / PULL (SAFE 7X ALTERNATIVE) [F6]
# ============================================================================

class AutoFarmer(object):
    FARM_MODES = [
        ("all", "Metin>Boss>Mob"),
        ("metin", "Sadece Metin"),
        ("metin_boss", "Metin+Boss"),
        ("boss", "Sadece Boss"),
        ("ore", "Maden Damari"),
    ]

    ENGAGE_RANGE = 195.0
    KEEP_RANGE = 230.0
    POINT_BLANK_RANGE = 128.0
    MELEE_RANGE = 195.0
    CLEAVE_RANGE = 195.0

    def __init__(self, radar):
        self.radar = radar
        self.enabled = False
        self.mode_idx = 0
        self.target_vid = 0
        self.target_lock_t = 0.0
        self.last_dist = 0.0
        self.last_progress_t = 0.0
        self.last_move_t = 0.0
        self.last_atk_t = 0.0
        self.last_cleave_t = 0.0
        self.last_cape_t = 0.0
        self.last_gap_close_t = 0.0
        self.melee_start_t = 0.0
        self.in_melee = False
        self.cleave_idx = 0
        self.blacklist = {}
        self.state_str = "HAZIR"
        self.nav_req_id = 0
        self.nav_target_vid = 0
        self.nav_req_t = 0.0
        self.nav_points = []
        self.nav_wp_idx = 0

    def get_mode_key(self):
        return self.FARM_MODES[self.mode_idx][0]

    def get_mode_label(self):
        return self.FARM_MODES[self.mode_idx][1]

    def cycle_mode(self):
        self.mode_idx = (self.mode_idx + 1) % len(self.FARM_MODES)
        self.target_vid = 0
        self.in_melee = False
        return self.get_mode_label()

    def set_enabled(self, flag):
        self.enabled = bool(flag)
        if not self.enabled:
            self.stop_actions()
            self.target_vid = 0
            self.in_melee = False
            self.state_str = "KAPALI"
        else:
            self.state_str = "TARANIYOR"

    def stop_actions(self):
        _NATIVE_BRIDGE.set_attack_key_direct(0)
        player = get_mod("player")
        if player is not None:
            if not _NATIVE_BRIDGE.ensure_ready():
                try:
                    player.SetAttackKeyState(0)
                except Exception:
                    pass
            if hasattr(player, "EndKeyWalkingImmediately"):
                try:
                    player.EndKeyWalkingImmediately()
                except Exception:
                    pass
        nav = get_mod("nav")
        if nav is not None and hasattr(nav, "Cancel"):
            try:
                nav.Cancel()
            except Exception:
                pass
        self.nav_req_id = 0
        self.nav_points = []
        self.in_melee = False

    def lock_manual_target(self, vid):
        if vid <= 0:
            return False
        self.target_vid = int(vid)
        now = time.clock()
        self.target_lock_t = now
        self.last_progress_t = now
        self.last_dist = 99999.0
        self.in_melee = False
        self.nav_req_id = 0
        self.nav_points = []
        if not self.enabled:
            self.set_enabled(True)
        return True

    def face_coords(self, my_vid, mx, my, tx, ty):
        chr_mod = get_mod("chr")
        if chr_mod is None or my_vid <= 0:
            return
        dx = tx - mx
        dy = ty - my
        if abs(dx) < 1.0 and abs(dy) < 1.0:
            return

        # CInstanceBase internal rotation (0x0098fb80 table):
        # 0 deg = South (+Y), 90 deg = East (+X), 180 deg = North (-Y), 270 deg = West (-X)
        internal_deg = (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0

        # 8-way direction index (0=N, 1=NE, 2=E, 3=SE, 4=S, 5=SW, 6=W, 7=NW)
        # chr.SetDirection (0x004b8140 -> 0x004abcd0) updates BOTH SetRotation AND m_fAdvancingRotation!
        dir_idx = int(round(((180.0 - internal_deg) % 360.0) / 45.0)) % 8

        # chr.SetRotation (0x004b84a0) adds +180.0 deg at 0x004b84e0 before calling CInstanceBase::SetRotation
        arg_deg = (math.degrees(math.atan2(-dx, -dy)) + 360.0) % 360.0

        # chr.BlendRotation (0x004b6de0) computes fmod(720.0 - blend_deg, 360.0)
        blend_deg = (360.0 - internal_deg) % 360.0

        try:
            chr_mod.SelectInstance(int(my_vid))
            if hasattr(chr_mod, "SetDirection"):
                chr_mod.SetDirection(int(dir_idx))
            if hasattr(chr_mod, "SetRotation"):
                chr_mod.SetRotation(float(arg_deg))
            if hasattr(chr_mod, "BlendRotation"):
                chr_mod.BlendRotation(float(blend_deg), 0.02)
        except Exception:
            pass

    def poll_nav_waypoints(self, mx, my, tx, ty, vid, now):
        nav = get_mod("nav")
        if nav is None or not hasattr(nav, "PreviewToPosition"):
            return tx, ty

        dist_2d = math.hypot(tx - mx, ty - my)
        if dist_2d < 450.0:
            return tx, ty

        if vid != self.nav_target_vid or (now - self.nav_req_t > 2.5):
            try:
                ok = nav.PreviewToPosition(float(tx), float(ty))
                if ok:
                    self.nav_req_id = 1
                    self.nav_target_vid = vid
                    self.nav_req_t = now
                    self.nav_points = []
                    self.nav_wp_idx = 0
            except Exception:
                pass

        if self.nav_req_id > 0 and not self.nav_points and hasattr(nav, "IsPreviewReady"):
            try:
                if int(nav.IsPreviewReady()) == 1 and hasattr(nav, "GetWaypointCount") and hasattr(nav, "GetWaypoint"):
                    cnt = int(nav.GetWaypointCount())
                    pts = []
                    for idx in range(min(cnt, 64)):
                        wp = nav.GetWaypoint(idx)
                        if wp and len(wp) >= 2:
                            pts.append((float(wp[0]), float(wp[1])))
                    if pts:
                        self.nav_points = pts
                        self.nav_wp_idx = 0
            except Exception:
                pass

        if self.nav_points:
            while self.nav_wp_idx < len(self.nav_points):
                wx, wy = self.nav_points[self.nav_wp_idx]
                if math.hypot(wx - mx, wy - my) < 200.0 and self.nav_wp_idx + 1 < len(self.nav_points):
                    self.nav_wp_idx += 1
                else:
                    return wx, wy
        return tx, ty

    def walk_toward(self, my_vid, mx, my, tx, ty, target_vid, now):
        if now - self.last_move_t < 0.22:
            return
        self.last_move_t = now

        player = get_mod("player")
        chr_mod = get_mod("chr")
        net_mod = get_mod("net")

        # Release attack key while walking so MOTION_RUN is not cancelled by attack swings
        _NATIVE_BRIDGE.set_attack_key_direct(0)
        if player is not None and not _NATIVE_BRIDGE.ensure_ready():
            try:
                player.SetAttackKeyState(0)
            except Exception:
                pass

        if target_vid > 0 and _NATIVE_BRIDGE.ensure_ready():
            t_inf = self.radar.entities.get(target_vid)
            iptr = t_inf.get("inst_ptr", 0) if t_inf is not None else 0
            _NATIVE_BRIDGE.reserve_click_actor_native(target_vid, iptr)

        if tx != 0.0 or ty != 0.0:
            wx, wy = self.poll_nav_waypoints(mx, my, tx, ty, target_vid, now)
            dx = wx - mx
            dy = wy - my
            d = math.hypot(dx, dy)
            if d > 1.0:
                self.face_coords(my_vid, mx, my, wx, wy)
                step_len = min(d + 100.0, 600.0)
                sx = int(mx + (dx / d) * step_len)
                sy = int(my + (dy / d) * step_len)
                if target_vid <= 0 and _NATIVE_BRIDGE.ensure_ready():
                    _NATIVE_BRIDGE.reserve_click_ground_native(sx, sy, 0.0)
                if chr_mod is not None and hasattr(chr_mod, "MoveToDestPosition"):
                    try:
                        chr_mod.MoveToDestPosition(int(my_vid), sx, sy)
                    except Exception:
                        pass

        if net_mod is not None and target_vid > 0 and hasattr(net_mod, "SendOnClickPacket"):
            try:
                net_mod.SendOnClickPacket(int(target_vid))
            except Exception:
                pass

    def use_bravery_cape(self, now, force=False):
        if not force and (now - self.last_cape_t < 6.5):
            return False, ""
        self.last_cape_t = now

        def _is_cape(vnum, nm, it, st):
            if vnum in BRAVERY_CAPE_VNUMS or vnum in (72001, 72002, 72003, 76038):
                return True
            if nm and ("pelerin" in nm or "cesaret" in nm or "manto" in nm or "cekici" in nm):
                return True
            return False

        win_t, slot_i, vnum, nm = scan_inventory_for_item(_is_cape, max_slot=1000)
        if slot_i >= 0:
            ok = use_inventory_item(win_t, slot_i)
            if ok:
                return True, "Pelerin kullanildi (%s, Slot %d)" % (nm or str(vnum), slot_i)

        # Fallback when user clicks "Simdi Pelerin Kullan" (force=True) or has no Cape item:
        # Packet Mob Pull (aggro-clicks nearby monsters within 2500 units)
        if force:
            net = get_mod("net")
            player = get_mod("player")
            pulled = 0
            if net is not None and hasattr(net, "SendOnClickPacket"):
                for vid, inf in list(self.radar.entities.items()):
                    if inf.get("kind") in ("monster", "boss") and 0.0 <= inf.get("dist", 99999.0) <= 2500.0:
                        try:
                            if player is not None and hasattr(player, "SetTarget"):
                                player.SetTarget(int(vid))
                            net.SendOnClickPacket(int(vid))
                            pulled += 1
                            if pulled >= 18:
                                break
                        except Exception:
                            pass
            if pulled > 0:
                return True, "Envanterde Pelerin yok -> Paket ile %d canavar cekildi!" % pulled
            return False, "Envanterde Pelerin yok ve yakinda canavar yok!"
        return False, ""

    def execute_melee_attack(self, my_vid, mx, my, target_info, now):
        player = get_mod("player")
        chr_mod = get_mod("chr")
        net = get_mod("net")
        target_vid = int(target_info["vid"])
        tx = target_info.get("x", 0.0)
        ty = target_info.get("y", 0.0)
        dist = target_info.get("dist", 0.0)
        inst_ptr = target_info.get("inst_ptr", 0)

        # Always keep character rotation & advancing rotation locked onto the primary target
        if tx != 0.0 or ty != 0.0:
            self.face_coords(my_vid, mx, my, tx, ty)

        # Ore Vein Mining Mode: click ore vein every 2.2s without holding attack key
        if target_info.get("kind") == "ore":
            _NATIVE_BRIDGE.set_attack_key_direct(0)
            if player is not None and not _NATIVE_BRIDGE.ensure_ready():
                try:
                    player.SetAttackKeyState(0)
                except Exception:
                    pass
            if now - self.last_atk_t >= 2.2:
                self.last_atk_t = now
                _NATIVE_BRIDGE.reserve_click_actor_native(target_vid, inst_ptr)
                if net is not None and hasattr(net, "SendOnClickPacket"):
                    try:
                        net.SendOnClickPacket(target_vid)
                    except Exception:
                        pass
            return

        # Drive 100% native CPythonPlayer::__ReserveClickActor (0x004fb590) + m_pkInstPick
        if _NATIVE_BRIDGE.ensure_ready():
            _NATIVE_BRIDGE.reserve_click_actor_native(target_vid, inst_ptr)
            _NATIVE_BRIDGE.set_actor_speeds_native(1.38, 1.35)
        elif player is not None and hasattr(player, "SetTarget"):
            try:
                player.SetTarget(target_vid)
            except Exception:
                pass

        # Micro gap-close if target is above POINT_BLANK_RANGE (128 units)
        if dist > self.POINT_BLANK_RANGE and (tx != 0.0 or ty != 0.0) and (now - self.last_gap_close_t >= 0.45):
            self.last_gap_close_t = now
            dx = tx - mx
            dy = ty - my
            d = math.hypot(dx, dy)
            if d > 1.0 and chr_mod is not None:
                if not _NATIVE_BRIDGE.ensure_ready() and dist > 148.0 and hasattr(chr_mod, "SetPixelPosition"):
                    nx = int(round(mx + (dx / d) * 28.0))
                    ny = int(round(my + (dy / d) * 28.0))
                    try:
                        chr_mod.SelectInstance(int(my_vid))
                        chr_mod.SetPixelPosition(nx, ny, 0)
                    except Exception:
                        pass
                if hasattr(chr_mod, "MoveToDestPosition"):
                    sx = int(round(mx + (dx / d) * (d + 110.0)))
                    sy = int(round(my + (dy / d) * (d + 110.0)))
                    try:
                        chr_mod.MoveToDestPosition(int(my_vid), sx, sy)
                    except Exception:
                        pass

        # Cycle target lock across nearby mobs in melee range while keeping primary facing
        if now - self.last_cleave_t >= 0.24:
            self.last_cleave_t = now
            near_mobs = [target_info]
            for vid, inf in self.radar.entities.items():
                if vid != target_vid and inf.get("kind") in ("monster", "boss", "metin"):
                    if 0.0 <= inf.get("dist", 9999.0) <= self.CLEAVE_RANGE:
                        near_mobs.append(inf)

            self.cleave_idx = (self.cleave_idx + 1) % len(near_mobs)
            focus = near_mobs[self.cleave_idx]
            if (tx == 0.0 and ty == 0.0) and focus.get("has_world_pos", False):
                self.face_coords(my_vid, mx, my, focus["x"], focus["y"])

            if net is not None and hasattr(net, "SendOnClickPacket"):
                try:
                    net.SendOnClickPacket(int(focus["vid"]))
                except Exception:
                    pass

        if now - self.last_atk_t >= 0.14:
            self.last_atk_t = now
            # Direct m_isAtkKey (+0xB8) write via EncWrite_B (0x006dc0a0) skips RascalGate (0x006ccc90)!
            if _NATIVE_BRIDGE.ensure_ready():
                _NATIVE_BRIDGE.set_attack_key_direct(1)
                if player is not None and hasattr(player, "SetMouseFunc") and hasattr(player, "SetMouseState"):
                    try:
                        mbt_l = getattr(player, "MBT_LEFT", 0)
                        mbf_a = getattr(player, "MBF_AUTO", 2)
                        mbs_p = getattr(player, "MBS_PRESS", 1)
                        player.SetMouseFunc(mbt_l, mbf_a)
                        player.SetMouseState(mbt_l, mbs_p)
                    except Exception:
                        pass
            elif player is not None:
                try:
                    player.SetAttackKeyState(1)
                except Exception:
                    pass
                if hasattr(player, "ComboAttack"):
                    try:
                        player.ComboAttack()
                    except Exception:
                        pass
            if net is not None and hasattr(net, "SendOnClickPacket"):
                try:
                    net.SendOnClickPacket(target_vid)
                except Exception:
                    pass

        # Auto-pull mobs when farming monsters or metin stones
        if self.get_mode_key() in ("all", "metin"):
            self.use_bravery_cape(now, force=False)

    def step(self, my_vid, mx, my):
        if not self.enabled or my_vid <= 0:
            return
        now = time.clock()
        player = get_mod("player")

        # Validate current target and drop dead/dying corpses immediately
        cur = self.radar.entities.get(self.target_vid) if self.target_vid > 0 else None
        if cur is not None and cur.get("kind") != "metin" and player is not None and hasattr(player, "CanAttackInstance"):
            try:
                if int(player.CanAttackInstance(int(self.target_vid))) == 0:
                    self.blacklist[self.target_vid] = now + 8.0
                    self.radar.entities.pop(self.target_vid, None)
                    cur = None
            except Exception:
                pass

        # Dynamic closer-target & higher-priority switching while walking
        if cur is not None and cur.get("dist", 0.0) > self.KEEP_RANGE:
            better = self.radar.pick_target(self.get_mode_key(), self.blacklist)
            if better is not None and int(better["vid"]) != self.target_vid:
                k_cur = cur.get("kind", "monster")
                k_bet = better.get("kind", "monster")
                p_cur = 0 if k_cur == "metin" else (1 if k_cur == "boss" else 2)
                p_bet = 0 if k_bet == "metin" else (1 if k_bet == "boss" else 2)
                if p_bet < p_cur or (p_bet == p_cur and better.get("dist", 99999.0) + 180.0 < cur.get("dist", 99999.0)):
                    cur = better
                    self.target_vid = int(better["vid"])
                    self.target_lock_t = now
                    self.last_progress_t = now
                    self.last_dist = better.get("dist", 99999.0)
                    self.in_melee = False

        if cur is None:
            self.target_vid = 0
            self.in_melee = False
            picked = self.radar.pick_target(self.get_mode_key(), self.blacklist)
            if picked is None and self.get_mode_key() != "all":
                # Fallback to all combat targets if specialized mode (Metin/Boss/Ore) has 0 targets nearby
                picked = self.radar.pick_target("all", self.blacklist)
            if picked is None:
                self.state_str = "TARANIYOR (%s)" % self.get_mode_label()
                self.stop_actions()
                return
            self.target_vid = int(picked["vid"])
            self.target_lock_t = now
            self.last_progress_t = now
            self.last_dist = picked.get("dist", 99999.0)
            cur = picked

        # Ensure locked target has world coordinates immediately on first lock frame
        if not cur.get("has_world_pos", False):
            self.radar.step_trilaterate(
                my_vid,
                mx,
                my,
                0.0,
                now,
                priority_vid=self.target_vid,
                farm_active=True,
                in_melee=False,
            )

        dist = cur.get("dist", 99999.0)
        tx = cur.get("x", 0.0)
        ty = cur.get("y", 0.0)

        # Hysteresis between ENGAGE_RANGE (185) and KEEP_RANGE (215) prevents walk/attack stutter at 2m
        threshold = self.KEEP_RANGE if self.in_melee else self.ENGAGE_RANGE

        if dist > threshold:
            self.in_melee = False
            if abs(self.last_dist - dist) > 25.0:
                self.last_dist = dist
                self.last_progress_t = now
            elif now - self.last_progress_t > 4.5:
                self.blacklist[self.target_vid] = now + 12.0
                log_msg("Target stuck timeout VID=%d dist=%.0f -> blacklisted 12s" % (self.target_vid, dist))
                self.target_vid = 0
                self.stop_actions()
                return

            self.state_str = "GIDILIYOR: %s (%.1fm)" % (cur.get("name", "Hedef")[:15], dist / 100.0)
            self.walk_toward(my_vid, mx, my, tx, ty, self.target_vid, now)
        else:
            if not self.in_melee:
                self.in_melee = True
                self.melee_start_t = now
                if player is not None and hasattr(player, "EndKeyWalkingImmediately"):
                    try:
                        player.EndKeyWalkingImmediately()
                    except Exception:
                        pass
            elif cur.get("kind") == "monster" and (now - self.melee_start_t > 12.0):
                # Drop unreachable/bugged mob after 12.0s in melee (CanAttackInstance==0 already drops dead mobs immediately)
                self.blacklist[self.target_vid] = now + 8.0
                self.target_vid = 0
                self.in_melee = False
                return

            self.last_progress_t = now
            self.state_str = "KESILIYOR: %s (%.1fm)" % (cur.get("name", "Hedef")[:15], dist / 100.0)
            self.execute_melee_attack(my_vid, mx, my, cur, now)


# ============================================================================
# 3. AUTO-PICKUP + SVSIDE CAPTCHA SOLVER [F7]
# ============================================================================

class LootAndCaptchaManager(object):
    def __init__(self):
        self.enabled = True
        self.last_pick_t = 0.0
        self.solved_count = 0
        self.last_code = "-"
        self.hooked_game = False

    def step_pickup(self, now):
        if not self.enabled or now - self.last_pick_t < 0.16:
            return
        self.last_pick_t = now
        player = get_mod("player")
        net = get_mod("net")

        # CPythonPlayer::PickCloseItem (0x004ffc10 -> 0x004fabb0) directly calls
        # CPythonItem::GetCloseItem (0x004c0590) + CPythonPlayer::SendClickItemPacket (0x004f8000)!
        if player is not None and hasattr(player, "PickCloseItem"):
            try:
                player.PickCloseItem()
            except Exception:
                pass

        # If NativeEngineBridge is active, also traverse CPythonItem::m_GroundItemInstanceMap
        if _NATIVE_BRIDGE.ensure_ready():
            try:
                g_items = _NATIVE_BRIDGE.scan_ground_items(0.0, 0.0, 99999.0)
                pl = _NATIVE_BRIDGE.get_player_ptr()
                for _, item_vid, _, _ in g_items[:4]:
                    if pl:
                        _NATIVE_BRIDGE.write_u32_plain(pl + 0xF7E4, item_vid)
                    if player is not None and hasattr(player, "SendClickItemPacket"):
                        player.SendClickItemPacket(int(item_vid))
                    if net is not None and hasattr(net, "SendItemPickUpPacket"):
                        net.SendItemPickUpPacket(int(item_vid))
            except Exception:
                pass

    def parse_and_reply_svside(self, text):
        if not text:
            return False
        s = str(text)
        low = s.lower()
        if "svside" not in low and "dogrulama" not in low and "captcha" not in low and "bot kontrol" not in low:
            return False

        # Match 4-6 digit code after colon/brackets or standalone
        m = re.search(r"(?:kod|code|dogrulama|svside)[^\d]{0,20}(\d{4,6})", low)
        if not m:
            m = re.search(r"\b(\d{4,6})\b", s)
        if not m:
            return False

        code = m.group(1)
        if code == self.last_code:
            return False
        self.last_code = code
        self.solved_count += 1

        net = get_mod("net")
        if net is not None and hasattr(net, "SendChatPacket"):
            try:
                net.SendChatPacket(str(code))
            except Exception:
                pass
        log_msg("SvSide captcha solved: %s" % code)
        chat_notice("SvSide Dogrulama Cozuldu: %s" % code)
        return True

    def install_chat_hook(self):
        if self.hooked_game:
            return
        game_mod = get_mod("game")
        if game_mod is None or not hasattr(game_mod, "GameWindow"):
            return
        gw = game_mod.GameWindow
        orig_append = getattr(gw, "OnRecvWhisper", None)
        if orig_append is not None and not getattr(gw, "_avr_whisper_hooked", False):
            mgr = self

            def hooked_whisper(self_gw, mode, name, line):
                try:
                    mgr.parse_and_reply_svside(line)
                except Exception:
                    pass
                return orig_append(self_gw, mode, name, line)

            try:
                gw.OnRecvWhisper = hooked_whisper
                gw._avr_whisper_hooked = True
                self.hooked_game = True
            except Exception:
                pass

    def step(self):
        now = time.clock()
        self.install_chat_hook()
        self.step_pickup(now)


# ============================================================================
# 4. SUSTAINABILITY: AUTO-POTION / ELIXIR / MOUNT / SKILL BUFF / REVIVE [F8]
# ============================================================================

class SustainManager(object):
    def __init__(self):
        self.enabled = True
        self.hp_threshold = 78
        self.sp_threshold = 45
        self.last_pot_t = 0.0
        self.last_elixir_t = 0.0
        self.last_buff_t = 0.0
        self.last_revive_t = 0.0
        self.ever_saw_positive_hp = False
        self.dead_since_t = 0.0
        self.last_pos_x = 0.0
        self.last_pos_y = 0.0

    def use_first_matching_item(self, vnum_set):
        win_t, slot_i, _, _ = scan_inventory_for_item(lambda v, nm, it, st: v in vnum_set, max_slot=1000)
        if slot_i >= 0:
            return use_inventory_item(win_t, slot_i)
        return False

    def step(self, mx=0.0, my=0.0, combat_active=False):
        if not self.enabled:
            return
        now = time.clock()
        player = get_mod("player")
        if player is None:
            return

        # 1. HP / SP check (in Avrasya2 STATUS: 1=LEVEL, 5=HP, 6=MAX_HP, 7=SP, 8=MAX_SP)
        hp_cur, hp_max, sp_cur, sp_max = 0, 0, 0, 0
        char_lvl = 1
        try:
            char_lvl = int(player.GetStatus(1))
            hp_cur = int(player.GetStatus(getattr(player, "HP", 5)))
            hp_max = int(player.GetStatus(getattr(player, "MAX_HP", 6)))
            sp_cur = int(player.GetStatus(getattr(player, "SP", 7)))
            sp_max = int(player.GetStatus(getattr(player, "MAX_SP", 8)))
        except Exception:
            pass

        if now - self.last_pot_t >= 0.25:
            self.last_pot_t = now
            if hp_max > 0 and 0 < hp_cur < hp_max and (hp_cur * 100.0 / hp_max) < self.hp_threshold:
                self.use_first_matching_item(HP_POTION_VNUMS)
            if sp_max > 0 and 0 < sp_cur < sp_max and (sp_cur * 100.0 / sp_max) < self.sp_threshold:
                self.use_first_matching_item(SP_POTION_VNUMS)

        # 2. Elixir / Dew refresh every 180s ONLY when actively farming/fighting
        if combat_active and (now - self.last_elixir_t >= 180.0):
            self.last_elixir_t = now
            self.use_first_matching_item(ELIXIR_DEW_VNUMS)

        # 3. Skill Buffs (slots 1..6) every 15s ONLY if character is Level >= 5 AND skill is actually learned (grade >= 1 or level >= 2)
        if combat_active and char_lvl >= 5 and (now - self.last_buff_t >= 15.0):
            self.last_buff_t = now
            is_active = getattr(player, "IsSkillActive", None)
            is_cool = getattr(player, "IsSkillCoolTime", None)
            get_grade = getattr(player, "GetSkillGrade", None)
            get_lvl = getattr(player, "GetSkillLevel", None)
            click_skill = getattr(player, "ClickSkillSlot", None)
            if click_skill is not None:
                for s_idx in range(1, 7):
                    try:
                        if is_active is not None and int(is_active(s_idx)) == 1:
                            continue
                        if is_cool is not None and int(is_cool(s_idx)) == 1:
                            continue
                        sk_grade = int(get_grade(s_idx)) if get_grade is not None else 0
                        sk_lvl = int(get_lvl(s_idx)) if get_lvl is not None else 0
                        # Unlearned skills at Level 5 before choosing doctrine report grade=0, level=1; require grade>=1 or level>=2
                        if sk_grade <= 0 and sk_lvl <= 1:
                            continue
                        sk_vnum = int(player.GetSkillIndex(s_idx)) if hasattr(player, "GetSkillIndex") else 0
                        if sk_vnum in (3, 4, 19, 34, 63, 64, 65, 78, 79, 94, 95, 96, 110, 111, 175):
                            click_skill(s_idx)
                            break
                    except Exception:
                        pass


# ============================================================================
# 5. REMOTE BIYOLOG / QUEST HELPER / JUNK GEAR FILTER [F9]
# ============================================================================

class BiyologAndJunkManager(object):
    def __init__(self):
        self.enabled = False
        self.last_bio_t = 0.0
        self.last_quest_t = 0.0

    def send_biyolog_packet(self):
        net = get_mod("net")
        player = get_mod("player")
        if net is None or not hasattr(net, "SendChatPacket"):
            return
        # Check if player holds any Biyolog material or send remote biyolog command
        has_mat = False
        if player is not None and hasattr(player, "GetItemIndex"):
            for slot in range(180):
                try:
                    if int(player.GetItemIndex(slot)) in BIYOLOG_MATERIAL_VNUMS:
                        has_mat = True
                        break
                except Exception:
                    pass
        try:
            net.SendChatPacket("/biyolog")
            if has_mat:
                net.SendChatPacket("/biyolog_ver")
        except Exception:
            pass

    def sell_junk_items(self):
        player = get_mod("player")
        net = get_mod("net")
        item = get_mod("item")
        shop = get_mod("shop")
        if player is None or net is None:
            return 0, "Moduller hazir degil"
        get_vnum = getattr(player, "GetItemIndex", None)
        get_attr = getattr(player, "GetItemAttribute", None)
        sell_pkt = getattr(net, "SendShopSellPacketNew", getattr(net, "SendShopSellPacket", None))
        if get_vnum is None or sell_pkt is None:
            return 0, "Satis fonksiyonu bulunamadi"

        junk_slots = []
        for slot in range(180):
            try:
                vnum = int(get_vnum(slot))
                if vnum <= 0 or vnum in BIYOLOG_MATERIAL_VNUMS or vnum in HP_POTION_VNUMS or vnum in SP_POTION_VNUMS:
                    continue
                if item is not None and hasattr(item, "SelectItem"):
                    item.SelectItem(vnum)
                    itype = int(item.GetItemType()) if hasattr(item, "GetItemType") else 0
                    # Only consider weapon (1) or armor (2) below +6
                    if itype not in (1, 2):
                        continue
                if (vnum % 10) >= 6:
                    continue
                valuable = False
                if get_attr is not None:
                    for a_idx in range(5):
                        at, av = get_attr(slot, a_idx)
                        if int(at) in VALUABLE_ATTRIBUTE_MIN and int(av) >= VALUABLE_ATTRIBUTE_MIN[int(at)]:
                            valuable = True
                            break
                if not valuable:
                    junk_slots.append(slot)
            except Exception:
                pass

        if not junk_slots:
            return 0, "Envanterde satilacak +6 alti cop ekipman yok."

        # Check if NPC Shop window is open (server rejects SendShopSellPacketNew unless shop is open)
        if shop is not None and hasattr(shop, "IsOpen"):
            try:
                if int(shop.IsOpen()) == 0:
                    return 0, "Satis icin once bir NPC Market acin! (%d cop esya hazir)" % len(junk_slots)
            except Exception:
                pass

        sold = 0
        for slot in junk_slots:
            try:
                try:
                    sell_pkt(slot, 1, 1)
                except TypeError:
                    try:
                        sell_pkt(slot, 1)
                    except TypeError:
                        sell_pkt(slot)
                sold += 1
            except Exception:
                pass
        return sold, "Cop Ekipman Satisi Tamamlandi (%d esya satildi)" % sold

    def step(self):
        if not self.enabled:
            return
        now = time.clock()
        if now - self.last_bio_t >= 45.0:
            self.last_bio_t = now
            self.send_biyolog_packet()


# ============================================================================
# 6. CAMERA ZOOM UNLOCK + FOG CLEAR + FPS BOOST [F10]
# ============================================================================

class CameraAndFpsBoost(object):
    PRESETS = [
        (5500.0, False, "Zoom 5500 + Sis Kapali"),
        (8500.0, True, "Zoom 8500 + FPS Boost"),
        (11500.0, True, "Ultra Zoom 11500 + Max FPS"),
    ]

    def __init__(self):
        self.enabled = False
        self.preset_idx = 0
        self.last_apply_t = 0.0

    def get_preset_label(self):
        return self.PRESETS[self.preset_idx][2]

    def cycle_preset(self):
        self.preset_idx = (self.preset_idx + 1) % len(self.PRESETS)
        if self.enabled:
            self.apply_now(force_camera_jump=True)
        return self.get_preset_label()

    def set_enabled(self, flag):
        self.enabled = bool(flag)
        if self.enabled:
            self.apply_now(force_camera_jump=True)
        else:
            self.restore_defaults()

    def apply_now(self, force_camera_jump=False):
        self.last_apply_t = time.clock()
        target_dist, fps_boost, _ = self.PRESETS[self.preset_idx]

        constInfo = get_mod("constInfo")
        if constInfo is not None:
            try:
                setattr(constInfo, "CAMERA_MAX_DISTANCE", 12500.0)
                setattr(constInfo, "CAMERA_MAX_DISTANCE_LONG", 12500.0)
            except Exception:
                pass

        app = get_mod("app")
        if app is not None:
            try:
                if hasattr(app, "SetCameraMaxDistance"):
                    app.SetCameraMaxDistance(12500.0)
                if hasattr(app, "SetMinFog"):
                    app.SetMinFog(30000.0)
                if force_camera_jump and hasattr(app, "GetCamera") and hasattr(app, "SetCamera"):
                    cam = app.GetCamera()
                    if cam and len(cam) >= 4:
                        _, pitch, rot, height = float(cam[0]), float(cam[1]), float(cam[2]), float(cam[3])
                        app.SetCamera(float(target_dist), max(32.0, pitch), rot, height)
            except Exception:
                pass

        bg = get_mod("background")
        if bg is not None:
            try:
                if hasattr(bg, "SetFogMode"):
                    bg.SetFogMode(0)
                if hasattr(bg, "SetRenderTree"):
                    bg.SetRenderTree(0 if fps_boost else 1)
                if hasattr(bg, "SetVisiblePart"):
                    # initBackground (0x004b1900): PART_OBJECT=1, PART_CLOUD=2, PART_WATER=3, PART_TREE=4, PART_SKY=5
                    part_tree = getattr(bg, "PART_TREE", 4)
                    part_cloud = getattr(bg, "PART_CLOUD", 2)
                    bg.SetVisiblePart(part_tree, 0 if fps_boost else 1)
                    bg.SetVisiblePart(part_cloud, 0 if fps_boost else 1)
            except Exception:
                pass

    def restore_defaults(self):
        app = get_mod("app")
        if app is not None:
            try:
                if hasattr(app, "SetCameraMaxDistance"):
                    app.SetCameraMaxDistance(2500.0)
                if hasattr(app, "GetCamera") and hasattr(app, "SetCamera"):
                    cam = app.GetCamera()
                    if cam and len(cam) >= 4:
                        _, pitch, rot, height = float(cam[0]), float(cam[1]), float(cam[2]), float(cam[3])
                        app.SetCamera(2500.0, pitch, rot, height)
            except Exception:
                pass
        bg = get_mod("background")
        if bg is not None:
            try:
                if hasattr(bg, "SetRenderTree"):
                    bg.SetRenderTree(1)
                if hasattr(bg, "SetVisiblePart"):
                    bg.SetVisiblePart(getattr(bg, "PART_TREE", 4), 1)
                    bg.SetVisiblePart(getattr(bg, "PART_CLOUD", 2), 1)
            except Exception:
                pass

    def step(self):
        if not self.enabled:
            return
        if time.clock() - self.last_apply_t >= 0.8:
            self.apply_now(force_camera_jump=False)


# ============================================================================
# 6B. NINJA DUAL-DAGGER ATTACK ANIMATION TRANSFORMER [F11]
# ============================================================================

class NinjaAnimManager(object):
    """
    Transforms the main character's client-side attack animation and weapon motion mode
    into Ninja Dual-Dagger (MOTION_MODE_DUALHAND_SWORD = 4) without sinking into the map
    or freezing ComboAttack:
      - Follows CInstanceBase::Create (0x004a01c0..0x004a02db) exact sequence:
        SetRace -> immediate SetPixelPosition(mx, my, mz) -> SetArmor -> SetWeapon ->
        SetMotionMode(4) -> SetLoopMotion(1) -> Refresh() -> SetPixelPosition(mx, my, mz).
      - Never sets motion_mode=4 on a non-Ninja race (which lacks dualhand_sword .msa
        in CRaceData and freezes ComboAttack).
    """

    PRESETS = [
        # (race_vnum, armor_vnum, weapon_vnum, motion_mode, label)
        (1, 11409, 1139, 4, "Ninja Cift Hancer (K)"),
        (5, 11409, 1139, 4, "Ninja Cift Hancer (E)"),
        (1, 11499, 4049, 4, "Ninja Siyah Ruzgar (K)"),
        (-1, 0, 0, 0, "Kendi Karakterin Hizli Kombo"),
    ]

    def __init__(self):
        self.enabled = False
        self.preset_idx = 0
        self.applied = False
        self.last_vid = 0
        self.last_apply_t = 0.0
        self.last_mode_t = 0.0
        self.pause_until_t = 0.0
        self.orig_race = None
        self.orig_armor = 0
        self.orig_weapon = 0

    def get_preset_label(self):
        return self.PRESETS[self.preset_idx][4]

    def cycle_preset(self):
        self.preset_idx = (self.preset_idx + 1) % len(self.PRESETS)
        self.applied = False
        if self.enabled and self.last_vid > 0:
            self.apply_ninja(self.last_vid, force=True)
        return self.get_preset_label()

    def set_enabled(self, flag, my_vid=0):
        self.enabled = bool(flag)
        vid = my_vid if my_vid > 0 else self.last_vid
        if self.enabled:
            self.applied = False
            if vid > 0:
                self.apply_ninja(vid, force=True)
        else:
            if vid > 0:
                self.restore_original(vid)

    def pause_for_skill(self, my_vid, duration=0.65):
        # Temporarily restore original race during class skill casting so Warrior/Sura .msa MotionEvent fires
        if not self.enabled or my_vid <= 0:
            return
        race_vnum, _, _, _, _ = self.PRESETS[self.preset_idx]
        if race_vnum >= 0 and self.orig_race is not None and race_vnum != self.orig_race:
            self.pause_until_t = time.clock() + float(duration)
            self.restore_original(my_vid)

    def _get_player_coords(self):
        player = get_mod("player")
        if player is not None and hasattr(player, "GetMainCharacterPosition"):
            try:
                pos = player.GetMainCharacterPosition()
                if pos and len(pos) >= 3:
                    return float(pos[0]), float(pos[1]), float(pos[2])
                elif pos and len(pos) >= 2:
                    return float(pos[0]), float(pos[1]), 0.0
            except Exception:
                pass
        return 0.0, 0.0, 0.0

    def _get_current_race(self, my_vid):
        chr_mod = get_mod("chr")
        if chr_mod is not None and hasattr(chr_mod, "GetRace"):
            try:
                chr_mod.SelectInstance(int(my_vid))
                r = int(chr_mod.GetRace())
                if 0 <= r <= 8:
                    return r
            except Exception:
                pass
        player = get_mod("player")
        if player is not None and hasattr(player, "GetRace"):
            try:
                r = int(player.GetRace())
                if 0 <= r <= 8:
                    return r
            except Exception:
                pass
        return -1

    def _get_native_motion_mode(self):
        # Detect exact C++ CRaceMotionData mode from equipped weapon subtype:
        # Unarmed=1, Sword(0)=2, TwoHand(3)=3, Dagger(1)=4, Bow(2)=5, Bell(4)=6, Fan(5)=7
        self._refresh_equipped_gear()
        if self.orig_weapon <= 0:
            return 1  # MOTION_MODE_GENERAL (Unarmed/Fist)
        _, it, st, _, _ = get_item_meta(self.orig_weapon)
        if it == 1:
            if st == 0:
                return 2  # MOTION_MODE_ONEHAND_SWORD
            if st == 1:
                return 4  # MOTION_MODE_DUALHAND_SWORD
            if st == 2:
                return 5  # MOTION_MODE_BOW
            if st == 3:
                return 3  # MOTION_MODE_TWOHAND_SWORD
            if st == 4:
                return 6  # MOTION_MODE_BELL
            if st == 5:
                return 7  # MOTION_MODE_FAN
        return 2          # MOTION_MODE_ONEHAND_SWORD

    def _refresh_equipped_gear(self):
        player = get_mod("player")
        if player is None or not hasattr(player, "GetItemIndex"):
            return
        eq_win = getattr(player, "EQUIPMENT", 2)
        armor_v = 0
        weapon_v = 0
        # EQUIPMENT_BODY = 90 (0x5a), COSTUME_SLOT_BODY = 109 (0x6d)
        for slot_cand in (109, 90):
            try:
                v = int(player.GetItemIndex(slot_cand))
                if v > 0:
                    armor_v = v
                    break
            except Exception:
                pass
        if armor_v <= 0:
            try:
                armor_v = int(player.GetItemIndex(eq_win, 0))
            except Exception:
                armor_v = 0
        # EQUIPMENT_WEAPON = 94 (0x5e), COSTUME_SLOT_WEAPON = 114 (0x72)
        for slot_cand in (114, 94):
            try:
                v = int(player.GetItemIndex(slot_cand))
                if v > 0:
                    weapon_v = v
                    break
            except Exception:
                pass
        if weapon_v <= 0:
            try:
                weapon_v = int(player.GetItemIndex(eq_win, 4))
            except Exception:
                weapon_v = 0
        if armor_v > 0 or self.orig_armor == 0:
            self.orig_armor = max(0, armor_v)
        if weapon_v > 0 or self.orig_weapon == 0:
            self.orig_weapon = max(0, weapon_v)

    def _capture_original(self, my_vid):
        if self.orig_race is None:
            r = self._get_current_race(my_vid)
            if r < 0 or r > 8:
                r = 0
            self.orig_race = r
        self._refresh_equipped_gear()

    def _is_mounting_horse(self):
        player = get_mod("player")
        if player is not None and hasattr(player, "IsMountingHorse"):
            try:
                return int(player.IsMountingHorse()) == 1
            except Exception:
                pass
        return False

    def apply_ninja(self, my_vid, force=False):
        if my_vid <= 0:
            return False
        chr_mod = get_mod("chr")
        if chr_mod is None or not hasattr(chr_mod, "SetRace"):
            return False

        mx, my, mz = self._get_player_coords()
        if abs(mx) < 1.0 and abs(my) < 1.0:
            return False
        ix = int(round(mx))
        iy = int(round(my))
        iz = int(round(mz))

        self._capture_original(my_vid)
        race_vnum, armor_vnum, weapon_vnum, motion_mode, _ = self.PRESETS[self.preset_idx]
        target_race = self.orig_race if (race_vnum < 0 and self.orig_race is not None) else max(0, race_vnum)
        target_armor = self.orig_armor if armor_vnum <= 0 else armor_vnum
        if target_race in (1, 5) and (self.orig_race not in (1, 5) or target_armor <= 0):
            target_armor = armor_vnum if armor_vnum > 0 else 11409
        target_weapon = self.orig_weapon if weapon_vnum <= 0 else weapon_vnum
        if target_race in (1, 5) and target_weapon <= 0:
            target_weapon = 1139
        target_mm = self._get_native_motion_mode() if motion_mode <= 0 else motion_mode

        try:
            chr_mod.SelectInstance(int(my_vid))
            cur_race = self._get_current_race(my_vid)

            if force or cur_race != target_race:
                chr_mod.SelectInstance(int(my_vid))
                chr_mod.SetRace(int(target_race))
                # Immediately restore world position after SetRace zeros m_v3Position (0x0059f630)
                if hasattr(chr_mod, "SetPixelPosition"):
                    chr_mod.SetPixelPosition(ix, iy, iz)

            # ALWAYS call SetArmor (even if target_armor == 0) so CInstanceBase loads the 3D body skeleton!
            if hasattr(chr_mod, "SetArmor"):
                chr_mod.SetArmor(int(max(0, target_armor)))
            elif hasattr(chr_mod, "ChangeShape"):
                chr_mod.ChangeShape(int(max(0, target_armor)))
                if hasattr(chr_mod, "SetPixelPosition"):
                    chr_mod.SetPixelPosition(ix, iy, iz)

            if hasattr(chr_mod, "SetWeapon"):
                chr_mod.SetWeapon(int(max(0, target_weapon)))
            if hasattr(chr_mod, "SetMotionMode"):
                chr_mod.SetMotionMode(int(target_mm))
            _NATIVE_BRIDGE.set_actor_speeds_native(1.38, 1.35)
            if hasattr(chr_mod, "SetAttackSpeed"):
                try:
                    chr_mod.SetAttackSpeed(1.35)
                except Exception:
                    pass
            if hasattr(chr_mod, "SetMoveSpeed"):
                try:
                    chr_mod.SetMoveSpeed(1.35)
                except Exception:
                    pass
            if hasattr(chr_mod, "SetLoopMotion"):
                chr_mod.SetLoopMotion(1)
            if hasattr(chr_mod, "Refresh"):
                chr_mod.Refresh()
            if hasattr(chr_mod, "testSetComboType"):
                chr_mod.testSetComboType(1)
            if hasattr(chr_mod, "SetPixelPosition"):
                chr_mod.SetPixelPosition(ix, iy, iz)

            self.applied = True
            self.last_vid = int(my_vid)
            self.last_apply_t = time.clock()
            self.last_mode_t = self.last_apply_t
            return True
        except Exception as e:
            log_msg("apply_ninja err: " + str(e), "ERROR")
            return False

    def restore_original(self, my_vid):
        if my_vid <= 0:
            return
        chr_mod = get_mod("chr")
        if chr_mod is None:
            return
        mx, my, mz = self._get_player_coords()
        ix = int(round(mx))
        iy = int(round(my))
        iz = int(round(mz))
        try:
            chr_mod.SelectInstance(int(my_vid))
            orig_r = self.orig_race if self.orig_race is not None else 0
            if hasattr(chr_mod, "SetRace"):
                chr_mod.SetRace(int(orig_r))
                if hasattr(chr_mod, "SetPixelPosition") and (ix != 0 or iy != 0):
                    chr_mod.SetPixelPosition(ix, iy, iz)
            if hasattr(chr_mod, "SetArmor"):
                chr_mod.SetArmor(int(max(0, self.orig_armor)))
            elif hasattr(chr_mod, "ChangeShape"):
                chr_mod.ChangeShape(int(max(0, self.orig_armor)))
                if hasattr(chr_mod, "SetPixelPosition") and (ix != 0 or iy != 0):
                    chr_mod.SetPixelPosition(ix, iy, iz)
            if hasattr(chr_mod, "SetWeapon"):
                chr_mod.SetWeapon(int(max(0, self.orig_weapon)))
            if hasattr(chr_mod, "SetMotionMode"):
                chr_mod.SetMotionMode(self._get_native_motion_mode() if self.orig_weapon > 0 else 1)
            _NATIVE_BRIDGE.set_actor_speeds_native(1.25, 1.25)
            if hasattr(chr_mod, "SetAttackSpeed"):
                try:
                    chr_mod.SetAttackSpeed(1.25)
                except Exception:
                    pass
            if hasattr(chr_mod, "SetMoveSpeed"):
                try:
                    chr_mod.SetMoveSpeed(1.25)
                except Exception:
                    pass
            if hasattr(chr_mod, "SetLoopMotion"):
                chr_mod.SetLoopMotion(1)
            if hasattr(chr_mod, "Refresh"):
                chr_mod.Refresh()
            if hasattr(chr_mod, "SetPixelPosition") and (ix != 0 or iy != 0):
                chr_mod.SetPixelPosition(ix, iy, iz)
            self.applied = False
        except Exception:
            pass

    def step(self, my_vid):
        if my_vid <= 0:
            return
        if my_vid != self.last_vid:
            self.last_vid = int(my_vid)
            self.applied = False

        if not self.enabled:
            if self.applied:
                self.restore_original(my_vid)
            return

        now = time.clock()
        if self.pause_until_t > now:
            return

        # Pause Ninja skeleton while mounted on horse so horse riding animations work normally
        if self._is_mounting_horse():
            if self.applied:
                self.restore_original(my_vid)
            return

        mx, my, _ = self._get_player_coords()
        if abs(mx) < 1.0 and abs(my) < 1.0:
            return

        race_vnum, _, _, motion_mode, _ = self.PRESETS[self.preset_idx]
        target_race = self.orig_race if (race_vnum < 0 and self.orig_race is not None) else max(0, race_vnum)
        target_mm = self._get_native_motion_mode() if motion_mode <= 0 else motion_mode
        cur_race = self._get_current_race(my_vid)

        if not self.applied or (cur_race >= 0 and cur_race != target_race):
            self.apply_ninja(my_vid, force=not self.applied)
            return

        # Lightweight motion-mode lock every 1.5s without touching SetRace/SetArmor or position
        if now - self.last_mode_t >= 1.5:
            self.last_mode_t = now
            chr_mod = get_mod("chr")
            if chr_mod is not None:
                try:
                    chr_mod.SelectInstance(int(my_vid))
                    if hasattr(chr_mod, "SetMotionMode"):
                        chr_mod.SetMotionMode(int(target_mm))
                    if hasattr(chr_mod, "testSetComboType"):
                        chr_mod.testSetComboType(1)
                except Exception:
                    pass


# ============================================================================
# 6C. 360 SNAP & BLINK WAITHACK + COMBO/KNOCKBACK/SKILL EXPLOITS [F12]
# ============================================================================

class WaithackAndCombatManager(object):
    """
    1. 360 Target-Lock & Melee-Step Waithack:
       - Mode 0 (350.0 units = 3.5m 360 Lock): Locks onto the closest alive target within
         3.5m, steps into point-blank melee contact (85 units in front of target) via
         MoveToDestPosition + SetPixelPosition, and stays locked on that target until it
         dies while swinging continuously (SetAttackKeyState(1) + ComboAttack()) and
         cleave-clicking surrounding mobs within 190 units.
       - Mode 1 (600.0 units = 6.0m Blink-Lock): Extends target acquisition to 6.0m and
         syncs movement into melee contact so every swing's C++ hit frame (0.38s-0.50s)
         transmits genuine SendAttackPacket (0x004fbeb0 -> 0x004cd6b0).
    2. Anti-Fall / No-Knockback (Sekmeme / Yere Dusmeme):
       - Stabilizes position only when an external knockback spike (> 135 units) occurs,
         never interrupting normal attack swings.
    3. 4th-Hit Knockback Cancel (4. Vurus Iptali - Infinite 1-2-3 Combo):
       - Resets combo cycle before the 4th swing so monsters are never knocked out of range.
    4. No-Cast Delay Moving Skill (Animasyonsuz Skill):
       - Automatically selects nearest target if none is selected, temporarily restores
         native race if NinjaAnim is active, casts learned skills, and cancels post-cast
         freeze after SendUseSkillPacket is transmitted.
    """

    MODES = [
        (350.0, False, "3.5m 360 Lock (Guvenli)"),
        (600.0, True, "6.0m Blink-Lock (Genis)"),
    ]

    def __init__(self, radar, farmer, ninja_anim=None):
        self.radar = radar
        self.farmer = farmer
        self.ninja_anim = ninja_anim
        self.waithack_enabled = False
        self.mode_idx = 0
        self.no_knockback = True
        self.cancel_4th_hit = True
        self.no_skill_delay = True
        self.last_wh_t = 0.0
        self.last_wh_step_t = 0.0
        self.last_wh_cleave_t = 0.0
        self.last_combo_reset_t = 0.0
        self.last_antifall_t = 0.0
        self.wh_target_vid = 0
        self.wh_target_lock_t = 0.0
        self.wh_cursor = 0
        self.anchor_pos = None
        self.snap_hold_until = 0.0
        self.last_stable_x = 0.0
        self.last_stable_y = 0.0
        self.last_stable_z = 0.0
        self.skill_queue = []
        self.last_skill_pop_t = 0.0
        self.pending_skill_cancel_t = 0.0
        self.pending_shield_reequip_t = 0.0

    def get_mode_label(self):
        return self.MODES[self.mode_idx][2]

    def cycle_mode(self):
        self.mode_idx = (self.mode_idx + 1) % len(self.MODES)
        return self.get_mode_label()

    def set_waithack(self, flag, my_vid=0):
        self.waithack_enabled = bool(flag)
        if not self.waithack_enabled:
            _NATIVE_BRIDGE.set_attack_key_direct(0)
            player = get_mod("player")
            if player is not None and not _NATIVE_BRIDGE.ensure_ready() and hasattr(player, "SetAttackKeyState"):
                try:
                    player.SetAttackKeyState(0)
                except Exception:
                    pass
            self.wh_target_vid = 0
            self.anchor_pos = None
            self.snap_hold_until = 0.0

    def _is_shield_item(self, vnum, nm, it, st):
        if 13000 <= vnum <= 13399:
            return True
        if it == 2 and st == 2:
            return True
        if nm and "kalkan" in nm:
            return True
        return False

    def trigger_shield_antistun(self):
        player = get_mod("player")
        net = get_mod("net")
        if player is None or net is None or not hasattr(net, "SendItemUsePacket"):
            return False
        # 1. Check if a shield exists in inventory (0..999) to swap/equip immediately
        win_t, inv_slot, inv_vnum, inv_nm = scan_inventory_for_item(self._is_shield_item, max_slot=1000)

        # 2. Check equipped shield at EQUIPMENT_SHIELD = 100 (0x64) or (EQUIPMENT=2, cell=10)
        eq_vnum = 0
        eq_win = getattr(player, "EQUIPMENT", 2)
        try:
            eq_vnum = int(player.GetItemIndex(100))
        except Exception:
            eq_vnum = 0
        if eq_vnum <= 0:
            try:
                eq_vnum = int(player.GetItemIndex(eq_win, 10))
            except Exception:
                eq_vnum = 0

        try:
            if eq_vnum > 0 and inv_slot >= 0:
                use_inventory_item(win_t, inv_slot)
                use_inventory_item(win_t, inv_slot)
                return True
            elif eq_vnum > 0:
                net.SendItemUsePacket(100)
                self.pending_shield_reequip_t = time.clock() + 0.14
                return True
            elif inv_slot >= 0:
                use_inventory_item(win_t, inv_slot)
                return True
        except Exception:
            pass
        return False

    def _ensure_combat_target_selected(self):
        player = get_mod("player")
        net = get_mod("net")
        if player is None:
            return 0
        cur_tvid = 0
        if hasattr(player, "GetTargetVID"):
            try:
                cur_tvid = int(player.GetTargetVID())
            except Exception:
                cur_tvid = 0
        if cur_tvid > 0:
            return cur_tvid

        # Pick nearest combat target from radar and lock it so offensive skills can fire
        best_vid = 0
        best_d = 99999.0
        for vid, inf in self.radar.entities.items():
            if inf.get("kind") in ("monster", "boss", "metin"):
                d = inf.get("dist", 99999.0)
                if 0.0 <= d < best_d:
                    best_d = d
                    best_vid = int(vid)
        if best_vid > 0:
            try:
                if hasattr(player, "SetTarget"):
                    player.SetTarget(best_vid)
                if net is not None and hasattr(net, "SendOnClickPacket"):
                    net.SendOnClickPacket(best_vid)
            except Exception:
                pass
        return best_vid

    def cast_skill_instant(self, slot_idx, my_vid):
        player = get_mod("player")
        if player is None or not hasattr(player, "ClickSkillSlot"):
            return False
        try:
            self._ensure_combat_target_selected()
            if self.ninja_anim is not None:
                self.ninja_anim.pause_for_skill(my_vid, duration=0.70)
            player.ClickSkillSlot(int(slot_idx))
            if self.no_skill_delay:
                # Delay SetLoopMotion(1) by 0.42s so C++ .msa MotionEvent transmits SendUseSkillPacket first!
                self.pending_skill_cancel_t = time.clock() + 0.42
            return True
        except Exception:
            return False

    def queue_skills_1_to_6(self, my_vid):
        player = get_mod("player")
        if player is None:
            return 0, "Oyuncu modulu hazir degil"

        learned = []
        ready = []
        for s_i in range(1, 7):
            sk_idx = 0
            sk_lvl = 0
            cool = 0
            try:
                if hasattr(player, "GetSkillIndex"):
                    sk_idx = int(player.GetSkillIndex(s_i))
                if hasattr(player, "GetSkillLevel"):
                    sk_lvl = int(player.GetSkillLevel(s_i))
                if hasattr(player, "IsSkillCoolTime"):
                    cool = int(player.IsSkillCoolTime(s_i))
            except Exception:
                pass
            if sk_idx > 0 and sk_lvl > 0:
                learned.append(s_i)
                if cool == 0:
                    ready.append(s_i)

        # If GetSkillLevel returns 0 across 1..6 (e.g. skills not learned yet or custom skill table),
        # check if any skill index > 0 is registered and try those
        if not learned:
            for s_i in range(1, 7):
                try:
                    sk_idx = int(player.GetSkillIndex(s_i)) if hasattr(player, "GetSkillIndex") else 0
                    if sk_idx > 0:
                        cool = int(player.IsSkillCoolTime(s_i)) if hasattr(player, "IsSkillCoolTime") else 0
                        if cool == 0:
                            ready.append(s_i)
                except Exception:
                    pass

        if not ready and not learned:
            return 0, "Karakterde henuz ogrenilmis aktif beceri (Skill 1-6) yok!"
        if not ready and learned:
            return 0, "Tum beceriler su an dolum suresinde (Cooldown)!"

        for s_i in ready:
            if s_i not in self.skill_queue:
                self.skill_queue.append(s_i)

        if self.skill_queue:
            first_s = self.skill_queue.pop(0)
            self.last_skill_pop_t = time.clock()
            self.cast_skill_instant(first_s, my_vid)
        return len(ready), "%d aktif beceri sirayla tetikleniyor!" % len(ready)

    def step(self, my_vid, mx, my, mz):
        if my_vid <= 0 or (abs(mx) < 1.0 and abs(my) < 1.0):
            return
        now = time.clock()
        chr_mod = get_mod("chr")
        player = get_mod("player")
        net = get_mod("net")
        if chr_mod is None or player is None:
            return

        # Complete pending 1-tick shield re-equip after unequip packet
        if self.pending_shield_reequip_t > 0.0 and now >= self.pending_shield_reequip_t:
            self.pending_shield_reequip_t = 0.0
            win_t, inv_slot, _, _ = scan_inventory_for_item(self._is_shield_item, max_slot=1000)
            if inv_slot >= 0:
                use_inventory_item(win_t, inv_slot)

        # Process queued skills (0.50s spacing so each skill's MotionEvent packet fires cleanly)
        if self.skill_queue and (now - self.last_skill_pop_t >= 0.50):
            self.last_skill_pop_t = now
            nxt_s = self.skill_queue.pop(0)
            self.cast_skill_instant(nxt_s, my_vid)

        # Cancel skill post-cast recovery freeze 0.42s after ClickSkillSlot
        if self.pending_skill_cancel_t > 0.0 and now >= self.pending_skill_cancel_t:
            self.pending_skill_cancel_t = 0.0
            if self.no_skill_delay and hasattr(chr_mod, "SetLoopMotion"):
                try:
                    chr_mod.SelectInstance(int(my_vid))
                    chr_mod.SetLoopMotion(1)
                except Exception:
                    pass

        ix = int(round(mx))
        iy = int(round(my))
        iz = int(round(mz))

        # 1. Anti-Fall / No-Knockback stabilization (ONLY on sudden knockback displacement > 135 units)
        if self.no_knockback and (self.farmer.in_melee or self.waithack_enabled):
            if self.last_stable_x != 0.0 or self.last_stable_y != 0.0:
                disp = math.hypot(mx - self.last_stable_x, my - self.last_stable_y)
                if 135.0 <= disp <= 380.0 and (now - self.last_antifall_t >= 0.30):
                    self.last_antifall_t = now
                    try:
                        chr_mod.SelectInstance(int(my_vid))
                        if hasattr(chr_mod, "SetPixelPosition"):
                            chr_mod.SetPixelPosition(int(round(self.last_stable_x)), int(round(self.last_stable_y)), iz)
                            mx, my = self.last_stable_x, self.last_stable_y
                            ix, iy = int(round(mx)), int(round(my))
                    except Exception:
                        pass
                else:
                    self.last_stable_x, self.last_stable_y, self.last_stable_z = mx, my, mz
            else:
                self.last_stable_x, self.last_stable_y, self.last_stable_z = mx, my, mz
        else:
            self.last_stable_x, self.last_stable_y, self.last_stable_z = mx, my, mz

        # 2. 4th-Hit Knockback Cancel (Infinite 1-2-3 Combo without scattering mobs)
        if self.cancel_4th_hit and (self.farmer.in_melee or self.waithack_enabled):
            if now - self.last_combo_reset_t >= 1.15:
                self.last_combo_reset_t = now
                try:
                    chr_mod.SelectInstance(int(my_vid))
                    if hasattr(chr_mod, "testSetComboType"):
                        chr_mod.testSetComboType(1)
                except Exception:
                    pass

        # 3. 360 Target-Lock & Server-Synced Melee-Step Waithack
        if not self.waithack_enabled or (now - self.last_wh_t < 0.14):
            return
        self.last_wh_t = now

        max_range, blink_sync, _ = self.MODES[self.mode_idx]

        # Validate current locked Waithack target so we don't switch targets mid-swing!
        t_info = self.radar.entities.get(self.wh_target_vid) if self.wh_target_vid > 0 else None
        if t_info is not None:
            if t_info.get("dist", 99999.0) > max_range + 100.0 or (now - self.wh_target_lock_t > 6.0):
                t_info = None
            elif t_info.get("kind") != "metin" and hasattr(player, "CanAttackInstance"):
                try:
                    if int(player.CanAttackInstance(int(self.wh_target_vid))) == 0:
                        self.radar.entities.pop(self.wh_target_vid, None)
                        t_info = None
                except Exception:
                    pass

        if t_info is None:
            targets = []
            for vid, info in self.radar.entities.items():
                if info.get("kind") in ("metin", "boss", "monster"):
                    d = info.get("dist", 99999.0)
                    if 0.0 <= d <= max_range:
                        if info.get("kind") != "metin" and hasattr(player, "CanAttackInstance"):
                            try:
                                if int(player.CanAttackInstance(int(vid))) == 0:
                                    continue
                            except Exception:
                                pass
                        targets.append(info)

            if not targets:
                self.wh_target_vid = 0
                _NATIVE_BRIDGE.set_attack_key_direct(0)
                if not _NATIVE_BRIDGE.ensure_ready():
                    try:
                        player.SetAttackKeyState(0)
                    except Exception:
                        pass
                return

            targets.sort(key=lambda inf: (0 if inf["kind"] == "metin" else (1 if inf["kind"] == "boss" else 2), inf.get("dist", 9999.0)))
            t_info = targets[0]
            self.wh_target_vid = int(t_info["vid"])
            self.wh_target_lock_t = now

        tvid = int(t_info["vid"])
        t_inst_ptr = int(t_info.get("inst_ptr", 0))
        tdist = float(t_info.get("dist", 0.0))
        if hasattr(player, "GetCharacterDistance"):
            try:
                live_d = float(player.GetCharacterDistance(tvid))
                if live_d >= 0.0:
                    tdist = live_d
                    t_info["dist"] = live_d
            except Exception:
                pass

        has_pos = bool(t_info.get("has_world_pos", False))
        pos_age = now - float(t_info.get("pos_t", 0.0))

        if not has_pos or (t_info.get("kind") != "metin" and pos_age >= 0.70):
            self.radar.step_trilaterate(my_vid, mx, my, mz, now, priority_vid=tvid, farm_active=False, in_melee=False)
            has_pos = bool(t_info.get("has_world_pos", False))

        tx = float(t_info.get("x", 0.0))
        ty = float(t_info.get("y", 0.0))
        dx = tx - mx
        dy = ty - my
        dlen = math.hypot(dx, dy) if has_pos else tdist

        walk_dist = max(tdist, dlen) + 110.0
        snap_dist = max(0.0, dlen - 85.0)
        if has_pos and dlen >= 1.0:
            wx = int(round(mx + (dx / dlen) * walk_dist))
            wy = int(round(my + (dy / dlen) * walk_dist))
            sx = int(round(mx + (dx / dlen) * snap_dist))
            sy = int(round(my + (dy / dlen) * snap_dist))
        else:
            wx, wy = ix, iy
            sx, sy = ix, iy

        in_live_client = ("app" in sys.modules)
        try:
            if has_pos and dlen >= 1.0:
                self.farmer.face_coords(my_vid, mx, my, tx, ty)

            if _NATIVE_BRIDGE.ensure_ready():
                _NATIVE_BRIDGE.reserve_click_actor_native(tvid, t_inst_ptr)
                _NATIVE_BRIDGE.set_actor_speeds_native(1.38, 1.35)
            elif hasattr(player, "SetTarget"):
                try:
                    player.SetTarget(tvid)
                except Exception:
                    pass

            if net is not None and hasattr(net, "SendOnClickPacket"):
                try:
                    net.SendOnClickPacket(tvid)
                except Exception:
                    pass

            if not in_live_client:
                if hasattr(chr_mod, "MoveToDestPosition"):
                    chr_mod.MoveToDestPosition(int(my_vid), sx, sy)
                if hasattr(chr_mod, "SetPixelPosition"):
                    chr_mod.SelectInstance(int(my_vid))
                    chr_mod.SetPixelPosition(sx, sy, iz)
                player.SetAttackKeyState(1)
                if hasattr(player, "ComboAttack"):
                    player.ComboAttack()
                return

            if tdist > 215.0:
                _NATIVE_BRIDGE.set_attack_key_direct(0)
                if has_pos and dlen >= 1.0 and (now - self.last_wh_step_t >= 0.22):
                    self.last_wh_step_t = now
                    if hasattr(chr_mod, "MoveToDestPosition"):
                        try:
                            chr_mod.MoveToDestPosition(int(my_vid), wx, wy)
                        except Exception:
                            pass
                return

            if tdist > 125.0 and has_pos and dlen >= 1.0 and (now - self.last_wh_step_t >= 0.44):
                self.last_wh_step_t = now
                if hasattr(chr_mod, "MoveToDestPosition"):
                    try:
                        chr_mod.MoveToDestPosition(int(my_vid), wx, wy)
                    except Exception:
                        pass

            # Cleave-click secondary mobs within 195 units every 0.22s while keeping primary facing
            if now - self.last_wh_cleave_t >= 0.22:
                self.last_wh_cleave_t = now
                near_vids = [tvid]
                for vid, inf in self.radar.entities.items():
                    if vid != tvid and inf.get("kind") in ("monster", "boss", "metin"):
                        if 0.0 <= inf.get("dist", 9999.0) <= 195.0:
                            near_vids.append(int(vid))
                if len(near_vids) > 1 and net is not None and hasattr(net, "SendOnClickPacket"):
                    self.wh_cursor = (self.wh_cursor + 1) % len(near_vids)
                    try:
                        net.SendOnClickPacket(near_vids[self.wh_cursor])
                    except Exception:
                        pass

            if _NATIVE_BRIDGE.ensure_ready():
                _NATIVE_BRIDGE.set_attack_key_direct(1)
                if hasattr(player, "SetMouseFunc") and hasattr(player, "SetMouseState"):
                    try:
                        mbt_l = getattr(player, "MBT_LEFT", 0)
                        mbf_a = getattr(player, "MBF_AUTO", 2)
                        mbs_p = getattr(player, "MBS_PRESS", 1)
                        player.SetMouseFunc(mbt_l, mbf_a)
                        player.SetMouseState(mbt_l, mbs_p)
                    except Exception:
                        pass
            else:
                try:
                    player.SetAttackKeyState(1)
                except Exception:
                    pass
                if hasattr(player, "ComboAttack"):
                    try:
                        player.ComboAttack()
                    except Exception:
                        pass
        finally:
            if not in_live_client:
                try:
                    if hasattr(chr_mod, "SetPixelPosition"):
                        chr_mod.SelectInstance(int(my_vid))
                        chr_mod.SetPixelPosition(ix, iy, iz)
                except Exception:
                    pass
                self.anchor_pos = None
                self.snap_hold_until = 0.0


# ============================================================================
# 6D. WORLD EXPLOITS: WALLHACK / OBJECT REMOVER / CLICK-BLINK / GHOST MODE
# ============================================================================

class WorldExploitManager(object):
    def __init__(self):
        self.wallhack_objects = False
        self.alt_click_blink = True
        self.ghost_mode_active = False
        self.last_blink_t = 0.0
        self.last_wall_t = 0.0
        self.last_phase_t = 0.0
        self.last_phase_x = 0.0
        self.last_phase_y = 0.0
        self.stuck_since_t = 0.0

    def set_wallhack_objects(self, flag):
        self.wallhack_objects = bool(flag)
        bg = get_mod("background")
        if bg is not None and hasattr(bg, "SetVisiblePart"):
            try:
                # Proven from initBackground (0x004b1900): PART_OBJECT = 1, PART_TREE = 4
                part_obj = getattr(bg, "PART_OBJECT", 1)
                part_tree = getattr(bg, "PART_TREE", 4)
                bg.SetVisiblePart(part_obj, 0 if self.wallhack_objects else 1)
                bg.SetVisiblePart(part_tree, 0 if self.wallhack_objects else 1)
                if hasattr(bg, "SetRenderTree"):
                    bg.SetRenderTree(0 if self.wallhack_objects else 1)
            except Exception:
                pass

    def trigger_ghost_walk(self, my_vid):
        if my_vid <= 0:
            return False
        chr_mod = get_mod("chr")
        player = get_mod("player")
        if chr_mod is None:
            return False
        self.ghost_mode_active = not self.ghost_mode_active
        try:
            chr_mod.SelectInstance(int(my_vid))
            if self.ghost_mode_active:
                # If character is dead (HP <= 0), revive client actor into Ghost state
                hp_cur = 100
                if player is not None and hasattr(player, "GetStatus"):
                    try:
                        hp_cur = int(player.GetStatus(getattr(player, "HP", 1)))
                    except Exception:
                        hp_cur = 100
                if hp_cur <= 0 and hasattr(chr_mod, "Revive"):
                    chr_mod.Revive()
                    if hasattr(chr_mod, "SetLoopMotion"):
                        chr_mod.SetLoopMotion(1)
                # Apply semi-transparent ghost visual so user sees Ghost Walk is active
                if hasattr(chr_mod, "SetBlendRenderMode"):
                    try:
                        chr_mod.SetBlendRenderMode(int(my_vid), 0.55)
                    except Exception:
                        pass
            else:
                if hasattr(chr_mod, "SetBlendRenderMode"):
                    try:
                        chr_mod.SetBlendRenderMode(int(my_vid), 1.0)
                    except Exception:
                        pass
            return True
        except Exception:
            return False

    def blink_to_coords(self, my_vid, mx, my, mz, tx, ty):
        if my_vid <= 0 or (abs(tx) < 1.0 and abs(ty) < 1.0):
            return False
        chr_mod = get_mod("chr")
        if chr_mod is None:
            return False
        dx = tx - mx
        dy = ty - my
        dist = math.hypot(dx, dy)
        if dist < 10.0:
            return False
        # Server-Synced Blink:
        # 1) Nudge SetPixelPosition by at most 85 units FIRST to clear local wall/tree/gate collision,
        # 2) Call MoveToDestPosition(my_vid, nx, ny) 280 units ahead SECOND so C++ starts walking
        #    from (sx, sy) -> (nx, ny) and transmits genuine SendCharacterStatePacket to the server!
        step_len = min(dist, 280.0)
        px_step = min(dist * 0.40, 85.0)
        nx = int(round(mx + (dx / dist) * step_len))
        ny = int(round(my + (dy / dist) * step_len))
        sx = int(round(mx + (dx / dist) * px_step))
        sy = int(round(my + (dy / dist) * px_step))
        iz = int(round(mz))
        try:
            chr_mod.SelectInstance(int(my_vid))
            if hasattr(chr_mod, "SetPixelPosition"):
                chr_mod.SetPixelPosition(sx, sy, iz)
            if hasattr(chr_mod, "MoveToDestPosition"):
                chr_mod.MoveToDestPosition(int(my_vid), nx, ny)
            return True
        except Exception:
            return False

    def blink_to_cursor(self, my_vid, mx, my, mz):
        bg = get_mod("background")
        if bg is not None and hasattr(bg, "GetPickingPoint"):
            try:
                pt = bg.GetPickingPoint()
                if pt and len(pt) >= 2:
                    px, py = abs(float(pt[0])), abs(float(pt[1]))
                    if px > 1.0 or py > 1.0:
                        if self.blink_to_coords(my_vid, mx, my, mz, px, py):
                            return True
            except Exception:
                pass
        # Fallback when clicking the GUI button (where cursor is over UI window):
        # blink 280 units forward along camera look direction!
        grp = get_mod("grp")
        if grp is not None and hasattr(grp, "GetCameraPosition") and hasattr(grp, "GetTargetPosition"):
            try:
                cpos = grp.GetCameraPosition()
                tpos = grp.GetTargetPosition()
                if cpos and tpos and len(cpos) >= 2 and len(tpos) >= 2:
                    fx = float(tpos[0]) - float(cpos[0])
                    fy = abs(float(tpos[1])) - abs(float(cpos[1]))
                    flen = math.hypot(fx, fy)
                    if flen > 0.1:
                        tx = mx + (fx / flen) * 280.0
                        ty = my + (fy / flen) * 280.0
                        return self.blink_to_coords(my_vid, mx, my, mz, tx, ty)
            except Exception:
                pass
        return False

    def _step_phase_through_walls(self, my_vid, mx, my, mz, now):
        # NEVER interrupt normal W/A/S/D walking on open ground!
        # Only phase when the user holds W/A/S/D and is physically blocked by a wall/gate/obstacle
        # (displacement < 12 units over 0.55s), then nudge 45 units + MoveToDestPosition with 0.85s cooldown.
        if now - self.last_phase_t < 0.85:
            return
        app = get_mod("app")
        chr_mod = get_mod("chr")
        if app is None or chr_mod is None or not hasattr(app, "IsPressed"):
            return
        try:
            ip = app.IsPressed
            w_dn = bool(ip(getattr(app, "DIK_W", 17)) or ip(getattr(app, "DIK_UP", 200)))
            s_dn = bool(ip(getattr(app, "DIK_S", 31)) or ip(getattr(app, "DIK_DOWN", 208)))
            a_dn = bool(ip(getattr(app, "DIK_A", 30)) or ip(getattr(app, "DIK_LEFT", 203)))
            d_dn = bool(ip(getattr(app, "DIK_D", 32)) or ip(getattr(app, "DIK_RIGHT", 205)))
            if not (w_dn or s_dn or a_dn or d_dn):
                self.stuck_since_t = 0.0
                self.last_phase_x, self.last_phase_y = mx, my
                return

            disp = math.hypot(mx - self.last_phase_x, my - self.last_phase_y)
            if disp >= 12.0 or (self.last_phase_x == 0.0 and self.last_phase_y == 0.0):
                # Character is moving normally via C++ SetSingleDIKKeyState -> do NOT interfere!
                self.last_phase_x, self.last_phase_y = mx, my
                self.stuck_since_t = now
                return

            if self.stuck_since_t <= 0.0:
                self.stuck_since_t = now
                return
            if now - self.stuck_since_t < 0.55:
                return

            self.last_phase_t = now
            self.stuck_since_t = now
            self.last_phase_x, self.last_phase_y = mx, my

            chr_mod.SelectInstance(int(my_vid))
            rot_deg = float(chr_mod.GetRotation()) if hasattr(chr_mod, "GetRotation") else 0.0
            rad = math.radians(rot_deg)
            vx = math.sin(rad)
            vy = math.cos(rad)
            px_step = 48.0
            walk_len = 185.0
            sx = int(round(mx + vx * px_step))
            sy = int(round(my + vy * px_step))
            nx = int(round(mx + vx * walk_len))
            ny = int(round(my + vy * walk_len))
            iz = int(round(mz))
            if hasattr(chr_mod, "SetPixelPosition"):
                chr_mod.SetPixelPosition(sx, sy, iz)
            if hasattr(chr_mod, "MoveToDestPosition"):
                chr_mod.MoveToDestPosition(int(my_vid), nx, ny)
        except Exception:
            pass

    def step(self, my_vid, mx, my, mz):
        now = time.clock()
        if self.wallhack_objects and (now - self.last_wall_t >= 2.0):
            self.last_wall_t = now
            self.set_wallhack_objects(True)

        if (self.wallhack_objects or self.ghost_mode_active) and my_vid > 0:
            self._step_phase_through_walls(my_vid, mx, my, mz, now)

        if self.alt_click_blink and my_vid > 0 and (now - self.last_blink_t >= 0.22):
            app = get_mod("app")
            if app is not None and hasattr(app, "IsPressed"):
                try:
                    alt_down = bool(
                        app.IsPressed(getattr(app, "DIK_LALT", 56))
                        or app.IsPressed(getattr(app, "DIK_RALT", 184))
                    )
                    c_down = bool(app.IsPressed(getattr(app, "DIK_C", 46)))
                    if alt_down and c_down:
                        self.last_blink_t = now
                        if self.blink_to_cursor(my_vid, mx, my, mz):
                            chat_notice("[ALT+C] Imlec Noktasina Blink Yapildi")
                except Exception:
                    pass


# ============================================================================
# 6E. PACKET & ECONOMY EXPLOITS: REMOTE REFINE / OFFLINESHOP / QUEST / EFSUN
# ============================================================================

class EconomyExploitManager(object):
    def __init__(self, radar=None):
        self.radar = radar
        self.fast_quest_skip = False
        self.efsun_bot_enabled = False
        self.target_avg_dmg = 45
        self.last_quest_t = 0.0
        self.last_efsun_t = 0.0
        self.efsun_count = 0
        self.pending_refine = None
        self.pending_safebox_pull_t = 0.0

    def _find_blacksmith_vid(self):
        if self.radar is not None:
            best_vid = 0
            best_d = 999999.0
            for vid, inf in self.radar.entities.items():
                vnum = int(inf.get("vnum", 0))
                nm = normalize_tr_ascii(inf.get("name", ""))
                if vnum in (20016, 20044, 20045, 20046, 20074) or ("demirci" in nm):
                    d = float(inf.get("dist", 99999.0))
                    if d < best_d:
                        best_d = d
                        best_vid = int(vid)
            if best_vid > 0:
                return best_vid
        return 0

    def remote_refine_slot0(self, refine_type=0):
        net = get_mod("net")
        player = get_mod("player")
        if net is None or not hasattr(net, "SendRefinePacket"):
            return False, "Paket modulu hazir degil"
        target_slot = 0
        target_vnum = 0
        if player is not None and hasattr(player, "GetItemIndex"):
            try:
                v0 = int(player.GetItemIndex(0))
                if v0 > 0:
                    target_slot = 0
                    target_vnum = v0
                else:
                    # Find first weapon/armor in inventory if Slot 0 is empty
                    for s in range(1, 90):
                        vs = int(player.GetItemIndex(s))
                        if vs > 0:
                            _, it, _, _, _ = get_item_meta(vs)
                            if it in (1, 2):
                                target_slot = s
                                target_vnum = vs
                                break
            except Exception:
                target_slot = 0

        item_nm = "Slot %d" % (target_slot + 1)
        if target_vnum > 0:
            nm, _, _, _, _ = get_item_meta(target_vnum)
            if nm:
                item_nm = "%s (Slot %d)" % (nm, target_slot + 1)

        try:
            # 1) If refine_type == 1 (Kutsama/Metal), apply scroll to target_slot first, then send SendRefinePacket 0.24s later!
            if int(refine_type) > 0 and hasattr(net, "SendItemUseToItemPacket"):
                def _is_scroll(vnum, nm, it, st):
                    if vnum in (25040, 25041, 71032, 39014, 71025, 71026):
                        return True
                    if nm and ("kutsama" in nm or "buyulu metal" in nm or "rituel" in nm or "demirci" in nm):
                        return True
                    return False
                win_t, sc_slot, sc_vnum, sc_nm = scan_inventory_for_item(_is_scroll, max_slot=1000)
                if sc_slot >= 0:
                    try:
                        if win_t is not None and win_t != 1:
                            net.SendItemUseToItemPacket(int(win_t), int(sc_slot), 1, int(target_slot))
                        else:
                            net.SendItemUseToItemPacket(int(sc_slot), int(target_slot))
                    except TypeError:
                        net.SendItemUseToItemPacket(int(sc_slot), int(target_slot))
                    if "app" in sys.modules:
                        self.pending_refine = (time.clock() + 0.24, int(target_slot), int(refine_type))
                        return True, "%s uzerine %s uygulandi ve +Bas gonderiliyor!" % (item_nm, sc_nm or "Kutsama")
                    else:
                        net.SendRefinePacket(int(target_slot), int(refine_type))
                        return True, "%s +Bas gonderildi" % item_nm
                else:
                    # No scroll in inventory -> fall through to Blacksmith GiveItem + Refine
                    refine_type = 0

            # 2) Blacksmith Refine (refine_type == 0):
            # Server clears ch->m_pkChrRefineNPC after EVERY single upgrade (+0->+1)!
            # To upgrade +1->+2->+3 continuously, first send SendGiveItemPacket(blacksmith_vid, 1, target_slot, 1)
            # to re-open the server refine session, then fire SendRefinePacket(target_slot, 0) 0.24s later!
            bs_vid = self._find_blacksmith_vid()
            if bs_vid > 0 and hasattr(net, "SendGiveItemPacket") and ("app" in sys.modules):
                try:
                    try:
                        net.SendGiveItemPacket(int(bs_vid), 1, int(target_slot), 1)
                    except TypeError:
                        net.SendGiveItemPacket(int(bs_vid), int(target_slot), 1)
                    self.pending_refine = (time.clock() + 0.24, int(target_slot), 0)
                    return True, "%s Demirciye (VID:%d) verildi ve +Bas yapiliyor!" % (item_nm, bs_vid)
                except Exception:
                    pass

            net.SendRefinePacket(int(target_slot), int(refine_type))
            return True, "%s icin Uzaktan Demirci +Bas paketi gonderildi!" % item_nm
        except Exception:
            return False, "+Bas paketi gonderilemedi"

    def _execute_safebox_valute_withdraw(self):
        offshop = get_mod("offlineshop")
        if offshop is None or not hasattr(offshop, "SendSafeboxGetValutes"):
            return
        # Never spam 10 descending packets in a burst (server disconnects on invalid/excessive safebox packets!).
        # Instead, read the exact balance received by GetOfflineshopBoard().ShopSafebox_SetValutes(valute).
        val = int(getattr(self, "_last_safebox_valute", 0))
        if val > 0:
            self._last_safebox_valute = 0
            try:
                offshop.SendSafeboxGetValutes(int(val))
                chat_notice("[OfflineShop] Pazar kasasindan %d Yang cekildi!" % val)
            except Exception:
                pass
        else:
            chat_notice("[OfflineShop] Pazar kasasinda cekilecek Yang yok (0 Yang).")

    def pull_offlineshop_safebox(self):
        offshop = get_mod("offlineshop")
        if offshop is None:
            return False
        ok = False
        try:
            # Hook ShopSafebox_SetValutes on offlineshop.GetOfflineshopBoard() to capture the exact server Yang balance
            if hasattr(offshop, "GetOfflineshopBoard"):
                brd = offshop.GetOfflineshopBoard()
                if brd is not None and hasattr(brd, "ShopSafebox_SetValutes") and not getattr(brd, "_avr_sb_hooked", False):
                    orig_set_val = brd.ShopSafebox_SetValutes
                    econ_self = self

                    def _hooked_set_val(valute, *a, **kw):
                        try:
                            econ_self._last_safebox_valute = int(valute)
                        except Exception:
                            pass
                        return orig_set_val(valute, *a, **kw)

                    brd.ShopSafebox_SetValutes = _hooked_set_val
                    brd._avr_sb_hooked = True
            if hasattr(offshop, "SendSafeboxOpen"):
                offshop.SendSafeboxOpen()
                ok = True
            self.pending_safebox_pull_t = time.clock() + 0.35
            return ok or hasattr(offshop, "SendSafeboxGetValutes")
        except Exception:
            return ok

    def _is_efsun_item(self, vnum, nm, it, st):
        if vnum in EFSUN_ITEM_VNUMS or vnum in (71085, 76013, 71189, 71190):
            return True
        if nm and ("efsun nesnesi" in nm or "efsun" in nm or "nesnesi" in nm):
            if "arttirma" not in nm and "kutsama" not in nm and "kure" not in nm:
                return True
        return False

    def step_efsun_bot(self, now):
        if not self.efsun_bot_enabled or (now - self.last_efsun_t < 0.08):
            return
        self.last_efsun_t = now
        player = get_mod("player")
        net = get_mod("net")
        if player is None or net is None:
            return
        get_vnum = getattr(player, "GetItemIndex", None)
        get_attr = getattr(player, "GetItemAttribute", None)
        use_to_item = getattr(net, "SendItemUseToItemPacket", None)
        if get_vnum is None or get_attr is None or use_to_item is None:
            return

        try:
            target_vnum = int(get_vnum(0))
            if target_vnum <= 0:
                self.efsun_bot_enabled = False
                chat_notice("[EfsunBot] Slot 1 bos! Efsunlanacak silahi 1. slota koyun.")
                return

            # Check if Slot 0 already reached target attribute (Avg Dmg >= target or Skill Dmg >= 18)
            avg_dmg = 0
            skill_dmg = 0
            for idx in range(5):
                at, av = get_attr(0, idx)
                if int(at) == 72:
                    avg_dmg = int(av)
                elif int(at) == 71:
                    skill_dmg = int(av)

            if avg_dmg >= self.target_avg_dmg or skill_dmg >= 18:
                self.efsun_bot_enabled = False
                chat_notice("[EfsunBot] HEDEF EFSUN GELDI! (Ort:%d / Bec:%d)" % (avg_dmg, skill_dmg))
                return

            # Find Efsun Nesnesi across all standard and special inventory windows (0..999)
            win_t, ef_slot, _, _ = scan_inventory_for_item(self._is_efsun_item, max_slot=1000)
            if ef_slot > 0 or (win_t is not None and ef_slot >= 0):
                try:
                    if win_t is not None and win_t != 1:
                        use_to_item(int(win_t), int(ef_slot), 1, 0)
                    else:
                        use_to_item(int(ef_slot), 0)
                except TypeError:
                    use_to_item(int(ef_slot), 0)
                self.efsun_count += 1
                return

            self.efsun_bot_enabled = False
            chat_notice("[EfsunBot] Envanterde (ve K Envanterinde) Efsun Nesnesi bulunamadi!")
        except Exception:
            pass

    def step(self):
        now = time.clock()
        if self.pending_refine is not None:
            fire_t, t_slot, r_type = self.pending_refine
            if now >= fire_t:
                self.pending_refine = None
                net = get_mod("net")
                if net is not None and hasattr(net, "SendRefinePacket"):
                    try:
                        net.SendRefinePacket(int(t_slot), int(r_type))
                    except Exception:
                        pass

        if self.pending_safebox_pull_t > 0.0 and now >= self.pending_safebox_pull_t:
            self.pending_safebox_pull_t = 0.0
            self._execute_safebox_valute_withdraw()

        if self.fast_quest_skip and (now - self.last_quest_t >= 0.15):
            self.last_quest_t = now
            ev = get_mod("event")
            if ev is not None and hasattr(ev, "Skip"):
                try:
                    ev.Skip(0)
                except Exception:
                    try:
                        ev.Skip()
                    except Exception:
                        pass

        self.step_efsun_bot(now)


# ============================================================================
# 7. HUD OVERLAY + 360 RADAR + 3D WORLD-TO-SCREEN ESP RENDERER
# ============================================================================

def safe_color(grp, r, g, b, a):
    if grp is not None and hasattr(grp, "GenerateColor"):
        try:
            return grp.GenerateColor(r, g, b, a)
        except Exception:
            pass
    ri = int(max(0, min(255, round(r * 255.0))))
    gi = int(max(0, min(255, round(g * 255.0))))
    bi = int(max(0, min(255, round(b * 255.0))))
    ai = int(max(0, min(255, round(a * 255.0))))
    return (ai << 24) | (ri << 16) | (gi << 8) | bi


def set_text_style(tl, hex_color, outline=False):
    if hasattr(tl, "SetPackedFontColor"):
        try:
            tl.SetPackedFontColor(hex_color)
        except Exception:
            pass
    elif hasattr(tl, "SetFontColor"):
        try:
            r = ((hex_color >> 16) & 0xFF) / 255.0
            g = ((hex_color >> 8) & 0xFF) / 255.0
            b = (hex_color & 0xFF) / 255.0
            tl.SetFontColor(r, g, b)
        except Exception:
            pass
    if outline and hasattr(tl, "SetOutline"):
        try:
            tl.SetOutline()
        except Exception:
            pass


def build_hud_and_attach(controller):
    ui = get_mod("ui")
    grp = get_mod("grp")
    wndMgr = get_mod("wndMgr")
    if ui is None or wndMgr is None:
        return None

    COLOR_BG = safe_color(grp, 0.05, 0.07, 0.11, 0.84)
    COLOR_RADAR_BG = safe_color(grp, 0.03, 0.05, 0.08, 0.92)
    COLOR_BORDER = safe_color(grp, 0.22, 0.62, 0.95, 0.90)
    COLOR_METIN = safe_color(grp, 1.00, 0.22, 0.85, 1.00)
    COLOR_BOSS = safe_color(grp, 1.00, 0.78, 0.10, 1.00)
    COLOR_MOB = safe_color(grp, 1.00, 0.30, 0.30, 0.92)
    COLOR_PLAYER = safe_color(grp, 0.25, 0.90, 1.00, 0.92)
    COLOR_LOCK = safe_color(grp, 0.20, 1.00, 0.35, 1.00)
    COLOR_GRID = safe_color(grp, 0.25, 0.35, 0.48, 0.65)
    COLOR_CAM = safe_color(grp, 0.35, 0.80, 1.00, 0.85)

    class SuiteOverlay(ui.Window):
        def __init__(self):
            ui.Window.__init__(self, "TOP_MOST")
            self.ctrl = controller
            self.SetSize(240, 306)
            sw = max(800, int(wndMgr.GetScreenWidth()))
            self.SetPosition(sw - 252, 135)
            if hasattr(self, "AddFlag"):
                try:
                    self.AddFlag("not_pick")
                except Exception:
                    pass
            self.Show()

            # Main HUD Background Bar
            self.bg_bar = ui.Bar()
            self.bg_bar.SetParent(self)
            self.bg_bar.SetPosition(0, 0)
            self.bg_bar.SetSize(240, 306)
            self.bg_bar.SetColor(COLOR_BG)
            if hasattr(self.bg_bar, "AddFlag"):
                try:
                    self.bg_bar.AddFlag("not_pick")
                except Exception:
                    pass
            self.bg_bar.Show()

            # Radar Square Area (144x144 at local pos 48, 24 -> center 120, 96)
            self.radar_bg = ui.Bar()
            self.radar_bg.SetParent(self)
            self.radar_bg.SetPosition(48, 24)
            self.radar_bg.SetSize(144, 144)
            self.radar_bg.SetColor(COLOR_RADAR_BG)
            if hasattr(self.radar_bg, "AddFlag"):
                try:
                    self.radar_bg.AddFlag("not_pick")
                except Exception:
                    pass
            self.radar_bg.Show()

            # Radar Crosshair Axis Bars
            self.axis_h = ui.Bar()
            self.axis_h.SetParent(self)
            self.axis_h.SetPosition(48, 96)
            self.axis_h.SetSize(144, 1)
            self.axis_h.SetColor(COLOR_GRID)
            self.axis_h.Show()

            self.axis_v = ui.Bar()
            self.axis_v.SetParent(self)
            self.axis_v.SetPosition(120, 24)
            self.axis_v.SetSize(1, 144)
            self.axis_v.SetColor(COLOR_GRID)
            self.axis_v.Show()

            # Camera Direction Indicator Dot on Radar
            self.cam_dot = ui.Bar()
            self.cam_dot.SetParent(self)
            self.cam_dot.SetPosition(119, 60)
            self.cam_dot.SetSize(3, 3)
            self.cam_dot.SetColor(COLOR_CAM)
            self.cam_dot.Show()

            # Player Center Dot on Radar
            self.center_dot = ui.Bar()
            self.center_dot.SetParent(self)
            self.center_dot.SetPosition(118, 94)
            self.center_dot.SetSize(5, 5)
            self.center_dot.SetColor(COLOR_LOCK)
            self.center_dot.Show()

            # Pool of 36 Native C++ ui.Bar Blips for 360 Radar Entities
            self.radar_dots = []
            for _ in range(36):
                dot = ui.Bar()
                dot.SetParent(self)
                dot.SetSize(4, 4)
                dot.SetColor(COLOR_MOB)
                if hasattr(dot, "AddFlag"):
                    try:
                        dot.AddFlag("not_pick")
                    except Exception:
                        pass
                dot.Hide()
                self.radar_dots.append(dot)

            self.title_line = ui.TextLine()
            self.title_line.SetParent(self)
            self.title_line.SetPosition(8, 5)
            self.title_line.SetText("Avrasya2 %s | [INS] Menu" % SUITE_VERSION)
            set_text_style(self.title_line, 0xFF55CCFF, outline=True)
            self.title_line.Show()

            self.status_lines = []
            for idx in range(8):
                tl = ui.TextLine()
                tl.SetParent(self)
                tl.SetPosition(8, 173 + idx * 16)
                set_text_style(tl, 0xFFE8F0FF, outline=True)
                tl.SetText("Avrasya2 %s Hazir" % SUITE_VERSION)
                tl.Show()
                self.status_lines.append(tl)
            self.lines = self.status_lines

            # Pool of 24 On-Screen 2D ESP Markers (ui.Bar Box + ui.TextLine Label)
            self.esp_pool = []
            for _ in range(24):
                marker = ui.Bar()
                marker.SetSize(8, 8)
                marker.SetColor(COLOR_MOB)
                if hasattr(marker, "AddFlag"):
                    try:
                        marker.AddFlag("not_pick")
                    except Exception:
                        pass
                marker.Hide()

                lbl = ui.TextLine()
                set_text_style(lbl, 0xFFFF5555, outline=True)
                if hasattr(lbl, "AddFlag"):
                    try:
                        lbl.AddFlag("not_pick")
                    except Exception:
                        pass
                lbl.Hide()
                self.esp_pool.append((marker, lbl))

        def OnUpdate(self):
            try:
                self.ctrl.on_frame_tick()
            except Exception as e:
                log_msg("OnUpdate err: " + str(e), "ERROR")

        def OnRender(self):
            try:
                self._render_lines()
            except Exception:
                pass

        def _render_lines(self):
            ctrl = self.ctrl
            if not ctrl.esp_enabled or grp is None:
                return
            if not hasattr(grp, "SetColor") or not hasattr(grp, "RenderLine"):
                return
            sw = max(800, int(wndMgr.GetScreenWidth()))
            sh = max(600, int(wndMgr.GetScreenHeight())) if hasattr(wndMgr, "GetScreenHeight") else 768
            px = sw - 252
            py = 135
            cx = px + 120
            cy = py + 96
            rad = 72
            scale = float(rad) / 6500.0

            locked_vid = ctrl.farmer.target_vid
            if locked_vid > 0 and locked_vid in ctrl.radar.entities:
                tinfo = ctrl.radar.entities[locked_vid]
                if tinfo.get("has_world_pos", False):
                    dx = max(-rad + 3, min(rad - 3, (tinfo["x"] - ctrl.last_mx) * scale))
                    dy = max(-rad + 3, min(rad - 3, (tinfo["y"] - ctrl.last_my) * scale))
                    grp.SetColor(COLOR_LOCK)
                    grp.RenderLine(cx, cy, int(cx + dx), int(cy + dy))
                if tinfo.get("on_screen", False):
                    grp.SetColor(COLOR_LOCK)
                    grp.RenderLine(sw // 2, sh - 90, int(tinfo["sx"]), int(tinfo["sy"]))

        def update_visuals(self):
            ctrl = self.ctrl
            cnt = ctrl.radar.get_counts()
            self.status_lines[0].SetText(
                "Metin:%d | Boss:%d | Mob:%d | Oyuncu:%d" % (cnt["metin"], cnt["boss"], cnt["monster"], cnt["player"])
            )
            self.status_lines[1].SetText(
                "[F5] Radar:%s (%s)" % ("ACIK" if ctrl.esp_enabled else "KAPALI", ctrl.radar.get_filter_label())
            )
            self.status_lines[2].SetText(
                "[F6] Farm:%s (%s)" % ("ACIK" if ctrl.farmer.enabled else "KAPALI", ctrl.farmer.get_mode_label())
            )
            self.status_lines[3].SetText(
                "Durum: %s" % ctrl.farmer.state_str
            )
            self.status_lines[4].SetText(
                "[F7] OtoToplama+SvSide:%s (Cozulen:%d)" % ("ACIK" if ctrl.looter.enabled else "KAPALI", ctrl.looter.solved_count)
            )
            self.status_lines[5].SetText(
                "[F8] Pot/Kutsama:%s | [F9] Biyolog:%s" % (
                    "ACIK" if ctrl.sustain.enabled else "KAPALI",
                    "ACIK" if ctrl.biyolog.enabled else "KAPALI",
                )
            )
            self.status_lines[6].SetText(
                "[F11] Anim:%s | [F12] WH:%s" % (
                    "ACIK" if ctrl.ninja_anim.enabled else "KAPALI",
                    "ACIK" if ctrl.combat.waithack_enabled else "KAPALI",
                )
            )
            self.status_lines[7].SetText(
                "[INSERT] Menu:%s | Sekmeme:%s" % (
                    "ACIK" if ctrl.menu_visible else "KAPALI",
                    "ACIK" if ctrl.combat.no_knockback else "KAPALI",
                )
            )

            if not ctrl.esp_enabled:
                for dot in self.radar_dots:
                    dot.Hide()
                for marker, lbl in self.esp_pool:
                    marker.Hide()
                    lbl.Hide()
                return

            sw = max(800, int(wndMgr.GetScreenWidth()))
            px = sw - 252
            py = 135
            self.SetPosition(px, py)

            # Radar local center is (120, 96), radius = 72
            lcx = 120
            lcy = 96
            rad = 72

            cam_lx = int(lcx + ctrl.radar.cam_dir_x * 42.0)
            cam_ly = int(lcy + ctrl.radar.cam_dir_y * 42.0)
            self.cam_dot.SetPosition(cam_lx - 1, cam_ly - 1)

            mx = ctrl.last_mx
            my = ctrl.last_my
            scale = float(rad) / 6500.0
            locked_vid = ctrl.farmer.target_vid

            items = ctrl.radar.get_filtered_list()
            dot_idx = 0
            esp_idx = 0

            for info in items:
                if not info.get("has_world_pos", False):
                    continue
                k = info.get("kind", "monster")
                dx = (info["x"] - mx) * scale
                dy = (info["y"] - my) * scale
                dx = max(-rad + 4, min(rad - 4, dx))
                dy = max(-rad + 4, min(rad - 4, dy))
                rx = int(lcx + dx)
                ry = int(lcy + dy)

                if info["vid"] == locked_vid:
                    col = COLOR_LOCK
                    hex_col = 0xFF33FF55
                    sz = 6
                elif k == "metin":
                    col = COLOR_METIN
                    hex_col = 0xFFFF44DD
                    sz = 6
                elif k == "boss":
                    col = COLOR_BOSS
                    hex_col = 0xFFFFCC22
                    sz = 6
                elif k == "player":
                    col = COLOR_PLAYER
                    hex_col = 0xFF44EEFF
                    sz = 4
                else:
                    col = COLOR_MOB
                    hex_col = 0xFFFF5555
                    sz = 4

                if dot_idx < len(self.radar_dots):
                    dot = self.radar_dots[dot_idx]
                    dot_idx += 1
                    dot.SetSize(sz, sz)
                    dot.SetColor(col)
                    dot.SetPosition(rx - sz // 2, ry - sz // 2)
                    dot.Show()

                if info.get("on_screen", False) and esp_idx < len(self.esp_pool):
                    if k in ("metin", "boss") or info["vid"] == locked_vid or esp_idx < 14:
                        sx = int(info["sx"])
                        sy = int(info["sy"])
                        marker, lbl = self.esp_pool[esp_idx]
                        esp_idx += 1

                        marker.SetColor(col)
                        marker.SetPosition(sx - 4, sy - 4)
                        if hasattr(marker, "SetTop"):
                            marker.SetTop()
                        marker.Show()

                        tag = "[%s] %s (%.0fm)" % (
                            "HEDEF" if info["vid"] == locked_vid else k.upper(),
                            info.get("name", "")[:16],
                            info.get("dist", 0.0) / 100.0,
                        )
                        lbl.SetText(tag)
                        set_text_style(lbl, hex_col, outline=True)
                        lbl.SetPosition(sx - 45, sy - 22)
                        if hasattr(lbl, "SetTop"):
                            lbl.SetTop()
                        lbl.Show()

            while dot_idx < len(self.radar_dots):
                self.radar_dots[dot_idx].Hide()
                dot_idx += 1

            while esp_idx < len(self.esp_pool):
                marker, lbl = self.esp_pool[esp_idx]
                marker.Hide()
                lbl.Hide()
                esp_idx += 1

    # Interactive Clickable [INSERT] GUI Panel
    COLOR_MENU_BG = safe_color(grp, 0.04, 0.06, 0.10, 0.94)
    COLOR_MENU_HEADER = safe_color(grp, 0.08, 0.14, 0.24, 0.98)
    COLOR_TAB_ACTIVE = safe_color(grp, 0.16, 0.48, 0.82, 0.98)
    COLOR_TAB_IDLE = safe_color(grp, 0.09, 0.13, 0.20, 0.92)
    COLOR_BTN_ON = safe_color(grp, 0.12, 0.56, 0.28, 0.95)
    COLOR_BTN_OFF = safe_color(grp, 0.14, 0.17, 0.24, 0.92)
    COLOR_BTN_ACT = safe_color(grp, 0.16, 0.36, 0.62, 0.95)
    COLOR_BTN_HOVER = safe_color(grp, 0.28, 0.58, 0.88, 0.98)

    class MenuButton(ui.Window):
        def __init__(self, parent, x, y, w, h, text, callback):
            ui.Window.__init__(self)
            self.SetParent(parent)
            self.SetPosition(x, y)
            self.SetSize(w, h)
            self.bx = x
            self.by = y
            self.bw = w
            self.bh = h
            self.callback = callback
            self.state = False
            self.last_click_t = 0.0
            self.Show()

            self.border = ui.Bar()
            self.border.SetParent(self)
            self.border.SetPosition(0, 0)
            self.border.SetSize(w, h)
            self.border.SetColor(COLOR_BORDER)
            if hasattr(self.border, "AddFlag"):
                try:
                    self.border.AddFlag("not_pick")
                except Exception:
                    pass
            self.border.Show()

            self.fill = ui.Bar()
            self.fill.SetParent(self)
            self.fill.SetPosition(1, 1)
            self.fill.SetSize(w - 2, h - 2)
            self.fill.SetColor(COLOR_BTN_OFF)
            if hasattr(self.fill, "AddFlag"):
                try:
                    self.fill.AddFlag("not_pick")
                except Exception:
                    pass
            self.fill.Show()

            self.label = ui.TextLine()
            self.label.SetParent(self)
            self.label.SetPosition(8, max(2, (h - 14) // 2))
            set_text_style(self.label, 0xFFF0F6FF, outline=True)
            self.label.SetText(str(text))
            if hasattr(self.label, "AddFlag"):
                try:
                    self.label.AddFlag("not_pick")
                except Exception:
                    pass
            self.label.Show()

        def trigger(self):
            now = time.clock()
            if now - self.last_click_t < 0.16:
                return
            self.last_click_t = now
            if self.callback is not None:
                try:
                    self.callback()
                except Exception as e:
                    log_msg("MenuButton err: " + str(e), "ERROR")

        def OnMouseLeftButtonDown(self):
            self.trigger()
            return True

        def OnMouseLeftButtonUp(self):
            self.trigger()
            return True

        def set_visual(self, text, state=None, is_tab=False, hovered=False):
            self.label.SetText(str(text))
            self.state = state
            if hovered:
                self.fill.SetColor(COLOR_BTN_HOVER)
            elif is_tab:
                self.fill.SetColor(COLOR_TAB_ACTIVE if state else COLOR_TAB_IDLE)
            elif state is True:
                self.fill.SetColor(COLOR_BTN_ON)
            elif state is False:
                self.fill.SetColor(COLOR_BTN_OFF)
            else:
                self.fill.SetColor(COLOR_BTN_ACT)

    class AvrasyaMenuWindow(ui.Window):
        def __init__(self):
            ui.Window.__init__(self, "TOP_MOST")
            self.ctrl = controller
            self.mw = 460
            self.mh = 358
            self.SetSize(self.mw, self.mh)
            sw = max(800, int(wndMgr.GetScreenWidth()))
            sh = max(600, int(wndMgr.GetScreenHeight())) if hasattr(wndMgr, "GetScreenHeight") else 768
            self.SetPosition((sw - self.mw) // 2, max(60, (sh - self.mh) // 2))
            if hasattr(self, "AddFlag"):
                for flg in ("movable", "float"):
                    try:
                        self.AddFlag(flg)
                    except Exception:
                        pass
            self.tab_idx = 0
            self.all_buttons = []

            # Main frame & header
            self.bg = ui.Bar()
            self.bg.SetParent(self)
            self.bg.SetPosition(0, 0)
            self.bg.SetSize(self.mw, self.mh)
            self.bg.SetColor(COLOR_MENU_BG)
            if hasattr(self.bg, "AddFlag"):
                try:
                    self.bg.AddFlag("not_pick")
                except Exception:
                    pass
            self.bg.Show()

            self.header = ui.Bar()
            self.header.SetParent(self)
            self.header.SetPosition(0, 0)
            self.header.SetSize(self.mw, 30)
            self.header.SetColor(COLOR_MENU_HEADER)
            if hasattr(self.header, "AddFlag"):
                try:
                    self.header.AddFlag("not_pick")
                except Exception:
                    pass
            self.header.Show()

            self.title = ui.TextLine()
            self.title.SetParent(self)
            self.title.SetPosition(12, 7)
            self.title.SetText("AVRASYA2 EXPLOIT & FARM SUITE %s  |  [INSERT] Gizle/Ac" % SUITE_VERSION)
            set_text_style(self.title, 0xFF55DDFF, outline=True)
            if hasattr(self.title, "AddFlag"):
                try:
                    self.title.AddFlag("not_pick")
                except Exception:
                    pass
            self.title.Show()

            # Close [X] button
            self.close_btn = MenuButton(
                self, self.mw - 34, 4, 28, 22, "X", lambda: self.ctrl.toggle_menu(False)
            )
            self.all_buttons.append(self.close_btn)

            # 4 Category Tabs
            tab_names = ["1. FARM & RADAR", "2. SAVAS & ANIM", "3. HARITA & FIZIK", "4. PAKET & EFSUN"]
            self.tab_buttons = []
            tw = (self.mw - 24) // 4
            for tidx, tname in enumerate(tab_names):
                btn = MenuButton(
                    self,
                    12 + tidx * tw,
                    36,
                    tw - 4,
                    26,
                    tname,
                    lambda i=tidx: self.select_tab(i),
                )
                self.tab_buttons.append(btn)
                self.all_buttons.append(btn)

            # 6 Action Rows (each row has Left Toggle Button + Right Mode/Action Button)
            self.row_pairs = []
            for r in range(6):
                ry = 72 + r * 40
                b_left = MenuButton(
                    self, 12, ry, 214, 32, "-", lambda row=r: self.on_row_click(row, 0)
                )
                b_right = MenuButton(
                    self, 234, ry, 214, 32, "-", lambda row=r: self.on_row_click(row, 1)
                )
                self.row_pairs.append((b_left, b_right))
                self.all_buttons.append(b_left)
                self.all_buttons.append(b_right)

            # Footer info line
            self.footer = ui.TextLine()
            self.footer.SetParent(self)
            self.footer.SetPosition(12, self.mh - 26)
            set_text_style(self.footer, 0xFFAAD4FF, outline=True)
            self.footer.SetText("Durum: Hazir | Tum butonlara fare ile tiklayabilirsiniz.")
            if hasattr(self.footer, "AddFlag"):
                try:
                    self.footer.AddFlag("not_pick")
                except Exception:
                    pass
            self.footer.Show()

            if self.ctrl.menu_visible:
                self.Show()
            else:
                self.Hide()

        def select_tab(self, idx):
            self.tab_idx = int(idx) % 4
            self.update_menu()

        def OnMouseLeftButtonDown(self):
            # Fallback parent hit-test so clicks always register even if child flags vary
            try:
                if hasattr(self, "GetMouseLocalPosition"):
                    lx, ly = self.GetMouseLocalPosition()
                elif hasattr(wndMgr, "GetMouseLocalPosition") and hasattr(self, "hWnd"):
                    lx, ly = wndMgr.GetMouseLocalPosition(self.hWnd)
                else:
                    return False
                for btn in self.all_buttons:
                    if btn.bx <= lx <= (btn.bx + btn.bw) and btn.by <= ly <= (btn.by + btn.bh):
                        btn.trigger()
                        return True
            except Exception:
                pass
            return False

        def on_row_click(self, row, col):
            c = self.ctrl
            t = self.tab_idx
            if t == 0:
                if row == 0:
                    if col == 0:
                        c.handle_hotkey(5, False, time.clock())
                    else:
                        c.handle_hotkey(5, True, time.clock())
                elif row == 1:
                    if col == 0:
                        c.handle_hotkey(6, False, time.clock())
                    else:
                        c.handle_hotkey(6, True, time.clock())
                elif row == 2:
                    if col == 0:
                        c.handle_hotkey(12, False, time.clock())
                    else:
                        c.handle_hotkey(12, True, time.clock())
                elif row == 3:
                    if col == 0:
                        c.handle_hotkey(7, False, time.clock())
                    else:
                        c.handle_hotkey(7, True, time.clock())
                elif row == 4:
                    if col == 0:
                        c.handle_hotkey(8, False, time.clock())
                    else:
                        c.sustain.hp_threshold = 60 if c.sustain.hp_threshold == 78 else (90 if c.sustain.hp_threshold == 60 else 78)
                        chat_notice("Oto-Pot HP Esigi: %%%d" % c.sustain.hp_threshold)
                elif row == 5:
                    if col == 0:
                        if c.farmer.enabled and c.farmer.get_mode_key() == "ore":
                            c.farmer.mode_idx = 0
                            chat_notice("Maden Modu Kapatildi -> Mod: %s" % c.farmer.get_mode_label())
                        else:
                            c.farmer.mode_idx = 4
                            c.farmer.set_enabled(True)
                            chat_notice("Maden Damari Kazici Modu Aktif!")
                    else:
                        c.farmer.blacklist.clear()
                        c.farmer.target_vid = 0
                        chat_notice("Hedef & Blacklist Sifirlandi.")
            elif t == 1:
                if row == 0:
                    if col == 0:
                        c.handle_hotkey(11, False, time.clock())
                    else:
                        c.handle_hotkey(11, True, time.clock())
                elif row == 1:
                    c.combat.no_knockback = not c.combat.no_knockback
                    chat_notice("Sekmeme / Yere Dusmeme (Anti-Knockback): %s" % ("ACIK" if c.combat.no_knockback else "KAPALI"))
                elif row == 2:
                    c.combat.cancel_4th_hit = not c.combat.cancel_4th_hit
                    chat_notice("4. Vurus Iptali (Slot Dagitmama): %s" % ("ACIK" if c.combat.cancel_4th_hit else "KAPALI"))
                elif row == 3:
                    if col == 0:
                        c.combat.no_skill_delay = not c.combat.no_skill_delay
                        chat_notice("0ms Animasyonsuz Skill: %s" % ("ACIK" if c.combat.no_skill_delay else "KAPALI"))
                    else:
                        _, msg = c.combat.queue_skills_1_to_6(c.last_my_vid)
                        chat_notice(msg)
                elif row == 4:
                    ok = c.combat.trigger_shield_antistun()
                    chat_notice("1-Tick Kalkan Anti-Stun: %s" % ("Uygulandi" if ok else "Kalkan Bulunamadi"))
                elif row == 5:
                    if col == 0:
                        c.handle_hotkey(6, False, time.clock())
                    else:
                        _, msg = c.farmer.use_bravery_cape(time.clock(), force=True)
                        chat_notice("Cesaret Pelerini: %s" % (msg or "Envanterde Pelerin Bulunamadi"))
            elif t == 2:
                if row == 0:
                    c.world.set_wallhack_objects(not c.world.wallhack_objects)
                    chat_notice("Wallhack (Obje/Kapi/Agac Silici + Duvar Gecis): %s" % ("ACIK" if c.world.wallhack_objects else "KAPALI"))
                elif row == 1:
                    if col == 0:
                        c.world.alt_click_blink = not c.world.alt_click_blink
                        chat_notice("ALT+C Imlece Blink: %s" % ("ACIK" if c.world.alt_click_blink else "KAPALI"))
                    else:
                        ok = c.world.blink_to_cursor(c.last_my_vid, c.last_mx, c.last_my, c.last_mz)
                        chat_notice("Imlece Blink: %s" % ("Basarili" if ok else "Hedef Nokta Yok"))
                elif row == 2:
                    ok = c.world.trigger_ghost_walk(c.last_my_vid)
                    chat_notice("Hayalet Modu (Ghost Walk + Duvar Gecis): %s" % (
                        "ACIK" if (ok and c.world.ghost_mode_active) else ("KAPALI" if ok else "Hazir Degil")
                    ))
                elif row == 3:
                    if col == 0:
                        c.handle_hotkey(10, False, time.clock())
                    else:
                        c.handle_hotkey(10, True, time.clock())
                elif row == 4:
                    c.radar.last_minimap_t = 0.0
                    c.radar.sync_minimap_waypoints(time.clock(), enabled=c.esp_enabled)
                    chat_notice("Minimap Metin/Boss Pinleri Yenilendi!")
                elif row == 5:
                    c.toggle_menu(False)
            elif t == 3:
                if row == 0:
                    if col == 0:
                        _, msg = c.economy.remote_refine_slot0(0)
                        chat_notice("Uzaktan Demirci +Bas: %s" % msg)
                    else:
                        _, msg = c.economy.remote_refine_slot0(1)
                        chat_notice("Uzaktan Kutsama/Metal +Bas: %s" % msg)
                elif row == 1:
                    if col == 0:
                        c.handle_hotkey(9, False, time.clock())
                    else:
                        c.biyolog.send_biyolog_packet()
                        chat_notice("Uzaktan Biyolog Paketi Gonderildi!")
                elif row == 2:
                    if col == 0:
                        c.economy.efsun_bot_enabled = not c.economy.efsun_bot_enabled
                        chat_notice("Paket Hizinda Efsun Botu (Slot 1): %s" % ("ACIK" if c.economy.efsun_bot_enabled else "KAPALI"))
                    else:
                        c.economy.target_avg_dmg = 50 if c.economy.target_avg_dmg == 45 else (40 if c.economy.target_avg_dmg == 50 else 45)
                        chat_notice("Efsun Hedef Ortalama Zarar: %d+" % c.economy.target_avg_dmg)
                elif row == 3:
                    c.economy.fast_quest_skip = not c.economy.fast_quest_skip
                    chat_notice("0ms Zindan/Gorev Diyalog Gecici: %s" % ("ACIK" if c.economy.fast_quest_skip else "KAPALI"))
                elif row == 4:
                    ok = c.economy.pull_offlineshop_safebox()
                    chat_notice("OfflineShop Pazar Kasasi Cek: %s" % ("Kasa Acildi & Cekim Gonderildi" if ok else "Mod Yok"))
                elif row == 5:
                    c.handle_hotkey(9, True, time.clock())
            self.update_menu()

        def update_menu(self):
            c = self.ctrl
            if not c.menu_visible:
                self.Hide()
                return
            self.Show()
            if hasattr(self, "SetTop"):
                try:
                    self.SetTop()
                except Exception:
                    pass

            lx, ly = -1, -1
            try:
                if hasattr(self, "GetMouseLocalPosition"):
                    lx, ly = self.GetMouseLocalPosition()
                elif hasattr(wndMgr, "GetMouseLocalPosition") and hasattr(self, "hWnd"):
                    lx, ly = wndMgr.GetMouseLocalPosition(self.hWnd)
            except Exception:
                pass

            def is_hov(btn):
                return btn.bx <= lx <= (btn.bx + btn.bw) and btn.by <= ly <= (btn.by + btn.bh)

            self.close_btn.set_visual("X", state=False, hovered=is_hov(self.close_btn))
            for idx, tbtn in enumerate(self.tab_buttons):
                tbtn.set_visual(
                    ["1. FARM & RADAR", "2. SAVAS & ANIM", "3. HARITA & FIZIK", "4. PAKET & EFSUN"][idx],
                    state=(idx == self.tab_idx),
                    is_tab=True,
                    hovered=is_hov(tbtn),
                )

            t = self.tab_idx
            if t == 0:
                rows_cfg = [
                    ("360 Radar & ESP: %s" % ("ACIK" if c.esp_enabled else "KAPALI"), c.esp_enabled,
                     "Filtre: %s" % c.radar.get_filter_label(), None),
                    ("Auto-Farm [F6]: %s" % ("ACIK" if c.farmer.enabled else "KAPALI"), c.farmer.enabled,
                     "Mod: %s" % c.farmer.get_mode_label(), None),
                    ("360 Waithack [F12]: %s" % ("ACIK" if c.combat.waithack_enabled else "KAPALI"), c.combat.waithack_enabled,
                     "Menzil: %s" % c.combat.get_mode_label(), None),
                    ("Oto-Toplama & SvSide: %s" % ("ACIK" if c.looter.enabled else "KAPALI"), c.looter.enabled,
                     "SvSide Cozulen: %d (Test)" % c.looter.solved_count, None),
                    ("Oto-Pot & Kutsama: %s" % ("ACIK" if c.sustain.enabled else "KAPALI"), c.sustain.enabled,
                     "HP Pot Esigi: %%%d" % c.sustain.hp_threshold, None),
                    ("Maden Damari Kazici Baslat", c.farmer.enabled and c.farmer.get_mode_key() == "ore",
                     "Hedef & Blacklist Sifirla", None),
                ]
            elif t == 1:
                rows_cfg = [
                    ("Saldiri Anim [F11]: %s" % ("ACIK" if c.ninja_anim.enabled else "KAPALI"), c.ninja_anim.enabled,
                     "Preset: %s" % c.ninja_anim.get_preset_label(), None),
                    ("Sekmeme / Yere Dusmeme: %s" % ("ACIK" if c.combat.no_knockback else "KAPALI"), c.combat.no_knockback,
                     "Anti-Knockback Korumasi", c.combat.no_knockback),
                    ("4. Vurus Iptali: %s" % ("ACIK" if c.combat.cancel_4th_hit else "KAPALI"), c.combat.cancel_4th_hit,
                     "Kombo 1-2-3 (Slot Dagitmaz)", c.combat.cancel_4th_hit),
                    ("0ms Animasyonsuz Skill: %s" % ("ACIK" if c.combat.no_skill_delay else "KAPALI"), c.combat.no_skill_delay,
                     "Simdi Skill 1-6 Tetikle", None),
                    ("1-Tick Kalkan Anti-Stun", None,
                     "Simdi Kalkan Cikar-Tak Yap", None),
                    ("Cesaret Pelerini (Oto)", c.farmer.enabled,
                     "Simdi Pelerin / Paket Cek", None),
                ]
            elif t == 2:
                rows_cfg = [
                    ("Wallhack (Obje/Kapi Sil): %s" % ("ACIK" if c.world.wallhack_objects else "KAPALI"), c.world.wallhack_objects,
                     "Bina/Agac Sil + Duvar Gec", c.world.wallhack_objects),
                    ("ALT+C Imlece Blink: %s" % ("ACIK" if c.world.alt_click_blink else "KAPALI"), c.world.alt_click_blink,
                     "Simdi Imlece Isinlan", None),
                    ("Hayalet Modu (Ghost): %s" % ("ACIK" if c.world.ghost_mode_active else "KAPALI"), c.world.ghost_mode_active,
                     "Duvar/Obje Icinden Yuru", c.world.ghost_mode_active),
                    ("Kamera Zoom & FPS [F10]: %s" % ("ACIK" if c.cam_boost.enabled else "KAPALI"), c.cam_boost.enabled,
                     "Mod: %s" % c.cam_boost.get_preset_label(), None),
                    ("Minimap Metin/Boss Pin: %s" % ("ACIK" if c.esp_enabled else "KAPALI"), c.esp_enabled,
                     "Minimap Pinlerini Yenile", None),
                    ("Menuyu Gizle [INSERT]", False,
                     "Menuyu Kapat", None),
                ]
            else:
                rows_cfg = [
                    ("Uzaktan Demirci +Bas (Slot 1)", None,
                     "Kutsama/Metal +Bas (Slot 1)", None),
                    ("Uzaktan Biyolog [F9]: %s" % ("ACIK" if c.biyolog.enabled else "KAPALI"), c.biyolog.enabled,
                     "Simdi Biyolog Gonder", None),
                    ("Hizli Efsun Botu (Slot 1): %s" % ("ACIK" if c.economy.efsun_bot_enabled else "KAPALI"), c.economy.efsun_bot_enabled,
                     "Hedef Ortalama: %d+ (Atilan:%d)" % (c.economy.target_avg_dmg, c.economy.efsun_count), None),
                    ("0ms Zindan/Gorev Gecici: %s" % ("ACIK" if c.economy.fast_quest_skip else "KAPALI"), c.economy.fast_quest_skip,
                     "Otomatik Diyalog Skip", c.economy.fast_quest_skip),
                    ("OfflineShop Pazar Kasasi", None,
                     "Uzaktan Pazar Yang/Won Cek", None),
                    ("Cop Ekipman Satisi (+6 Alti)", None,
                     "Simdi Cop Esyalari Sat", None),
                ]

            for r_idx, (lt, ls, rt, rs) in enumerate(rows_cfg):
                bl, br = self.row_pairs[r_idx]
                bl.set_visual(lt, state=ls, hovered=is_hov(bl))
                br.set_visual(rt, state=rs, hovered=is_hov(br))

            cnt = c.radar.get_counts()
            self.footer.SetText(
                "Durum: %s | Metin:%d Boss:%d Mob:%d Maden:%d | [INSERT] Menu"
                % (c.farmer.state_str, cnt["metin"], cnt["boss"], cnt["monster"], cnt["ore"])
            )

    ov = SuiteOverlay()
    menu = AvrasyaMenuWindow()
    controller.menu_wnd = menu
    return ov


# ============================================================================
# 8. MASTER CONTROLLER & HOTKEY DISPATCHER
# ============================================================================

class SuiteController(object):
    def __init__(self):
        self.radar = EntityRadar()
        self.farmer = AutoFarmer(self.radar)
        self.looter = LootAndCaptchaManager()
        self.sustain = SustainManager()
        self.biyolog = BiyologAndJunkManager()
        self.cam_boost = CameraAndFpsBoost()
        self.ninja_anim = NinjaAnimManager()
        self.combat = WaithackAndCombatManager(self.radar, self.farmer, self.ninja_anim)
        self.world = WorldExploitManager()
        self.economy = EconomyExploitManager(self.radar)

        self.esp_enabled = True
        self.menu_visible = True
        self.overlay = None
        self.hud = None
        self.menu_wnd = None
        self.frames = 0
        self.last_my_vid = 0
        self.last_mx = 0.0
        self.last_my = 0.0
        self.last_mz = 0.0
        self.key_latch = {}
        self.last_stats_log_t = 0.0
        self.first_world_t = 0.0
        self.diag_attempts = 0
        self.greeted = False
        self.diag_logged = False

    def log_character_diagnostics(self):
        player = get_mod("player")
        if player is None:
            return 0
        try:
            inv_items = []
            if hasattr(player, "GetItemIndex"):
                for s in range(1000):
                    try:
                        v = int(player.GetItemIndex(s))
                        if v > 0:
                            nm, _, _, _, _ = get_item_meta(v)
                            inv_items.append("%d:%d(%s)" % (s, v, nm[:14] if nm else "?"))
                    except Exception:
                        pass
                if not inv_items:
                    for w in range(1, 8):
                        for s in range(180):
                            try:
                                v = int(player.GetItemIndex(w, s))
                                if v > 0:
                                    nm, _, _, _, _ = get_item_meta(v)
                                    inv_items.append("w%d_%d:%d(%s)" % (w, s, v, nm[:14] if nm else "?"))
                            except Exception:
                                break
            sk_items = []
            for s_i in range(1, 7):
                try:
                    si = int(player.GetSkillIndex(s_i)) if hasattr(player, "GetSkillIndex") else 0
                    sl = int(player.GetSkillLevel(s_i)) if hasattr(player, "GetSkillLevel") else 0
                    sk_items.append("%d:%d(L%d)" % (s_i, si, sl))
                except Exception:
                    pass
            st_items = []
            if hasattr(player, "GetStatus"):
                for st_i in range(1, 9):
                    try:
                        st_items.append("%d=%d" % (st_i, int(player.GetStatus(st_i))))
                    except Exception:
                        pass
            log_msg("[DIAG_INV] count=%d items=%s" % (len(inv_items), ", ".join(inv_items[:40])))
            log_msg("[DIAG_SKILLS] %s | STATUS: %s" % (", ".join(sk_items), ", ".join(st_items)))
            return len(inv_items)
        except Exception as e:
            log_msg("log_character_diagnostics err: " + str(e), "ERROR")
            return 0

    def toggle_menu(self, flag=None):
        if flag is None:
            self.menu_visible = not self.menu_visible
        else:
            self.menu_visible = bool(flag)
        if self.menu_wnd is not None:
            try:
                self.menu_wnd.update_menu()
            except Exception:
                pass

    def on_update(self):
        return self.on_frame_tick()

    def poll_hotkeys(self):
        app = get_mod("app")
        if app is None or not hasattr(app, "IsPressed"):
            return
        is_pressed = app.IsPressed

        shift_down = False
        try:
            shift_down = bool(
                is_pressed(getattr(app, "DIK_LSHIFT", 42))
                or is_pressed(getattr(app, "DIK_RSHIFT", 54))
            )
        except Exception:
            shift_down = False

        f_keys = [
            (5, getattr(app, "DIK_F5", 63)),
            (6, getattr(app, "DIK_F6", 64)),
            (7, getattr(app, "DIK_F7", 65)),
            (8, getattr(app, "DIK_F8", 66)),
            (9, getattr(app, "DIK_F9", 67)),
            (10, getattr(app, "DIK_F10", 68)),
            (11, getattr(app, "DIK_F11", 87)),
            (12, getattr(app, "DIK_F12", 88)),
            (99, getattr(app, "DIK_INSERT", 210)),
        ]

        now = time.clock()
        for f_num, dik in f_keys:
            down = False
            try:
                down = bool(is_pressed(dik))
            except Exception:
                down = False
            was_down = self.key_latch.get(f_num, False)
            self.key_latch[f_num] = down
            if down and not was_down:
                self.handle_hotkey(f_num, shift_down, now)

    def handle_hotkey(self, f_num, shift_down, now):
        if f_num == 99:
            self.toggle_menu()
            chat_notice("[INSERT] Kontrol Paneli: %s" % ("ACIK" if self.menu_visible else "KAPALI"))
        elif f_num == 5:
            if shift_down:
                lbl = self.radar.cycle_filter()
                chat_notice("[SHIFT+F5] Radar Filtresi: %s" % lbl)
            else:
                self.esp_enabled = not self.esp_enabled
                chat_notice("[F5] 360 Radar & ESP: %s" % ("ACIK" if self.esp_enabled else "KAPALI"))
        elif f_num == 6:
            if shift_down:
                lbl = self.farmer.cycle_mode()
                chat_notice("[SHIFT+F6] Farm Hedef Modu: %s" % lbl)
            else:
                self.farmer.set_enabled(not self.farmer.enabled)
                chat_notice("[F6] Auto-Farm: %s (%s)" % (
                    "ACIK" if self.farmer.enabled else "KAPALI",
                    self.farmer.get_mode_label(),
                ))
        elif f_num == 7:
            if shift_down:
                self.looter.parse_and_reply_svside("<svside> Test Dogrulama Kodu: 4829")
            else:
                self.looter.enabled = not self.looter.enabled
                chat_notice("[F7] Oto-Toplama & SvSide Solver: %s" % ("ACIK" if self.looter.enabled else "KAPALI"))
        elif f_num == 8:
            if shift_down:
                self.ninja_anim.set_enabled(not self.ninja_anim.enabled, self.last_my_vid)
                chat_notice("[SHIFT+F8] Ninja Cift Hancer Saldiri Animasyonu: %s" % ("ACIK" if self.ninja_anim.enabled else "KAPALI"))
            else:
                self.sustain.enabled = not self.sustain.enabled
                chat_notice("[F8] Oto-Pot / Ikram / Kutsama / Dirilme: %s" % ("ACIK" if self.sustain.enabled else "KAPALI"))
        elif f_num == 9:
            if shift_down:
                _, msg = self.biyolog.sell_junk_items()
                chat_notice("[SHIFT+F9] %s" % msg)
            else:
                self.biyolog.enabled = not self.biyolog.enabled
                if self.biyolog.enabled:
                    self.biyolog.send_biyolog_packet()
                chat_notice("[F9] Uzaktan Biyolog: %s" % ("ACIK" if self.biyolog.enabled else "KAPALI"))
        elif f_num == 10:
            if shift_down:
                lbl = self.cam_boost.cycle_preset()
                chat_notice("[SHIFT+F10] Kamera/FPS Modu: %s" % lbl)
            else:
                self.cam_boost.set_enabled(not self.cam_boost.enabled)
                chat_notice("[F10] Kamera Zoom & Sis/FPS: %s (%s)" % (
                    "ACIK" if self.cam_boost.enabled else "KAPALI",
                    self.cam_boost.get_preset_label() if self.cam_boost.enabled else "Standart",
                ))
        elif f_num == 11:
            if shift_down:
                lbl = self.ninja_anim.cycle_preset()
                chat_notice("[SHIFT+F11] Ninja Animasyon Modu: %s" % lbl)
            else:
                self.ninja_anim.set_enabled(not self.ninja_anim.enabled, self.last_my_vid)
                chat_notice("[F11] Ninja Cift Hancer Saldiri Animasyonu: %s (%s)" % (
                    "ACIK" if self.ninja_anim.enabled else "KAPALI",
                    self.ninja_anim.get_preset_label() if self.ninja_anim.enabled else "Orijinal",
                ))
        elif f_num == 12:
            if shift_down:
                lbl = self.combat.cycle_mode()
                chat_notice("[SHIFT+F12] Waithack Menzil Modu: %s" % lbl)
            else:
                self.combat.set_waithack(not self.combat.waithack_enabled, self.last_my_vid)
                chat_notice("[F12] 360 Waithack: %s (%s)" % (
                    "ACIK" if self.combat.waithack_enabled else "KAPALI",
                    self.combat.get_mode_label(),
                ))

    def on_frame_tick(self):
        self.frames += 1
        self.poll_hotkeys()

        my_vid, mx, my, mz = self.radar.step(
            esp_enabled=self.esp_enabled,
            priority_vid=self.farmer.target_vid or self.combat.wh_target_vid,
            farm_active=self.farmer.enabled or self.combat.waithack_enabled,
            in_melee=self.farmer.in_melee,
        )
        self.last_my_vid = my_vid
        self.last_mx = mx
        self.last_my = my
        self.last_mz = mz

        now = time.clock()
        if my_vid <= 0:
            last_pre = getattr(self, "_last_pre_world_log_t", 0.0)
            if now - last_pre >= 2.0:
                self._last_pre_world_log_t = now
                _NATIVE_BRIDGE.log_pid_and_gate_state("PRE_WORLD")

        if my_vid > 0 and not self.greeted:
            self.greeted = True
            _NATIVE_BRIDGE.log_pid_and_gate_state("WORLD_ENTER_VID_%d" % my_vid)
            _NATIVE_BRIDGE.dump_live_offsets("WORLD_ENTER")
            chat_notice("Avrasya2 Suite %s Aktif! [INSERT] Tiklanabilir Menu | [F6] Farm | [F11] Anim | [F12] Waithack" % SUITE_VERSION)

        if my_vid > 0:
            w_tag = "ACTIVE" if (self.farmer.enabled or self.combat.waithack_enabled) else "MANUAL"
            _NATIVE_BRIDGE.watch_live_transitions(tag=w_tag)

        if my_vid > 0 and len(self.radar.entities) > 0:
            if self.first_world_t <= 0.0:
                self.first_world_t = now
            elif not self.diag_logged and (now - self.first_world_t >= 3.5):
                inv_cnt = self.log_character_diagnostics()
                self.diag_attempts += 1
                if inv_cnt > 0 or self.diag_attempts >= 2:
                    self.diag_logged = True
                else:
                    self.first_world_t = now + 5.0

        self.ninja_anim.step(my_vid)
        self.farmer.step(my_vid, mx, my)
        self.combat.step(my_vid, mx, my, mz)
        self.world.step(my_vid, mx, my, mz)
        self.economy.step()
        self.looter.step()
        self.sustain.step(mx, my, combat_active=(self.farmer.enabled or self.combat.waithack_enabled))
        self.biyolog.step()
        self.cam_boost.step()

        if self.overlay is not None:
            try:
                self.overlay.update_visuals()
            except Exception as e:
                log_msg("update_visuals err: " + str(e), "ERROR")

        if self.menu_wnd is not None:
            try:
                self.menu_wnd.update_menu()
            except Exception as e:
                log_msg("update_menu err: " + str(e), "ERROR")

        now = time.clock()
        if my_vid > 0 and now - self.last_stats_log_t >= 8.0:
            self.last_stats_log_t = now
            cnt = self.radar.get_counts()
            log_msg(
                "[STATS] vid_cnt=%d metin=%d boss=%d mob=%d target=%d state=%s ninja=%s pos=(%d, %d)"
                % (
                    len(self.radar.entities),
                    cnt["metin"],
                    cnt["boss"],
                    cnt["monster"],
                    self.farmer.target_vid,
                    self.farmer.state_str,
                    "ON" if self.ninja_anim.applied else "OFF",
                    int(mx),
                    int(my),
                )
            )
            tag = "ACTIVE" if (self.farmer.enabled or self.combat.waithack_enabled) else "IDLE"
            _NATIVE_BRIDGE.dump_live_offsets(tag=tag)


# ============================================================================
# 9. BOOTSTRAP & STANDALONE SIMULATION TEST
# ============================================================================

_CONTROLLER = None


def bootstrap_in_client():
    global _CONTROLLER
    if _CONTROLLER is not None:
        return _CONTROLLER

    log_msg("Avrasya2 Suite %s bootstrap starting (PID=%s)..." % (
        SUITE_VERSION, str(os.getpid() if hasattr(os, "getpid") else "?")
    ))
    _NATIVE_BRIDGE.log_pid_and_gate_state("PID_BOOT")
    _CONTROLLER = SuiteController()
    setattr(sys, "_ui_frame_ctl", _CONTROLLER)

    # Try immediate overlay creation or hook ui.Window / game.GameWindow
    ov = build_hud_and_attach(_CONTROLLER)
    if ov is not None:
        _CONTROLLER.overlay = ov
        _CONTROLLER.hud = ov
        log_msg("Overlay attached immediately.")
        return _CONTROLLER

    # Deferred hook via __import__ until ui & wndMgr are ready
    try:
        import __builtin__
    except ImportError:
        import builtins as __builtin__
    orig_import = __builtin__.__import__
    logged_imports = set()

    def hooked_import(name, *args, **kwargs):
        mod = orig_import(name, *args, **kwargs)
        if name in ("introLogin", "introSelect", "introLoading", "networkModule", "game", "interfacemodule", "ui") and name not in logged_imports:
            logged_imports.add(name)
            _NATIVE_BRIDGE.log_pid_and_gate_state("IMPORT_" + str(name))
        if _CONTROLLER is not None and _CONTROLLER.overlay is None:
            if name in ("game", "interfacemodule", "introLogin", "ui", "networkModule"):
                try:
                    ov_new = build_hud_and_attach(_CONTROLLER)
                    if ov_new is not None:
                        _CONTROLLER.overlay = ov_new
                        _CONTROLLER.hud = ov_new
                        log_msg("Deferred overlay attached on import(%s)." % name)
                except Exception:
                    pass
        return mod

    __builtin__.__import__ = hooked_import
    return _CONTROLLER


def run_simulation_test():
    print("=== Avrasya2 Suite %s Simulation Test ===" % SUITE_VERSION)

    # Create mock C-API modules to verify trilateration, classification, W2S, and farm logic
    class MockMod(object):
        pass

    m_player = MockMod()
    m_chr = MockMod()
    m_nonplayer = MockMod()
    m_grp = MockMod()
    m_wndMgr = MockMod()
    m_net = MockMod()

    sim_state = {
        "mx": 478200.0,
        "my": 955000.0,
        "mz": 0.0,
        "selected_vid": 100,
        "entities": {
            2001: {"vnum": 8005, "name": "Uzuntu Metini", "type": 2, "event": 1, "grade": 0, "hp": 15000, "x": 479400.0, "y": 954200.0},
            2002: {"vnum": 191, "name": "Lykos", "type": 0, "event": 1, "grade": 4, "hp": 25000, "x": 477500.0, "y": 955900.0},
            2003: {"vnum": 102, "name": "Kurt", "type": 0, "event": 1, "grade": 0, "hp": 450, "x": 478320.0, "y": 955080.0},
            2004: {"vnum": 20104, "name": "Zirhli At", "type": 1, "event": 0, "grade": 0, "hp": 0, "x": 478220.0, "y": 955010.0},
            2005: {"vnum": 9003, "name": "Satici", "type": 1, "event": 2, "grade": 0, "hp": 0, "x": 478100.0, "y": 954900.0},
        },
    }
    sim_state["entities"][2001]["name"] = "Uzuntu Metini"

    m_player.GetMainCharacterIndex = lambda: 100
    m_player.GetMainCharacterPosition = lambda: (sim_state["mx"], sim_state["my"], sim_state["mz"])
    m_player.CanAttackInstance = lambda vid: 1 if vid in (2001, 2002, 2003) else 0
    m_player.GetCharacterDistance = lambda vid: (
        math.hypot(sim_state["entities"][vid]["x"] - sim_state["mx"], sim_state["entities"][vid]["y"] - sim_state["my"])
        if vid in sim_state["entities"] else -1.0
    )
    m_player.SetAttackKeyState = lambda st: None
    m_player.ComboAttack = lambda: None
    m_player.PickCloseItem = lambda: None
    m_player.GetStatus = lambda st: 1000

    m_chr.HasInstance = lambda vid: 1 if (vid == 100 or vid in sim_state["entities"]) else 0
    m_chr.GetVirtualNumber = lambda vid: sim_state["entities"][vid]["vnum"] if vid in sim_state["entities"] else 0
    m_chr.GetNameByVID = lambda vid: sim_state["entities"][vid]["name"] if vid in sim_state["entities"] else "None"
    m_chr.SelectInstance = lambda vid: sim_state.__setitem__("selected_vid", int(vid))
    m_chr.SetDirection = lambda d: sim_state.__setitem__("last_dir", int(d))
    m_chr.SetRotation = lambda deg: sim_state.__setitem__("last_rot_arg", float(deg))
    m_chr.BlendRotation = lambda deg, t: sim_state.__setitem__("last_blend_arg", float(deg))
    def sim_set_race(r):
        sim_state["race"] = int(r)
        sim_state["set_race_calls"] = sim_state.get("set_race_calls", 0) + 1
        # Simulate CActorInstance::SetRace (0x00600f70 -> 0x0059f630) zeroing m_v3Position!
        sim_state["mx"] = 0.0
        sim_state["my"] = 0.0
        sim_state["mz"] = 0.0

    m_chr.SetRace = sim_set_race
    m_chr.GetRace = lambda: sim_state.get("race", 0)
    m_chr.SetArmor = lambda a: sim_state.__setitem__("armor", int(a))
    m_chr.ChangeShape = lambda s: sim_state.__setitem__("shape", int(s))
    m_chr.SetWeapon = lambda w: sim_state.__setitem__("weapon", int(w))
    m_chr.SetMotionMode = lambda m: sim_state.__setitem__("motion_mode", int(m))
    m_chr.SetLoopMotion = lambda m: sim_state.__setitem__("loop_motion", int(m))
    m_chr.Refresh = lambda: None
    m_chr.testSetComboType = lambda c: sim_state.__setitem__("combo_type", int(c))
    m_chr.MoveToDestPosition = lambda vid, x, y: sim_state.__setitem__("last_dest", (int(vid), int(x), int(y)))

    def sim_set_pixel_pos(x, y, z):
        if sim_state["selected_vid"] == 100:
            sim_state["mx"] = float(x)
            sim_state["my"] = float(y)
            sim_state["mz"] = float(z)

    m_chr.SetPixelPosition = sim_set_pixel_pos

    m_nonplayer.IsMonsterStone = lambda vnum: 1 if vnum == 8005 else 0
    m_nonplayer.GetEventTypeByVID = lambda vid: sim_state["entities"][vid]["event"] if vid in sim_state["entities"] else 0
    m_nonplayer.GetEventType = lambda vnum: 1 if vnum in (8005, 191, 102) else 2
    m_nonplayer.GetGradeByVID = lambda vid: sim_state["entities"][vid]["grade"] if vid in sim_state["entities"] else 0
    m_nonplayer.GetMonsterMaxHP = lambda vnum: 15000 if vnum in (8005, 191, 102) else 0
    m_nonplayer.GetRaceNumByVID = lambda vid: sim_state["entities"][vid]["vnum"] if vid in sim_state["entities"] else -1
    m_nonplayer.GetMonsterName = lambda vnum: "Mob_%d" % vnum

    m_grp.GetCameraPosition = lambda: (478200.0, -956200.0, 650.0)
    m_grp.GetTargetPosition = lambda: (478200.0, -955000.0, 90.0)
    m_wndMgr.GetScreenWidth = lambda: 1280
    m_wndMgr.GetScreenHeight = lambda: 720
    m_net.SendOnClickPacket = lambda vid: sim_state.__setitem__("last_click_vid", int(vid))
    m_net.SendChatPacket = lambda txt: None
    m_net.SendRefinePacket = lambda slot, rtype: sim_state.__setitem__("last_refine", (int(slot), int(rtype)))

    sys.modules["player"] = m_player
    sys.modules["chr"] = m_chr
    sys.modules["nonplayer"] = m_nonplayer
    sys.modules["grp"] = m_grp
    sys.modules["wndMgr"] = m_wndMgr
    sys.modules["net"] = m_net

    ctrl = SuiteController()
    for vid in (2001, 2002, 2003, 2004, 2005):
        inf = ctrl.radar.classify_vid(vid, 100, m_chr, m_nonplayer, m_player)
        if inf is not None:
            ctrl.radar._merge_entity(vid, inf, time.clock())

    ctrl.radar.last_trilat_t = 0.0
    ctrl.radar.step_trilaterate(100, sim_state["mx"], sim_state["my"], sim_state["mz"], time.clock())
    ctrl.radar.last_w2s_t = 0.0
    ctrl.radar.step_screen_projection(100, sim_state["mx"], sim_state["my"], sim_state["mz"], time.clock())

    cnt = ctrl.radar.get_counts()
    print("Counts:", cnt)
    assert cnt["metin"] == 1, "Expected 1 metin"
    assert cnt["boss"] == 1, "Expected 1 boss"
    assert cnt["monster"] == 1, "Expected 1 monster"
    assert cnt["npc"] == 2, "Expected 2 NPCs (horse + shop)"

    for vid in (2001, 2002, 2003):
        ent = ctrl.radar.entities[vid]
        real_x = sim_state["entities"][vid]["x"]
        real_y = sim_state["entities"][vid]["y"]
        err = math.hypot(ent["x"] - real_x, ent["y"] - real_y)
        print("VID %d (%s): trilat=(%.1f, %.1f) real=(%.1f, %.1f) err=%.3f on_screen=%s" % (
            vid, ent["kind"], ent["x"], ent["y"], real_x, real_y, err, ent["on_screen"]
        ))
        assert err < 1.0, "Trilateration error too high: %.3f" % err

    picked = ctrl.radar.pick_target("all")
    print("Picked top priority target:", picked["vid"], picked["kind"], picked["name"])
    assert picked["vid"] == 2001 and picked["kind"] == "metin"

    # Verify rotation math (0x004b84a0 adds +180 deg, 0x0098fb80 table: N=0(180), E=2(90), S=4(0), W=6(270))
    ctrl.farmer.face_coords(100, 1000.0, 1000.0, 1100.0, 1000.0)  # East (+X) -> dir=2, internal=90, arg=270
    assert sim_state["last_dir"] == 2 and abs((sim_state["last_rot_arg"] + 180.0) % 360.0 - 90.0) < 0.01
    ctrl.farmer.face_coords(100, 1000.0, 1000.0, 1000.0, 900.0)   # North (-Y) -> dir=0, internal=180, arg=0
    assert sim_state["last_dir"] == 0 and abs((sim_state["last_rot_arg"] + 180.0) % 360.0 - 180.0) < 0.01

    # Verify Ninja Dual-Dagger animation transformation preserves exact world coords and never loops SetRace
    ctrl.ninja_anim.set_enabled(True, 100)
    ctrl.ninja_anim.step(100)
    ctrl.ninja_anim.step(100)
    assert sim_state["race"] == 1 and sim_state["armor"] == 11409 and sim_state["weapon"] == 1139 and sim_state["motion_mode"] == 4
    assert sim_state["set_race_calls"] == 1, "SetRace should only be called once, got %d" % sim_state["set_race_calls"]
    assert abs(sim_state["mx"] - 478200.0) < 1.0 and abs(sim_state["my"] - 955000.0) < 1.0, "Position was not restored after SetRace!"

    # Verify 360 Snap Waithack & Remote Refine & [INSERT] Menu Toggle
    ctrl.combat.waithack_enabled = True
    ctrl.combat.step(100, sim_state["mx"], sim_state["my"], sim_state["mz"])
    assert sim_state.get("last_click_vid") == 2003, "Waithack should target VID 2003 (Kurt at 1.44m)"
    assert abs(sim_state["mx"] - 478200.0) < 1.0 and abs(sim_state["my"] - 955000.0) < 1.0, "Waithack must restore position!"

    ctrl.economy.remote_refine_slot0(1)
    assert sim_state.get("last_refine") == (0, 1)

    assert ctrl.menu_visible is True
    ctrl.handle_hotkey(99, False, time.clock())
    assert ctrl.menu_visible is False
    ctrl.handle_hotkey(99, False, time.clock())
    assert ctrl.menu_visible is True

    print("Rotation, Waithack, Remote Refine, Ninja Anim & [INSERT] GUI verified!")
    print("=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_simulation_test()
    else:
        bootstrap_in_client()
else:
    bootstrap_in_client()
