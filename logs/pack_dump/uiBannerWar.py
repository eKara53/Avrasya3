# DUMPED FROM LIVE COMPILE: uiBannerWar.py (len=51371)
#
# Sancak Savasi (Banner War): pencere + oyun butonu + Tasa Git + bayrak ustu lonca yazisi.
#
# Veri akisi (client C++ degisikligi YOK):
#   sunucu -> ChatPacket(CHAT_TYPE_COMMAND, "BW_...") -> game.py serverCommandList -> bu dosya
#   bu dosya -> net.SendChatPacket("/sancak") / "/sancak durum" / "/sancak git <bayrak>" -> sunucu
#   "[Sancak Savasi]" duyurulari -> game.py BINARY_SetTipMessage/BigMessage -> OnNotice (Savas Gunlugu)
#
# Gorunum tamamen orijinal Metin2 parcalarindan kurulur (yeni gorsel YOK):
#   pencere ................ ui.BoardWithTitleBar + ui.ThinBoard           (tum orijinal pencereler)
#   bolum basliklari ....... ui.HorizontalBar                              (Lonca > Bilgi sayfasi)
#   sekmeler ............... ui.RadioButton + public/large_button_0X.sub   (Oyun Secenekleri)
#   tablo hucreleri ........ ui.SlotBar, satir araligi 20                  (Lonca > Uyeler listesi)
#   tas cani ............... ui.Gauge "red"                                (hedef HP bari)
#   lonca armasi ........... ui.MarkBox                                    (Lonca Savasi skor tablosu)
#   bayrak resimleri ....... intro/empire/empireflag_a/b/c.sub             (karakter secim ekrani)
#   renkler ................ uiToolTip paleti (TITLE / SPECIAL_TITLE / NORMAL / POSITIVE / NEGATIVE / CONDITION)
#   oyun butonu ............ "Bayrak" esya ikonu, gorev mektubu gibi yanip soner (interfacemodule BINARY_RecvQuest)
#
import ui
import net
import app
import chr
import chat
import guild
import player
import wndMgr
import miniMap
import localeInfo

try:
	import nav
	NAV_ENABLED = True
except ImportError:
	nav = None
	NAV_ENABLED = False

try:
	import time as _time
except ImportError:
	_time = None

FRONT_NONE = 0
FRONT_ALIVE = 1
FRONT_FALLEN = 2
FRONT_DEFENDED = 3

PHASE_NONE = 0
PHASE_SOON = 1
PHASE_ACTIVE = 2
PHASE_RESULT = 3

RANK_TYPE_PLAYER = 0
RANK_TYPE_GUILD = 1

TAB_PLAYER = 0
TAB_GUILD = 1
TAB_LOG = 2
TAB_HELP = 3
TAB_COUNT = 4

ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2

# --- renkler: uiToolTip.ToolTip paletinin aynisi
COLOR_TITLE = 0xFFF2E7C1		# TITLE_COLOR
COLOR_GOLD = 0xFFFFC800			# SPECIAL_TITLE_COLOR
COLOR_NORMAL = 0xFFC2C2C2		# NORMAL_COLOR
COLOR_LABEL = 0xFFBEB47D		# CONDITION_COLOR
COLOR_POSITIVE = 0xFF8AB98E		# POSITIVE_COLOR
COLOR_NEGATIVE = 0xFFE57976		# NEGATIVE_COLOR
COLOR_MUTED = 0xFF8C8C8C
COLOR_WHITE = 0xFFFFFFFF
COLOR_ALERT = 0xFFFF5A5A		# "SAVAS SURUYOR" / oyun butonu geri sayimi
COLOR_HUD_GREEN = 0xFF7CFF7C	# oyun butonu "Sonuclar!"

EMPIRE_COLOR = {
	1 : 0xFFFF6E6E,	# Kirmizi
	2 : 0xFFFFD75A,	# Sari
	3 : 0xFF6EAAFF,	# Mavi
}

RANK_POS_COLOR = {
	1 : 0xFFFFD700,	# altin
	2 : 0xFFD8D8D8,	# gumus
	3 : 0xFFE3A869,	# bronz
}

# --- orijinal gorseller (hepsi bu client'in uiscript'lerinde zaten kullaniliyor)
MIDDLE_BUTTON = ("d:/ymir work/ui/public/middle_button_01.sub", "d:/ymir work/ui/public/middle_button_02.sub", "d:/ymir work/ui/public/middle_button_03.sub")	# 61x21
LARGE_BUTTON = ("d:/ymir work/ui/public/large_button_01.sub", "d:/ymir work/ui/public/large_button_02.sub", "d:/ymir work/ui/public/large_button_03.sub")	# 88x21
PLUS_BUTTON = ("d:/ymir work/ui/game/windows/btn_bigplus_up.sub", "d:/ymir work/ui/game/windows/btn_bigplus_over.sub", "d:/ymir work/ui/game/windows/btn_bigplus_down.sub")	# 32x32
EMPIRE_FLAG = {
	1 : "d:/ymir work/ui/intro/empire/empireflag_a.sub",
	2 : "d:/ymir work/ui/intro/empire/empireflag_b.sub",
	3 : "d:/ymir work/ui/intro/empire/empireflag_c.sub",
}

# Oyun butonunun ikonu: "Bayrak" esyasi (item_list: 30052 ETC icon/item/30052.tga).
# Dosya pakette yoksa Statu (+) butonu gorunumu kullanilir.
GAME_BUTTON_ICON = "icon/item/30052.tga"

# --- pencere yerlesimi (piksel)
WINDOW_WIDTH = 560
WINDOW_HEIGHT = 548

CONTENT_X = 10
CONTENT_WIDTH = WINDOW_WIDTH - CONTENT_X * 2	# 540

STATUS_Y = 34
STATUS_HEIGHT = 42

CARD_Y = 82
CARD_WIDTH = 176
CARD_HEIGHT = 160
CARD_GAP = (CONTENT_WIDTH - CARD_WIDTH * 3) // 2	# 6

TAB_Y = 248
TAB_GAP = 4

CONTENT_Y = 274
CONTENT_HEIGHT = 236

FOOTER_Y = 518

ROW_HEIGHT = 17		# ui.SlotBar yuksekligi (Lonca > Uyeler ile ayni)
ROW_STEP = 20		# satir araligi (Lonca > Uyeler ile ayni)
FIRST_ROW_Y = 28	# baslik barinin (6..23) altindan
TEXT_PAD = 6		# sola dayali hucre yazisinin hucre icindeki boslugu
MARK_PAD = 22		# arma (16x12) + bosluk

RANK_ROWS = 10
LOG_LINES = 10
LOG_MAX_CHARS = 160			# ust sinir; asil kisaltma piksel genisligine gore (LOG_TEXT_WIDTH)
HELP_LINES = 11
HELP_ROW_STEP = 19

# Siralama sutunlari: (x, genislik). Sira: #, isim, bayrak, zafer, les, fetih
RANK_COLUMNS = ((10, 28), (42, 196), (242, 84), (330, 70), (404, 60), (468, 62))
COL_NAME = 1

LOG_COLUMNS = ((10, 44), (58, 472))	# saat, olay
LOG_TEXT_WIDTH = LOG_COLUMNS[1][1] - TEXT_PAD - 6	# olay hucresine sigan en genis yazi (piksel)

AUTO_REFRESH_SEC = 15.0		# savas surerken acik pencere bu aralikla (hafif istekle) yenilenir
FLIP_REFRESH_SEC = 5.0		# geri sayim 0'a vurunca (savas basladi / bitti) daha sik sorulur
MANUAL_OPEN_SEC = 5.0		# butona basildiktan sonra bu sure icinde gelen cevap pencereyi her durumda acar

NOTICE_PREFIX = "[Sancak Sava"	# sunucu duyurularinin ASCII kismi ("[Sancak Savasi] ...")

# Oyun butonunun yeri: sol altta, orijinal "Yardim" butonunun (50, H-170) 70 px ustu. Yaninda "Tasa Git".
GAME_BUTTON_X = 50
GAME_BUTTON_BOTTOM = 240

# Minimap / atlas isareti (uiminimap.py navigasyon isareti 0x4E415601 kullanir; carpismaz).
WAYPOINT_ID = 0x42570001

