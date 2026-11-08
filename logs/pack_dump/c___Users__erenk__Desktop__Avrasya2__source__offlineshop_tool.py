# DUMPED FROM LIVE COMPILE: C:\Users\erenk\Desktop\Avrasya2\source\offlineshop_tool.py (len=214256)
# -*- coding: ascii -*-
# c:/Users/erenk/Desktop/Avrasya2/source/offlineshop_tool.py
"""Avrasya2 Unified Bot & Market Automation Suite v2.0 (Python 2.7 / x86)

Pure-ASCII Python 2.7 module for metin2client.bin:
  1. Multi-Module Extensible GUI ([INSERT] or top-screen button):
     - Modul 1: PAZAR & FIRSATLAR (Pazar Arama, Al-Sat Kar, NPC Arbitraj, Harita Pazarlari, Canli Satislar)
     - Modul 2: OTO-MAGAZA & TICARET (Envanter -> Pazara Koy, Magazam & Oto-Fiyat, Envanter -> NPC Sat, Oto-Sniper, Kasa & Islem)
     - Modul 3: FARM & METIN BOTU (Canli Metin/Boss Radari, Harita Hedefleri, Farm Ayarlari, Oto-Pot & Kutsama, Oto-Toplama & SvSide)
     - Modul 4: SAVAS, EFSUN & ARACLAR (Waithack & Hiz, Kombo & Animasyon, Efsun Botu & Uzaktan +Bas/Biyolog, Harita/Wallhack/Kamera, Sistem)
  2. End-to-End Market & Shop Automation:
     - Auto-List Bought Items (Oto-Magazaya Koy): Automatically lists items bought via AL, Sniper, or Oto-Al-Sat
       into the player's own Offline Shop via offlineshop.SendAddItem at smart competitor-aware prices.
     - Auto-Create Shop: Opens a 5-day (7200m) Offline Shop via offlineshop.SendShopCreate if none is open.
     - Auto-Repricer (Oto-Fiyat Guncelle): Compares player's shop items against live competitors and updates prices
       via offlineshop.SendEditItem.
     - Auto-Safebox Withdraw (Oto-Kasa Cekim): Periodically checks offlineshop.SendSafeboxOpen and withdraws earned
       Yang (SendSafeboxGetValutes) and items (SendSafeboxGetItem) into inventory.
     - Auto-NPC Walk & Sell: Finds the nearest Shop NPC (9001..9010), walks within 2.6m, opens NPC shop, and sells
       NPC arbitrage items automatically without blocking background OfflineShop scanning.
"""

import os
import sys
import time
import math
import struct
import traceback
import __builtin__

try:
    import app
except Exception:
    app = None
try:
    import chr
except Exception:
    chr = None
try:
    import net
except Exception:
    net = None
try:
    import player
except Exception:
    player = None
try:
    import item
except Exception:
    item = None
try:
    import shop
except Exception:
    shop = None
try:
    import offlineshop
except Exception:
    offlineshop = None
try:
    import background
except Exception:
    background = None
try:
    import ui
except Exception:
    ui = None
try:
    import wndMgr
except Exception:
    wndMgr = None

SKILL_BOOK_NAMES = {
    1: "Uc Yonlu Kesme", 2: "Kilic Cevirme", 3: "Ofke", 4: "Hava Kilici", 5: "Hamle", 6: "Yasam Iradesi",
    16: "Ruh Vurusu", 17: "Siddetli Vurus", 18: "Guclu Vurus", 19: "Guclu Beden", 20: "Kilic Darbesi", 21: "Kilic Cemberi",
    31: "Suikast", 32: "Hizli Saldiri", 33: "Bicak Cevirme", 34: "Kamuflaj", 35: "Zehirli Bulut", 36: "Sinsi Zehir",
    46: "Tekrarlanan Atis", 47: "Ok Yagmuru", 48: "Atesli Ok", 49: "Hafif Adim", 50: "Zehirli Ok", 51: "Kivilcim Vurusu",
    61: "Parmak Darbesi", 62: "Ejderha Donusu", 63: "Buyulu Keskinlik", 64: "Dehset", 65: "Buyulu Zirh", 66: "Buyu Cozme",
    76: "Karanlik Vurus", 77: "Ates Vurusu", 78: "Ates Hayaleti", 79: "Karanlik Koruma", 80: "Hayalet Vurus", 81: "Karanlik Kure",
    91: "Ucan Tilsim", 92: "Ejderha Atisi", 93: "Ejderha Kukremesi", 94: "Kutsama", 95: "Yansitma", 96: "Ejderha Yardimi",
    106: "Simsek Atma", 107: "Simsek Cagirma", 108: "Simsek Pencesi", 109: "Iyilestirme", 110: "Hiz", 111: "Yuksek Saldiri",
}

TOOL_VERSION = "2.0.0"
SOURCE_DIR = r"C:\Users\erenk\Desktop\Avrasya2\source"
EXPORT_JSON_PATH = r"C:\Users\erenk\Desktop\Avrasya2\logs\offlineshop_market_dump.json"
EXPORT_TXT_PATH = r"C:\Users\erenk\Desktop\Avrasya2\logs\offlineshop_market_dump.txt"
TOOL_LOG_PATH = r"C:\Users\erenk\Desktop\Avrasya2\logs\offlineshop_tool.log"
NPC_CACHE_PATH = r"C:\Users\erenk\Desktop\Avrasya2\logs\offlineshop_npc_cache.txt"

# Static RVAs inside metin2client.bin (ImageBase = 0x00400000)
RVA_NET_STREAM_SINGLETON = 0x005C53C8   # CPythonNetworkStream* ms_singleton
RVA_OFFSHOP_SINGLETON = 0x005C54E0      # CPythonOfflineshop* ms_singleton
RVA_CHAR_MGR_SINGLETON = 0x005C47C0     # CPythonCharacterManager* ms_singleton
RVA_SEND_CLICK_SHOP = 0x000E8600        # __thiscall CPythonNetworkStream::SendOfflineshopClickShop(DWORD)
RVA_THUNK_THISCALL_1 = 0x003DBDE7       # __stdcall (this_ptr, fn_ptr, arg1) -> this->fn(arg1)
RVA_THUNK_THISCALL_2 = 0x003DBDF7       # __stdcall (this_ptr, fn_ptr, arg1, arg2) -> this->fn(arg1, arg2)
RVA_ENC_READ_A = 0x002DBD90             # __cdecl EncRead_A(void* field_addr, void* out_buf, uint32_t size)
RVA_ENC_MAP_COUNT = 0x002DC310          # __cdecl EncMapCount(void* map_handle)
RVA_ENC_MAP_BY_IDX = 0x002DC240         # __cdecl EncMapByIdx(void* map_h, int idx, void* out_p, uint32_t sz, uint32_t* out_sz)

SHOP_NPC_VNUMS = set([9001, 9002, 9003, 9004, 9007, 9008, 9009, 9010, 20094])
POTION_AND_SKIP_VNUMS = set([
    27001, 27002, 27003, 27004, 27005, 27006, 27007, 27008,
    27051, 27052, 27100, 27101, 27102, 27103, 27104, 27105,
    27201, 27202, 27203, 27204, 27205, 27206, 27207, 27208,
    27209, 27210, 27211, 27212, 50200, 72723, 72724, 72725,
    72726, 72727, 72728, 72729, 72730,
])

ATTR_MAX_HP = 1
ATTR_CON = 6
ATTR_INT = 9
ATTR_STR = 12
ATTR_DEX = 14
ATTR_CRIT = 15
ATTR_PENETRATE = 16
ATTR_HALF_HUMAN = 17
ATTR_UNDEAD = 21
ATTR_DEVIL = 22
ATTR_MONSTER = 63
ATTR_SKILL_DMG = 71
ATTR_AVG_DMG = 72

ATTR_SHORT_NAMES = {
    1: "HP",
    2: "SP",
    3: "Canlilik",
    4: "Zeka",
    5: "Guc",
    6: "Ceviklik",
    7: "SaldiriHizi",
    8: "HareketHizi",
    9: "BuyuHizi",
    10: "HP-Uretimi",
    12: "Zehirleme",
    13: "Sersemletme",
    14: "Yavaslatma",
    15: "Kritik",
    16: "Delici",
    17: "YariInsan",
    18: "Hayvan",
    19: "Ork",
    20: "Mistik",
    21: "Olumsuz",
    22: "Seytan",
    23: "HP-Absorbe",
    27: "Bloklama",
    28: "Ok-Koruma",
    29: "Kilic-Sav",
    30: "CiftEl-Sav",
    31: "Bicak-Sav",
    32: "Can-Sav",
    33: "Yelpaze-Sav",
    34: "Ok-Sav",
    37: "Buyu-Day",
    39: "Yansitma",
    41: "Zehir-Day",
    43: "EXP-Bonus",
    44: "Yang-Dusme",
    45: "Esya-Dusme",
    48: "Sersem-Bagisik",
    49: "Yavas-Bagisik",
    53: "SaldiriDegeri",
    63: "Canavar",
    71: "Beceri",
    72: "Ort.Zarar",
}


def _safe_ascii(val):
    if val is None:
        return ""
    s = str(val)
    out = []
    for ch in s:
        o = ord(ch)
        if 32 <= o <= 126:
            out.append(ch)
        elif o in (0xFD, 0xDD):
            out.append("i" if o == 0xFD else "I")
        elif o in (0xFE, 0xDE):
            out.append("s" if o == 0xFE else "S")
        elif o in (0xF0, 0xD0):
            out.append("g" if o == 0xF0 else "G")
        elif o in (0xFC, 0xDC):
            out.append("u" if o == 0xFC else "U")
        elif o in (0xF6, 0xD6):
            out.append("o" if o == 0xF6 else "O")
        elif o in (0xE7, 0xC7):
            out.append("c" if o == 0xE7 else "C")
        else:
            out.append(" ")
    return "".join(out)


def _fmt_yang(amount):
    try:
        v = int(amount)
    except Exception:
        return "0"
    if v < 0:
        return "-" + _fmt_yang(-v)
    s = str(v)
    parts = []
    while len(s) > 3:
        parts.append(s[-3:])
        s = s[:-3]
    parts.append(s)
    parts.reverse()
    return ".".join(parts)


def _fmt_yang_short(amount):
    try:
        v = float(amount)
    except Exception:
        return "0"
    if v >= 1000000000.0:
        return "%.2fT" % (v / 1000000000.0)
    if v >= 1000000.0:
        return "%.1fM" % (v / 1000000.0)
    if v >= 1000.0:
        if v < 100000.0 and (int(v) % 1000) >= 100:
            return "%.1fK" % (v / 1000.0)
        return "%.0fK" % (v / 1000.0)
    return "%d" % int(v)


