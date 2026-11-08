import dbg
import app
import net
import ui
import ime
import snd
import wndMgr
import musicInfo
import serverInfo
import systemSetting
import ServerStateChecker
import localeInfo
import constInfo
import uiCommon
import time
import serverCommandParser
import ime
import uiScriptLocale

LOGIN_DELAY_SEC = 0.0
SKIP_LOGIN_PHASE = False
SKIP_LOGIN_PHASE_SUPPORT_CHANNEL = False
FULL_BACK_IMAGE = False

VIRTUAL_KEYBOARD_NUM_KEYS = 46
VIRTUAL_KEYBOARD_RAND_KEY = True

def Suffle(src):
	if VIRTUAL_KEYBOARD_RAND_KEY:
		items = [item for item in src]

		itemCount = len(items)
		for oldPos in xrange(itemCount):
			newPos = app.GetRandom(0, itemCount-1)
			items[newPos], items[oldPos] = items[oldPos], items[newPos]

		return "".join(items)
	else:
		return src

def IsFullBackImage():
	global FULL_BACK_IMAGE
	return FULL_BACK_IMAGE

def IsLoginDelay():
	global LOGIN_DELAY_SEC
	if LOGIN_DELAY_SEC > 0.0:
		return True
	else:
		return False

def GetLoginDelay():
	global LOGIN_DELAY_SEC
	return LOGIN_DELAY_SEC

app.SetGuildMarkPath("test")

# SAB_F5_FIX: ui.EditLine sadece F1-F4'u gecirir, F5'i yutar.
# Bu filtre sadece login ID/sifre kutularina takilir: kayitli hesap
# tuslarini (F1..F5) LoginWindow.OnKeyDown'a gecirir, diger tuslar ayni kalir.
class SAB_EditLineKeyFilter:
	def __init__(self, editLine):
		self.orgOnKeyDown = ui.__mem_func__(editLine.OnKeyDown)

	def __call__(self, key):
		if app.DIK_F1 <= key < app.DIK_F1 + constInfo.SAB.slotCount:
			return False
		return self.orgOnKeyDown(key)

class ConnectingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("%.0f%s" % (waitTime, localeInfo.SECOND))

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			self.SetCountDownMessage(self.endTime - time.clock())

	def OnPressExitKey(self):
		#self.eventExit()
		return True