# Dusen sancagin ustundeki lonca yazisi (chr.GetProjectPosition + buyuk font).
# Bayrak (20035-20037) gorunumu bir efekt mesh'idir: effect/etc/guild_war_flag/flag_*.mde, yerden 196 birim boy
# (dosyadan olculdu). Client C++ (InstanceBase.cpp c_akRaceScale) bayragi %200 buyutur; ikisi AYNI olmali.
FLAG_MODEL_HEIGHT = 196
FLAG_MODEL_SCALE = 2.0
FLAG_NAME_GAP = 25				# PythonTextTail.cpp c_fBannerFlagNameGap ile ayni (bayragin tepesi - isim arasi)
FLAG_TAG_HEIGHT = int(FLAG_MODEL_HEIGHT * FLAG_MODEL_SCALE) + FLAG_NAME_GAP	# C++ isim yazisinin taban noktasi
# Lonca adini ve armasini bayragin ustune kim yazar?
#   False: client C++ isim yamasi (CLIENT_PATCH 7) uygulandi. Ad bayrak renginde ve buyuk, lonca armasi
#          yaninda (oyuncu isimlerindeki gibi) C++ tarafindan yazilir; burada sadece "... bu sancagi fethetti"
#          satiri, o ismin hemen ustunde (cift isim / cift arma olmaz).
#   True : 7 uygulanmadi; lonca adini ve armasini bu dosya yazar.
FLAG_TAG_SHOW_TITLE = False
FLAG_NAME_HEIGHT_PX = 20		# C++ isim yazisinin (Tahoma:18) ekrandaki yuksekligi
FLAG_GUILD_LINE_OFFSET = 15		# C++ "[arma] isim" satirinin ana isimden yuksekligi (PythonTextTail.cpp c_fyGuildNamePosition)
FLAG_TAG_FONT = "Tahoma:18"	# C++ isim fontuyla ayni boy. Motor sadece "i" (italik) ekini tanir, "b" (kalin) yok sayilir.
FLAG_TAG_MARK_SCALE = 2			# arma 16x12 -> 32x24

# Tasa Git (otomatik navigasyon) durum makinesi
NAV_IDLE = 0
NAV_WAIT_DATA = 1		# harita/navigasyon verisi hazirlaniyor, tekrar denenecek
NAV_WAIT_PREVIEW = 2	# rota hesaplaniyor, hazir olunca onaylanacak
PREVIEW_NONE = 0		# navigasyonda on izleme yok
PREVIEW_OURS = 1		# on izleme bizim tas hedefimiz
PREVIEW_OTHER = 2		# oyuncunun kendi (atlas) rotasi
NAV_RETRY_SEC = 1.0
NAV_RETRY_MAX = 10
NAV_PREVIEW_TIMEOUT = 10.0
AUTO_NAV_AFTER_WARP_SEC = 90.0

# "Cepheye Git" ile isinlanan oyuncu, yeni haritaya girince tasa otomatik yurur.
# Modul seviyesinde tutulur: isinlanmada pencere yeniden olusur, modul kalir.
_autoNavRequestedAt = [-1000.0]


def _T(key):
	# locale_game.txt satiri eksikse oyun cokmesin, anahtar adi gorunsun (hata hemen fark edilir).
	return getattr(localeInfo, key, key)


def _F(key, *args):
	try:
		return getattr(localeInfo, key) % args
	except Exception:
		return key


def _ToInt(value, default = 0):
	try:
		return int(value)
	except (TypeError, ValueError):
		return default


def _EmpireName(empire):
	return _T("BANNER_WAR_EMPIRE_%d" % empire)


def _EmpireColor(empire):
	return EMPIRE_COLOR.get(empire, COLOR_NORMAL)


def _HasName(name):
	return bool(name) and name != "-"


def _FormatTime(seconds):
	if seconds < 0:
		seconds = 0

	day = seconds // 86400
	hour = (seconds % 86400) // 3600
	minute = (seconds % 3600) // 60
	second = seconds % 60

	if day > 0:
		return _F("BANNER_WAR_TIME_DHM", day, hour, minute)

	if hour > 0:
		return _F("BANNER_WAR_TIME_HM", hour, minute)

	return _F("BANNER_WAR_TIME_MS", minute, second)


def _Clock():
	if _time:
		try:
			return _time.strftime("%H:%M")
		except Exception:
			pass
	return ""


def _SetGuildMark(markBox, guildID, scale = 1):
	# Arma sadece client'in tanidigi bir lonca icin gosterilir. Bilinmeyen loncada GuildIDToMarkID -1 dondurur
	# (MarkManager INVALID_MARK_ID); o durumda bos/yanlis arma cizilmesin diye gizlenir.
	# Olcek SetIndex'ten SONRA verilir: her SetIndex yeni bir arma ornegi yaratir (CMarkBox::LoadImage),
	# ornek yokken SetScale hicbir sey yapmaz (uiguild.py da boyle: SetIndex, sonra SetScale(3)).
	if not markBox:
		return False

	if guildID > 0:
		try:
			if guild.GuildIDToMarkID(guildID) >= 0:
				markBox.SetIndex(guildID)

				if scale != 1:
					markBox.SetScale(scale)

				markBox.Show()
				return True
		except Exception:
			pass

	markBox.Hide()
	return False


def _GameButtonVisuals():
	try:
		if app.IsExistFile(GAME_BUTTON_ICON):
			return (GAME_BUTTON_ICON, GAME_BUTTON_ICON, GAME_BUTTON_ICON)
	except Exception:
		pass
	return PLUS_BUTTON


def _NavRetryable(result):
	if not NAV_ENABLED:
		return False
	return result in (nav.START_FAIL_NO_DATA, nav.START_FAIL_NO_ATLAS, nav.START_FAIL_NO_ACTOR,
					nav.START_FAIL_CANNOT_MOVE, nav.START_FAIL_BUSY)


class BannerWarGameButton(ui.Button):
	# Gorev mektubu gibi: esya ikonu, savasta yanip soner. Altinda "Sancak Savasi" ve geri sayim
	# (orijinal Yardim/Statu butonlarinin yazi yeri: x 16, y 40).
	#
	# Motor notlari (EterPythonLib/PythonWindow.cpp):
	#  - CButton::OnUpdate bos; Button alt sinifinin Python OnUpdate'i HIC cagrilmaz.
	#    Geri sayimi bu yuzden BannerWarHud.OnUpdate surer (UpdateCountdown).
	#  - Flash() bir kez acilir, kapatan fonksiyon yoktur. Yanip sonme bitmesi gerekince
	#    BannerWarHud butonu yeniden olusturur (isFlashing).

	def __init__(self):
		ui.Button.__init__(self)
		self.nameText = None
		self.timeText = None
		self.phase = PHASE_NONE
		self.remainSec = 0
		self.remainBase = 0.0
		self.lastShownSec = -1
		self.isFlashing = False
		self.__Create()

	def __del__(self):
		ui.Button.__del__(self)

	def __Create(self):
		visuals = _GameButtonVisuals()
		self.SetUpVisual(visuals[0])
		self.SetOverVisual(visuals[1])
		self.SetDownVisual(visuals[2])

		centerX = max(32, self.GetWidth()) // 2
		labelY = max(32, self.GetHeight()) + 8

		self.nameText = ui.TextLine()
		self.nameText.SetParent(self)
		self.nameText.SetPosition(centerX, labelY)
		self.nameText.SetHorizontalAlignCenter()
		self.nameText.SetOutline()
		self.nameText.SetPackedFontColor(COLOR_TITLE)
		self.nameText.SetText(_T("BANNER_WAR_BTN_NAME"))
		self.nameText.AddFlag("not_pick")
		self.nameText.Show()

		self.timeText = ui.TextLine()
		self.timeText.SetParent(self)
		self.timeText.SetPosition(centerX, labelY + 14)
		self.timeText.SetHorizontalAlignCenter()
		self.timeText.SetOutline()
		self.timeText.AddFlag("not_pick")
		self.timeText.Show()

		self.SetToolTipText(_T("BANNER_WAR_BTN_TOOLTIP"))
		self.Hide()

	def Destroy(self):
		self.SetEvent(None)
		self.Hide()
		self.nameText = None
		self.timeText = None

	def SetState(self, phase, remain):
		self.phase = phase
		self.remainSec = remain
		self.remainBase = app.GetTime()
		self.lastShownSec = -1

		if phase == PHASE_NONE:
			self.Hide()
			return

		self.__RefreshTime(max(0, remain))
		self.Show()

		if phase in (PHASE_ACTIVE, PHASE_RESULT) and not self.isFlashing:
			self.isFlashing = True
			self.Flash()

	def UpdateCountdown(self):
		if self.phase not in (PHASE_SOON, PHASE_ACTIVE):
			return

		sec = max(0, int(self.remainSec - (app.GetTime() - self.remainBase)))

		if sec != self.lastShownSec:
			self.lastShownSec = sec
			self.__RefreshTime(sec)

	def __RefreshTime(self, sec):
		if not self.timeText:
			return

		if self.phase == PHASE_SOON:
			self.timeText.SetText(_F("BANNER_WAR_BTN_SOON", _FormatTime(sec)))
			self.timeText.SetPackedFontColor(COLOR_WHITE)
		elif self.phase == PHASE_ACTIVE:
			self.timeText.SetText(_F("BANNER_WAR_BTN_ACTIVE", _FormatTime(sec)))
			self.timeText.SetPackedFontColor(COLOR_ALERT)
		else:
			self.timeText.SetText(_T("BANNER_WAR_BTN_RESULT"))
			self.timeText.SetPackedFontColor(COLOR_HUD_GREEN)


