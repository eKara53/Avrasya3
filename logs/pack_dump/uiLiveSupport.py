# DUMPED FROM LIVE COMPILE: uiLiveSupport.py (len=41753)
##
## Oyun ici canli destek - "Canli Destek" fisilti penceresi.
##
## Oyuncu, normal bir fisilti (PM) yazar gibi yazar; mesaj oyun sunucusuna DEGIL, dogrudan
## live.avrasyamt2.com canli destek altyapisina gider (temsilci panelindeki sohbetler).
## Tum ag islemleri istemcinin C++ "liveSupport" modulunde, arka plan thread'inde yapilir;
## bu dosya her karede yalniz hazir yanitlari okur (oyun beklemez, donmaz).
##
## Dosya kodlamasý: cp1254 (ANSI), LF satýr sonu.
##
import os
import re
import app
import ui
import chat
import player
import net
import constInfo
import uiWhisper

try:
	import liveSupport		# istemci C++ modulu (PythonLiveSupportModule.cpp). Eski istemcide yoksa sistem kapali kalir.
except ImportError:
	liveSupport = None

HAS_LEAVE = liveSupport is not None and hasattr(liveSupport, "SetLeave")		# v1.1: "oyuncu ayrildi" bildirimi
HAS_PROTECT = liveSupport is not None and hasattr(liveSupport, "Protect")	# v1.1: sifreli oturum dosyasi (DPAPI)

#####################################################################
## Ayarlar

BASE_URL		= "https://live.avrasyamt2.com"
SITE_KEY		= "pk_exxyir7bhdovovk9qvbtj5lueoqvas1l"	# panel: Yonetim -> Widget & site (oyun icin ayri site onerilir)
PAGE_URL		= "https://live.avrasyamt2.com/oyun-ici"	# panel baglam kurali bu yolla eslesir -> "Oyun Ici" gelen kutusu (yapay zeka KAPALI)
API				= "/api/support/v1"
USER_AGENT		= "Avrasya2Client/1.0 (Metin2 oyun ici)"
TARGET_NAME		= "Canlý Destek"		# fisilti adi; bosluk + noktasiz i iceren ad hicbir oyuncu adiyla cakisamaz
MESSAGE_MAX		= 300					# tek mesaj ust siniri (sunucu 4000 kabul eder)
TOKEN_FILE		= "livesupport_%s.dat"	# constInfo.CLIENT_YOL altinda, karakter basina oturum dosyasi

POLL_OPEN		= 2.0					# pencere acikken yeni mesaj kontrolu (sn)
POLL_BACKGROUND	= 15.0					# pencere kapali ama gorusme suruyor
RETRY_STEPS		= (5.0, 10.0, 30.0, 60.0)	# ag hatasinda bekleme adimlari
READ_INTERVAL	= 5.0					# "okundu" bildirimi en sik
SEND_GAP		= 1.0					# iki mesaj arasi en az (sunucu siniri dakikada 20)
MAX_PER_MINUTE	= 10					# dakikada en fazla mesaj (istemci tarafi; sunucu da ayrica sinirlar)
DUPLICATE_WINDOW = 30.0					# ayni metin bu sure icinde tekrar gonderilemez
LEAVE_GRACE_MS	= 45000					# cikis yapilip bu surede oyuna donulmezse temsilciye "oyundan cikti" notu (yavas PC'de harita yuklemesi uzun surebilir)
MESSAGE_LINES_MAX = 40					# tek mesajin pencereye yazilan en fazla satiri (tamami panelde)
CLOSED_GRACE	= 30.0					# pencere kapatilip bu surede yeniden acilmazsa temsilciye "pencereyi kapatti" notu
AGENT_COLOR		= "|cFFFFA100"			# temsilci satiri: GM turuncusu, normal (italik olmayan) yazi tipi
RESULTS_PER_FRAME = 8					# karede en fazla islenen yanit (kare suresi sabit kalir)
REQUEST_STALE	= 45.0					# yaniti bu kadar gelmeyen istek ag hatasi sayilir (C++ zaman asimi 20 sn)
WATCHDOG_EVERY	= 5.0
LINE_LIMIT		= 400					# fisilti penceresinde tutulan en fazla satir (RAM ust siniri)
LINE_KEEP		= 300					# sinir asilinca kalan son satir sayisi
DISPLAY_MAX		= 2000					# tek mesajin ekrana yazilan en fazla karakteri
DIALOG_WIDTH	= 350					# kutu genisligi (350-50=300) = fisilti nesnesinin varsayilan 300 px'i: tum satirlar ayni sarilir
DIALOG_HEIGHT	= 240					# yazi siniri resmi formulle 123 karakter (3 satir, kutudan tasmaz)
ERROR_LOG_EVERY	= 30.0					# beklenmeyen hata logu en sik (her kare log yazilmaz)
RENDER_PER_BATCH = 60					# tek yanitta yazilan en fazla mesaj (fazlasi atlanir, tumu panelde)
RESYNC_GAP		= 1.0					# "devami var" yanitinda bir sonraki istege en az bekleme

#####################################################################
## Metinler