class LoginWindow(ui.ScriptWindow):

	IS_TEST = net.IsTest()

	def __init__(self, stream):
		print "NEW LOGIN WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		self.lastLoginTime = 0
		self.inputDialog = None
		self.connectingDialog = None
		self.stream=stream
		self.isNowCountDown=False
		self.isStartError=False

		self.xServerBoard = 0
		self.yServerBoard = 0
		if app.ENABLE_SECURITY_COMPUTER_REDVEGAS:
			self.isSecurityPC = False
		if app.ENABLE_AUTO_SYSTEM:
			self.local_timer = 0

		self.loadingImage = None

		self.virtualKeyboard = None
		self.virtualKeyboardMode = "ALPHABET"
		self.virtualKeyboardIsUpper = False

		# @fixme001 BEGIN (timeOutMsg and timeOutOk undefined)
		self.timeOutMsg = False
		self.timeOutOk = False
		# @fixme001 END

	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE LOGIN WINDOW"

	def Open(self):
		ServerStateChecker.Create(self)

		print "LOGIN WINDOW OPEN ----------------------------------------------------------------------------"

		self.loginFailureMsgDict={
			#"DEFAULT" : localeInfo.LOGIN_FAILURE_UNKNOWN,

			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
			"BADSCLID"	: localeInfo.LOGIN_FAILURE_WRONG_SOCIALID,
			"AGELIMIT"	: localeInfo.LOGIN_FAILURE_SHUTDOWN_TIME,
			"DBLOCK"	: "Sýnýrsýz ban yedin.",
			"CRIMINAL_ERROR"	: "Ceza puanýnýz 100'ü geçtiði için giriþ yapamazsýnýz.",
			"CR_ERR_AVAIL"	: "Ceza puaný nedeniyle süreli banlandýnýz. Açýlma zamanýný siteden bakabilirsiniz.",
			"CR_ERR_HWID"	: "Ceza puaný nedeniyle limitsiz banlandýnýz.",
			"GBLOCK"	: "Þuanlýk sadece oyun yöneticileri giriþ yapabilir.",
			"VBLOCK"	: "Giriþ yapmak için client güncellemeniz gerekmektedir.",
			"NO_SPC"	: "Bu bilgisayar güvenli bilgisayarda ekli deðil giriþ yapamazsýnýz.",
			"NO_SPF"	: "Bu bilgisayar güvenli bilgisayarda deðil. Lütfen kaydedilen bilgisayarýnýzý kullanýn.",
		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: self.__DisconnectAndInputPassword,
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		if not self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "LoginWindow.py"):
			dbg.TraceError("LoginWindow.Open - __LoadScript Error")
			return

		self.__LoadLoginInfo("loginInfo.xml")

		if app.loggined:
			self.loginFailureFuncDict = {
			"WRONGPWD"	: app.Exit,
			"WRONGMAT"	: app.Exit,
			"QUIT"		: app.Exit,
			}

		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		# pevent key "[" "]"
		ime.AddExceptKey(91)
		ime.AddExceptKey(93)

		self.Show()

		global SKIP_LOGIN_PHASE
		if SKIP_LOGIN_PHASE:
			if self.isStartError:
				self.connectBoard.Hide()
				self.loginBoard.Hide()
				if constInfo.ENABLE_SAVE_ACCOUNT:
					self.saveAccountBoard.Hide()
				self.serverBoard.Hide()
				self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.__ExitGame)
				return

			if self.loginInfo:
				self.serverBoard.Hide()
			else:
				self.__RefreshServerList()
				self.__OpenServerBoard()
		else:
			connectingIP = self.stream.GetConnectAddr()
			if connectingIP:
				if app.USE_OPENID and not app.OPENID_TEST :
					self.__RefreshServerList()
					self.__OpenServerBoard()
				else:
					self.__OpenLoginBoard()
					if IsFullBackImage():
						self.GetChild("bg1").Hide()
						self.GetChild("bg2").Show()

			else:
				self.__RefreshServerList()
				self.__OpenServerBoard()

		app.ShowCursor()
		if app.ENABLE_AUTO_SYSTEM:
			if constInfo.AUTO_LOGIN == True:
				self.__OpenServerBoard()
				self.idEditLine.SetText(constInfo.AUTO_LOGIN_ID)
				self.pwdEditLine.SetText(constInfo.AUTO_LOGIN_PW)
				self.__OnClickSelectServerButton()
				self.__OnClickLoginButton()
				constInfo.AUTO_HUNT_STATE = False
				constInfo.CMD_FIRST = False

	def Close(self):

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		ServerStateChecker.Initialize(self)

		print "---------------------------------------------------------------------------- CLOSE LOGIN WINDOW "
		#
		#
		if musicInfo.loginMusic != "" and musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.loginMusic)

		self.idEditLine.SetTabEvent(0)
		self.idEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetTabEvent(0)

		self.connectBoard = None
		self.loginBoard = None
		if constInfo.ENABLE_SAVE_ACCOUNT:
			self.saveAccountBoard = None
		self.idEditLine = None
		self.pwdEditLine = None
		self.inputDialog = None
		self.connectingDialog = None
		self.loadingImage = None

		self.serverBoard				= None
		self.serverList					= None
		self.channelList				= None

		self.VIRTUAL_KEY_ALPHABET_LOWERS = None
		self.VIRTUAL_KEY_ALPHABET_UPPERS = None
		self.VIRTUAL_KEY_SYMBOLS = None
		self.VIRTUAL_KEY_NUMBERS = None

		# VIRTUAL_KEYBOARD_BUG_FIX
		if self.virtualKeyboard:
			for keyIndex in xrange(0, VIRTUAL_KEYBOARD_NUM_KEYS+1):
				key = self.GetChild2("key_%d" % keyIndex)
				if key:
					key.SetEvent(None)

			self.GetChild("key_space").SetEvent(None)
			self.GetChild("key_backspace").SetEvent(None)
			self.GetChild("key_enter").SetEvent(None)
			self.GetChild("key_shift").SetToggleDownEvent(None)
			self.GetChild("key_shift").SetToggleUpEvent(None)
			self.GetChild("key_at").SetToggleDownEvent(None)
			self.GetChild("key_at").SetToggleUpEvent(None)

			self.virtualKeyboard = None

		self.KillFocus()
		self.Hide()

		self.stream.popupWindow.Close()
		self.loginFailureFuncDict=None

		ime.ClearExceptKey()

		app.HideCursor()

	def __SaveChannelInfo(self):
		try:
			file=old_open("channel.inf", "w")
			file.write("%d %d %d" % (self.__GetServerID(), self.__GetChannelID(), self.__GetRegionID()))
		except:
			print "LoginWindow.__SaveChannelInfo - SaveError"

	def __LoadChannelInfo(self):
		try:
			file=old_open("channel.inf")
			lines=file.readlines()

			if len(lines)>0:
				tokens=lines[0].split()

				selServerID=int(tokens[0])
				selChannelID=int(tokens[1])

				if len(tokens) == 3:
					regionID = int(tokens[2])

				return regionID, selServerID, selChannelID

		except:
			print "LoginWindow.__LoadChannelInfo - OpenError"
			return -1, -1, -1

	def __ExitGame(self):
		app.Exit()

	def SetIDEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetFocus()

	def SetPasswordEditLineFocus(self):
		if constInfo.ENABLE_CLEAN_DATA_IF_FAIL_LOGIN:
			if self.idEditLine != None:
				self.idEditLine.SetText("")
				self.idEditLine.SetFocus()

			if self.pwdEditLine != None:
				self.pwdEditLine.SetText("")
		else:
			if self.pwdEditLine != None:
				self.pwdEditLine.SetFocus()

	def OnEndCountDown(self):
		self.isNowCountDown = False
		self.timeOutMsg = False
		self.OnConnectFailure()

	def OnConnectFailure(self):

		if self.isNowCountDown:
			return

		snd.PlaySound("sound/ui/loginfail.wav")

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		if app.loggined:
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.__ExitGame)
		elif self.timeOutMsg:
			self.PopupNotifyMessage(localeInfo.LOGIN_FAILURE_TIMEOUT, self.SetPasswordEditLineFocus)
		else:
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.SetPasswordEditLineFocus)

	def OnHandShake(self):
		if not IsLoginDelay():
			snd.PlaySound("sound/ui/loginok.wav")
			self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		if not IsLoginDelay():
			self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN  + error

		# if self.loginFailureFuncDict is None:
			# self.PopupNotifyMessage(loginFailureMsg, self.__ExitGame)
			# snd.PlaySound("sound/ui/loginfail.wav")
			# return

		loginFailureFunc=self.loginFailureFuncDict.get(error, self.SetPasswordEditLineFocus)

		if app.loggined:
			self.PopupNotifyMessage(loginFailureMsg, self.__ExitGame)
		else:
			self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)

		snd.PlaySound("sound/ui/loginfail.wav")

	def __DisconnectAndInputID(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetIDEditLineFocus()
		net.Disconnect()

	def __DisconnectAndInputPassword(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetPasswordEditLineFocus()
		net.Disconnect()

	if constInfo.ENABLE_SAVE_ACCOUNT:
		if constInfo.ENABLE_TWO_SERVER_SELECT:
			def SAB_LoadAccountData(self):
				constInfo.SAB.accData = {}

				if constInfo.SAB.storeType == constInfo.SAB.ST_CACHE:
					return

				for idx in xrange(constInfo.SAB.slotCount):
					if constInfo.SAB.storeType == constInfo.SAB.ST_REGISTRY:
						id = constInfo.GetWinRegKeyValue(
							constInfo.SAB.regPath,
							constInfo.SAB.regName % (idx, constInfo.SAB.regValueId)
						)
						pwd = constInfo.GetWinRegKeyValue(
							constInfo.SAB.regPath,
							constInfo.SAB.regName % (idx, constInfo.SAB.regValuePwd)
						)

						if id and pwd:
							self.SAB_SetAccountData(idx, (id, pwd))

					elif constInfo.SAB.storeType == constInfo.SAB.ST_FILE:
						(id, pwd) = constInfo.GetJsonSABData(idx)

						if id and pwd:
							self.SAB_SetAccountData(idx, (id, pwd))
			
			def SAB_RefreshByServer(self):
				try:
					serverID = self.__GetServerID()
					serverType = constInfo.SAB_GetServerTypeByServerID(serverID)

					constInfo.SAB_SetServerType(serverType)

					self.SAB_LoadAccountData()

					if hasattr(self, "saveAccountBoard") and self.saveAccountBoard:
						self.SAB_BtnRearrange()

				except:
					import exception
					exception.Abort("LoginWindow.SAB_RefreshByServer")


			def SAB_GetServerText(self):
				if constInfo.SAB.activeServerType == "FETIH":
					return "Fetih"

				return "Kale"
			def SAB_OpenSaveServerPopup(self):
				try:
					self.SAB_CloseSaveServerPopup()

					self.sabSavePopup = ui.BoardWithTitleBar()
					self.sabSavePopup.SetParent(self)
					self.sabSavePopup.SetSize(240, 120)
					self.sabSavePopup.SetCenterPosition()
					self.sabSavePopup.AddFlag("float")
					self.sabSavePopup.SetTitleName("Kaydet?")
					self.sabSavePopup.SetCloseEvent(self.SAB_CloseSaveServerPopup)
					self.sabSavePopup.Show()

					text = ui.TextLine()
					text.SetParent(self.sabSavePopup)
					text.SetHorizontalAlignCenter()
					text.SetPosition(120, 38)
					text.SetText("Hangi sunucuya kaydedilsin?")
					text.Show()
					self.sabSavePopupText = text

					btnKale = ui.Button()
					btnKale.SetParent(self.sabSavePopup)
					btnKale.SetPosition(35, 70)
					btnKale.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
					btnKale.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
					btnKale.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
					btnKale.SetText("Kale")
					btnKale.SAFE_SetEvent(self.SAB_SaveToServer, "KALE")
					btnKale.Show()
					self.sabBtnKale = btnKale

					btnFetih = ui.Button()
					btnFetih.SetParent(self.sabSavePopup)
					btnFetih.SetPosition(140, 70)
					btnFetih.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
					btnFetih.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
					btnFetih.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
					btnFetih.SetText("Fetih")
					btnFetih.SAFE_SetEvent(self.SAB_SaveToServer, "FETIH")
					btnFetih.Show()
					self.sabBtnFetih = btnFetih

				except:
					import exception
					exception.Abort("LoginWindow.SAB_OpenSaveServerPopup")


			def SAB_CloseSaveServerPopup(self):
				try:
					if hasattr(self, "sabSavePopup") and self.sabSavePopup:
						self.sabSavePopup.Hide()

					self.sabSavePopup = None
					self.sabSavePopupText = None
					self.sabBtnKale = None
					self.sabBtnFetih = None
				except:
					pass


			def SAB_SaveToServer(self, serverType):
				try:
					if not hasattr(self, "sabPendingSaveSlot"):
						return

					slot = self.sabPendingSaveSlot
					data = self.sabPendingSaveData

					constInfo.SAB_SetServerType(serverType)

					self.SAB_LoadAccountData()
					self.SAB_SetAccountData(slot, data)
					self.SAB_SaveAccountData()
					self.SAB_BtnRearrange()

					self.SAB_CloseSaveServerPopup()

				except:
					import exception
					exception.Abort("LoginWindow.SAB_SaveToServer")
		else:
			def SAB_LoadAccountData(self):
				if constInfo.SAB.storeType == constInfo.SAB.ST_CACHE:
					return
				for idx in xrange(constInfo.SAB.slotCount):
					if constInfo.SAB.storeType == constInfo.SAB.ST_REGISTRY:
						id = constInfo.GetWinRegKeyValue(constInfo.SAB.regPath, constInfo.SAB.regName % (idx, constInfo.SAB.regValueId))
						pwd = constInfo.GetWinRegKeyValue(constInfo.SAB.regPath, constInfo.SAB.regName % (idx, constInfo.SAB.regValuePwd))
						if id and pwd:
							self.SAB_SetAccountData(idx, (id, pwd))
					elif constInfo.SAB.storeType == constInfo.SAB.ST_FILE:
						(id, pwd) = constInfo.GetJsonSABData(idx)
						if id and pwd:
							self.SAB_SetAccountData(idx, (id, pwd))

		def SAB_SaveAccountData(self):
			if constInfo.SAB.storeType == constInfo.SAB.ST_CACHE:
				return
			for idx in xrange(constInfo.SAB.slotCount):
				if constInfo.SAB.storeType == constInfo.SAB.ST_REGISTRY:
					_tSlot = self.SAB_GetAccountData(idx)
					if _tSlot:
						(id, pwd) = _tSlot
						constInfo.SetWinRegKeyValue(constInfo.SAB.regPath, constInfo.SAB.regName % (idx, constInfo.SAB.regValueId), id)
						constInfo.SetWinRegKeyValue(constInfo.SAB.regPath, constInfo.SAB.regName % (idx, constInfo.SAB.regValuePwd), pwd)
					else:
						constInfo.DelWinRegKeyValue(constInfo.SAB.regPath, constInfo.SAB.regName % (idx, constInfo.SAB.regValueId))
						constInfo.DelWinRegKeyValue(constInfo.SAB.regPath, constInfo.SAB.regName % (idx, constInfo.SAB.regValuePwd))
				elif constInfo.SAB.storeType == constInfo.SAB.ST_FILE:
					_tSlot = self.SAB_GetAccountData(idx)
					if _tSlot:
						constInfo.SetJsonSABData(idx, _tSlot)
					else:
						constInfo.DelJsonSABData(idx)

		def SAB_DelAccountData(self, slot):
			if constInfo.SAB.accData.get(slot):
				del constInfo.SAB.accData[slot]

		def SAB_GetAccountData(self, slot):
			return constInfo.SAB.accData.get(slot)

		def SAB_SetAccountData(self, slot, data):
			constInfo.SAB.accData[slot] = data

		def SAB_BtnRearrange(self):
			def tooltipArrange(_btnObj):
				_tMexTip = "Account ID: %s" % id
				_btnObj.SetToolTipText(_tMexTip)
				if _btnObj.ToolTipText:
					_btnObj.ToolTipText.SetPackedFontColor(0xff66FFFF)
			## def code
			GetObject=self.GetChild
			SetObject=self.InsertChild
			## button names
			btnNameSave = constInfo.SAB.btnName["Save"]
			btnNameAccess = constInfo.SAB.btnName["Access"]
			btnNameRemove = constInfo.SAB.btnName["Remove"]
			## rearrange code
			for idx in xrange(constInfo.SAB.slotCount):
				_tSlot = self.SAB_GetAccountData(idx)
				# button objects
				btnObjSave = GetObject(btnNameSave % idx)
				btnObjAccess = GetObject(btnNameAccess % idx)
				btnObjRemove = GetObject(btnNameRemove % idx)
				if _tSlot:
					(id, pwd) = _tSlot
					btnObjSave.Hide()
					btnObjAccess.Show()
					btnObjRemove.Show()
					if constInfo.ENABLE_TWO_SERVER_SELECT:
						btnObjAccess.SetText("|cffFF0000|h[F{}]|r [{}] {}".format(idx+1, self.SAB_GetServerText(), id))
					else:
						btnObjAccess.SetText("|cffFF0000|h[F{}]|r Baðlan {}".format(idx+1, id))
				else:
					btnObjSave.Show()
					btnObjAccess.Hide()
					btnObjRemove.Hide()
			# done

		def SAB_Click_Save(self, slot):
			if slot >= constInfo.SAB.slotCount:
				return
			## def code
			GetObject=self.GetChild
			SetObject=self.InsertChild
			## button stuff
			_tmpName = constInfo.SAB.btnName["Save"] % slot
			_tmpObj = GetObject(_tmpName)
			## code stuff
			try:
				id = self.idEditLine.GetText()
				pwd = self.pwdEditLine.GetText()

				turkish_chars = "çÇðÐýÝöÖþÞüÜ"
				if any(char in id for char in turkish_chars) or any(char in pwd for char in turkish_chars):
					self.PopupNotifyMessage("ID veya PW (TR) karakter desteklenmez!", self.SetIDEditLineFocus)
					return

				if len(id)==0:
					self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, self.SetIDEditLineFocus)
					return

				if len(pwd)==0:
					self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, self.SetPasswordEditLineFocus)
					return
			except:
				return
			if constInfo.ENABLE_TWO_SERVER_SELECT:
				self.SAB_RefreshByServer()

				self.SAB_SetAccountData(slot, (id, pwd))
				self.SAB_SaveAccountData()

				self.SAB_BtnRearrange()
			else:
				self.SAB_SetAccountData(slot, (id,pwd))
				self.SAB_SaveAccountData()
				## rearrange stuff
				self.SAB_BtnRearrange()

		def SAB_Click_Access(self, slot):
			if slot >= constInfo.SAB.slotCount:
				return
			## def code
			GetObject=self.GetChild
			SetObject=self.InsertChild
			## button stuff
			_tmpName = constInfo.SAB.btnName["Access"] % slot
			_tmpObj = GetObject(_tmpName)
			## code stuff
			_tSlot = self.SAB_GetAccountData(slot)
			if _tSlot:
				(id, pwd) = _tSlot
				self.idEditLine.SetText(id)
				self.pwdEditLine.SetText(pwd)
				self.__OnClickSelectServerButton()
				self.__OnClickLoginButton()

		def SAB_Click_Remove(self, slot):
			if slot >= constInfo.SAB.slotCount:
				return
			## def code
			GetObject=self.GetChild
			SetObject=self.InsertChild
			## button stuff
			_tmpName = constInfo.SAB.btnName["Remove"] % slot
			_tmpObj = GetObject(_tmpName)
			
			if constInfo.ENABLE_TWO_SERVER_SELECT:
				self.SAB_RefreshByServer()
			## code stuff
			self.SAB_DelAccountData(slot)
			self.SAB_SaveAccountData()
			## rearrange stuff
			self.SAB_BtnRearrange()

		def __CreateSaveAccountBoard(self):
			### SAB INIT
			self.SAB_LoadAccountData()
			## def code
			GetObject=self.GetChild
			SetObject=self.InsertChild
			## gui stuff
			SCREEN_WIDTH = wndMgr.GetScreenWidth()
			SCREEN_HEIGHT = wndMgr.GetScreenHeight()
			## button space
			SPACE_FOR_BUTTON = 25+1
			ALL_BUTTON_SPACE = SPACE_FOR_BUTTON * constInfo.SAB.slotCount
			## board stuff
			if app.ENABLE_SECURITY_COMPUTER_REDVEGAS:
				BOARD_SIZE = (210+120, 28 + ALL_BUTTON_SPACE + 40)
			else:
				BOARD_SIZE = (210+120, 28 + ALL_BUTTON_SPACE)
			if app.ENABLE_SECURITY_COMPUTER_REDVEGAS:
				BOARD_POS = ((SCREEN_WIDTH - 208) / 2 + 210, (SCREEN_HEIGHT - 410) - (10*constInfo.SAB.slotCount) - 40)
			else:
				BOARD_POS = ((SCREEN_WIDTH - 208) / 2 + 210, (SCREEN_HEIGHT - 410) - (10*constInfo.SAB.slotCount))
			## button stuff
			btnNameSave = constInfo.SAB.btnName["Save"]
			btnNameAccess = constInfo.SAB.btnName["Access"]
			btnNameRemove = constInfo.SAB.btnName["Remove"]
			btnPath = "d:/ymir work/ui/public/%s_button_%02d.sub" # xsmall small middle large xlarge big
			btnImage = {"default":1,"over":2,"down":3}
			## SAB BOARD
			try:
				## default init
				_tmpName = "SaveAccountBoard"
				SetObject(_tmpName, ui.ThinBoard())
				#
				_tmpObj = GetObject(_tmpName)
				_tmpObj.SetParent(self)
				## custom data
				_tmpObj.SetSize(*BOARD_SIZE)
				## default data
				_tmpObj.SetPosition(*BOARD_POS)
				_tmpObj.Show()
				self.saveAccountBoard = _tmpObj
			except:
				import exception; exception.Abort("__CreateSaveAccountBoard SAB BOARD")
			### SAB TITLE
			try:
				## default init
				_tmpName = "SaveAccountTitle"
				SetObject(_tmpName, ui.TextLine())
				_tmpObj = GetObject(_tmpName)
				_tmpObj.SetParent(self.saveAccountBoard)
				## custom data
				_tmpObj.SetHorizontalAlignCenter()
				_tmpObj.SetPackedFontColor(0xFFffbf00)
				_tmpObj.SetOutline()
				_tmpObj.SetText("Hesap Kaydetme Panosu")
				## default data
				_tmpObj.SetPosition(BOARD_SIZE[0]/2, 5)
				_tmpObj.Show()
			except:
				import exception; exception.Abort("__CreateSaveAccountBoard SAB TITLE")
			### SAB LINE
			try:
				## default init
				_tmpName = "SaveAccountLine"
				SetObject(_tmpName, ui.Line())
				_tmpObj = GetObject(_tmpName)
				_tmpObj.SetParent(self.saveAccountBoard)
				## custom data
				_tmpObj.SetColor(0xFF777777)
				_tmpObj.SetSize(BOARD_SIZE[0]-10, 0)
				## default data
				_tmpObj.SetPosition(5, 20)
				_tmpObj.Show()
			except:
				import exception; exception.Abort("__CreateSaveAccountBoard SAB LINE")
			## SaveAccountButtons
			for idx in xrange(constInfo.SAB.slotCount):
				### SAB SAVE
				try:
					## default init
					_tmpName = btnNameSave % (idx)
					SetObject(_tmpName, ui.Button())
					_tmpObj = GetObject(_tmpName)
					_tmpObj.SetParent(self.saveAccountBoard)
					## custom data
					_tmpBtnPath = "d:/ymir work/ui/public/xlarge_button_%02d.sub" # xsmall small middle large xlarge big
					_tmpObj.SetUpVisual(_tmpBtnPath % (btnImage["default"]))
					_tmpObj.SetOverVisual(_tmpBtnPath % (btnImage["over"]))
					_tmpObj.SetDownVisual(_tmpBtnPath % (btnImage["down"]))
					_tmpObj.SetText("Hesabý Kaydet")
					_tmpObj.SAFE_SetEvent(self.SAB_Click_Save, idx)
					## default data
					_tmpObj.SetPosition(15 + 60, 25 + (idx * SPACE_FOR_BUTTON))
					_tmpObj.Hide()
				except:
					import exception; exception.Abort("__CreateSaveAccountBoard SAB SAVE")
				### SAB ACCESS
				try:
					## default init
					_tmpName = btnNameAccess % (idx)
					SetObject(_tmpName, ui.Button())
					_tmpObj = GetObject(_tmpName)
					_tmpObj.SetParent(self.saveAccountBoard)
					## custom data
					_tmpBtnPath = "d:/ymir work/ui/public/xlarge_button_%02d.sub" # xsmall small middle large xlarge big
					_tmpObj.SetUpVisual(_tmpBtnPath % (btnImage["default"]))
					_tmpObj.SetOverVisual(_tmpBtnPath % (btnImage["over"]))
					_tmpObj.SetDownVisual(_tmpBtnPath % (btnImage["down"]))
					_tmpObj.SetText("Baðlan #{}".format(idx+1))
					_tmpObj.SAFE_SetEvent(self.SAB_Click_Access, idx)
					## default data
					_tmpObj.SetPosition(35, 25 + (idx * SPACE_FOR_BUTTON))
					_tmpObj.Show()
				except:
					import exception; exception.Abort("__CreateSaveAccountBoard SAB ACCESS")
				### SAB REMOVE
				try:
					## default init
					_tmpName = btnNameRemove % (idx)
					SetObject(_tmpName, ui.Button())
					_tmpObj = GetObject(_tmpName)
					_tmpObj.SetParent(self.saveAccountBoard)
					## custom data
					_tmpBtnPath = "d:/ymir work/ui/public/middle_button_%02d.sub" # xsmall small middle large xlarge big
					_tmpObj.SetUpVisual(_tmpBtnPath % (btnImage["default"]))
					_tmpObj.SetOverVisual(_tmpBtnPath % (btnImage["over"]))
					_tmpObj.SetDownVisual(_tmpBtnPath % (btnImage["down"]))
					_tmpObj.SetText("Sil")
					_tmpObj.SAFE_SetEvent(self.SAB_Click_Remove, idx)
					## default data
					_tmpObj.SetPosition(35 + 190, 25 + (idx * SPACE_FOR_BUTTON))
					_tmpObj.Show()
				except:
					import exception; exception.Abort("__CreateSaveAccountBoard SAB REMOVE")
			self.SAB_BtnRearrange()

	def __LoadScript(self, fileName):
		import dbg
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")
		try:
			GetObject=self.GetChild
			self.serverBoard			= GetObject("ServerBoard")
			self.serverList				= GetObject("ServerList")
			self.channelList			= GetObject("ChannelList")
			self.serverSelectButton		= GetObject("ServerSelectButton")
			self.serverExitButton		= GetObject("ServerExitButton")
			self.connectBoard			= GetObject("ConnectBoard")
			self.loginBoard				= GetObject("LoginBoard")
			self.idEditLine				= GetObject("ID_EditLine")
			self.pwdEditLine			= GetObject("Password_EditLine")
			self.serverInfo				= GetObject("ConnectName")
			self.selectConnectButton	= GetObject("SelectConnectButton")
			self.loginButton			= GetObject("LoginButton")
			self.loginExitButton		= GetObject("LoginExitButton")

			if constInfo.ENABLE_SAVE_ACCOUNT:
				self.__CreateSaveAccountBoard()

			if app.ENABLE_SECURITY_COMPUTER_REDVEGAS:
				self.checkBox = ui.CheckBox()
				if self.saveAccountBoard:
					self.checkBox.SetParent(self.saveAccountBoard)
				else:
					self.checkBox.SetParent(self.loginBoard)
				self.checkBox.SetPosition(60, 15)
				self.checkBox.SetWindowVerticalAlignBottom()
				self.checkBox.SetEvent(ui.__mem_func__(self.SetSecurityPC), "ON_CHECK", True)
				self.checkBox.SetEvent(ui.__mem_func__(self.SetSecurityPC), "ON_UNCKECK", False)
				self.checkBox.SetCheckStatus(constInfo.SECURE_PC)
				self.checkBox.SetTextInfo("Bu bilgisayarý güvenli bilgisayara ekle")
				self.checkBox.Show()

				self.buttonSafetyPanel = ui.Button()
				if self.saveAccountBoard:
					self.buttonSafetyPanel.SetParent(self.saveAccountBoard)
				else:
					self.buttonSafetyPanel.SetParent(self.loginBoard)
				self.buttonSafetyPanel.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
				self.buttonSafetyPanel.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
				self.buttonSafetyPanel.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
				self.buttonSafetyPanel.SetText("Güvenli Panel")
				self.buttonSafetyPanel.SetPosition(110, 160)
				self.buttonSafetyPanel.SetEvent(lambda : self.OpenSecurityPanel())
				self.buttonSafetyPanel.Show()

			self.virtualKeyboard		= self.GetChild2("VirtualKeyboard")

			if self.virtualKeyboard:
				self.VIRTUAL_KEY_ALPHABET_UPPERS = Suffle(localeInfo.VIRTUAL_KEY_ALPHABET_UPPERS)
				self.VIRTUAL_KEY_ALPHABET_LOWERS = "".join([localeInfo.VIRTUAL_KEY_ALPHABET_LOWERS[localeInfo.VIRTUAL_KEY_ALPHABET_UPPERS.index(e)] for e in self.VIRTUAL_KEY_ALPHABET_UPPERS])
				if localeInfo.IsBRAZIL():
					self.VIRTUAL_KEY_SYMBOLS_BR = Suffle(localeInfo.VIRTUAL_KEY_SYMBOLS_BR)
				else:
					self.VIRTUAL_KEY_SYMBOLS = Suffle(localeInfo.VIRTUAL_KEY_SYMBOLS)
				self.VIRTUAL_KEY_NUMBERS = Suffle(localeInfo.VIRTUAL_KEY_NUMBERS)
				self.__VirtualKeyboard_SetAlphabetMode()

				self.GetChild("key_space").SetEvent(lambda : self.__VirtualKeyboard_PressKey(' '))
				self.GetChild("key_backspace").SetEvent(lambda : self.__VirtualKeyboard_PressBackspace())
				self.GetChild("key_enter").SetEvent(lambda : self.__VirtualKeyboard_PressReturn())
				self.GetChild("key_shift").SetToggleDownEvent(lambda : self.__VirtualKeyboard_SetUpperMode())
				self.GetChild("key_shift").SetToggleUpEvent(lambda : self.__VirtualKeyboard_SetLowerMode())
				self.GetChild("key_at").SetToggleDownEvent(lambda : self.__VirtualKeyboard_SetSymbolMode())
				self.GetChild("key_at").SetToggleUpEvent(lambda : self.__VirtualKeyboard_SetAlphabetMode())

		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

		if self.IS_TEST:
			self.selectConnectButton.Hide()
		else:
			self.selectConnectButton.SetEvent(ui.__mem_func__(self.__OnClickSelectConnectButton))

		self.serverBoard.OnKeyUp = ui.__mem_func__(self.__ServerBoard_OnKeyUp)
		self.xServerBoard, self.yServerBoard = self.serverBoard.GetLocalPosition()

		self.serverSelectButton.SetEvent(ui.__mem_func__(self.__OnClickSelectServerButton))
		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitButton))

		self.loginButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.loginExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitButton))

		self.serverList.SetEvent(ui.__mem_func__(self.__OnSelectServer))

		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))

		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))

		# SAB_F5_FIX: kayitli hesap kisayollari (F1..F5) kutu odaktayken de calissin
		if constInfo.ENABLE_SAVE_ACCOUNT:
			self.idEditLine.OnKeyDown = SAB_EditLineKeyFilter(self.idEditLine)
			self.pwdEditLine.OnKeyDown = SAB_EditLineKeyFilter(self.pwdEditLine)

		if IsFullBackImage():
			self.GetChild("bg1").Show()
			self.GetChild("bg2").Hide()
		return 1

	if app.ENABLE_SECURITY_COMPUTER_REDVEGAS:
		def PopupRiot(self, msg):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(msg, self.EmptyFunc, localeInfo.UI_OK)
		def OpenSecurityPanel(self):
			import webbrowser
			webbrowser.open('https://avrasyamt2.com/')
		def SetSecurityPC(self, checkType, autoFlag):
			regionID = self.__GetRegionID()
			serverID = self.__GetServerID()
			channelID = self.__GetChannelID()
			ip = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["ip"]
			self.isSecurityPC = autoFlag
			if autoFlag:
				id = self.idEditLine.GetText()
				pwd = self.pwdEditLine.GetText()
				if len(id) <= 0:
					self.PopupRiot("ID BOÞ OLAMAZ!")
					return
				if len(pwd) <= 0:
					self.PopupRiot("ÞÝFRE BOÞ OLAMAZ!")
					return
				result = net.SendAddSecurityPCPacket(id,pwd,1,"",ip)
				result2 = result.split("|")
				if str(result2[0]) == "true":
					self.SMSBoard = uiCommon.InputDialogWithDescription2()
					self.SMSBoard.AddFlag('float')
					self.SMSBoard.AddFlag('movable')
					self.SMSBoard.SetMaxLength(6)
					self.SMSBoard.SetAcceptEvent(ui.__mem_func__(self.__OnAcceptSmsCode))
					self.SMSBoard.SetCancelEvent(ui.__mem_func__(self.__OnCancelSmsCode))
					self.SMSBoard.SetTitle("SMS Kodunu Giriniz")
					self.SMSBoard.SetPosition((wndMgr.GetScreenWidth() - 130) / 2, wndMgr.GetScreenHeight()/2-50)
					self.SMSBoard.SetDescription1("Bu bilgisayarý güvenli yapmak için")
					self.SMSBoard.SetDescription2("%s gelen Kodu giriniz."%str(result2[1].replace("_", " ")))
					self.SMSBoard.login = str(self.idEditLine.GetText())
					self.SMSBoard.pwd = str(self.pwdEditLine.GetText())
					self.SMSBoard.Open()
					self.SMSBoard.SetTop()
					snd.PlaySound("sound/ui/loginfail.wav")
				else:
					self.PopupRiot(str(result2[1].replace("_", " ")))
		def __OnAcceptSmsCode(self):
			regionID = self.__GetRegionID()
			serverID = self.__GetServerID()
			channelID = self.__GetChannelID()
			ip = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["ip"]
			text = self.SMSBoard.GetText()
			if self.SMSBoard:
				self.SMSBoard.Hide()
			result = net.SendAddSecurityPCPacket(self.SMSBoard.login,self.SMSBoard.pwd,2,text,ip)
			result2 = result.split("|")
			if str(result2[0]) == "true":
				self.PopupRiot(str(result2[1].replace("_", " ")))
				self.stream.SetLoginInfo(self.SMSBoard.login, self.SMSBoard.pwd)
				constInfo.channelidx = channelID
				self.stream.Connect()
			else:
				self.PopupRiot(str(result2[1].replace("_", " ")))
				if not self.SMSBoard.IsShow():
					self.SMSBoard.Show()
		def __OnCancelSmsCode(self):
			if self.SMSBoard:
				self.SMSBoard.Hide()

	def __VirtualKeyboard_SetKeys(self, keyCodes):
		uiDefFontBackup = localeInfo.UI_DEF_FONT
		localeInfo.UI_DEF_FONT = localeInfo.UI_DEF_FONT_LARGE

		keyIndex = 1
		for keyCode in keyCodes:
			key = self.GetChild2("key_%d" % keyIndex)
			if key:
				key.SetEvent(lambda x=keyCode: self.__VirtualKeyboard_PressKey(x))
				key.SetText(keyCode)
				key.ButtonText.SetFontColor(0, 0, 0)
				keyIndex += 1

		for keyIndex in xrange(keyIndex, VIRTUAL_KEYBOARD_NUM_KEYS+1):
			key = self.GetChild2("key_%d" % keyIndex)
			if key:
				key.SetEvent(lambda x=' ': self.__VirtualKeyboard_PressKey(x))
				key.SetText(' ')

		localeInfo.UI_DEF_FONT = uiDefFontBackup

	def __VirtualKeyboard_PressKey(self, code):
		ime.PasteString(code)

		#if self.virtualKeyboardMode == "ALPHABET" and self.virtualKeyboardIsUpper:
		#	self.__VirtualKeyboard_SetLowerMode()

	def __VirtualKeyboard_PressBackspace(self):
		ime.PasteBackspace()

	def __VirtualKeyboard_PressReturn(self):
		ime.PasteReturn()

	def __VirtualKeyboard_SetUpperMode(self):
		self.virtualKeyboardIsUpper = True

		if self.virtualKeyboardMode == "ALPHABET":
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_ALPHABET_UPPERS)
		elif self.virtualKeyboardMode == "NUMBER":
			if localeInfo.IsBRAZIL():
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS_BR)
			else:
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS)
		else:
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_NUMBERS)

	def __VirtualKeyboard_SetLowerMode(self):
		self.virtualKeyboardIsUpper = False

		if self.virtualKeyboardMode == "ALPHABET":
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_ALPHABET_LOWERS)
		elif self.virtualKeyboardMode == "NUMBER":
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_NUMBERS)
		else:
			if localeInfo.IsBRAZIL():
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS_BR)
			else:
				self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS)

	def __VirtualKeyboard_SetAlphabetMode(self):
		self.virtualKeyboardIsUpper = False
		self.virtualKeyboardMode = "ALPHABET"
		self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_ALPHABET_LOWERS)

	def __VirtualKeyboard_SetNumberMode(self):
		self.virtualKeyboardIsUpper = False
		self.virtualKeyboardMode = "NUMBER"
		self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_NUMBERS)

	def __VirtualKeyboard_SetSymbolMode(self):
		self.virtualKeyboardIsUpper = False
		self.virtualKeyboardMode = "SYMBOL"
		if localeInfo.IsBRAZIL():
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS_BR)
		else:
			self.__VirtualKeyboard_SetKeys(self.VIRTUAL_KEY_SYMBOLS)

	def Connect(self, id, pwd):

		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()

		if IsLoginDelay():
			loginDelay = GetLoginDelay()
			self.connectingDialog = ConnectingDialog()
			self.connectingDialog.Open(loginDelay)
			self.connectingDialog.SAFE_SetTimeOverEvent(self.OnEndCountDown)
			self.connectingDialog.SAFE_SetExitEvent(self.OnPressExitKey)
			self.isNowCountDown = True

		else:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, self.SetPasswordEditLineFocus, localeInfo.UI_CANCEL)

		constInfo.AUTO_LOGIN_ID = id
		constInfo.AUTO_LOGIN_PW = pwd

		self.stream.SetLoginInfo(id, pwd)
		constInfo.channelidx = self.__GetChannelID()
		self.stream.Connect()

	def __OnClickExitButton(self):
		self.stream.SetPhaseWindow(0)

	def __SetServerInfo(self, name):
		net.SetServerInfo(name.strip())
		self.serverInfo.SetText(name)

	def __LoadLoginInfo(self, loginInfoFileName):
		def getValue(element, name, default):
			if [] != element.getElementsByTagName(name):
				return element.getElementsByTagName(name).item(0).firstChild.nodeValue
			else:
				return default

		self.id = None
		self.pwd = None
		self.loginnedServer = None
		self.loginnedChannel = None
		app.loggined = False

		self.loginInfo = True

		from xml.dom.minidom import parse
		try:
			f = old_open(loginInfoFileName, "r")
			dom = parse(f)
		except:
			return
		serverLst = dom.getElementsByTagName("server")
		if [] != dom.getElementsByTagName("logininfo"):
			logininfo = dom.getElementsByTagName("logininfo")[0]
		else:
			return

		try:
			server_name = logininfo.getAttribute("name")
			channel_idx = int(logininfo.getAttribute("channel_idx"))
		except:
			return

		try:
			matched = False

			for k, v in serverInfo.REGION_DICT[0].iteritems():
				if v["name"] == server_name:
					account_addr = serverInfo.REGION_AUTH_SERVER_DICT[0][k]["ip"]
					account_port = serverInfo.REGION_AUTH_SERVER_DICT[0][k]["port"]

					channel_info = v["channel"][channel_idx]
					channel_name = channel_info["name"]
					addr = channel_info["ip"]
					port = channel_info["tcp_port"]

					net.SetMarkServer(addr, port)
					self.stream.SetConnectInfo(addr, port, account_addr, account_port)

					matched = True
					break

			if False == matched:
				return
		except:
			return

		self.__SetServerInfo("%s, %s " % (server_name, channel_name))
		id = getValue(logininfo, "id", "")
		pwd = getValue(logininfo, "pwd", "")
		self.idEditLine.SetText(id)
		self.pwdEditLine.SetText(pwd)
		slot = getValue(logininfo, "slot", "0")
		locale = getValue(logininfo, "locale", "")
		locale_dir = getValue(logininfo, "locale_dir", "")
		is_auto_login = int(getValue(logininfo, "auto_login", "0"))

		self.stream.SetCharacterSlot(int(slot))
		self.stream.isAutoLogin=is_auto_login
		self.stream.isAutoSelect=is_auto_login

		if locale and locale_dir:
			app.ForceSetLocale(locale, locale_dir)

		if 0 != is_auto_login:
			self.Connect(id, pwd)

		return


	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	if app.ENABLE_AUTO_SYSTEM:
		def AutoHuntTimer(self,timer):
			self.local_timer = time.clock() + timer

	def PopupNotifyMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc
		if app.ENABLE_AUTO_SYSTEM:
			if msg == localeInfo.LOGIN_CONNECT_FAILURE:
				if constInfo.AUTO_LOGIN == True and constInfo.TRY_CONNECT_COUNT <= 15:
					constInfo.TRY_CONNECT_COUNT = constInfo.TRY_CONNECT_COUNT + 1
					self.AutoHuntTimer(int(constInfo.AUTO_HUNT_RELOAD_LOGIN_TIMER))
			elif msg == localeInfo.LOGIN_PROCESSING:
				constInfo.TRY_CONNECT_COUNT = 0
				self.local_timer = 0
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def __OnCloseInputDialog(self):
		if self.inputDialog:
			self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnPressExitKey(self):
		self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return True

	def OnExit(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE, app.Exit, localeInfo.UI_OK)

	def OnUpdate(self):
		ServerStateChecker.Update()

	def EmptyFunc(self):
		pass

	#####################################################################################

	def __ServerBoard_OnKeyUp(self, key):
		if self.serverBoard.IsShow():
			if app.DIK_RETURN==key:
				self.__OnClickSelectServerButton()
		return True

	def __GetRegionID(self):
		return 0

	def __GetServerID(self):
		return self.serverList.GetSelectedItem()

	def __GetChannelID(self):
		# constInfo.channelidx = self.channelList.GetSelectedItem()
		return self.channelList.GetSelectedItem()

	# SEVER_LIST_BUG_FIX
	def __ServerIDToServerIndex(self, regionID, targetServerID):
		try:
			regionDict = serverInfo.REGION_DICT[regionID]
		except KeyError:
			return -1

		retServerIndex = 0
		for eachServerID, regionDataDict in regionDict.items():
			if eachServerID == targetServerID:
				return retServerIndex

			retServerIndex += 1

		return -1

	def __ChannelIDToChannelIndex(self, channelID):
		# constInfo.channelidx = channelID - 1
		return channelID - 1
	# END_OF_SEVER_LIST_BUG_FIX

	def __OpenServerBoard(self):

		loadRegionID, loadServerID, loadChannelID = self.__LoadChannelInfo()

		serverIndex = self.__ServerIDToServerIndex(loadRegionID, loadServerID)
		channelIndex = self.__ChannelIDToChannelIndex(loadChannelID)

		self.serverList.SelectItem(serverIndex)

		if constInfo.ENABLE_TWO_SERVER_SELECT:
			self.SAB_RefreshByServer()

		rand = 0
		if constInfo.ENABLE_RANDOM_CHANNEL_SEL:
			rand = app.GetRandom(0, self.channelList.GetItemCount())
			self.channelList.SelectItem(rand)
			# constInfo.channelidx = rand
		else:
			if channelIndex >= 0:
				self.channelList.SelectItem(channelIndex)
				# constInfo.channelidx = channelIndex


		self.serverBoard.SetPosition(self.xServerBoard, self.yServerBoard)
		self.serverBoard.Show()
		self.connectBoard.Hide()
		self.loginBoard.Hide()
		if constInfo.ENABLE_SAVE_ACCOUNT:
			self.saveAccountBoard.Hide()

		if self.virtualKeyboard:
			self.virtualKeyboard.Hide()

		if app.loggined and not SKIP_LOGIN_PHASE_SUPPORT_CHANNEL:
			self.serverList.SelectItem(self.loginnedServer-1)
			if constInfo.ENABLE_TWO_SERVER_SELECT:
				self.SAB_RefreshByServer()
			self.channelList.SelectItem(self.loginnedChannel-1)
			# constInfo.channelidx = self.loginnedChannel-1
			self.__OnClickSelectServerButton()

	def __OpenLoginBoard(self):

		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitServerButton))
		self.serverExitButton.SetText(localeInfo.UI_CLOSE)

		self.serverBoard.SetPosition(self.xServerBoard, wndMgr.GetScreenHeight())
		self.serverBoard.Hide()

		if self.virtualKeyboard:
			self.virtualKeyboard.Show()

		if app.loggined:
			self.Connect(self.id, self.pwd)
			self.connectBoard.Hide()
			self.loginBoard.Hide()
			if constInfo.ENABLE_SAVE_ACCOUNT:
				self.saveAccountBoard.Hide()
		elif not self.stream.isAutoLogin:
			self.connectBoard.Show()
			self.loginBoard.Show()
			if constInfo.ENABLE_SAVE_ACCOUNT:
				self.saveAccountBoard.Show()

		## if users have the login infomation, then don't initialize.2005.9 haho
		if self.idEditLine == None:
			self.idEditLine.SetText("")
		if self.pwdEditLine == None:
			self.pwdEditLine.SetText("")

		self.idEditLine.SetFocus()

		global SKIP_LOGIN_PHASE
		if SKIP_LOGIN_PHASE:
			if not self.loginInfo:
				self.connectBoard.Hide()

	def __OnSelectRegionGroup(self):
		self.__RefreshServerList()

	def __OnSelectSettlementArea(self):
		# SEVER_LIST_BUG_FIX
		regionID = self.__GetRegionID()
		serverID = self.serverListOnRegionBoard.GetSelectedItem()

		serverIndex = self.__ServerIDToServerIndex(regionID, serverID)
		self.serverList.SelectItem(serverIndex)
		# END_OF_SEVER_LIST_BUG_FIX

		self.__OnSelectServer()

	def __RefreshServerList(self):
		regionID = self.__GetRegionID()

		if not serverInfo.REGION_DICT.has_key(regionID):
			return

		self.serverList.ClearItem()

		regionDict = serverInfo.REGION_DICT[regionID]

		# SEVER_LIST_BUG_FIX
		visible_index = 1
		for id, regionDataDict in regionDict.items():
			name = regionDataDict.get("name", "noname")
			try:
				server_id = serverInfo.SERVER_ID_DICT[id]
			except:
				server_id = visible_index

			self.serverList.InsertItem(id, "  %02d. %s" % (int(server_id), name))

			visible_index += 1

		# END_OF_SEVER_LIST_BUG_FIX

	def __OnSelectServer(self):
		self.__OnCloseInputDialog()
		self.__RequestServerStateList()
		self.__RefreshServerStateList()
		if constInfo.ENABLE_TWO_SERVER_SELECT:
			self.SAB_RefreshByServer()

	def __RequestServerStateList(self):
		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except:
			print " __RequestServerStateList - serverInfo.REGION_DICT(%d, %d)" % (regionID, serverID)
			return

		ServerStateChecker.Initialize()
		for id, channelDataDict in channelDict.items():
			key=channelDataDict["key"]
			ip=channelDataDict["ip"]
			udp_port=channelDataDict["udp_port"]
			ServerStateChecker.AddChannel(key, ip, udp_port)

		ServerStateChecker.Request()

	def __RefreshServerStateList(self):

		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()
		bakChannelID = self.channelList.GetSelectedItem()

		self.channelList.ClearItem()

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except:
			print " __RequestServerStateList - serverInfo.REGION_DICT(%d, %d)" % (regionID, serverID)
			return

		for channelID, channelDataDict in channelDict.items():
			channelName = channelDataDict["name"]
			channelState = channelDataDict["state"]
			self.channelList.InsertItem(channelID, " %s %s" % (channelName, channelState))

		self.channelList.SelectItem(bakChannelID-1)
		# constInfo.channelidx = bakChannelID-1

	def __GetChannelName(self, regionID, selServerID, selChannelID):
		try:
			return serverInfo.REGION_DICT[regionID][selServerID]["channel"][selChannelID]["name"]
		except KeyError:
			if 9==selChannelID:
				return localeInfo.CHANNEL_PVP
			else:
				return localeInfo.CHANNEL_NORMAL % (selChannelID)

	def NotifyChannelState(self, addrKey, state):
		try:
			stateName = serverInfo.STATE_DICT[state]
		except:
			stateName = serverInfo.STATE_NONE

		try:
			found = False

			for regionID, regionData in serverInfo.REGION_DICT.items():
				for serverID, serverData in regionData.items():
					channelDict = serverData.get("channel", {})

					for channelID, channelData in channelDict.items():
						if channelData.get("key") == addrKey:
							channelData["state"] = stateName
							found = True
							break

					if found:
						break

				if found:
					break

			if not found:
				raise KeyError(addrKey)

			self.__RefreshServerStateList()

		except Exception as e:
			import dbg
			dbg.TraceError("NotifyChannelState Error addrKey=%s state=%s err=%s" % (addrKey, state, e))

			import exception
			exception.Abort(localeInfo.CHANNEL_NOT_FIND_INFO)

	# def NotifyChannelState(self, addrKey, state):
		# try:
			# stateName=serverInfo.STATE_DICT[state]
		# except:
			# stateName=serverInfo.STATE_NONE

		# regionID=int(addrKey/1000)
		# serverID=int(addrKey/10) % 100
		# channelID=addrKey%10

		# try:
			# serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["state"] = stateName
			# self.__RefreshServerStateList()

		# except:
			# import exception
			# exception.Abort(localeInfo.CHANNEL_NOT_FIND_INFO)

	def __OnClickExitServerButton(self):
		print "exit server"
		self.__OpenLoginBoard()

		if IsFullBackImage():
			self.GetChild("bg1").Hide()
			self.GetChild("bg2").Show()


	def __OnClickSelectRegionButton(self):
		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()

		if (not serverInfo.REGION_DICT.has_key(regionID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_REGION)
			return

		if (not serverInfo.REGION_DICT[regionID].has_key(serverID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_SERVER)
			return

		self.__SaveChannelInfo()

		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitServerButton))
		self.serverExitButton.SetText(localeInfo.UI_CLOSE)

		self.__RefreshServerList()
		self.__OpenServerBoard()

	def __OnClickSelectServerButton(self):
		if IsFullBackImage():
			self.GetChild("bg1").Hide()
			self.GetChild("bg2").Show()

		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()
		channelID = self.__GetChannelID()

		if (not serverInfo.REGION_DICT.has_key(regionID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_REGION)
			return

		if (not serverInfo.REGION_DICT[regionID].has_key(serverID)):
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_SERVER)
			return

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except KeyError:
			return

		try:
			state = channelDict[channelID]["state"]
		except KeyError:
			self.PopupNotifyMessage(localeInfo.CHANNEL_SELECT_CHANNEL)
			return

		if state == serverInfo.STATE_DICT[3]:
			self.PopupNotifyMessage(localeInfo.CHANNEL_NOTIFY_FULL)
			return

		self.__SaveChannelInfo()

		if constInfo.ENABLE_TWO_SERVER_SELECT:
			self.SAB_RefreshByServer()

		try:
			serverName = serverInfo.REGION_DICT[regionID][serverID]["name"]
			channelName = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["name"]
			addrKey = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["key"]

		except:
			print " ERROR __OnClickSelectServerButton(%d, %d, %d)" % (regionID, serverID, channelID)
			serverName = localeInfo.CHANNEL_EMPTY_SERVER
			channelName = localeInfo.CHANNEL_NORMAL % channelID

		self.__SetServerInfo("%s, %s " % (serverName, channelName))
		
		# constInfo.channelidx=channelID

		try:
			ip = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["ip"]
			tcp_port = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["tcp_port"]
		except:
			import exception
			exception.Abort("LoginWindow.__OnClickSelectServerButton")

		try:
			account_ip = serverInfo.REGION_AUTH_SERVER_DICT[regionID][serverID]["ip"]
			account_port = serverInfo.REGION_AUTH_SERVER_DICT[regionID][serverID]["port"]
		except:
			account_ip = 0
			account_port = 0

		try:
			markKey = regionID*1000 + serverID*10
			markAddrValue=serverInfo.MARKADDR_DICT[markKey]
			net.SetMarkServer(markAddrValue["ip"], markAddrValue["tcp_port"])
			app.SetGuildMarkPath(markAddrValue["mark"])
			# GUILD_SYMBOL
			app.SetGuildSymbolPath(markAddrValue["symbol_path"])
			# END_OF_GUILD_SYMBOL

		except:
			import exception
			exception.Abort("LoginWindow.__OnClickSelectServerButton")


		self.stream.SetConnectInfo(ip, tcp_port, account_ip, account_port)
		self.__OpenLoginBoard()


	def __OnClickSelectConnectButton(self):
		if IsFullBackImage():
			self.GetChild("bg1").Show()
			self.GetChild("bg2").Hide()
		self.__RefreshServerList()
		self.__OpenServerBoard()

	def __OnClickLoginButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()

		if len(id)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, self.SetIDEditLineFocus)
			return

		if len(pwd)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, self.SetPasswordEditLineFocus)
			return

		self.Connect(id, pwd)

	def OnKeyDown(self, key):
		if constInfo.ENABLE_SAVE_ACCOUNT:
			for idx in xrange(constInfo.SAB.slotCount):
				if app.DIK_F1+idx == key and self.SAB_GetAccountData(idx):
					self.SAB_Click_Access(idx)
		return True