class BannerWarHud(ui.Window):
	# Ekrandaki buton grubu: [Sancak Savasi]  [Tasa Git]
	# Konteyner "not_pick": bos alani oyun tiklamalarini yutmaz, cocuk butonlar tiklanir
	# (orijinal uiscript/gamewindow.py ile ayni yapi).

	def __init__(self):
		ui.Window.__init__(self)
		self.gameButton = None
		self.gameButtonEvent = None
		self.goStoneButton = None
		self.phase = PHASE_NONE
		self.hereFront = 0
		self.stoneX = 0
		self.stoneY = 0
		self.waypointShown = False
		self.navState = NAV_IDLE
		self.navStartedAt = 0.0
		self.navRetryAt = 0.0
		self.navRetries = 0
		self.navManual = False
		self.navTargetX = 0.0
		self.navTargetY = 0.0
		self.__Create()

	def __del__(self):
		ui.Window.__del__(self)

	def __Create(self):
		self.AddFlag("not_pick")
		self.SetSize(140, 72)
		self.SetPosition(GAME_BUTTON_X, wndMgr.GetScreenHeight() - GAME_BUTTON_BOTTOM)

		self.__MakeGameButton()

		self.goStoneButton = ui.Button()
		self.goStoneButton.SetParent(self)
		self.goStoneButton.SetPosition(40, 6)
		self.goStoneButton.SetUpVisual(MIDDLE_BUTTON[0])
		self.goStoneButton.SetOverVisual(MIDDLE_BUTTON[1])
		self.goStoneButton.SetDownVisual(MIDDLE_BUTTON[2])
		self.goStoneButton.SetText(_T("BANNER_WAR_GOTO_STONE"))
		self.goStoneButton.SetToolTipText(_T("BANNER_WAR_GOTO_STONE_TIP"))
		self.goStoneButton.SAFE_SetEvent(self.__OnClickGoStone)
		self.goStoneButton.Hide()

		self.Show()

	def Destroy(self):
		self.__RemoveWaypoint()

		if self.gameButton:
			self.gameButton.Destroy()

		if self.goStoneButton:
			self.goStoneButton.SetEvent(None)

		self.Hide()
		self.gameButton = None
		self.gameButtonEvent = None
		self.goStoneButton = None

	def __MakeGameButton(self):
		self.gameButton = BannerWarGameButton()
		self.gameButton.SetParent(self)
		self.gameButton.SetPosition(0, 0)

		if self.gameButtonEvent:
			self.gameButton.SetEvent(self.gameButtonEvent)

	def SetGameButtonEvent(self, event):
		# Zayif sarmalayici saklanir: buton yeniden olusturulunca ayni olay baglanir, pencereyi hayatta tutmaz.
		self.gameButtonEvent = ui.__mem_func__(event)

		if self.gameButton:
			self.gameButton.SetEvent(self.gameButtonEvent)

	def SetPhase(self, phase, remain):
		self.phase = phase

		# Yanip sonme motorda kapatilamaz: savas/sonuc bitince buton temiz haliyle yeniden olusturulur.
		if self.gameButton and self.gameButton.isFlashing and phase not in (PHASE_ACTIVE, PHASE_RESULT):
			self.gameButton.Destroy()
			self.gameButton = None
			self.__MakeGameButton()

		if self.gameButton:
			self.gameButton.SetState(phase, remain)

		self.__Refresh()

	def SetHere(self, front, stoneX, stoneY):
		self.hereFront = front
		self.stoneX = stoneX
		self.stoneY = stoneY
		self.__Refresh()

		# "Cepheye Git" ile gelen oyuncu: yeni haritaya girer girmez tasa otomatik yurusun.
		if front and self.phase == PHASE_ACTIVE and app.GetTime() - _autoNavRequestedAt[0] < AUTO_NAV_AFTER_WARP_SEC:
			_autoNavRequestedAt[0] = -1000.0
			self.navRetries = 0
			self.__StartNav(False)

	def __CanGoStone(self):
		return self.phase == PHASE_ACTIVE and self.hereFront > 0 and self.stoneX > 0 and self.stoneY > 0

	def __Refresh(self):
		if self.goStoneButton:
			if NAV_ENABLED and self.__CanGoStone():
				self.goStoneButton.Show()
			else:
				self.goStoneButton.Hide()

		if self.__CanGoStone():
			miniMap.AddWayPoint(WAYPOINT_ID, float(self.stoneX), float(self.stoneY),
					_F("BANNER_WAR_WAYPOINT", _EmpireName(self.hereFront)))
			self.waypointShown = True
		else:
			self.__RemoveWaypoint()

	def __RemoveWaypoint(self):
		if self.waypointShown:
			miniMap.RemoveWayPoint(WAYPOINT_ID)
			self.waypointShown = False

	def __OnClickGoStone(self):
		self.navRetries = 0
		self.__StartNav(True)

	def __StartNav(self, manual):
		if not NAV_ENABLED or not self.__CanGoStone() or self.navState != NAV_IDLE:
			return

		self.navManual = manual
		self.navTargetX = float(self.stoneX)
		self.navTargetY = float(self.stoneY)
		result = nav.PreviewToPosition(self.navTargetX, self.navTargetY)

		if result == nav.START_OK:
			self.navState = NAV_WAIT_PREVIEW
			self.navStartedAt = app.GetTime()
			chat.AppendChat(chat.CHAT_TYPE_INFO, _T("BANNER_WAR_NAV_START"))
		elif result == nav.START_FAIL_TOO_CLOSE:
			if manual:
				chat.AppendChat(chat.CHAT_TYPE_INFO, _T("BANNER_WAR_NAV_CLOSE"))
		elif _NavRetryable(result) and self.navRetries < NAV_RETRY_MAX:
			# Isinlanmadan hemen sonra harita/navigasyon verisi hazir olmayabilir: 1 sn sonra tekrar.
			self.navRetries += 1
			self.navState = NAV_WAIT_DATA
			self.navRetryAt = app.GetTime() + NAV_RETRY_SEC
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, _T("BANNER_WAR_NAV_FAIL"))

	def __GetPreviewOwner(self):
		# Beklerken oyuncu atlas'tan kendi (ucretli) rotasini secmis olabilir; yeni on izleme eskisinin yerine gecer.
		# O rota bizim degildir: onaylanmaz / iptal edilmez, karari uiminimap'in kendi onay penceresi verir.
		# PreviewToPosition hedefi aynen saklar (PythonNavigation.cpp: m_kRequestedTarget = kGoal).
		try:
			(hasTarget, targetX, targetY) = nav.GetRequestedTarget()
		except Exception:
			return PREVIEW_OURS

		if not hasTarget:
			return PREVIEW_NONE		# on izleme bitti (rota bulunamadi / iptal)

		if abs(targetX - self.navTargetX) < 1.0 and abs(targetY - self.navTargetY) < 1.0:
			return PREVIEW_OURS

		return PREVIEW_OTHER

	def OnUpdate(self):
		# Button alt sinifinda OnUpdate calismadigi icin geri sayim buradan surulur.
		if self.gameButton:
			self.gameButton.UpdateCountdown()

		if self.navState == NAV_IDLE:
			return

		now = app.GetTime()

		if self.navState == NAV_WAIT_DATA:
			if now >= self.navRetryAt:
				self.navState = NAV_IDLE
				self.__StartNav(self.navManual)
			return

		# NAV_WAIT_PREVIEW: rota hazir olunca onayla. Sunucu tas icin ucret almaz (CheckFreeNav).
		# Olay kuyrugu (nav.PopEvent) uiminimap.py'nindir; burada TUKETILMEZ.
		owner = self.__GetPreviewOwner()

		if owner != PREVIEW_OURS:
			self.navState = NAV_IDLE
			self.navRetries = 0

			if owner == PREVIEW_NONE:
				chat.AppendChat(chat.CHAT_TYPE_INFO, _T("BANNER_WAR_NAV_FAIL"))
			return

		if nav.IsPreviewReady():
			self.navState = NAV_IDLE
			self.navRetries = 0

			if not nav.Confirm():
				chat.AppendChat(chat.CHAT_TYPE_INFO, _T("BANNER_WAR_NAV_FAIL"))
		elif now - self.navStartedAt > NAV_PREVIEW_TIMEOUT:
			self.navState = NAV_IDLE
			nav.CancelPreview()
			chat.AppendChat(chat.CHAT_TYPE_INFO, _T("BANNER_WAR_NAV_FAIL"))