AGENT_DEFAULT		= "Destek Ekibi"
BTN_END				= "Bitir"
TXT_NEED_CLIENT		= "Canlý destek için güncel oyun istemcisi gerekiyor."
TXT_CONNECTING		= "Canlý desteðe baðlanýlýyor..."
TXT_UNAVAILABLE		= "Canlý destek þu anda kullanýlamýyor. Lütfen biraz sonra tekrar deneyin."
TXT_WELCOME			= "Merhaba! Sorununuzu yazýn, bir temsilcimiz en kýsa sürede size dönecek."
TXT_OFFLINE			= "Þu anda çevrimiçi temsilci yok. Mesajýnýzý býrakýn, en kýsa sürede yanýtlanacak."
TXT_QUEUE			= "Sýradaki yeriniz: %d"
TXT_ASSIGNED		= "Temsilci %s ile görüþüyorsunuz."
TXT_NEW_MESSAGE		= "[Canlý Destek] Yeni mesajýnýz var."
TXT_SEND_FAIL		= "Mesaj gönderilemedi: %s"
TXT_SEND_RETRY		= "Baðlantý sorunu, mesajýnýz tekrar gönderilecek..."
TXT_SEND_GIVEUP		= "Mesaj gönderilemedi. Baðlantýnýzý kontrol edip tekrar yazýn."
TXT_TOO_FAST		= "Çok hýzlý yazýyorsunuz, biraz bekleyin."
TXT_DUPLICATE		= "Ayný mesajý az önce gönderdiniz."
TXT_NO_CONV			= "Açýk bir görüþmeniz yok."
TXT_ENDED			= "Görüþme sonlandýrýldý. Yeni bir mesaj yazarak tekrar ulaþabilirsiniz."
TXT_RATE_PROMPT		= "Görüþmeyi 1-5 arasý puanlamak için yalnýzca rakamý yazýp gönderin (örn. 5)."
TXT_RATE_THANKS		= "Deðerlendirmeniz için teþekkürler!"
TXT_ACTION_FAIL		= "Ýþlem yapýlamadý: %s"
TXT_ATTACHMENT		= "[Dosya: %s] (oyun içinde açýlamaz)"
TXT_PAGE_TITLE		= "Oyun içi | %s"
TXT_CONNECTION		= "baðlantý hatasý"
TXT_SKIPPED			= "(%d eski mesaj burada gösterilmedi)"
TXT_SAFETY			= "Güvenliðiniz için: destek ekibimiz sizden asla þifre veya eþya istemez, oyunda size oyuncu adýyla fýsýltý atmaz. Bize yalnýzca Yardým > Canlý Destek penceresinden ulaþýrsýnýz."

#####################################################################

def _ErrorInfo(doc):
	if isinstance(doc, dict):
		error = doc.get("error")
		if isinstance(error, dict):
			return (str(error.get("code") or ""), str(error.get("message") or ""), error.get("retry_after"))
	return ("", "", None)

def _RetryAfter(doc, default):
	(code, message, retryAfter) = _ErrorInfo(doc)
	if isinstance(retryAfter, (int, long)) and retryAfter > 0:
		return float(min(retryAfter, 120))
	return default

def _Reason(status, doc):
	(code, message, retryAfter) = _ErrorInfo(doc)
	if message:
		return message
	if code:
		return code
	if not status:
		return TXT_CONNECTION
	return str(status)

def _IsToken(value):
	# Ziyaretci anahtari: "v1." + base64url. Baska her sey (NUL, bosluk, satir sonu, ASCII disi) reddedilir.
	if not isinstance(value, str) or not value.startswith("v1.") or not (23 <= len(value) <= 128):
		return False
	for c in value[3:]:
		if not (("a" <= c <= "z") or ("A" <= c <= "Z") or ("0" <= c <= "9") or c in "-_"):
			return False
	return True

_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")	# satir sonu (\n) disindaki kontrol karakterleri

def _Clean(text):
	# Metin motoru ozel dizileri: "|" (renk/baglanti/emoji) ve "@" + 4 rakam (kod sayfasi degisimi; ornegin @0037 ile
	# 0x7C bayti olmadan "|" uretilebilir). Sunucudan gelen her metinde ikisi de etkisiz hale getirilir.
	text = text.replace("|", "¦")
	# Kontrol karakterleri (\r, NUL, ...) "@" denetiminden ONCE silinir: sonradan silinseler "@\r0037" -> "@0037" olurdu
	text = _CONTROL.sub("", text.replace("\t", " "))
	if "@" not in text:
		return text
	parts = text.split("@")
	out = [parts[0]]
	for part in parts[1:]:
		if len(part) >= 4 and part[0] in "0123456789" and part[1] in "0123456789" and part[2] in "0123456789" and part[3] in "0123456789":
			out.append("@ " + part)
		else:
			out.append("@" + part)
	return "".join(out)

def _ServerName():
	try:
		return net.GetServerInfo().split(",")[0].strip()
	except:
		return ""

def _IsId(value):
	return isinstance(value, str) and 0 < len(value) <= 40 and value.isalnum()

def _AppendWhisper(whisperType, text):
	if getattr(app, "ENABLE_VEGAS_MULTI_LANGUAGE", 0):
		chat.AppendWhisper(whisperType, TARGET_NAME, text, 255)	# 255 = dil bayragi yok
	else:
		chat.AppendWhisper(whisperType, TARGET_NAME, text)

def _OpenFromButton():
	GetManager().Open()

_nextErrorLogAt = [0.0]

def _LogError(where, error):
	# beklenmeyen hata: oyun akisi surer, log seyrek yazilir (her kare dosyaya yazilmaz)
	try:
		now = app.GetTime()
		if now >= _nextErrorLogAt[0]:
			_nextErrorLogAt[0] = now + ERROR_LOG_EVERY
			import dbg
			dbg.TraceError("uiLiveSupport.%s: %s" % (where, error))
	except:
		pass

def _Safe(default):
	# Oyun kodundan (arayuz kurulumu, isinlanma, pencere olaylari) cagrilan yontemler: hicbir istisna disari cikmaz,
	# yukleme / isinlanma akisi canli destek yuzunden asla kesilmez.
	def wrap(function):
		def call(*args):
			try:
				return function(*args)
			except Exception as e:
				_LogError(function.__name__, e)
				return default
		call.__name__ = function.__name__
		return call
	return wrap

def _ParseSession(data):
	# oturum dosyasi -> (anahtar, gorusme, gorulen_sira, suren_gorusme, eski_bicim) | None (bozuk / cozulemeyen)
	if data.startswith("v2|"):
		if not HAS_PROTECT:
			return None
		parts = liveSupport.Unprotect(data[3:]).split("|")	# baska bilgisayar / Windows hesabinda cozulemez -> bos
		if len(parts) < 4:
			return None
		legacy = False
	elif data.startswith("v1|"):
		parts = data[3:].split("|")			# eski (sifresiz) bicim: okunur, bir sonraki kayitta sifrelenir
		if len(parts) < 3:
			return None
		parts.append("1")
		legacy = True
	else:
		return None
	token = parts[0] if _IsToken(parts[0]) else ""
	conversationId = parts[1] if _IsId(parts[1]) else ""
	try:
		lastSeenSeq = max(0, int(parts[2]))
	except ValueError:
		lastSeenSeq = 0
	return (token, conversationId, lastSeenSeq, bool(token) and "1" == parts[3], legacy)

