import ui
import uiScriptLocale
import wndMgr
import player
import miniMap
import localeInfo
import net
import app
import colorInfo
import constInfo
import background
import chr
import chat
from constInfo import TextColor

try:
	import nav
	NAV_ENABLED = True
except ImportError:
	nav = None
	NAV_ENABLED = False


NAV_TITLE = "Otomatik Navigasyon Sistemi"
NAV_HINT  = "Gitmek istedigin yere tikla, otomatik olarak git."

# nav.PreviewFromAtlas() donus kodlari
NAV_FAIL_MESSAGE = {
	1: "Otomatik Navigasyon su anda kapali.",
	2: "Bu haritada Otomatik Navigasyon yok.",
	3: "Navigasyon verileri hazirlaniyor, birazdan tekrar dene...",
	4: "Karakter bulunamadi.",
	5: "Su anda hareket edemezsin.",
	6: "Harita disina tiklandi.",
	7: "Hedef zaten cok yakin.",
	8: "Onceki istek hala sonuclanmadi.",
}

# nav.EVENT_* -> oyuncuya gosterilecek metin.
# None olanlar BILEREK sessizdir; sohbeti doldurmak oyuncuyu rahatsiz eder.
NAV_EVENT_MESSAGE = {}

def NavBuildEventMessages():
	# DIKKAT: adi "__" ile BASLAMAMALI. Sinif icinden cagrilan "__ad"
	# Python tarafindan "_SinifAdi__ad" olarak yeniden adlandirilir.
	if not NAV_ENABLED:
		return

	NAV_EVENT_MESSAGE[nav.EVENT_TARGET_SELECTED] = None
	NAV_EVENT_MESSAGE[nav.EVENT_ROUTE_PREPARING] = None
	NAV_EVENT_MESSAGE[nav.EVENT_ROUTE_READY]     = None
	NAV_EVENT_MESSAGE[nav.EVENT_DEST_ADJUSTED]   = None
	NAV_EVENT_MESSAGE[nav.EVENT_AWAIT_SERVER]    = "Onay bekleniyor..."
	NAV_EVENT_MESSAGE[nav.EVENT_NAV_STARTED]     = "Otomatik Navigasyon basladi."
	NAV_EVENT_MESSAGE[nav.EVENT_ARRIVED]         = "Hedefe ulasildi."
	NAV_EVENT_MESSAGE[nav.EVENT_MANUAL_CANCEL]   = None
	NAV_EVENT_MESSAGE[nav.EVENT_CANCELLED]       = None
	NAV_EVENT_MESSAGE[nav.EVENT_MAP_CHANGED]     = None
	NAV_EVENT_MESSAGE[nav.EVENT_OBSTACLE_AHEAD]  = None
	NAV_EVENT_MESSAGE[nav.EVENT_CROWD_DETOUR]    = None
	NAV_EVENT_MESSAGE[nav.EVENT_CROWD_WAITING]   = None
	NAV_EVENT_MESSAGE[nav.EVENT_NOT_ENOUGH_YANG] = "Yeterli Yang yok."
	NAV_EVENT_MESSAGE[nav.EVENT_INVALID_TARGET]  = "Bu hedefe gidilemez."
	NAV_EVENT_MESSAGE[nav.EVENT_NO_ROUTE]        = "Bu hedefe rota bulunamadi."
	NAV_EVENT_MESSAGE[nav.EVENT_SERVER_REJECT]   = "Istek reddedildi."
	NAV_EVENT_MESSAGE[nav.EVENT_TIMEOUT]         = "Sunucudan cevap alinamadi."
	NAV_EVENT_MESSAGE[nav.EVENT_STUCK]           = "Yol kapandi, navigasyon durduruldu."

	# TEMBEL YUKLEME
	#
	# Veri haritaya girisde DEGIL, ilk kullanimda yuklenir (bellek icin).
	# Oyuncuya "sistem calismiyor" hissi vermemek icin bu iki mesaj var.
	NAV_EVENT_MESSAGE[nav.EVENT_DATA_LOADING]    = "Navigasyon verileri hazirlaniyor, birazdan tekrar dene..."
	NAV_EVENT_MESSAGE[nav.EVENT_DATA_READY]      = "Navigasyon hazir. Gitmek istedigin yere tiklayabilirsin."