def _round_market_price(val):
    v = max(1, int(val))
    if v >= 1000000:
        return (v // 10000) * 10000
    if v >= 100000:
        return (v // 2500) * 2500
    if v >= 10000:
        return (v // 500) * 500
    if v >= 1000:
        return (v // 100) * 100
    return v


def _tool_log(msg):
    try:
        open_fn = getattr(__builtin__, "open", open)
        f = open_fn(TOOL_LOG_PATH, "a")
        try:
            f.write("%s %s\n" % (time.strftime("%H:%M:%S"), _safe_ascii(msg)))
        finally:
            f.close()
    except Exception:
        pass


def _chat_notice(msg):
    try:
        chat_mod = sys.modules.get("chat")
        if chat_mod is not None and hasattr(chat_mod, "AppendChat"):
            chat_mod.AppendChat(1, "[AvrasyaBot] " + str(msg))
    except Exception:
        pass
    _tool_log(msg)


# ============================================================================
# 1. NATIVE SHOP & ENTITY ENGINE
# ============================================================================

class _NativeShopEngine(object):
    def __init__(self, ct_mod=None):
        self.ct = ct_mod
        self.exe_base = 0
        self._call_this1 = None
        self._call_this2 = None
        self._fn_enc_read_a = None
        self._fn_map_count = None
        self._fn_map_by_idx = None
        self._item_name_cache = {}
        self._skill_name_cache = {}
        self._mob_name_cache = {}
        self._item_npc_price_cache = {}
        self.last_click_pkt_t = 0.0
        self.min_click_interval = 0.22
        self._init_ctypes()

    def _init_ctypes(self):
        if self.ct is None:
            self.ct = sys.modules.get("ctypes")
            if self.ct is None:
                try:
                    import ctypes as ct
                    self.ct = ct
                except Exception:
                    return
        try:
            k32 = self.ct.windll.kernel32
            k32.GetModuleHandleA.argtypes = [self.ct.c_char_p]
            k32.GetModuleHandleA.restype = self.ct.c_uint32
            self.exe_base = int(k32.GetModuleHandleA(None) or 0x00400000) & 0xFFFFFFFF

            thunk1_addr = (self.exe_base + RVA_THUNK_THISCALL_1) & 0xFFFFFFFF
            proto1 = self.ct.WINFUNCTYPE(None, self.ct.c_uint32, self.ct.c_uint32, self.ct.c_uint32)
            self._call_this1 = proto1(thunk1_addr)

            thunk2_addr = (self.exe_base + RVA_THUNK_THISCALL_2) & 0xFFFFFFFF
            proto2 = self.ct.WINFUNCTYPE(self.ct.c_uint8, self.ct.c_uint32, self.ct.c_uint32, self.ct.c_uint32, self.ct.c_uint32)
            self._call_this2 = proto2(thunk2_addr)

            t_rw = self.ct.CFUNCTYPE(None, self.ct.c_uint32, self.ct.c_void_p, self.ct.c_uint32)
            t_cnt = self.ct.CFUNCTYPE(self.ct.c_int32, self.ct.c_uint32)
            t_idx = self.ct.CFUNCTYPE(self.ct.c_int32, self.ct.c_uint32, self.ct.c_int32, self.ct.c_void_p, self.ct.c_uint32, self.ct.c_void_p)
            self._fn_enc_read_a = t_rw((self.exe_base + RVA_ENC_READ_A) & 0xFFFFFFFF)
            self._fn_map_count = t_cnt((self.exe_base + RVA_ENC_MAP_COUNT) & 0xFFFFFFFF)
            self._fn_map_by_idx = t_idx((self.exe_base + RVA_ENC_MAP_BY_IDX) & 0xFFFFFFFF)
        except Exception as e:
            _tool_log("[ENGINE_INIT_ERR] %s" % e)

    def r32(self, addr):
        if self.ct is None or not addr or addr < 0x10000:
            return 0
        try:
            return int(self.ct.c_uint32.from_address(int(addr) & 0xFFFFFFFF).value) & 0xFFFFFFFF
        except Exception:
            return 0

    def r32_signed(self, addr):
        if self.ct is None or not addr or addr < 0x10000:
            return 0
        try:
            return int(self.ct.c_int32.from_address(int(addr) & 0xFFFFFFFF).value)
        except Exception:
            return 0

    def w32(self, addr, val):
        if self.ct is None or not addr or addr < 0x10000:
            return (1 == 0)
        try:
            self.ct.c_uint32.from_address(int(addr) & 0xFFFFFFFF).value = int(val) & 0xFFFFFFFF
            return (1 == 1)
        except Exception:
            return (1 == 0)

    def read_msvc_string(self, addr):
        if self.ct is None or not addr or addr < 0x10000:
            return ""
        try:
            sz = self.r32(addr + 0x10)
            cap = self.r32(addr + 0x14)
            if sz == 0 or sz > 256 or cap > 1024:
                return ""
            buf_ptr = self.r32(addr) if cap >= 16 else addr
            if buf_ptr < 0x10000:
                return ""
            return self.ct.string_at(buf_ptr, sz)
        except Exception:
            return ""

    def get_player_pos(self):
        try:
            pl = sys.modules.get("player")
            if pl is not None and hasattr(pl, "GetMainCharacterPosition"):
                pos = pl.GetMainCharacterPosition()
                if pos and len(pos) >= 2:
                    return (float(pos[0]), float(pos[1]))
        except Exception:
            pass
        return (0.0, 0.0)

    def get_player_name(self):
        try:
            pl = sys.modules.get("player")
            if pl is not None and hasattr(pl, "GetMainCharacterName"):
                return _safe_ascii(pl.GetMainCharacterName()).strip()
        except Exception:
            pass
        return ""

    def get_player_yang(self):
        try:
            pl = sys.modules.get("player")
            if pl is not None and hasattr(pl, "GetElk"):
                return int(pl.GetElk())
        except Exception:
            pass
        return 0

    def get_item_name(self, vnum):
        v = int(vnum)
        if v <= 0:
            return "Bilinmeyen"
        if v in self._item_name_cache:
            return self._item_name_cache[v]
        try:
            item_mod = sys.modules.get("item")
            if item_mod is not None and hasattr(item_mod, "SelectItem"):
                item_mod.SelectItem(v)
                raw_name = item_mod.GetItemName() if hasattr(item_mod, "GetItemName") else ""
                clean = _safe_ascii(raw_name).strip()
                if clean:
                    self._item_name_cache[v] = clean
                    return clean
        except Exception:
            pass
        fallback = "Vnum#%d" % v
        self._item_name_cache[v] = fallback
        return fallback

    def is_item_myshop_tradable(self, vnum):
        v = int(vnum)
        if v <= 0 or v in POTION_AND_SKIP_VNUMS:
            return (1 == 0)
        try:
            item_mod = sys.modules.get("item")
            if item_mod is not None and hasattr(item_mod, "SelectItem"):
                item_mod.SelectItem(v)
                af_myshop = getattr(item_mod, "ITEM_ANTIFLAG_MYSHOP", getattr(item_mod, "ANTIFLAG_MYSHOP", 0))
                af_give = getattr(item_mod, "ITEM_ANTIFLAG_GIVE", getattr(item_mod, "ANTIFLAG_GIVE", 0))
                if af_myshop and hasattr(item_mod, "IsAntiFlag") and item_mod.IsAntiFlag(af_myshop):
                    return (1 == 0)
                if af_give and hasattr(item_mod, "IsAntiFlag") and item_mod.IsAntiFlag(af_give):
                    return (1 == 0)
                return (1 == 1)
        except Exception:
            pass
        return (1 == 1)

    def get_item_npc_unit_price(self, vnum):
        v = int(vnum)
        if v <= 0:
            return 0
        if v in self._item_npc_price_cache:
            return self._item_npc_price_cache[v]
        val = 0
        try:
            item_mod = sys.modules.get("item")
            app_mod = sys.modules.get("app")
            if item_mod is not None and hasattr(item_mod, "SelectItem"):
                item_mod.SelectItem(v)
                anti_sell = getattr(item_mod, "ANTIFLAG_SELL", getattr(item_mod, "ITEM_ANTIFLAG_SELL", 0))
                if anti_sell and hasattr(item_mod, "IsAntiFlag") and item_mod.IsAntiFlag(anti_sell):
                    val = 0
                elif hasattr(item_mod, "Is1GoldItem") and item_mod.Is1GoldItem():
                    val = 0
                elif hasattr(item_mod, "GetISellItemPrice"):
                    raw_p = int(item_mod.GetISellItemPrice())
                    if not getattr(app_mod, "ENABLE_NO_SELL_PRICE_DIVIDED_BY_5", 0):
                        raw_p = raw_p // 5
                    val = max(0, int(raw_p))
        except Exception:
            val = 0
        self._item_npc_price_cache[v] = val
        return val

    def get_skill_name(self, skill_idx):
        sidx = int(skill_idx)
        if sidx <= 0:
            return ""
        if sidx in self._skill_name_cache:
            return self._skill_name_cache[sidx]
        clean = ""
        try:
            sk_mod = sys.modules.get("skill")
            if sk_mod is not None and hasattr(sk_mod, "GetSkillName"):
                raw = sk_mod.GetSkillName(sidx)
                clean = _safe_ascii(raw).strip()
        except Exception:
            clean = ""
        self._skill_name_cache[sidx] = clean
        return clean

    def get_mob_name(self, mob_vnum):
        mv = int(mob_vnum)
        if mv <= 0:
            return ""
        if mv in self._mob_name_cache:
            return self._mob_name_cache[mv]
        clean = ""
        try:
            np_mod = sys.modules.get("nonplayer")
            if np_mod is not None and hasattr(np_mod, "GetMonsterName"):
                raw = np_mod.GetMonsterName(mv)
                clean = _safe_ascii(raw).strip()
        except Exception:
            clean = ""
        self._mob_name_cache[mv] = clean
        return clean

    def get_item_full_name_and_key(self, vnum, sockets=None):
        v = int(vnum)
        base_name = self.get_item_name(v)
        sock0 = 0
        if sockets and len(sockets) > 0:
            try:
                sock0 = int(sockets[0])
            except Exception:
                sock0 = 0

        if v == 50300 and sock0 > 0:
            sk_name = self.get_skill_name(sock0)
            if sk_name:
                return ("%s BK" % sk_name, "50300:%d" % sock0)
            return ("BK (#%d)" % sock0, "50300:%d" % sock0)

        if v in (70037, 70055) and sock0 > 0:
            sk_name = self.get_skill_name(sock0)
            if sk_name:
                return ("%s Unutkanlik" % sk_name, "%d:%d" % (v, sock0))
            return ("%s (#%d)" % (base_name, sock0), "%d:%d" % (v, sock0))

        if v in (70104, 70105, 70106, 70107) and sock0 > 0:
            mob_name = self.get_mob_name(sock0)
            if mob_name:
                return ("%s Kuresi" % mob_name, "%d:%d" % (v, sock0))
            return ("%s (#%d)" % (base_name, sock0), "%d:%d" % (v, sock0))

        if v == 50026 and sock0 > 0:
            return ("%s (%s)" % (base_name, _fmt_yang_short(sock0)), "50026:%d" % sock0)

        return (base_name, str(v))

    def get_slot_npc_sell_price(self, slot, vnum, count):
        val = 0
        try:
            pl_mod = sys.modules.get("player")
            inven_type = getattr(pl_mod, "INVENTORY", 1) if pl_mod else 1
            if pl_mod is not None and hasattr(pl_mod, "GetISellItemPrice"):
                try:
                    val = int(pl_mod.GetISellItemPrice(inven_type, int(slot)))
                except TypeError:
                    val = int(pl_mod.GetISellItemPrice(int(slot)))
        except Exception:
            val = 0
        fallback_val = int(self.get_item_npc_unit_price(vnum) * max(1, int(count)))
        if val <= 0 or (fallback_val > 0 and val > fallback_val * 5):
            return fallback_val
        return val

    def get_player_xy(self):
        px, py = self.get_player_pos()
        return (int(px), int(py), 0)

    def move_character_to_xy(self, tx, ty):
        try:
            pl_mod = sys.modules.get("player")
            chr_mod = sys.modules.get("chr")
            my_vid = int(pl_mod.GetMainCharacterIndex()) if (pl_mod and hasattr(pl_mod, "GetMainCharacterIndex")) else 0
            if my_vid > 0 and chr_mod is not None and hasattr(chr_mod, "MoveToDestPosition"):
                chr_mod.MoveToDestPosition(my_vid, int(tx), int(ty))
                return (1 == 1)
        except Exception as e:
            _tool_log("[MOVE_ERR] %s" % e)
        return (1 == 0)

    def teleport_character_to_xy(self, tx, ty):
        try:
            pl_mod = sys.modules.get("player")
            chr_mod = sys.modules.get("chr")
            my_vid = int(pl_mod.GetMainCharacterIndex()) if (pl_mod and hasattr(pl_mod, "GetMainCharacterIndex")) else 0
            if my_vid > 0 and chr_mod is not None:
                if hasattr(chr_mod, "SelectInstance"):
                    chr_mod.SelectInstance(my_vid)
                if hasattr(chr_mod, "SetPixelPosition"):
                    chr_mod.SetPixelPosition(int(tx), int(ty))
                    return (1 == 1)
        except Exception as e:
            _tool_log("[TELE_ERR] %s" % e)
        return self.move_character_to_xy(tx, ty)

    def enumerate_map_entities(self, only_targets=(1 == 0)):
        """Enumerates alive map instances directly via EncMapCount/EncMapByIdx in < 0.05ms."""
        if self.ct is None or self._fn_map_count is None:
            self._init_ctypes()
        if self.ct is None or self._fn_map_count is None:
            return []
        try:
            cm = self.r32(self.exe_base + RVA_CHAR_MGR_SINGLETON)
            if cm < 0x10000:
                return []
            map_h = self.r32(cm + 0x20)
            if map_h < 0x10000:
                return []
            cnt = int(self._fn_map_count(map_h))
            if cnt <= 0 or cnt > 2048:
                return []

            px, py = self.get_player_pos()
            chr_mod = sys.modules.get("chr")
            np_mod = sys.modules.get("nonplayer")
            pl_mod = sys.modules.get("player")
            my_vid = int(pl_mod.GetMainCharacterIndex()) if (pl_mod and hasattr(pl_mod, "GetMainCharacterIndex")) else 0

            inst = self.ct.c_uint32(0)
            out_sz = self.ct.c_uint32(0)
            u_buf = self.ct.c_uint32(0)
            f_buf = self.ct.c_float(0.0)
            out = []

            for i in xrange(cnt):
                inst.value = 0
                out_sz.value = 0
                ok = int(self._fn_map_by_idx(map_h, i, self.ct.byref(inst), 4, self.ct.byref(out_sz)))
                if not ok or int(out_sz.value) != 4 or inst.value < 0x10000:
                    continue
                p = int(inst.value) & 0xFFFFFFFF
                self._fn_enc_read_a(p + 0x75C, self.ct.byref(u_buf), 4)
                vid = int(u_buf.value)
                if vid <= 0 or vid == my_vid:
                    continue
                self._fn_enc_read_a(p + 0x170, self.ct.byref(u_buf), 4)
                vnum = int(u_buf.value)
                self._fn_enc_read_a(p + 0x5E8, self.ct.byref(u_buf), 4)
                atype = int(u_buf.value)
                self._fn_enc_read_a(p + 0x654, self.ct.byref(f_buf), 4)
                ix = float(f_buf.value)
                self._fn_enc_read_a(p + 0x658, self.ct.byref(f_buf), 4)
                iy = abs(float(f_buf.value))

                # Distance in game units (divide by 100 for meters)
                dist = int(math.hypot(ix - px, iy - py)) if (px > 0.0 or py > 0.0) else 0
                raw_nm = ""
                if chr_mod is not None and hasattr(chr_mod, "GetNameByVID"):
                    try:
                        raw_nm = chr_mod.GetNameByVID(vid)
                    except Exception:
                        raw_nm = ""
                if (not raw_nm or raw_nm == "None") and np_mod is not None and hasattr(np_mod, "GetMonsterName"):
                    try:
                        raw_nm = np_mod.GetMonsterName(vnum)
                    except Exception:
                        raw_nm = ""
                nm = _safe_ascii(raw_nm).strip() or ("Vnum#%d" % vnum)

                kind = "mob"
                cat = "MOB"
                if atype == 2 or (8000 <= vnum <= 8999) or "metin" in nm.lower():
                    kind = "metin"
                    cat = "METIN"
                elif 20047 <= vnum <= 20059 or 30301 <= vnum <= 30305:
                    kind = "ore"
                    cat = "MADEN"
                elif atype == 1 or (9000 <= vnum <= 20999) or (29000 <= vnum <= 35999):
                    kind = "npc"
                    cat = "NPC"
                elif atype == 6:
                    kind = "player"
                    cat = "PLAYER"
                elif vnum in (191, 192, 193, 194, 491, 492, 493, 494, 591, 691, 791, 991, 992, 993, 1091, 1092, 1093, 1191, 1192, 1304, 1901, 2091, 2191, 2206, 2306, 2491, 2492, 2493, 2598, 3090, 3091, 3190, 3191, 3290, 3291):
                    kind = "boss"
                    cat = "BOSS"

                if only_targets and cat not in ("METIN", "BOSS", "MOB", "MADEN"):
                    continue

                out.append({
                    "vid": vid,
                    "vnum": vnum,
                    "actor_type": atype,
                    "kind": kind,
                    "category": cat,
                    "name": nm,
                    "x": int(ix),
                    "y": int(iy),
                    "dist": dist,
                    "inst_ptr": p,
                })
            out.sort(key=lambda e: (e["category"] != "METIN", e["category"] != "BOSS", e["dist"]))
            return out
        except Exception as e:
            _tool_log("[ENUM_ENT_ERR] %s" % e)
            return []

    def find_nearest_shop_npc(self):
        entities = self.enumerate_map_entities(only_targets=(1 == 0))
        npcs = [e for e in entities if e["vnum"] in SHOP_NPC_VNUMS]
        if npcs:
            npcs.sort(key=lambda e: e["dist"])
            return npcs[0]
        for e in entities:
            if e["kind"] == "npc" and any(k in e["name"].lower() for k in ("satici", "market", "zirh", "silah")):
                return e
        return None

    def get_map_shops(self):
        if self.ct is None or not self.exe_base:
            self._init_ctypes()
        if self.ct is None or not self.exe_base:
            return []

        off_inst = self.r32(self.exe_base + RVA_OFFSHOP_SINGLETON)
        if off_inst < 0x10000:
            return []

        vec_begin = self.r32(off_inst + 0x1C)
        vec_end = self.r32(off_inst + 0x20)
        if vec_begin < 0x10000 or vec_end < vec_begin:
            return []

        count = (vec_end - vec_begin) // 4
        if count <= 0 or count > 2000:
            return []

        px, py = self.get_player_pos()
        shops = []
        for i in xrange(count):
            ptr = self.r32(vec_begin + i * 4)
            if ptr < 0x10000:
                continue
            vid = self.r32(ptr + 0x2B4)
            race = self.r32(ptr + 0x2B8)
            raw_sign = self.read_msvc_string(ptr + 0x2BC)
            sx = self.r32_signed(ptr + 0x2D4)
            sy = self.r32_signed(ptr + 0x2D8)

            if "@" in raw_sign:
                at_idx = raw_sign.find("@")
                owner_raw = raw_sign[:at_idx]
                title_raw = raw_sign[at_idx + 1:]
            else:
                owner_raw = raw_sign
                title_raw = raw_sign

            dist = 0
            if px > 0.0 or py > 0.0:
                dx = float(sx) - px
                dy = float(sy) - py
                dist = int(math.sqrt(dx * dx + dy * dy))

            shops.append({
                "vid": int(vid),
                "owner_id": int(vid),
                "db_owner_id": 0,
                "race": int(race),
                "raw_sign": raw_sign,
                "owner": _safe_ascii(owner_raw).strip() or ("ID#%d" % vid),
                "title": _safe_ascii(title_raw).strip(),
                "x": int(sx),
                "y": int(sy),
                "dist": int(dist),
                "ptr": int(ptr),
                "scanned": (1 == 0),
                "item_count": 0,
            })
        return shops

    def scan_map_shops(self):
        lst = self.get_map_shops()
        out = {}
        for s in lst:
            out[int(s["vid"])] = s
        return out

    def send_click_shop_packet(self, shop_vid, force=(1 == 0)):
        if self.ct is None or self._call_this1 is None:
            self._init_ctypes()
        if self.ct is None or self._call_this1 is None:
            return (1 == 0)
        try:
            now = time.clock() if hasattr(time, "clock") else time.time()
            min_gap = 0.30 if force else self.min_click_interval
            if (now - self.last_click_pkt_t) < min_gap:
                return (1 == 0)
            net_stream = self.r32(self.exe_base + RVA_NET_STREAM_SINGLETON)
            if net_stream < 0x10000:
                return (1 == 0)
            self.w32(net_stream + 0xAC, 0)
            fn_addr = (self.exe_base + RVA_SEND_CLICK_SHOP) & 0xFFFFFFFF
            self.last_click_pkt_t = now
            self._call_this1(net_stream, fn_addr, int(shop_vid) & 0xFFFFFFFF)
            return (1 == 1)
        except Exception as e:
            _tool_log("[CLICK_SHOP_ERR] vid=%s err=%s" % (shop_vid, e))
            return (1 == 0)


# ============================================================================
# 2. OFFLINE SHOP DATABASE & SMART PRICING ENGINE
# ============================================================================

class OfflineShopDatabase(object):
    def __init__(self, engine):
        self.engine = engine
        self.map_shops = {}
        self.map_shops_by_sign = {}
        self.map_shops_by_owner = {}
        self.vid_by_owner_id = {}
        self.owner_id_by_vid = {}
        self.scanned_shops = {}
        self.items_by_shop = {}
        self.all_items = []
        self.vnum_stats = {}
        self.bargains = []
        self.npc_bargains = []
        self.npc_arbitrage_vnums = set()
        self.bought_vnums = set()
        self.bought_item_names = set()
        self.our_bought_item_ids = set()
        self.real_sales_by_key = {}
        self.sales_feed = []
        self.total_live_sales = 0
        self.budget_filter_only = (1 == 0)
        self.npc_sniped_ids = set()
        self.flip_sniped_ids = set()
        self.sniper_rules = []
        self.sniper_enabled = (1 == 0)
        self.auto_flip_enabled = (1 == 0)
        self.auto_list_bought = (1 == 1)
        self.auto_safebox_enabled = (1 == 1)
        self.pricing_mode = 0           # 0=Rekabetci (-2%), 1=Medyan (Dengeli), 2=Yuksek Kar (+10%)
        self.pricing_strategy = 0
        self.sniper_log = []
        self.automation_log = []
        self.auto_events_log = []
        self.sniper_buy_cb = None

        # Player's Own Offline Shop state
        self.my_owner_id = 0
        self.my_shop_open = (1 == 0)
        self.my_shop_name = ""
        self.my_shop_title = "PAZAR"
        self.my_shop_duration = 0
        self.my_shop_last_sync_ts = 0.0
        self.my_shop_items = []         # parsed items currently on sale in our own shop
        self.my_shop_sold = []
        self.my_shop_raw_info = {}
        self.my_shop_raw_items = []
        self.my_shop_raw_sold = []
        self.safebox_yang = 0
        self.safebox_items = []
        self.my_safebox_yang = 0
        self.my_safebox_items = []
        self.total_npc_sold_yang = 0

        self.revision = 0
        self._load_npc_cache()

    def log_auto_event(self, text):
        ts = time.strftime("%H:%M:%S")
        clean_msg = _safe_ascii(text)
        line = "%s %s" % (ts, clean_msg)
        self.automation_log.insert(0, line)
        self.auto_events_log.insert(0, {"ts": ts, "msg": clean_msg})
        if len(self.automation_log) > 100:
            self.automation_log = self.automation_log[:100]
        if len(self.auto_events_log) > 100:
            self.auto_events_log = self.auto_events_log[:100]
        self.revision += 1

    def record_npc_sale(self, amount):
        val = max(0, int(amount))
        self.total_npc_sold_yang += val
        self.log_auto_event("NPC SATIS GELIRI: +%s Yang" % _fmt_yang(val))

    def _load_npc_cache(self):
        open_fn = getattr(__builtin__, "open", open)
        try:
            if os.path.exists(NPC_CACHE_PATH):
                f = open_fn(NPC_CACHE_PATH, "r")
                try:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) >= 2 and parts[0].isdigit():
                            v = int(parts[0])
                            if v > 0:
                                self.npc_arbitrage_vnums.add(v)
                                self.bought_vnums.add(v)
                            nm = parts[1].strip().lower()
                            if nm:
                                self.bought_item_names.add(nm)
                finally:
                    f.close()
        except Exception:
            pass

    def record_bought_item(self, item_rec):
        if not isinstance(item_rec, dict):
            return
        vnum = int(item_rec.get("vnum", 0))
        iid = int(item_rec.get("id", 0))
        nm = str(item_rec.get("base_name", "") or item_rec.get("name", "")).strip().lower()
        if iid > 0:
            self.our_bought_item_ids.add(iid)
        if vnum > 0:
            self.bought_vnums.add(vnum)
            npc_u = self.engine.get_item_npc_unit_price(vnum)
            if int(item_rec.get("npc_profit", 0)) > 0 or (npc_u > 0 and int(item_rec.get("unit_price", 0)) <= npc_u):
                self.npc_arbitrage_vnums.add(vnum)
        if nm:
            self.bought_item_names.add(nm)
        try:
            open_fn = getattr(__builtin__, "open", open)
            f = open_fn(NPC_CACHE_PATH, "a")
            try:
                f.write("%d|%s\n" % (vnum, nm))
            finally:
                f.close()
        except Exception:
            pass

    def is_our_own_shop(self, owner_id, seller_name=""):
        if self.my_owner_id > 0 and int(owner_id) == self.my_owner_id:
            return (1 == 1)
        my_nm = self.engine.get_player_name().lower()
        if my_nm and seller_name and str(seller_name).lower().strip() == my_nm:
            return (1 == 1)
        return (1 == 0)

    def ingest_my_shop(self, shop_info, raw_items, raw_sold=None):
        """Captures and parses the player's own Offline Shop state."""
        try:
            oid = int(shop_info.get("owner_id", 0))
        except Exception:
            oid = 0
        if oid > 0:
            self.my_owner_id = oid
        self.my_shop_open = (1 == 1)
        self.my_shop_duration = int(shop_info.get("duration", 0))
        raw_name = str(shop_info.get("name", ""))
        self.my_shop_name = raw_name
        if "@" in raw_name:
            self.my_shop_title = _safe_ascii(raw_name.split("@", 1)[1]).strip() or "PAZAR"
        elif raw_name:
            self.my_shop_title = _safe_ascii(raw_name).strip() or "PAZAR"

        self.my_shop_raw_info = dict(shop_info)
        self.my_shop_raw_items = list(raw_items) if raw_items else []
        self.my_shop_raw_sold = list(raw_sold) if raw_sold is not None else list(self.my_shop_raw_sold)

        # Remove our own shop from competitor items_by_shop if it was previously scanned as a foreign shop
        if oid > 0 and oid in self.items_by_shop:
            self.items_by_shop.pop(oid, None)

        parsed = []
        for it in self.my_shop_raw_items:
            if not isinstance(it, dict):
                continue
            iid = int(it.get("id", 0))
            vnum = int(it.get("vnum", 0))
            if vnum <= 0 or iid <= 0:
                continue
            cnt = max(1, int(it.get("count", 1)))
            price = int(it.get("price", 0))
            unit_p = int(price // cnt)
            raw_sockets = it.get("socket", {})
            sockets = [int(raw_sockets.get(s_i, 0)) for s_i in xrange(6)]
            raw_attrs = it.get("attr", {})
            attrs = []
            avg_dmg = 0
            for a_i in xrange(7):
                ae = raw_attrs.get(a_i)
                if isinstance(ae, dict):
                    at, av = int(ae.get("type", 0)), int(ae.get("value", 0))
                elif isinstance(ae, (tuple, list)) and len(ae) >= 2:
                    at, av = int(ae[0]), int(ae[1])
                else:
                    at, av = 0, 0
                attrs.append((at, av))
                if at == ATTR_AVG_DMG:
                    avg_dmg = av

            name, mkey = self.engine.get_item_full_name_and_key(vnum, sockets)
            st = self.vnum_stats.get(mkey) or self.vnum_stats.get(vnum)
            comp_min = st["min_unit"] if st else 0
            comp_med = st["median_unit"] if st else 0
            opt_unit = self.compute_smart_unit_price_for_key(mkey, vnum, current_unit=unit_p)
            opt_total = int(opt_unit * cnt)

            if comp_min <= 0:
                status_str = "TEK SATICI"
            elif unit_p < int(comp_min * 0.85):
                status_str = "COK UCUZ (Rakip:%s)" % _fmt_yang_short(comp_min)
            elif unit_p <= comp_min:
                status_str = "EN UCUZ (Rakip:%s)" % _fmt_yang_short(comp_min)
            else:
                status_str = "PAHALI (Rakip:%s)" % _fmt_yang_short(comp_min)

            parsed.append({
                "id": iid,
                "owner_id": oid,
                "vnum": vnum,
                "market_key": mkey,
                "name": name,
                "name_lower": name.lower(),
                "count": cnt,
                "price": price,
                "unit_price": unit_p,
                "comp_min": comp_min,
                "comp_med": comp_med,
                "min_other": comp_min,
                "unique_sellers": int(st["unique_sellers"]) if st else 1,
                "opt_unit": opt_unit,
                "opt_total": opt_total,
                "smart_unit": opt_unit,
                "smart_total": opt_total,
                "status_str": status_str,
                "status": status_str,
                "sockets": sockets,
                "attrs": attrs,
                "avg_dmg": avg_dmg,
            })

        self.my_shop_items = parsed
        self.my_shop_sold = list(self.my_shop_raw_sold)
        self.my_shop_last_sync_ts = time.time()
        self._rebuild_aggregates()
        self.revision += 1

    def compute_smart_unit_price_for_key(self, mkey, vnum, buy_unit=0, current_unit=0):
        """Computes optimal resale unit price based on live competitor stats and pricing_mode."""
        self.pricing_mode = getattr(self, "pricing_strategy", self.pricing_mode)
        st = self.vnum_stats.get(mkey) or self.vnum_stats.get(int(vnum))
        target_u = 0
        if st:
            min_u = int(st.get("min_unit", 0))
            sec_u = int(st.get("second_min_unit", min_u))
            med_u = int(st.get("median_unit", min_u))
            offers = int(st.get("offers", 1))

            # If we just bought the lowest outlier (min_u == buy_unit), base competitor price on sec_u
            comp_ref = sec_u if (buy_unit > 0 and min_u <= buy_unit and sec_u > buy_unit) else min_u
            if offers >= 3 and comp_ref < int(med_u * 0.60):
                comp_ref = sec_u if sec_u >= int(med_u * 0.65) else med_u

            if self.pricing_mode == 0:
                # Fast turnover: 2% below lowest serious competitor
                target_u = int(comp_ref * 0.98) if comp_ref > 1000 else comp_ref
            elif self.pricing_mode == 1:
                # Balanced median
                target_u = med_u
            else:
                # High margin (+10% over median)
                target_u = int(med_u * 1.10)

        if target_u <= 0:
            if current_unit > 0:
                target_u = current_unit
            elif buy_unit > 0:
                target_u = int(buy_unit * 1.35)
            else:
                npc_u = self.engine.get_item_npc_unit_price(vnum)
                if int(vnum) == 50300:
                    target_u = 25000
                elif 28000 <= int(vnum) <= 28499:
                    target_u = 15000
                elif npc_u > 0:
                    target_u = max(5000, npc_u * 3)
                else:
                    target_u = 15000

        if buy_unit > 0:
            min_floor = int(buy_unit * 1.18)
            if target_u < min_floor:
                target_u = min_floor

        return _round_market_price(target_u)

    def compute_smart_resale_unit_price(self, item_rec):
        if not isinstance(item_rec, dict):
            return 10000
        mkey = item_rec.get("market_key", str(item_rec.get("vnum", 0)))
        vnum = int(item_rec.get("vnum", 0))
        buy_u = int(item_rec.get("unit_price", 0))
        return self.compute_smart_unit_price_for_key(mkey, vnum, buy_unit=buy_u)

    def refresh_map_shops(self):
        lst = self.engine.get_map_shops()
        new_map = {}
        by_sign = {}
        by_owner = {}
        for s in lst:
            vid = int(s["vid"])
            new_map[vid] = s
            if s["raw_sign"]:
                by_sign[s["raw_sign"]] = s
            owner_key = s["owner"].lower().strip()
            if owner_key:
                by_owner[owner_key] = s

            db_oid = self.owner_id_by_vid.get(vid, 0)
            if db_oid <= 0:
                for sc_oid, sc_info in self.scanned_shops.items():
                    if sc_info.get("owner", "").lower().strip() == owner_key and owner_key:
                        db_oid = int(sc_oid)
                        self.owner_id_by_vid[vid] = db_oid
                        self.vid_by_owner_id[db_oid] = vid
                        break

            if db_oid > 0 and db_oid in self.scanned_shops:
                sc = self.scanned_shops[db_oid]
                sc["shop_vid"] = vid
                sc["x"] = s["x"]
                sc["y"] = s["y"]
                sc["dist"] = s["dist"]
                s["db_owner_id"] = db_oid
                s["scanned"] = (1 == 1)
                s["item_count"] = sc.get("count", 0)
                for it in self.items_by_shop.get(db_oid, []):
                    it["shop_vid"] = vid
                    it["x"] = s["x"]
                    it["y"] = s["y"]
                    it["dist"] = s["dist"]

        self.map_shops = new_map
        self.map_shops_by_sign = by_sign
        self.map_shops_by_owner = by_owner
        self.revision += 1
        return lst

    def update_map_shops(self, shops=None):
        self.refresh_map_shops()
        return self.map_shops

    def ingest_open_shop(self, shop_info, raw_items, clicked_vid=0):
        return self.ingest_opened_shop(shop_info, raw_items, clicked_vid=clicked_vid)

    def resolve_shop_vid(self, target):
        if isinstance(target, dict):
            if int(target.get("vid", 0)) > 0 and int(target.get("vid", 0)) in self.map_shops:
                return int(target["vid"])
            if int(target.get("shop_vid", 0)) > 0 and int(target.get("shop_vid", 0)) in self.map_shops:
                return int(target["shop_vid"])
            oid = int(target.get("owner_id", 0))
            if oid in self.map_shops:
                return oid
            if oid in self.vid_by_owner_id and self.vid_by_owner_id[oid] in self.map_shops:
                return int(self.vid_by_owner_id[oid])
            seller = str(target.get("seller", "") or target.get("owner", "")).lower().strip()
            if seller and seller in self.map_shops_by_owner:
                return int(self.map_shops_by_owner[seller]["vid"])
            if int(target.get("shop_vid", 0)) > 0:
                return int(target["shop_vid"])
            if int(target.get("vid", 0)) > 0:
                return int(target["vid"])
            return oid

        try:
            val = int(target)
        except Exception:
            return 0
        if val in self.map_shops:
            return val
        if val in self.vid_by_owner_id:
            return int(self.vid_by_owner_id[val])
        if val in self.scanned_shops:
            sv = int(self.scanned_shops[val].get("shop_vid", 0))
            if sv > 0:
                return sv
            seller = self.scanned_shops[val].get("owner", "").lower().strip()
            if seller in self.map_shops_by_owner:
                return int(self.map_shops_by_owner[seller]["vid"])
        return val

    def get_map_shop_for_target(self, target):
        vid = self.resolve_shop_vid(target)
        if vid in self.map_shops:
            return self.map_shops[vid]
        if isinstance(target, dict):
            seller = str(target.get("seller", "") or target.get("owner", "")).lower().strip()
            if seller in self.map_shops_by_owner:
                return self.map_shops_by_owner[seller]
        return {}

    def ingest_opened_shop(self, shop_info, raw_items, clicked_vid=0):
        try:
            owner_id = int(shop_info.get("owner_id", 0))
        except Exception:
            return
        if owner_id <= 0:
            return

        # If this is our own shop, route to ingest_my_shop instead of foreign market items!
        if shop_info.get("my_shop") or self.is_our_own_shop(owner_id):
            self.ingest_my_shop(shop_info, raw_items)
            return

        raw_name = str(shop_info.get("name", ""))
        if "@" in raw_name:
            at = raw_name.find("@")
            owner_str = _safe_ascii(raw_name[:at]).strip()
            title_str = _safe_ascii(raw_name[at + 1:]).strip()
        else:
            owner_str = _safe_ascii(raw_name).strip()
            title_str = owner_str

        if self.is_our_own_shop(owner_id, owner_str):
            self.ingest_my_shop(shop_info, raw_items)
            return

        mshop = None
        if owner_id in self.vid_by_owner_id:
            mshop = self.map_shops.get(self.vid_by_owner_id[owner_id])
        if mshop is None and raw_name and raw_name in self.map_shops_by_sign:
            mshop = self.map_shops_by_sign[raw_name]
        if mshop is None and owner_str and owner_str.lower() in self.map_shops_by_owner:
            mshop = self.map_shops_by_owner[owner_str.lower()]
        if mshop is None and clicked_vid and int(clicked_vid) in self.map_shops:
            mshop = self.map_shops[int(clicked_vid)]

        shop_vid = int(mshop["vid"]) if mshop else int(self.vid_by_owner_id.get(owner_id, clicked_vid or 0))
        if shop_vid > 0:
            self.vid_by_owner_id[owner_id] = shop_vid
            self.owner_id_by_vid[shop_vid] = owner_id
            if mshop is not None:
                mshop["db_owner_id"] = owner_id
                mshop["scanned"] = (1 == 1)

        mshop_dict = mshop if mshop is not None else {}
        sx = int(mshop_dict.get("x", 0))
        sy = int(mshop_dict.get("y", 0))
        dist = int(mshop_dict.get("dist", 0))
        if not owner_str:
            owner_str = mshop_dict.get("owner", "ID#%d" % owner_id)
        if not title_str:
            title_str = mshop_dict.get("title", "")

        parsed_items = []
        new_item_ids = set()
        for idx, it in enumerate(raw_items):
            if not isinstance(it, dict):
                continue
            item_id = int(it.get("id", 0))
            vnum = int(it.get("vnum", 0))
            if vnum <= 0 or item_id <= 0:
                continue
            new_item_ids.add(item_id)
            count = max(1, int(it.get("count", 1)))
            price = int(it.get("price", 0))
            trans = int(it.get("trans", 0))
            unit_price = int(price // count)

            raw_sockets = it.get("socket", {})
            sockets = []
            for s_idx in xrange(6):
                sockets.append(int(raw_sockets.get(s_idx, 0)))

            base_name = self.engine.get_item_name(vnum)
            name, market_key = self.engine.get_item_full_name_and_key(vnum, sockets)

            raw_attrs = it.get("attr", {})
            attrs = []
            avg_dmg = 0
            skill_dmg = 0
            bonus_parts = []
            has_bonus = (1 == 0)
            for a_idx in xrange(7):
                a_entry = raw_attrs.get(a_idx)
                if isinstance(a_entry, dict):
                    atype = int(a_entry.get("type", 0))
                    aval = int(a_entry.get("value", 0))
                elif isinstance(a_entry, (tuple, list)) and len(a_entry) >= 2:
                    atype = int(a_entry[0])
                    aval = int(a_entry[1])
                else:
                    atype, aval = 0, 0
                attrs.append((atype, aval))
                if atype != 0 and aval != 0:
                    has_bonus = (1 == 1)
                    if atype == ATTR_AVG_DMG:
                        avg_dmg = aval
                    elif atype == ATTR_SKILL_DMG:
                        skill_dmg = aval
                    bname = ATTR_SHORT_NAMES.get(atype, "Ef#%d" % atype)
                    bonus_parts.append("%s:%+d" % (bname, aval))

            if trans > 0:
                bonus_parts.insert(0, "Yansitma:%d" % trans)

            npc_unit = self.engine.get_item_npc_unit_price(vnum)
            npc_total = int(npc_unit * count)
            npc_profit = max(0, int(npc_total - price)) if price > 0 else 0
            if npc_profit > 0:
                bonus_parts.insert(0, "NPC_KAR:+%s" % _fmt_yang_short(npc_profit))

            bonus_summary = " ".join(bonus_parts[:4]) if bonus_parts else "-"

            rec = {
                "id": item_id,
                "owner_id": owner_id,
                "shop_vid": shop_vid,
                "seller": owner_str,
                "shop_title": title_str,
                "vnum": vnum,
                "market_key": market_key,
                "base_name": base_name,
                "name": name,
                "name_lower": ("%s %s" % (name, base_name)).lower(),
                "count": count,
                "price": price,
                "unit_price": unit_price,
                "npc_unit": npc_unit,
                "npc_total": npc_total,
                "npc_profit": npc_profit,
                "trans": trans,
                "sockets": sockets,
                "attrs": attrs,
                "has_bonus": has_bonus,
                "avg_dmg": avg_dmg,
                "skill_dmg": skill_dmg,
                "bonus_summary": bonus_summary,
                "x": sx,
                "y": sy,
                "dist": dist,
                "discount_pct": 0,
                "avg_ref": unit_price,
                "target_sell_unit": unit_price,
                "flip_profit": 0,
                "roi_pct": 0,
                "demand_tier": 1,
                "demand_label": "DENGELI",
                "supply_demand_summary": "1 Paz",
            }
            parsed_items.append(rec)

        if owner_id in self.items_by_shop and len(parsed_items) > 0:
            prev_items = self.items_by_shop[owner_id]
            for old_it in prev_items:
                old_id = int(old_it.get("id", 0))
                if old_id > 0 and old_id not in new_item_ids and old_id not in self.our_bought_item_ids:
                    mkey = old_it.get("market_key", str(old_it.get("vnum", 0)))
                    self.real_sales_by_key[mkey] = self.real_sales_by_key.get(mkey, 0) + int(old_it.get("count", 1))
                    self.total_live_sales += 1
                    self.sales_feed.insert(0, {
                        "ts": time.strftime("%H:%M:%S"),
                        "name": old_it.get("name", "?"),
                        "count": int(old_it.get("count", 1)),
                        "unit_price": int(old_it.get("unit_price", 0)),
                        "price": int(old_it.get("price", 0)),
                        "seller": old_it.get("seller", "?"),
                        "market_key": mkey,
                    })
                    if len(self.sales_feed) > 120:
                        self.sales_feed = self.sales_feed[:120]

        if mshop is not None:
            mshop["item_count"] = len(parsed_items)

        self.scanned_shops[owner_id] = {
            "owner_id": owner_id,
            "shop_vid": shop_vid,
            "owner": owner_str,
            "title": title_str,
            "duration": int(shop_info.get("duration", 0)),
            "count": len(parsed_items),
            "ts": time.time(),
            "x": sx,
            "y": sy,
            "dist": dist,
        }
        self.items_by_shop[owner_id] = parsed_items
        self._rebuild_aggregates()
        self._check_sniper_and_autoflip(parsed_items)
        self.revision += 1

    def remove_bought_item(self, owner_id, item_id):
        oid = int(owner_id)
        iid = int(item_id)
        if iid > 0:
            self.our_bought_item_ids.add(iid)
        if oid in self.items_by_shop:
            for x in self.items_by_shop[oid]:
                if x["id"] == iid:
                    self.record_bought_item(x)
            self.items_by_shop[oid] = [x for x in self.items_by_shop[oid] if x["id"] != iid]
            if oid in self.scanned_shops:
                self.scanned_shops[oid]["count"] = len(self.items_by_shop[oid])
        self._rebuild_aggregates()
        self.revision += 1

    def _compute_demand_profile(self, mkey, vnum, name_lower, unique_sellers, offers, total_qty, sold_qty, avg_dmg):
        score = 0
        if sold_qty > 0:
            score += min(45, sold_qty * 18)
        if unique_sellers >= 8:
            score += 35
        elif unique_sellers >= 5:
            score += 28
        elif unique_sellers >= 3:
            score += 20
        elif unique_sellers == 2:
            score += 10
        if vnum == 50300:
            score += 22
            if any(k in name_lower for k in ("hava", "ofke", "keskin", "kutsama", "ejderha", "beden", "dehset", "buyulu")):
                score += 18
        elif any(k in name_lower for k in ("ruhtasi", "ruh tasi", "efsun", "kutsama", "zen", "inci", "istiridye", "metal", "tas", "kuresi", "sandik", "parcacigi", "postu", "pencesi", "kuyrugu")):
            score += 22
        elif avg_dmg >= 40:
            score += 25
        elif avg_dmg >= 35:
            score += 15
        elif total_qty > offers and unique_sellers >= 2:
            score += 12

        if score >= 50:
            tier = 3
            label = "COK YUKSEK"
        elif score >= 30:
            tier = 2
            label = "YUKSEK"
        elif score >= 12:
            tier = 1
            label = "DENGELI"
        else:
            tier = 0
            label = "DUSUK"

        if sold_qty > 0:
            summary = "%s (%dPaz|%dSatis)" % (label, unique_sellers, sold_qty)
        else:
            summary = "%s (%dPaz|%dAd)" % (label, unique_sellers, total_qty)
        return (score, tier, label, summary)

    def _rebuild_aggregates(self):
        flat = []
        by_key = {}
        for oid, items in self.items_by_shop.items():
            if self.is_our_own_shop(oid):
                continue
            for it in items:
                flat.append(it)
                mkey = it.get("market_key", str(it["vnum"]))
                if mkey not in by_key:
                    by_key[mkey] = []
                by_key[mkey].append(it)

        stats = {}
        for mkey, lst in by_key.items():
            u_prices = sorted(x["unit_price"] for x in lst if x["unit_price"] > 0)
            if not u_prices:
                continue
            n = len(u_prices)
            min_u = u_prices[0]
            max_u = u_prices[-1]
            med_u = u_prices[n // 2]
            if n >= 4:
                trimmed = u_prices[:-1]
                avg_u = int(sum(trimmed) // len(trimmed))
            else:
                avg_u = int(sum(u_prices) // n)

            min_seller = lst[0]["owner_id"]
            for x in lst:
                if x["unit_price"] == min_u:
                    min_seller = x["owner_id"]
                    break
            other_seller_prices = sorted(x["unit_price"] for x in lst if x["owner_id"] != min_seller and x["unit_price"] > 0)
            if other_seller_prices:
                second_min_u = other_seller_prices[0]
            else:
                second_min_u = u_prices[1] if n >= 2 else min_u

            unique_sellers = len(set(x["owner_id"] for x in lst))
            total_qty = sum(x["count"] for x in lst)
            sold_qty = int(self.real_sales_by_key.get(mkey, 0))
            sample = lst[0]
            d_score, d_tier, d_label, d_summary = self._compute_demand_profile(
                mkey, sample["vnum"], sample["name_lower"], unique_sellers, n, total_qty, sold_qty, sample.get("avg_dmg", 0)
            )
            st_entry = {
                "market_key": mkey,
                "min_unit": min_u,
                "second_min_unit": second_min_u,
                "avg_unit": avg_u,
                "median_unit": med_u,
                "max_unit": max_u,
                "offers": n,
                "unique_sellers": unique_sellers,
                "total_qty": total_qty,
                "sold_qty": sold_qty,
                "demand_score": d_score,
                "demand_tier": d_tier,
                "demand_label": d_label,
                "supply_demand_summary": d_summary,
            }
            stats[mkey] = st_entry
            if sample["vnum"] not in stats:
                stats[sample["vnum"]] = st_entry

        bargains = []
        npc_bargains = []
        for it in flat:
            mkey = it.get("market_key", str(it["vnum"]))
            st = stats.get(mkey) or stats.get(it["vnum"])
            if st:
                it["demand_tier"] = st["demand_tier"]
                it["demand_label"] = st["demand_label"]
                it["supply_demand_summary"] = st["supply_demand_summary"]
                unique_sellers = st["unique_sellers"]
                offers = st["offers"]

                if offers >= 3:
                    target_u = min(st["second_min_unit"], int(st["median_unit"] * 1.20))
                    if target_u < st["min_unit"]:
                        target_u = st["median_unit"]
                elif offers == 2:
                    target_u = min(st["second_min_unit"], int(st["avg_unit"] * 1.15))
                else:
                    target_u = it["unit_price"]

                target_u = _round_market_price(max(it["unit_price"], target_u))
                it["avg_ref"] = st["median_unit"] if offers >= 3 else st["second_min_unit"]
                it["target_sell_unit"] = target_u

                if unique_sellers >= 2 and target_u > it["unit_price"] and it["price"] > 0:
                    gross_resell = int(target_u * it["count"])
                    net_resell = int(gross_resell * 97 // 100)
                    flip_profit = max(0, net_resell - it["price"])
                    roi_pct = int((flip_profit * 100) // max(1, it["price"])) if flip_profit > 0 else 0
                    disc = int(((target_u - it["unit_price"]) * 100) // max(1, target_u))
                    it["flip_profit"] = flip_profit
                    it["roi_pct"] = min(999, roi_pct)
                    it["discount_pct"] = max(0, min(99, disc))

                    if flip_profit >= 3000 and roi_pct >= 15 and disc >= 15:
                        bargains.append(it)
                else:
                    it["flip_profit"] = 0
                    it["roi_pct"] = 0
                    it["discount_pct"] = 0
            else:
                it["avg_ref"] = it["unit_price"]
                it["target_sell_unit"] = it["unit_price"]
                it["flip_profit"] = 0
                it["roi_pct"] = 0
                it["discount_pct"] = 0

            if it.get("npc_profit", 0) > 0:
                npc_bargains.append(it)
                if it.get("npc_unit", 0) > it["unit_price"] and it.get("npc_unit", 0) > 0:
                    npc_disc = int(((it["npc_unit"] - it["unit_price"]) * 100) // it["npc_unit"])
                    if npc_disc > it["discount_pct"]:
                        it["discount_pct"] = max(0, min(99, npc_disc))
                        it["avg_ref"] = it["npc_unit"]

        npc_bargains.sort(key=lambda x: (-x.get("npc_profit", 0), x["price"]))
        bargains.sort(key=lambda x: (-x.get("demand_tier", 0), -x.get("flip_profit", 0), -x.get("roi_pct", 0), x["price"]))
        self.all_items = flat
        self.vnum_stats = stats
        self.bargains = bargains
        self.npc_bargains = npc_bargains

    def _check_sniper_and_autoflip(self, items):
        if not self.sniper_enabled and not self.auto_flip_enabled:
            return
        if self.sniper_buy_cb is None:
            return
        my_yang = self.engine.get_player_yang()
        if my_yang <= 0:
            return

        for it in items:
            if self.is_our_own_shop(it.get("owner_id", 0), it.get("seller", "")):
                continue
            price = int(it.get("price", 0))
            if price <= 0 or price > my_yang:
                continue

            # 1. Guaranteed NPC Arbitrage Auto-Buy (active when either Sniper or Auto-Flip is ON)
            if it.get("npc_profit", 0) > 0 and it["id"] not in self.npc_sniped_ids:
                self.npc_sniped_ids.add(it["id"])
                self.npc_arbitrage_vnums.add(it["vnum"])
                try:
                    self.sniper_buy_cb(it, from_sniper=(1 == 1), auto_list=(1 == 0))
                    my_yang = max(0, my_yang - price)
                    msg = "OTO-NPC ALIM (+%s Kar): %s x%d (%s -> NPC:%s)" % (
                        _fmt_yang_short(it["npc_profit"]), it["name"], it["count"],
                        _fmt_yang_short(price), _fmt_yang_short(it["npc_total"])
                    )
                    self.log_auto_event(msg)
                    _chat_notice(msg)
                except Exception as e:
                    _tool_log("[NPC_SNIPER_ERR] %s" % e)
                continue

            # 2. Full Auto-Flip Bot (when auto_flip_enabled is ON): buys high-liquidity bargains & auto-lists in My Shop!
            if self.auto_flip_enabled and it["id"] not in self.flip_sniped_ids:
                if (
                    it.get("demand_tier", 0) >= 2
                    and it.get("flip_profit", 0) >= 5000
                    and it.get("roi_pct", 0) >= 25
                    and it.get("discount_pct", 0) >= 22
                    and self.engine.is_item_myshop_tradable(it["vnum"])
                ):
                    self.flip_sniped_ids.add(it["id"])
                    try:
                        self.sniper_buy_cb(it, from_sniper=(1 == 1), auto_list=(1 == 1))
                        my_yang = max(0, my_yang - price)
                        msg = "OTO AL-SAT: %s x%d (%s -> Hedef:%s, Kar:+%s)" % (
                            it["name"], it["count"],
                            _fmt_yang_short(price),
                            _fmt_yang_short(int(it.get("target_sell_unit", it["unit_price"]) * it["count"])),
                            _fmt_yang_short(it["flip_profit"]),
                        )
                        self.log_auto_event(msg)
                        _chat_notice(msg)
                    except Exception as e:
                        _tool_log("[AUTO_FLIP_ERR] %s" % e)
                    continue

            # 3. User-defined Sniper Rules
            if self.sniper_enabled:
                for rule in self.sniper_rules:
                    if not rule.get("enabled", (1 == 1)):
                        continue
                    if it["id"] in rule["bought_ids"]:
                        continue
                    q = rule["query"].lower().strip()
                    if not q:
                        continue
                    if q.isdigit():
                        if it["vnum"] != int(q):
                            continue
                    else:
                        if q not in it["name_lower"]:
                            continue
                    if it["unit_price"] > rule["max_unit"]:
                        continue
                    if rule["min_avg_dmg"] > 0 and it["avg_dmg"] < rule["min_avg_dmg"]:
                        continue

                    rule["bought_ids"].add(it["id"])
                    try:
                        self.sniper_buy_cb(it, from_sniper=(1 == 1), auto_list=self.auto_list_bought)
                        my_yang = max(0, my_yang - price)
                        msg = "SNIPER ALIM: %s x%d (%s Yang) -> %s" % (
                            it["name"], it["count"], _fmt_yang(price), it["seller"]
                        )
                        self.log_auto_event(msg)
                        _chat_notice(msg)
                    except Exception as e:
                        _tool_log("[SNIPER_ERR] %s" % e)

    def add_sniper_rule(self, query, max_unit, min_avg_dmg=0):
        q = _safe_ascii(query).strip()
        if not q or max_unit <= 0:
            return (1 == 0)
        self.sniper_rules.append({
            "query": q,
            "max_unit": int(max_unit),
            "min_avg_dmg": int(min_avg_dmg),
            "enabled": (1 == 1),
            "bought_ids": set(),
        })
        self.revision += 1
        return (1 == 1)

    def populate_default_sniper_rules(self):
        """Populates smart Sniper rules from the top high-demand market items at 70% of lowest price."""
        added = 0
        existing_q = set(r["query"].lower() for r in self.sniper_rules)
        candidates = []
        for mkey, st in self.vnum_stats.items():
            if not isinstance(mkey, str):
                continue
            if st.get("unique_sellers", 0) >= 5 and st.get("min_unit", 0) >= 5000:
                candidates.append((st.get("demand_score", 0), mkey, st))
        candidates.sort(key=lambda t: -t[0])
        for _, mkey, st in candidates[:8]:
            sample_nm = ""
            for it in self.all_items:
                if it.get("market_key") == mkey:
                    sample_nm = it["name"]
                    break
            if not sample_nm or sample_nm.lower() in existing_q:
                continue
            max_u = _round_market_price(max(1000, int(st["min_unit"] * 0.72)))
            self.add_sniper_rule(sample_nm, max_u, 0)
            existing_q.add(sample_nm.lower())
            added += 1
        if added > 0:
            self.sniper_enabled = (1 == 1)
            _chat_notice("%d adet yuksek talepli esya icin akilli Sniper kurali eklendi." % added)
        return added

    def export_to_disk(self):
        try:
            open_fn = getattr(__builtin__, "open", open)
            f = open_fn(EXPORT_TXT_PATH, "wb")
            try:
                f.write("=== AVRASYA2 OFFLINE SHOP PIYASA RAPORU (%s) ===\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
                f.write("Haritadaki Pazar: %d | Taranan Pazar: %d | Toplam Esya: %d | Firsat Esya: %d\n\n" % (
                    len(self.map_shops), len(self.scanned_shops), len(self.all_items), len(self.bargains)
                ))
                f.write("--- EN IYI FIRSATLAR (PIYASA ALTI ESYALAR) ---\n")
                for b in self.bargains[:80]:
                    f.write("[-%2d%%] %-26s x%-3d | Birim: %-12s (Hedef: %-12s) | NetKar: +%-11s | Satici: %-16s\n" % (
                        b["discount_pct"],
                        b["name"][:26],
                        b["count"],
                        _fmt_yang(b["unit_price"]),
                        _fmt_yang(b["target_sell_unit"]),
                        _fmt_yang(b["flip_profit"]),
                        b["seller"][:16],
                    ))
            finally:
                f.close()
            _chat_notice("Piyasa raporu kaydedildi: logs/offlineshop_market_dump.txt (%d esya)" % len(self.all_items))
            return (1 == 1)
        except Exception as e:
            _tool_log("[EXPORT_ERR] %s" % e)
            return (1 == 0)


# ==============================================================================
# 4. SILENT BACKGROUND SHOP SCANNER, AUTO-SHOP & FARM CONTROLLER
# ==============================================================================
class _ShopScannerController(object):
    def __init__(self, engine, db):
        self.engine = engine
        self.db = db
        self.hooked_board = None
        self.orig_open_shop_end = None
        self.orig_open_shop_owner_end = None
        self.orig_open_shop_owner_no_shop = None
        self.orig_safebox_refresh_end = None

        self.auto_scan_enabled = (1 == 1)
        self.scan_queue = []
        self.queued_set = set()
        self.in_flight_owner = 0
        self.in_flight_ts = 0.0
        self.last_map_poll_ts = 0.0
        self.last_scan_send_ts = 0.0
        self.scan_interval = 0.42
        self.rescan_cooldown = 180.0
        self.silent_intercept_until = 0.0

        self.user_open_shop_owner = 0
        self.user_open_shop_until = 0.0
        self.pending_buy_queue = []
        self.active_buy_req = None

        self.npc_sell_queue = []
        self.last_npc_sell_ts = 0.0
        self.auto_npc_sell_arbitrage = (1 == 1)
        self.walking_to_npc = (1 == 0)
        self.walking_npc_vid = 0
        self.walking_npc_ts = 0.0

        # Own OfflineShop automation queues
        self.shop_add_queue = []     # list of {"slot": int, "vnum": int, "count": int, "price": long, "name": str}
        self.shop_edit_queue = []    # list of {"item_id": int, "price": long, "name": str}
        self.shop_remove_queue = []  # list of {"item_id": int, "name": str}
        self.last_shop_op_ts = 0.0
        self.my_shop_sync_in_flight = (1 == 0)
        self.my_shop_sync_ts = 0.0
        self.last_my_shop_auto_sync_ts = 0.0
        self.safebox_sync_in_flight = (1 == 0)
        self.safebox_withdraw_requested = (1 == 0)

        # Embedded Farm/Combat/Utility state (integrates with main.py SuiteController or direct native calls)
        self.suite_ctrl = None
        self.farm_selected_vnums = set()

        self.db.sniper_buy_cb = self.request_buy_item

    def get_suite_controller(self):
        """Lazily binds or initializes main.py SuiteController for Farm/Combat/Efsun integration."""
        if self.suite_ctrl is not None:
            return self.suite_ctrl
        try:
            main_mod = sys.modules.get("main")
            if main_mod is None:
                import os
                src_dir = r"C:\Users\erenk\Desktop\Avrasya2\source"
                if src_dir not in sys.path:
                    sys.path.insert(0, src_dir)
                import main as main_mod
            if hasattr(main_mod, "init_or_get_controller"):
                self.suite_ctrl = main_mod.init_or_get_controller()
        except Exception as e:
            _tool_log("[SUITE_CTRL_BIND_ERR] %s" % e)
        return self.suite_ctrl

    def ensure_board_hook(self):
        if offlineshop is None or not hasattr(offlineshop, "GetOfflineshopBoard"):
            return None
        try:
            board = offlineshop.GetOfflineshopBoard()
        except Exception:
            board = None
        if board is None:
            return None

        if self.hooked_board is not board:
            self._install_hook_on_board(board)
        else:
            cur_fn = getattr(board, "OpenShop_End", None)
            if cur_fn is not None and not getattr(cur_fn, "_is_offshop_tool_hook", (1 == 0)):
                self._install_hook_on_board(board)
        return board

    def _install_hook_on_board(self, board):
        try:
            orig_end = getattr(board, "OpenShop_End", None)
            if orig_end is None:
                return
            if getattr(orig_end, "_controller_ref", None) is self:
                self.hooked_board = board
                return
            # Unwrap previous hook if hot-reloaded
            while getattr(orig_end, "_orig_fn", None) is not None:
                orig_end = getattr(orig_end, "_orig_fn")

            # Capture existing own shop data if already present on board before scanning starts!
            try:
                s_info = getattr(board, "ShopOpenInfo", None)
                s_items = getattr(board, "ShopItemForSale", None)
                s_sold = getattr(board, "ShopItemSold", None)
                if isinstance(s_info, dict) and s_info.get("my_shop", (1 == 0)):
                    self.db.ingest_my_shop(s_info, s_items or [], s_sold or [])
                valutes = getattr(board, "ShopSafeboxValutes", 0)
                sb_items = getattr(board, "ShopSafeboxItems", None)
                if valutes or sb_items:
                    self.db.my_safebox_yang = int(valutes or 0)
                    self.db.my_safebox_items = list(sb_items or [])
            except Exception:
                pass

            self.orig_open_shop_end = orig_end
            orig_owner_end = getattr(board, "OpenShopOwner_End", None)
            while getattr(orig_owner_end, "_orig_fn", None) is not None:
                orig_owner_end = getattr(orig_owner_end, "_orig_fn")
            self.orig_open_shop_owner_end = orig_owner_end

            orig_no_shop = getattr(board, "OpenShopOwnerNoShop", None)
            while getattr(orig_no_shop, "_orig_fn", None) is not None:
                orig_no_shop = getattr(orig_no_shop, "_orig_fn")
            self.orig_open_shop_owner_no_shop = orig_no_shop

            orig_sb_end = getattr(board, "ShopSafebox_RefreshEnd", None)
            while getattr(orig_sb_end, "_orig_fn", None) is not None:
                orig_sb_end = getattr(orig_sb_end, "_orig_fn")
            self.orig_safebox_refresh_end = orig_sb_end

            controller = self

            def _hooked_open_shop_end(*args, **kwargs):
                return controller._on_board_open_shop_end(board, *args, **kwargs)

            _hooked_open_shop_end._is_offshop_tool_hook = (1 == 1)
            _hooked_open_shop_end._controller_ref = controller
            _hooked_open_shop_end._orig_fn = orig_end
            board.OpenShop_End = _hooked_open_shop_end

            if self.orig_open_shop_owner_end is not None:
                orig_owner_end = self.orig_open_shop_owner_end
                def _hooked_owner_end(*args, **kwargs):
                    return controller._on_board_open_shop_owner_end(board, *args, **kwargs)
                _hooked_owner_end._is_offshop_tool_hook = (1 == 1)
                _hooked_owner_end._orig_fn = orig_owner_end
                board.OpenShopOwner_End = _hooked_owner_end

            if self.orig_open_shop_owner_no_shop is not None:
                orig_no_shop = self.orig_open_shop_owner_no_shop
                def _hooked_no_shop(*args, **kwargs):
                    return controller._on_board_open_shop_owner_no_shop(board, *args, **kwargs)
                _hooked_no_shop._is_offshop_tool_hook = (1 == 1)
                _hooked_no_shop._orig_fn = orig_no_shop
                board.OpenShopOwnerNoShop = _hooked_no_shop

            if self.orig_safebox_refresh_end is not None:
                orig_sb_end = self.orig_safebox_refresh_end
                def _hooked_sb_end(*args, **kwargs):
                    return controller._on_board_safebox_refresh_end(board, *args, **kwargs)
                _hooked_sb_end._is_offshop_tool_hook = (1 == 1)
                _hooked_sb_end._orig_fn = orig_sb_end
                board.ShopSafebox_RefreshEnd = _hooked_sb_end

            self.hooked_board = board
            _tool_log("[HOOK] Installed silent OpenShop_End + Owner + Safebox hooks on board=%r" % (board,))
        except Exception as e:
            _tool_log("[HOOK_ERR] %s\n%s" % (e, traceback.format_exc()))

    def _restore_my_shop_on_board(self, board):
        """Restores the player's own shop dictionaries onto board after a silent background scan."""
        try:
            if self.db.my_shop_raw_info is not None:
                board.ShopOpenInfo = dict(self.db.my_shop_raw_info)
                board.ShopItemForSale = list(self.db.my_shop_raw_items)
                board.ShopItemSold = list(self.db.my_shop_raw_sold)
        except Exception:
            pass

    def _on_board_open_shop_owner_end(self, board, *args, **kwargs):
        now = time.time()
        try:
            shop_info = getattr(board, "ShopOpenInfo", None)
            items_for_sale = getattr(board, "ShopItemForSale", None)
            items_sold = getattr(board, "ShopItemSold", None)
            if isinstance(shop_info, dict) and isinstance(items_for_sale, list):
                self.db.ingest_my_shop(shop_info, items_for_sale, items_sold or [])
        except Exception as e:
            _tool_log("[OWNER_HOOK_ERR] %s" % e)

        was_silent_sync = self.my_shop_sync_in_flight
        self.my_shop_sync_in_flight = (1 == 0)

        try:
            wnd = getattr(board, "wndOffShop", None)
            is_wnd_shown = wnd.IsShow() if (wnd is not None and hasattr(wnd, "IsShow")) else (1 == 0)
        except Exception:
            is_wnd_shown = (1 == 0)

        if was_silent_sync and not is_wnd_shown:
            return None

        if self.orig_open_shop_owner_end is not None:
            try:
                return self.orig_open_shop_owner_end(*args, **kwargs)
            except Exception as e:
                _tool_log("[ORIG_OWNER_END_ERR] %s" % e)
        return None

    def _on_board_open_shop_owner_no_shop(self, board, *args, **kwargs):
        self.db.my_shop_open = (1 == 0)
        self.db.my_shop_items = []
        self.db.revision += 1
        was_silent_sync = self.my_shop_sync_in_flight
        self.my_shop_sync_in_flight = (1 == 0)
        if was_silent_sync:
            return None
        if self.orig_open_shop_owner_no_shop is not None:
            try:
                return self.orig_open_shop_owner_no_shop(*args, **kwargs)
            except Exception:
                pass
        return None

    def _on_board_safebox_refresh_end(self, board, *args, **kwargs):
        try:
            valutes = getattr(board, "ShopSafeboxValutes", 0)
            sb_items = getattr(board, "ShopSafeboxItems", None)
            self.db.my_safebox_yang = int(valutes or 0)
            self.db.my_safebox_items = list(sb_items or [])
            self.db.revision += 1
            if self.safebox_withdraw_requested:
                self.safebox_withdraw_requested = (1 == 0)
                self._execute_safebox_withdraw_now()
        except Exception as e:
            _tool_log("[SAFEBOX_HOOK_ERR] %s" % e)

        was_silent = self.safebox_sync_in_flight
        self.safebox_sync_in_flight = (1 == 0)
        if was_silent:
            return None
        if self.orig_safebox_refresh_end is not None:
            try:
                return self.orig_safebox_refresh_end(*args, **kwargs)
            except Exception:
                pass
        return None

    def _on_board_open_shop_end(self, board, *args, **kwargs):
        now = time.time()
        owner_id = 0
        try:
            shop_info = getattr(board, "ShopOpenInfo", None)
            items_for_sale = getattr(board, "ShopItemForSale", None)
            items_sold = getattr(board, "ShopItemSold", None)
            if isinstance(shop_info, dict) and isinstance(items_for_sale, list):
                owner_id = int(shop_info.get("owner_id", 0))
                if shop_info.get("my_shop", (1 == 0)) or self.db.is_our_own_shop(owner_id, shop_info.get("name", "")):
                    self.db.ingest_my_shop(shop_info, items_for_sale, items_sold or [])
                else:
                    self.db.ingest_open_shop(shop_info, items_for_sale, clicked_vid=self.in_flight_owner)
        except Exception as e:
            _tool_log("[INGEST_ERR] %s" % e)

        if self.active_buy_req is not None:
            req = self.active_buy_req
            if int(req.get("owner_id", 0)) == owner_id and req.get("state") == "WAIT_OPEN":
                req["state"] = "SEND_BUY"
                req["open_received_ts"] = now
                self.in_flight_owner = 0
                self._restore_my_shop_on_board(board)
                return None

        if now < self.user_open_shop_until and (
            self.user_open_shop_owner == 0
            or self.user_open_shop_owner == owner_id
            or self.db.resolve_shop_vid(self.user_open_shop_owner) == self.db.resolve_shop_vid(owner_id)
        ):
            self.user_open_shop_until = 0.0
            self.user_open_shop_owner = 0
            self.in_flight_owner = 0
            if self.orig_open_shop_end is not None:
                return self.orig_open_shop_end(*args, **kwargs)
            return None

        is_our_bg_scan = (self.in_flight_owner != 0) or (now < self.silent_intercept_until)
        self.in_flight_owner = 0

        if is_our_bg_scan:
            self._restore_my_shop_on_board(board)
            return None

        if self.orig_open_shop_end is not None:
            return self.orig_open_shop_end(*args, **kwargs)
        return None

    def _send_open_foreign_shop(self, target_id, force=(1 == 0)):
        vid = self.db.resolve_shop_vid(target_id)
        if vid > 0 and self.engine.send_click_shop_packet(vid, force=force):
            return (1 == 1)
        if offlineshop is not None and hasattr(offlineshop, "SendOpenShop"):
            try:
                offlineshop.SendOpenShop(int(target_id))
                return (1 == 1)
            except Exception:
                pass
        return (1 == 0)

    def open_shop_for_user(self, owner_id):
        oid = int(owner_id)
        if oid <= 0:
            return (1 == 0)
        self.ensure_board_hook()
        self.user_open_shop_owner = oid
        self.user_open_shop_until = time.time() + 4.0
        try:
            return self._send_open_foreign_shop(oid, force=(1 == 1))
        except Exception as e:
            _tool_log("[USER_OPEN_ERR] %s" % e)
            return (1 == 0)

    def _snapshot_inventory_slots(self):
        """Returns dict of {slot: (vnum, count)} for inventory slots 0..179."""
        snap = {}
        if player is None or not hasattr(player, "GetItemIndex"):
            return snap
        for slot in range(180):
            try:
                vnum = int(player.GetItemIndex(slot))
                if vnum > 0:
                    cnt = int(player.GetItemCount(slot))
                    snap[slot] = (vnum, max(1, cnt))
            except Exception:
                pass
        return snap

    def request_buy_item(self, item_rec, from_sniper=(1 == 0), auto_list=None):
        if item_rec is None or offlineshop is None:
            return (1 == 0)
        owner_id = int(item_rec.get("owner_id", 0))
        item_id = int(item_rec.get("id", 0))
        price = int(item_rec.get("price", 0))
        if owner_id <= 0 or item_id <= 0:
            return (1 == 0)

        if self.db.is_our_own_shop(owner_id, item_rec.get("seller", "")):
            if not from_sniper:
                _chat_notice("Bu esya zaten sizin kendi magazanizda bulunuyor!")
            return (1 == 0)

        my_yang = self.engine.get_player_yang()
        if price > my_yang:
            if not from_sniper:
                _chat_notice("Yetersiz Yang! Gereken: %s | Mevcut: %s" % (_fmt_yang(price), _fmt_yang(my_yang)))
            return (1 == 0)

        for q in self.pending_buy_queue:
            if q["owner_id"] == owner_id and q["item_id"] == item_id:
                return (1 == 0)
        if self.active_buy_req and self.active_buy_req["item_id"] == item_id:
            return (1 == 0)

        if auto_list is None:
            # Default: if it's an NPC arbitrage item, don't put in shop; if it's a flip item and auto_list_bought is ON, list it!
            if item_rec.get("npc_profit", 0) > 0 and item_rec.get("npc_profit", 0) >= item_rec.get("flip_profit", 0):
                auto_list = (1 == 0)
            else:
                auto_list = self.db.auto_list_bought

        target_unit = self.db.compute_smart_resale_unit_price(item_rec)
        count = max(1, int(item_rec.get("count", 1)))
        resale_total = long(target_unit) * long(count)

        self.pending_buy_queue.append({
            "owner_id": owner_id,
            "item_id": item_id,
            "vnum": int(item_rec.get("vnum", 0)),
            "name": item_rec.get("name", "?"),
            "count": count,
            "price": price,
            "npc_profit": int(item_rec.get("npc_profit", 0)),
            "flip_profit": int(item_rec.get("flip_profit", 0)),
            "auto_list": bool(auto_list),
            "resale_total": resale_total,
            "resale_unit": target_unit,
            "state": "QUEUED",
            "ts": time.time(),
        })
        if int(item_rec.get("npc_profit", 0)) > 0:
            self.db.npc_arbitrage_vnums.add(int(item_rec.get("vnum", 0)))
        if not from_sniper:
            if auto_list:
                _chat_notice("Alim + Oto-Magaza kuyruga eklendi: %s x%d (Alis: %s -> Satis: %s)" % (
                    item_rec.get("name", "?"), count, _fmt_yang_short(price), _fmt_yang_short(resale_total)
                ))
            else:
                _chat_notice("Satin alma kuyruga eklendi: %s x%d (%s Yang)" % (
                    item_rec.get("name", "?"), count, _fmt_yang(price)
                ))
        return (1 == 1)

    # --------------------------------------------------------------------------
    # Own OfflineShop Management & Auto-Pricing
    # --------------------------------------------------------------------------
    def request_my_shop_sync(self, silent=(1 == 1)):
        if offlineshop is None or not hasattr(offlineshop, "SendOpenShopOwner"):
            return (1 == 0)
        self.ensure_board_hook()
        self.my_shop_sync_in_flight = bool(silent)
        self.my_shop_sync_ts = time.time()
        self.last_my_shop_auto_sync_ts = time.time()
        try:
            offlineshop.SendOpenShopOwner()
            return (1 == 1)
        except Exception as e:
            _tool_log("[MY_SHOP_SYNC_ERR] %s" % e)
            self.my_shop_sync_in_flight = (1 == 0)
            return (1 == 0)

    def request_safebox_sync(self, withdraw_all=(1 == 0)):
        if offlineshop is None or not hasattr(offlineshop, "SendSafeboxOpen"):
            return (1 == 0)
        self.ensure_board_hook()
        self.safebox_sync_in_flight = (1 == 1)
        if withdraw_all:
            self.safebox_withdraw_requested = (1 == 1)
        try:
            offlineshop.SendSafeboxOpen()
            return (1 == 1)
        except Exception as e:
            _tool_log("[SAFEBOX_OPEN_ERR] %s" % e)
            self.safebox_sync_in_flight = (1 == 0)
            return (1 == 0)

    def _execute_safebox_withdraw_now(self):
        if offlineshop is None:
            return 0
        actions = 0
        try:
            yang = int(self.db.my_safebox_yang or 0)
            if yang > 0 and hasattr(offlineshop, "SendSafeboxGetValutes"):
                offlineshop.SendSafeboxGetValutes(long(yang))
                msg = "PAZAR KASASI: %s Yang envantere cekildi!" % _fmt_yang(yang)
                self.db.log_auto_event(msg)
                _chat_notice(msg)
                self.db.my_safebox_yang = 0
                actions += 1
            for it in list(self.db.my_safebox_items):
                iid = int(it.get("id", 0))
                if iid > 0 and hasattr(offlineshop, "SendSafeboxGetItem"):
                    offlineshop.SendSafeboxGetItem(iid)
                    actions += 1
            if actions > 0:
                self.db.my_safebox_items = []
                self.db.revision += 1
            if hasattr(offlineshop, "SendSafeboxClose"):
                offlineshop.SendSafeboxClose()
        except Exception as e:
            _tool_log("[SAFEBOX_WITHDRAW_ERR] %s" % e)
        return actions

    def get_inventory_market_items(self):
        """Scans player inventory (0..179) for tradable items and computes smart Offline Shop prices."""
        rows = []
        if player is None or not hasattr(player, "GetItemIndex"):
            return rows

        equipped_vnums = set()
        for eq_slot in range(180, 215):
            try:
                ev = int(player.GetItemIndex(eq_slot))
                if ev > 0:
                    equipped_vnums.add(ev)
            except Exception:
                pass

        for slot in range(180):
            try:
                vnum = int(player.GetItemIndex(slot))
            except Exception:
                vnum = 0
            if vnum <= 0:
                continue
            if not self.engine.is_item_myshop_tradable(vnum):
                continue

            try:
                count = max(1, int(player.GetItemCount(slot)))
            except Exception:
                count = 1

            sockets = []
            for s_idx in range(3):
                try:
                    sockets.append(int(player.GetItemMetinSocket(slot, s_idx)))
                except Exception:
                    sockets.append(0)

            attrs = []
            avg_dmg = 0
            has_good_bonus = (1 == 0)
            bonus_parts = []
            for a_idx in range(7):
                try:
                    atype, aval = player.GetItemAttribute(slot, a_idx)
                    atype, aval = int(atype), int(aval)
                except Exception:
                    atype, aval = 0, 0
                attrs.append((atype, aval))
                if atype != 0 and aval != 0:
                    if atype == ATTR_AVG_DMG:
                        avg_dmg = aval
                        if aval >= 35:
                            has_good_bonus = (1 == 1)
                    elif atype == ATTR_SKILL_DMG and aval >= 12:
                        has_good_bonus = (1 == 1)
                    elif aval >= 10 or atype in (1, 15, 16, 17, 43, 53):
                        has_good_bonus = (1 == 1)
                    bname = ATTR_SHORT_NAMES.get(atype, "Ef#%d" % atype)
                    bonus_parts.append("%s:%+d" % (bname, aval))

            base_name = self.engine.get_item_name(vnum)
            mkey, name = self._build_inv_market_key(vnum, base_name, sockets)
            st = self.db.vnum_stats.get(mkey) or self.db.vnum_stats.get(vnum)
            smart_unit = self.db.compute_smart_unit_price_for_key(mkey, vnum)
            npc_unit = self.engine.get_item_npc_unit_price(vnum)

            if smart_unit <= 0 and st:
                smart_unit = int(st.get("median_unit", 0) or st.get("min_unit", 0))
            smart_total = int(smart_unit * count) if smart_unit > 0 else 0

            min_u = int(st["min_unit"]) if st else 0
            med_u = int(st["median_unit"]) if st else 0
            offers = int(st["offers"]) if st else 0
            demand_label = st.get("demand_label", "VERI YOK") if st else "VERI YOK"
            demand_tier = int(st.get("demand_tier", 0)) if st else 0

            rows.append({
                "slot": slot,
                "vnum": vnum,
                "market_key": mkey,
                "name": name,
                "count": count,
                "smart_unit": smart_unit,
                "smart_total": smart_total,
                "min_unit": min_u,
                "med_unit": med_u,
                "npc_unit": npc_unit,
                "npc_total": int(npc_unit * count),
                "offers": offers,
                "demand_label": demand_label,
                "demand_tier": demand_tier,
                "avg_dmg": avg_dmg,
                "has_good_bonus": has_good_bonus,
                "bonus_summary": " ".join(bonus_parts[:3]) if bonus_parts else "-",
            })

        rows.sort(key=lambda r: (-r["smart_total"], -r["demand_tier"], r["slot"]))
        return rows

    def _build_inv_market_key(self, vnum, base_name, sockets):
        s0 = sockets[0] if sockets else 0
        if vnum == 50300 and s0 > 0:
            sk_name = SKILL_BOOK_NAMES.get(s0, "Beceri#%d" % s0)
            return ("50300:%d" % s0, "BK: %s" % sk_name)
        if vnum in (50401, 50402, 50403, 50404, 50405, 50416, 50417, 50418, 50419, 50420) and s0 > 0:
            sk_name = SKILL_BOOK_NAMES.get(s0, "Beceri#%d" % s0)
            return ("%d:%d" % (vnum, s0), "%s (%s)" % (base_name, sk_name))
        if vnum in (70104, 70105, 70106, 70107) and s0 > 0:
            mob_name = self.engine.get_mob_name(s0)
            if mob_name:
                return ("%d:%d" % (vnum, s0), "%s [%s]" % (base_name, mob_name))
        return (str(vnum), base_name)

    def queue_add_inventory_slot_to_my_shop(self, slot, custom_total_price=0):
        """Queues an inventory slot to be automatically placed into the player's Offline Shop."""
        if player is None:
            return (1 == 0)
        slot = int(slot)
        vnum = int(player.GetItemIndex(slot))
        if vnum <= 0:
            _chat_notice("Slot #%d bos!" % (slot + 1))
            return (1 == 0)
        if not self.engine.is_item_myshop_tradable(vnum):
            _chat_notice("Bu esya pazara konulamaz (ANTIFLAG_MYSHOP).")
            return (1 == 0)

        count = max(1, int(player.GetItemCount(slot)))
        sockets = [int(player.GetItemMetinSocket(slot, i)) for i in range(3)]
        base_name = self.engine.get_item_name(vnum)
        mkey, name = self._build_inv_market_key(vnum, base_name, sockets)

        if custom_total_price > 0:
            total_price = long(custom_total_price)
        else:
            unit_p = self.db.compute_smart_unit_price_for_key(mkey, vnum)
            if unit_p <= 0:
                _chat_notice("'%s' icin piyasa fiyati bulunamadi! Once pazarlarin taranmasini bekleyin." % name)
                return (1 == 0)
            total_price = long(unit_p) * long(count)

        for q in self.shop_add_queue:
            if q["slot"] == slot:
                return (1 == 0)

        self.shop_add_queue.append({
            "slot": slot,
            "vnum": vnum,
            "count": count,
            "price": total_price,
            "name": name,
        })
        msg = "PAZARA EKLEME KUYRUGU: %s x%d -> %s Yang (Slot #%d)" % (
            name, count, _fmt_yang(total_price), slot + 1
        )
        self.db.log_auto_event(msg)
        _chat_notice(msg)
        return (1 == 1)

    def queue_batch_inventory_to_my_shop(self, only_high_demand=(1 == 0)):
        """Queues all tradable inventory items that have a valid market price into the player's Offline Shop."""
        inv_items = self.get_inventory_market_items()
        queued = 0
        for r in inv_items:
            if r["smart_total"] <= 0 or r["offers"] < 1:
                continue
            if r["has_good_bonus"]:
                continue
            if only_high_demand and r["demand_tier"] < 1:
                continue
            # Skip equipment +7..+9 unless it's a material/book
            if "+9" in r["name"] or "+8" in r["name"]:
                continue
            if self.queue_add_inventory_slot_to_my_shop(r["slot"], r["smart_total"]):
                queued += 1
        if queued == 0:
            _chat_notice("Pazara otomatik konulacak uygun envanter esyasi bulunamadi.")
        else:
            _chat_notice("%d esya akilli piyasa fiyatiyla magazaniza eklenmek uzere kuyruga alindi!" % queued)
        return queued

    def queue_reprice_my_shop_item(self, my_item_rec):
        if not my_item_rec:
            return (1 == 0)
        item_id = int(my_item_rec.get("id", 0))
        new_total = long(my_item_rec.get("smart_total", 0))
        cur_total = long(my_item_rec.get("price", 0))
        if item_id <= 0 or new_total <= 0 or new_total == cur_total:
            return (1 == 0)
        for q in self.shop_edit_queue:
            if q["item_id"] == item_id:
                return (1 == 0)
        self.shop_edit_queue.append({
            "item_id": item_id,
            "price": new_total,
            "name": my_item_rec.get("name", "?"),
            "old_price": cur_total,
        })
        return (1 == 1)

    def reprice_all_my_shop_items(self):
        """Updates all items in the player's Offline Shop whose prices differ from the smart market price."""
        if not self.db.my_shop_items:
            self.request_my_shop_sync(silent=(1 == 1))
            _chat_notice("Magaza verisi senkronize ediliyor, 1 sn sonra tekrar basin.")
            return 0
        count = 0
        for it in self.db.my_shop_items:
            smart_total = int(it.get("smart_total", 0))
            cur_price = int(it.get("price", 0))
            if smart_total > 0 and abs(smart_total - cur_price) >= max(500, int(cur_price * 0.03)):
                if self.queue_reprice_my_shop_item(it):
                    count += 1
        if count > 0:
            msg = "OTO-FIYAT GUNCELLEME: Magazanizdaki %d esyanin fiyati piyasaya gore guncelleniyor!" % count
            self.db.log_auto_event(msg)
            _chat_notice(msg)
        else:
            _chat_notice("Magazanizdaki tum esyalarin fiyati zaten guncel piyasa seviyesinde.")
        return count

    def queue_remove_my_shop_item(self, item_id, name="?"):
        iid = int(item_id)
        if iid <= 0:
            return (1 == 0)
        self.shop_remove_queue.append({"item_id": iid, "name": name})
        _chat_notice("Magazadan geri cekme kuyruga eklendi: %s" % name)
        return (1 == 1)

    # --------------------------------------------------------------------------
    # Inventory Valuation & NPC Auto-Sell Engine
    # --------------------------------------------------------------------------
    def is_npc_shop_open(self):
        if shop is None or not hasattr(shop, "IsOpen"):
            return (1 == 0)
        try:
            return bool(shop.IsOpen())
        except Exception:
            return (1 == 0)

    def walk_and_open_nearest_npc(self):
        """Finds the nearest Shop NPC on the map, walks within interaction range, and opens the shop."""
        if self.is_npc_shop_open():
            _chat_notice("NPC dukkani zaten acik!")
            return (1 == 1)
        npc = self.engine.find_nearest_shop_npc()
        if npc is None:
            _chat_notice("Yakinda satici NPC bulunamadi! Lutfen Satici / Zirhci / Silahci yanina yaklasin.")
            return (1 == 0)
        vid = int(npc["vid"])
        dist = int(npc["dist"])
        if dist <= 280 and net is not None and hasattr(net, "SendOnClickPacket"):
            try:
                net.SendOnClickPacket(vid)
                _chat_notice("NPC aciliyor: %s (Mesafe: %dm)" % (npc["name"], dist // 100))
                return (1 == 1)
            except Exception:
                pass
        self.engine.move_character_to_xy(npc["x"], npc["y"])
        self.walking_to_npc = (1 == 1)
        self.walking_npc_vid = vid
        self.walking_npc_ts = time.time()
        _chat_notice("En yakin NPC'ye yurunuyor: %s (%dm) -> Varinca otomatik acilacak!" % (npc["name"], dist // 100))
        return (1 == 1)

    def get_inventory_npc_items(self):
        rows = []
        if player is None or not hasattr(player, "GetItemIndex"):
            return rows

        for slot in range(180):
            try:
                vnum = int(player.GetItemIndex(slot))
            except Exception:
                vnum = 0
            if vnum <= 0:
                continue

            try:
                count = max(1, int(player.GetItemCount(slot)))
            except Exception:
                count = 1

            npc_unit = self.engine.get_item_npc_unit_price(vnum)
            npc_total = int(npc_unit * count)
            if npc_total <= 0:
                continue

            name = self.engine.get_item_name(vnum)
            st = self.db.vnum_stats.get(str(vnum)) or self.db.vnum_stats.get(vnum)
            market_min_unit = int(st["min_unit"]) if st else 0
            market_med_unit = int(st["median_unit"]) if st else 0
            market_total = int(market_min_unit * count)

            attrs = []
            avg_dmg = 0
            has_good_bonus = (1 == 0)
            bonus_parts = []
            for a_idx in range(7):
                try:
                    atype, aval = player.GetItemAttribute(slot, a_idx)
                    atype, aval = int(atype), int(aval)
                except Exception:
                    atype, aval = 0, 0
                attrs.append((atype, aval))
                if atype != 0 and aval != 0:
                    if atype == ATTR_AVG_DMG:
                        avg_dmg = aval
                        if aval >= 35:
                            has_good_bonus = (1 == 1)
                    elif atype == ATTR_SKILL_DMG and aval >= 12:
                        has_good_bonus = (1 == 1)
                    elif aval >= 10:
                        has_good_bonus = (1 == 1)
                    bname = ATTR_SHORT_NAMES.get(atype, "Ef#%d" % atype)
                    bonus_parts.append("%s:%+d" % (bname, aval))

            is_arb_item = vnum in self.db.npc_arbitrage_vnums
            if is_arb_item or (market_min_unit > 0 and npc_unit > market_min_unit):
                category = "NPC_ARB_KAR"
                rec_label = "NPC'YE SAT (+%s)" % _fmt_yang_short(max(0, npc_total - market_total))
            elif market_min_unit > int(npc_unit * 1.35):
                category = "PAZARDA_DEGERLI"
                rec_label = "PAZARA KOY (%s)" % _fmt_yang_short(int(market_med_unit * count))
            elif has_good_bonus:
                category = "EFSUNLU_KORU"
                rec_label = "EFSUNLU (KORU)"
            else:
                category = "NPC_NORMAL"
                rec_label = "NPC SAT (%s)" % _fmt_yang_short(npc_total)

            rows.append({
                "slot": slot,
                "vnum": vnum,
                "name": name,
                "count": count,
                "npc_unit": npc_unit,
                "npc_total": npc_total,
                "market_min_unit": market_min_unit,
                "market_med_unit": market_med_unit,
                "market_total": market_total,
                "avg_dmg": avg_dmg,
                "has_good_bonus": has_good_bonus,
                "bonus_summary": " ".join(bonus_parts[:3]) if bonus_parts else "-",
                "category": category,
                "rec_label": rec_label,
            })

        rows.sort(key=lambda r: (
            0 if r["category"] == "NPC_ARB_KAR" else (1 if r["category"] == "NPC_NORMAL" else 2),
            -r["npc_total"],
            r["slot"]
        ))
        return rows

    def sell_single_inventory_slot(self, slot):
        if player is None:
            return (1 == 0)
        slot = int(slot)
        vnum = int(player.GetItemIndex(slot))
        if vnum <= 0:
            return (1 == 0)
        count = max(1, int(player.GetItemCount(slot)))
        npc_unit = self.engine.get_item_npc_unit_price(vnum)
        npc_total = int(npc_unit * count)
        name = self.engine.get_item_name(vnum)

        for q in self.npc_sell_queue:
            if q["slot"] == slot:
                return (1 == 0)

        self.npc_sell_queue.append({
            "slot": slot,
            "vnum": vnum,
            "count": count,
            "npc_total": npc_total,
            "name": name,
        })
        if not self.is_npc_shop_open():
            self.walk_and_open_nearest_npc()
            _chat_notice("'%s' NPC satis kuyruguna alindi. En yakin NPC acilinca otomatik satilacak!" % name)
        return (1 == 1)

    def sell_inventory_items_to_npc(self, only_arbitrage=(1 == 0)):
        inv_rows = self.get_inventory_npc_items()
        queued = 0
        total_expected = 0
        for r in inv_rows:
            if r["has_good_bonus"]:
                continue
            if only_arbitrage:
                if r["category"] != "NPC_ARB_KAR":
                    continue
            else:
                if r["category"] not in ("NPC_ARB_KAR", "NPC_NORMAL"):
                    continue
                if "+9" in r["name"] or "+8" in r["name"] or "+7" in r["name"]:
                    continue

            already = (1 == 0)
            for q in self.npc_sell_queue:
                if q["slot"] == r["slot"]:
                    already = (1 == 1)
                    break
            if not already:
                self.npc_sell_queue.append({
                    "slot": r["slot"],
                    "vnum": r["vnum"],
                    "count": r["count"],
                    "npc_total": r["npc_total"],
                    "name": r["name"],
                })
                queued += 1
                total_expected += r["npc_total"]

        if queued == 0:
            _chat_notice("NPC'ye satilacak uygun esya bulunamadi.")
            return 0

        if not self.is_npc_shop_open():
            self.walk_and_open_nearest_npc()
        else:
            _chat_notice("%d esya NPC'ye satiliyor (Beklenen gelir: +%s Yang)..." % (queued, _fmt_yang(total_expected)))
        return queued

    def _tick_npc_walk_and_sell(self, now):
        if self.walking_to_npc:
            if self.is_npc_shop_open():
                self.walking_to_npc = (1 == 0)
            elif now - self.walking_npc_ts > 8.0:
                self.walking_to_npc = (1 == 0)
            else:
                npc = self.engine.find_nearest_shop_npc()
                if npc and int(npc["dist"]) <= 275 and net is not None and hasattr(net, "SendOnClickPacket"):
                    try:
                        net.SendOnClickPacket(int(npc["vid"]))
                        self.walking_to_npc = (1 == 0)
                    except Exception:
                        pass

        if not self.is_npc_shop_open():
            return

        if not self.npc_sell_queue and self.auto_npc_sell_arbitrage and self.db.npc_arbitrage_vnums:
            if now - self.last_npc_sell_ts >= 0.8:
                for slot in range(180):
                    try:
                        vnum = int(player.GetItemIndex(slot))
                    except Exception:
                        vnum = 0
                    if vnum > 0 and vnum in self.db.npc_arbitrage_vnums:
                        cnt = max(1, int(player.GetItemCount(slot)))
                        npc_u = self.engine.get_item_npc_unit_price(vnum)
                        self.npc_sell_queue.append({
                            "slot": slot,
                            "vnum": vnum,
                            "count": cnt,
                            "npc_total": int(npc_u * cnt),
                            "name": self.engine.get_item_name(vnum),
                        })

        if not self.npc_sell_queue:
            return
        if now - self.last_npc_sell_ts < 0.22:
            return

        req = self.npc_sell_queue.pop(0)
        slot = int(req["slot"])
        expected_vnum = int(req["vnum"])
        cur_vnum = int(player.GetItemIndex(slot)) if player else 0
        if cur_vnum <= 0 or (expected_vnum > 0 and cur_vnum != expected_vnum):
            return

        cnt = max(1, int(player.GetItemCount(slot)))
        sold_ok = (1 == 0)
        try:
            if net is not None and hasattr(net, "SendShopSellPacketNew"):
                net.SendShopSellPacketNew(slot, cnt, 1)
                sold_ok = (1 == 1)
            elif net is not None and hasattr(net, "SendShopSellPacket"):
                net.SendShopSellPacket(slot)
                sold_ok = (1 == 1)
        except Exception as e:
            _tool_log("[NPC_SELL_ERR] %s" % e)

        if sold_ok:
            self.last_npc_sell_ts = now
            self.db.record_npc_sale(req.get("npc_total", 0))
            _chat_notice("NPC SATILDI: %s x%d (+%s Yang)" % (
                req.get("name", "?"), cnt, _fmt_yang(req.get("npc_total", 0))
            ))

    # --------------------------------------------------------------------------
    # Own Offline Shop Automation State Machine (Add / Edit / Remove / Create)
    # --------------------------------------------------------------------------
    def _tick_shop_automation(self, now):
        if offlineshop is None:
            return

        # Periodically refresh player's own shop status if not yet synced
        if self.db.my_shop_last_sync_ts == 0.0 and now - self.last_my_shop_auto_sync_ts > 5.0:
            if self.in_flight_owner == 0 and self.active_buy_req is None:
                self.request_my_shop_sync(silent=(1 == 1))
                return

        has_pending_ops = bool(self.shop_add_queue or self.shop_edit_queue or self.shop_remove_queue)
        if not has_pending_ops:
            return

        if now - self.last_shop_op_ts < 0.38:
            return

        # Ensure we have synced own shop status recently before adding/editing
        if self.my_shop_sync_in_flight:
            if now - self.my_shop_sync_ts > 2.5:
                self.my_shop_sync_in_flight = (1 == 0)
            else:
                return

        if now - self.db.my_shop_last_sync_ts > 30.0:
            self.request_my_shop_sync(silent=(1 == 1))
            return

        # 1. Process shop_add_queue
        if self.shop_add_queue:
            # If player does not have an open Offline Shop yet, create one with all queued items!
            if not self.db.my_shop_open:
                items_tuple_list = []
                names_added = []
                while self.shop_add_queue and len(items_tuple_list) < 40:
                    q = self.shop_add_queue.pop(0)
                    slot = int(q["slot"])
                    cur_vnum = int(player.GetItemIndex(slot)) if player else 0
                    if cur_vnum > 0 and cur_vnum == int(q["vnum"]) and long(q["price"]) > 0:
                        items_tuple_list.append((1, slot, long(q["price"])))
                        names_added.append("%s (%s)" % (q["name"], _fmt_yang_short(q["price"])))
                if items_tuple_list and hasattr(offlineshop, "SendShopCreate"):
                    try:
                        title = str(self.db.my_shop_title or "PAZAR")[:28]
                        offlineshop.SendShopCreate(title, 7200, tuple(items_tuple_list))
                        self.last_shop_op_ts = now
                        msg = "OTO-MAGAZA KURULDU ('%s'): %d esya satisa cikarildi!" % (title, len(items_tuple_list))
                        self.db.log_auto_event(msg)
                        _chat_notice(msg)
                        self.db.my_shop_last_sync_ts = 0.0
                    except Exception as e:
                        _tool_log("[SHOP_CREATE_ERR] %s" % e)
                return

            # Player already has an open Offline Shop -> SendAddItem(1, slot, long(price))
            q = self.shop_add_queue.pop(0)
            slot = int(q["slot"])
            cur_vnum = int(player.GetItemIndex(slot)) if player else 0
            if cur_vnum <= 0 or (int(q["vnum"]) > 0 and cur_vnum != int(q["vnum"])):
                return
            price = long(q["price"])
            if price <= 0:
                return
            try:
                offlineshop.SendAddItem(1, slot, price)
                self.last_shop_op_ts = now
                msg = "MAGAZAYA EKLENDI: %s x%d -> %s Yang" % (q["name"], q["count"], _fmt_yang(price))
                self.db.log_auto_event(msg)
                _chat_notice(msg)
                # Trigger a silent sync after last item in queue
                if not self.shop_add_queue:
                    self.db.my_shop_last_sync_ts = 0.0
            except Exception as e:
                _tool_log("[SHOP_ADD_ERR] %s" % e)
            return

        # 2. Process shop_edit_queue
        if self.shop_edit_queue:
            q = self.shop_edit_queue.pop(0)
            iid = int(q["item_id"])
            new_p = long(q["price"])
            if iid > 0 and new_p > 0 and hasattr(offlineshop, "SendEditItem"):
                try:
                    offlineshop.SendEditItem(iid, new_p)
                    self.last_shop_op_ts = now
                    msg = "FIYAT GUNCELLENDI: %s (%s -> %s Yang)" % (
                        q.get("name", "?"), _fmt_yang_short(q.get("old_price", 0)), _fmt_yang_short(new_p)
                    )
                    self.db.log_auto_event(msg)
                    if not self.shop_edit_queue:
                        _chat_notice("Magaza fiyat guncellemeleri tamamlandi.")
                        self.db.my_shop_last_sync_ts = 0.0
                except Exception as e:
                    _tool_log("[SHOP_EDIT_ERR] %s" % e)
            return

        # 3. Process shop_remove_queue
        if self.shop_remove_queue:
            q = self.shop_remove_queue.pop(0)
            iid = int(q["item_id"])
            if iid > 0 and hasattr(offlineshop, "SendRemoveItem"):
                try:
                    offlineshop.SendRemoveItem(iid)
                    self.last_shop_op_ts = now
                    msg = "MAGAZADAN CEKILDI: %s" % q.get("name", "?")
                    self.db.log_auto_event(msg)
                    _chat_notice(msg)
                    if not self.shop_remove_queue:
                        self.db.my_shop_last_sync_ts = 0.0
                except Exception as e:
                    _tool_log("[SHOP_REMOVE_ERR] %s" % e)
            return

    def _is_busy_with_user_action(self, now):
        if self.active_buy_req is not None or len(self.pending_buy_queue) > 0:
            return (1 == 1)
        if now < self.user_open_shop_until:
            return (1 == 1)
        # Only pause background scanning for NPC selling if NPC shop is actually open!
        if self.npc_sell_queue and self.is_npc_shop_open():
            return (1 == 1)
        if self.my_shop_sync_in_flight or self.safebox_sync_in_flight:
            return (1 == 1)
        if self.shop_add_queue or self.shop_edit_queue or self.shop_remove_queue:
            return (1 == 1)
        # Pause background scanning while native OfflineShop UI window is open so user can manage their shop peacefully
        try:
            if self.hooked_board is not None:
                wnd = getattr(self.hooked_board, "wndOffShop", None)
                if wnd is not None and hasattr(wnd, "IsShow") and wnd.IsShow():
                    return (1 == 1)
        except Exception:
            pass
        return (1 == 0)

    def _tick_buy_state_machine(self, now):
        if self.active_buy_req is None and self.pending_buy_queue:
            self.active_buy_req = self.pending_buy_queue.pop(0)
            self.active_buy_req["state"] = "SEND_OPEN"
            self.active_buy_req["started_ts"] = now

        req = self.active_buy_req
        if req is None:
            return

        state = req.get("state", "")
        owner_id = int(req.get("owner_id", 0))
        item_id = int(req.get("item_id", 0))

        if state == "SEND_OPEN":
            self.in_flight_owner = 0
            self.silent_intercept_until = now + 2.5
            req["state"] = "WAIT_OPEN"
            req["open_sent_ts"] = now
            req["yang_before"] = self.engine.get_player_yang()
            req["inv_before"] = self._snapshot_inventory_slots()
            try:
                self._send_open_foreign_shop(owner_id, force=(1 == 1))
            except Exception as e:
                _tool_log("[BUY_OPEN_ERR] %s" % e)
                self.active_buy_req = None
            return

        if state == "WAIT_OPEN":
            if now - req.get("open_sent_ts", now) > 1.8:
                req["state"] = "SEND_BUY"
            return

        if state == "SEND_BUY":
            try:
                offlineshop.SendBuyItem(owner_id, item_id)
                req["state"] = "WAIT_CONFIRM"
                req["buy_sent_ts"] = now
            except Exception as e:
                _tool_log("[BUY_SEND_ERR] %s" % e)
                self.active_buy_req = None
            return

        if state == "WAIT_CONFIRM":
            cur_yang = self.engine.get_player_yang()
            yang_before = req.get("yang_before", cur_yang)
            inv_before = req.get("inv_before", {})
            inv_now = self._snapshot_inventory_slots()

            # Find newly acquired or incremented slot matching the item vnum
            new_slot = -1
            expected_vnum = int(req.get("vnum", 0))
            for sl, (vn, cnt) in inv_now.items():
                if expected_vnum > 0 and vn != expected_vnum:
                    continue
                if sl not in inv_before or inv_before[sl][1] < cnt:
                    new_slot = sl
                    break

            if cur_yang < yang_before or new_slot >= 0:
                self.db.remove_bought_item(owner_id, item_id)
                msg = "ALINDI: %s x%d (%s Yang)" % (req.get("name", "?"), req.get("count", 1), _fmt_yang(req.get("price", 0)))
                self.db.log_auto_event(msg)
                _chat_notice(msg)

                # Automatic relisting into player's own Offline Shop if auto_list is enabled!
                if req.get("auto_list") and new_slot >= 0 and long(req.get("resale_total", 0)) > 0:
                    self.queue_add_inventory_slot_to_my_shop(new_slot, req["resale_total"])

                self.active_buy_req = None
                return

            if now - req.get("buy_sent_ts", now) > 0.65:
                self.db.remove_bought_item(owner_id, item_id)
                self.active_buy_req = None
            return

    def force_full_rescan(self):
        shops = self.engine.scan_map_shops()
        self.db.update_map_shops(shops)
        self.scan_queue = []
        self.queued_set.clear()
        for oid in sorted(self.db.map_shops.keys(), key=lambda k: self.db.map_shops[k]["dist"]):
            if self.db.is_our_own_shop(oid):
                continue
            self.scan_queue.append(oid)
            self.queued_set.add(oid)
        _chat_notice("Tum harita pazarlari yeniden tarama kuyruguna eklendi (%d pazar)." % len(self.scan_queue))

    def tick(self):
        now = time.time()
        self.ensure_board_hook()

        # Tick main.py SuiteController if active (so Farm Bot / Waithack / Efsun / Auto-Pot run seamlessly!)
        if self.suite_ctrl is not None:
            try:
                self.suite_ctrl.on_update()
            except Exception:
                pass

        self._tick_buy_state_machine(now)
        self._tick_npc_walk_and_sell(now)
        self._tick_shop_automation(now)

        if now - self.last_map_poll_ts >= 1.5:
            self.last_map_poll_ts = now
            self.db.refresh_map_shops()
            for vid, mshop in sorted(self.db.map_shops.items(), key=lambda kv: kv[1]["dist"]):
                db_oid = int(mshop.get("db_owner_id", 0)) or int(self.db.owner_id_by_vid.get(vid, 0))
                if self.db.is_our_own_shop(db_oid, mshop.get("owner", "")):
                    continue
                if vid in self.queued_set or vid == self.in_flight_owner:
                    continue
                scanned = self.db.scanned_shops.get(db_oid) or self.db.scanned_shops.get(vid)
                if scanned is None or (now - scanned.get("ts", 0.0) >= self.rescan_cooldown):
                    self.scan_queue.append(vid)
                    self.queued_set.add(vid)

        if self.in_flight_owner != 0 and (now - self.in_flight_ts) > 1.35:
            self.in_flight_owner = 0

        if not self.auto_scan_enabled:
            return
        if self._is_busy_with_user_action(now):
            return
        if self.in_flight_owner != 0:
            return
        if not self.scan_queue:
            return
        if now - self.last_scan_send_ts < self.scan_interval:
            return

        next_oid = self.scan_queue.pop(0)
        self.queued_set.discard(next_oid)
        if self.db.is_our_own_shop(next_oid):
            return
        self.in_flight_owner = next_oid
        self.in_flight_ts = now
        self.last_scan_send_ts = now
        self.silent_intercept_until = now + 1.25

        try:
            self._send_open_foreign_shop(next_oid, force=(1 == 0))
        except Exception as e:
            _tool_log("[SCAN_SEND_ERR] oid=%d err=%s" % (next_oid, e))
            self.in_flight_owner = 0


# ==============================================================================
# 5. MULTI-MODULE IN-GAME SUITE GUI (PAZAR + OTO-MAGAZA + FARM + SAVAS/ARACLAR)
# ==============================================================================
class OfflineShopSuiteGUI(object):
    WIDTH = 900
    HEIGHT = 536
    ROWS_PER_PAGE = 11

    def __init__(self, engine, db, scanner):
        self.engine = engine
        self.db = db
        self.scanner = scanner

        self.widgets = []
        self.visible = (1 == 1)
        self.module_idx = 0   # 0: Pazar, 1: Oto-Magaza, 2: Farm Bot, 3: Savas & Araclar
        self.sub_idx = 0      # 0..4 within current module
        self.page = 0
        self.total_pages = 1
        self.sort_mode = 0    # 0: BirimFiyat+, 1: Indirim/Kar-, 2: ToplamFiyat+, 3: Mesafe+, 4: Talep-
        self.filter_mode = 0  # 0: Tumu, 1: Efsunlu, 2: Ort35+, 3: BK/Tas/Sandik, 4: YuksekTalep
        self.budget_filter_only = (1 == 0)
        self.pricing_mode = 0

        self.search_query = ""
        self.filtered_rows = []
        self.last_rendered_rev = -1
        self.last_ui_refresh_ts = 0.0
        self.last_hotkey_ts = {}

        self.main_win = None
        self.toggle_win = None
        self.module_btns = []
        self.sub_btns = []
        self.row_Controls = []
        self.input_edits = {}
        self.action_btn_1 = None
        self.action_btn_2 = None
        self.action_btn_3 = None

        self._build_ui()

    def _keep(self, w):
        self.widgets.append(w)
        return w

    def _make_bar(self, parent, x, y, w, h, color):
        b = ui.Bar()
        b.SetParent(parent)
        b.SetPosition(x, y)
        b.SetSize(w, h)
        b.SetColor(color)
        b.Show()
        return self._keep(b)

    def _make_text(self, parent, x, y, text, color=0xFFE8EEF5, center=(1 == 0)):
        t = ui.TextLine()
        t.SetParent(parent)
        t.SetPosition(x, y)
        t.SetPackedFontColor(color)
        t.SetText(_safe_ascii(text))
        if center and hasattr(t, "SetHorizontalAlignCenter"):
            t.SetHorizontalAlignCenter()
        t.Show()
        return self._keep(t)

    def _make_rect_border(self, parent, x, y, w, h, color):
        self._make_bar(parent, x, y, w, 1, color)
        self._make_bar(parent, x, y + h - 1, w, 1, color)
        self._make_bar(parent, x, y, 1, h, color)
        self._make_bar(parent, x + w - 1, y, 1, h, color)

    def _make_btn(self, parent, x, y, w, h, label, bg_color, border_color, text_color, cmd):
        bar = ui.Bar()
        bar.SetParent(parent)
        bar.SetPosition(x, y)
        bar.SetSize(w, h)
        bar.SetColor(bg_color)
        bar.Show()
        self._keep(bar)

        b_top = self._make_bar(bar, 0, 0, w, 1, border_color)
        b_bot = self._make_bar(bar, 0, h - 1, w, 1, border_color)
        b_lft = self._make_bar(bar, 0, 0, 1, h, border_color)
        b_rgt = self._make_bar(bar, w - 1, 0, 1, h, border_color)

        txt = ui.TextLine()
        txt.SetParent(bar)
        txt.SetPosition(w // 2, max(1, (h - 14) // 2))
        if hasattr(txt, "SetHorizontalAlignCenter"):
            txt.SetHorizontalAlignCenter()
        txt.SetPackedFontColor(text_color)
        txt.SetText(_safe_ascii(label))
        txt.Show()
        self._keep(txt)

        def _on_click():
            try:
                cmd()
            except Exception as e:
                _tool_log("[BTN_ERR] %s\n%s" % (e, traceback.format_exc()))

        for widget in (bar, txt):
            if hasattr(widget, "SetMouseLeftButtonDownEvent"):
                try:
                    widget.SetMouseLeftButtonDownEvent(ui.__mem_func__(_on_click) if hasattr(ui, "__mem_func__") else _on_click)
                except Exception:
                    try:
                        widget.OnMouseLeftButtonDown = _on_click
                    except Exception:
                        pass
            else:
                try:
                    widget.OnMouseLeftButtonDown = _on_click
                except Exception:
                    pass

        return {
            "bar": bar,
            "txt": txt,
            "borders": (b_top, b_bot, b_lft, b_rgt),
            "set_text": lambda s: txt.SetText(_safe_ascii(s)),
            "set_color": lambda c: bar.SetColor(c),
            "set_text_color": lambda c: txt.SetPackedFontColor(c),
            "show": lambda: bar.Show(),
            "hide": lambda: bar.Hide(),
        }

    def _make_edit(self, parent, x, y, w, h, default_text="", max_len=36):
        bg = self._make_bar(parent, x, y, w, h, 0xFF0A0F18)
        self._make_rect_border(bg, 0, 0, w, h, 0xFF2E496E)

        ed = ui.EditLine()
        ed.SetParent(bg)
        ed.SetPosition(6, max(2, (h - 14) // 2))
        ed.SetSize(w - 12, h - 4)
        ed.SetMax(max_len)
        ed.SetPackedFontColor(0xFFF5F8FA)
        ed.SetText(_safe_ascii(default_text))
        ed.Show()
        self._keep(ed)

        def _focus_edit():
            try:
                ed.SetFocus()
            except Exception:
                pass

        if hasattr(bg, "SetMouseLeftButtonDownEvent"):
            try:
                bg.SetMouseLeftButtonDownEvent(_focus_edit)
            except Exception:
                pass
        return {"bg": bg, "edit": ed}

    def _build_ui(self):
        if ui is None:
            return
        try:
            screen_w = wndMgr.GetScreenWidth() if wndMgr else 1280
            screen_h = wndMgr.GetScreenHeight() if wndMgr else 768
        except Exception:
            screen_w, screen_h = 1280, 768

        # Floating mini-toggle button on top-right
        self.toggle_win = ui.Window()
        self.toggle_win.SetSize(165, 26)
        self.toggle_win.SetPosition(max(10, screen_w - 185), 8)
        if hasattr(self.toggle_win, "AddFlag"):
            try:
                self.toggle_win.AddFlag("movable")
                self.toggle_win.AddFlag("float")
            except Exception:
                pass
        self.toggle_win.Show()
        self._keep(self.toggle_win)

        self.toggle_btn = self._make_btn(
            self.toggle_win, 0, 0, 165, 26,
            "AVRASYA2 BOT [INS]",
            0xE8101C2E, 0xFF00D4AA, 0xFF00FFCC,
            self.toggle_visibility
        )

        # Main Dashboard Window
        win_x = max(16, (screen_w - self.WIDTH) // 2)
        win_y = max(24, (screen_h - self.HEIGHT) // 2)

        self.main_win = ui.Window()
        self.main_win.SetSize(self.WIDTH, self.HEIGHT)
        self.main_win.SetPosition(win_x, win_y)
        if hasattr(self.main_win, "AddFlag"):
            try:
                self.main_win.AddFlag("movable")
                self.main_win.AddFlag("float")
            except Exception:
                pass
        self.main_win.Show()
        self._keep(self.main_win)

        # Outer frame & dark background
        self._make_bar(self.main_win, 0, 0, self.WIDTH, self.HEIGHT, 0xF40B1018)
        self._make_rect_border(self.main_win, 0, 0, self.WIDTH, self.HEIGHT, 0xFF28466C)

        # Header Bar (h=30)
        self._make_bar(self.main_win, 1, 1, self.WIDTH - 2, 30, 0xFF111C2D)
        self._make_bar(self.main_win, 1, 30, self.WIDTH - 2, 1, 0xFF00D4AA)

        self.title_lbl = self._make_text(
            self.main_win, 12, 7,
            "AVRASYA2 ALL-IN-ONE SUITE v2.0  |  PAZAR & AL-SAT  |  OTO-MAGAZA  |  FARM & SAVAS BOTU",
            0xFF00FFCC
        )
        self.stats_lbl = self._make_text(
            self.main_win, 535, 8,
            "Pazar: 0/0 | Esya: 0 | Firsat: 0",
            0xFFFFD166
        )

        self._make_btn(
            self.main_win, self.WIDTH - 68, 4, 62, 22,
            "GIZLE [X]", 0xFF4A1822, 0xFF9E3044, 0xFFFFB3C1,
            self.toggle_visibility
        )

        # Top-Level 4 Modules Bar (y=34, h=26)
        mod_defs = [
            (0, "1. PAZAR & FIRSATLAR", 218),
            (1, "2. OTO-MAGAZA & TICARET", 224),
            (2, "3. FARM & METIN BOTU", 216),
            (3, "4. SAVAS, EFSUN & ARACLAR", 218),
        ]
        mx = 8
        for m_idx, m_label, mw in mod_defs:
            btn = self._make_btn(
                self.main_win, mx, 34, mw, 26,
                m_label, 0xFF152236, 0xFF2C4870, 0xFFD0DFEF,
                lambda idx=m_idx: self.switch_module(idx)
            )
            self.module_btns.append(btn)
            mx += mw + 3

        # Sub-Tab Bar (5 dynamic sub-tabs + 3 global automation toggles, y=64, h=24)
        sx = 8
        for s_idx in range(5):
            btn = self._make_btn(
                self.main_win, sx, 64, 118, 24,
                "Sekme %d" % (s_idx + 1), 0xFF121C2C, 0xFF243B5C, 0xFF9EB4CC,
                lambda idx=s_idx: self.switch_subtab(idx)
            )
            self.sub_btns.append(btn)
            sx += 121

        # Quick Global Toggles on right side of Sub-Tab Bar
        self.scan_toggle_btn = self._make_btn(
            self.main_win, 616, 64, 92, 24,
            "Tarama: ACIK", 0xFF123B2A, 0xFF1E7E52, 0xFF66FFB2,
            self.toggle_auto_scan
        )
        self.autolist_toggle_btn = self._make_btn(
            self.main_win, 711, 64, 96, 24,
            "OtoPazar: ACIK", 0xFF123B2A, 0xFF1E7E52, 0xFF66FFB2,
            self.toggle_auto_list
        )
        self.autoflip_toggle_btn = self._make_btn(
            self.main_win, 810, 64, 82, 24,
            "OtoBot: KPL", 0xFF3A1E28, 0xFF7A3848, 0xFFFF99AA,
            self.toggle_auto_flip
        )

        # Control / Search / Action Bar (y=92, h=30)
        self._make_bar(self.main_win, 8, 92, self.WIDTH - 16, 30, 0xFF101928)
        self._make_rect_border(self.main_win, 8, 92, self.WIDTH - 16, 30, 0xFF1F334F)

        self._make_text(self.main_win, 14, 99, "Ara:", 0xFF8FB8E6)
        self.search_box = self._make_edit(self.main_win, 44, 96, 150, 22, "", 32)

        self._make_btn(
            self.main_win, 198, 96, 42, 22,
            "ARA", 0xFF1A3A5C, 0xFF2E6DA4, 0xFFE6F2FF,
            self.apply_search_input
        )
        self._make_btn(
            self.main_win, 243, 96, 36, 22,
            "SIL", 0xFF2B2233, 0xFF59416B, 0xFFD9C2EB,
            self.clear_search_input
        )

        self.sort_btn = self._make_btn(
            self.main_win, 283, 96, 114, 22,
            "Sira: BirimFiyat+", 0xFF192940, 0xFF31517A, 0xFFD0E4F7,
            self.cycle_sort_mode
        )
        self.filter_btn = self._make_btn(
            self.main_win, 400, 96, 102, 22,
            "Filtre: Tumu", 0xFF192940, 0xFF31517A, 0xFFD0E4F7,
            self.cycle_filter_mode
        )
        self.budget_btn = self._make_btn(
            self.main_win, 505, 96, 86, 22,
            "Butce: KPL", 0xFF192940, 0xFF31517A, 0xFFD0E4F7,
            self.toggle_budget_filter
        )

        # 3 Context-Sensitive Action Buttons on the right of Control Bar (x=595..888)
        self.action_btn_1 = self._make_btn(
            self.main_win, 595, 96, 98, 22,
            "PAZAR TARA", 0xFF163C40, 0xFF25737A, 0xFF7FFFD4,
            self.on_context_action_1
        )
        self.action_btn_2 = self._make_btn(
            self.main_win, 696, 96, 98, 22,
            "MAGAZAM SYNC", 0xFF2E2A16, 0xFF6B6027, 0xFFFFE066,
            self.on_context_action_2
        )
        self.action_btn_3 = self._make_btn(
            self.main_win, 797, 96, 91, 22,
            "FILTRE SIFIRLA", 0xFF3D2235, 0xFF7D3C68, 0xFFFFB8E6,
            self.on_context_action_3
        )

        # Table Column Header Bar (y=126, h=22)
        self._make_bar(self.main_win, 8, 126, self.WIDTH - 16, 22, 0xFF17263B)
        self._make_bar(self.main_win, 8, 147, self.WIDTH - 16, 1, 0xFF2E4D73)

        self.col_hdr_1 = self._make_text(self.main_win, 14, 130, "ESYA / HEDEF ADI", 0xFF80BFFF)
        self.col_hdr_2 = self._make_text(self.main_win, 232, 130, "AD", 0xFF80BFFF)
        self.col_hdr_3 = self._make_text(self.main_win, 272, 130, "BIRIM FIYAT", 0xFF80BFFF)
        self.col_hdr_4 = self._make_text(self.main_win, 376, 130, "TOPLAM / PIYASA", 0xFF80BFFF)
        self.col_hdr_5 = self._make_text(self.main_win, 488, 130, "KAR / DURUM", 0xFF80BFFF)
        self.col_hdr_6 = self._make_text(self.main_win, 580, 130, "DETAY / ARZ-TALEP", 0xFF80BFFF)
        self.col_hdr_7 = self._make_text(self.main_win, 738, 130, "ISLEMLER", 0xFF80BFFF)

        # Table Rows (11 rows, y=150..458, each h=27)
        row_y = 150
        for r_idx in range(self.ROWS_PER_PAGE):
            bg_col = 0xFF0E1623 if (r_idx % 2 == 0) else 0xFF131D2E
            row_bar = self._make_bar(self.main_win, 8, row_y, self.WIDTH - 16, 26, bg_col)

            c1 = self._make_text(row_bar, 6, 6, "", 0xFFF0F4F8)
            c2 = self._make_text(row_bar, 224, 6, "", 0xFFD0DCE8)
            c3 = self._make_text(row_bar, 264, 6, "", 0xFFFFE066)
            c4 = self._make_text(row_bar, 368, 6, "", 0xFF99E6B3)
            c5 = self._make_text(row_bar, 480, 6, "", 0xFF66FF99)
            c6 = self._make_text(row_bar, 572, 6, "", 0xFFB8C8D8)

            btn_buy = self._make_btn(
                row_bar, 718, 3, 76, 20,
                "AL+PAZAR", 0xFF14452F, 0xFF248F59, 0xFF80FFBF,
                lambda idx=r_idx: self.on_row_primary_action(idx)
            )
            btn_open = self._make_btn(
                row_bar, 797, 3, 42, 20,
                "AC", 0xFF1C3554, 0xFF34659E, 0xFFB3D9FF,
                lambda idx=r_idx: self.on_row_secondary_action(idx)
            )
            btn_go = self._make_btn(
                row_bar, 842, 3, 38, 20,
                "GIT", 0xFF3A2847, 0xFF6E4B87, 0xFFE6CCFF,
                lambda idx=r_idx: self.on_row_tertiary_action(idx)
            )

            self.row_Controls.append({
                "bar": row_bar,
                "base_color": bg_col,
                "c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5, "c6": c6,
                "btn_buy": btn_buy, "btn_open": btn_open, "btn_go": btn_go,
            })
            row_y += 28

        # Sniper Quick-Add Bar (y=460, h=30)
        self.sniper_bar = self._make_bar(self.main_win, 8, 460, self.WIDTH - 16, 30, 0xFF141E30)
        self._make_rect_border(self.sniper_bar, 0, 0, self.WIDTH - 16, 30, 0xFF2B4469)
        self.sniper_lbl_1 = self._make_text(self.sniper_bar, 8, 7, "Hizli Sniper Esya/Vnum:", 0xFFFFCC66)
        self.sniper_q_edit = self._make_edit(self.sniper_bar, 146, 4, 150, 22, "Hava Kilici", 28)
        self._make_text(self.sniper_bar, 304, 7, "Maks Birim:", 0xFFFFCC66)
        self.sniper_p_edit = self._make_edit(self.sniper_bar, 374, 4, 100, 22, "500000", 16)
        self._make_text(self.sniper_bar, 482, 7, "Min Ort:", 0xFFFFCC66)
        self.sniper_d_edit = self._make_edit(self.sniper_bar, 532, 4, 46, 22, "0", 4)
        self._make_btn(
            self.sniper_bar, 586, 4, 96, 22,
            "+ KURAL EKLE", 0xFF184A34, 0xFF288A5E, 0xFF80FFBF,
            self.on_add_sniper_rule_click
        )
        self._make_btn(
            self.sniper_bar, 686, 4, 114, 22,
            "AKILLI KURALLAR", 0xFF1C3554, 0xFF34659E, 0xFFB3D9FF,
            self.on_populate_smart_sniper_click
        )
        self._make_btn(
            self.sniper_bar, 804, 4, 74, 22,
            "TEMIZLE", 0xFF4A1B26, 0xFF8A3347, 0xFFFFB3C1,
            self.on_clear_sniper_rules_click
        )

        # Footer & Pagination Bar (y=496, h=32)
        self._make_bar(self.main_win, 8, 496, self.WIDTH - 16, 32, 0xFF111C2D)
        self._make_rect_border(self.main_win, 8, 496, self.WIDTH - 16, 32, 0xFF23395B)

        self.footer_info_lbl = self._make_text(
            self.main_win, 16, 504,
            "Durum: Hazir | Yang: 0 | Kuyruk: 0",
            0xFFA8C6E8
        )

        self._make_btn(
            self.main_win, self.WIDTH - 245, 501, 68, 22,
            "< ONCEKI", 0xFF1A2C47, 0xFF315282, 0xFFD9E8F5,
            self.prev_page
        )
        self.page_lbl = self._make_text(
            self.main_win, self.WIDTH - 140, 505,
            "Sayfa 1 / 1", 0xFFFFE066, center=(1 == 1)
        )
        self._make_btn(
            self.main_win, self.WIDTH - 102, 501, 86, 22,
            "SONRAKI >", 0xFF1A2C47, 0xFF315282, 0xFFD9E8F5,
            self.next_page
        )

        self.switch_module(0)

    # --------------------------------------------------------------------------
    # Navigation & Controls
    # --------------------------------------------------------------------------
    def toggle_visibility(self):
        self.visible = not self.visible
        if self.main_win is not None:
            if self.visible:
                self.main_win.Show()
                self.refresh_table(force=(1 == 1))
            else:
                self.main_win.Hide()

    def _get_subtab_labels(self, mod_idx):
        if mod_idx == 0:
            return [
                "Pazar Arama",
                "Al-Sat (%d)" % len(self.db.bargains),
                "NPC Kar (%d)" % len(self.db.npc_bargains),
                "Pazarlar (%d)" % len(self.db.map_shops),
                "Canli Satis (%d)" % self.db.total_live_sales,
            ]
        elif mod_idx == 1:
            return [
                "Envanter->Pazar",
                "Magazam (%d)" % len(self.db.my_shop_items),
                "Envanter->NPC",
                "Oto-Sniper (%d)" % len(self.db.sniper_rules),
                "Pazar Kasasi",
            ]
        elif mod_idx == 2:
            return [
                "Metin & Boss",
                "Harita Hedefleri",
                "Farm Ayarlari",
                "Oto-Pot & Skill",
                "Loot & Guvenlik",
            ]
        else:
            return [
                "Waithack & Hiz",
                "Kombo & Sekmeme",
                "Efsun & +Basma",
                "Wallhack & Zoom",
                "Sistem & Rapor",
            ]

    def switch_module(self, mod_idx):
        self.module_idx = int(mod_idx) % 4
        self.sub_idx = 0
        self.page = 0
        if self.module_idx == 1:
            self.scanner.request_my_shop_sync(silent=(1 == 1))
        elif self.module_idx in (2, 3):
            self.scanner.get_suite_controller()
        self._update_navigation_styles()
        self.refresh_table(force=(1 == 1))

    def switch_subtab(self, sub_idx):
        self.sub_idx = int(sub_idx) % 5
        self.page = 0
        if self.module_idx == 1 and self.sub_idx == 1:
            self.scanner.request_my_shop_sync(silent=(1 == 1))
        elif self.module_idx == 1 and self.sub_idx == 4:
            self.scanner.request_safebox_sync(withdraw_all=(1 == 0))
        self._update_navigation_styles()
        self.refresh_table(force=(1 == 1))

    def _update_navigation_styles(self):
        for idx, btn in enumerate(self.module_btns):
            if idx == self.module_idx:
                btn["set_color"](0xFF1F4E78)
                btn["set_text_color"](0xFF00FFCC)
            else:
                btn["set_color"](0xFF142033)
                btn["set_text_color"](0xFFA2B9D4)

        sub_labels = self._get_subtab_labels(self.module_idx)
        for idx, btn in enumerate(self.sub_btns):
            if idx < len(sub_labels):
                btn["set_text"](sub_labels[idx])
            if idx == self.sub_idx:
                btn["set_color"](0xFF1B4366)
                btn["set_text_color"](0xFFFFE066)
            else:
                btn["set_color"](0xFF121C2C)
                btn["set_text_color"](0xFF9EB4CC)

        # Context Action Buttons per Module/Subtab
        if self.module_idx == 0:
            self.action_btn_1["set_text"]("TUMUNU TARA")
            self.action_btn_2["set_text"]("FIYAT: %s" % ("REKABET" if self.pricing_mode == 0 else ("DENGE" if self.pricing_mode == 1 else "MAKS")))
            self.action_btn_3["set_text"]("FILTRE SIFIRLA")
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                self.action_btn_1["set_text"]("TUMUNU PAZARA")
                self.action_btn_2["set_text"]("FIYAT: %s" % ("REKABET" if self.pricing_mode == 0 else ("DENGE" if self.pricing_mode == 1 else "MAKS")))
                self.action_btn_3["set_text"]("MAGAZAMI AC")
            elif self.sub_idx == 1:
                self.action_btn_1["set_text"]("FIYAT GUNCELLE")
                self.action_btn_2["set_text"]("MAGAZA YENILE")
                self.action_btn_3["set_text"]("KASAYI CEK")
            elif self.sub_idx == 2:
                self.action_btn_1["set_text"]("NPC'YE YURU")
                self.action_btn_2["set_text"]("ARB ESYA SAT")
                self.action_btn_3["set_text"]("COP ESYA SAT")
            else:
                self.action_btn_1["set_text"]("AKILLI KURAL")
                self.action_btn_2["set_text"]("KASAYI CEK")
                self.action_btn_3["set_text"]("MAGAZA YENILE")
        elif self.module_idx == 2:
            self.action_btn_1["set_text"]("FARM BASLAT/DUR")
            self.action_btn_2["set_text"]("EN YAKIN METIN")
            self.action_btn_3["set_text"]("PELERIN BAS")
        else:
            self.action_btn_1["set_text"]("WAITHACK AC/KPL")
            self.action_btn_2["set_text"]("WALLHACK AC/KPL")
            self.action_btn_3["set_text"]("RAPOR KAYDET")

        # Update Column Headers
        if self.module_idx == 0:
            if self.sub_idx == 3:
                self.col_hdr_1.SetText("PAZAR SAHIBI")
                self.col_hdr_2.SetText("ESYA")
                self.col_hdr_3.SetText("MESAFE")
                self.col_hdr_4.SetText("KOORDINAT")
                self.col_hdr_5.SetText("DURUM")
                self.col_hdr_6.SetText("PAZAR BASLIGI")
            elif self.sub_idx == 4:
                self.col_hdr_1.SetText("ESYA / OLAY")
                self.col_hdr_2.SetText("AD")
                self.col_hdr_3.SetText("BIRIM FIYAT")
                self.col_hdr_4.SetText("TOPLAM FIYAT")
                self.col_hdr_5.SetText("SAAT")
                self.col_hdr_6.SetText("SATICI / DETAY")
            else:
                self.col_hdr_1.SetText("ESYA ADI")
                self.col_hdr_2.SetText("AD")
                self.col_hdr_3.SetText("BIRIM FIYAT")
                self.col_hdr_4.SetText("TOPLAM FIYAT")
                self.col_hdr_5.SetText("NET KAR / IND")
                self.col_hdr_6.SetText("ARZ-TALEP | SATICI")
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                self.col_hdr_1.SetText("ENVANTER ESYASI (SLOT)")
                self.col_hdr_2.SetText("AD")
                self.col_hdr_3.SetText("ONERILEN BIRIM")
                self.col_hdr_4.SetText("TOPLAM SATIS")
                self.col_hdr_5.SetText("PIYASA MIN")
                self.col_hdr_6.SetText("TALEP | TEKLIF SAYISI")
            elif self.sub_idx == 1:
                self.col_hdr_1.SetText("MAGAZAMDAKI ESYA")
                self.col_hdr_2.SetText("AD")
                self.col_hdr_3.SetText("MEVCUT BIRIM")
                self.col_hdr_4.SetText("ONERILEN TOPLAM")
                self.col_hdr_5.SetText("DURUM")
                self.col_hdr_6.SetText("PIYASA KIYASLAMASI")
            elif self.sub_idx == 2:
                self.col_hdr_1.SetText("ENVANTER ESYASI (SLOT)")
                self.col_hdr_2.SetText("AD")
                self.col_hdr_3.SetText("NPC TOPLAM")
                self.col_hdr_4.SetText("PAZAR EN UCUZ")
                self.col_hdr_5.SetText("ONERI")
                self.col_hdr_6.SetText("EFSUN / UYARI")
            elif self.sub_idx == 3:
                self.col_hdr_1.SetText("SNIPER ARAMA / VNUM")
                self.col_hdr_2.SetText("ORT")
                self.col_hdr_3.SetText("MAKS BIRIM")
                self.col_hdr_4.SetText("ALINAN ADET")
                self.col_hdr_5.SetText("DURUM")
                self.col_hdr_6.SetText("OTO-PAZAR MODU")
            else:
                self.col_hdr_1.SetText("KASA / SATILAN ESYA")
                self.col_hdr_2.SetText("AD")
                self.col_hdr_3.SetText("BIRIM FIYAT")
                self.col_hdr_4.SetText("TOPLAM TUTAR")
                self.col_hdr_5.SetText("DURUM")
                self.col_hdr_6.SetText("ACIKLAMA")
        elif self.module_idx == 2:
            if self.sub_idx in (0, 1):
                self.col_hdr_1.SetText("CANLI HEDEF / METIN / BOSS")
                self.col_hdr_2.SetText("VNUM")
                self.col_hdr_3.SetText("MESAFE")
                self.col_hdr_4.SetText("KOORDINAT")
                self.col_hdr_5.SetText("HEDEF")
                self.col_hdr_6.SetText("KATEGORI / BILGI")
            else:
                self.col_hdr_1.SetText("FARM / BOT OZELLIGI")
                self.col_hdr_2.SetText("MOD")
                self.col_hdr_3.SetText("AKTIF DEGER")
                self.col_hdr_4.SetText("HEDEF / SINIR")
                self.col_hdr_5.SetText("DURUM")
                self.col_hdr_6.SetText("ACIKLAMA & KULLANIM")
        else:
            self.col_hdr_1.SetText("SAVAS / SISTEM ARACI")
            self.col_hdr_2.SetText("MOD")
            self.col_hdr_3.SetText("AKTIF DEGER")
            self.col_hdr_4.SetText("HEDEF / SINIR")
            self.col_hdr_5.SetText("DURUM")
            self.col_hdr_6.SetText("ACIKLAMA & KULLANIM")

    # --------------------------------------------------------------------------
    # Top Control Actions
    # --------------------------------------------------------------------------
    def on_context_action_1(self):
        if self.module_idx == 0:
            self.scanner.force_full_rescan()
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                self.scanner.queue_batch_inventory_to_my_shop(only_high_demand=(1 == 0))
            elif self.sub_idx == 1:
                self.scanner.reprice_all_my_shop_items()
            elif self.sub_idx == 2:
                self.scanner.walk_and_open_nearest_npc()
            else:
                self.on_populate_smart_sniper_click()
        elif self.module_idx == 2:
            ctrl = self.scanner.get_suite_controller()
            if ctrl:
                ctrl.cfg["farm_enabled"] = not ctrl.cfg.get("farm_enabled", (1 == 0))
                _chat_notice("Oto-Farm Botu: %s" % ("ACIK" if ctrl.cfg["farm_enabled"] else "KAPALI"))
        else:
            ctrl = self.scanner.get_suite_controller()
            if ctrl:
                ctrl.cfg["waithack_enabled"] = not ctrl.cfg.get("waithack_enabled", (1 == 0))
                _chat_notice("Waithack (7x Aura): %s" % ("ACIK" if ctrl.cfg["waithack_enabled"] else "KAPALI"))
        self.refresh_table(force=(1 == 1))

    def on_context_action_2(self):
        if self.module_idx == 0 or (self.module_idx == 1 and self.sub_idx == 0):
            self.pricing_mode = (self.pricing_mode + 1) % 3
            self.db.pricing_strategy = self.pricing_mode
            self.db._rebuild_aggregates()
            self._update_navigation_styles()
            _chat_notice("Fiyatlandirma stratejisi: %s" % (
                "REKABETCI (En Ucuzun %2 Alti)" if self.pricing_mode == 0 else (
                    "DENGELI (2. En Ucuz / Medyan)" if self.pricing_mode == 1 else "MAKS KAR (Medyan)"
                )
            ))
        elif self.module_idx == 1 and self.sub_idx == 1:
            self.scanner.request_my_shop_sync(silent=(1 == 1))
            _chat_notice("Magaza verisi yenileniyor...")
        elif self.module_idx == 1 and self.sub_idx == 2:
            self.scanner.sell_inventory_items_to_npc(only_arbitrage=(1 == 1))
        elif self.module_idx == 1:
            self.scanner.request_safebox_sync(withdraw_all=(1 == 1))
        elif self.module_idx == 2:
            ents = self.engine.enumerate_map_entities(only_targets=(1 == 1))
            metins = [e for e in ents if e["category"] in ("METIN", "BOSS")]
            if metins:
                m = metins[0]
                self.engine.move_character_to_xy(m["x"], m["y"])
                _chat_notice("En yakin hedefe gidiliyor: %s (%dm)" % (m["name"], m["dist"] // 100))
            else:
                _chat_notice("Cevrede Metin veya Boss bulunamadi.")
        else:
            ctrl = self.scanner.get_suite_controller()
            if ctrl:
                ctrl.toggle_wallhack(not ctrl.cfg.get("wallhack_enabled", (1 == 0)))
                _chat_notice("Wallhack: %s" % ("ACIK" if ctrl.cfg["wallhack_enabled"] else "KAPALI"))
        self.refresh_table(force=(1 == 1))

    def on_context_action_3(self):
        if self.module_idx == 0:
            self.reset_all_filters()
        elif self.module_idx == 1 and self.sub_idx == 0:
            self.scanner.request_my_shop_sync(silent=(1 == 0))
        elif self.module_idx == 1 and self.sub_idx == 1:
            self.scanner.request_safebox_sync(withdraw_all=(1 == 1))
        elif self.module_idx == 1 and self.sub_idx == 2:
            self.scanner.sell_inventory_items_to_npc(only_arbitrage=(1 == 0))
        elif self.module_idx == 1:
            self.scanner.request_my_shop_sync(silent=(1 == 1))
        elif self.module_idx == 2:
            ctrl = self.scanner.get_suite_controller()
            if ctrl:
                ctrl._use_item_by_vnums([70038, 70057, 76007])
                _chat_notice("Cesaret Pelerini tetiklendi.")
        else:
            self.db.export_to_disk()
        self.refresh_table(force=(1 == 1))

    def reset_all_filters(self):
        self.search_query = ""
        try:
            self.search_box["edit"].SetText("")
        except Exception:
            pass
        self.filter_mode = 0
        self.budget_filter_only = (1 == 0)
        self.filter_btn["set_text"]("Filtre: Tumu")
        self.budget_btn["set_text"]("Butce: KPL")
        self.budget_btn["set_color"](0xFF192940)
        self.budget_btn["set_text_color"](0xFFD0E4F7)
        self.page = 0
        self.refresh_table(force=(1 == 1))

    def apply_search_input(self):
        try:
            txt = self.search_box["edit"].GetText()
        except Exception:
            txt = ""
        self.search_query = _safe_ascii(txt).strip().lower()
        self.page = 0
        self.refresh_table(force=(1 == 1))

    def clear_search_input(self):
        self.reset_all_filters()

    def cycle_sort_mode(self):
        self.sort_mode = (self.sort_mode + 1) % 5
        labels = [
            "Sira: BirimFiyat+",
            "Sira: NetKar-",
            "Sira: ToplamFiyat+",
            "Sira: Mesafe+",
            "Sira: Arz/Talep-",
        ]
        self.sort_btn["set_text"](labels[self.sort_mode])
        self.page = 0
        self.refresh_table(force=(1 == 1))

    def cycle_filter_mode(self):
        self.filter_mode = (self.filter_mode + 1) % 5
        labels = [
            "Filtre: Tumu",
            "Filtre: Efsunlu",
            "Filtre: Ort35+",
            "Filtre: BK/Tas",
            "Filtre: YuksekTalep",
        ]
        self.filter_btn["set_text"](labels[self.filter_mode])
        self.page = 0
        self.refresh_table(force=(1 == 1))

    def toggle_budget_filter(self):
        self.budget_filter_only = not self.budget_filter_only
        if self.budget_filter_only:
            self.budget_btn["set_text"]("Butce: ACIK")
            self.budget_btn["set_color"](0xFF14452F)
            self.budget_btn["set_text_color"](0xFF80FFBF)
        else:
            self.budget_btn["set_text"]("Butce: KPL")
            self.budget_btn["set_color"](0xFF192940)
            self.budget_btn["set_text_color"](0xFFD0E4F7)
        self.page = 0
        self.refresh_table(force=(1 == 1))

    def toggle_auto_scan(self):
        self.scanner.auto_scan_enabled = not self.scanner.auto_scan_enabled
        if self.scanner.auto_scan_enabled:
            self.scan_toggle_btn["set_text"]("Tarama: ACIK")
            self.scan_toggle_btn["set_color"](0xFF123B2A)
            self.scan_toggle_btn["set_text_color"](0xFF66FFB2)
        else:
            self.scan_toggle_btn["set_text"]("Tarama: DURDU")
            self.scan_toggle_btn["set_color"](0xFF4A2511)
            self.scan_toggle_btn["set_text_color"](0xFFFFCC66)

    def toggle_auto_list(self):
        self.db.auto_list_bought = not self.db.auto_list_bought
        if self.db.auto_list_bought:
            self.autolist_toggle_btn["set_text"]("OtoPazar: ACIK")
            self.autolist_toggle_btn["set_color"](0xFF123B2A)
            self.autolist_toggle_btn["set_text_color"](0xFF66FFB2)
            _chat_notice("Oto-Magaza: ACIK (Al-Sat icin alinan esyalar otomatik magazaniza konur).")
        else:
            self.autolist_toggle_btn["set_text"]("OtoPazar: KPL")
            self.autolist_toggle_btn["set_color"](0xFF3A1E28)
            self.autolist_toggle_btn["set_text_color"](0xFFFF99AA)
            _chat_notice("Oto-Magaza: KAPALI (Alinan esyalar envanterde kalir).")

    def toggle_auto_flip(self):
        self.db.auto_flip_enabled = not self.db.auto_flip_enabled
        self.db.sniper_enabled = self.db.auto_flip_enabled or bool(self.db.sniper_rules)
        if self.db.auto_flip_enabled:
            self.autoflip_toggle_btn["set_text"]("OtoBot: ACIK")
            self.autoflip_toggle_btn["set_color"](0xFF123B2A)
            self.autoflip_toggle_btn["set_text_color"](0xFF66FFB2)
            _chat_notice("Tam Otomatik Al-Sat & Arbitraj Botu AKTIF! Yuksek talepli firsatlar otomatik alinip magazaniza konacak.")
            self.db._check_sniper_and_autoflip(self.db.bargains)
        else:
            self.autoflip_toggle_btn["set_text"]("OtoBot: KPL")
            self.autoflip_toggle_btn["set_color"](0xFF3A1E28)
            self.autoflip_toggle_btn["set_text_color"](0xFFFF99AA)
            _chat_notice("Tam Otomatik Al-Sat Botu durduruldu.")

    def on_add_sniper_rule_click(self):
        try:
            q = self.sniper_q_edit["edit"].GetText()
            p_str = self.sniper_p_edit["edit"].GetText().replace(".", "").replace(",", "").strip()
            d_str = self.sniper_d_edit["edit"].GetText().strip()
            max_p = int(p_str) if p_str else 0
            min_d = int(d_str) if d_str else 0
        except Exception:
            _chat_notice("Gecersiz Sniper kurali degeri!")
            return

        if self.db.add_sniper_rule(q, max_p, min_d):
            self.db.sniper_enabled = (1 == 1)
            _chat_notice("Sniper Kurali Eklendi: '%s' | Maks Birim: %s Yang" % (_safe_ascii(q), _fmt_yang(max_p)))
            self.db._check_sniper_and_autoflip(self.db.all_items)
            self.refresh_table(force=(1 == 1))

    def on_populate_smart_sniper_click(self):
        self.db.populate_default_sniper_rules()
        self._update_navigation_styles()
        self.refresh_table(force=(1 == 1))

    def on_clear_sniper_rules_click(self):
        self.db.sniper_rules = []
        self.db.revision += 1
        _chat_notice("Tum Sniper kurallari temizlendi.")
        self.refresh_table(force=(1 == 1))

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.refresh_table(force=(1 == 1))

    def next_page(self):
        if self.page + 1 < self.total_pages:
            self.page += 1
            self.refresh_table(force=(1 == 1))

    # --------------------------------------------------------------------------
    # Row Button Dispatchers
    # --------------------------------------------------------------------------
    def _get_row_data_at(self, row_offset):
        idx = self.page * self.ROWS_PER_PAGE + row_offset
        if 0 <= idx < len(self.filtered_rows):
            return self.filtered_rows[idx]
        return None

    def on_row_primary_action(self, row_offset):
        data = self._get_row_data_at(row_offset)
        if data is None:
            return
        if isinstance(data, dict) and "_empty_action" in data:
            act = data["_empty_action"]
            if act == "RESET_FILTERS":
                self.reset_all_filters()
            elif act == "SWITCH_BARGAINS":
                self.reset_all_filters()
                self.switch_subtab(1)
            elif act == "SYNC_MY_SHOP":
                self.scanner.request_my_shop_sync(silent=(1 == 1))
            elif act == "POPULATE_SNIPER":
                self.on_populate_smart_sniper_click()
            elif act == "WITHDRAW_SAFEBOX":
                self.scanner.request_safebox_sync(withdraw_all=(1 == 1))
            elif act == "RESCAN":
                self.scanner.force_full_rescan()
            self.refresh_table(force=(1 == 1))
            return

        if self.module_idx == 0:
            if self.sub_idx in (0, 1, 2):
                # Buy item (+ auto-list if sub_idx == 1 or auto_list_bought is ON)
                auto_l = (1 == 1) if (self.sub_idx == 1 and self.db.auto_list_bought) else None
                self.scanner.request_buy_item(data, from_sniper=(1 == 0), auto_list=auto_l)
            elif self.sub_idx == 3:
                self.scanner.open_shop_for_user(data.get("owner_id", 0))
            elif self.sub_idx == 4:
                q = data.get("name", "")
                if q:
                    self.search_query = q.lower()
                    self.search_box["edit"].SetText(q)
                    self.switch_subtab(0)
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                self.scanner.queue_add_inventory_slot_to_my_shop(data["slot"], data.get("smart_total", 0))
            elif self.sub_idx == 1:
                if not self.scanner.queue_reprice_my_shop_item(data):
                    _chat_notice("Bu esyanin fiyati zaten guncel.")
            elif self.sub_idx == 2:
                if data.get("category") == "PAZARDA_DEGERLI":
                    self.scanner.queue_add_inventory_slot_to_my_shop(data["slot"], int(data.get("market_med_unit", 0) * data.get("count", 1)))
                else:
                    self.scanner.sell_single_inventory_slot(data["slot"])
            elif self.sub_idx == 3:
                data["enabled"] = not data.get("enabled", (1 == 1))
            elif self.sub_idx == 4:
                self.scanner.request_safebox_sync(withdraw_all=(1 == 1))
        elif self.module_idx == 2:
            if self.sub_idx == 0:
                vid = int(data.get("vid", 0))
                if vid > 0:
                    self.engine.move_character_to_xy(data["x"], data["y"])
                    ctrl = self.scanner.get_suite_controller()
                    if ctrl:
                        ctrl._attack_target(vid)
                    _chat_notice("Hedefe saldiriliyor: %s (VID:%d)" % (data["name"], vid))
            elif self.sub_idx == 1:
                vnum = int(data.get("vnum", 0))
                if vnum in self.scanner.farm_selected_vnums:
                    self.scanner.farm_selected_vnums.discard(vnum)
                    _chat_notice("Farm hedef listesinden cikarildi: %s" % data["name"])
                else:
                    self.scanner.farm_selected_vnums.add(vnum)
                    _chat_notice("Farm hedef listesine eklendi: %s" % data["name"])
            else:
                fn = data.get("action_1")
                if callable(fn):
                    fn()
        else:
            fn = data.get("action_1")
            if callable(fn):
                fn()
        self.refresh_table(force=(1 == 1))

    def on_row_secondary_action(self, row_offset):
        data = self._get_row_data_at(row_offset)
        if data is None or "_empty_action" in data:
            return
        if self.module_idx == 0:
            oid = int(data.get("owner_id", 0))
            if oid > 0:
                self.scanner.open_shop_for_user(oid)
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                # Put at minimum market price for instant sale
                min_tot = int(data.get("min_unit", 0) * data.get("count", 1))
                if min_tot > 0:
                    self.scanner.queue_add_inventory_slot_to_my_shop(data["slot"], min_tot)
            elif self.sub_idx == 1:
                self.scanner.queue_remove_my_shop_item(data.get("id", 0), data.get("name", "?"))
            elif self.sub_idx == 2:
                self.scanner.sell_single_inventory_slot(data["slot"])
            elif self.sub_idx == 3:
                try:
                    self.db.sniper_rules.remove(data)
                except Exception:
                    pass
            elif self.sub_idx == 4:
                self.scanner.request_my_shop_sync(silent=(1 == 0))
        elif self.module_idx == 2:
            if self.sub_idx in (0, 1):
                self.engine.teleport_character_to_xy(data["x"], data["y"])
                _chat_notice("Hedefe isinlandi: %s (%d, %d)" % (data["name"], data["x"] // 100, data["y"] // 100))
            else:
                fn = data.get("action_2")
                if callable(fn):
                    fn()
        else:
            fn = data.get("action_2")
            if callable(fn):
                fn()
        self.refresh_table(force=(1 == 1))

    def on_row_tertiary_action(self, row_offset):
        data = self._get_row_data_at(row_offset)
        if data is None or "_empty_action" in data:
            return
        if self.module_idx == 0:
            tx = int(data.get("x", 0))
            ty = int(data.get("y", 0))
            if tx > 0 and ty > 0:
                self.engine.move_character_to_xy(tx, ty)
                _chat_notice("Pazara yurunuyor: %s (%d, %d)" % (data.get("seller", data.get("owner", "?")), tx // 100, ty // 100))
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                self.search_query = data.get("name", "").lower()
                self.search_box["edit"].SetText(data.get("name", ""))
                self.switch_module(0)
            elif self.sub_idx == 1:
                self.scanner.request_my_shop_sync(silent=(1 == 0))
            elif self.sub_idx == 2:
                self.scanner.walk_and_open_nearest_npc()
        elif self.module_idx == 2:
            if self.sub_idx in (0, 1):
                self.engine.move_character_to_xy(data["x"], data["y"])
                _chat_notice("Hedefe yurunuyor: %s" % data["name"])
            else:
                fn = data.get("action_3")
                if callable(fn):
                    fn()
        else:
            fn = data.get("action_3")
            if callable(fn):
                fn()
        self.refresh_table(force=(1 == 1))

    # --------------------------------------------------------------------------
    # Data Providers for All 4 Modules x 5 Sub-Tabs
    # --------------------------------------------------------------------------
    def _build_config_rows_for_farm(self):
        ctrl = self.scanner.get_suite_controller()
        cfg = ctrl.cfg if ctrl else {}
        st = ctrl.stats if ctrl else {}

        def _toggle(key, label):
            if ctrl:
                ctrl.cfg[key] = not ctrl.cfg.get(key, (1 == 0))
                _chat_notice("%s: %s" % (label, "ACIK" if ctrl.cfg[key] else "KAPALI"))

        def _adj(key, delta, mn, mx, label):
            if ctrl:
                val = int(ctrl.cfg.get(key, mn)) + delta
                ctrl.cfg[key] = max(mn, min(mx, val))
                _chat_notice("%s: %s" % (label, ctrl.cfg[key]))

        if self.sub_idx == 2:
            mode_names = {0: "SADECE METIN", 1: "METIN + BOSS", 2: "TUM SLOTLAR", 3: "MADEN DAMARI"}
            cur_mode = int(cfg.get("farm_target_mode", 1))
            return [
                {
                    "title": "Otomatik Metin & Boss Farm Botu",
                    "mod": "BOT",
                    "val": "ACIK" if cfg.get("farm_enabled") else "KAPALI",
                    "limit": "Hedef: %d Kesim" % int(st.get("metins_destroyed", 0)),
                    "status": "AKTIF" if cfg.get("farm_enabled") else "BEKLEMEDE",
                    "desc": "Haritadaki Metin ve Bosslara otomatik kosar ve keser",
                    "b1": "KAPAT" if cfg.get("farm_enabled") else "BASLAT",
                    "b2": "MOD", "b3": "SIFIRLA",
                    "action_1": lambda: _toggle("farm_enabled", "Oto-Farm Botu"),
                    "action_2": lambda: _adj("farm_target_mode", 1 if cur_mode < 3 else -3, 0, 3, "Farm Hedef Modu"),
                    "action_3": lambda: ctrl.visited_blacklist.clear() if ctrl else None,
                },
                {
                    "title": "Farm Hedef Oncelik Modu",
                    "mod": "HEDEF",
                    "val": mode_names.get(cur_mode, "METIN+BOSS"),
                    "limit": "Ozel Secim: %d Vnum" % len(self.scanner.farm_selected_vnums),
                    "status": "ONCELIKLI",
                    "desc": "Metin / Metin+Boss / Tum Slotlar / Maden secimi",
                    "b1": "DEGISTIR", "b2": "METIN", "b3": "TUMU",
                    "action_1": lambda: _adj("farm_target_mode", 1 if cur_mode < 3 else -3, 0, 3, "Farm Modu"),
                    "action_2": lambda: cfg.update({"farm_target_mode": 0}),
                    "action_3": lambda: cfg.update({"farm_target_mode": 2}),
                },
                {
                    "title": "Farm Tarama Menzili (Mesafe)",
                    "mod": "MENZIL",
                    "val": "%d m" % (int(cfg.get("farm_scan_range", 8000)) // 100),
                    "limit": "Maks: 150 m",
                    "status": "NORMAL",
                    "desc": "Karakterin ne kadar uzaktaki Metin/Bosslara kosacagi",
                    "b1": "+15m", "b2": "-15m", "b3": "80m",
                    "action_1": lambda: _adj("farm_scan_range", 1500, 1500, 15000, "Tarama Menzili"),
                    "action_2": lambda: _adj("farm_scan_range", -1500, 1500, 15000, "Tarama Menzili"),
                    "action_3": lambda: cfg.update({"farm_scan_range": 8000}),
                },
                {
                    "title": "Anti-KS (Baskasinin Metnine Dalmama)",
                    "mod": "KORUMA",
                    "val": "ACIK" if cfg.get("farm_anti_ks", (1 == 1)) else "KAPALI",
                    "limit": "Yakin Oyuncu: 3.5m",
                    "status": "GUVENLI" if cfg.get("farm_anti_ks", (1 == 1)) else "AGRESIF",
                    "desc": "Metnin dibinde baska oyuncu varsa o metni pas gecer",
                    "b1": "AC / KPL", "b2": "-", "b3": "-",
                    "action_1": lambda: _toggle("farm_anti_ks", "Anti-KS Korumasi"),
                },
                {
                    "title": "Otomatik Dirilme (Olunce Kalkma)",
                    "mod": "DIRILME",
                    "val": "ACIK" if cfg.get("auto_revive", (1 == 1)) else "KAPALI",
                    "limit": "Bekleme: 2.5 sn",
                    "status": "AKTIF" if cfg.get("auto_revive", (1 == 1)) else "KAPALI",
                    "desc": "Karakter oldugunde 'Burada Basla' ile otomatik kalkar",
                    "b1": "AC / KPL", "b2": "-", "b3": "-",
                    "action_1": lambda: _toggle("auto_revive", "Otomatik Dirilme"),
                },
                {
                    "title": "Takilma Kurtarma (Unstuck Sistemi)",
                    "mod": "UNSTUCK",
                    "val": "%d sn" % int(cfg.get("farm_stuck_timeout", 7)),
                    "limit": "Wallhack Destekli",
                    "status": "AKTIF",
                    "desc": "Hedefe giderken engele takilirsa hedefi degistirir",
                    "b1": "+2 sn", "b2": "-2 sn", "b3": "7 sn",
                    "action_1": lambda: _adj("farm_stuck_timeout", 2, 3, 20, "Takilma Suresi"),
                    "action_2": lambda: _adj("farm_stuck_timeout", -2, 3, 20, "Takilma Suresi"),
                    "action_3": lambda: cfg.update({"farm_stuck_timeout": 7.0}),
                },
            ]
        elif self.sub_idx == 3:
            return [
                {
                    "title": "Otomatik Kirmizi Pot (HP Yenileme)",
                    "mod": "HP POT",
                    "val": "ACIK" if cfg.get("auto_hp_pot", (1 == 1)) else "KAPALI",
                    "limit": "Esik: %%%d HP" % int(cfg.get("hp_threshold", 75)),
                    "status": "Basilan: %d" % int(st.get("pots_used", 0)),
                    "desc": "HP belirlenen yuzdenin altina indiginde aninda Kirmizi Pot basar",
                    "b1": "AC / KPL", "b2": "+%5", "b3": "-%5",
                    "action_1": lambda: _toggle("auto_hp_pot", "Oto Kirmizi Pot"),
                    "action_2": lambda: _adj("hp_threshold", 5, 20, 95, "HP Pot Esigi"),
                    "action_3": lambda: _adj("hp_threshold", -5, 20, 95, "HP Pot Esigi"),
                },
                {
                    "title": "Otomatik Mavi Pot (SP Yenileme)",
                    "mod": "SP POT",
                    "val": "ACIK" if cfg.get("auto_sp_pot", (1 == 1)) else "KAPALI",
                    "limit": "Esik: %%%d SP" % int(cfg.get("sp_threshold", 45)),
                    "status": "AKTIF" if cfg.get("auto_sp_pot", (1 == 1)) else "KAPALI",
                    "desc": "SP belirlenen yuzdenin altina indiginde Mavi Pot basar",
                    "b1": "AC / KPL", "b2": "+%10", "b3": "-%10",
                    "action_1": lambda: _toggle("auto_sp_pot", "Oto Mavi Pot"),
                    "action_2": lambda: _adj("sp_threshold", 10, 10, 90, "SP Pot Esigi"),
                    "action_3": lambda: _adj("sp_threshold", -10, 10, 90, "SP Pot Esigi"),
                },
                {
                    "title": "Otomatik Buff & Skiller (Hava / Ofke / Beden)",
                    "mod": "SKILL",
                    "val": "ACIK" if cfg.get("auto_buff_skills") else "KAPALI",
                    "limit": "Slot: 1, 2, 3, 4",
                    "status": "AKTIF" if cfg.get("auto_buff_skills") else "KAPALI",
                    "desc": "Suresi biten buff skillerini otomatik yakar",
                    "b1": "AC / KPL", "b2": "-", "b3": "-",
                    "action_1": lambda: _toggle("auto_buff_skills", "Otomatik Buff Skilleri"),
                },
                {
                    "title": "Otomatik Cesaret Pelerini (Mob Cekme)",
                    "mod": "PELERIN",
                    "val": "ACIK" if cfg.get("auto_cape") else "KAPALI",
                    "limit": "Aralik: %.1f sn" % float(cfg.get("cape_interval", 4.5)),
                    "status": "Cekilen: %d" % int(st.get("capes_pulled", 0)),
                    "desc": "Envanterdeki Cesaret Pelerinini periyodik olarak basar",
                    "b1": "AC / KPL", "b2": "+1 sn", "b3": "SIMDI BAS",
                    "action_1": lambda: _toggle("auto_cape", "Oto Cesaret Pelerini"),
                    "action_2": lambda: _adj("cape_interval", 1, 2, 15, "Pelerin Suresi"),
                    "action_3": lambda: ctrl._use_item_by_vnums([70038, 70057, 76007]) if ctrl else None,
                },
            ]
        else:
            return [
                {
                    "title": "Otomatik Yerdeki Esyalari Toplama (Auto-Loot)",
                    "mod": "LOOT",
                    "val": "ACIK" if cfg.get("auto_pickup", (1 == 1)) else "KAPALI",
                    "limit": "Hiz: 0.20 sn",
                    "status": "Toplanan: %d" % int(st.get("loots_picked", 0)),
                    "desc": "Dusen Yang ve esyalari C-API uzerinden aninda toplar",
                    "b1": "AC / KPL", "b2": "SIMDI TOPLA", "b3": "-",
                    "action_1": lambda: _toggle("auto_pickup", "Otomatik Toplama"),
                    "action_2": lambda: player.PickCloseItem() if (player and hasattr(player, "PickCloseItem")) else None,
                },
                {
                    "title": "GM & Oyuncu Guvenlik Dedektoru",
                    "mod": "GUVENLIK",
                    "val": "ACIK" if cfg.get("gm_detector", (1 == 1)) else "KAPALI",
                    "limit": "[GM] / [GA] / [TL]",
                    "status": "UYARI: %d" % int(st.get("gm_alerts", 0)),
                    "desc": "Haritada yetkili goruldugunde hiz/waithack ozelliklerini duraklatir",
                    "b1": "AC / KPL", "b2": "-", "b3": "-",
                    "action_1": lambda: _toggle("gm_detector", "GM Dedektoru"),
                },
                {
                    "title": "SvSide / Captcha Anti-Ban Korumasi",
                    "mod": "SVSIDE",
                    "val": "AKTIF",
                    "limit": "Paket Limiti Koruma",
                    "status": "GUVENLI",
                    "desc": "Sunucu tarafi paket asimi ve Captcha pencerelerini izler",
                    "b1": "KONTROL ET", "b2": "-", "b3": "-",
                    "action_1": lambda: _chat_notice("SvSide koruma kalkanlari aktif ve calisiyor."),
                },
            ]

    def _build_config_rows_for_combat(self):
        ctrl = self.scanner.get_suite_controller()
        cfg = ctrl.cfg if ctrl else {}
        st = ctrl.stats if ctrl else {}

        def _toggle(key, label):
            if ctrl:
                ctrl.cfg[key] = not ctrl.cfg.get(key, (1 == 0))
                _chat_notice("%s: %s" % (label, "ACIK" if ctrl.cfg[key] else "KAPALI"))

        def _adj(key, delta, mn, mx, label):
            if ctrl:
                val = int(ctrl.cfg.get(key, mn)) + delta
                ctrl.cfg[key] = max(mn, min(mx, val))
                _chat_notice("%s: %s" % (label, ctrl.cfg[key]))

        if self.sub_idx == 0:
            return [
                {
                    "title": "Waithack (7x Aura Uzaktan Otomatik Vurus)",
                    "mod": "WAITHACK",
                    "val": "ACIK" if cfg.get("waithack_enabled") else "KAPALI",
                    "limit": "Menzil: %dm" % (int(cfg.get("waithack_range", 750)) // 100),
                    "status": "Vurus: %d" % int(st.get("waithack_hits", 0)),
                    "desc": "Cevredeki tum hedeflere animasyonsuz paket vurusu gonderir",
                    "b1": "AC / KPL", "b2": "+Menzil", "b3": "-Menzil",
                    "action_1": lambda: _toggle("waithack_enabled", "Waithack (7x)"),
                    "action_2": lambda: _adj("waithack_range", 150, 250, 2500, "Waithack Menzili"),
                    "action_3": lambda: _adj("waithack_range", -150, 250, 2500, "Waithack Menzili"),
                },
                {
                    "title": "Waithack Maksimum Eszamanli Hedef Sayisi",
                    "mod": "HEDEF",
                    "val": "%d Hedef" % int(cfg.get("waithack_max_targets", 8)),
                    "limit": "Tek Tick Basina",
                    "status": "NORMAL",
                    "desc": "Her dalgada kac farkli yaratiga ayni anda vurulacagi",
                    "b1": "+2 Hedef", "b2": "-2 Hedef", "b3": "8 Hedef",
                    "action_1": lambda: _adj("waithack_max_targets", 2, 1, 24, "Maks Hedef"),
                    "action_2": lambda: _adj("waithack_max_targets", -2, 1, 24, "Maks Hedef"),
                    "action_3": lambda: cfg.update({"waithack_max_targets": 8}),
                },
                {
                    "title": "Saldiri Hizi & Hareket Hizi Boost",
                    "mod": "SPEED",
                    "val": "ACIK" if cfg.get("speed_boost_enabled") else "KAPALI",
                    "limit": "Saldiri:%d | Kosu:%d" % (int(cfg.get("atk_speed_val", 175)), int(cfg.get("mov_speed_val", 185))),
                    "status": "AKTIF" if cfg.get("speed_boost_enabled") else "KAPALI",
                    "desc": "C++ CInstanceBase uzerinden saldiri ve kosu hizini arttirir",
                    "b1": "AC / KPL", "b2": "HIZ +10", "b3": "HIZ -10",
                    "action_1": lambda: _toggle("speed_boost_enabled", "Speed Boost"),
                    "action_2": lambda: (_adj("atk_speed_val", 10, 100, 300, "Saldiri Hizi"), _adj("mov_speed_val", 10, 100, 300, "Kosu Hizi")),
                    "action_3": lambda: (_adj("atk_speed_val", -10, 100, 300, "Saldiri Hizi"), _adj("mov_speed_val", -10, 100, 300, "Kosu Hizi")),
                },
            ]
        elif self.sub_idx == 1:
            return [
                {
                    "title": "Kombo Kilidi (Combo Hack)",
                    "mod": "COMBO",
                    "val": "ACIK" if cfg.get("combo_hack_enabled") else "KAPALI",
                    "limit": "Mod: %d" % int(cfg.get("combo_mode", 2)),
                    "status": "AKTIF" if cfg.get("combo_hack_enabled") else "KAPALI",
                    "desc": "Kesintisiz kombo zinciri uygular",
                    "b1": "AC / KPL", "b2": "MOD+", "b3": "-",
                    "action_1": lambda: _toggle("combo_hack_enabled", "Kombo Hilesi"),
                    "action_2": lambda: _adj("combo_mode", 1, 1, 4, "Kombo Modu"),
                },
                {
                    "title": "Yere Dusmeme / Sekmeme (No-Knockback)",
                    "mod": "SEKMEME",
                    "val": "ACIK" if cfg.get("no_knockback_enabled") else "KAPALI",
                    "limit": "Boss & Metin",
                    "status": "KORUMALI" if cfg.get("no_knockback_enabled") else "NORMAL",
                    "desc": "Boss ve slot vuruslarinda karakterin savrulmasini engeller",
                    "b1": "AC / KPL", "b2": "-", "b3": "-",
                    "action_1": lambda: _toggle("no_knockback_enabled", "Sekmeme (No-Knockback)"),
                },
            ]
        elif self.sub_idx == 2:
            return [
                {
                    "title": "Otomatik Efsun Botu (Slot #1)",
                    "mod": "EFSUN",
                    "val": "ACIK" if cfg.get("switchbot_enabled") else "KAPALI",
                    "limit": "Hedef Ort >= %d%%" % int(cfg.get("switchbot_min_avg_dmg", 40)),
                    "status": "Basilan: %d" % int(st.get("switch_count", 0)),
                    "desc": "Envanter 1. slottaki silaha hedef Ortalama Zarar gelene kadar efsun atar",
                    "b1": "AC / KPL", "b2": "ORT +5", "b3": "ORT -5",
                    "action_1": lambda: _toggle("switchbot_enabled", "Oto Efsun Botu"),
                    "action_2": lambda: _adj("switchbot_min_avg_dmg", 5, 25, 55, "Hedef Ortalama Zarar"),
                    "action_3": lambda: _adj("switchbot_min_avg_dmg", -5, 25, 55, "Hedef Ortalama Zarar"),
                },
                {
                    "title": "Uzaktan Demirci & Kutsama Kagidi +Basma (Slot #1)",
                    "mod": "+BASMA",
                    "val": "ENVANTER SLOT #1",
                    "limit": "Demirci / Kutsama",
                    "status": "HAZIR",
                    "desc": "Envanterin 1. slotundaki esyaya uzaktan + basar",
                    "b1": "NORMAL +BAS", "b2": "KUTSAMA +BAS", "b3": "-",
                    "action_1": lambda: ctrl.upgrade_slot_item(0, 0) if ctrl else None,
                    "action_2": lambda: ctrl.upgrade_slot_item(0, 1) if ctrl else None,
                },
                {
                    "title": "Otomatik Biyolog Gorevi Teslimi",
                    "mod": "BIYOLOG",
                    "val": "ACIK" if cfg.get("auto_biolog_enabled") else "KAPALI",
                    "limit": "Envanter Tarama",
                    "status": "AKTIF" if cfg.get("auto_biolog_enabled") else "KAPALI",
                    "desc": "Envanterdeki Biyolog esyalarini suresi doldukca teslim eder",
                    "b1": "AC / KPL", "b2": "SIMDI VER", "b3": "-",
                    "action_1": lambda: _toggle("auto_biolog_enabled", "Oto Biyolog"),
                    "action_2": lambda: ctrl._run_auto_biolog(time.time()) if ctrl else None,
                },
            ]
        elif self.sub_idx == 3:
            return [
                {
                    "title": "Wallhack (Dag / Bina / Obje Icindan Gecme)",
                    "mod": "WALLHACK",
                    "val": "ACIK" if cfg.get("wallhack_enabled") else "KAPALI",
                    "limit": "4x Native Patch",
                    "status": "AKTIF" if cfg.get("wallhack_enabled") else "NORMAL",
                    "desc": "C++ fizik ve engel carpismalarini devre disi birakir",
                    "b1": "AC / KPL", "b2": "-", "b3": "-",
                    "action_1": lambda: ctrl.toggle_wallhack(not cfg.get("wallhack_enabled")) if ctrl else None,
                },
                {
                    "title": "Zoom Hack & Sis Kaldirma (Sinirsiz Kamera)",
                    "mod": "KAMERA",
                    "val": "ACIK" if cfg.get("zoom_hack_enabled", (1 == 1)) else "KAPALI",
                    "limit": "Max Mesafe: 25.000",
                    "status": "AKTIF",
                    "desc": "Kamera uzaklastirma limitini kaldirir ve sisi temizler",
                    "b1": "UYGULA", "b2": "GECE", "b3": "GUNDUZ",
                    "action_1": lambda: ctrl._apply_visual_patches() if ctrl else None,
                    "action_2": lambda: background.SetEnvironmentData(1) if (background and hasattr(background, "SetEnvironmentData")) else None,
                    "action_3": lambda: background.SetEnvironmentData(0) if (background and hasattr(background, "SetEnvironmentData")) else None,
                },
            ]
        else:
            return [
                {
                    "title": "Tam Piyasa Raporunu Disa Aktar (logs/offlineshop_market_dump.txt)",
                    "mod": "RAPOR",
                    "val": "%d Esya" % len(self.db.all_items),
                    "limit": "%d Firsat" % len(self.db.bargains),
                    "status": "HAZIR",
                    "desc": "Tum taranan pazarlari ve firsat analizini dosyaya yazar",
                    "b1": "KAYDET", "b2": "-", "b3": "-",
                    "action_1": lambda: self.db.export_to_disk(),
                },
                {
                    "title": "Tum Harita Pazarlarini Bastan Tara",
                    "mod": "TARAMA",
                    "val": "%d / %d Pazar" % (len(self.db.scanned_shops), len(self.db.map_shops)),
                    "limit": "Kuyruk: %d" % len(self.scanner.scan_queue),
                    "status": "AKTIF" if self.scanner.auto_scan_enabled else "DURDU",
                    "desc": "Haritadaki tum pazarlari yeniden tarama kuyruguna ekler",
                    "b1": "YENIDEN TARA", "b2": "AC / KPL", "b3": "-",
                    "action_1": lambda: self.scanner.force_full_rescan(),
                    "action_2": lambda: self.toggle_auto_scan(),
                },
                {
                    "title": "Kendi Offline Magazami & Kasami Senkronize Et",
                    "mod": "MAGAZAM",
                    "val": "%d Esya Satista" % len(self.db.my_shop_items),
                    "limit": "Kasa: %s Yang" % _fmt_yang_short(self.db.my_safebox_yang),
                    "status": "ACIK" if self.db.my_shop_open else "KAPALI",
                    "desc": "Sunucudan kendi magazanizin ve pazar kasanizin bilgisini ceker",
                    "b1": "MAGAZA SYNC", "b2": "KASAYI CEK", "b3": "-",
                    "action_1": lambda: self.scanner.request_my_shop_sync(silent=(1 == 1)),
                    "action_2": lambda: self.scanner.request_safebox_sync(withdraw_all=(1 == 1)),
                },
            ]

    def _compute_filtered_rows(self):
        my_yang = self.engine.get_player_yang()
        q = self.search_query

        # MODULE 0: PAZAR & FIRSATLAR
        if self.module_idx == 0:
            if self.sub_idx in (0, 1, 2):
                if self.sub_idx == 1:
                    src = self.db.bargains
                elif self.sub_idx == 2:
                    src = self.db.npc_bargains
                else:
                    src = self.db.all_items

                out = []
                for it in src:
                    if q:
                        if q.isdigit():
                            if int(q) != it["vnum"] and q not in it["name_lower"]:
                                continue
                        elif q not in it["name_lower"] and q not in it["seller"].lower() and q not in it["bonus_summary"].lower():
                            continue
                    if self.budget_filter_only and my_yang > 0 and it["price"] > my_yang:
                        continue
                    if self.filter_mode == 1 and not it["has_bonus"]:
                        continue
                    elif self.filter_mode == 2 and it["avg_dmg"] < 35:
                        continue
                    elif self.filter_mode == 3:
                        nm = it["name_lower"]
                        if not any(k in nm for k in ("beceri", "bk:", "tas", "ruh", "efsun", "kutsama", "zen", "inci", "sandik", "kuresi", "postu", "pencesi")):
                            continue
                    elif self.filter_mode == 4 and it.get("demand_tier", 0) < 2:
                        continue
                    out.append(it)

                if self.sort_mode == 0:
                    out.sort(key=lambda x: (x["unit_price"], x["price"]))
                elif self.sort_mode == 1:
                    if self.sub_idx == 2:
                        out.sort(key=lambda x: (-x.get("npc_profit", 0), x["price"]))
                    else:
                        out.sort(key=lambda x: (-x.get("flip_profit", 0), -x.get("discount_pct", 0), x["price"]))
                elif self.sort_mode == 2:
                    out.sort(key=lambda x: (x["price"], x["unit_price"]))
                elif self.sort_mode == 3:
                    out.sort(key=lambda x: (x["dist"], x["unit_price"]))
                elif self.sort_mode == 4:
                    out.sort(key=lambda x: (-x.get("demand_tier", 0), -x.get("flip_profit", 0), x["unit_price"]))

                if not out:
                    if self.budget_filter_only or self.filter_mode != 0 or q:
                        out = [{
                            "_empty_action": "RESET_FILTERS",
                            "msg": "Aktif filtre/butce (%s Yang) nedeniyle esya gizlendi (Toplam: %d esya, %d firsat)." % (
                                _fmt_yang_short(my_yang), len(self.db.all_items), len(self.db.bargains)
                            ),
                            "btn": "FILTRE SIFIRLA",
                        }]
                    elif self.sub_idx == 2:
                        out = [{
                            "_empty_action": "SWITCH_BARGAINS",
                            "msg": "Su an NPC satisi pazar fiyatindan yuksek esya yok. Al-Sat sekmesinde %d karli firsat var!" % len(self.db.bargains),
                            "btn": "AL-SAT (%d)" % len(self.db.bargains),
                        }]
                    else:
                        out = [{
                            "_empty_action": "RESCAN",
                            "msg": "Pazarlar taraniyor (%d/%d pazar tarandi). Lutfen bekleyin veya TARA'ya basin." % (
                                len(self.db.scanned_shops), len(self.db.map_shops)
                            ),
                            "btn": "SIMDI TARA",
                        }]
                return out

            elif self.sub_idx == 3:
                px, py, _ = self.engine.get_player_xy()
                out = []
                for oid, mshop in self.db.map_shops.items():
                    sc = self.db.scanned_shops.get(oid)
                    owner = sc["owner"] if sc else mshop["owner"]
                    title = sc["title"] if sc else mshop["title"]
                    cnt = sc["count"] if sc else mshop["item_count"]
                    dist = int(math.hypot(mshop["x"] - px, mshop["y"] - py)) if (px or py) else mshop["dist"]
                    if q and q not in owner.lower() and q not in title.lower():
                        continue
                    out.append({
                        "owner_id": oid,
                        "owner": owner,
                        "title": title,
                        "count": cnt,
                        "x": mshop["x"],
                        "y": mshop["y"],
                        "dist": dist,
                        "scanned": sc is not None,
                    })
                out.sort(key=lambda x: x["dist"])
                return out

            else:
                out = list(self.db.sales_feed)
                for ev in self.db.auto_events_log[:30]:
                    out.append({
                        "ts": ev["ts"],
                        "name": ev["msg"],
                        "count": 1,
                        "unit_price": 0,
                        "price": 0,
                        "seller": "OTO-BOT",
                    })
                if not out:
                    out = [{
                        "_empty_action": "RESCAN",
                        "msg": "Henuz canli satis veya otomasyon islemi kaydedilmedi. Tarama devam ediyor...",
                        "btn": "PAZARLARI TARA",
                    }]
                return out

        # MODULE 1: OTO-MAGAZA & TICARET
        elif self.module_idx == 1:
            if self.sub_idx == 0:
                out = self.scanner.get_inventory_market_items()
                if q:
                    out = [r for r in out if q in r["name"].lower() or q in r["bonus_summary"].lower()]
                if not out:
                    out = [{
                        "_empty_action": "RESET_FILTERS",
                        "msg": "Envanterinizde pazara konulabilecek esya bulunamadi.",
                        "btn": "YENILE",
                    }]
                return out

            elif self.sub_idx == 1:
                out = list(self.db.my_shop_items)
                if q:
                    out = [r for r in out if q in r["name"].lower()]
                if not out:
                    out = [{
                        "_empty_action": "SYNC_MY_SHOP",
                        "msg": "Kendi magazanizda esya gorunmuyor veya henuz senkronize edilmedi.",
                        "btn": "MAGAZAMI YENILE",
                    }]
                return out

            elif self.sub_idx == 2:
                out = self.scanner.get_inventory_npc_items()
                if q:
                    out = [r for r in out if q in r["name"].lower()]
                if not out:
                    out = [{
                        "_empty_action": "RESET_FILTERS",
                        "msg": "Envanterde NPC'ye satilabilecek esya bulunamadi.",
                        "btn": "YENILE",
                    }]
                return out

            elif self.sub_idx == 3:
                out = list(self.db.sniper_rules)
                if not out:
                    out = [{
                        "_empty_action": "POPULATE_SNIPER",
                        "msg": "Henuz Sniper kurali yok. Tek tikla piyasadaki en cok satan esyalari ekleyebilirsiniz!",
                        "btn": "AKILLI KURALLAR",
                    }]
                return out

            else:
                out = []
                if self.db.my_safebox_yang > 0:
                    out.append({
                        "is_safebox_yang": (1 == 1),
                        "name": "PAZAR KASASI NAKIT BAKIYE",
                        "count": 1,
                        "unit_price": self.db.my_safebox_yang,
                        "price": self.db.my_safebox_yang,
                        "status": "CEKILEBILIR",
                        "desc": "Magazanizda satilan esyalardan biriken Yang",
                    })
                for sb_it in self.db.my_safebox_items:
                    vnum = int(sb_it.get("vnum", 0))
                    out.append({
                        "is_safebox_item": (1 == 1),
                        "id": int(sb_it.get("id", 0)),
                        "name": self.engine.get_item_name(vnum),
                        "count": int(sb_it.get("count", 1)),
                        "unit_price": 0,
                        "price": 0,
                        "status": "KASADA BEKLIYOR",
                        "desc": "Kasadan envantere cekilebilir esya",
                    })
                for s_it in self.db.my_shop_sold:
                    vnum = int(s_it.get("vnum", 0))
                    cnt = max(1, int(s_it.get("count", 1)))
                    pr = int(s_it.get("price", 0))
                    out.append({
                        "is_sold_history": (1 == 1),
                        "name": self.engine.get_item_name(vnum),
                        "count": cnt,
                        "unit_price": int(pr // cnt),
                        "price": pr,
                        "status": "SATILDI",
                        "desc": "Kendi magazanizda satilan esya gecmisi",
                    })
                if not out:
                    out = [{
                        "_empty_action": "WITHDRAW_SAFEBOX",
                        "msg": "Pazar kasasi verisi sorgulaniyor veya kasanizda bekleyen Yang yok.",
                        "btn": "KASAYI SORGULA",
                    }]
                return out

        # MODULE 2: FARM & METIN BOTU
        elif self.module_idx == 2:
            if self.sub_idx == 0:
                ents = self.engine.enumerate_map_entities(only_targets=(1 == 1))
                if q:
                    ents = [e for e in ents if q in e["name"].lower() or q == str(e["vnum"])]
                if not ents:
                    ents = [{
                        "_empty_action": "RESET_FILTERS",
                        "msg": "Cevrede canli Metin, Boss veya Yaratik bulunamadi.",
                        "btn": "YENILE",
                    }]
                return ents

            elif self.sub_idx == 1:
                ents = self.engine.enumerate_map_entities(only_targets=(1 == 1))
                by_vnum = {}
                for e in ents:
                    vn = e["vnum"]
                    if vn not in by_vnum:
                        by_vnum[vn] = {
                            "vnum": vn,
                            "name": e["name"],
                            "category": e["category"],
                            "count": 0,
                            "dist": e["dist"],
                            "x": e["x"],
                            "y": e["y"],
                        }
                    by_vnum[vn]["count"] += 1
                    if e["dist"] < by_vnum[vn]["dist"]:
                        by_vnum[vn]["dist"] = e["dist"]
                        by_vnum[vn]["x"] = e["x"]
                        by_vnum[vn]["y"] = e["y"]
                out = sorted(by_vnum.values(), key=lambda x: (x["category"] != "METIN", x["dist"]))
                if not out:
                    out = [{
                        "_empty_action": "RESET_FILTERS",
                        "msg": "Haritada gruplanacak hedef bulunamadi.",
                        "btn": "YENILE",
                    }]
                return out

            else:
                return self._build_config_rows_for_farm()

        # MODULE 3: SAVAS, EFSUN & ARACLAR
        else:
            return self._build_config_rows_for_combat()

    # --------------------------------------------------------------------------
    # Rendering Engine
    # --------------------------------------------------------------------------
    def refresh_table(self, force=(1 == 0)):
        if not self.visible or self.main_win is None:
            return

        now = time.time()
        if not force and self.db.revision == self.last_rendered_rev and (now - self.last_ui_refresh_ts) < 0.7:
            return

        self.last_rendered_rev = self.db.revision
        self.last_ui_refresh_ts = now

        # Update top stats
        self.stats_lbl.SetText(
            "Pazar:%d/%d | Esya:%d | Al-Sat:%d | Magazam:%d" % (
                len(self.db.scanned_shops),
                max(len(self.db.map_shops), len(self.db.scanned_shops)),
                len(self.db.all_items),
                len(self.db.bargains),
                len(self.db.my_shop_items),
            )
        )
        self._update_navigation_styles()

        self.filtered_rows = self._compute_filtered_rows()
        total_rows = len(self.filtered_rows)
        self.total_pages = max(1, (total_rows + self.ROWS_PER_PAGE - 1) // self.ROWS_PER_PAGE)
        if self.page >= self.total_pages:
            self.page = max(0, self.total_pages - 1)

        self.page_lbl.SetText("Sayfa %d / %d (%d)" % (self.page + 1, self.total_pages, total_rows))

        my_yang = self.engine.get_player_yang()
        self.footer_info_lbl.SetText(
            "Yang: %s | Magazam: %s (%d Esya) | Kasa: %s | Kuyruk: Tarama=%d, Alim=%d, PazarEkle=%d" % (
                _fmt_yang(my_yang),
                "ACIK" if self.db.my_shop_open else "KAPALI",
                len(self.db.my_shop_items),
                _fmt_yang_short(self.db.my_safebox_yang),
                len(self.scanner.scan_queue),
                len(self.scanner.pending_buy_queue) + (1 if self.scanner.active_buy_req else 0),
                len(self.scanner.shop_add_queue) + len(self.scanner.shop_edit_queue),
            )
        )

        start_idx = self.page * self.ROWS_PER_PAGE
        for r_idx in range(self.ROWS_PER_PAGE):
            ctrl = self.row_Controls[r_idx]
            data_idx = start_idx + r_idx
            if data_idx >= total_rows:
                ctrl["bar"].SetColor(ctrl["base_color"])
                ctrl["c1"].SetText("")
                ctrl["c2"].SetText("")
                ctrl["c3"].SetText("")
                ctrl["c4"].SetText("")
                ctrl["c5"].SetText("")
                ctrl["c6"].SetText("")
                ctrl["btn_buy"]["hide"]()
                ctrl["btn_open"]["hide"]()
                ctrl["btn_go"]["hide"]()
                continue

            row = self.filtered_rows[data_idx]

            # Empty-State Actionable Row
            if isinstance(row, dict) and "_empty_action" in row:
                ctrl["bar"].SetColor(0xFF1A2436)
                ctrl["c1"].SetPackedFontColor(0xFFFFD166)
                ctrl["c1"].SetText(row.get("msg", "Veri bulunamadi."))
                ctrl["c2"].SetText("")
                ctrl["c3"].SetText("")
                ctrl["c4"].SetText("")
                ctrl["c5"].SetText("")
                ctrl["c6"].SetText("")
                ctrl["btn_buy"]["show"]()
                ctrl["btn_buy"]["set_text"](row.get("btn", "SIFIRLA"))
                ctrl["btn_buy"]["set_color"](0xFF1F4E78)
                ctrl["btn_open"]["hide"]()
                ctrl["btn_go"]["hide"]()
                continue

            # Render by Module & Subtab
            if self.module_idx == 0:
                self._render_mod0_row(ctrl, row, my_yang)
            elif self.module_idx == 1:
                self._render_mod1_row(ctrl, row)
            elif self.module_idx == 2:
                self._render_mod2_row(ctrl, row)
            else:
                self._render_mod3_row(ctrl, row)

    def _render_mod0_row(self, ctrl, row, my_yang):
        if self.sub_idx in (0, 1, 2):
            disc = row.get("discount_pct", 0)
            flip_p = row.get("flip_profit", 0)
            npc_p = row.get("npc_profit", 0)
            if npc_p > 0:
                ctrl["bar"].SetColor(0xFF143322)
            elif disc >= 35 or flip_p >= 50000:
                ctrl["bar"].SetColor(0xFF112E22)
            else:
                ctrl["bar"].SetColor(ctrl["base_color"])

            nm = row["name"]
            if len(nm) > 28:
                nm = nm[:26] + ".."
            ctrl["c1"].SetPackedFontColor(0xFF00FFCC if row["has_bonus"] else 0xFFF0F4F8)
            ctrl["c1"].SetText(nm)
            ctrl["c2"].SetText("x%d" % row["count"])
            ctrl["c3"].SetText(_fmt_yang(row["unit_price"]))

            can_afford = my_yang >= row["price"]
            ctrl["c4"].SetPackedFontColor(0xFF99E6B3 if can_afford else 0xFFFF8080)
            ctrl["c4"].SetText(_fmt_yang(row["price"]))

            if self.sub_idx == 2 or npc_p > flip_p:
                ctrl["c5"].SetPackedFontColor(0xFF00FF99)
                ctrl["c5"].SetText("+%s NPC" % _fmt_yang_short(npc_p))
            elif flip_p > 0:
                ctrl["c5"].SetPackedFontColor(0xFF00FF99 if disc >= 25 else 0xFFFFD166)
                ctrl["c5"].SetText("+%s (%%-%d)" % (_fmt_yang_short(flip_p), disc))
            else:
                ctrl["c5"].SetPackedFontColor(0xFF7A8FA6)
                ctrl["c5"].SetText("Piyasa")

            sd = row.get("supply_demand_summary", "")
            seller = row.get("seller", "?")[:10]
            ctrl["c6"].SetPackedFontColor(0xFF66FFCC if row.get("demand_tier", 0) >= 2 else 0xFFB8C8D8)
            ctrl["c6"].SetText(("%s | %s" % (sd, seller))[:25])

            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("AL+PAZAR" if (self.db.auto_list_bought and npc_p <= 0) else "SATIN AL")
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("AC")
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"]("GIT")

        elif self.sub_idx == 3:
            ctrl["bar"].SetColor(ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFFFFE066)
            ctrl["c1"].SetText(row["owner"][:26])
            ctrl["c2"].SetText("%d" % row["count"])
            ctrl["c3"].SetText("%dm" % (row["dist"] // 100))
            ctrl["c4"].SetText("%d, %d" % (row["x"] // 100, row["y"] // 100))
            ctrl["c5"].SetPackedFontColor(0xFF66FF99 if row["scanned"] else 0xFFFFAA66)
            ctrl["c5"].SetText("TARANDI" if row["scanned"] else "KUYRUKTA")
            ctrl["c6"].SetText(row["title"][:25])
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("PAZARI AC")
            ctrl["btn_open"]["hide"]()
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"]("GIT")

        else:
            ctrl["bar"].SetColor(ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFF80FFBF)
            ctrl["c1"].SetText(row.get("name", "?")[:28])
            ctrl["c2"].SetText("x%d" % int(row.get("count", 1)))
            ctrl["c3"].SetText(_fmt_yang(row.get("unit_price", 0)) if row.get("unit_price") else "-")
            ctrl["c4"].SetText(_fmt_yang(row.get("price", 0)) if row.get("price") else "-")
            ctrl["c5"].SetPackedFontColor(0xFFFFD166)
            ctrl["c5"].SetText(row.get("ts", ""))
            ctrl["c6"].SetText(row.get("seller", "")[:24])
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("ARA")
            ctrl["btn_open"]["hide"]()
            ctrl["btn_go"]["hide"]()

    def _render_mod1_row(self, ctrl, row):
        if self.sub_idx == 0:
            ctrl["bar"].SetColor(0xFF122822 if row.get("smart_total", 0) > 0 else ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFF00FFCC if row.get("demand_tier", 0) >= 2 else 0xFFF0F4F8)
            ctrl["c1"].SetText(("#%02d %s" % (row["slot"] + 1, row["name"]))[:28])
            ctrl["c2"].SetText("x%d" % row["count"])
            ctrl["c3"].SetText(_fmt_yang(row["smart_unit"]) if row["smart_unit"] > 0 else "Veri Yok")
            ctrl["c4"].SetPackedFontColor(0xFF66FF99 if row["smart_total"] > 0 else 0xFFFF8080)
            ctrl["c4"].SetText(_fmt_yang(row["smart_total"]) if row["smart_total"] > 0 else "-")
            ctrl["c5"].SetPackedFontColor(0xFFFFD166)
            ctrl["c5"].SetText(_fmt_yang(row["min_unit"]) if row["min_unit"] > 0 else "-")
            ctrl["c6"].SetText("%s (%d Teklif)" % (row["demand_label"], row["offers"]))
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("PAZARA KOY")
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("MIN")
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"]("ARA")

        elif self.sub_idx == 1:
            st_lbl = row.get("status", "GUNCEL")
            ctrl["bar"].SetColor(0xFF2B1E16 if "PAHALI" in st_lbl else ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFFFFE066)
            ctrl["c1"].SetText(row["name"][:28])
            ctrl["c2"].SetText("x%d" % row["count"])
            ctrl["c3"].SetText(_fmt_yang(row["unit_price"]))
            ctrl["c4"].SetPackedFontColor(0xFF80FFBF)
            ctrl["c4"].SetText(_fmt_yang(row["smart_total"]))
            ctrl["c5"].SetPackedFontColor(0xFFFF8080 if "PAHALI" in st_lbl else (0xFFFFD166 if "UCUZ" in st_lbl else 0xFF66FF99))
            ctrl["c5"].SetText(st_lbl[:13])
            ctrl["c6"].SetText("Min:%s | %dPaz" % (_fmt_yang_short(row["min_other"]), row["unique_sellers"]))
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("GUNCELLE")
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("CEK")
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"]("AC")

        elif self.sub_idx == 2:
            cat = row.get("category", "")
            ctrl["bar"].SetColor(0xFF143322 if cat == "NPC_ARB_KAR" else ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFFFFCC66 if cat == "PAZARDA_DEGERLI" else 0xFFF0F4F8)
            ctrl["c1"].SetText(("#%02d %s" % (row["slot"] + 1, row["name"]))[:28])
            ctrl["c2"].SetText("x%d" % row["count"])
            ctrl["c3"].SetText(_fmt_yang(row["npc_total"]))
            ctrl["c4"].SetText(_fmt_yang(row["market_total"]) if row["market_total"] > 0 else "Pazarda Yok")
            ctrl["c5"].SetPackedFontColor(0xFF00FF99 if cat == "NPC_ARB_KAR" else (0xFF80BFFF if cat == "PAZARDA_DEGERLI" else 0xFFD0DCE8))
            ctrl["c5"].SetText(row["rec_label"][:14])
            ctrl["c6"].SetText(row["bonus_summary"][:24])
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("PAZARA" if cat == "PAZARDA_DEGERLI" else "NPC SAT")
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("SAT")
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"]("NPC")

        elif self.sub_idx == 3:
            ctrl["bar"].SetColor(ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFF00FFCC)
            ctrl["c1"].SetText(row["query"][:26])
            ctrl["c2"].SetText(">=%d" % row["min_avg_dmg"] if row["min_avg_dmg"] > 0 else "-")
            ctrl["c3"].SetText(_fmt_yang(row["max_unit"]))
            ctrl["c4"].SetText("%d Adet" % len(row["bought_ids"]))
            en = row.get("enabled", (1 == 1))
            ctrl["c5"].SetPackedFontColor(0xFF66FF99 if en else 0xFFFF8080)
            ctrl["c5"].SetText("AKTIF" if en else "DURDU")
            ctrl["c6"].SetText("Oto-Magaza: %s" % ("ACIK" if self.db.auto_list_bought else "KAPALI"))
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("DURDUR" if en else "BASLAT")
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("SIL")
            ctrl["btn_go"]["hide"]()

        else:
            ctrl["bar"].SetColor(0xFF143322 if row.get("is_safebox_yang") else ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFFFFE066 if row.get("is_safebox_yang") else 0xFFF0F4F8)
            ctrl["c1"].SetText(row["name"][:28])
            ctrl["c2"].SetText("x%d" % row["count"])
            ctrl["c3"].SetText(_fmt_yang(row["unit_price"]) if row["unit_price"] else "-")
            ctrl["c4"].SetText(_fmt_yang(row["price"]) if row["price"] else "-")
            ctrl["c5"].SetPackedFontColor(0xFF66FF99)
            ctrl["c5"].SetText(row["status"][:13])
            ctrl["c6"].SetText(row["desc"][:25])
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("YANGI CEK")
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("AC")
            ctrl["btn_go"]["hide"]()

    def _render_mod2_row(self, ctrl, row):
        if self.sub_idx in (0, 1):
            cat = row.get("category", "MOB")
            ctrl["bar"].SetColor(0xFF1A2E22 if cat in ("METIN", "BOSS") else ctrl["base_color"])
            ctrl["c1"].SetPackedFontColor(0xFF00FFCC if cat == "METIN" else (0xFFFFCC66 if cat == "BOSS" else 0xFFF0F4F8))
            ctrl["c1"].SetText(row["name"][:28])
            ctrl["c2"].SetText(str(row["vnum"]))
            ctrl["c3"].SetText("%dm" % (row["dist"] // 100))
            ctrl["c4"].SetText("%d, %d" % (row["x"] // 100, row["y"] // 100))
            in_farm = row["vnum"] in self.scanner.farm_selected_vnums
            ctrl["c5"].SetPackedFontColor(0xFF66FF99 if (in_farm or cat == "METIN") else 0xFFB8C8D8)
            ctrl["c5"].SetText("SECILI" if in_farm else cat)
            cnt_txt = "Adet: %d" % row["count"] if "count" in row else "VID: %d" % row.get("vid", 0)
            ctrl["c6"].SetText("%s | %s" % (cat, cnt_txt))
            ctrl["btn_buy"]["show"]()
            ctrl["btn_buy"]["set_text"]("SALDIR" if self.sub_idx == 0 else ("CIKAR" if in_farm else "HEDEF EKLE"))
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"]("ISINLAN")
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"]("YURU")
        else:
            self._render_mod3_row(ctrl, row)

    def _render_mod3_row(self, ctrl, row):
        val = str(row.get("val", ""))
        ctrl["bar"].SetColor(0xFF122922 if val == "ACIK" else ctrl["base_color"])
        ctrl["c1"].SetPackedFontColor(0xFF00FFCC)
        ctrl["c1"].SetText(row.get("title", "")[:28])
        ctrl["c2"].SetText(row.get("mod", "")[:6])
        ctrl["c3"].SetPackedFontColor(0xFF66FF99 if val == "ACIK" else (0xFFFF8080 if val == "KAPALI" else 0xFFFFE066))
        ctrl["c3"].SetText(val[:14])
        ctrl["c4"].SetText(row.get("limit", "")[:15])
        ctrl["c5"].SetPackedFontColor(0xFF80FFBF)
        ctrl["c5"].SetText(row.get("status", "")[:12])
        ctrl["c6"].SetText(row.get("desc", "")[:26])

        b1 = row.get("b1", "DEGIS")
        b2 = row.get("b2", "-")
        b3 = row.get("b3", "-")
        ctrl["btn_buy"]["show"]()
        ctrl["btn_buy"]["set_text"](b1)
        if b2 and b2 != "-":
            ctrl["btn_open"]["show"]()
            ctrl["btn_open"]["set_text"](b2)
        else:
            ctrl["btn_open"]["hide"]()
        if b3 and b3 != "-":
            ctrl["btn_go"]["show"]()
            ctrl["btn_go"]["set_text"](b3)
        else:
            ctrl["btn_go"]["hide"]()

    def poll_hotkeys(self):
        if app is None or not hasattr(app, "IsPressed"):
            return
        now = time.time()
        dik_insert = getattr(app, "DIK_INSERT", 210)
        try:
            if app.IsPressed(dik_insert):
                if now - self.last_hotkey_ts.get(dik_insert, 0.0) > 0.35:
                    self.last_hotkey_ts[dik_insert] = now
                    self.toggle_visibility()
        except Exception:
            pass

    def tick(self):
        self.poll_hotkeys()
        self.scanner.tick()
        if self.visible:
            self.refresh_table(force=(1 == 0))


# ==============================================================================
# 6. SINGLETON INITIALIZER & HOT-RELOAD STATE MIGRATION
# ==============================================================================
_SUITE_INSTANCE = None


def _migrate_from_previous_instance(prev_suite, new_suite):
    """Preserves scanned market database across live hot-reloads and hides old UI windows."""
    if prev_suite is None or new_suite is None:
        return
    try:
        # Hide old UI windows so they don't overlap with the new v2.0 dashboard
        for w_attr in ("main_win", "toggle_win"):
            old_w = getattr(prev_suite, w_attr, None)
            if old_w is not None and hasattr(old_w, "Hide"):
                try:
                    old_w.Hide()
                except Exception:
                    pass

        old_scanner = getattr(prev_suite, "scanner", None)
        if old_scanner is not None:
            old_board = getattr(old_scanner, "hooked_board", None)
            orig_fn = getattr(old_scanner, "orig_open_shop_end", None)
            if old_board is not None and orig_fn is not None and not getattr(orig_fn, "_is_offshop_tool_hook", (1 == 0)):
                try:
                    old_board.OpenShop_End = orig_fn
                except Exception:
                    pass

        old_db = getattr(prev_suite, "db", None)
        new_db = new_suite.db
        if old_db is not None and new_db is not None:
            new_db.map_shops = dict(getattr(old_db, "map_shops", {}))
            new_db.map_shops_by_sign = dict(getattr(old_db, "map_shops_by_sign", {}))
            new_db.map_shops_by_owner = dict(getattr(old_db, "map_shops_by_owner", {}))
            new_db.vid_by_owner_id = dict(getattr(old_db, "vid_by_owner_id", {}))
            new_db.owner_id_by_vid = dict(getattr(old_db, "owner_id_by_vid", {}))
            new_db.scanned_shops = dict(getattr(old_db, "scanned_shops", {}))
            new_db.items_by_shop = dict(getattr(old_db, "items_by_shop", {}))
            new_db.real_sales_by_key = dict(getattr(old_db, "real_sales_by_key", {}))
            new_db.sales_feed = list(getattr(old_db, "sales_feed", []))
            new_db.total_live_sales = int(getattr(old_db, "total_live_sales", 0))
            new_db._rebuild_aggregates()
            new_db.revision += 1
            _tool_log("[MIGRATE] Migrated %d map_shops, %d scanned_shops, %d items to v2.0 Suite!" % (
                len(new_db.map_shops), len(new_db.scanned_shops), len(new_db.all_items)
            ))
    except Exception as e:
        _tool_log("[MIGRATE_ERR] %s\n%s" % (e, traceback.format_exc()))


def init_or_get_suite():
    global _SUITE_INSTANCE
    if _SUITE_INSTANCE is not None:
        return _SUITE_INSTANCE

    try:
        engine = _NativeShopEngine()
        db = OfflineShopDatabase(engine)
        scanner = _ShopScannerController(engine, db)
        _SUITE_INSTANCE = OfflineShopSuiteGUI(engine, db, scanner)

        # Check if sitecustomize passed a previous namespace during hot-reload
        prev_ns = globals().get("__prev_offshop_ns__", None)
        if isinstance(prev_ns, dict) and prev_ns.get("_SUITE_INSTANCE") is not None:
            _migrate_from_previous_instance(prev_ns.get("_SUITE_INSTANCE"), _SUITE_INSTANCE)

        # Immediately sync player's own Offline Shop & Safebox
        scanner.ensure_board_hook()
        scanner.request_my_shop_sync(silent=(1 == 1))
        scanner.request_safebox_sync(withdraw_all=(1 == 0))
        _SUITE_INSTANCE.refresh_table(force=(1 == 1))

        _tool_log("[INIT] OfflineShopSuiteGUI v2.0 initialized successfully.")
        _chat_notice("Avrasya2 All-In-One Bot v2.0 Hazir! [INSERT] ile acip kapatabilirsiniz.")
    except Exception as e:
        _tool_log("[INIT_FATAL] %s\n%s" % (e, traceback.format_exc()))
    return _SUITE_INSTANCE


def tick_suite():
    suite = init_or_get_suite()
    if suite is not None:
        try:
            suite.tick()
        except Exception as e:
            _tool_log("[TICK_ERR] %s" % e)