#####################################################################
## Pencere: resmi fisilti penceresi, yalniz gonderme/kapatma davranisi farkli

class LiveSupportDialog(uiWhisper.WhisperDialog):

	def __init__(self):
		uiWhisper.WhisperDialog.__init__(self, None, None)

	def __del__(self):
		uiWhisper.WhisperDialog.__del__(self)

	def LoadDialog(self):
		uiWhisper.WhisperDialog.LoadDialog(self)

		self.titleName.SetText(TARGET_NAME)
		self.titleNameEdit.Hide()
		self.ignoreButton.Hide()
		self.acceptButton.Hide()
		self.gamemasterMark.Hide()
		self.minimizeButton.Show()
		# "Sikayet" butonu yerine: gorusmeyi bitir
		self.reportViolentWhisperButton.SetText(BTN_END)
		self.reportViolentWhisperButton.SetEvent(ui.__mem_func__(self.__OnClickEnd))
		self.reportViolentWhisperButton.Hide()
		# Varsayilan boyut: resmi yeniden boyutlandirma yolu (yazi siniri ve kutu olculeri temel sinifla ayni hesaplanir)
		self.resizeButton.SetPosition(DIALOG_WIDTH - 20, DIALOG_HEIGHT - 20)
		self.ResizeWhisperDialog()

	def OpenLive(self):
		# chat.CreateWhisper burada cagrilmaz: ayni adla her cagri C++ tarafinda bir nesne sizdirir; fisilti ilk satirla olusur
		chat.SetWhisperBoxSize(TARGET_NAME, self.GetWidth() - 50, self.GetHeight() - 90)
		self.targetName = TARGET_NAME
		self.textRenderer.SetTargetName(TARGET_NAME)
		self.titleName.SetText(TARGET_NAME)
		self.chatLine.SetFocus()

	def SetEndButtonVisible(self, isVisible):
		if isVisible:
			self.reportViolentWhisperButton.Show()
		else:
			self.reportViolentWhisperButton.Hide()

	## WhisperDialog davranis degisiklikleri

	def SendWhisper(self):
		text = self.chatLine.GetText()
		if not text:
			return
		if GetManager().SendText(text):
			self.chatLine.SetText("")

	def Minimize(self):
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()
		GetManager().OnDialogMinimized()

	def Close(self):
		# Normal fisiltiden farkli: yazismalar silinmez (chat.ClearWhisper yok), yalniz pencere kapanir.
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()
		GetManager().OnDialogClosed()

	def IgnoreTarget(self):
		pass

	def ReportViolentWhisper(self):
		pass

	def AcceptTarget(self):
		pass

	def SetGameMasterLook(self):
		pass

	def __OnClickEnd(self):
		GetManager().EndConversation()

#####################################################################
## Yonetici: protokol + durum. Modul duzeyinde tek nesne; isinlanmada (GameWindow yeniden kurulur) korunur.