NavBuildEventMessages()


##########################################################################
# OLAY POMPASI  -  ATLAS KAPALIYKEN DE CALISIR
#
# SORUN: __NavUpdate yalnizca AtlasWindow.OnUpdate icinden cagriliyordu.
# AtlasWindow yalnizca Atlas ACIKKEN guncellenir. Oyuncu "EVET" deyip
# Atlas'i kapatinca olaylar (ozellikle "Yol kapandi, navigasyon
# durduruldu") HIC OKUNMUYORDU: karakter sessizce duruyor, hicbir mesaj
# cikmiyordu. "bazen de bunu yazmadan gitmiyor" bunun ta kendisidir.
#
# COZUM: pompayi her karede calisan game.py OnUpdate'ten cagir.
#
# DIKKAT: olay kuyrugu TEK yerden tuketilmelidir. nav.PopEvent() olayi
# bir kez dondurup siler; iki yerden cagrilirsa mesajlar bolunur ve
# kaybolur. Bu yuzden AtlasWindow.OnUpdate icindeki cagri KALDIRILDI.
##########################################################################

# AtlasWindow kendini buraya kaydeder.
#
# ZAYIF REFERANS (weakref): modul duzeyinde GUCLU bir referans tutmak,
# oyun->giris->oyun gecisinde eski pencereyi hayatta tutar ve __del__
# calismaz. ui.Window yeni stil bir siniftir (ui.py:98
# "class Window(object)"), yani weakref desteklenir.
NAV_ATLAS_WINDOW = None


def NavPumpEvents():
	# game.py OnUpdate icinden HER KARE cagrilir.
	if not NAV_ENABLED:
		return

	if NAV_ATLAS_WINDOW is None:
		return

	wnd = NAV_ATLAS_WINDOW()		# zayif referansi coz
	if wnd is None:
		return						# pencere yok edilmis

	try:
		wnd.NavPump()
	except:
		import dbg
		dbg.TraceError("NavPumpEvents")


##########################################################################
# COK SATIRLI ONAY PENCERESI
#
# "\n" ILE ALT SATIRA GECILMEZ.
#
# KANIT  ClientSource/EterLib/GrpTextInstance.cpp:653-661
#     if ((fCurX+fFontWidth)-m_v3Position.x > m_fLimitWidth)
#     {
#         if (m_isMultiLine) { fCurX=fStanX; fCurY+=fFontMaxHeight; }
#         else               { break; }
#     }
#
# SetMultiLine() "\n" karakterini DEGIL, yalnizca m_fLimitWidth
# tasmasini isler - ve varsayilan limit 1600 px'tir
# (GrpTextInstance.cpp:1186). Bu yuzden "\n" ile birlestirilen metin
# TEK SATIR halinde ciziliyordu.
#
# Ustelik tasma ile bolunen satirlar ayri ayri ORTALANMAZ (fStanX bir
# kez, tum metnin genisligine gore hesaplanir), yani SetLimitWidth ile
# de duzgun gorunmezdi.
#
# COZUM: her satir icin AYRI bir ui.TextLine. Boylece satir sonlari tam
# istedigimiz yerde olur ve her satir kendi icinde ortalanir.
##########################################################################

