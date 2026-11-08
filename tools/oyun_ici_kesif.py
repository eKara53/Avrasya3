# -*- coding: latin-1 -*-
"""Avrasya2 Oyun Ici Canli Kesif ve Dinamik Analiz Araci (Dumper v2.0).

Oyun acildiginda kareye yayilmis (frame-sliced) sekilde calisir, istemciyi
dondurmadan su verileri tools/cikti/ altina cikarir:
  1. istemci_modulleri.txt : sys.modules ve tum C++/Python sabit, sinif ve metodlari
  2. pack_py/              : pack.Get() + recursive import kesfi ile TUM FoxFS .py dosyalari
  3. yetenek_tablosu.tsv   : skill modulu uzerinden tum yetenek (skill) verileri
  4. canavar_vnum.tsv      : nonplayer uzerinden tum mob/metin/boss/npc vnum tablosu
  5. hedefler.txt          : Farm icin SALT ASCII metin/canavar tablosu
  6. esya_vnum.tsv         : item uzerinden tum esya vnum, tur, alt tur, deger0..5
  7. dinamik_durum.txt     : Calisma zamani oyun motoru durumu (nav, background, net, player, game)
"""

import os
import re
import sys
import time

OUT_DIR = r"C:\Users\erenk\Desktop\Avrasya2\tools\cikti"
PACK_OUT_DIR = os.path.join(OUT_DIR, "pack_py")
LOG_FILE = r"C:\Users\erenk\Desktop\Avrasya2\logs\kesif.log"

MOB_MAX_VNUM = 40000
MOB_STEP = 2000

ITEM_MAX_VNUM = 160000
ITEM_STEP = 2500

# CP1254 Turkce karakter -> ASCII donusum tablosu (byte bazli)
_TR_MAP = {
    "\xe7": "c", "\xc7": "C",
    "\xf0": "g", "\xd0": "G",
    "\xfd": "i", "\xdd": "I",
    "\xf6": "o", "\xd6": "O",
    "\xfe": "s", "\xde": "S",
    "\xfc": "u", "\xdc": "U",
    "\xe2": "a", "\xee": "i", "\xfb": "u",
}


def to_ascii(text):
    if not text:
        return ""
    out = []
    for ch in str(text):
        if ch in _TR_MAP:
            out.append(_TR_MAP[ch])
        elif 32 <= ord(ch) < 127:
            out.append(ch)
        else:
            out.append("?")
    return "".join(out)


def log(msg):
    try:
        d = os.path.dirname(LOG_FILE)
        if not os.path.isdir(d):
            os.makedirs(d)
        f = open(LOG_FILE, "a")
        try:
            f.write("%s %s\n" % (time.strftime("%H:%M:%S"), msg))
        finally:
            f.close()
    except Exception:
        pass


def chat_notice(msg):
    chat_mod = sys.modules.get("chat")
    if chat_mod is not None and hasattr(chat_mod, "AppendChat"):
        try:
            chat_mod.AppendChat(7, "[Avrasya2-Kesif] " + str(msg))
        except Exception:
            pass


