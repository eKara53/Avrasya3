# DUMPED FROM LIVE COMPILE: game.py (len=109510)
import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import snd
import chat
import textTail
import snd
import net
import effect
import wndMgr
import fly
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uiMiniMap			# OTOMATIK NAVIGASYON olay pompasi icin

# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander

from _weakref import proxy

if constInfo.SVSIDE_ONLINE:
	svsidedia = None
	svsidedi_cp =  ""
	from svsideoi import SvsideDialog
	import binascii

if app.__ENABLE_NEW_OFFLINESHOP__:
	import uiofflineshop_ae
	import offlineshop
if app.ENABLE_OFFLINESHOP_SYSTEM:
	import uiOfflineShopBuilder
	import shop
if app.ENABLE_VEGAS_NEW_HORSE_MANAGER:
	import uiNewHorse
if app.ENABLE_HORSE_UPGRADE_SYSTEM:
	import uiHorseMenu
if app.ENABLE_SPECIAL_MISSION_SYSTEM:
	import nonplayer
if app.ENABLE_AUTO_SYSTEM:
	import uiAuto
if app.ENABLE_ALL_PLAYERS_PM:
	import uiWhisperAdmin
if constInfo.TIKTOK_PANEL == True:
	import uitiktokers
import time
import uipvpduel
import uiLiveSupport
# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = True
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)
		
		if constInfo.SVSIDE_ONLINE:
			global svsidedia
			if svsidedia == None:
				svsidedia = SvsideDialog()
			svsidedia.Board.Hide()

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.uiNewShopCreate = None
		self.uiNewShop = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None

		self.pvpDuelBoard = None
		self.pvpRules = None
		self.pvpAdmin = None
		self.pvpTrnClosed = False

		if app.ENABLE_AUTO_SYSTEM:
			self.timer = 0
			self.used_item = 0

		if app.ENABLE_HORSE_UPGRADE_SYSTEM:
			self.horse_board = None
		if app.ENABLE_BIYOLOG_MISSION_SYSTEM:
			self.biyolog_board = None

		if app.ENABLE_SPECIAL_MISSION_SYSTEM:
			self.mission_gui = None
			self.guage_text = None
			self.guage_progress = None
			self.guage_reward = None
			self.guage_bitir = None

		self.stream=stream
		self.interface = interfaceModule.Interface()
		
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			constInfo.SetGameInstance(self)
			constInfo.SetInterfaceInstance(self.interface)
		
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		if app.ENABLE_ALL_PLAYERS_PM:
			self.whisperAdmin = uiWhisperAdmin.AdminWhisperManager()
			self.whisperAdmin.Close()

		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()

		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if app.__ENABLE_NEW_SHOP_IN_CITIES__:
				offlineshop.HideShopNames()

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			if app.ENABLE_NEW_FONT_CHANGER:
				if constInfo.OPTION_FONT == 0:
					self.testPKMode.SetFontName(constInfo.UI_DEF_FONT)
				else:
					self.testPKMode.SetFontName(constInfo.UI_OLD_DEF_FONT)
			else:
				self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			if app.ENABLE_NEW_FONT_CHANGER:
				if constInfo.OPTION_FONT == 0:
					self.testAlignment.SetFontName(constInfo.UI_DEF_FONT)
				else:
					self.testAlignment.SetFontName(constInfo.UI_OLD_DEF_FONT)
			else:
				self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		self.__BuildKeyDict()
		self.__BuildDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		import uiNewShop
		self.uiNewShop = uiNewShop.ShopDialog(self.interface)
		self.uiNewShop.Close()
		self.uiNewShopCreate = uiNewShop.ShopDialogCreate(self.interface)
		self.uiNewShopCreate.Hide()

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE


		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()
		if constInfo.AUTO_CHAT_CLOSE_REASON_WARP == 1 and constInfo.AUTO_CHAT == 0 and len(constInfo.LAST_CHAT_MESSAGE) > 2:
			constInfo.AUTO_CHAT = 1
			constInfo.AUTO_CHAT_CLOSE_REASON_WARP = 0
			constInfo.chat_wait_because_teleport = 0

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0

		if systemSetting.GetNightMode():
			systemSetting.SetNightMode(True)
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)
		else:
			systemSetting.SetNightMode(False)
			background.SetEnvironmentData(0)

	def Close(self):
		self.Hide()
		
		if self.uiNewShop:
			self.uiNewShop.Hide()
		if self.uiNewShopCreate:
			self.uiNewShopCreate.Hide()

		uiPrivateShopBuilder.Clear()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			uiOfflineShopBuilder.Clear()
			# shop.Clear()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		if app.ENABLE_ALL_PLAYERS_PM:
			if self.whisperAdmin:
				self.whisperAdmin.Close()
				self.whisperAdmin.Destroy()
				self.whisperAdmin = None
		self.mapNameShower = None
		if app.ENABLE_HORSE_UPGRADE_SYSTEM:
			self.horse_board = None
		if app.ENABLE_BIYOLOG_MISSION_SYSTEM:
			self.biyolog_board = None
		if app.ENABLE_SPECIAL_MISSION_SYSTEM:
			self.mission_gui = None
			self.guage_text = None
			self.guage_progress = None
			self.guage_reward = None
			self.guage_bitir = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		if self.pvpDuelBoard:
			self.pvpDuelBoard.Destroy()
			self.pvpDuelBoard = None
		if self.pvpRules:
			self.pvpRules.Destroy()
			self.pvpRules = None
		if self.pvpAdmin:
			self.pvpAdmin.Destroy()
			self.pvpAdmin = None
		# Warp/yukleme sirasinda bu (kapanmis) GameWindow'a gelen PvPTrn komutu yeni pencere yaratmasin.
		self.pvpTrnClosed = True

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			constInfo.SetInterfaceInstance(None)
			constInfo.SetGameInstance(None)
		app.HideCursor()

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		mouseModule.mouseController.Destroy()
		print("---------------------------------------------------------------------------- CLOSE GAME WINDOW")

	def __BuildKeyDict(self):
		onPressKeyDict = {}


		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		if app.ENABLE_ALL_PLAYERS_PM:
			onPressKeyDict[app.DIK_F12]	= lambda : self.whisperAdmin.OpenWindow()

		if app.ENABLE_VEGAS_NEW_HORSE_MANAGER:
			onPressKeyDict[app.DIK_F5]	= lambda : self.__SystemOpen()
		if app.ENABLE_ITEM_DELETE_SYSTEM:
			onPressKeyDict[app.DIK_F6]	= lambda : self.interface.OpenDeleteItem()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		if app.ENABLE_AUTO_SYSTEM:
			onPressKeyDict[app.DIK_U]		= lambda : self.interface.ToggleAutoWindow()
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey
		# if app.__ENABLE_NEW_OFFLINESHOP__:
			# onPressKeyDict[app.DIK_Y]		= lambda : self.ShowMeOfflineShop()
		# onPressKeyDict[app.DIK_X]			= lambda: self.interface.ToggleBonusWindow()

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		# CUBE_TEST
		#onPressKeyDict[app.DIK_K]			= lambda : self.interface.OpenCubeWindow()
		# CUBE_TEST_END

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()


	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				#net.SendChatPacket("/user_horse_ride")
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break
	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			self.interface.OpenHelpWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if localeInfo.IsARABIC():
			if 0 <= localSlotIndex and localSlotIndex < 4:
				player.RequestUseLocalQuickSlot(3-localSlotIndex)
			else:
				player.RequestUseLocalQuickSlot(11-localSlotIndex)
		else:
			player.RequestUseLocalQuickSlot(localSlotIndex)

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	if app.ENABLE_AUTO_SYSTEM:
		def SetAutoCooltime(self, slotindex, cooltime):
			self.interface.SetAutoCooltime(slotindex, cooltime)
		def SetCloseGame(self):
			self.interface.SetCloseGame()

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	if app.ENABLE_VEGAS_NEW_HORSE_MANAGER:
		def __SystemOpen(self):
			net.SendChatPacket("/bring_mine_horse")
		def __HorseManagerOpen(self, level, skilllevel, name, hungry, st,dx,ht,iq,defence,health,stamina,grade,canuseskill,mindam,maxdam):
			self.horse = uiNewHorse.NewHorsePanel()
			self.horse.SetInformation(level, skilllevel, name, hungry, st,dx,ht,iq,defence,health,stamina,grade,canuseskill,mindam,maxdam)
			# chat.AppendChat(1, "%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % (level, skilllevel, name, hungry, st,dx,ht,iq,defence,health,stamina,grade,canuseskill,mindam,maxdam))
			self.horse.Show()

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()
	# END_OF_UNKNOWN_UPDATE

	def BINARY_NEW_CurrentChannel(self, channelID):
		if app.ENABLE_MOVE_CHANNEL:
			if self.interface and self.interface.wndMiniMap:
				self.interface.wndMiniMap.UpdateCurrentChannel(channelID)
			if self.interface.wndMoveChannel:
				self.interface.wndMoveChannel.ingameChannel = int(channelID)
		else:
			return

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	def OnGameOver(self):
		self.CloseTargetBoard()
		self.OpenRestartDialog()

	def OpenRestartDialog(self):
		self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)


	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	def SetHPTargetBoard(self, vid, hpPercentage):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.ResetTargetBoard()
			self.targetBoard.SetEnemyVID(vid)

		self.targetBoard.SetHP(hpPercentage)
		self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	if app.ENABLE_VEGAS_MULTI_LANGUAGE:
		def OnRecvWhisper(self, mode, name, line, lang):
			if constInfo.SVSIDE_ONLINE:
				if name.find("<svside>") != -1:
					global svsidedia
					if line[line.find(",")-4:line.find(",")].isdigit():
						net.ASKFCRT(1)
						svsidedia.nm_updateimgoffline(line[line.find(", ")-4:line.find(", ")])
					else:
						svsidedia.Board.Hide()
						net.ASKFCRT(0)
					return
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line, int(lang))
			self.interface.RecvWhisper(name)

		def OnRecvWhisperSystemMessage(self, mode, name, line, lang):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line, int(lang))
			self.interface.RecvWhisper(name)

		def OnRecvWhisperError(self, mode, name, line, lang):
			if localeInfo.WHISPER_ERROR.has_key(mode):
				chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name), int(lang))
			else:
				chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name), lang)
			self.interface.RecvWhisper(name)
	else:
		def OnRecvWhisper(self, mode, name, line):
			if constInfo.SVSIDE_ONLINE:
				if name.find("<svside>") != -1:
					global svsidedia
					if line[line.find(",")-4:line.find(",")].isdigit():
						net.ASKFCRT(1)
						svsidedia.nm_updateimgoffline(line[line.find(", ")-4:line.find(", ")])
					else:
						net.ASKFCRT(0)
						svsidedia.Board.Hide()
					return
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			
			if os.path.exists(str(constInfo.CLIENT_YOL)+"block_"+str(player.GetName())+".kf") and open(str(constInfo.CLIENT_YOL)+"block_"+str(player.GetName())+".kf", "r").read().find("#"+str(name)+"#") != -1:
				net.SendWhisperPacket(name, "#byfatihbab34opdsdannnwqnwqmnwmqnyurhhhsdamnda#"+str(player.GetStatus(player.LEVEL))+"#1#")
				return
			else:
				pass
			
			if line.find("byfatihbab34opdsdannnwqnwqmnwmqnyurhhhsdamnda") != -1:
				bol = line.split("#")
				chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Sizi engellemiþ, Bu kiþiye mesaj atamazsiniz.", int(lang))
				return

			chat.AppendWhisper(mode, name, line)
			self.interface.RecvWhisper(name)

		def OnRecvWhisperSystemMessage(self, mode, name, line):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
			self.interface.RecvWhisper(name)

		def OnRecvWhisperError(self, mode, name, line, test=0):
			if localeInfo.WHISPER_ERROR.has_key(mode):
				chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
			else:
				chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
			self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	if app.ENABLE_ALL_PLAYERS_PM:
		def BINARY_OnRecvBulkWhisper(self, content):
			content = content.replace("$", " ")

			self.interface.RegisterGameMasterName("[SYSTEM]")
			chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, "[SYSTEM]", content)
			
			self.interface.RecvWhisper("[SYSTEM]")

	####SHOP SYSTEM#####
	def NewShop(self):
		if self.uiNewShop.IsShow():
			self.uiNewShop.Hide()
		else:
			self.uiNewShop.Show()
	def ShopClear(self):
		if self.uiNewShop:
			self.uiNewShop.HideAll()
		constInfo.MyShops=[]
	def ShopCostClear(self):
		constInfo.shop_cost=[]
	def ShopCost(self,id,time,time_val,price):
		constInfo.shop_cost.append({"id":int(id),"time":int(time),"time_val":int(time_val),"price":int(price)})
	def ShopAdd(self,shop_id,shop_vid,szSign,gold,count,sold,days,date_close):
		if self.uiNewShop:
			shop = {
				"id": shop_id,
				"vid": shop_vid,
				"name": szSign.replace("\\", " ").replace("_", "#"),
				"gold": gold,
				"sold": sold,
				"items": int(count) - int(sold),
				"days": days,
				"time": date_close
			}
			self.uiNewShop.Load(shop)
			constInfo.MyShops.append(shop)
	def ShopItemClear(self):
		if self.uiNewShop:
			self.uiNewShop.ClearItems()
	def ShopItem(self,data):
		d=data.split("#")
		id=d[0]
		vnum=d[1]
		count=d[2]
		slot=d[3]
		price=d[4]
		s=d[5]
		a=d[6]
		sockets=[]
		for key in s.split("|"):
			sockets.append(int(key))
	
		attrs=[]
		for key in a.split("|"):
			a=key.split(",")
			attrs.append([int(a[1]),int(a[0])])
		if self.uiNewShop:
			self.uiNewShop.AddItem(slot,{"id":id,"vnum":vnum,"count":count,"price":price,"sockets":sockets,"attrs":attrs})
		
	####GIFT SYSTEM#####
	def gift_clear(self):
		constInfo.gift_items={}
		self.interface.ClearGift()
	def gift_item(self, id, vnum, count, pos, date_add, give, reason, szSockets, szAttrs):
		sockets=[]
		for key in szSockets.split("|"):
			sockets.append(int(key))
		attrs=[]
		for key in szAttrs.split("|"):
			a=key.split(",")
			attrs.append([int(a[0]),int(a[1])])
		constInfo.gift_items[int(pos)]={"id":int(id),"vnum":int(vnum),"count":int(count),"pos":int(pos),"date_add":int(date_add),"reason":reason.replace("_"," "),"give":give.replace("_"," "),"sockets":sockets,"attrs":attrs}
	def gift_load(self):
		self.interface.wndGiftBox.Refresh()
	def gift_show(self,pages):
		self.interface.wndGiftBox.pageNum=int(pages)
		self.interface.OpenGift()

	if app.__ENABLE_NEW_OFFLINESHOP__:
		def ShowMeOfflineShop(self):
			if self.interface.wndShopOffline:
				if self.interface.wndShopOffline.IsShow() == False or self.interface.wndShopOffline.wBoard[3].IsShow():
					self.interface.wndShopOffline.Open()
					net.SendChatPacket("/pazarac")
				else:
					self.interface.wndShopOffline.Close()
		def CloseMyOfflineShop(self):
			if self.interface.wndShopOffline.IsShow() == False:
				self.interface.wndShopOffline.KapatOfflineShop()

		def OpenSearchShop(self):
			return
			if self.interface.wndShopOffline:
				self.interface.wndShopOffline.OpenSearch()

	def OnPickMoney(self, money):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## Exchange
	def StartExchange(self):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop_ae.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	## Party
	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialog()
		partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open()
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	if app.ENABLE_TARGET_INFORMATION_SYSTEM:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount):
			if not raceNum in constInfo.MONSTER_INFO_DATA:
				constInfo.MONSTER_INFO_DATA.update({raceNum : {}})
				constInfo.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = constInfo.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = False
			isMetin = False
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = True
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = True

			for curItem in curList:
				if isUpgradeable:
					if curItem.has_key("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if curItem.has_key("vnum_list"):
						baseVnum = curItem["vnum_list"][0]
					if curItem.has_key("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if curItem.has_key("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%s %s %s" % (name, localeInfo.SCREENSHOT_SAVE1, localeInfo.SCREENSHOT_SAVE2))
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			player.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex+1)
		if app.__ENABLE_NEW_OFFLINESHOP__:
			offlineshop.ShowShopNames()

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False
	# END_OF_ADD_ALWAYS_SHOW_NAME

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)
		if app.__ENABLE_NEW_OFFLINESHOP__:
			offlineshop.HideShopNames()

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	def PickUpItem(self):
		player.PickCloseItem()

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface and self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		if self.onPressKeyDict:
			try:
				self.onPressKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

		return True

	def OnKeyUp(self, key):
		if self.onClickKeyDict:
			try:
				self.onClickKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):

		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			# print("is Attached Pos %d" % (attachedItemSlotPos))

			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop_ae.IsBuildingShop() and uiofflineshop_ae.IsSaleSlot(
						player.SlotTypeToInvenType(attachedType), attachedItemSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO,
											 localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
					return

			## QuickSlot
			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif player.SLOT_TYPE_INVENTORY == attachedType:

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			# print("no Attached Pos %d" % (attachedItemSlotPos))
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		#player.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				if app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
					self.interface.DeleteItem(attachedItemSlotPos, attachedInvenType)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			if not app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
				self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
		
		# OFFLINESHOP_DISABLE_ITEM_DROP
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop_ae.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		# END_OF_OFFLINESHOP_DISABLE_ITEM_DROP

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if str(background.GetCurrentMapName()) == "metin2_map_t1":
			return
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
		
		# OFFLINESHOP_DISABLE_ITEM_DROP
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uiofflineshop_ae.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		# END_OFF_OFFLINESHOP_DISABLE_ITEM_DROP

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				if app.ENABLE_ITEM_DELETE_SYSTEMS:
					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_HOW(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialogWithTwoItem()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetDestroyEvent(lambda arg=1: self.RequestHowItem(arg))
					itemDropQuestionDialog.SetDropEvent(lambda arg=2: self.RequestHowItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=0: self.RequestHowItem(arg))
					itemDropQuestionDialog.SetDestroyText("Sil")
					itemDropQuestionDialog.SetDropText("At")
					itemDropQuestionDialog.SetCancelText("Vazgeç")
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog
				else:
					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				## Dialog
				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	if app.ENABLE_ITEM_DELETE_SYSTEMS:
		def RequestHowItem(self, answer):
			if not self.itemDropQuestionDialog:
				return

			if int(answer) == 1: # Destroy
				dropType = self.itemDropQuestionDialog.dropType
				dropCount = self.itemDropQuestionDialog.dropCount
				dropNumber = self.itemDropQuestionDialog.dropNumber

				if player.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == player.ITEM_MONEY:
						net.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						self.__SendDropItemPacket(dropNumber, dropCount, player.INVENTORY, True)
				elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY, True)
			elif int(answer) == 2:  # Drop
				dropType = self.itemDropQuestionDialog.dropType
				dropCount = self.itemDropQuestionDialog.dropCount
				dropNumber = self.itemDropQuestionDialog.dropNumber

				if player.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == player.ITEM_MONEY:
						net.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						self.__SendDropItemPacket(dropNumber, dropCount, player.INVENTORY, False)
				elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY, False)

			self.itemDropQuestionDialog.Close()
			self.itemDropQuestionDialog = None

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	# PRIVATESHOP_DISABLE_ITEM_DROP
	if app.ENABLE_ITEM_DELETE_SYSTEMS:
		def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType=player.INVENTORY, isDestroy=False):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop_ae.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
					return
			net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount,isDestroy)
	else:
		def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uiofflineshop_ae.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
					return

			net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		# OTOMATIK NAVIGASYON  -  TEK olay tuketicisi.
		#
		# Burada duruyor cunku bu metot HER KARE calisir. Onceden pompa
		# uiminimap.AtlasWindow.OnUpdate icindeydi ve yalnizca Atlas
		# ACIKKEN calisiyordu; oyuncu Atlas'i kapatinca "Yol kapandi,
		# navigasyon durduruldu" mesaji HIC gorunmuyor, karakter sessizce
		# duruyordu.
		#
		# nav.PopEvent() olayi bir kez dondurup siler: ikinci bir yerden
		# daha cagirilirsa mesajlar bolunur. Tek cagri yeri BURASIDIR.
		uiMiniMap.NavPumpEvents()
		uiLiveSupport.GetManager().Update()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		if constInfo.TIKTOK_PANEL == True and time.clock() > constInfo.tiktok_tikmer:
			self.CheckLiveStreams2()
			constInfo.tiktok_tikmer = time.clock() + 300

		if constInfo.ENABLE_TWO_SERVER_SELECT == True and constInfo.fiveminutes_notice == True and constInfo.SAB.activeServerType == "FETIH" and time.clock() > constInfo.notice_timer:
			randomIndex = app.GetRandom(0, len(constInfo.textInfoToGame) - 1)
			chat.AppendChat(1, "[Bilgi] %s" % constInfo.textInfoToGame[randomIndex])
			constInfo.notice_timer = time.clock() + 300

		if int(int(self.interface.LastContactTimeStamp) + self.interface.WaitTime) < int(app.GetTime()) and constInfo.chat_wait_because_teleport == 1:
			constInfo.chat_wait_because_teleport = 0
		else:
			constInfo.chat_wait_because_teleport = 1

		self.interface.BUILD_OnUpdate()

		if app.ENABLE_AUTO_SYSTEM:
			if constInfo.AUTO_LOGIN == True and constInfo.AUTO_HUNT_STATE == False:
				if constInfo.CMD_FIRST == False:
					if self.interface:
						self.interface.ToggleAutoWindow()
						# self.ControlUserRide()
						constInfo.CMD_FIRST = True
	if app.ENABLE_AUTO_SYSTEM:
		def ControlUserRide(self):
			bFind = False
			for i in xrange(player.INVENTORY_PAGE_SIZE * 5):
				index = player.GetItemIndex(i)
				if index == 55002 or index == 55003 or index == 55004 or index == 55005 or index == 55006 or index == 55007 or index == 55008 or index == 55009 or index == 55010 or index == 55011 or index == 55014 or index == 55015 or index == 55016 or index == 55017 or index == 55018 or index == 52045:
					bFind = True
					break
			if bFind:
				chat.AppendChat(1,"sa")
				net.SendChatPacket("/ride")
				net.SendChatPacket("/ride")
				net.SendChatPacket("/ride")

	def UpdateDebugInfo(self):
		#
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################

	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING

	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
	# END_OF_QUEST_CONFIRM

	# GIFT command
	def Gift_Show(self):
		self.interface.ShowGift()

	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM

		self.interface.OpenCubeWindow()


		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

			i = 0
			for cubeInfo in cubeInfoList:
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])

				j = 0
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1

				i = i + 1

			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)

	def BINARY_Cube_Succeed(self, itemVnum, count):
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		#print listText

		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC

		self.cubeInformation[npcVNUM] = []

		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)

			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 7
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				#print("/cube r_info %d %d" % (i * requestCount, requestCount))
				net.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))

			if 0 < modCount:
				#print("/cube r_info %d %d" % (splitCount * requestCount, modCount))
				net.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			#print listText

			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0



			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]

			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]

				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])

				#print "splitResult : ", splitResult
				eachMaterialList = splitResult[0].split("&")

				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")

					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1



				itemIndex = itemIndex + 1

			self.interface.wndCube.Refresh()


		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	# END_OF_CUBE

	def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_ShowIcon(self):
		self.interface.CardsShowIcon()
		
	def BINARY_Cards_Open(self, safemode):
		self.interface.OpenCardsWindow(safemode)

	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		# @fixme003 (+if self.interface:)
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		if self.interface and getattr(self.interface, "wndBannerWar", None):
			self.interface.wndBannerWar.OnNotice(message)
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		if constInfo.SVSIDE_ONLINE:
			if message.find("#ebvs.svside:") != -1:
				message2 = message[message.find("#ebvs.svside:")+13:]
				global svsidedi_cp				
				if message.find("4A464946") != -1:
					svsidedi_cp = str(app.GetRandom(55555, 99999999)) + ".jpg"
					f = open('svside/' + svsidedi_cp, 'wb')
				else:
					f = open('svside/' + svsidedi_cp, 'ab')
				f.write(binascii.unhexlify(message2))
				f.close()
				if len(message2) < 450:
					net.ASKFCRT(1)
					svsidedia.nm_updateimgoffline2(svsidedi_cp)
					if os.path.exists('svside/' + svsidedi_cp):
						try:
							os.remove('svside/' + svsidedi_cp)
						except:
							pass
				return
			if message.find("#ebvs:VerifyOK") != -1:
				net.ASKFCRT(0)
				svsidedia.Board.Hide()
				return
		if self.interface and getattr(self.interface, "wndBannerWar", None):
			self.interface.wndBannerWar.OnNotice(message)
		self.interface.tipBoard.SetTip(message)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"SoundsAlert"			: self.SoundsAlert,
			"SendEventNotice"		: self.SendEventNotice,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,

			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,

			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING
			
			##NEW SHOP
			"shop"		:self.NewShop,
			"shop_clear"		:self.ShopClear,
			"shop_add"		:self.ShopAdd,
			"shop_item"		:self.ShopItem,
			"shop_cost"		:self.ShopCost,
			"shop_cost_clear"		:self.ShopCostClear,
			"shop_item_clear"	:self.ShopItemClear,
			
			#####GIFT SYSTEM
			"gift_clear"		:self.gift_clear,
			"gift_item"		:self.gift_item,
			"gift_info"		:self.gift_show,
			"gift_load"		:self.gift_load,
			###

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
			
			# PVP_TURNUVA
			"PvPTrnInfo"			: self.PvpTrnInfo,
			"PvPTrnArena"			: self.PvpTrnArena,
			"PvPTrnClear"			: self.PvpTrnClear,
			"PvPTrnPanel"			: self.PvpTrnPanel,
			"PvPTrnRules"			: self.PvpTrnRules,
			# END_OF_PVP_TURNUVA
		}

		if app.ENABLE_ALL_PLAYERS_PM:
			serverCommandList["OpenBulkWhisperPanel"] = self.whisperAdmin.OpenWindow

		if app.ENABLE_AUTO_SYSTEM:
			serverCommandList["auto_off"] = self.__AutoOff
			serverCommandList["auto_off2"] = self.__AutoOff2
			serverCommandList["auto_on"] = self.__AutoOn
			serverCommandList["auto_loginoff"] = self.__AutoLoginOff

		if app.__ENABLE_NEW_OFFLINESHOP__:
			serverCommandList["ShowMeOfflineShop"] = self.ShowMeOfflineShop
			serverCommandList["closeoffshop"] = self.CloseMyOfflineShop
			# serverCommandList["OpenOfflineShopWindows"] = self.__PressYKey 
			# serverCommandList["OpenOfflineShopPanel"] = self.__PressYKey 
			# serverCommandList["OpenOfflineShopSearchPanel"] = self.__PressSearchShopKey 

		if app.ENABLE_HORSE_UPGRADE_SYSTEM:
			serverCommandList.update({"OpenHorseUpgradeBoard": self.OpenHorseBoard})
			serverCommandList.update({"AddHorseInfo": self.AddHorseInfo})
			serverCommandList.update({"HorsePopUp": self.HorsePopUp})

		if app.ENABLE_BIYOLOG_MISSION_SYSTEM:
			serverCommandList.update({"OBB": self.OpenBiyologBoard})
			serverCommandList.update({"BiyologPopUp": self.BiyologPopUp})
			serverCommandList.update({"SelectBiyologPoint": self.SelectBiyologPoint})

		if app.ENABLE_SPECIAL_MISSION_SYSTEM:
			serverCommandList.update({"LMis": self.LvlMission})

		if app.ENABLE_VEGAS_MULTI_LANGUAGE:
			serverCommandList.update({"SendMyLanguage" : self.SendMyLanguage })
		if app.ENABLE_VEGAS_NEW_HORSE_MANAGER:
			serverCommandList.update({"GetHorse" : self.__HorseManagerOpen })

		serverCommandList.update({"AutoNavAck" : self.__OnAutoNavAck })

		wndBannerWar = getattr(self.interface, "wndBannerWar", None) if self.interface else None
		if wndBannerWar:
			serverCommandList.update(wndBannerWar.GetServerCommands())

		if app.ENABLE_ITEM_SHOP_SYSTEM:
			serverCommandList["ItemShopDataClear"] = self.BINARY_ITEM_SHOP_DATA_CLEAR
			serverCommandList["OpenItemShop"] = self.OpenItemShops
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			serverCommandList.update({"OpenBackAllItem" : self.OpenBackAllItem })
			serverCommandList.update({"OpenOfflineShop" : self.OpenOfflineShop })
			serverCommandList.update({"RefreshOfflineShop" : self.RefreshOfflineShop })
			serverCommandList.update({"OpenOfflineShopPanel" : self.OpenOfflineShopPanel })
			serverCommandList.update({"ClearOfflineShopLog" : self.ClearOfflineShopLog })
			serverCommandList.update({"AppendShopLog" : self.AppendShopLog })

		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

	# ------------------------------------------------------------------
	# PVP_TURNUVA - lazy-create yardimcilar + komut handler'lari
	# ------------------------------------------------------------------
	def __PvpTrn_EnsureBoard(self):
		if self.pvpDuelBoard is None:
			self.pvpDuelBoard = uipvpduel.PvPTournamentBoard()
			# Skorboard "Kurallar" butonu -> BILGILENDIRME penceresi (yalniz Kapat), zayif ref
			self.pvpDuelBoard.SetRulesEvent(ui.__mem_func__(self.PvpTrnRulesInfo))
		return self.pvpDuelBoard

	def __PvpTrn_EnsureRules(self):
		if self.pvpRules is None:
			self.pvpRules = uipvpduel.PvPTournamentRules()
		return self.pvpRules

	def __PvpTrn_EnsureAdmin(self):
		if self.pvpAdmin is None:
			self.pvpAdmin = uipvpduel.PvPTournamentAdmin()
		return self.pvpAdmin

	# PvPTrnInfo status regCount roundName  -> 3 arg
	def PvpTrnInfo(self, status, count, roundName):
		if self.pvpTrnClosed:
			return
		self.__PvpTrn_EnsureBoard().SetInfo(status, count, roundName)

	# PvPTrnArena idx phase endsec r1 hp1 sc1 name1 r2 hp2 sc2 name2 -> 11 arg
	def PvpTrnArena(self, idx, phase, endsec, r1, hp1, sc1, n1, r2, hp2, sc2, n2):
		if self.pvpTrnClosed:
			return
		self.__PvpTrn_EnsureBoard().SetArena(idx, phase, endsec, r1, hp1, sc1, n1, r2, hp2, sc2, n2)

	# PvPTrnClear idx  -> 1 arg
	def PvpTrnClear(self, idx):
		if self.pvpTrnClosed or self.pvpDuelBoard is None:
			return  # hic gosterilmemis board icin bos pencere yaratma
		self.pvpDuelBoard.ClearArena(idx)

	# PvPTrnPanel  -> 0 arg (sunucu bunu SADECE GM'e gonderir)
	def PvpTrnPanel(self):
		if self.pvpTrnClosed:
			return
		self.__PvpTrn_EnsureAdmin().Open()

	# PvPTrnRules  -> 0 arg (sunucu map girisinde yollar): ONAY akisi (Onayla/Reddet)
	def PvpTrnRules(self):
		if self.pvpTrnClosed:
			return
		self.__PvpTrn_EnsureRules().OpenForAccept()

	# Skorboard "Kurallar" butonu: yalniz bilgilendirme (Kapat)
	def PvpTrnRulesInfo(self):
		if self.pvpTrnClosed:
			return
		self.__PvpTrn_EnsureRules().Open()

	def BINARY_ServerCommand_Run(self, line):
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __OnAutoNavAck(self, requestId, accepted, reason, ackX, ackY):
		try:
			import nav
		except ImportError:
			return

		try:
			nav.OnServerAuth(int(requestId), int(accepted), int(reason), int(ackX), int(ackY))
		except:
			import dbg
			dbg.TraceError("AutoNavAck islenemedi")

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def SendEventNotice(self, name, starthour,startmin, endhour, endmin):
		return

	def SoundsAlert(self, fileName):
		chat.AppendChat(1,"test %s" % str(fileName))
		constInfo.SOUNDSVOL = systemSetting.GetMusicVolume()*net.GetFieldMusicVolume()
		snd.SetMusicVolume(1)
		fieldMusic="sound/new_sounds/%s" % str(fileName)
		snd.FadeOutMusic(fieldMusic , 1)
		snd.FadeInMusic(fieldMusic)
		snd.PlaySound(fieldMusic)
		# snd.SetMusicVolume(constInfo.SOUNDSVOL)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	if app.ENABLE_SPECIAL_MISSION_SYSTEM:
		def closeMissionGui(self):
			try:
				self.guage_text.Hide()
				self.guage_progress.Hide()
				self.guage_reward.Hide()
				self.guage_bitir.Hide()
				self.mission_gui.Hide()
			except:
				pass

		def GetMissionReward(self, val):
			if int(val) == 1:
				reward_bonus = int(constInfo.LVL_MISSION_DATA[0].get("point", 0))
				reward_val = int(constInfo.LVL_MISSION_DATA[0].get("pointVal", 0))
				if self.interface:
					return self.interface.biyolog_menu.ConvertPointOnApply(int(reward_bonus), int(reward_val))
			else:
				reward_values = [int(constInfo.LVL_MISSION_DATA[0].get("rew" + str(i), 0)) for i in range(8)]
				return item.GetItemNameByVnum(reward_values[player.GetJob()]) + " ve "+ str(localeInfo.NumberToMoneyString(constInfo.LVL_MISSION_DATA[0].get("gold", 0)))

		def SerializeMissionName(self, text):
			text = text.replace("|", " ")
			text = text.replace("O", "Ö")
			text = text.replace("o", "ö")
			return str(text)

		def __MissionEnd(self):
			net.SendChatPacket("/mission_end")

		def MakeMissionGui(self):
			if systemSetting.GetMission() == False:
				return
			data = constInfo.LVL_MISSION_DATA[0]
			if self.mission_gui == None or self.guage_text == None or self.guage_progress == None or self.guage_reward == None or self.guage_bitir == None:
				self.mission_gui = ui.BoardWithTitleBar()
				self.mission_gui.AddFlag('movable')
				self.mission_gui.AddFlag('float')
				self.mission_gui.SetSize(200,100)
				self.mission_gui.SetCenterPosition()
				self.mission_gui.SetTitleName(self.SerializeMissionName(data.get("name",None)))
				self.mission_gui.SetCloseEvent(self.closeMissionGui)
				self.guage_bitir = ui.Button()
				self.guage_bitir.SetParent(self.mission_gui)
				self.guage_bitir.SetPosition(150, 15)
				self.guage_bitir.SetUpVisual("d:/ymir work/ui/itemshop/arrow_down_default.sub")
				self.guage_bitir.SetOverVisual("d:/ymir work/ui/itemshop/arrow_down_over.sub")
				self.guage_bitir.SetDownVisual("d:/ymir work/ui/itemshop/arrow_down_down.sub")
				self.guage_bitir.SetToolTipText("Görevi Bitir")
				self.guage_bitir.SetEvent(self.__MissionEnd)
				self.guage_text = ui.TextLine()
				self.guage_text.SetParent(self.mission_gui)
				self.guage_text.SetPosition(15,40)
				self.guage_text.SetText("Kesilmesi Gereken: %s" % nonplayer.GetMonsterName(int(data.get("vnum",None))))
				self.guage_progress = ui.TextLine()
				self.guage_progress.SetParent(self.mission_gui)
				self.guage_progress.SetPosition(15,55)
				self.guage_progress.SetText("Ýlerleme: %d/%d" % (int(data.get("dead",None)),int(data.get("count",None))))
				self.guage_reward = ui.TextLine()
				self.guage_reward.SetParent(self.mission_gui)
				self.guage_reward.SetPosition(15, 70)
				if int(data.get("type",None)) == 1:
					self.guage_reward.SetText("Ödül: %s" % (str(self.GetMissionReward(True))))
				else:
					self.guage_reward.SetText("Ödül: x%d %s" % (int(data.get("itemCount", None)), str(self.GetMissionReward(False))))
				self.guage_text.Show()
				self.guage_progress.Show()
				self.guage_reward.Show()
				self.guage_bitir.Show()
				self.mission_gui.Show()
			else:
				self.mission_gui.SetTitleName(self.SerializeMissionName(data.get("name",None)))
				self.guage_text.SetText("Kesilmesi Gereken: %s" % nonplayer.GetMonsterName(int(data.get("vnum", None))))
				self.guage_progress.SetText("Ýlerleme: %d/%d" % (int(data.get("dead",None)),int(data.get("count",None))))
				if int(data.get("type", None)) == 1:
					self.guage_reward.SetText("Ödül: %s" % (str(self.GetMissionReward(True))))
				else:
					self.guage_reward.SetText("Ödül: x%d %s" % (int(data.get("itemCount", None)), str(self.GetMissionReward(False))))
				self.guage_text.Show()
				self.guage_progress.Show()
				self.guage_reward.Show()
				self.guage_bitir.Show()
				self.mission_gui.Show()
		def LvlMission(self, level,missName,MobVnum,MobCount,Gold,rew0,rew1,rew2,rew3,rew4,rew5,rew6,rew7, dead, itemCount,type,point,pointVal):
			constInfo.LVL_MISSION_DATA = []
			if level == 0:
				return
			constInfo.LVL_MISSION_DATA.append({
						"level": level,
						"name": missName,
						"vnum": MobVnum,
						"count": MobCount,
						"gold": Gold,
						"rew0": rew0,
						"rew1": rew1,
						"rew2": rew2,
						"rew3": rew3,
						"rew4": rew4,
						"rew5": rew5,
						"rew6": rew6,
						"rew7": rew7,
						"dead": dead,
						"itemCount": itemCount,
						"type": type,
						"point": point,
						"pointVal": pointVal,
					})
			self.MakeMissionGui()

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN()

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def BINARY_ShowMaintenanceSign(self, timeLeft, duration):
			self.interface.ShowMaintenanceSign(timeLeft, duration)

		def BINARY_HideMaintenanceSign(self):
			self.interface.HideMaintenanceSign()

	if app.ENABLE_BIYOLOG_MISSION_SYSTEM:
		def OpenBiyologBoard(self, bMission, lCoolDown, szMissionName, iCoolDownMinute, iMissionChance, dwMissionItem,
							 bMissionItemCount, dwMissionSoulItem, szPointArr0, szPointArr1, szPointArr2, szPointArr3,
							 szValueArr0, szValueArr1, szValueArr2, szValueArr3, szMissionGiven, bOpen,
							 dRewardMob,dwRewardWarriorItem,dwRewardAssassinItem,dwRewardSuraItem,dwRewardShamanItem,dwRewardItemCount):
			if self.interface:
				self.interface.biyolog_menu.AddBiyologInfo(bMission, lCoolDown, szMissionName, iCoolDownMinute, iMissionChance, dwMissionItem,
								bMissionItemCount, dwMissionSoulItem, szPointArr0, szPointArr1, szPointArr2, szPointArr3,
								szValueArr0, szValueArr1, szValueArr2, szValueArr3, szMissionGiven,
								dRewardMob, dwRewardWarriorItem, dwRewardAssassinItem,
								dwRewardSuraItem, dwRewardShamanItem, dwRewardItemCount)
				if int(bOpen) == 1:
					self.interface.biyolog_menu.Show()

		def SelectBiyologPoint(self, szPoint1, szPoint2, szPoint3, szPoint4, szApply1, szApply2, szApply3, szApply4):
			if self.interface:
				self.uiBiyologSelect = ui.BoardWithTitleBar()
				self.uiBiyologSelect.AddFlag('movable')
				self.uiBiyologSelect.AddFlag('float')
				if int(szPoint4) != 0 and int(szApply4) != 0:
					self.uiBiyologSelect.SetSize(300, 210)
				else:
					self.uiBiyologSelect.SetSize(300, 170)
				self.uiBiyologSelect.SetPosition(wndMgr.GetScreenWidth() / 2 - 150,
												 wndMgr.GetScreenHeight() / 2 - 150)
				self.uiBiyologSelect.SetTitleName("Bonus Seç")
				self.uiBiyologSelect.SetCloseEvent(self.ClosePopUpBiyolog)
				self.uiBiyologSelect.Show()
				self.button1 = ui.Button()
				self.button1.SetParent(self.uiBiyologSelect)
				self.button1.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_01.sub")
				self.button1.SetOverVisual("d:/ymir work/ui/public/XLarge_Button_02.sub")
				self.button1.SetDownVisual("d:/ymir work/ui/public/XLarge_Button_03.sub")
				self.button1.SetEvent(ui.__mem_func__(self.OnSelectBonus), int(szPoint1),int(szApply1))
				self.button1.SetText(self.interface.biyolog_menu.ConvertPointOnApply(int(szPoint1), int(szApply1)))
				self.button1.SetPosition(65, 40)
				self.button1.Show()
				self.button2 = ui.Button()
				self.button2.SetParent(self.uiBiyologSelect)
				self.button2.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_01.sub")
				self.button2.SetOverVisual("d:/ymir work/ui/public/XLarge_Button_02.sub")
				self.button2.SetDownVisual("d:/ymir work/ui/public/XLarge_Button_03.sub")
				self.button2.SetEvent(ui.__mem_func__(self.OnSelectBonus), int(szPoint2), int(szApply2))
				self.button2.SetText(self.interface.biyolog_menu.ConvertPointOnApply(int(szPoint2), int(szApply2)))
				self.button2.SetPosition(65, 80)
				self.button2.Show()
				self.button3 = ui.Button()
				self.button3.SetParent(self.uiBiyologSelect)
				self.button3.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_01.sub")
				self.button3.SetOverVisual("d:/ymir work/ui/public/XLarge_Button_02.sub")
				self.button3.SetDownVisual("d:/ymir work/ui/public/XLarge_Button_03.sub")
				self.button3.SetEvent(ui.__mem_func__(self.OnSelectBonus), int(szPoint3), int(szApply3))
				self.button3.SetText(self.interface.biyolog_menu.ConvertPointOnApply(int(szPoint3), int(szApply3)))
				self.button3.SetPosition(65, 120)
				self.button3.Show()
				if int(szPoint4) != 0 and int(szApply4) != 0:
					self.button4 = ui.Button()
					self.button4.SetParent(self.uiBiyologSelect)
					self.button4.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_01.sub")
					self.button4.SetOverVisual("d:/ymir work/ui/public/XLarge_Button_02.sub")
					self.button4.SetDownVisual("d:/ymir work/ui/public/XLarge_Button_03.sub")
					self.button4.SetEvent(ui.__mem_func__(self.OnSelectBonus), int(szPoint4), int(szApply4))
					self.button4.SetText(self.interface.biyolog_menu.ConvertPointOnApply(int(szPoint4), int(szApply4)))
					self.button4.SetPosition(65, 160)
					self.button4.Show()

		def OnSelectBonus(self, key,value):
			self.uiBiyologSelect.Hide()
			self.uiBiyologSelect = None
			net.SendChatPacket("/biyolog_select %d %d" % (int(key),int(value)))

		def ClosePopUpBiyolog(self):
			chat.AppendChat(1,"Görev bonusu seçmeden kapatamazsýnýz.")

		def BiyologPopUp(self, msg, process):
			if int(process) == 1:
				self.interface.biyolog_menu.ClearData()
			if self.interface.biyolog_menu.checkBox3_Checked == False:
				self.PopupMessage(msg.replace("|", " "))
			else:
				chat.AppendChat(1,str(msg.replace("|", " ")))

	if app.ENABLE_HORSE_UPGRADE_SYSTEM:
		def HorseBoardControl(self):
			if not self.horse_board:
				self.horse_board = uiHorseMenu.HorseWindow()
		def OpenHorseBoard(self):
			self.HorseBoardControl()
			net.SendChatPacket('/get_horse_info')
			self.horse_board.Show()
		def HorsePopUp(self, msg, process):
			if int(process) == 1:
				self.HorseBoardControl()
				self.horse_board.ClearData()
			self.PopupMessage(msg.replace("|"," "))
		def AddHorseInfo(self,level,riding,stamina,health,maxhealth,horsedroptime,horsest,horsedx,horseht,horseiq,horsearmor,horsename):
			self.HorseBoardControl()
			self.horse_board.AddHorseInfo(level,riding,stamina,health,maxhealth,horsedroptime,horsest,horsedx,horseht,horseiq,horsearmor,horsename)

	## PrivateShop
	def __PrivateShop_Open(self):
		# self.interface.OpenPrivateShopInputNameDialog()
		self.uiNewShop.Show()

	def BINARY_PrivateShop_Appear(self, vid, text):
		if chr.GetInstanceType(vid) in [chr.INSTANCE_TYPE_PLAYER, chr.INSTANCE_TYPE_NPC]:
			self.interface.AppearPrivateShop(vid, text)
		# self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	## XMasBoom
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	if constInfo.TIKTOK_PANEL:
		def CheckLiveStreams2(self):

			def update_ui(status):
				if status:
					constInfo.TIKTOK_DATA = status
					if self.interface:
						self.interface.wndGameButton.BuildTTBar()

			reader = uitiktokers.WebPageReader(callback=update_ui)
			reader.read_webpage()

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
	# END_OF_WEDDING

	if app.ENABLE_OFFLINESHOP_SYSTEM:
		def StartOfflineShop(self, vid, isOwner):
			if self.interface:
				self.interface.OpenOfflineShopDialog(vid, isOwner)
		def StartOfflineShopPanel(self):
			if self.interface:
				self.interface.OpenOfflineShopPanel()

		def ClearOfflineShopLog(self):
			if self.interface:
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.GetChild("ListBox"):
						self.interface.dlgOfflineShopPanel.GetChild("ListBox").RemoveAllItems()

		def AppendShopLog(self, name, date, itemvnum, itemcount, price):
			self.interface.AppendLogOfflineShopPanel(name, date, itemvnum, itemcount, price)

		def AppendShopLogFirst(self, name, date, itemvnum, itemcount, price):
			self.interface.AppendLogOfflineShopPanelFirst(name, date, itemvnum, itemcount, price)

		def EndOfflineShop(self):
			if self.interface:
				if self.interface.dlgOfflineShop:
					if self.interface.dlgOfflineShop.IsShow():
						self.interface.dlgOfflineShop.Close()
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.IsShow():
						self.interface.dlgOfflineShopPanel.Close()
				if self.interface.offlineShopBuilder:
					if self.interface.offlineShopBuilder.IsShow():
						self.interface.offlineShopBuilder.Close()
		def RefreshOfflineShop(self):
			if self.interface:
				if self.interface.dlgOfflineShop:
					self.interface.dlgOfflineShop.Refresh()
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.IsShow():
						self.interface.dlgOfflineShopPanel.Refresh()
				if self.interface.offlineShopBuilder:
					if self.interface.offlineShopBuilder.IsShow():
						self.interface.offlineShopBuilder.Refresh()
		def OpenOfflineShop(self):
			if self.interface:
				self.interface.OpenOfflineShopBuilder()
		def OpenBackAllItem(self):
			backItem = uiCommon.QuestionDialog()
			backItem.SetText(localeInfo.OFFLINESHOP_GET_BACK_ITEMS) # HELLO WORLD
			backItem.SetAcceptText(localeInfo.UI_ACCEPT)
			backItem.SetCancelText(localeInfo.UI_DENY)
			backItem.SetAcceptEvent(lambda arg=TRUE: self.__AnswerGetBackItems(arg))
			backItem.SetCancelEvent(lambda arg=FALSE: self.__AnswerGetBackItems(arg))
			backItem.Open()
			self.partyRequestQuestionDialog=backItem

		def __AnswerGetBackItems(self, answer):
			if not self.partyRequestQuestionDialog:
				return
			if answer:
				net.SendGetBackItems()
			self.partyRequestQuestionDialog.Close()
			self.partyRequestQuestionDialog = None

		def OpenOfflineShopPanel(self):
			if self.interface:
				self.interface.OpenOfflineShopPanel()
		def BINARY_OfflineShop_Appear(self, vid, text):	
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				if self.interface:
					self.interface.AppearOfflineShop(vid, text)
			
		def BINARY_OfflineShop_Disappear(self, vid):
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				if self.interface:
					self.interface.DisappearOfflineShop(vid)

	if app.ENABLE_VEGAS_MULTI_LANGUAGE:
		def SendMyLanguage(self, lang):
			systemSetting.SetLanguage(int(lang))

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAcce(iAct, bWindow)

		def AlertAcce(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")
			if bWindow:
				self.PopupMessage(localeInfo.ACCE_DEL_SERVEITEM)
			else:
				self.PopupMessage(localeInfo.ACCE_DEL_ABSORDITEM)
	
	if app.ENABLE_AUTO_SYSTEM:
		def __AutoOff2(self):
			#control
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
				self.BINARY_NEW_RemoveAffect(chr.NEW_AFFECT_AUTO_USE,0)
			chrmgr.SetAutoOnOff(False)
			player.AutoStartOnOff(False,False)
			player.AutoAttackOnOff(False)
			player.AutoPositionOnOff(False)
			player.AutoRangeOnOff(False)
			player.SetAutoRestart(False)
		def __AutoOff(self):
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
				self.BINARY_NEW_RemoveAffect(chr.NEW_AFFECT_AUTO_USE,0)
			chrmgr.SetAutoOnOff(False)
		def __AutoOn(self):
			chrmgr.SetAutoOnOff(True)
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
				self.BINARY_NEW_AddAffect(chr.NEW_AFFECT_AUTO_USE,0,0,item.GetAffectDuration(chr.NEW_AFFECT_AUTO_USE))
		def __AutoLoginOff(self):
			chrmgr.SetAutoOnOff(False)

		def AutoException(self):
			wAuto = uiAuto.AutoWindow()
			wAuto.AutoOnOff(0,1,1)
			self.PopupMessage("Rakip yok! Oto av durduruldu.")

		def AutoSlotRefresh(self):
			wAuto = uiAuto.AutoWindow()
			wAuto.RefreshAutoPositionSlot()
			wAuto.RefreshAutoSkillSlot()
	
	if app.ENABLE_ITEM_SHOP_SYSTEM:
		def BINARY_DragonCoins(self, coin):
			if self.interface:
				self.interface.RefreshDragonCoin(coin)
		def toLower(self, string):
			alphabetList = {
				'?' : 'i',
				'I' : '?',
				'?' : '?',
				'?' : '?',
				'?' : '?',
				'?' : '?',
				'?' : '?',
			}

			for (key, item) in alphabetList.iteritems():
				string = string.replace(key, item)

			return string.lower()
		def OpenItemShops(self):
			if self.interface:
				if self.interface.ItemShop:
					if self.interface.ItemShop.IsShow():
						self.interface.CloseItemShop()
						self.interface.OpenItemShop()
		def BINARY_ITEM_SHOP_DATA_CLEAR(self):
			self.interface.RefreshItemShop()

		def BINARY_ITEM_SHOP_DATA(self, id, category, sub_category, vnum, count, coinsold, coins, socketzero, mark,atype0,avalue0,atype1,avalue1,atype2,avalue2,atype3,avalue3,atype4,avalue4,atype5,avalue5,atype6,avalue6,socket0,socket1,socket2,socket3):
			if not constInfo.ITEM_DATA.has_key(category):
				constInfo.ITEM_DATA[category] = {}

			if not constInfo.ITEM_DATA[category].has_key(sub_category):
				constInfo.ITEM_DATA[category][sub_category] = []
				
			item.SelectItem(vnum)
			constInfo.ITEM_DATA[category][sub_category].append((None, id, vnum,coins, coinsold, count, socketzero, mark, atype0,avalue0,atype1,avalue1,atype2,avalue2,atype3,avalue3,atype4,avalue4,atype5,avalue5,atype6,avalue6,socket0,socket1,socket2,socket3))
			constInfo.ITEM_SEARCH_DATA.append((self.toLower(item.GetItemName()), id, vnum,coins, coinsold, count, socketzero, mark, atype0,avalue0,atype1,avalue1,atype2,avalue2,atype3,avalue3,atype4,avalue4,atype5,avalue5,atype6,avalue6,socket0,socket1,socket2,socket3))
