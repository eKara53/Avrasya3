# DUMPED FROM LIVE COMPILE: uiGameButton.py (len=4499)
import app
import ui
import player
import net

import constInfo
if constInfo.TIKTOK_PANEL:
	import wndMgr
	import webbrowser
	import random
	import time
	from datetime import datetime, timedelta

class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow("UIScript/gamewindow.py")
		if constInfo.TIKTOK_PANEL:
			self.TiktokPanel = []
			self.tiktok_tikmer = 0
			self.build_bar = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, filename)
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		try:
			self.gameButtonDict={
				"STATUS" : self.GetChild("StatusPlusButton"),
				"SKILL" : self.GetChild("SkillPlusButton"),
				"QUEST" : self.GetChild("QuestButton"),
				"HELP" : self.GetChild("HelpButton"),
				"BUILD" : self.GetChild("BuildGuildBuilding"),
				"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
				"GIFT" : self.GetChild("GiftIcon"),
			}

			self.gameButtonDict["EXIT_OBSERVER"].SetEvent(ui.__mem_func__(self.__OnClickExitObserver))

		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		self.__HideAllGameButton()
		self.SetObserverMode(player.IsObserverMode())
		return True

	if constInfo.TIKTOK_PANEL:
		def BuildTTBar(self):
			self.TiktokPanel = []
			i = 0
			online_count = 0
			randomColor = [ "|cffCD661D", "|cffff6060", "|cff0000ff", "|cffDA70D6" ]
			if constInfo.TIKTOK_PANEL and constInfo.TIKTOK_DATA:
				for key, value in constInfo.TIKTOK_DATA.items():
					if value == "online":
						tiktokBg = ui.Button()
						tiktokBg.SetParent(self)
						tiktokBg.SetPosition(wndMgr.GetScreenWidth() - 190 - 160, 25)
						tiktokBg.SetUpVisual('sosyal/tiktokas_default.png')
						tiktokBg.SetOverVisual('sosyal/tiktokas_over.png')
						tiktokBg.SetDownVisual('sosyal/tiktokas_down.png')
						tiktokBg.SetText("    %s@%s yayýnda!"%(str(random.choice(randomColor)),str(key)))
						tiktokBg.SetEvent(ui.__mem_func__(self.OpenUrl),str(key))
						if i == 0:
							tiktokBg.Show()
						else:
							tiktokBg.Hide()
						i = i + 1
						online_count = online_count + 1
						self.TiktokPanel.append(tiktokBg)
			if online_count == 0:
				if self.TiktokPanel:
					for button in self.TiktokPanel:
						button.Hide()
		def OnUpdate(self):
			if constInfo.TIKTOK_PANEL and constInfo.TIKTOK_DATA and self.build_bar == False:
				self.BuildTTBar()
				self.build_bar = True
			if time.clock() > self.tiktok_tikmer:
				for button in self.TiktokPanel:
					button.Hide()
				if self.TiktokPanel:
					random_button = random.choice(self.TiktokPanel)
					random_button.Show()
					# random_button.Flash()
				self.tiktok_tikmer = time.clock() + 5
		def OpenUrl(self, url):
			link = "https://www.tiktok.com/@%s/live" % url
			webbrowser.open(link)

	def Destroy(self):
		for key in self.gameButtonDict:
			self.gameButtonDict[key].SetEvent(0)

		self.gameButtonDict={}

	def SetButtonEvent(self, name, event):
		try:
			self.gameButtonDict[name].SetEvent(event)
		except Exception, msg:
			print "GameButtonWindow.LoadScript - %s" % (msg)
			app.Abort()
			return

	def ShowGiftButton(self):
		self.gameButtonDict["GIFT"].Show()

	def HideGiftButton(self):
		self.gameButtonDict["GIFT"].Hide()

	def ShowBuildButton(self):
		self.gameButtonDict["BUILD"].Show()

	def HideBuildButton(self):
		self.gameButtonDict["BUILD"].Hide()

	def CheckGameButton(self):

		if not self.IsShow():
			return

		statusPlusButton=self.gameButtonDict["STATUS"]
		skillPlusButton=self.gameButtonDict["SKILL"]
		helpButton=self.gameButtonDict["HELP"]

		if player.GetStatus(player.STAT) > 0:
			statusPlusButton.Show()
		else:
			statusPlusButton.Hide()

		if self.__IsSkillStat():
			skillPlusButton.Show()
		else:
			skillPlusButton.Hide()

		if 0 == player.GetPlayTime():
			helpButton.Show()
		else:
			helpButton.Hide()

	def __IsSkillStat(self):
		if player.GetStatus(player.SKILL_ACTIVE) > 0:
			return True

		return False

	def __OnClickExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()

	def SetObserverMode(self, isEnable):
		if isEnable:
			self.gameButtonDict["EXIT_OBSERVER"].Show()
		else:
			self.gameButtonDict["EXIT_OBSERVER"].Hide()