def NavSetDialogLines(dlg, kLineList, nWidth):
	nCount = len(kLineList)
	if 0 == nCount:
		return

	# uiscript/questiondialog.py olculeri:
	#     pencere / board    340 x 105
	#     "message" metni    y = 38   (dikey ortali)
	#     accept / cancel    y = 63   -> alttan 105 - 63 = 42
	nStep   = 18								# satir araligi (px)
	nHeight = 105 + max(0, nCount - 2) * nStep

	dlg.SetSize(nWidth, nHeight)

	if dlg.board:
		dlg.board.SetSize(nWidth, nHeight)

	# Metin blogu, dugmelerin ustunde kalan alanin ortasina otursun.
	nTop = nHeight / 2 - 22 - ((nCount - 1) * nStep) / 2

	# --- 1. satir: betikteki "message" nesnesi
	dlg.textLine.SetHorizontalAlignCenter()
	dlg.textLine.SetVerticalAlignCenter()
	dlg.textLine.SetPosition(0, nTop)
	dlg.textLine.SetText(kLineList[0])

	# --- kalan satirlar: yeni TextLine cocuklari
	kExtraList = []

	for i in range(1, nCount):
		txt = ui.TextLine()
		txt.SetParent(dlg.board)
		txt.SetWindowHorizontalAlignCenter()	# konum: zeminin ortasina gore
		txt.SetHorizontalAlignCenter()			# metin: kendi icinde ortali
		txt.SetVerticalAlignCenter()
		txt.SetPosition(0, nTop + i * nStep)
		txt.SetText(kLineList[i])
		txt.Show()

		kExtraList.append(txt)

	# REFERANSLARI TUT. Aksi halde cop toplayici TextLine'lari siler ve
	# satirlar ekrandan kaybolur.
	dlg.navExtraLines = kExtraList

	# Dugmeler alttan 42 px. "horizontal_align: center" ile yuklendikleri
	# icin SetPosition(-40, y) ortalamayi BOZMAZ (ui.py:5729 yukleyicisi
	# de tam olarak boyle cagiriyor).
	if dlg.acceptButton:
		dlg.acceptButton.SetPosition(-40, nHeight - 42)
	if dlg.cancelButton:
		dlg.cancelButton.SetPosition(40, nHeight - 42)

	dlg.SetCenterPosition()
	dlg.UpdateRect()


def NavFormatYang(nAmount):
	# 60000 -> "60.000"
	s = str(int(nAmount))
	out = ""
	while len(s) > 3:
		out = "." + s[-3:] + out
		s = s[:-3]
	return s + out

class MapTextToolTip(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetHorizontalAlignCenter()
		textLine.SetOutline()
		textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetTooltipPosition(self, PosX, PosY):
		if localeInfo.IsARABIC():
			w, h = self.textLine.GetTextSize()
			self.textLine.SetPosition(PosX - w - 5, PosY)
		else:
			self.textLine.SetPosition(PosX - 5, PosY)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)

	def GetTextSize(self):
		return self.textLine.GetTextSize()

