# DUMPED FROM LIVE COMPILE: uipvpduel.py (len=27340)
import ui
import app
import grp
import wndMgr
import localeInfo
import chat
import net
import playerSettingModule

# --- Sabitler ---------------------------------------------------------------

ARENA_COUNT = 8   # server MAX_ARENA; yalniz maci olan satirlar gorunur (__Relayout)
IMG_DIR = "d:/ymir work/ui/game/pvp_duel/"
ALPHA = 0.6

# Turnuva durumu (PvPTrnInfo status alani)
STATUS_IDLE      = 0
STATUS_PREP      = 1   # kayit acik
STATUS_REGCLOSED = 2   # kayit kapali
STATUS_RUNNING   = 3   # devam ediyor
STATUS_DONE      = 4
STATUS_CANCEL    = 5

# Arena fazi (PvPTrnArena phase alani)
PHASE_EMPTY  = 0
PHASE_FREEZE = 1   # donma/geri sayim
PHASE_FIGHT  = 2   # dovus (VS)
PHASE_BREAK  = 3   # ara (geri sayim)

# Satir olcumleri (referans yerlesime gore)
ROW_W       = 402
ROW_H       = 46
ROW_GAP     = 5
HEADER_H    = 24
AV_W        = 43
BAR_W       = 123
GAUGE_H     = 11
CENTER_W    = 37

X_LEFT_AV   = 5      # sol avatar
X_LEFT_COL  = 53     # 5 + 43 + 5  (sol isim/gauge)
X_LEFT_END  = 176    # 53 + 123    (sol skor sag hizasi)
X_CENTER    = 184    # 176 + 8     (merkez: vs/loading)
X_RIGHT_COL = 226    # 184 + 37 + 5 (sag skor/gauge)
X_RIGHT_END = 349    # 226 + 123   (sag isim sag hizasi)
X_RIGHT_AV  = 354    # 349 + 5     (sag avatar)

GAUGE_FRAME_COUNT = 7   # hp_red/01..07.tga  (08 YOK)

# Renkler
COLOR_ROW_BG = grp.GenerateColor(0.267, 0.267, 0.267, ALPHA)   # koyu yari saydam
COLOR_HEADER = grp.GenerateColor(0.078, 0.086, 0.117, 0.75)    # koyu baslik seridi
NAME_R, NAME_G, NAME_B = 0.98, 0.86, 0.45   # altin - isimler
ROUND_R, ROUND_G, ROUND_B = 0.75, 0.90, 1.0 # acik mavi - tur adi

# Irk basina yuz resmi (uicharacter.py FACE_IMAGE_DICT ile ayni dosyalar): cinsiyet dogru gorunur.
# playerSettingModule.FACE_IMAGE_DICT yalniz 4 job yuzu icerir (ninja erkek / sura kadin vb. eksik kaliyordu).
FACE_BY_RACE = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}
if getattr(app, "ENABLE_WOLFMAN_CHARACTER", 0) and hasattr(playerSettingModule, "RACE_WOLFMAN_M"):
	FACE_BY_RACE[playerSettingModule.RACE_WOLFMAN_M] = "icon/face/wolfman_m.tga"

AV_H = ROW_H - 4   # avatar kutusu yuksekligi (resim buyukse orantili kucultulur)

# Kurallar penceresi satir anahtarlari (locale'de tanimli olmali; eksikse atlanir)
RULE_LINE_KEYS = [
	"PVP_TRN_RULE_1", "PVP_TRN_RULE_2", "PVP_TRN_RULE_3", "PVP_TRN_RULE_4",
	"PVP_TRN_RULE_5", "PVP_TRN_RULE_6", "PVP_TRN_RULE_7", "PVP_TRN_RULE_8",
]