class LiveDiscoveryRunner(object):
    def __init__(self):
        if not os.path.isdir(OUT_DIR):
            os.makedirs(OUT_DIR)
        if not os.path.isdir(PACK_OUT_DIR):
            os.makedirs(PACK_OUT_DIR)
        self.phase = "modules"
        self.mob_vnum = 1
        self.item_vnum = 1
        self.mobs = []
        self.items = []
        self.t0 = time.time()
        self.done = (1 == 0)
        self.game_dumped = (1 == 0)
        self.in_game_dumped = (1 == 0)
        self.last_wait_log = 0.0
        log("Canli kesif v2.0 baslatildi")
        chat_notice("Canli kesif basladi (moduller + recursive pack + skill + vnum)...")

    def _proto_ready(self):
        np = sys.modules.get("nonplayer")
        it = sys.modules.get("item")
        try:
            if np and hasattr(np, "GetMonsterName") and np.GetMonsterName(101):
                return (1 == 1)
        except Exception:
            pass
        try:
            if it and hasattr(it, "SelectItem") and hasattr(it, "GetItemName"):
                it.SelectItem(10)
                if it.GetItemName():
                    return (1 == 1)
        except Exception:
            pass
        return (1 == 0)

    def step(self):
        # Oyun modulu yuklendiginde modulleri ve pack'i tekrar dok
        if not self.game_dumped and "game" in sys.modules:
            try:
                self._dump_modules()
                self._dump_pack_scripts()
                self._dump_dynamic_state()
                self.game_dumped = (1 == 1)
                log("game modulu algilandi, moduller, pack ve dinamik durum guncellendi")
            except Exception:
                pass

        # Karakter haritaya girdiginde (GetMainCharacterIndex > 0) canli durumu dok
        if not self.in_game_dumped:
            pl = sys.modules.get("player")
            if pl is not None and hasattr(pl, "GetMainCharacterIndex"):
                try:
                    if pl.GetMainCharacterIndex() > 0:
                        self._dump_dynamic_state()
                        self._dump_modules()
                        self._dump_pack_scripts()
                        self.in_game_dumped = (1 == 1)
                        log("Harita girisi algilandi, dinamik durum guncellendi")
                except Exception:
                    pass

        if self.done:
            return (1 == 1)
        try:
            if self.phase == "modules":
                self._dump_modules()
                self.phase = "pack"
            elif self.phase == "pack":
                self._dump_pack_scripts()
                self.phase = "skills"
            elif self.phase == "skills":
                self._dump_skills()
                self._dump_dynamic_state()
                self.phase = "wait_proto"
            elif self.phase == "wait_proto":
                if self._proto_ready():
                    log("proto tablolari hazir, vnum taramasi basliyor")
                    self.t0 = time.time()
                    self.phase = "mobs"
                else:
                    now = time.time()
                    if now - self.last_wait_log > 5.0:
                        self.last_wait_log = now
                        log("proto tablolari bekleniyor (karakter secimi / oyun girisi)...")
            elif self.phase == "mobs":
                if self._step_mobs():
                    self._save_mobs()
                    self.phase = "items"
            elif self.phase == "items":
                if self._step_items():
                    self._save_items()
                    self.phase = "done"
            elif self.phase == "done":
                elapsed = time.time() - self.t0
                msg = "Tamamlandi (%.1f sn): %d mob/metin, %d esya" % (
                    elapsed, len(self.mobs), len(self.items))
                log(msg)
                chat_notice(msg)
                self.done = (1 == 1)
        except Exception:
            import traceback
            log("HATA (%s):\n%s" % (self.phase, traceback.format_exc()))
            self.done = (1 == 1)
        return (1 == 1)

    def _dump_modules(self):
        path = os.path.join(OUT_DIR, "istemci_modulleri.txt")
        names = sorted(sys.modules.keys())
        f = open(path, "w")
        try:
            f.write("# Yuklu sys.modules (%d adet)\n\n" % len(names))
            for name in names:
                mod = sys.modules.get(name)
                if mod is None:
                    continue
                ffile = getattr(mod, "__file__", "")
                f.write("=== [%s] (%s) ===\n" % (name, ffile))
                try:
                    attrs = sorted(dir(mod))
                except Exception:
                    attrs = []
                for a in attrs:
                    if a.startswith("__") and a.endswith("__"):
                        continue
                    try:
                        val = getattr(mod, a)
                        tname = type(val).__name__
                        if tname in ("int", "long", "float", "str", "bool"):
                            f.write("  %s = %r (%s)\n" % (a, val, tname))
                        elif tname in ("tuple", "list", "dict") and len(repr(val)) < 160:
                            f.write("  %s = %r (%s)\n" % (a, val, tname))
                        elif tname in ("classobj", "type"):
                            methods = [m for m in dir(val) if not m.startswith("__")]
                            f.write("  class %s: %s\n" % (a, ", ".join(methods[:80])))
                        else:
                            f.write("  %s (%s)\n" % (a, tname))
                    except Exception:
                        f.write("  %s (?)\n" % a)
                f.write("\n")
        finally:
            f.close()
        log("istemci_modulleri.txt yazildi (%d modul)" % len(names))

    def _dump_pack_scripts(self):
        pack_mod = sys.modules.get("pack")
        if pack_mod is None or not hasattr(pack_mod, "Get"):
            log("pack.Get bulunamadi, pack_py atlandi")
            return

        seed_files = [
            "system.py", "prototype.py", "game.py", "ui.py",
            "interfacemodule.py", "interfaceModule.py",
            "networkmodule.py", "networkModule.py",
            "intrologin.py", "introLogin.py",
            "introselect.py", "introSelect.py",
            "introcreate.py", "introCreate.py",
            "introloading.py", "introLoading.py",
            "introempire.py", "introEmpire.py",
            "constinfo.py", "constInfo.py",
            "localeinfo.py", "localeInfo.py",
            "playersettingmodule.py", "playerSettingModule.py",
            "emotion.py", "musicinfo.py", "musicInfo.py",
            "debuginfo.py", "debugInfo.py",
            " mousemodule.py", "mouseModule.py",
            "consolemodule.py", "consoleModule.py",
            "stringcommander.py", "stringCommander.py",
            "uicommon.py", "uiCommon.py",
            "uiinventory.py", "uiInventory.py",
            "uiminimap.py", "uiMiniMap.py",
            "uiaffectshower.py", "uiAffectShower.py",
            "uitarget.py", "uiTarget.py",
            "uitaskbar.py", "uiTaskBar.py",
            "uicharacter.py", "uiCharacter.py",
            "uichat.py", "uiChat.py",
            "uigameoption.py", "uiGameOption.py",
            "uisystemoption.py", "uiSystemOption.py",
            "uishop.py", "uiShop.py",
            "uiofflineshop.py", "uiOfflineShop.py",
            "uiofflineshopbuilder.py", "uiOfflineShopBuilder.py",
            "uiprivateshopbuilder.py", "uiPrivateShopBuilder.py",
            "uisafebox.py", "uiSafebox.py",
            "uiexchange.py", "uiExchange.py",
            "uirefine.py", "uiRefine.py",
            "uiguild.py", "uiGuild.py",
            "uimessenger.py", "uiMessenger.py",
            "uiparty.py", "uiParty.py",
            "uiquest.py", "uiQuest.py",
            "uiwhisper.py", "uiWhisper.py",
            "uitooltip.py", "uiToolTip.py",
            "uidragonsoul.py", "uiDragonSoul.py",
            "uiacce.py", "uiAcce.py",
            "uiaura.py", "uiAura.py",
            "uiswitchbot.py", "uiSwitchbot.py", "uiSwitchBot.py",
            "uiefsun.py", "uiEfsun.py",
            "uibiolog.py", "uiBiolog.py",
            "uidungeoninfo.py", "uiDungeonInfo.py",
            "uibosstracking.py", "uiBossTracking.py",
            "uiautohunt.py", "uiAutoHunt.py",
            "uibotkontrol.py", "uiBotKontrol.py",
            "uicaptcha.py", "uiCaptcha.py",
            "uifishing.py", "uiFishing.py",
            "uicube.py", "uiCube.py",
            "uicards.py", "uiCards.py",
            "uibattlepass.py", "uiBattlePass.py",
            "uiwheel.py", "uiWheel.py",
            "uirank.py", "uiRank.py",
            "uiranking.py", "uiRanking.py",
            "uiteleport.py", "uiTeleport.py",
            "uispecialstorage.py", "uiSpecialStorage.py",
            "uichestdrop.py", "uiChestDrop.py",
            "uirestart.py", "uiRestart.py",
            "uipickmoney.py", "uiPickMoney.py",
            "uipickitem.py", "uiPickItem.py",
            "uiattachmetin.py", "uiAttachMetin.py",
            "uiselectitem.py", "uiSelectItem.py",
            "uiselectmusic.py", "uiSelectMusic.py",
            "uihelp.py", "uiHelp.py",
            "uitip.py", "uiTip.py",
            "uigamebutton.py", "uiGameButton.py",
            "uipointreset.py", "uiPointReset.py",
            "uimapnameshower.py", "uiMapNameShower.py",
            "uiphasecurtain.py", "uiPhaseCurtain.py",
            "uiscrollbar.py", "uiScrollBar.py",
            "servercommandparser.py", "serverCommandParser.py",
            "serverinfo.py", "serverInfo.py",
        ]

        queue = list(seed_files)
        for mname in list(sys.modules.keys()):
            if mname and not mname.startswith("_"):
                fn = mname.strip() + ".py"
                if fn not in queue:
                    queue.append(fn)

        saved = 0
        seen_lower = {}
        import_re = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_]+)", re.MULTILINE)

        idx = 0
        while idx < len(queue):
            fn = queue[idx].strip()
            idx += 1
            low = fn.lower()
            if low in seen_lower:
                continue
            seen_lower[low] = (1 == 1)

            try:
                if hasattr(pack_mod, "Exist") and not pack_mod.Exist(fn):
                    continue
                data = pack_mod.Get(fn)
                if not data:
                    continue
                if isinstance(data, unicode):
                    raw_bytes = data.encode("utf-8")
                else:
                    raw_bytes = str(data)

                if len(raw_bytes) == 0:
                    continue

                out_path = os.path.join(PACK_OUT_DIR, os.path.basename(fn))
                fh = open(out_path, "wb")
                try:
                    fh.write(raw_bytes)
                finally:
                    fh.close()
                saved += 1

                # Cikarilan betik icindeki import ifadelerini bulup kuyruga ekle
                for m in import_re.findall(raw_bytes):
                    cand = m + ".py"
                    if cand.lower() not in seen_lower:
                        queue.append(cand)
                    cand_low = m.lower() + ".py"
                    if cand_low not in seen_lower:
                        queue.append(cand_low)
            except Exception as e:
                log("pack.Get(%s) hata: %s" % (fn, e))

        log("pack_py altina %d betik kaydedildi (taranan aday: %d)" % (saved, len(queue)))

    def _dump_skills(self):
        sk = sys.modules.get("skill")
        if sk is None:
            return
        path = os.path.join(OUT_DIR, "yetenek_tablosu.tsv")
        f = open(path, "w")
        count = 0
        try:
            f.write("# id\tad_ascii\ttip\tmax_level\tsp_cost\tis_standing\tad_ham\n")
            for i in range(1, 300):
                try:
                    name = sk.GetSkillName(i) if hasattr(sk, "GetSkillName") else ""
                except Exception:
                    name = ""
                if not name:
                    continue
                stype = 0
                max_lvl = 0
                sp_cost = 0
                standing = 0
                try:
                    stype = sk.GetSkillType(i)
                except Exception:
                    pass
                try:
                    max_lvl = sk.GetSkillMaxLevel(i)
                except Exception:
                    pass
                try:
                    sp_cost = sk.GetSkillNeedSP(i, 1)
                except Exception:
                    pass
                try:
                    standing = sk.IsStandingSkill(i)
                except Exception:
                    pass
                f.write("%d\t%s\t%d\t%d\t%d\t%d\t%s\n" % (
                    i, to_ascii(name), stype, max_lvl, sp_cost, standing, name))
                count += 1
        finally:
            f.close()
        log("yetenek_tablosu.tsv yazildi (%d yetenek)" % count)

    def _dump_dynamic_state(self):
        path = os.path.join(OUT_DIR, "dinamik_durum.txt")
        f = open(path, "w")
        try:
            f.write("=== AVRASYA2 RUNTIME DINAMIK DURUM RAPORU ===\n")
            f.write("Zaman: %s\n\n" % time.strftime("%Y-%m-%d %H:%M:%S"))

            # 1. Nav modulu durumu
            nav = sys.modules.get("nav")
            if nav is not None:
                f.write("[nav Modulu]\n")
                for fn in ("IsAvailable", "IsActive", "IsRunning", "GetState",
                           "IsMapReady", "GetDiagnostics", "GetDebugText"):
                    if hasattr(nav, fn):
                        try:
                            f.write("  nav.%s() = %r\n" % (fn, getattr(nav, fn)()))
                        except Exception as e:
                            f.write("  nav.%s() -> hata: %s\n" % (fn, e))
                f.write("\n")

            # 2. Background modulu durumu
            bg = sys.modules.get("background")
            if bg is not None:
                f.write("[background Modulu]\n")
                for fn in ("GetCurrentMapName", "GetFarClip", "GetRenderShadowTime",
                           "GetRenderedSplatNum", "GetRenderedGraphicThingInstanceNum"):
                    if hasattr(bg, fn):
                        try:
                            f.write("  background.%s() = %r\n" % (fn, getattr(bg, fn)()))
                        except Exception as e:
                            f.write("  background.%s() -> hata: %s\n" % (fn, e))
                f.write("\n")

            # 3. Net modulu durumu
            net = sys.modules.get("net")
            if net is not None:
                f.write("[net Modulu]\n")
                for fn in ("GetServerInfo", "GetMainActorVID", "GetMainActorRace",
                           "GetMainActorEmpire", "GetMainActorSkillGroup", "IsConnect"):
                    if hasattr(net, fn):
                        try:
                            f.write("  net.%s() = %r\n" % (fn, getattr(net, fn)()))
                        except Exception as e:
                            f.write("  net.%s() -> hata: %s\n" % (fn, e))
                f.write("\n")

            # 4. Player modulu durumu
            pl = sys.modules.get("player")
            if pl is not None:
                f.write("[player Modulu]\n")
                for fn in ("GetMainCharacterIndex", "GetMainCharacterName",
                           "GetMainCharacterPosition", "GetName", "GetJob",
                           "GetRace", "GetPlayTime", "GetMoney", "GetDragonCoin",
                           "GetDragonMark", "GetPKMode", "IsInSafeArea", "IsMountingHorse"):
                    if hasattr(pl, fn):
                        try:
                            f.write("  player.%s() = %r\n" % (fn, getattr(pl, fn)()))
                        except Exception as e:
                            f.write("  player.%s() -> hata: %s\n" % (fn, e))
                f.write("\n")

            # 5. constInfo icerigi
            ci = sys.modules.get("constInfo") or sys.modules.get("constinfo")
            if ci is not None:
                f.write("[constInfo Degiskenleri]\n")
                for k in sorted(dir(ci)):
                    if not k.startswith("__"):
                        try:
                            f.write("  constInfo.%s = %r\n" % (k, getattr(ci, k)))
                        except Exception:
                            pass
                f.write("\n")
        finally:
            f.close()
        log("dinamik_durum.txt yazildi")

    def _step_mobs(self):
        np = sys.modules.get("nonplayer")
        if np is None or not hasattr(np, "GetMonsterName"):
            log("nonplayer.GetMonsterName yok, mob taramasi atlandi")
            return (1 == 1)

        get_name = np.GetMonsterName
        get_lvl = getattr(np, "GetMonsterLevel", None)
        get_hp = getattr(np, "GetMonsterMaxHP", None)
        is_stone = getattr(np, "IsMonsterStone", None)

        end = min(MOB_MAX_VNUM, self.mob_vnum + MOB_STEP)
        v = self.mob_vnum
        while v < end:
            try:
                name = get_name(v)
            except Exception:
                name = ""
            if name:
                lvl = 0
                hp = 0
                stone = 0
                try:
                    if get_lvl:
                        lvl = get_lvl(v)
                except Exception:
                    pass
                try:
                    if get_hp:
                        hp = get_hp(v)
                except Exception:
                    pass
                try:
                    if is_stone:
                        stone = is_stone(v)
                except Exception:
                    pass
                if stone or (8000 <= v <= 8999):
                    kind = "metin"
                else:
                    kind = "canavar"
                self.mobs.append((v, kind, lvl, hp, name, to_ascii(name)))
            v += 1

        self.mob_vnum = end
        return self.mob_vnum >= MOB_MAX_VNUM

    def _save_mobs(self):
        tsv_path = os.path.join(OUT_DIR, "canavar_vnum.tsv")
        f = open(tsv_path, "w")
        try:
            f.write("# vnum\ttur\tseviye\tmax_hp\tad_ascii\tad_ham\n")
            for v, kind, lvl, hp, name, asc in self.mobs:
                f.write("%d\t%s\t%d\t%d\t%s\t%s\n" % (v, kind, lvl, hp, asc, name))
        finally:
            f.close()

        hedef_path = os.path.join(OUT_DIR, "hedefler.txt")
        f2 = open(hedef_path, "w")
        try:
            for v, kind, lvl, hp, _name, asc in self.mobs:
                f2.write("%d\t%s\t%d\t%s\n" % (v, kind, lvl, asc))
        finally:
            f2.close()
        log("canavar_vnum.tsv ve hedefler.txt yazildi (%d kayit)" % len(self.mobs))

    def _step_items(self):
        it = sys.modules.get("item")
        if it is None or not hasattr(it, "SelectItem"):
            log("item.SelectItem yok, esya taramasi atlandi")
            return (1 == 1)

        sel = it.SelectItem
        get_name = getattr(it, "GetItemName", None)
        get_type = getattr(it, "GetItemType", None)
        get_sub = getattr(it, "GetItemSubType", None)
        get_val = getattr(it, "GetValue", None)

        end = min(ITEM_MAX_VNUM, self.item_vnum + ITEM_STEP)
        v = self.item_vnum
        while v < end:
            try:
                sel(v)
                name = get_name() if get_name else ""
            except Exception:
                name = ""
            if name:
                itype = 0
                isub = 0
                vals = []
                try:
                    if get_type:
                        itype = get_type()
                except Exception:
                    pass
                try:
                    if get_sub:
                        isub = get_sub()
                except Exception:
                    pass
                if get_val:
                    for idx in range(6):
                        try:
                            vals.append(str(get_val(idx)))
                        except Exception:
                            vals.append("0")
                self.items.append((v, itype, isub, to_ascii(name), name, ",".join(vals)))
            v += 1

        self.item_vnum = end
        return self.item_vnum >= ITEM_MAX_VNUM

    def _save_items(self):
        tsv_path = os.path.join(OUT_DIR, "esya_vnum.tsv")
        f = open(tsv_path, "w")
        try:
            f.write("# vnum\ttur\talt_tur\tad_ascii\tdeger0_5\tad_ham\n")
            for v, itype, isub, asc, name, vals in self.items:
                f.write("%d\t%d\t%d\t%s\t%s\t%s\n" % (v, itype, isub, asc, vals, name))
        finally:
            f.close()
        log("esya_vnum.tsv yazildi (%d esya)" % len(self.items))