class BannerWarFlagTag(ui.Window):
	# Dusen sancagin (bayrak NPC) ustunde, oyuncu ALT'a basmadan da gorunen: lonca armasi + alt satir
	# (lonca adini C++ isim yazisi bayrak renginde yazar; FLAG_TAG_SHOW_TITLE True ise burada da yazilir).
	# Bayrak ekranda degilse (uzak / kamera arkasi) chr.GetProjectPosition -100 dondurur, yazi gizlenir.

	def __init__(self):
		ui.Window.__init__(self)
		self.markBox = None
		self.titleText = None
		self.subText = None
		self.vid = 0
		self.hasMark = False
		self.isTextShown = True
		self.__Create()

	def __del__(self):
		ui.Window.__del__(self)

	def __Create(self):
		self.AddFlag("not_pick")
		self.SetSize(1, 1)

		# Dikey dizilim (0 = C++ isminin taban noktasi, yukari negatif):
		#   FLAG_TAG_SHOW_TITLE False:  alt satir / (C++: [arma] bayrak adi)   -> konum SetFlag'de (lonca var/yok)
		#   FLAG_TAG_SHOW_TITLE True :  [arma] / buyuk lonca adi / alt satir
		# Olcek her SetIndex'ten sonra _SetGuildMark icinde verilir (burada verilse etkisiz kalir).
		self.markBox = ui.MarkBox()
		self.markBox.SetParent(self)
		self.markBox.SetPosition(-8 * FLAG_TAG_MARK_SCALE, -46 - 12 * FLAG_TAG_MARK_SCALE)
		self.markBox.AddFlag("not_pick")

		self.titleText = ui.TextLine()
		self.titleText.SetParent(self)
		self.titleText.SetFontName(FLAG_TAG_FONT)
		self.titleText.SetPosition(0, -42)
		self.titleText.SetHorizontalAlignCenter()
		self.titleText.SetOutline()
		self.titleText.AddFlag("not_pick")

		self.subText = ui.TextLine()
		self.subText.SetParent(self)
		self.subText.SetPosition(0, -20)
		self.subText.SetHorizontalAlignCenter()
		self.subText.SetOutline()
		self.subText.SetPackedFontColor(COLOR_TITLE)
		self.subText.AddFlag("not_pick")

		self.__ShowText(False)
		self.Show()

	def Destroy(self):
		self.vid = 0
		self.Hide()
		self.markBox = None
		self.titleText = None
		self.subText = None

	def SetFlag(self, vid, taker, guildName, guildID):
		self.vid = vid

		if not vid or not self.titleText:
			self.__ShowText(False)
			return

		if _HasName(guildName):
			self.titleText.SetText(guildName)
		else:
			self.titleText.SetText(_F("BANNER_WAR_FLAG_EMPIRE", _EmpireName(taker)))

		self.titleText.SetPackedFontColor(_EmpireColor(taker))
		self.subText.SetText(_F("BANNER_WAR_FLAG_SUB", _EmpireName(taker)))

		if FLAG_TAG_SHOW_TITLE:
			# Arma, yazi gorunurken gosterilir (__ShowText); burada sadece hazirlanir.
			self.hasMark = _SetGuildMark(self.markBox, guildID, FLAG_TAG_MARK_SCALE)
		else:
			# Arma C++ isim satirinda. Loncali bayrakta isim, ana ismin FLAG_GUILD_LINE_OFFSET ustundeki satirdadir.
			self.hasMark = False
			nameTop = FLAG_NAME_HEIGHT_PX + (FLAG_GUILD_LINE_OFFSET if guildID > 0 else 0)
			self.subText.SetPosition(0, -(nameTop + 4 + 13))

		if not self.isTextShown:
			self.markBox.Hide()

	def __ShowText(self, show):
		if show == self.isTextShown or not self.titleText:
			return

		self.isTextShown = show

		for widget in (self.titleText, self.subText):
			if show and (widget is not self.titleText or FLAG_TAG_SHOW_TITLE):
				widget.Show()
			else:
				widget.Hide()

		if show and self.hasMark:
			self.markBox.Show()
		else:
			self.markBox.Hide()

	def OnUpdate(self):
		if not self.vid:
			return

		(x, y) = chr.GetProjectPosition(self.vid, FLAG_TAG_HEIGHT)

		if x == -100 and y == -100:
			self.__ShowText(False)
			return

		self.SetPosition(x, y)
		self.__ShowText(True)