class LiveSupportManager(object):

	def __init__(self):
		self.interface = None
		self.dialog = None
		self.button = None
		self.configured = False
		self.safetyShown = False
		self.nextRequestId = 1
		self.pending = {}
		self.attachServer = ""		# AttachUI anindaki sunucu adi
		self.charServer = ""		# yuklu oturumun sunucusu (ayni ad baska sunucuda baska karakterdir)
		self.deferTrim = False		# toplu yazimda satir kirpma sona birakilir
		self.__ResetState("")

	def __ResetState(self, charName):
		self.charName = charName
		self.token = ""
		self.conversationId = ""
		self.conversationActive = False
		self.human = False
		self.assigneeName = ""
		self.queuePosition = None
		self.lastSeq = 0			# bu gorusmede alinan son mesaj sirasi
		self.lastSeenSeq = 0		# oyuncunun gordugu son sira (dosyada; relog sonrasi "yeni mesaj" bildirimi icin)
		self.lastReadSentSeq = 0
		self.nextReadAt = 0.0
		self.renderedIds = {}
		self.sentClientIds = {}
		self.outbox = []
		self.sending = False
		self.ready = False
		self.bootstrapping = False
		self.bootstrapSilent = False
		self.nextBootstrapAt = 0.0
		self.wantSilentBootstrap = False
		self.config = {}
		self.syncInFlight = False
		self.nextSyncAt = 0.0
		self.failCount = 0
		self.awaitingRating = False
		self.ratingConversationId = ""
		self.unread = False
		self.lastSendAt = -SEND_GAP
		self.humanRequested = {}
		self.greetingShown = False
		self.fileDirty = False
		self.lines = []				# (tur, metin): fisilti satirlarinin kopyasi, LINE_LIMIT ile sinirli
		self.active = False			# tembel etkinlesme: canli destek hic acilmadiysa her kare yalniz bu bayrak okunur
		self.sendTimes = []
		self.lastSentText = ""
		self.lastSentTextAt = -DUPLICATE_WINDOW
		self.leaveKey = ""			# C++ modulunde hazirda tutulan "oyuncu ayrildi" bildiriminin anahtari
		self.maybeAway = False		# temsilciye "kapatti/cikti" notu gitmis olabilir -> geri donuste "tekrar cevrimici"
		self.closedNoteAt = 0.0		# pencere kapatildi: "kapatti" notunun gidecegi an (0 = yok)
		self.savedActive = False	# dosyadaki bayrak: suren gorusme / okunmamis yanit vardi
		self.nextWatchdogAt = 0.0
		self.nextErrorLogAt = 0.0
		self.minimized = False
		self.fileKey = charName

	#################################################################
	## Arayuz baglantisi (interfacemodule)

	@_Safe(None)
	def AttachUI(self, interface):
		self.interface = interface
		self.attachServer = _ServerName()
		if not liveSupport or not self.__CheckCharacter():
			return
		if HAS_LEAVE and self.leaveKey and liveSupport.LeaveTimer(0):
			# cikista zamanlayici "oyundan cikti" notunu gonderdi ve oyuncu geri geldi: bildirim yeniden kurulur
			self.maybeAway = True
			self.leaveKey = ""
			self.__UpdateLeave()
		if not self.active:
			return					# canli destek bu karakterde hic kullanilmadi: hicbir is yok
		self.wantSilentBootstrap = True	# giriste: kayitli gorusme varsa sessizce yeni mesaj kontrolu
		# Karakter seciminden giriste chat.Clear() fisilti hafizasini siler, isinlanmada korunur: iki durumda da ayni
		# gorunum icin satirlar yeniden yazilir (en fazla LINE_LIMIT, yukleme sirasinda bir kez). Buton geri yuklemesi
		# hemen ardindan chat.InitWhisper -> interface.MakeWhisperButton -> OnWhisperRestore ile yapilir.
		self.__RebuildWhisper()
		self.__ReportReturned()

	@_Safe(None)
	def DetachUI(self):
		dialog = self.dialog
		self.dialog = None
		try:
			if HAS_LEAVE and self.leaveKey:
				# isinlanma kisa surer; LEAVE_GRACE_MS icinde geri gelinmezse (cikis / karakter secimi) temsilciye not gider
				liveSupport.LeaveTimer(LEAVE_GRACE_MS)
			self.__HideButton()
		finally:
			# eski arayuze hicbir baglanti kalmaz (pencere/buton her durumda birakilir)
			self.button = None
			self.interface = None
			if dialog:
				dialog.Hide()
				dialog.Destroy()

	@_Safe(None)
	def OnWhisperRestore(self):
		# chat.InitWhisper isinlanmadan sonra her fisilti icin buton ister: okunmamis mesaj varsa ya da pencere kucultulmusse
		if self.unread or self.minimized:
			self.__ShowButton(self.unread)

	@_Safe(None)
	def OnDialogMinimized(self):
		self.minimized = True
		self.__ShowButton(False)

	@_Safe(None)
	def OnDialogClosed(self):
		self.minimized = False
		if self.conversationActive:
			# temsilciye ic not (pencereyi kapatti; hala oyunda, bildirim alir) CLOSED_GRACE sonra gider: kisa kapat/ac not uretmez
			self.closedNoteAt = app.GetTime() + CLOSED_GRACE

	@_Safe(None)
	def Open(self):
		if not liveSupport:
			chat.AppendChat(chat.CHAT_TYPE_INFO, TXT_NEED_CLIENT)
			return
		if not self.interface or not self.__CheckCharacter():
			return
		self.active = True

		if not self.dialog:
			dialog = LiveSupportDialog()
			dialog.BindInterface(self.interface)
			dialog.LoadDialog()
			dialog.SetCenterPosition()
			self.dialog = dialog

		self.__HideButton()
		if self.unread:
			self.unread = False
			self.fileDirty = True
		self.minimized = False
		self.closedNoteAt = 0.0			# "kapatti" notu henuz gitmediyse iptal (geri donus notu da gerekmez)
		self.dialog.OpenLive()
		if not self.safetyShown:
			self.safetyShown = True
			self.__System(TXT_SAFETY)
		self.dialog.Show()
		self.dialog.SetTop()
		self.__UpdateEndButton()

		if not self.ready:
			if not self.bootstrapping and app.GetTime() >= self.nextBootstrapAt:	# hata sonrasi bekleme suresine uyulur
				self.__Bootstrap(False)
		else:
			self.nextSyncAt = app.GetTime()
			self.__MarkSeen()
			self.__ShowGreetingIfIdle()
			self.__ReportReturned()

	def IsDialogVisible(self):
		return self.dialog is not None and self.dialog.IsShow()

	#################################################################
	## Her kare (game.GameWindow.OnUpdate)

	def Update(self):
		if not liveSupport or not self.active:
			return	# canli destegi hic acmayan oyuncu icin kare basi maliyet: iki bayrak okuma
		try:
			self.__UpdateInner()
		except Exception as e:
			# game.OnUpdate'in geri kalani her karede calismaya devam etsin; log seyrek yazilir
			now = app.GetTime()
			if now >= self.nextErrorLogAt:
				self.nextErrorLogAt = now + ERROR_LOG_EVERY
				import dbg
				dbg.TraceError("uiLiveSupport.Update: %s" % e)

	def __UpdateInner(self):
		if not self.__CheckCharacter():
			return

		for i in xrange(RESULTS_PER_FRAME):
			result = liveSupport.Poll()
			if result is None:
				break
			(requestId, status, curlCode, doc) = result
			entry = self.pending.pop(requestId, None)
			if entry is None:
				continue
			self.__SafeDispatch(entry[0], entry[1], status, doc)

		now = app.GetTime()

		# Bekci: yaniti kaybolan istek (kuyruk tasmasi vb.) durumu kilitlemesin -> ag hatasi gibi islenir
		if now >= self.nextWatchdogAt:
			self.nextWatchdogAt = now + WATCHDOG_EVERY
			for requestId in [key for (key, value) in self.pending.items() if now - value[2] > REQUEST_STALE]:
				entry = self.pending.pop(requestId)
				self.__SafeDispatch(entry[0], entry[1], 0, None)

		if self.wantSilentBootstrap:
			self.wantSilentBootstrap = False
			if self.token and not self.ready and not self.bootstrapping:
				self.__Bootstrap(True)

		if not self.ready and not self.bootstrapping and self.nextBootstrapAt and now >= self.nextBootstrapAt:
			if self.IsDialogVisible() or self.outbox:
				self.__Bootstrap(True)

		if self.closedNoteAt and now >= self.closedNoteAt:
			self.closedNoteAt = 0.0
			if not self.IsDialogVisible() and self.conversationActive:
				self.__SendPresence("closed")
				self.maybeAway = True

		self.__ProcessOutbox(now)

		if self.ready and self.conversationId and not self.syncInFlight and now >= self.nextSyncAt:
			if self.__PollInterval() is not None:
				self.__Sync()

		if self.IsDialogVisible() and self.lastSeq > self.lastReadSentSeq:
			self.__MarkSeen()

		if self.fileDirty:
			self.__SaveFile()

	#################################################################
	## Oyuncu yazdi (pencere)

	@_Safe(False)
	def SendText(self, text):
		if not liveSupport:
			self.__System(TXT_NEED_CLIENT)
			return True
		if not self.__CheckCharacter():
			return False

		text = text.strip()
		if not text:
			return True

		if self.awaitingRating and len(text) == 1 and text in "12345":
			self.__SendRating(int(text))
			return True

		now = app.GetTime()
		self.sendTimes = [t for t in self.sendTimes if now - t < 60.0]
		if now - self.lastSendAt < SEND_GAP or len(self.outbox) >= 5 or len(self.sendTimes) >= MAX_PER_MINUTE:
			self.__System(TXT_TOO_FAST)
			return False	# metin kutuda kalir
		if text == self.lastSentText and now - self.lastSentTextAt < DUPLICATE_WINDOW:
			self.__System(TXT_DUPLICATE)
			return False

		clientMessageId = liveSupport.NewUuid()
		if not clientMessageId:
			return False

		text = text[:MESSAGE_MAX]
		self.sentClientIds[clientMessageId] = 1
		self.__AppendLines(chat.WHISPER_TYPE_CHAT, self.charName, text)
		self.outbox.append({"cmid": clientMessageId, "body": text, "tries": 0, "nextAt": 0.0})
		self.lastSendAt = now
		self.sendTimes.append(now)
		self.lastSentText = text
		self.lastSentTextAt = now
		self.awaitingRating = False
		self.active = True
		self.__ReportReturned()

		if not self.ready and not self.bootstrapping:
			self.__Bootstrap(False)
		return True

	@_Safe(None)
	def EndConversation(self):
		if not self.conversationId or not self.conversationActive:
			self.__System(TXT_NO_CONV)
			return
		for entry in self.pending.values():
			if "close" == entry[0]:
				return					# istek zaten yolda (cift tiklama)
		self.__Request("close", "POST", "/conversations/%s/close" % self.conversationId, None)

	#################################################################
	## Istekler

	def __EnsureConfigured(self):
		if self.configured:
			return True
		if not liveSupport:
			return False
		self.configured = bool(liveSupport.Configure(BASE_URL, SITE_KEY, USER_AGENT))
		return self.configured

	def __Request(self, kind, method, path, body, data = None):
		if not self.__EnsureConfigured():
			return False
		requestId = self.nextRequestId
		self.nextRequestId = (self.nextRequestId % 1000000) + 1
		if not liveSupport.Request(requestId, method, API + path, body, self.token):
			return False
		self.pending[requestId] = (kind, data, app.GetTime())
		return True

	def __SafeDispatch(self, kind, data, status, doc):
		try:
			self.__Dispatch(kind, data, status, doc)
		except Exception as e:
			import dbg
			dbg.TraceError("uiLiveSupport.%s: %s" % (kind, e))

	def __Bootstrap(self, silent):
		body = {"page": self.__Page(), "locale": "tr"}
		if self.__Request("bootstrap", "POST", "/widget/bootstrap", body):
			self.bootstrapping = True
			self.bootstrapSilent = silent
			self.nextBootstrapAt = 0.0
			if not silent:
				self.__System(TXT_CONNECTING)
		else:
			self.nextBootstrapAt = app.GetTime() + RETRY_STEPS[0]
			if not silent:
				self.__System(TXT_UNAVAILABLE)

	def __Sync(self):
		if not _IsId(self.conversationId):
			return
		path = "/sync?conversation_id=%s&after_seq=%d" % (self.conversationId, self.lastSeq)
		if self.__Request("sync", "GET", path, None):
			self.syncInFlight = True
		else:
			self.nextSyncAt = app.GetTime() + 2.0

	def __ProcessOutbox(self, now):
		if self.sending or not self.outbox or not self.ready:
			return
		item = self.outbox[0]
		if now < item["nextAt"]:
			return
		body = {"client_message_id": item["cmid"], "body": item["body"], "page": self.__Page()}
		if _IsId(self.conversationId):
			body["conversation_id"] = self.conversationId	# kapaliysa sunucu 30 dk icinde yeniden acar, sonra yeni gorusme
		if self.__Request("send", "POST", "/messages", body, item["cmid"]):
			self.sending = True
		else:
			item["nextAt"] = now + 2.0

	def __SendRating(self, value):
		conversationId = self.ratingConversationId
		self.awaitingRating = False
		if _IsId(conversationId):
			self.__Request("rating", "POST", "/conversations/%s/rating" % conversationId, {"rating": value})

	def __EnsureHuman(self):
		# Guvenlik agi: oyun ici gelen kutusunda yapay zeka kapali olmali; yine de bir yapay zeka yaniti gelirse temsilci istenir.
		conversationId = self.conversationId
		if not _IsId(conversationId) or self.human or not self.conversationActive or conversationId in self.humanRequested:
			return
		self.humanRequested[conversationId] = 1
		self.__Request("human", "POST", "/conversations/%s/human" % conversationId, None)

	def __MarkSeen(self):
		if self.lastSeq > self.lastSeenSeq:
			self.lastSeenSeq = self.lastSeq
			self.fileDirty = True
		now = app.GetTime()
		if _IsId(self.conversationId) and self.lastSeq > self.lastReadSentSeq and now >= self.nextReadAt:
			if self.__Request("read", "POST", "/conversations/%s/read" % self.conversationId, {"seq": self.lastSeq}):
				self.lastReadSentSeq = self.lastSeq
				self.nextReadAt = now + READ_INTERVAL
			else:
				self.nextReadAt = now + 1.0

	#################################################################
	## Yanitlar

	def __Dispatch(self, kind, data, status, doc):
		if "bootstrap" == kind:
			self.__OnBootstrap(status, doc)
		elif "sync" == kind:
			self.__OnSync(status, doc)
		elif "send" == kind:
			self.__OnSend(data, status, doc)
		elif "close" == kind:
			self.__OnClose(status, doc)
		elif "rating" == kind:
			self.__OnRating(status, doc)
		elif "human" == kind:
			if 200 == status and isinstance(doc, dict):
				self.__ApplyConversation(doc.get("conversation"))
		# "presence" / "read" yanitlari bilgi amaclidir; sunucuda uc yoksa (eski surum) sessizce yok sayilir

	def __OnBootstrap(self, status, doc):
		self.bootstrapping = False
		silent = self.bootstrapSilent
		now = app.GetTime()

		if 200 == status and isinstance(doc, dict):
			if not doc.get("available"):
				self.nextBootstrapAt = now + RETRY_STEPS[-1]
				if not silent or self.IsDialogVisible():
					self.__System(TXT_UNAVAILABLE)
				return

			token = doc.get("token")
			if _IsToken(token):
				self.token = token			# yeni ziyaretci oturumu (eskisi gecersizdi ya da ilk kez)
				self.fileDirty = True

			config = doc.get("config")
			self.config = config if isinstance(config, dict) else {}
			self.ready = True
			self.failCount = 0

			conversation = doc.get("conversation")
			if isinstance(conversation, dict):
				self.__ApplyConversation(conversation)
			else:
				# aktif ya da son 30 dk icinde kapanmis gorusme yok: dosyadaki eski kimlik kullanilmaz
				self.conversationId = ""
				self.conversationActive = False
				self.fileDirty = True
				self.__UpdateLeave()
				self.__UpdateEndButton()
			staffNew = self.__RenderMessages(doc.get("messages") or [])

			if self.IsDialogVisible():
				self.__MarkSeen()
				self.__ShowGreetingIfIdle()
			elif staffNew:
				self.__NotifyStaffMessage()
			self.__ReportReturned()

			self.nextSyncAt = now + (POLL_OPEN if self.IsDialogVisible() else POLL_BACKGROUND)
			return

		if 429 == status:
			self.nextBootstrapAt = now + _RetryAfter(doc, 10.0)
		else:
			self.failCount += 1
			self.nextBootstrapAt = now + RETRY_STEPS[min(self.failCount, len(RETRY_STEPS)) - 1]

		if not silent or (self.IsDialogVisible() and self.failCount <= 1):	# tekrar denemelerde uyari yinelenmez
			(code, message, retryAfter) = _ErrorInfo(doc)
			self.__System(message or TXT_UNAVAILABLE)

	def __OnSync(self, status, doc):
		self.syncInFlight = False
		now = app.GetTime()

		if 200 == status and isinstance(doc, dict):
			self.failCount = 0
			self.__ApplyConversation(doc.get("conversation"))
			if self.__RenderMessages(doc.get("messages") or []):
				if self.IsDialogVisible():
					self.__MarkSeen()
				else:
					self.__NotifyStaffMessage()

			if doc.get("complete") is False:
				self.nextSyncAt = now + RESYNC_GAP	# 200'den fazla mesaj: devami kisa aralikla
			else:
				interval = self.__PollInterval()
				self.nextSyncAt = now + (interval if interval is not None else POLL_BACKGROUND)
			return

		if 401 == status:
			self.__InvalidateToken()
			return

		if 429 == status:
			self.nextSyncAt = now + _RetryAfter(doc, 10.0)
		else:
			self.failCount += 1
			self.nextSyncAt = now + RETRY_STEPS[min(self.failCount, len(RETRY_STEPS)) - 1]

	def __OnSend(self, clientMessageId, status, doc):
		self.sending = False
		if not self.outbox or self.outbox[0]["cmid"] != clientMessageId:
			return
		item = self.outbox[0]
		now = app.GetTime()

		if status in (200, 201) and isinstance(doc, dict):
			self.outbox.pop(0)
			self.__ApplyConversation(doc.get("conversation"))
			message = doc.get("message")
			if isinstance(message, dict):
				self.__RenderMessages([message])	# kendi mesaji zaten yazildi; sira/kimlik kaydi
			self.__RenderMessages(doc.get("extra") or [])
			self.nextSyncAt = min(self.nextSyncAt, now + 1.0)
			return

		if 401 == status:
			self.__InvalidateToken()		# mesaj kuyrukta kalir; yeni oturum acilinca ayni kimlikle gider
			return

		if 429 == status:
			item["nextAt"] = now + _RetryAfter(doc, 10.0)
			return

		if status >= 400 and status < 500:
			self.outbox.pop(0)
			self.sentClientIds.pop(clientMessageId, None)
			self.__System(TXT_SEND_FAIL % _Reason(status, doc))
			return

		# ag hatasi / 5xx: ayni client_message_id ile tekrar (sunucu cift kaydi engeller)
		item["tries"] += 1
		if item["tries"] > len(RETRY_STEPS):
			self.outbox.pop(0)
			self.sentClientIds.pop(clientMessageId, None)
			self.__System(TXT_SEND_GIVEUP)
			return
		if 1 == item["tries"]:
			self.__System(TXT_SEND_RETRY)
		item["nextAt"] = now + RETRY_STEPS[item["tries"] - 1]

	def __OnClose(self, status, doc):
		if 200 == status and isinstance(doc, dict):
			self.__System(TXT_ENDED)
			self.__ApplyConversation(doc.get("conversation"))
			return
		if 401 == status:
			self.__InvalidateToken()
		self.__System(TXT_ACTION_FAIL % _Reason(status, doc))

	def __OnRating(self, status, doc):
		if 200 == status:
			self.__System(TXT_RATE_THANKS)
			return
		self.__System(TXT_ACTION_FAIL % _Reason(status, doc))

	def __InvalidateToken(self):
		self.token = ""
		self.fileDirty = True
		self.ready = False
		self.__UpdateLeave()
		if not self.bootstrapping:
			self.__Bootstrap(True)

	#################################################################
	## Durum

	def __ApplyConversation(self, conversation):
		if not isinstance(conversation, dict):
			return
		conversationId = conversation.get("id")
		if not _IsId(conversationId):
			return

		if conversationId != self.conversationId:
			# yeni gorusme: sira numaralari gorusme basinadir
			self.conversationId = conversationId
			self.lastSeq = 0
			self.lastSeenSeq = 0
			self.lastReadSentSeq = 0
			self.assigneeName = ""
			self.queuePosition = None
			self.fileDirty = True

		wasActive = self.conversationActive
		isActive = bool(conversation.get("active"))
		self.conversationActive = isActive
		if wasActive != isActive:
			self.fileDirty = True
		self.human = bool(conversation.get("human"))
		self.__UpdateLeave()

		assignee = conversation.get("assignee")
		assigneeName = assignee.get("name") if isinstance(assignee, dict) else None
		if isActive and assigneeName and assigneeName != self.assigneeName:
			self.assigneeName = assigneeName
			self.__System(TXT_ASSIGNED % assigneeName)

		queue = conversation.get("queue")
		if isActive and not assigneeName and isinstance(queue, (int, long)) and queue > 0:
			if queue != self.queuePosition:
				self.queuePosition = queue
				self.__System(TXT_QUEUE % queue)
		else:
			self.queuePosition = None

		if wasActive and not isActive:
			ratingEnabled = self.config.get("rating_enabled", True)
			if ratingEnabled and conversation.get("rating") is None:
				self.awaitingRating = True
				self.ratingConversationId = conversationId
				self.__System(TXT_RATE_PROMPT)

		self.__UpdateEndButton()

	def __RenderMessages(self, messages):
		staffNew = False
		if not isinstance(messages, list):
			return False

		if len(messages) > RENDER_PER_BATCH:
			# siralari kaydet, yalniz son RENDER_PER_BATCH mesaji yaz (uzun cevrimdisi / kotu niyetli yanit donma yaratmasin)
			for message in messages[:-RENDER_PER_BATCH]:
				if isinstance(message, dict):
					seq = message.get("seq")
					if isinstance(seq, (int, long)) and seq > self.lastSeq:
						self.lastSeq = seq
					if message.get("sender") in ("agent", "ai") and isinstance(seq, (int, long)) and seq > self.lastSeenSeq:
						staffNew = True
			self.__System(TXT_SKIPPED % (len(messages) - RENDER_PER_BATCH))
			messages = messages[-RENDER_PER_BATCH:]

		self.deferTrim = True		# tek yanitta cok satir: RAM siniri kirpmasi sonda bir kez (her satirda yeniden yazim yok)
		try:
			for message in messages:
				if not isinstance(message, dict):
					continue

				seq = message.get("seq")
				if isinstance(seq, (int, long)) and seq > self.lastSeq:
					self.lastSeq = seq

				messageId = message.get("id")
				if not isinstance(messageId, str) or not messageId or messageId in self.renderedIds:
					continue
				self.renderedIds[messageId] = 1

				sender = message.get("sender")
				body = message.get("body")

				if "visitor" == sender:
					clientMessageId = message.get("client_message_id")
					if clientMessageId and clientMessageId in self.sentClientIds:
						del self.sentClientIds[clientMessageId]	# oyuncu yazdiginda zaten gosterildi
					else:
						self.__AppendLines(chat.WHISPER_TYPE_CHAT, self.charName, body)
				elif sender in ("agent", "ai"):
					author = message.get("author")
					name = author.get("name") if isinstance(author, dict) else None
					self.__AppendLines(chat.WHISPER_TYPE_CHAT, name or AGENT_DEFAULT, body, AGENT_COLOR)
					if isinstance(seq, (int, long)) and seq > self.lastSeenSeq:
						staffNew = True
					if "ai" == sender:
						self.__EnsureHuman()
				else:
					self.__AppendLines(chat.WHISPER_TYPE_SYSTEM, "", body)

				attachments = message.get("attachments")
				if isinstance(attachments, list):
					for attachment in attachments:
						if isinstance(attachment, dict):
							self.__System(TXT_ATTACHMENT % str(attachment.get("name") or "?"))
		finally:
			self.deferTrim = False
		if len(self.lines) > LINE_LIMIT:
			self.__TrimLines()

		if len(self.renderedIds) > 3000:
			self.renderedIds = {}	# sonraki mesajlar zaten after_seq ile gelir; tekrar yazilmaz

		return staffNew

	def __PollInterval(self):
		if self.IsDialogVisible():
			return POLL_OPEN
		if self.conversationActive:
			return POLL_BACKGROUND
		return None

	def __UpdateEndButton(self):
		if self.dialog:
			self.dialog.SetEndButtonVisible(self.conversationActive)

	def __ShowGreetingIfIdle(self):
		if self.greetingShown or self.conversationId:
			return
		self.greetingShown = True
		availability = self.config.get("availability")
		if isinstance(availability, dict) and not availability.get("online", True):
			self.__System(self.config.get("offline_message") or TXT_OFFLINE)
		else:
			self.__System(self.config.get("greeting") or TXT_WELCOME)

	def __NotifyStaffMessage(self):
		self.unread = True
		self.fileDirty = True
		self.__ShowButton(True)
		chat.AppendChat(chat.CHAT_TYPE_INFO, TXT_NEW_MESSAGE)

	#################################################################
	## Gorunum

	def __System(self, text):
		self.__AppendLines(chat.WHISPER_TYPE_SYSTEM, "", text)

	def __AppendLines(self, whisperType, name, body, color = ""):
		if not body:
			return
		# "|" metin motorunda renk/baglanti/emoji kodudur: sunucudan gelen metinde etkisiz hale getirilir
		name = _Clean(str(name or "")[:60]).replace("\n", " ")	# ad tek satir
		text = str(body)
		if len(text) > DISPLAY_MAX:
			text = text[:DISPLAY_MAX] + " ..."
		text = _Clean(text)
		first = True
		count = 0
		for line in text.split("\n"):
			line = line.rstrip()
			if first:
				first = False
				out = (name + " : " + line) if name else line
			elif line:
				out = "    " + line
			else:
				continue
			count += 1
			if count > MESSAGE_LINES_MAX:
				out = "    ..."			# cok satirli mesaj kisaltilir (tamami panelde)
			# renk kodu YALNIZ temizlenmis metnin disina eklenir (sunucu metni renk/baglanti kodu uretemez)
			self.__Emit(whisperType, (color + out + "|r") if color else out)
			if count > MESSAGE_LINES_MAX:
				break

	def __Emit(self, whisperType, text):
		self.lines.append((whisperType, text))
		_AppendWhisper(whisperType, text)
		if 1 == len(self.lines) and self.dialog:
			# fisilti nesnesi ilk satirla olusur (C++ varsayilan kutusu 120 px): pencere olcusu hemen uygulanir
			chat.SetWhisperBoxSize(TARGET_NAME, self.dialog.GetWidth() - 50, self.dialog.GetHeight() - 90)
		if len(self.lines) > LINE_LIMIT and not self.deferTrim:
			self.__TrimLines()

	def __TrimLines(self):
		# RAM ust siniri: eski satirlar atilir, son LINE_KEEP satir yeniden yazilir (seyrek; tek yanitta en fazla bir kez)
		self.lines = self.lines[-LINE_KEEP:]
		self.__RebuildWhisper()

	def __RebuildWhisper(self):
		if not self.lines:
			return
		chat.ClearWhisper(TARGET_NAME)	# nesneyi haritadan siler; ardindan CreateWhisper sizinti yapmaz
		chat.CreateWhisper(TARGET_NAME)
		if self.dialog:
			chat.SetWhisperBoxSize(TARGET_NAME, self.dialog.GetWidth() - 50, self.dialog.GetHeight() - 90)
		for (lineType, lineText) in self.lines:
			_AppendWhisper(lineType, lineText)

	def __ShowButton(self, flash):
		if not self.interface:
			return
		if not self.button:
			button = uiWhisper.WhisperButton()
			button.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			button.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			button.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			button.SetToolTipTextWithColor(TARGET_NAME, 0xffffa200)
			button.ToolTipText.SetHorizontalAlignCenter()
			button.SetEvent(_OpenFromButton)
			button.name = TARGET_NAME
			button.Show()
			self.button = button
			self.interface.AddExternalWhisperButton(button)
		if flash:
			self.button.Flash()

	def __HideButton(self):
		if not self.button:
			return
		if self.interface:
			self.interface.RemoveExternalWhisperButton(self.button)
		self.button.SetEvent(0)
		self.button.Hide()
		self.button = None

	#################################################################
	## Karakter / kayitli oturum

	def __CheckCharacter(self):
		name = player.GetName()
		if not name:
			return False
		if name != self.charName or self.attachServer != self.charServer:
			if self.charName:
				# baska karakter: onceki gorusmeye "oyundan cikti" notu (kuyruga alinir, Reset atmaz), sonra
				# onceki karakterin istekleri ve yazismalari atilir
				if HAS_LEAVE:
					if self.leaveKey:
						liveSupport.FireLeave()
					liveSupport.LeaveTimer(0)
				liveSupport.Reset()
				self.pending = {}
				chat.ClearWhisper(TARGET_NAME)
				self.__HideButton()
				if self.dialog:
					self.dialog.Hide()
			self.__ResetState(name)
			self.charServer = self.attachServer
			self.fileKey = name + "@" + self.charServer
			self.__LoadFile()
			if self.savedActive:
				# suren gorusme / okunmamis yanit vardi: girista sessiz kontrol; oyuncu donmus sayilir
				self.active = True
				self.maybeAway = True
				self.wantSilentBootstrap = True
		return True

	def __SendPresence(self, state):
		# Temsilciye ic not (yalniz temsilciler gorur): closed = pencereyi kapatti, returned = tekrar cevrimici
		if self.token and self.conversationActive and _IsId(self.conversationId):
			self.__Request("presence", "POST", "/conversations/%s/presence" % self.conversationId, {"state": state})

	def __ReportReturned(self):
		if self.maybeAway and self.ready and self.conversationActive:
			self.maybeAway = False
			self.__SendPresence("returned")

	def __UpdateLeave(self):
		# Suren gorusme varken "oyuncu oyundan cikti" bildirimi C++ modulunde hazirda tutulur: oyun kapanirken
		# (en fazla 2 sn), karakter degisiminde ya da cikis yapilip LEAVE_GRACE_MS icinde donulmezse gonderilir.
		if not HAS_LEAVE:
			return
		key = ""
		if self.token and self.conversationActive and _IsId(self.conversationId):
			key = self.token + "|" + self.conversationId
		if key == self.leaveKey:
			return
		if key:
			if liveSupport.SetLeave(API + "/conversations/%s/presence" % self.conversationId, {"state": "left"}, self.token):
				self.leaveKey = key
		else:
			liveSupport.ClearLeave()
			self.leaveKey = ""

	def __Page(self):
		title = TXT_PAGE_TITLE % self.charName
		try:
			title += " | Lv %d" % player.GetStatus(player.LEVEL)
		except:
			pass
		try:
			serverInfo = net.GetServerInfo()
			if serverInfo:
				title += " | " + serverInfo.strip()
		except:
			pass
		return {"url": PAGE_URL, "title": title[:190]}

	def __FilePath(self):
		if not self.fileKey:
			return ""
		safeName = "".join(["%02x" % ord(c) for c in self.fileKey])	# karakter@sunucu; Turkce harfli adlar da cakismaz, codec gerekmez
		return constInfo.CLIENT_YOL + (TOKEN_FILE % safeName)

	def __LoadFile(self):
		path = self.__FilePath()
		if not path:
			return
		try:
			handle = open(path, "r")
			data = handle.read(16384)		# ust sinir: bozuk / buyutulmus dosya RAM'i sisirmez (gecerli dosya ~1 KB)
			handle.close()
		except:
			return
		try:
			parsed = _ParseSession(data.strip())
		except Exception as e:
			_LogError("LoadFile", e)		# bozuk dosya yok sayilir; bir sonraki kayitta yeniden yazilir
			parsed = None
		if not parsed:
			return
		(self.token, self.conversationId, self.lastSeenSeq, self.savedActive, legacy) = parsed
		if legacy:
			self.fileDirty = True

	def __SaveFile(self):
		self.fileDirty = False
		path = self.__FilePath()
		if not path:
			return
		# Oturum kalici tutulur (ayni oyuncu hep ayni ziyaretci -> panelde "Onceki konusmalar" dolu gelir), ama Windows
		# DPAPI ile bu Windows kullanicisina bagli sifrelenir: baska bilgisayara / hesaba kopyalanan dosya ise yaramaz.
		# Anahtar gecersizse ya da sifreleme yoksa dosya silinir (oturum yalniz bellekte kalir).
		protected = ""
		if self.token and HAS_PROTECT:
			flag = "1" if (self.conversationActive or self.unread) else "0"
			protected = liveSupport.Protect("%s|%s|%d|%s" % (self.token, self.conversationId, self.lastSeenSeq, flag))
		try:
			if not protected:
				if os.path.exists(path):
					os.remove(path)
				return
			handle = open(path, "w")
			handle.write("v2|" + protected)
			handle.close()
		except:
			pass

#####################################################################

_manager = None

def GetManager():
	global _manager
	if _manager is None:
		_manager = LiveSupportManager()
	return _manager
