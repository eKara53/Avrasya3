import dbg
import ui
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import chrmgr
import player
import musicInfo

import uiSelectMusic
import background

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.nightModeOptionButtonList = []
		if app.ENABLE_VEGAS_MULTI_LANGUAGE:
			self.languageModeButtonList = []
		if app.ENABLE_NEW_FONT_CHANGER:
			self.fontModeList = []
		# if app.ENABLE_SPECIAL_MISSION_SYSTEM:
		# self.MissionList = []
		self.ctrlShadowQuality = 0
		if app.__BL_ENVIRONMENT_EFFECT_OPTION__:
			self.snowModeButtonList			= []
			self.snowTextureModeButtonList	= []


	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			if app.ENABLE_VEGAS_MULTI_LANGUAGE:
				self.languageModeButtonList.append(GetObject("lang_tr"))
				self.languageModeButtonList.append(GetObject("lang_en"))
				self.languageModeButtonList.append(GetObject("lang_de"))
				self.languageModeButtonList.append(GetObject("lang_ro"))
				self.languageModeButtonList.append(GetObject("lang_it"))
			if app.ENABLE_NEW_FONT_CHANGER:
				self.fontModeList.append(GetObject("font_old"))
				self.fontModeList.append(GetObject("font_new"))
			# if app.ENABLE_SPECIAL_MISSION_SYSTEM:
			# self.MissionList.append(GetObject("mission_false"))
			# self.MissionList.append(GetObject("mission_true"))
			self.tilingApplyButton=GetObject("tiling_apply")
			#self.ctrlShadowQuality = GetObject("shadow_bar")
			self.nightModeOptionButtonList.append(GetObject("night_on"))
			self.nightModeOptionButtonList.append(GetObject("night_off"))
			if app.__BL_ENVIRONMENT_EFFECT_OPTION__:
				self.snowModeButtonList.append(GetObject("snow_mode_off"))
				self.snowModeButtonList.append(GetObject("snow_mode_on"))
				self.snowTextureModeButtonList.append(GetObject("snow_texture_mode_off"))
				self.snowTextureModeButtonList.append(GetObject("snow_texture_mode_on"))


		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

		self.nightModeOptionButtonList[0].SAFE_SetEvent(self.__OnClickNightModeOptionEnableButton)
		self.nightModeOptionButtonList[1].SAFE_SetEvent(self.__OnClickNightModeOptionDisableButton)

		if app.ENABLE_VEGAS_MULTI_LANGUAGE:
			self.languageModeButtonList[0].SAFE_SetEvent(self.__OnClickTRLanguage)
			self.languageModeButtonList[1].SAFE_SetEvent(self.__OnClickENLanguage)
			self.languageModeButtonList[2].SAFE_SetEvent(self.__OnClickDELanguage)
			self.languageModeButtonList[3].SAFE_SetEvent(self.__OnClickROLanguage)
			self.languageModeButtonList[4].SAFE_SetEvent(self.__OnClickITLanguage)
			self.RefreshLanguageList()

		if app.ENABLE_NEW_FONT_CHANGER:
			self.fontModeList[0].SAFE_SetEvent(self.__OnClickOldFont)
			self.fontModeList[1].SAFE_SetEvent(self.__OnClickNewFont)
			self.RefreshFontList()

		# if app.ENABLE_SPECIAL_MISSION_SYSTEM:
		# self.MissionList[0].SAFE_SetEvent(self.__MissionClose)
		# self.MissionList[1].SAFE_SetEvent(self.__MissionOpen)
		# self.RefreshMissionList()

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if app.__BL_ENVIRONMENT_EFFECT_OPTION__:
			self.snowModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowModeOffButton)
			self.snowModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowModeOnButton)
			self.__InitSnowModeOption()
			
			self.snowTextureModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowTextureModeOffButton)
			self.snowTextureModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowTextureModeOnButton)		
			self.__InitSnowTextureModeOption()


		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

	if app.__BL_ENVIRONMENT_EFFECT_OPTION__:
		def __InitSnowModeOption(self):
			self.SnowModeOn	= systemSetting.GetSnowModeOption()
			self.__ClickRadioButton(self.snowModeButtonList, self.SnowModeOn)
			background.SetSnowModeOption(self.SnowModeOn)
	
		def __InitSnowTextureModeOption(self):
			self.SnowTextureModeOn	= systemSetting.GetSnowTextureModeOption()
			self.__ClickRadioButton(self.snowTextureModeButtonList, self.SnowTextureModeOn)
			background.SetSnowTextureModeOption(self.SnowTextureModeOn)
			
		def __OnClickSnowModeOffButton(self):
			self.__ClickRadioButton(self.snowModeButtonList, 0)
			self.__SetSnowMode(0)
			
		def __OnClickSnowModeOnButton(self):
			self.__ClickRadioButton(self.snowModeButtonList, 1)
			self.__SetSnowMode(1)
			
		def __OnClickSnowTextureModeOffButton(self):
			self.__ClickRadioButton(self.snowTextureModeButtonList, 0)
			self.__SetSnowTextureMode(0)
			
		def __OnClickSnowTextureModeOnButton(self):
			self.__ClickRadioButton(self.snowTextureModeButtonList, 1)
			self.__SetSnowTextureMode(1)
			
		def __SetSnowMode(self, index):
			systemSetting.SetSnowModeOption(index)
			background.SetSnowModeOption(index)
			background.EnableSnowMode(index)
	
		def __SetSnowTextureMode(self, index):
			systemSetting.SetSnowTextureModeOption(index)
			background.SetSnowTextureModeOption(index)
			background.EnableSnowTextureMode()
	
		def __SetNightMode(self, index):
			systemSetting.SetNightModeOption(index)	
			background.SetNightModeOption(index)
			
			if not background.GetDayMode():
				return
				
			if not background.IsBoomMap():
				return
			
			if 1 == index:
				self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)
			else:
				self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)		
		
		def __DayMode_OnCompleteChangeToLight(self):
			background.ChangeEnvironmentData(0)
			self.curtain.FadeIn()
	
		def __DayMode_OnCompleteChangeToDark(self):		
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.ChangeEnvironmentData(1)
			self.curtain.FadeIn()

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:

			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()

	# if app.ENABLE_SPECIAL_MISSION_SYSTEM:
	# def RefreshMissionList(self):
		# self.__ClickRadioButton(self.MissionList, systemSetting.IsShowLevel())
	# def __MissionOpen(self):
		# self.__ClickRadioButton(self.MissionList, 1)
		# systemSetting.SetShowLevelFlag(1)
		# chat.AppendChat(1, "Artýk Level Gösterilecek.")
	# def __MissionClose(self):
		# self.__ClickRadioButton(self.MissionList, 0)
		# systemSetting.SetShowLevelFlag(0)
		# chat.AppendChat(1, "Artýk Level Gösterilmeyecek.")

	if app.ENABLE_NEW_FONT_CHANGER:
		def RefreshFontList(self):
			self.__ClickRadioButton(self.fontModeList, systemSetting.GetFontMode())
		def __OnClickOldFont(self):
			constInfo.OPTION_FONT = 0
			self.__ClickRadioButton(self.fontModeList, 0)
			systemSetting.SetFontMode(0)
			chat.AppendChat(1,"Tamamen çalýþmasý için lütfen ýþýnlanýn.")
			app.SetDefaultFontName(constInfo.UI_DEF_FONT)
		def __OnClickNewFont(self):
			constInfo.OPTION_FONT = 1
			self.__ClickRadioButton(self.fontModeList, 1)
			systemSetting.SetFontMode(1)
			chat.AppendChat(1,"Tamamen çalýþmasý için lütfen ýþýnlanýn.")
			app.SetDefaultFontName(constInfo.UI_OLD_DEF_FONT)

	if app.ENABLE_VEGAS_MULTI_LANGUAGE:
		def RefreshLanguageList(self):
			self.__ClickRadioButton(self.languageModeButtonList, systemSetting.GetLanguage())
		def __OnClickTRLanguage(self):
			self.__ClickRadioButton(self.languageModeButtonList, 0)
			systemSetting.SetLanguage(0)
			net.SendChatPacket("/change_language %d" % (int(0)))
			chat.AppendChat(1,"Tamamen çalýþmasý için lütfen oyunu tekrar açýn.")
		def __OnClickENLanguage(self):
			self.__ClickRadioButton(self.languageModeButtonList, 1)
			systemSetting.SetLanguage(1)
			net.SendChatPacket("/change_language %d" % (int(1)))
			chat.AppendChat(1,"Please reopen the game for it to fully work.")
		def __OnClickDELanguage(self):
			self.__ClickRadioButton(self.languageModeButtonList, 2)
			systemSetting.SetLanguage(2)
			net.SendChatPacket("/change_language %d" % (int(2)))
			chat.AppendChat(1,"Bitte öffnen Sie das Spiel erneut, damit es vollständig funktioniert.")
		def __OnClickROLanguage(self):
			self.__ClickRadioButton(self.languageModeButtonList, 3)
			systemSetting.SetLanguage(3)
			net.SendChatPacket("/change_language %d" % (int(3)))
			chat.AppendChat(1,"Va rugam sa redeschideti jocul pentru ca acesta sa functioneze complet.")
		def __OnClickITLanguage(self):
			self.__ClickRadioButton(self.languageModeButtonList, 4)
			systemSetting.SetLanguage(4)
			net.SendChatPacket("/change_language %d" % (int(4)))
			chat.AppendChat(1,"Riapri il gioco affinché funzioni completamente.")

	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()

		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def __OnClickNightModeOptionEnableButton(self):
		systemSetting.SetNightMode(True)
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.RefreshNightOption()

	def __OnClickNightModeOptionDisableButton(self):
		systemSetting.SetNightMode(False)
		background.SetEnvironmentData(0)
		self.RefreshNightOption()

	def RefreshNightOption(self):
		if systemSetting.GetNightMode():
			self.nightModeOptionButtonList[0].Down()
			self.nightModeOptionButtonList[1].SetUp()
		else:
			self.nightModeOptionButtonList[0].SetUp()
			self.nightModeOptionButtonList[1].Down()

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.__SetCurTilingMode()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)