class AtlasWindow(ui.ScriptWindow):

	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		# Olay pompasinin hedefi. Yeni bir AtlasWindow olusursa
		# (ornegin yeniden giris) en yenisi gecerli olur.
		#
		# ZAYIF referans: bu modul pencereyi hayatta TUTMAMALIDIR.
		import weakref
		global NAV_ATLAS_WINDOW
		NAV_ATLAS_WINDOW = weakref.ref(self)

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetMapName(self, mapName):
		if 949==app.GetDefaultCodePage():
			try:
				self.board.SetTitleName(localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])
			except:
				pass

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AtlasWindow.py")
		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.LoadScript")

		try:
			self.board = self.GetChild("board")

		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.BindObject")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Hide)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(7, 30)
		self.tooltipInfo.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10, 0)
		self.board.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnMouseLeftButtonUpEvent))
		self.Hide()

		if NAV_ENABLED and nav.IsAvailable():
			self.navHintText = ui.TextLine()
			self.navHintText.SetParent(self)
			self.navHintText.SetPosition(10, 10)
			self.navHintText.SetPackedFontColor(0xFFC8C8C8)
			self.navHintText.SetText("%s - %s" % (NAV_TITLE, NAV_HINT))
			self.navHintText.Hide()

		miniMap.RegisterAtlasWindow(self)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipAtlasClose = 0
		self.tooltipInfo = None
		self.infoGuildMark = None
		self.board = None

	def NavPump(self):
		# Modul duzeyindeki NavPumpEvents() buraya girer.
		#
		# "__NavUpdate" sinif icinde "_AtlasWindow__NavUpdate" olur ve
		# disaridan cagrilamaz (Python ad bozma). Bu acik kapi gerekli.
		self.__NavUpdate()

	def __NavEnsureState(self):
		if not hasattr(self, "navWaitingPreview"):
			self.navWaitingPreview = False
		if not hasattr(self, "navQuestionDialog"):
			self.navQuestionDialog = None
		if not hasattr(self, "navWasActive"):
			self.navWasActive = False

	def __NavCloseDialog(self):
		if getattr(self, "navQuestionDialog", None):
			self.navQuestionDialog.Close()
			self.navQuestionDialog = None

	def __RefreshNavigationMark(self):
		if not NAV_ENABLED:
			return

		# miniMap.AddWayPoint imzasi: (ID, x, y, metin)
		NAV_WAYPOINT_ID = 0x4E415601	# baska waypoint ID'leriyle carpismaz

		miniMap.RemoveWayPoint(NAV_WAYPOINT_ID)

		(bHas, fx, fy) = nav.GetDestination()
		if bHas:
			miniMap.AddWayPoint(NAV_WAYPOINT_ID, fx, fy, "")

	def __NavOpenConfirm(self):
		import uiCommon

		(bHas, fSnapX, fSnapY) = nav.GetSnappedTarget()
		if not bHas:
			return

		# 100 birim = 1 metre. Gosterilen X,Y, npc.txt / Town.txt ile
		# ayni olcektedir.
		nShowX = int(fSnapX / 100.0)
		nShowY = int(fSnapY / 100.0)

		fSnapDistance = nav.GetSnapDistance()

		#################################################################
		# TAKSIMETRE
		#
		# Ucret SABIT DEGILDIR: gidilecek rotanin uzunluguna gore
		# 20.000 - 120.000 Yang arasinda degisir.
		#
		# nav.GetTravelCost() ile sunucunun kesecegi tutar AYNI formulden
		# gelir (GameLib/NavigationTariff.h == game/src/AutoNavTariff.h;
		# 450.001 noktalik tam alan taramasiyla esitlikleri dogrulandi -
		# 21_EKLENTILER/tarife_kaniti.txt).
		#
		# Pencere ACIKKEN kosarsan sunucu senin YENI konumundan hesaplar
		# ve tutar bir kademe (1.000 Yang) oynayabilir; bu yuzden sunucu
		# kesilen tutari ayrica sohbete yazar.
		#################################################################
		nCost       = nav.GetTravelCost()
		nRouteMetre = int(nav.GetPreviewRouteLength() / 100.0)

		kLineList = [
			"%s   -   X: %d   Y: %d" % (NAV_TITLE, nShowX, nShowY),

			"Rota yaklasik %d metre.   Ucret: %s Yang." % (
				nRouteMetre, NavFormatYang(nCost)),

			"Tarife yolun uzunluguna gore %s - %s Yang arasindadir." % (
				NavFormatYang(nav.PRICE_MIN), NavFormatYang(nav.PRICE_MAX)),

			# Oyuncu BASLAMADAN once bilmeli.
			"Yol kapanir ve navigasyon durursa UCRET IADE EDILMEZ.",

			"Gitmek istiyor musun?",
		]

		# Hedef kaydirildiysa oyuncuya ACIKCA soyle.
		if fSnapDistance > 100.0:
			chat.AppendChat(chat.CHAT_TYPE_INFO,
				"Tikladigin nokta yurunemez oldugu icin hedef %d metre yakina alindi."
				% int(fSnapDistance / 100.0))

		self.__NavCloseDialog()

		dlg = uiCommon.QuestionDialog()

		# DIKKAT: dlg.SetText(... + "\n" + ...) KULLANILMAZ.
		# "\n" alt satira gecirmez (GrpTextInstance.cpp:653-661);
		# butun metin TEK SATIR halinde cizilir. Her satir icin ayri
		# bir TextLine olusturulur:
		NavSetDialogLines(dlg, kLineList, 600)
		dlg.SetAcceptText("EVET")
		dlg.SetCancelText("HAYIR")
		dlg.SetAcceptEvent(ui.__mem_func__(self.__NavOnAccept))
		dlg.SetCancelEvent(ui.__mem_func__(self.__NavOnCancel))
		dlg.Open()

		self.navQuestionDialog = dlg

	def __NavOnAccept(self):
		self.__NavCloseDialog()

		# ADIM 2 - EVET.
		# Ucret istegini C++ katmani gonderir; Python paket URETMEZ.
		# Boylece arayuz betigi degistirilse bile odeme akisi degismez.
		if not nav.Confirm():
			chat.AppendChat(chat.CHAT_TYPE_INFO, NAV_FAIL_MESSAGE.get(8, ""))
		return True

	def __NavOnCancel(self):
		self.__NavCloseDialog()
		nav.CancelPreview()
		return True

	def __NavUpdate(self):
		if not NAV_ENABLED:
			return

		self.__NavEnsureState()

		# --- olaylar  (TEK tuketici)
		while True:
			nEvent = nav.PopEvent()
			if nEvent == nav.EVENT_NONE:
				break

			strMessage = NAV_EVENT_MESSAGE.get(nEvent, None)
			if strMessage:
				chat.AppendChat(chat.CHAT_TYPE_INFO, strMessage)

			# Bu olaylarda onay penceresi ve bekleme durumu temizlenir.
			if nEvent in (nav.EVENT_SERVER_REJECT, nav.EVENT_TIMEOUT,
						  nav.EVENT_NOT_ENOUGH_YANG, nav.EVENT_INVALID_TARGET,
						  nav.EVENT_NO_ROUTE, nav.EVENT_MAP_CHANGED,
						  nav.EVENT_CANCELLED, nav.EVENT_MANUAL_CANCEL):
				self.navWaitingPreview = False
				self.__NavCloseDialog()

		# --- rota hazir mi -> ONAY PENCERESI
		if self.navWaitingPreview and nav.IsPreviewReady():
			self.navWaitingPreview = False
			self.__NavOpenConfirm()

		# --- navigasyon bittiyse hedef isaretini kaldir
		bActive = nav.IsActive()
		if self.navWasActive and not bActive:
			self.__RefreshNavigationMark()
		self.navWasActive = bActive

	def OnUpdate(self):

		# OTOMATIK NAVIGASYON olay pompasi BURADAN KALDIRILDI.
		#
		# NEDEN: bu metot yalnizca Atlas ACIKKEN calisir. Oyuncu "EVET"
		# deyip Atlas'i kapatinca "Yol kapandi, navigasyon durduruldu"
		# gibi olaylar hic okunmuyordu; karakter sessizce duruyordu.
		#
		# Pompa artik game.py OnUpdate icinden uiMiniMap.NavPumpEvents()
		# ile cagriliyor. Kuyruk TEK yerden tuketilmelidir: buraya GERI
		# EKLEME, yoksa mesajlar iki cagri arasinda bolunur.

		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()

		if False == self.board.IsIn():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeInfo.GUILD_EMPTY_AREA

		if localeInfo.IsARABIC() and sName[-1].isalnum():
			self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
		else:
			self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))

		(x, y) = self.GetGlobalPosition()
		self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
		self.tooltipInfo.SetTextColor(dwTextColor)
		self.tooltipInfo.Show()
		self.tooltipInfo.SetTop()

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 15, iSizeY + 38)

				if localeInfo.IsARABIC():
					self.board.SetPosition(iSizeX+15, 0)

				self.board.SetSize(iSizeX + 15, iSizeY + 38)
				#self.AtlasMainWindow.SetSize(iSizeX, iSizeY)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def OnMouseLeftButtonUpEvent(self):
		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

		# if chr.IsGameMaster(player.GetMainCharacterIndex()):
			# net.SendChatPacket("/go %s %s" % (str(iPosX), str(iPosY)))
			# return

		# --------------------------------------------------------------
		# ADIM 1 - ROTA ON IZLEME
		#
		# Burada HICBIR UCRET ISTENMEZ. Yalnizca rotanin gercekten
		# hesaplanabilir olup olmadigi olculur. Sonuc asenkron gelir;
		# onay penceresi __NavUpdate icinde acilir.
		# --------------------------------------------------------------
		if not NAV_ENABLED:
			return

		if not nav.IsAvailable():
			return

		self.__NavEnsureState()

		nResult = nav.PreviewFromAtlas(float(mouseX), float(mouseY))

		if nResult != nav.START_OK:
			strMessage = NAV_FAIL_MESSAGE.get(nResult, None)
			if strMessage:
				chat.AppendChat(chat.CHAT_TYPE_INFO, strMessage)
			return

		self.navWaitingPreview = True

	# def OnMouseLeftButtonUpEvent(self):
		# (mouseX, mouseY) = wndMgr.GetMousePosition()
		# (bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)
		# if chr.IsGameMaster(player.GetMainCharacterIndex()):
			# net.SendChatPacket("/go %s %s" % (str(iPosX), str(iPosY)))

	def OnPressEscapeKey(self):
		# Atlas acikken ESC once navigasyonu iptal eder.
		if NAV_ENABLED and nav.IsActive():
			self.__NavCloseDialog()
			nav.Cancel()
			self.__RefreshNavigationMark()
			return True

		self.Hide()
		return True