# ============================================================================
# A) SKORBOARD - 4 arena
# ============================================================================
class PvPTournamentBoard(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def __Initialize(self):
		# Rule 2: tum instance alanlari burada sifirlanir
		self.isActive = False
		self.headerBar = None
		self.statusText = None
		self.roundText = None
		self.countText = None
		self.rulesButton = None
		self.rulesEvent = None
		self.arenas = []

	def Destroy(self):
		# ui.WindowDestroy bu fork'ta yok; referanslar elle birakilir.
		self.Hide()
		self.rulesEvent = None
		self.__Initialize()

	# --- kurulum ---------------------------------------------------------
	def __LoadWindow(self):
		self.SetWindowName("PvPTournamentBoard")
		self.AddFlag("not_pick")

		self.SetSize(ROW_W, HEADER_H)

		self.__MakeHeader()
		for i in xrange(ARENA_COUNT):
			self.__MakeArenaRow(i)
		self.__Relayout()

		self.Hide()

	def __Relayout(self):
		# Yalniz maci olan arenalar ust uste dizilir: 4 arenalik turnuvada 4, buyuk turnuvada 8 satir;
		# bos arena yer kaplamaz. Pencere sol altta sabit kalir (yukari dogru uzar).
		visible = 0
		for arena in self.arenas:
			bar = arena["bar"]
			if arena["active"]:
				bar.SetPosition(0, HEADER_H + visible * (ROW_H + ROW_GAP))
				if not bar.IsShow():
					bar.Show()
				visible += 1
			elif bar.IsShow():
				bar.Hide()
		windowHeight = HEADER_H + visible * (ROW_H + ROW_GAP)
		self.SetSize(ROW_W, windowHeight)
		posY = wndMgr.GetScreenHeight() - windowHeight - 120
		if posY < 5:
			posY = 5
		self.SetPosition(5, posY)

	def __MakeHeader(self):
		bar = ui.Bar()
		bar.SetParent(self)
		bar.AddFlag("not_pick")
		bar.SetSize(ROW_W, HEADER_H)
		bar.SetPosition(0, 0)
		bar.SetColor(COLOR_HEADER)
		bar.Show()
		self.headerBar = bar

		status = ui.TextLine()
		status.SetParent(bar)
		status.AddFlag("not_pick")
		status.SetPosition(8, 5)
		status.SetHorizontalAlignLeft()
		status.SetOutline()
		status.Show()
		self.statusText = status

		roundLine = ui.TextLine()
		roundLine.SetParent(bar)
		roundLine.AddFlag("not_pick")
		roundLine.SetPosition(ROW_W / 2, 5)
		roundLine.SetHorizontalAlignCenter()
		roundLine.SetFontColor(ROUND_R, ROUND_G, ROUND_B)
		roundLine.SetOutline()
		roundLine.Show()
		self.roundText = roundLine

		count = ui.TextLine()
		count.SetParent(bar)
		count.AddFlag("not_pick")
		count.SetPosition(ROW_W - 66, 5)
		count.SetHorizontalAlignRight()
		count.SetOutline()
		count.Show()
		self.countText = count

		# Kurallar butonu - HUD icindeki tek tiklanabilir eleman
		rulesBtn = ui.Button()
		rulesBtn.SetParent(bar)
		rulesBtn.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
		rulesBtn.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
		rulesBtn.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
		rulesBtn.SetPosition(ROW_W - 62, 2)
		rulesBtn.SetText(localeInfo.PVP_TRN_RULES_BTN)
		rulesBtn.SAFE_SetEvent(self.__OnClickRules)
		rulesBtn.Show()
		self.rulesButton = rulesBtn

	def __MakeArenaRow(self, index):
		rowY = HEADER_H + index * (ROW_H + ROW_GAP)

		bar = ui.Bar()
		bar.SetParent(self)
		bar.AddFlag("not_pick")
		bar.SetSize(ROW_W, ROW_H)
		bar.SetPosition(0, rowY)
		bar.SetColor(COLOR_ROW_BG)
		bar.Hide()  # satir, arenada mac oldugunda __Relayout ile gosterilir

		# Avatarlar (arka planda)
		leftAvatar = self.__MakeAvatar(bar, X_LEFT_AV)
		rightAvatar = self.__MakeAvatar(bar, X_RIGHT_AV)

		# Isimler
		leftName = self.__MakeName(bar, X_LEFT_COL, "left")
		rightName = self.__MakeName(bar, X_RIGHT_END, "right")

		# HP gauge'lari
		leftGauge = self.__MakeGauge(bar, X_LEFT_COL)
		rightGauge = self.__MakeGauge(bar, X_RIGHT_COL)

		# Skorlar (merkeze yakin, buyuk)
		leftScore = self.__MakeScore(bar, X_LEFT_END, "right")
		rightScore = self.__MakeScore(bar, X_RIGHT_COL, "left")

		# Merkez: loading (donen), sayac, vs (en ust)
		loadingImg = ui.ExpandedImageBox()
		loadingImg.SetParent(bar)
		loadingImg.AddFlag("not_pick")
		loadingImg.LoadImage(IMG_DIR + "loading.tga")
		loadingImg.SetPosition(X_CENTER, 1)
		loadingImg.SetAlpha(ALPHA)
		loadingImg.Hide()

		vsImg = ui.ExpandedImageBox()
		vsImg.SetParent(bar)
		vsImg.AddFlag("not_pick")
		vsImg.LoadImage(IMG_DIR + "vs.tga")
		vsImg.SetPosition(X_CENTER, 1)
		vsImg.SetAlpha(ALPHA)
		vsImg.Hide()

		countLine = ui.TextLine()
		countLine.SetParent(bar)
		countLine.AddFlag("not_pick")
		countLine.SetPosition(X_CENTER + CENTER_W / 2, 14)
		countLine.SetHorizontalAlignCenter()
		countLine.SetFontName("Tahoma:14")
		countLine.SetOutline()
		countLine.Hide()

		arena = {
			"bar"         : bar,
			"leftAvatar"  : leftAvatar,
			"rightAvatar" : rightAvatar,
			"leftName"    : leftName,
			"rightName"   : rightName,
			"leftGauge"   : leftGauge,
			"rightGauge"  : rightGauge,
			"leftScore"   : leftScore,
			"rightScore"  : rightScore,
			"loading"     : loadingImg,
			"vs"          : vsImg,
			"count"       : countLine,
			"phase"       : PHASE_EMPTY,
			"target"      : 0,
			"rotation"    : 0,
			"active"      : False,
		}
		self.arenas.append(arena)
		self.__ClearArenaDict(arena)

	def __MakeAvatar(self, parent, x):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.AddFlag("not_pick")
		img.SetPosition(x, 2)
		img.SetAlpha(ALPHA)
		img.Hide()
		return img

	def __MakeName(self, parent, x, align):
		name = ui.TextLine()
		name.SetParent(parent)
		name.AddFlag("not_pick")
		name.SetPosition(x, 7)
		if align == "right":
			name.SetHorizontalAlignRight()
		else:
			name.SetHorizontalAlignLeft()
		name.SetFontColor(NAME_R, NAME_G, NAME_B)
		name.SetOutline()
		name.Hide()
		return name

	def __MakeGauge(self, parent, x):
		# ExpandedImageBox (AniImageBox DEGIL): dosyadaki loading/vs/avatar ile ayni tip ->
		# parent'a gore dogru konumlanir ve ANIMASYON YAPMAZ. AniImageBox 7 kareyi surekli
		# dondururdu (sacma gorunum) ve bu fork'ta konum/pozisyon sorunlu olabiliyordu.
		# Tam bar tek gorsel yuklenir, doluluk SetRenderingRect ile kirpilarak gosterilir.
		gauge = ui.ExpandedImageBox()
		gauge.SetParent(parent)
		gauge.AddFlag("not_pick")
		gauge.SetPosition(x, 28)
		gauge.LoadImage(IMG_DIR + "hp_red/%02d.tga" % GAUGE_FRAME_COUNT)  # tam (dolu) bar
		gauge.Hide()
		return gauge

	def __MakeScore(self, parent, x, align):
		score = ui.TextLine()
		score.SetParent(parent)
		score.AddFlag("not_pick")
		score.SetPosition(x, 3)
		score.SetFontName("Tahoma:14")
		if align == "right":
			score.SetHorizontalAlignRight()
		else:
			score.SetHorizontalAlignLeft()
		score.SetOutline()
		score.Hide()
		return score

	# --- kurallar butonu koprusu ----------------------------------------
	def SetRulesEvent(self, event):
		# game.py bunu ui.__mem_func__(...) ile sarmalanmis olarak verir (zayif ref)
		self.rulesEvent = event

	def __OnClickRules(self):
		if self.rulesEvent:
			self.rulesEvent()

	# --- genel API (handler'lar buradan cagirir) ------------------------
	def SetInfo(self, status, count, roundName):
		# status ve count string gelir (stringCommander)
		try:
			status = int(status)
		except ValueError:
			status = STATUS_IDLE
		try:
			count = int(count)
		except ValueError:
			count = 0

		self.statusText.SetText(self.__StatusText(status))

		if roundName == "-" or roundName == "":
			self.roundText.SetText(localeInfo.PVP_TRN_ROUND_NONE)
		else:
			self.roundText.SetText(roundName.replace("_", " "))

		self.countText.SetText("%s %d" % (localeInfo.PVP_TRN_REGISTERED, count))

		if status in (STATUS_PREP, STATUS_REGCLOSED, STATUS_RUNNING):
			# SetTop yalnizca gizli->gorunur gecisinde; aksi halde her kayit
			# guncellemesinde HUD, oyuncunun acik penceresinin (envanter vb.)
			# ustune firlar.
			if not self.isActive:
				self.isActive = True
				self.Show()
				self.SetTop()
		else:
			self.isActive = False
			self.Hide()

	def SetArena(self, idx, phase, endsec, r1, hp1, sc1, n1, r2, hp2, sc2, n2):
		arena = self.__GetArena(idx)
		if arena is None:
			return
		if not arena["active"]:
			arena["active"] = True
			self.__Relayout()
		try:
			phase = int(phase)
		except ValueError:
			phase = PHASE_EMPTY
		try:
			endsec = int(endsec)
		except ValueError:
			endsec = 0

		arena["phase"] = phase
		if endsec > 0:
			# Yerel hedef zaman damgasi; OnUpdate geri sayar
			arena["target"] = app.GetGlobalTimeStamp() + endsec
		else:
			arena["target"] = 0

		self.__SetSide(arena, "left", r1, hp1, sc1, n1)
		self.__SetSide(arena, "right", r2, hp2, sc2, n2)

	def ClearArena(self, idx):
		arena = self.__GetArena(idx)
		if arena is None:
			return
		self.__ClearArenaDict(arena)
		if arena["active"]:
			arena["active"] = False
			self.__Relayout()

	# --- ic yardimcilar --------------------------------------------------
	def __GetArena(self, idx):
		try:
			i = int(idx) - 1
		except ValueError:
			return None
		if i < 0 or i >= len(self.arenas):
			return None
		return self.arenas[i]

	def __StatusText(self, status):
		table = {
			STATUS_IDLE      : localeInfo.PVP_TRN_STATUS_IDLE,
			STATUS_PREP      : localeInfo.PVP_TRN_STATUS_PREP,
			STATUS_REGCLOSED : localeInfo.PVP_TRN_STATUS_REGCLOSED,
			STATUS_RUNNING   : localeInfo.PVP_TRN_STATUS_RUNNING,
			STATUS_DONE      : localeInfo.PVP_TRN_STATUS_DONE,
			STATUS_CANCEL    : localeInfo.PVP_TRN_STATUS_CANCEL,
		}
		if status in table:
			return table[status]
		return localeInfo.PVP_TRN_STATUS_IDLE

	def __SetSide(self, arena, side, race, hp, score, name):
		avatar = arena[side + "Avatar"]
		nameLine = arena[side + "Name"]
		gauge = arena[side + "Gauge"]
		scoreLine = arena[side + "Score"]

		# Bos slot
		if name == "-" or name == "":
			if nameLine.IsShow():
				nameLine.Hide()
			if avatar.IsShow():
				avatar.Hide()
			if gauge.IsShow():
				gauge.Hide()
			if scoreLine.IsShow():
				scoreLine.Hide()
			return

		nameLine.SetText(name)
		if not nameLine.IsShow():
			nameLine.Show()

		self.__SetRace(avatar, race)

		try:
			scoreValue = int(score)
		except ValueError:
			scoreValue = 0
		scoreLine.SetText(str(scoreValue))
		if not scoreLine.IsShow():
			scoreLine.Show()

		self.__SetGauge(gauge, hp, side == "right")

	def __SetRace(self, avatar, race):
		try:
			raceValue = int(race)
		except ValueError:
			raceValue = -1
		imageName = FACE_BY_RACE.get(raceValue, "")
		if not imageName:
			if avatar.IsShow():
				avatar.Hide()
			return
		avatar.LoadImage(imageName)
		if avatar.GetWidth() <= 0 or avatar.GetHeight() <= 0:
			# pack'te irk resmi yoksa job yuzune dus (0..3 job, 4..7 ayni job'un diger cinsiyeti)
			jobFaces = playerSettingModule.FACE_IMAGE_DICT
			job = raceValue - 4 if raceValue >= 4 and raceValue <= 7 else raceValue
			if job not in jobFaces:
				if avatar.IsShow():
					avatar.Hide()
				return
			avatar.LoadImage(jobFaces[job])
		# Resim kutudan buyukse orantili kucult (icon/face boyutu pack'e gore degisebilir).
		width, height = avatar.GetWidth(), avatar.GetHeight()
		scale = 1.0
		if width > 0 and height > 0 and (width > AV_W or height > AV_H):
			scale = min(float(AV_W) / width, float(AV_H) / height)
		avatar.SetScale(scale, scale)
		# LoadImage image instance'i yeniden yaratir; alpha her yuklemeden SONRA verilmeli.
		avatar.SetAlpha(ALPHA)
		if not avatar.IsShow():
			avatar.Show()

	def __SetGauge(self, gauge, hp, reverse):
		try:
			hpValue = int(hp)
		except ValueError:
			hpValue = 0
		if hpValue < 0:
			hpValue = 0
		if hpValue > 100:
			hpValue = 100
		if hpValue == 0:
			if gauge.IsShow():
				gauge.Hide()
			return
		self.__ApplyGaugePercentage(gauge, hpValue, reverse)
		if not gauge.IsShow():
			gauge.Show()

	def __ApplyGaugePercentage(self, gauge, hp, reverse):
		# Tam bar gorseli kirpilarak doluluk gosterilir. Ofset NEGATIF olmali (client
		# konvansiyonu; pozitif verirsek ters/bozuk dolar).
		ratio = float(hp) / 100.0
		if ratio < 0.0: ratio = 0.0
		if ratio > 1.0: ratio = 1.0
		if reverse:
			# sag oyuncu: soldan kirp -> bar merkeze dogru bosalir (aynali)
			wndMgr.SetRenderingRect(gauge.hWnd, ratio - 1.0, 0.0, 0.0, 0.0)
		else:
			# sol oyuncu: sagdan kirp -> bar merkezden disa dogru bosalir
			wndMgr.SetRenderingRect(gauge.hWnd, 0.0, 0.0, ratio - 1.0, 0.0)

	def __ClearArenaDict(self, arena):
		arena["phase"] = PHASE_EMPTY
		arena["target"] = 0
		arena["rotation"] = 0
		keys = (
			"leftName", "rightName", "leftScore", "rightScore",
			"leftAvatar", "rightAvatar", "leftGauge", "rightGauge",
			"loading", "vs", "count",
		)
		for key in keys:
			w = arena[key]
			if w.IsShow():
				w.Hide()

	# --- her kare: geri sayim / spinner / vs ----------------------------
	def OnUpdate(self):
		if not self.isActive:
			return
		now = app.GetGlobalTimeStamp()
		for arena in self.arenas:
			self.__UpdateArenaCenter(arena, now)

	def __UpdateArenaCenter(self, arena, now):
		loading = arena["loading"]
		vs = arena["vs"]
		count = arena["count"]

		# Bos arena -> merkez kapali
		if not arena["leftName"].IsShow() and not arena["rightName"].IsShow():
			if loading.IsShow():
				loading.Hide()
			if vs.IsShow():
				vs.Hide()
			if count.IsShow():
				count.Hide()
			return

		phase = arena["phase"]

		if phase == PHASE_FIGHT:
			# Dovus: VS sabit
			if loading.IsShow():
				loading.Hide()
			if count.IsShow():
				count.Hide()
			if not vs.IsShow():
				vs.Show()
			return

		if phase == PHASE_FREEZE or phase == PHASE_BREAK:
			leftTime = arena["target"] - now
			if leftTime < 0:
				leftTime = 0
			if vs.IsShow():
				vs.Hide()
			count.SetText(str(leftTime))
			if not count.IsShow():
				count.Show()
			rotation = arena["rotation"] + 5
			if rotation > 360:
				rotation = 0
			arena["rotation"] = rotation
			loading.SetRotation(rotation)
			if not loading.IsShow():
				loading.Show()
			return

		# PHASE_EMPTY ama slot dolu (gecis) -> merkez kapali
		if loading.IsShow():
			loading.Hide()
		if vs.IsShow():
			vs.Hide()
		if count.IsShow():
			count.Hide()


# ============================================================================
# B) KURALLAR PENCERESI
# ============================================================================
class PvPTournamentRules(ui.BoardWithTitleBar):
	WIDTH = 580
	MAX_LINE_CHARS = 74   # Arial:12 ~6.5 px/karakter; olcum calismasa da satir pencereye sigar
	MARGIN_X = 24
	TEXT_TOP = 42
	LINE_STEP = 18

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def __Initialize(self):
		self.bodyLines = []
		self.acceptButton = None
		self.rejectButton = None
		self.closeButton = None

	def Destroy(self):
		# ui.WindowDestroy bu fork'ta yok; referanslar elle birakilir.
		self.Hide()
		self.__Initialize()

	def __LoadWindow(self):
		self.AddFlag("movable")
		# "float" yoksa CWindow::SetTop hicbir sey yapmaz (Open/OpenForAccept SetTop cagirir).
		self.AddFlag("float")
		# BoardWithTitleBar.__init__ X butonuna self.Hide'i GUCLU ref ile baglar ->
		# self->titleBar->btnClose->self dongusu (__del__ olan nesne: py2 GC toplamaz).
		# Zayif ref ile degistir; X ayni sekilde yalniz gizler.
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		texts = []
		for key in RULE_LINE_KEYS:
			value = getattr(localeInfo, key, "")
			if value:
				texts.append(value)

		textWidth = self.WIDTH - self.MARGIN_X * 2

		# Bu fork'ta TextLine "\n" ile satir KIRMAZ ve GetTextSize() tek satir
		# yuksekligi dondurur (EterLib/GrpTextInstance.cpp; ayrica uiminimap.py notu).
		# Bu yuzden her satir icin ayri TextLine; uzun kurallar kelime bazinda sarilir.
		lineY = self.TEXT_TOP
		for text in texts:
			for lineText in self.__WrapText(text, textWidth):
				line = ui.TextLine()
				line.SetParent(self)
				line.AddFlag("not_pick")
				line.SetPosition(self.MARGIN_X, lineY)
				line.SetHorizontalAlignLeft()
				line.SetOutline()
				line.SetText(lineText)
				line.Show()
				self.bodyLines.append(line)
				lineY += self.LINE_STEP

		textHeight = lineY - self.TEXT_TOP
		if textHeight < 40:
			textHeight = 40
		# butonlar her zaman metnin ALTINDA: son satir + bosluk (satir sayisindan hesaplanir)
		btnY = self.TEXT_TOP + textHeight + 20

		# Onayliyorum / Reddediyorum (kayit oncesi onay akisi - TRN-17). Sunucuya komut yollar.
		acceptBtn = ui.Button()
		acceptBtn.SetParent(self)
		acceptBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		acceptBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		acceptBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		acceptBtn.SetText(localeInfo.PVP_TRN_ACCEPT_BTN)
		acceptBtn.SetPosition(self.WIDTH / 2 - 100, btnY)
		acceptBtn.SAFE_SetEvent(self.__OnAccept)
		acceptBtn.Hide()
		self.acceptButton = acceptBtn

		rejectBtn = ui.Button()
		rejectBtn.SetParent(self)
		rejectBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		rejectBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		rejectBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		rejectBtn.SetText(localeInfo.PVP_TRN_REJECT_BTN)
		rejectBtn.SetPosition(self.WIDTH / 2 + 10, btnY)
		rejectBtn.SAFE_SetEvent(self.__OnReject)
		rejectBtn.Hide()
		self.rejectButton = rejectBtn

		# Kapat (yalniz bilgilendirme modunda) - ayni konumda, moda gore gosterilir/gizlenir
		closeBtn = ui.Button()
		closeBtn.SetParent(self)
		closeBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		closeBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		closeBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		closeBtn.SetText(localeInfo.PVP_TRN_CLOSE_BTN)
		closeBtn.SetPosition((self.WIDTH - 90) / 2, btnY)
		closeBtn.SAFE_SetEvent(self.Close)
		closeBtn.Hide()
		self.closeButton = closeBtn

		height = btnY + 25 + 20   # buton (25) + alt kenar bosluk
		self.SetSize(self.WIDTH, height)
		self.SetCenterPosition()
		self.SetTitleName(localeInfo.PVP_TRN_RULES_TITLE)
		self.Hide()

	def __WrapText(self, text, width):
		# Kelime bazli sarma. Iki sinir birden: karakter sayisi (her zaman gecerli, deterministik) ve
		# olculebiliyorsa gercek font genisligi (GetTextSize render oncesi 0 donebilir -> yalniz karakter siniri).
		measure = ui.TextLine()
		lines = []
		current = ""
		for word in text.split(" "):
			if not word:
				continue
			if current:
				candidate = current + " " + word
			else:
				candidate = word
			tooLong = len(candidate) > self.MAX_LINE_CHARS
			if not tooLong:
				measure.SetText(candidate)
				measured = measure.GetTextSize()[0]
				tooLong = measured > width
			if current and tooLong:
				lines.append(current)
				current = word
			else:
				current = candidate
		if current:
			lines.append(current)
		return lines

	# Giris akisi: Onayla/Reddet goster (server PvPTrnRules komutu bunu cagirir)
	def OpenForAccept(self):
		if self.acceptButton: self.acceptButton.Show()
		if self.rejectButton: self.rejectButton.Show()
		if self.closeButton:  self.closeButton.Hide()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	# Bilgilendirme: yalniz Kapat (skorboard "Kurallar" butonu bunu cagirir)
	def Open(self):
		if self.acceptButton: self.acceptButton.Hide()
		if self.rejectButton: self.rejectButton.Hide()
		if self.closeButton:  self.closeButton.Show()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def __OnAccept(self):
		net.SendChatPacket("/pvp_trn_rules onay")
		self.Hide()

	def __OnReject(self):
		net.SendChatPacket("/pvp_trn_rules red")
		self.Hide()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		# ESC yalnizca gizler (kazara eleme olmasin); ayrilmak icin Reddediyorum'a basilir.
		self.Hide()
		return True


# ============================================================================
# C) GM YONETIM PANELI
# ============================================================================
class PvPTournamentAdmin(ui.BoardWithTitleBar):
	WIDTH = 340
	HEIGHT = 270

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def __Initialize(self):
		self.labels = []
		self.slots = []
		self.buttons = []
		self.minEdit = None
		self.maxEdit = None
		self.prepEdit = None
		self.playersEdit = None

	def Destroy(self):
		# ui.WindowDestroy bu fork'ta yok; referanslar elle birakilir.
		# Odak EditLine'da kalirsa wndMgr.Destroy OnKillFocus cagirmadan aktif pencereyi
		# siler -> ime capture acik kalir. Once odagi birak.
		self.__KillEditFocus()
		self.Hide()
		self.__Initialize()

	def __KillEditFocus(self):
		# Gizli panelde odakli EditLine tum tuslari yutar (RunKeyDown: aktif pencerenin
		# kendi IsShow'u yeterli, parent'a bakmaz) -> hotkey/1-4 slot calismaz.
		for edit in (self.minEdit, self.maxEdit, self.prepEdit, self.playersEdit):
			if edit:
				edit.KillFocus()

	def __LoadWindow(self):
		self.AddFlag("movable")
		# "float" yoksa CWindow::SetTop hicbir sey yapmaz (Open SetTop cagirir).
		self.AddFlag("float")
		# X butonu: guclu self.Hide yerine zayif ref Close (dongu/sizinti yok, odak birakilir).
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.SetCenterPosition()
		self.SetTitleName(localeInfo.PVP_TRN_PANEL_TITLE)

		# Etiket + sayi kutulari
		self.minEdit     = self.__MakeField(localeInfo.PVP_TRN_MIN_LEVEL,   40,  "1",  3)
		self.maxEdit     = self.__MakeField(localeInfo.PVP_TRN_MAX_LEVEL,   70,  "99", 3)
		self.prepEdit    = self.__MakeField(localeInfo.PVP_TRN_PREP_MIN,    100, "5",  4)
		self.playersEdit = self.__MakeField(localeInfo.PVP_TRN_MAX_PLAYERS, 130, "64", 4)

		# Butonlar (sag sutun alan kutulariyla ayni x'te hizali)
		rightX = self.WIDTH - 110
		self.__MakeButton(localeInfo.PVP_TRN_BTN_START,     20,     165, self.__OnStart)
		self.__MakeButton(localeInfo.PVP_TRN_BTN_REG_CLOSE, rightX, 165, self.__OnRegClose)
		self.__MakeButton(localeInfo.PVP_TRN_BTN_CANCEL,    20,     195, self.__OnCancel)
		self.__MakeButton(localeInfo.PVP_TRN_BTN_RELOAD,    rightX, 195, self.__OnReload)
		self.__MakeButton(localeInfo.PVP_TRN_CLOSE_BTN,     (self.WIDTH - 90) / 2, 228, self.Close)

		self.Hide()

	def __MakeField(self, labelText, y, default, maxLen):
		label = ui.TextLine()
		label.SetParent(self)
		label.AddFlag("not_pick")
		label.SetPosition(20, y + 2)
		label.SetHorizontalAlignLeft()
		label.SetOutline()
		label.SetText(labelText)
		label.Show()
		self.labels.append(label)

		slot = ui.SlotBar()
		slot.SetParent(self)
		slot.AddFlag("attach")
		slot.SetSize(90, 20)
		slot.SetPosition(self.WIDTH - 110, y)
		slot.Show()
		self.slots.append(slot)   # SlotBar referansi da tutulmali (GC)

		edit = ui.EditLine()
		edit.SetParent(slot)
		edit.SetPosition(4, 3)
		edit.SetSize(84, 16)
		edit.SetMax(maxLen)
		edit.SetNumberMode()
		edit.SetText(default)
		# Gorunur her EditLine ESC'yi yutar (OnPressEscapeKey -> True); aksi halde panelin
		# OnPressEscapeKey'i hic cagrilmaz. ESC -> Close.
		edit.SetEscapeEvent(ui.__mem_func__(self.Close))
		edit.Show()
		return edit

	def __MakeButton(self, text, x, y, callback):
		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		btn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		btn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		btn.SetText(text)
		btn.SetPosition(x, y)
		btn.SAFE_SetEvent(callback)
		btn.Show()
		self.buttons.append(btn)
		return btn

	# --- buton olaylari --------------------------------------------------
	def __OnStart(self):
		minLvl = self.minEdit.GetText()
		maxLvl = self.maxEdit.GetText()
		prepMin = self.prepEdit.GetText()
		maxPlayers = self.playersEdit.GetText()

		for value in (minLvl, maxLvl, prepMin, maxPlayers):
			if not value.isdigit():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PVP_TRN_WARN_DIGITS)
				return

		# Sunucu imzasi: /pvp_tournement start <minLvl> <maxLvl> <prepDakika> <maxKatilimci>
		# (prep DAKIKA olarak gonderilir; sunucu *60 yapar)
		net.SendChatPacket("/pvp_tournement start %s %s %s %s" % (minLvl, maxLvl, prepMin, maxPlayers))
		self.Close()

	def __OnRegClose(self):
		net.SendChatPacket("/pvp_tournement close")

	def __OnCancel(self):
		net.SendChatPacket("/pvp_tournement cancel")

	def __OnReload(self):
		net.SendChatPacket("/pvp_tournement reload")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.__KillEditFocus()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