class BannerWarWindow(ui.BoardWithTitleBar):

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def __Initialize(self):
		# widgets
		self.hud = None
		self.flagTag = None
		self.statusText = None
		self.subText = None
		self.cards = {}
		self.tabButtons = []
		self.pages = []
		self.refreshButton = None
		self.rankRows = [[], []]
		self.rankEmpty = [None, None]
		self.logRows = []
		self.logEmpty = None
		self.helpRows = []
		self.footMe = None
		self.footGuild = None
		self.footWar = None
		# SetParent Python referansi tutmaz: sabit (dekor) parcalar burada yasar, yoksa silinirler.
		self.keep = []

		# state
		self.isActive = False
		self.remainSec = -1
		self.remainBase = 0.0
		self.lastShownSec = -2
		self.warChannel = 1
		self.nextWeekDay = -1
		self.nextHour = 0
		self.nextMinute = 0
		self.onWarChannel = False
		self.rules = (1, 5, 3, 5, 5, 50, 40, 5, 45)
		self.slots = []
		self.fronts = {}
		self.ranks = [[], []]
		self.myScore = 0
		self.logLines = []
		self.curTab = TAB_PLAYER
		self.tabAutoChosen = False
		self.nextAutoRefresh = 0.0
		self.lastAutoRequest = -100.0
		self.manualRequestAt = -100.0

	def __LoadWindow(self):
		self.SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.SetTitleName(_T("BANNER_WAR_TITLE"))
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.AddFlag("movable")
		self.AddFlag("float")

		self.__MakeStatus()

		for empire in (1, 2, 3):
			self.__MakeFrontCard(empire)

		self.__MakeTabs()
		self.__MakeContent()
		self.__MakeFooter()

		# ekrandaki buton grubu (Sancak Savasi + Tasa Git) ve bayrak ustu lonca yazisi (ust seviye pencereler)
		self.hud = BannerWarHud()
		self.hud.SetGameButtonEvent(self.__OnClickGameButton)
		self.flagTag = BannerWarFlagTag()

		for empire in (1, 2, 3):
			self.__RefreshFront(empire)

		self.__RefreshStatus(0)
		self.__RefreshRank()
		self.__RefreshLog()
		self.__RefreshHelp()
		self.__SetFooter(0, 0, 0, 0, 0, 0, 0)
		self.__SelectTab(TAB_PLAYER)

		self.SetCenterPosition()
		self.Hide()

	# ------------------------------------------------------------ yapim yardimcilari

	def __MakeText(self, parent, x, y, color, align = ALIGN_LEFT, outline = True):
		text = ui.TextLine()
		text.SetParent(parent)
		text.SetPosition(x, y)

		if align == ALIGN_CENTER:
			text.SetHorizontalAlignCenter()
		elif align == ALIGN_RIGHT:
			text.SetHorizontalAlignRight()

		text.SetPackedFontColor(color)

		if outline:
			text.SetOutline()

		text.AddFlag("not_pick")
		text.Show()
		return text

	def __MakeLabel(self, parent, x, y, key, color = COLOR_LABEL, align = ALIGN_LEFT, outline = True):
		text = self.__MakeText(parent, x, y, color, align, outline)
		text.SetText(_T(key))
		self.keep.append(text)
		return text

	def __MakeSlot(self, parent, x, y, width):
		# Orijinal gomuk deger kutusu (ui.SlotBar = wndMgr Bar3D), Lonca > Uyeler listesindeki hucreler.
		slot = ui.SlotBar()
		slot.SetParent(parent)
		slot.SetPosition(x, y)
		slot.SetSize(width, ROW_HEIGHT)
		slot.AddFlag("not_pick")
		slot.Show()
		self.keep.append(slot)
		return slot

	def __MakeSlotText(self, slot, color, left = -1):
		# left < 0: hucrede ortali (ui.MakeTextLine ile ayni hizalama), aksi halde soldan 'left' px.
		text = ui.TextLine()
		text.SetParent(slot)

		if left < 0:
			text.SetWindowHorizontalAlignCenter()
			text.SetHorizontalAlignCenter()
			text.SetPosition(0, 0)
		else:
			text.SetPosition(left, 0)

		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()
		text.SetPackedFontColor(color)
		text.AddFlag("not_pick")
		text.Show()
		return text

	def __MakeMark(self, slot):
		mark = ui.MarkBox()
		mark.SetParent(slot)
		mark.SetPosition(4, (ROW_HEIGHT - 12) // 2)
		mark.AddFlag("not_pick")
		mark.Hide()
		return mark

	def __MakeBar(self, parent, x, y, width):
		bar = ui.HorizontalBar()
		bar.SetParent(parent)
		bar.Create(width)
		bar.SetPosition(x, y)
		bar.AddFlag("not_pick")
		bar.Show()
		self.keep.append(bar)
		return bar

	def __MakeButton(self, parent, x, y, label, visuals):
		button = ui.Button()
		button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(visuals[0])
		button.SetOverVisual(visuals[1])
		button.SetDownVisual(visuals[2])
		button.SetText(label)
		button.Show()
		return button

	def __MakeFlagImage(self, parent, empire, x, y, boxWidth, boxHeight):
		# Karakter secim ekranindaki bayrak resmi, kutuya orani bozulmadan sigdirilir.
		image = ui.ExpandedImageBox()
		image.SetParent(parent)
		image.AddFlag("not_pick")
		image.LoadImage(EMPIRE_FLAG[empire])
		self.keep.append(image)

		width = image.GetWidth()
		height = image.GetHeight()

		if width <= 0 or height <= 0:
			image.Hide()
			return

		scale = min(float(boxWidth) / width, float(boxHeight) / height)
		image.SetScale(scale, scale)
		image.SetPosition(x + int((boxWidth - width * scale) / 2), y + int((boxHeight - height * scale) / 2))
		image.Show()

	def __MakeHeader(self, page, columns):
		# Tablo basligi: orijinal HorizontalBar uzerinde sutun adlari.
		self.__MakeBar(page, 6, 6, CONTENT_WIDTH - 12)

		for x, align, key in columns:
			self.__MakeLabel(page, x, 8, key, COLOR_TITLE, align)

	# ------------------------------------------------------------ yapim

	def __MakeStatus(self):
		board = ui.ThinBoard()
		board.SetParent(self)
		board.SetPosition(CONTENT_X, STATUS_Y)
		board.SetSize(CONTENT_WIDTH, STATUS_HEIGHT)
		board.Show()
		self.keep.append(board)

		self.statusText = self.__MakeText(board, CONTENT_WIDTH // 2, 6, COLOR_GOLD, ALIGN_CENTER)
		self.statusText.SetFontName(getattr(localeInfo, "UI_DEF_FONT_LARGE", "Tahoma:14"))
		self.subText = self.__MakeText(board, CONTENT_WIDTH // 2, 25, COLOR_NORMAL, ALIGN_CENTER)

	def __MakeFrontCard(self, empire):
		card = ui.ThinBoard()
		card.SetParent(self)
		card.SetPosition(CONTENT_X + (empire - 1) * (CARD_WIDTH + CARD_GAP), CARD_Y)
		card.SetSize(CARD_WIDTH, CARD_HEIGHT)
		card.Show()
		self.keep.append(card)

		# baslik: "Kirmizi Sancak"
		self.__MakeBar(card, 5, 5, CARD_WIDTH - 10)
		title = self.__MakeText(card, CARD_WIDTH // 2, 7, _EmpireColor(empire), ALIGN_CENTER)
		title.SetText(_F("BANNER_WAR_FRONT_NAME", _EmpireName(empire)))
		self.keep.append(title)

		# bayrak resmi | durum + tas cani
		self.__MakeFlagImage(card, empire, 8, 28, 44, 34)

		widgets = {}
		widgets["state"] = self.__MakeText(card, 58, 28, COLOR_NORMAL)

		gauge = ui.Gauge()
		gauge.SetParent(card)
		gauge.MakeGauge(76, "red")
		gauge.SetPosition(58, 48)
		gauge.AddFlag("not_pick")
		gauge.Show()
		widgets["gauge"] = gauge
		widgets["hp"] = self.__MakeText(card, CARD_WIDTH - 6, 44, COLOR_TITLE, ALIGN_RIGHT)

		# Cephede: [kirmizi] [sari] [mavi]  (tasin yanindaki oyuncu sayisi)
		self.__MakeLabel(card, 8, 70, "BANNER_WAR_ROW_NEAR")
		near = []

		for index in xrange(3):
			slot = self.__MakeSlot(card, 62 + index * 38, 68, 32)
			near.append(self.__MakeSlotText(slot, _EmpireColor(index + 1)))

		widgets["near"] = near

		# Fatih / Muhafiz: [arma] lonca
		widgets["guildLabel"] = self.__MakeText(card, 8, 92, COLOR_LABEL)
		slot = self.__MakeSlot(card, 62, 90, 108)
		widgets["mark"] = self.__MakeMark(slot)
		widgets["guild"] = self.__MakeSlotText(slot, COLOR_NORMAL, TEXT_PAD)

		# Bonus: +%5 drop / Intikam +%50
		self.__MakeLabel(card, 8, 114, "BANNER_WAR_ROW_BONUS")
		slot = self.__MakeSlot(card, 62, 112, 108)
		widgets["bonus"] = self.__MakeSlotText(slot, COLOR_MUTED)

		# Cepheye Git (savas yokken yerinde kisa bir not)
		button = self.__MakeButton(card, (CARD_WIDTH - 88) // 2, 134, _T("BANNER_WAR_GO"), LARGE_BUTTON)
		button.SetToolTipText(_T("BANNER_WAR_GO_TIP"))
		button.SAFE_SetEvent(self.__OnClickGo, empire)
		button.Hide()
		widgets["go"] = button
		widgets["goHint"] = self.__MakeText(card, CARD_WIDTH // 2, 138, COLOR_MUTED, ALIGN_CENTER)

		self.cards[empire] = widgets

	def __MakeTabs(self):
		keys = ("BANNER_WAR_TAB_PLAYER", "BANNER_WAR_TAB_GUILD", "BANNER_WAR_TAB_LOG", "BANNER_WAR_TAB_HELP")
		x = CONTENT_X

		for index in xrange(TAB_COUNT):
			button = ui.RadioButton()
			button.SetParent(self)
			button.SetUpVisual(LARGE_BUTTON[0])
			button.SetOverVisual(LARGE_BUTTON[1])
			button.SetDownVisual(LARGE_BUTTON[2])
			button.SetPosition(x, TAB_Y)
			button.SetText(_T(keys[index]))
			button.SAFE_SetEvent(self.__OnClickTab, index)
			button.Show()
			self.tabButtons.append(button)
			x += max(88, button.GetWidth()) + TAB_GAP

		self.refreshButton = self.__MakeButton(self, WINDOW_WIDTH - CONTENT_X - 61, TAB_Y, _T("BANNER_WAR_REFRESH"), MIDDLE_BUTTON)
		self.refreshButton.SetToolTipText(_T("BANNER_WAR_REFRESH_TIP"))
		self.refreshButton.SAFE_SetEvent(self.__OnClickRefresh)

	def __MakeContent(self):
		board = ui.ThinBoard()
		board.SetParent(self)
		board.SetPosition(CONTENT_X, CONTENT_Y)
		board.SetSize(CONTENT_WIDTH, CONTENT_HEIGHT)
		board.Show()
		self.keep.append(board)

		for index in xrange(TAB_COUNT):
			page = ui.Window()
			page.SetParent(board)
			page.SetPosition(0, 0)
			page.SetSize(CONTENT_WIDTH, CONTENT_HEIGHT)
			page.AddFlag("not_pick")
			page.Hide()
			self.pages.append(page)

		self.__MakeRankPage(RANK_TYPE_PLAYER, self.pages[TAB_PLAYER])
		self.__MakeRankPage(RANK_TYPE_GUILD, self.pages[TAB_GUILD])
		self.__MakeLogPage(self.pages[TAB_LOG])
		self.__MakeHelpPage(self.pages[TAB_HELP])

	def __MakeRankPage(self, rankType, page):
		keys = ("BANNER_WAR_COL_POS",
				"BANNER_WAR_COL_NAME" if rankType == RANK_TYPE_PLAYER else "BANNER_WAR_COL_GUILD",
				"BANNER_WAR_COL_EMPIRE", "BANNER_WAR_COL_SCORE", "BANNER_WAR_COL_KILLS", "BANNER_WAR_COL_STONES")
		header = []

		for column in xrange(len(RANK_COLUMNS)):
			x, width = RANK_COLUMNS[column]

			if column == COL_NAME:
				header.append((x + TEXT_PAD, ALIGN_LEFT, keys[column]))
			else:
				header.append((x + width // 2, ALIGN_CENTER, keys[column]))

		self.__MakeHeader(page, header)

		nameLeft = MARK_PAD if rankType == RANK_TYPE_GUILD else TEXT_PAD

		for row in xrange(RANK_ROWS):
			y = FIRST_ROW_Y + row * ROW_STEP
			slots = [self.__MakeSlot(page, x, y, width) for (x, width) in RANK_COLUMNS]

			cells = {"slots" : slots}
			cells["pos"] = self.__MakeSlotText(slots[0], COLOR_NORMAL)
			cells["mark"] = self.__MakeMark(slots[1]) if rankType == RANK_TYPE_GUILD else None
			cells["name"] = self.__MakeSlotText(slots[1], COLOR_NORMAL, nameLeft)
			cells["empire"] = self.__MakeSlotText(slots[2], COLOR_NORMAL)
			cells["score"] = self.__MakeSlotText(slots[3], COLOR_TITLE)
			cells["kills"] = self.__MakeSlotText(slots[4], COLOR_NORMAL)
			cells["stones"] = self.__MakeSlotText(slots[5], COLOR_NORMAL)
			self.rankRows[rankType].append(cells)

		self.rankEmpty[rankType] = self.__MakeLabel(page, CONTENT_WIDTH // 2, 110, "BANNER_WAR_RANK_EMPTY", COLOR_MUTED, ALIGN_CENTER)

	def __MakeLogPage(self, page):
		self.__MakeHeader(page, (
			(LOG_COLUMNS[0][0] + LOG_COLUMNS[0][1] // 2, ALIGN_CENTER, "BANNER_WAR_COL_TIME"),
			(LOG_COLUMNS[1][0] + TEXT_PAD, ALIGN_LEFT, "BANNER_WAR_COL_EVENT"),
		))

		for line in xrange(LOG_LINES):
			y = FIRST_ROW_Y + line * ROW_STEP
			timeSlot = self.__MakeSlot(page, LOG_COLUMNS[0][0], y, LOG_COLUMNS[0][1])
			textSlot = self.__MakeSlot(page, LOG_COLUMNS[1][0], y, LOG_COLUMNS[1][1])
			self.logRows.append((timeSlot, textSlot, self.__MakeSlotText(timeSlot, COLOR_GOLD), self.__MakeSlotText(textSlot, COLOR_NORMAL, TEXT_PAD)))

		self.logEmpty = self.__MakeLabel(page, CONTENT_WIDTH // 2, 110, "BANNER_WAR_LOG_EMPTY", COLOR_MUTED, ALIGN_CENTER)

	def __MakeHelpPage(self, page):
		self.__MakeHeader(page, ((CONTENT_WIDTH // 2, ALIGN_CENTER, "BANNER_WAR_HELP_TITLE"),))

		for line in xrange(HELP_LINES):
			y = FIRST_ROW_Y + line * HELP_ROW_STEP
			key = self.__MakeText(page, 14, y, COLOR_GOLD)
			body = self.__MakeText(page, 104, y, COLOR_NORMAL)
			self.helpRows.append((key, body))

	def __MakeFooter(self):
		# Orijinal "etiket + deger kutusu" dizilimi (Lonca > Bilgi sayfasi): etiket kutunun soluna sagdan dayali.
		values = []

		for x, width, key in ((88, 112, "BANNER_WAR_FOOT_ME"), (262, 114, "BANNER_WAR_FOOT_GUILD"), (446, 104, "BANNER_WAR_FOOT_WAR")):
			self.__MakeLabel(self, x - 6, FOOTER_Y + 2, key, COLOR_LABEL, ALIGN_RIGHT, False)
			values.append(self.__MakeSlotText(self.__MakeSlot(self, x, FOOTER_Y, width), COLOR_TITLE))

		self.footMe, self.footGuild, self.footWar = values

	# ------------------------------------------------------------ yasam dongusu

	def Destroy(self):
		# Bu client'ta ui.WindowDestroy dekoratoru yok; temizlik elle yapilir.
		self.Hide()

		if self.hud:
			self.hud.Destroy()

		if self.flagTag:
			self.flagTag.Destroy()

		if self.refreshButton:
			self.refreshButton.SetEvent(None)

		for button in self.tabButtons:
			if button:
				button.SetEvent(None)

		for widgets in self.cards.values():
			if widgets.get("go"):
				widgets["go"].SetEvent(None)

		self.SetCloseEvent(None)
		self.__Initialize()

	def GetServerCommands(self):
		# game.py __ServerCommand_Build bu sozlugu serverCommandList'e ekler.
		# (stringCommander zayif referans tutar; pencere Destroy olunca komutlar sessizce duser.)
		return {
			"BW_Info"		: self.SetInfo,
			"BW_Rules"		: self.SetRules,
			"BW_SlotClear"	: self.ClearSlots,
			"BW_Slot"		: self.AddSlot,
			"BW_Front"		: self.SetFront,
			"BW_RankClear"	: self.ClearRank,
			"BW_Rank"		: self.AddRank,
			"BW_Me"			: self.SetMe,
			"BW_MyWar"		: self.SetMyWar,
			"BW_Button"		: self.SetButtonState,
			"BW_Here"		: self.SetHere,
			"BW_Open"		: self.OnServerOpen,
		}

	def Open(self):
		if not self.IsShow():
			self.SetCenterPosition()

		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		now = app.GetTime()

		if self.remainSec >= 0:
			sec = max(0, int(self.remainSec - (now - self.remainBase)))

			if sec != self.lastShownSec:
				self.lastShownSec = sec
				self.__RefreshStatus(sec)

			# Savas basladiginda / bittiginde pencere kendini yeniler.
			if sec == 0 and now >= self.nextAutoRefresh:
				self.__RequestAuto(now, FLIP_REFRESH_SEC)
				return

		# Savas surerken acik pencere 15 sn'de bir guncellenir (can yuzdesi, cephedekiler, canli siralama).
		if self.isActive and now >= self.nextAutoRefresh:
			self.__RequestAuto(now, AUTO_REFRESH_SEC)

	def __RequestAuto(self, now, interval):
		self.nextAutoRefresh = now + interval
		self.lastAutoRequest = now
		net.SendChatPacket("/sancak durum")

	# ------------------------------------------------------------ butonlar

	def __OnClickGameButton(self):
		if self.IsShow():
			self.Close()
			return

		self.manualRequestAt = app.GetTime()
		net.SendChatPacket("/sancak")

	def __OnClickRefresh(self):
		net.SendChatPacket("/sancak")

	def __OnClickGo(self, empire):
		# Isinlanip yeni haritaya girince tasa otomatik yurusun (dusman cephesi: toplanma noktasindan).
		_autoNavRequestedAt[0] = app.GetTime()
		net.SendChatPacket("/sancak git %d" % empire)

	def __OnClickTab(self, index):
		self.__SelectTab(index)

	def __SelectTab(self, index):
		if index < 0 or index >= TAB_COUNT:
			return

		self.curTab = index

		for tab in xrange(len(self.tabButtons)):
			if tab == index:
				self.tabButtons[tab].Down()
			else:
				self.tabButtons[tab].SetUp()

		for tab in xrange(len(self.pages)):
			if tab == index:
				self.pages[tab].Show()
			else:
				self.pages[tab].Hide()

		if index == TAB_HELP:
			self.__RefreshHelp()

	# ------------------------------------------------------------ sunucudan gelenler (BW_*)
	# Yeni alanlar komutlarin SONUNA eklenir: stringCommander fazla argumani yok sayar,
	# eksik argumanda hata verir. Bu yuzden once sunucu, sonra client guncellenebilir.

	def SetButtonState(self, phase, remain):
		if self.hud:
			self.hud.SetPhase(_ToInt(phase), _ToInt(remain))

	def SetHere(self, front, stoneX, stoneY, flagVid, flagTaker, flagGuild, flagGuildID):
		# Her giriste / isinlanmada ve bayrak degisince: bu haritadaki tas ve bayrak.
		if self.hud:
			self.hud.SetHere(_ToInt(front), _ToInt(stoneX), _ToInt(stoneY))

		if self.flagTag:
			self.flagTag.SetFlag(_ToInt(flagVid), _ToInt(flagTaker), flagGuild, _ToInt(flagGuildID))

	def SetInfo(self, active, remain, warChannel, weekDay, hour, minute, onWarChannel):
		self.isActive = (_ToInt(active) == 1)
		self.remainSec = _ToInt(remain, -1)
		self.remainBase = app.GetTime()
		self.lastShownSec = -2
		self.warChannel = _ToInt(warChannel, 1)
		self.nextWeekDay = _ToInt(weekDay, -1)
		self.nextHour = _ToInt(hour)
		self.nextMinute = _ToInt(minute)
		self.onWarChannel = (_ToInt(onWarChannel) == 1)

		if self.isActive and self.nextAutoRefresh < app.GetTime():
			self.nextAutoRefresh = app.GetTime() + AUTO_REFRESH_SEC

		for empire in (1, 2, 3):
			self.__RefreshFront(empire)

		self.__RefreshStatus(max(0, self.remainSec))

	def SetRules(self, kill, capture, defend, bonusDefend, bonusCapture, revengePct, minLevel, minFallMin, durationMin):
		self.rules = (_ToInt(kill), _ToInt(capture), _ToInt(defend), _ToInt(bonusDefend), _ToInt(bonusCapture),
				_ToInt(revengePct), _ToInt(minLevel), _ToInt(minFallMin), _ToInt(durationMin))

	def ClearSlots(self):
		self.slots = []

	def AddSlot(self, weekDay, hour, minute):
		if len(self.slots) < 14:
			self.slots.append((_ToInt(weekDay), _ToInt(hour), _ToInt(minute)))

	def SetFront(self, empire, state, hp, taker, bonus, revenge, nearRed, nearYellow, nearBlue, guildName, guildID):
		empire = _ToInt(empire)

		if empire not in self.cards:
			return

		self.fronts[empire] = {
			"state"		: _ToInt(state),
			"hp"		: max(0, min(100, _ToInt(hp))),
			"taker"		: _ToInt(taker),
			"bonus"		: _ToInt(bonus),
			"revenge"	: _ToInt(revenge) == 1,
			"near"		: (_ToInt(nearRed), _ToInt(nearYellow), _ToInt(nearBlue)),
			"guildName"	: guildName,
			"guildID"	: _ToInt(guildID),
		}

		self.__RefreshFront(empire)

	def ClearRank(self):
		self.ranks = [[], []]

	def AddRank(self, rankType, pos, name, empire, score, kills, guildID, stones):
		rankType = _ToInt(rankType, -1)

		if rankType not in (RANK_TYPE_PLAYER, RANK_TYPE_GUILD):
			return

		if len(self.ranks[rankType]) >= RANK_ROWS:
			return

		self.ranks[rankType].append((_ToInt(pos), name, _ToInt(empire), _ToInt(score), _ToInt(kills), _ToInt(guildID), _ToInt(stones)))

	def SetMe(self, score, rank, guildScore, guildRank, hasGuild, loadLimit):
		self.myScore = _ToInt(score)
		self.__SetFooter(self.myScore, _ToInt(rank), _ToInt(guildScore), _ToInt(guildRank), _ToInt(hasGuild), -1, -1)

	def SetMyWar(self, score, kills):
		self.__SetFooter(None, None, None, None, None, _ToInt(score), _ToInt(kills))

	def OnServerOpen(self):
		self.__RefreshRank()

		if self.curTab == TAB_HELP:
			self.__RefreshHelp()

		# Acik pencere sadece yenilenir; one firlamaz (savas sirasindaki otomatik yenileme).
		if self.IsShow():
			return

		# Arka plandaki otomatik yenilemenin cevabi, az once kapatilan pencereyi tekrar acmasin.
		# Oyuncu butona yeni bastiysa (manualRequestAt) bu engel uygulanmaz.
		now = app.GetTime()

		if now - self.manualRequestAt > MANUAL_OPEN_SEC and now - self.lastAutoRequest < 3.0:
			return

		self.manualRequestAt = -100.0

		# Ilk acilista, henuz hic Zafer Puani olmayan oyuncuya once "Nasil Oynanir?" sekmesi gosterilir.
		if not self.tabAutoChosen:
			self.tabAutoChosen = True

			if self.myScore <= 0:
				self.__SelectTab(TAB_HELP)

		self.Open()

	def OnNotice(self, message):
		# game.py'den: her duyuru buraya da gelir; sadece Sancak Savasi duyurulari gunluge yazilir.
		if not message or not message.startswith(NOTICE_PREFIX):
			return

		pos = message.find("]")
		text = message[pos + 1:].strip() if pos >= 0 else message

		text = text[:LOG_MAX_CHARS]

		# Satir, hucreye piksel olarak sigacak kadar kisaltilir (olcum icin ilk satirin yazisi kullanilir;
		# __RefreshLog hemen ardindan dogru metni yazar).
		if self.logRows:
			text = self.__FitText(self.logRows[0][3], text, LOG_TEXT_WIDTH)

		self.logLines.insert(0, (_Clock(), text))
		del self.logLines[LOG_LINES:]

		self.__RefreshLog()

	def __FitText(self, textLine, text, maxWidth):
		# SetText metni hemen olcer (CTextLine::OnSetText -> Update); uiToolTip de ayni sekilde GetTextSize kullanir.
		textLine.SetText(text)

		if textLine.GetTextSize()[0] <= maxWidth:
			return text

		low, high = 0, len(text)

		while low < high:
			middle = (low + high + 1) // 2
			textLine.SetText(text[:middle].rstrip() + "...")

			if textLine.GetTextSize()[0] <= maxWidth:
				low = middle
			else:
				high = middle - 1

		return text[:low].rstrip() + "..."

	# ------------------------------------------------------------ cizim

	def __RefreshStatus(self, sec):
		if not self.statusText or not self.subText:
			return

		if self.isActive:
			self.statusText.SetText(_F("BANNER_WAR_STATUS_ACTIVE", _FormatTime(sec)))
			self.statusText.SetPackedFontColor(COLOR_ALERT)

			if self.onWarChannel:
				self.subText.SetText(_T("BANNER_WAR_SUB_ACTIVE"))
				self.subText.SetPackedFontColor(COLOR_NORMAL)
			else:
				self.subText.SetText(_F("BANNER_WAR_SUB_WRONG_CH", self.warChannel))
				self.subText.SetPackedFontColor(COLOR_NEGATIVE)
			return

		self.statusText.SetPackedFontColor(COLOR_GOLD)
		self.subText.SetPackedFontColor(COLOR_NORMAL)

		if 0 <= self.nextWeekDay <= 6 and self.remainSec >= 0:
			dayName = _T("BANNER_WAR_DAY_%d" % self.nextWeekDay)
			self.statusText.SetText(_F("BANNER_WAR_STATUS_NEXT", dayName, self.nextHour, self.nextMinute, _FormatTime(sec)))
			self.subText.SetText(_F("BANNER_WAR_SUB_WHERE", self.warChannel))
		else:
			self.statusText.SetText(_T("BANNER_WAR_STATUS_NONE"))
			self.subText.SetText("")

	def __RefreshFront(self, empire):
		widgets = self.cards.get(empire)

		if not widgets:
			return

		front = self.fronts.get(empire)
		state = front["state"] if front else FRONT_NONE
		hp = front["hp"] if front else 0
		taker = front["taker"] if front else 0
		guildName = front["guildName"] if front else "-"
		guildID = front["guildID"] if front else 0

		# --- durum + can
		stateText = widgets["state"]
		hpText = widgets["hp"]

		if state == FRONT_ALIVE:
			stateText.SetText(_T("BANNER_WAR_ST_ALIVE"))
			stateText.SetPackedFontColor(COLOR_WHITE if hp > 25 else COLOR_NEGATIVE)
		elif state == FRONT_FALLEN:
			stateText.SetText(_T("BANNER_WAR_ST_FALLEN"))
			stateText.SetPackedFontColor(COLOR_NEGATIVE)
			hp = 0
		elif state == FRONT_DEFENDED:
			stateText.SetText(_T("BANNER_WAR_ST_DEFENDED"))
			stateText.SetPackedFontColor(COLOR_POSITIVE)
		elif self.isActive:
			stateText.SetText(_T("BANNER_WAR_ST_CLOSED"))
			stateText.SetPackedFontColor(COLOR_MUTED)
		else:
			stateText.SetText(_T("BANNER_WAR_ST_WAIT"))
			stateText.SetPackedFontColor(COLOR_MUTED)

		widgets["gauge"].SetPercentage(hp, 100)

		if state == FRONT_NONE:
			hpText.SetText("-")
			hpText.SetPackedFontColor(COLOR_MUTED)
		else:
			hpText.SetText(_F("BANNER_WAR_HP_PCT", hp))
			hpText.SetPackedFontColor(COLOR_TITLE)

		# --- cephedekiler (sadece savas surerken, tas ayaktayken anlamli)
		showNear = self.isActive and state == FRONT_ALIVE

		for index in xrange(3):
			if showNear:
				widgets["near"][index].SetText(str(front["near"][index]))
			else:
				widgets["near"][index].SetText("-")

		# --- fatih / muhafiz lonca
		label = widgets["guildLabel"]
		guildText = widgets["guild"]
		hasGuild = _HasName(guildName)

		if state == FRONT_DEFENDED:
			label.SetText(_T("BANNER_WAR_ROW_GUARD"))
		else:
			label.SetText(_T("BANNER_WAR_ROW_TAKER"))

		hasMark = False

		if state in (FRONT_FALLEN, FRONT_DEFENDED) and hasGuild:
			hasMark = _SetGuildMark(widgets["mark"], guildID)
			guildText.SetText(guildName)
			guildText.SetPackedFontColor(_EmpireColor(taker) if state == FRONT_FALLEN else COLOR_POSITIVE)
		elif state == FRONT_FALLEN:
			widgets["mark"].Hide()
			guildText.SetText(_F("BANNER_WAR_FLAG_EMPIRE", _EmpireName(taker)))
			guildText.SetPackedFontColor(_EmpireColor(taker))
		else:
			widgets["mark"].Hide()
			guildText.SetText("-")
			guildText.SetPackedFontColor(COLOR_MUTED)

		guildText.SetPosition(MARK_PAD if hasMark else TEXT_PAD, 0)

		# --- bonus / intikam
		bonusText = widgets["bonus"]

		if front and front["revenge"]:
			bonusText.SetText(_F("BANNER_WAR_REVENGE", self.rules[5]))
			bonusText.SetPackedFontColor(COLOR_NEGATIVE)
		elif front and front["bonus"] > 0:
			bonusText.SetText(_F("BANNER_WAR_BONUS", front["bonus"]))
			bonusText.SetPackedFontColor(COLOR_POSITIVE)
		else:
			bonusText.SetText(_T("BANNER_WAR_NO_BONUS"))
			bonusText.SetPackedFontColor(COLOR_MUTED)

		# --- Cepheye Git / not
		if self.isActive:
			widgets["go"].Show()
			widgets["goHint"].SetText("")
		else:
			widgets["go"].Hide()
			widgets["goHint"].SetText(_T("BANNER_WAR_GO_WAIT"))

	def __RefreshRank(self):
		myName = player.GetName()

		try:
			myGuildID = guild.GetGuildID()
		except Exception:
			myGuildID = 0

		for rankType in (RANK_TYPE_PLAYER, RANK_TYPE_GUILD):
			rows = self.ranks[rankType]
			hasRows = len(rows) > 0

			if self.rankEmpty[rankType]:
				if hasRows:
					self.rankEmpty[rankType].Hide()
				else:
					self.rankEmpty[rankType].Show()

			for index in xrange(len(self.rankRows[rankType])):
				cells = self.rankRows[rankType][index]

				# Hic veri yoksa bos tablo yerine tek satirlik "Henuz kimse yok" gorunur.
				for slot in cells["slots"]:
					if hasRows:
						slot.Show()
					else:
						slot.Hide()

				if index >= len(rows):
					for key in ("pos", "name", "empire", "score", "kills", "stones"):
						cells[key].SetText("")

					if cells["mark"]:
						cells["mark"].Hide()
					continue

				pos, name, empire, score, kills, guildID, stones = rows[index]

				if rankType == RANK_TYPE_PLAYER:
					isMine = (name == myName)
				else:
					isMine = (myGuildID > 0 and guildID == myGuildID)

				cells["pos"].SetText(str(pos))
				cells["pos"].SetPackedFontColor(RANK_POS_COLOR.get(pos, COLOR_NORMAL))

				cells["name"].SetText(name)
				cells["name"].SetPackedFontColor(COLOR_GOLD if isMine else COLOR_NORMAL)

				if cells["mark"]:
					hasMark = _SetGuildMark(cells["mark"], guildID)
					cells["name"].SetPosition(MARK_PAD if hasMark else TEXT_PAD, 0)

				cells["empire"].SetText(_EmpireName(empire))
				cells["empire"].SetPackedFontColor(_EmpireColor(empire))
				cells["score"].SetText(str(score))
				cells["kills"].SetText(str(kills))
				cells["stones"].SetText(str(stones))

	def __RefreshLog(self):
		hasLines = len(self.logLines) > 0

		for index in xrange(len(self.logRows)):
			timeSlot, textSlot, timeText, text = self.logRows[index]

			if hasLines:
				timeSlot.Show()
				textSlot.Show()
			else:
				timeSlot.Hide()
				textSlot.Hide()

			if index < len(self.logLines):
				clock, message = self.logLines[index]
				timeText.SetText(clock)
				text.SetText(message)
				text.SetPackedFontColor(COLOR_WHITE if index == 0 else COLOR_NORMAL)
			else:
				timeText.SetText("")
				text.SetText("")

		if self.logEmpty:
			if hasLines:
				self.logEmpty.Hide()
			else:
				self.logEmpty.Show()

	def __RefreshHelp(self):
		kill, capture, defend, bonusDefend, bonusCapture, revengePct, minLevel, minFallMin, durationMin = self.rules

		slotNames = []

		for weekDay, hour, minute in self.slots:
			slotNames.append("%s %02d:%02d" % (_T("BANNER_WAR_DAY_%d" % weekDay), hour, minute))

		bodies = (
			_F("BANNER_WAR_HELP_1", ", ".join(slotNames) or "-", durationMin, self.warChannel),
			_T("BANNER_WAR_HELP_2"),
			_T("BANNER_WAR_HELP_3"),
			_F("BANNER_WAR_HELP_4", minLevel),
			_T("BANNER_WAR_HELP_5"),
			_F("BANNER_WAR_HELP_6", minFallMin),
			_T("BANNER_WAR_HELP_7"),
			_F("BANNER_WAR_HELP_8", bonusDefend, bonusCapture),
			_F("BANNER_WAR_HELP_9", revengePct),
			_F("BANNER_WAR_HELP_10", kill, capture, defend),
			_T("BANNER_WAR_HELP_11"),
		)

		for index in xrange(len(self.helpRows)):
			key, body = self.helpRows[index]

			if index < len(bodies):
				key.SetText(_T("BANNER_WAR_HELP_KEY_%d" % (index + 1)))
				body.SetText(bodies[index])
			else:
				key.SetText("")
				body.SetText("")

	def __SetFooter(self, score, rank, guildScore, guildRank, hasGuild, warScore, warKills):
		# None = o kutuya dokunma (BW_Me ve BW_MyWar ayri gelir).
		if score is not None and self.footMe:
			if rank > 0:
				self.footMe.SetText(_F("BANNER_WAR_VAL_RANK", score, rank))
				self.footMe.SetPackedFontColor(COLOR_GOLD)
			else:
				self.footMe.SetText(_T("BANNER_WAR_VAL_NONE"))
				self.footMe.SetPackedFontColor(COLOR_MUTED)

		if guildScore is not None and self.footGuild:
			if hasGuild != 1:
				self.footGuild.SetText(_T("BANNER_WAR_VAL_NO_GUILD"))
				self.footGuild.SetPackedFontColor(COLOR_MUTED)
			elif guildRank > 0:
				self.footGuild.SetText(_F("BANNER_WAR_VAL_RANK", guildScore, guildRank))
				self.footGuild.SetPackedFontColor(COLOR_TITLE)
			else:
				self.footGuild.SetText(_T("BANNER_WAR_VAL_NONE"))
				self.footGuild.SetPackedFontColor(COLOR_MUTED)

		if warScore is not None and warScore >= 0 and self.footWar:
			if warScore > 0 or warKills > 0:
				self.footWar.SetText(_F("BANNER_WAR_VAL_WAR", warScore, warKills))
				self.footWar.SetPackedFontColor(COLOR_POSITIVE)
			else:
				self.footWar.SetText("-")
				self.footWar.SetPackedFontColor(COLOR_MUTED)