def __RegisterMiniMapColor(type, rgb):
	miniMap.RegisterColor(type, rgb[0], rgb[1], rgb[2])

class MiniMap(ui.ScriptWindow):

	CANNOT_SEE_INFO_MAP_DICT = {
		"metin2_map_monkeydungeon" : False,
		"metin2_map_monkeydungeon_02" : False,
		"metin2_map_monkeydungeon_03" : False,
		"metin2_map_devilsCatacomb" : False,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipMiniMapOpen = MapTextToolTip()
		self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		self.tooltipMiniMapOpen.Show()
		self.tooltipMiniMapClose = MapTextToolTip()
		self.tooltipMiniMapClose.SetText(localeInfo.UI_CLOSE)
		self.tooltipMiniMapClose.Show()
		self.tooltipScaleUp = MapTextToolTip()
		self.tooltipScaleUp.SetText(localeInfo.MINIMAP_INC_SCALE)
		self.tooltipScaleUp.Show()
		self.tooltipScaleDown = MapTextToolTip()
		self.tooltipScaleDown.SetText(localeInfo.MINIMAP_DEC_SCALE)
		self.tooltipScaleDown.Show()
		self.tooltipAtlasOpen = MapTextToolTip()
		self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		self.tooltipAtlasOpen.Show()
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		if miniMap.IsAtlas():
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		else:
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_CAN_NOT_SHOW_AREAMAP)

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True

		# AUTOBAN
		self.imprisonmentDuration = 0
		self.imprisonmentEndTime = 0
		self.imprisonmentEndTimeText = ""
		# END_OF_AUTOBAN

	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0

		self.OpenWindow = 0
		self.CloseWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.MiniMapHideButton = 0
		self.MiniMapShowButton = 0
		self.AtlasShowButton = 0

		self.tooltipMiniMapOpen = 0
		self.tooltipMiniMapClose = 0
		self.tooltipScaleUp = 0
		self.tooltipScaleDown = 0
		self.tooltipAtlasOpen = 0
		self.tooltipInfo = None
		self.serverInfo = None

	def SetMapName(self, mapName):
		self.mapName=mapName
		self.AtlasWindow.SetMapName(mapName)

		if self.CANNOT_SEE_INFO_MAP_DICT.has_key(mapName):
			self.canSeeInfo = False
			self.HideMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP_CANNOT_SEE)
		else:
			self.canSeeInfo = True
			self.ShowMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)

	# AUTOBAN
	def SetImprisonmentDuration(self, duration):
		self.imprisonmentDuration = duration
		self.imprisonmentEndTime = app.GetGlobalTimeStamp() + duration

		self.__UpdateImprisonmentDurationText()

	def __UpdateImprisonmentDurationText(self):
		restTime = max(self.imprisonmentEndTime - app.GetGlobalTimeStamp(), 0)

		imprisonmentEndTimeText = localeInfo.SecondToDHM(restTime)
		if imprisonmentEndTimeText != self.imprisonmentEndTimeText:
			self.imprisonmentEndTimeText = imprisonmentEndTimeText
			self.serverInfo.SetText("%s: %s" % (uiScriptLocale.AUTOBAN_QUIZ_REST_TIME, self.imprisonmentEndTimeText))
	# END_OF_AUTOBAN

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "Minimap.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/MiniMap.py")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.LoadScript")

		try:
			self.OpenWindow = self.GetChild("OpenWindow")
			self.MiniMapWindow = self.GetChild("MiniMapWindow")
			self.ScaleUpButton = self.GetChild("ScaleUpButton")
			self.ScaleDownButton = self.GetChild("ScaleDownButton")
			self.MiniMapHideButton = self.GetChild("MiniMapHideButton")
			self.AtlasShowButton = self.GetChild("AtlasShowButton")
			self.CloseWindow = self.GetChild("CloseWindow")
			self.MiniMapShowButton = self.GetChild("MiniMapShowButton")
			self.positionInfo = self.GetChild("PositionInfo")
			self.observerCount = self.GetChild("ObserverCount")
			self.serverInfo = self.GetChild("ServerInfo")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.Bind")

		if constInfo.MINIMAP_POSITIONINFO_ENABLE==0:
			self.positionInfo.Hide()
		if constInfo.MINIMAP_DATE_SYSTEM:
			self.positionInfo.SetPosition(72,155)

		self.serverInfo.SetText(net.GetServerInfo())
		self.ScaleUpButton.SetEvent(ui.__mem_func__(self.ScaleUp))
		self.ScaleDownButton.SetEvent(ui.__mem_func__(self.ScaleDown))
		self.MiniMapHideButton.SetEvent(ui.__mem_func__(self.HideMiniMap))
		self.MiniMapShowButton.SetEvent(ui.__mem_func__(self.ShowMiniMap))

		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(ui.__mem_func__(self.ToggleAtlasWindow)) # @fixme014 ShowAtlas

		(ButtonPosX, ButtonPosY) = self.MiniMapShowButton.GetGlobalPosition()
		self.tooltipMiniMapOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.MiniMapHideButton.GetGlobalPosition()
		self.tooltipMiniMapClose.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleUpButton.GetGlobalPosition()
		self.tooltipScaleUp.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleDownButton.GetGlobalPosition()
		self.tooltipScaleDown.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.AtlasShowButton.GetGlobalPosition()
		self.tooltipAtlasOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		self.ShowMiniMap()

	def Destroy(self):
		self.HideMiniMap()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None

		self.ClearDictionary()

		self.__Initialize()

	def UpdateCurrentChannel(self, channelID):
		(serverName, channelName) = net.GetServerInfo().split(",")
		channelName = "CH{}".format(channelID)
		# constInfo.channelidx=int(channelID)
		net.SetServerInfo("{}, {}".format(serverName, channelName))
		if self.serverInfo:
			self.serverInfo.SetText(net.GetServerInfo())

	def UpdateObserverCount(self, observerCount):
		if observerCount>0:
			self.observerCount.Show()
		elif observerCount<=0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeInfo.MINIMAP_OBSERVER_COUNT % observerCount)

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)

		if constInfo.MINIMAP_DATE_SYSTEM:
			self.positionInfo.SetText("%s" % (constInfo.GetTimeDate()))
		else:
			self.positionInfo.SetText("(%.0f, %.0f)" % (x/100, y/100))

		if self.tooltipInfo:
			if True == self.MiniMapWindow.IsIn():
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
				if bFind == 0:
					self.tooltipInfo.Hide()
				elif not self.canSeeInfo:
					self.tooltipInfo.SetText("%s(%s)" % (sName, localeInfo.UI_POS_UNKNOWN))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
				else:
					if localeInfo.IsARABIC() and sName[-1].isalnum():
						self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
					else:
						self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
			else:
				self.tooltipInfo.Hide()

			# AUTOBAN
			if self.imprisonmentDuration:
				self.__UpdateImprisonmentDurationText()
			# END_OF_AUTOBAN

		if True == self.MiniMapShowButton.IsIn():
			self.tooltipMiniMapOpen.Show()
		else:
			self.tooltipMiniMapOpen.Hide()

		if True == self.MiniMapHideButton.IsIn():
			self.tooltipMiniMapClose.Show()
		else:
			self.tooltipMiniMapClose.Hide()

		if True == self.ScaleUpButton.IsIn():
			self.tooltipScaleUp.Show()
		else:
			self.tooltipScaleUp.Hide()

		if True == self.ScaleDownButton.IsIn():
			self.tooltipScaleDown.Show()
		else:
			self.tooltipScaleDown.Hide()

		if True == self.AtlasShowButton.IsIn():
			self.tooltipAtlasOpen.Show()
		else:
			self.tooltipAtlasOpen.Hide()

	def OnRender(self):
		(x, y) = self.GetGlobalPosition()
		fx = float(x)
		fy = float(y)
		miniMap.Render(fx + 4.0, fy + 5.0)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		miniMap.Hide()
		self.OpenWindow.Hide()
		self.CloseWindow.Show()

	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		miniMap.Show()
		self.OpenWindow.Show()
		self.CloseWindow.Hide()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if not self.AtlasWindow.IsShow():
			self.AtlasWindow.Show()

	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()
