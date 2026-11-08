import ui
import net
import app
import grp
import uiCommon
import constInfo
import chat
import player
import localeInfo
import uiToolTip
import uiScriptLocale
import mouseModule
import wndMgr
import time
from datetime import datetime, timedelta
from _weakref import proxy

class HorseWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Initialize()
		self.LoadWindow()

	def Initialize(self):
		self.horse_info = []
		self.timer = 0

	def Destroy(self):
		self.horse_info = []
		self.timer = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/horse_menu.py")
		except:
			import exception
			exception.Abort("MobaModeScoreBoard.LoadWindow.LoadObject")
		try:
		
			self.BBloodThinboard = self.GetChild("horse_board")
			self.Horse_Level = self.GetChild("Horse_Level")
			self.Horse_Ride = self.GetChild("Horse_Ride")
			self.Horse_Stamina = self.GetChild("Horse_Stamina")
			self.Horse_HP_and_MAXHP = self.GetChild("Horse_HP_and_MAXHP")
			self.Horse_Time = self.GetChild("Horse_Time")
			self.Horse_STR = self.GetChild("Horse_STR")
			self.Horse_DX = self.GetChild("Horse_DX")
			self.Horse_HT = self.GetChild("Horse_HT")
			self.Horse_IQ = self.GetChild("Horse_IQ")
			self.Horse_DEF = self.GetChild("Horse_DEF")
			self.Horse_DEF = self.GetChild("Horse_DEF")
			self.Horse_Name = self.GetChild("Horse_Name")

			self.upgrade_Slot = self.GetChild("upgrade_Slot")
			self.Money = self.GetChild("Money")

			self.Horse_Upgrade_Button = self.GetChild("Horse_Upgrade_Button")
			self.Horse_Upgrade_Button.SetToolTipText("Atý Geliþtir")
			self.Horse_Upgrade_Button.SetEvent(ui.__mem_func__(self.HorseAdvance))
			self.TitleBar = self.GetChild("TitleBar")

			self.TitleBar.SetCloseEvent(self.Close)

		except:
			import exception
			exception.Abort("MobaModeScoreBoard.LoadWindow.BindObject")

	def ClearData(self):
		self.horse_info = []

	def HorseAdvance(self):
		if time.clock() > self.timer:
			net.SendChatPacket("/my_horse_upgrade")
			self.timer = time.clock() + 1
		else:
			remaining_time = (self.timer - time.clock()) * 1000  # Kalan süreyi milisaniye cinsine dönüþtür
			chat.AppendChat(1, "{:.2f} ms sonra deneyiniz.".format(remaining_time))

	def AddHorseInfo(self, level,riding,stamina,health,maxhealth,horsedroptime,horsest,horsedx,horseht,horseiq,horsearmor,horsename):
		self.horse_info.append({
			"level": level,
			"riding": riding,
			"stamina": stamina,
			"health": health,
			"maxhealth": maxhealth,
			"horsedroptime": horsedroptime,
			"horsest": horsest,
			"horsedx": horsedx,
			"horseht": horseht,
			"horseiq": horseiq,
			"horsearmor": horsearmor,
			"horsename": horsename
		})

	def GetHorseInfo(self, attribute):
		horse_data = self.horse_info[0]
		return horse_data.get(attribute, None)

	def OnUpdate(self):
		if self.horse_info:
			self.Horse_Level.SetText(self.GetHorseInfo("level"))
			self.Horse_Ride.SetText("Sürüþ yapýlýyor." if self.GetHorseInfo("riding") == 1 else "Sürüþ bitmiþ.")
			self.Horse_Stamina.SetText(self.GetHorseInfo("stamina"))
			self.Horse_HP_and_MAXHP.SetText("%s / %s" % (str(self.GetHorseInfo("health")),str(self.GetHorseInfo("maxhealth"))))
			self.Horse_Time.SetText(self.calculate_time_difference(long(self.GetHorseInfo("horsedroptime"))))
			self.Horse_STR.SetText(self.GetHorseInfo("horsest"))
			self.Horse_DX.SetText(self.GetHorseInfo("horsedx"))
			self.Horse_HT.SetText(self.GetHorseInfo("horseht"))
			self.Horse_IQ.SetText(self.GetHorseInfo("horseiq"))
			self.Horse_DEF.SetText(self.GetHorseInfo("horsearmor"))
			self.Horse_Name.SetText(self.GetHorseInfo("horsename"))

			self.upgrade_Slot.SetItemSlot(0, 50050, 1)
			self.Money.SetText(localeInfo.NumberToMoneyString(100000))

	def calculate_time_difference(self,timestamp):
		target_date = datetime.fromtimestamp(timestamp)
		now = datetime.now()
		difference = target_date - now
		years = difference.days // 365
		days = difference.days % 365
		hours = difference.seconds // 3600
		minutes = (difference.seconds % 3600) // 60
		if difference.total_seconds() > 0:
			return "{0} yýl, {1} gün, {2} saat, {3} dakika sonra".format(years, days, hours, minutes)
		else:
			return "{0} yýl, {1} gün, {2} saat, {3} dakika önce".format(years, days, hours, minutes)

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
	def Close(self):
		self.Destroy()
		self.Hide()

