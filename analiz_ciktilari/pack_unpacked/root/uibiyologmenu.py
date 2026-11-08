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
import chr
import time
import nonplayer
from datetime import datetime, timedelta
from _weakref import proxy

class BiyologWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Initialize()
		self.LoadWindow()

	def Initialize(self):
		self.biyolog_info = []
		self.component = []
		self.component2 = []
		self.checkBox1_Checked = False
		self.checkBox2_Checked = False
		self.checkBox3_Checked = False
		self.tooltipItem = None
		self.timer = 0

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Destroy(self):
		self.biyolog_info = []
		self.component = []
		self.component2 = []
		self.timer = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def OnOverInItem(self, slotIndex):
		if (self.tooltipItem):
			itemVnum = int(self.GetBiyologInfo("dwMissionItem"))
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetBiyologItemToolTip(itemVnum)
	def OnOverInItem2(self, slotIndex):
		if (self.tooltipItem):
			itemVnum = int(self.GetBiyologInfo("dwMissionSoulItem"))
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetBiyologItemToolTip(itemVnum)
	def OnOverOutItem(self):
		if (self.tooltipItem):
			self.tooltipItem.HideToolTip()

	def OverInItemReward(self, slotIndex):
		if (self.tooltipItem):
			itemVnum = int(self.getRewardInfo())
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetBiyologItemToolTip(itemVnum)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/biyolog_menu.py")
		except:
			import exception
			exception.Abort("MobaModeScoreBoard.LoadWindow.LoadObject")
		try:

			self.BBloodThinboard = self.GetChild("biyolog_board")

			self.Mission_Name = self.GetChild("Mission_Name")
			self.Cooldown_text = self.GetChild("Cooldown_text")
			self.Periyod = self.GetChild("Periyod")
			self.Ilerleme = self.GetChild("Ilerleme")

			self.wndItem = self.GetChild("wnd_item_slot")
			self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItemReward))
			self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
			self.wndItem.Hide()

			self.upgrade_Slot = self.GetChild("upgrade_Slot")
			self.upgrade_Slot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
			self.upgrade_Slot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

			self.upgrade_Slot2 = self.GetChild("upgrade_Slot2")
			self.upgrade_Slot2.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem2))
			self.upgrade_Slot2.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

			self.VerButton = self.GetChild("VerButton")
			self.VerButton.SetEvent(ui.__mem_func__(self.BiyologVer))
			self.TitleBar = self.GetChild("TitleBar")

			self.checkBox = ui.CheckBoxNew()
			self.checkBox.SetParent(self.BBloodThinboard)
			self.checkBox.SetPosition(215, 50)
			self.checkBox.SetWindowVerticalAlignBottom()
			self.checkBox.SetEvent(ui.__mem_func__(self.SetUseArchievement), "ON_CHECK", True)
			self.checkBox.SetEvent(ui.__mem_func__(self.SetUseArchievement), "ON_UNCKECK", False)
			self.checkBox.SetCheckStatus(self.checkBox1_Checked)
			self.checkBox.SetTextInfo("Araþtýrmacýnýn Özütü Kullan")
			self.checkBox.Show()

			self.checkBox2 = ui.CheckBoxNew()
			self.checkBox2.SetParent(self.BBloodThinboard)
			self.checkBox2.SetPosition(215, 75)
			self.checkBox2.SetWindowVerticalAlignBottom()
			self.checkBox2.SetEvent(ui.__mem_func__(self.SetUseTimeReset), "ON_CHECK", True)
			self.checkBox2.SetEvent(ui.__mem_func__(self.SetUseTimeReset), "ON_UNCKECK", False)
			self.checkBox2.SetCheckStatus(self.checkBox2_Checked)
			self.checkBox2.SetTextInfo("Süre Sýfýrlayýcý Kullan")
			self.checkBox2.Show()

			self.checkBox3 = ui.CheckBoxNew()
			self.checkBox3.SetParent(self.BBloodThinboard)
			self.checkBox3.SetPosition(215, 25)
			self.checkBox3.SetWindowVerticalAlignBottom()
			self.checkBox3.SetEvent(ui.__mem_func__(self.SetPopUpClose), "ON_CHECK", True)
			self.checkBox3.SetEvent(ui.__mem_func__(self.SetPopUpClose), "ON_UNCKECK", False)
			self.checkBox3.SetCheckStatus(self.checkBox3_Checked)
			self.checkBox3.SetTextInfo("Pop-Up Kapat")
			self.checkBox3.Show()

			self.TitleBar.SetCloseEvent(self.Close)

		except:
			import exception
			exception.Abort("MobaModeScoreBoard.LoadWindow.BindObject")

	def SetUseArchievement(self, checkType, autoFlag):
		self.checkBox1_Checked = autoFlag
		if autoFlag:
			chat.AppendChat(1,"Teslim ederken araþtýrmacýnýn özütü kullanýlacak.")
		else:
			chat.AppendChat(1, "Araþtýrmacýnýn özütü kullanýlmasý devre dýþý býrakýldý.")

	def SetPopUpClose(self, checkType, autoFlag):
		self.checkBox3_Checked = autoFlag
		if autoFlag:
			chat.AppendChat(1, "Pop up bildirim kapatýldý.")
		else:
			chat.AppendChat(1, "Pop up bildirim açýldý.")

	def SetUseTimeReset(self, checkType, autoFlag):
		self.checkBox2_Checked = autoFlag
		if autoFlag:
			chat.AppendChat(1,"Teslim ederken süre sýfýrlayýcý nesne kullanýlacak.")
		else:
			chat.AppendChat(1, "Süre sýfýrlayýcý kullanýlmasý devre dýþý býrakýldý.")

	def BiyologVer(self):
		if not chr.IsGameMaster(0):
			if time.clock() > self.timer:
				net.SendChatPacket("/biyolog_ver %d %d" % (int(self.checkBox1_Checked),int(self.checkBox2_Checked)))
				self.timer = time.clock() + 1
			else:
				remaining_time = (self.timer - time.clock()) * 1000
				chat.AppendChat(1, "{:.2f} ms sonra deneyiniz.".format(remaining_time))
		else:
			net.SendChatPacket("/biyolog_ver %d %d" % (int(self.checkBox1_Checked), int(self.checkBox2_Checked)))

	def ClearData(self):
		self.biyolog_info = []

	def AddBiyologInfo(self, bMission, lCoolDown, szMissionName, iCoolDownMinute, iMissionChance, dwMissionItem,
					bMissionItemCount, dwMissionSoulItem, szPointArr0, szPointArr1, szPointArr2, szPointArr3,
					szValueArr0, szValueArr1, szValueArr2, szValueArr3,szMissionGiven,
					dRewardMob,dwRewardWarriorItem,dwRewardAssassinItem,dwRewardSuraItem,dwRewardShamanItem,dwRewardItemCount):
		self.biyolog_info.append({
			"bMission": bMission,
			"lCoolDown": lCoolDown,
			"szMissionName": szMissionName,
			"iCoolDownMinute": iCoolDownMinute,
			"iMissionChance": iMissionChance,
			"dwMissionItem": dwMissionItem,
			"bMissionItemCount": bMissionItemCount,
			"dwMissionSoulItem": dwMissionSoulItem,
			"szPointArr0": szPointArr0,
			"szPointArr1": szPointArr1,
			"szPointArr2": szPointArr2,
			"szPointArr3": szPointArr3,
			"szValueArr0": szValueArr0,
			"szValueArr1": szValueArr1,
			"szValueArr2": szValueArr2,
			"szValueArr3": szValueArr3,
			"szMissionGiven": szMissionGiven,
			"dRewardMob": dRewardMob,
			"dwRewardWarriorItem": dwRewardWarriorItem,
			"dwRewardAssassinItem": dwRewardAssassinItem,
			"dwRewardSuraItem": dwRewardSuraItem,
			"dwRewardShamanItem": dwRewardShamanItem,
			"dwRewardItemCount": dwRewardItemCount,
		})
		self.BuildBonus()
		self.BuildItem()

	def GetBiyologInfo(self, attribute):
		biyolog_data = self.biyolog_info[0]
		return biyolog_data.get(attribute, None)

	def getRewardInfo(self):
		job = player.GetJob()
		if job == 0 or job == 4:
			return int(self.GetBiyologInfo("dwRewardWarriorItem"))
		if job == 1 or job == 5:
			return int(self.GetBiyologInfo("dwRewardAssassinItem"))
		if job == 2 or job == 6:
			return int(self.GetBiyologInfo("dwRewardSuraItem"))
		if job == 3 or job == 7:
			return int(self.GetBiyologInfo("dwRewardShamanItem"))

	def BuildItem(self):
		if self.getRewardInfo() != 0:
			self.component2 = []
			wndText2 = ui.TextLine()
			wndText2.SetParent(self.BBloodThinboard)
			wndText2.SetText("Yok Et: %s" % str(nonplayer.GetMonsterName(int(self.GetBiyologInfo("dRewardMob")))))
			wndText2.SetPosition(250, 140)
			wndText2.Show()
			wndText = ui.TextLine()
			wndText.SetParent(self.BBloodThinboard)
			wndText.SetText("Elde edilecek eþya:")
			wndText.SetPosition(251,150)
			self.wndItem.SetItemSlot(0, self.getRewardInfo(), int(self.GetBiyologInfo("dwRewardItemCount")))
			self.wndItem.Show()
			wndText.Show()
			wndText2.Show()
			self.component2.append(wndText)
			self.component2.append(wndText2)
		else:
			for i in self.component2:
				i.Hide()
			self.wndItem.Hide()

	def ConvertPointOnApply(self, point,value):
		if self.tooltipItem and point != 0:
			return self.tooltipItem.GetAffectStr(int(point),int(value))

	def BuildBonus(self):
		self.component = []

		TextLayn2 = ui.TextLine()
		TextLayn2.SetParent(self.BBloodThinboard)
		TextLayn2.SetPosition(228, 98)
		TextLayn2.SetText("Yok Et:")
		SlotBar2 = ui.SlotBar()
		SlotBar2.SetParent(self.BBloodThinboard)
		SlotBar2.SetSize(105, 18)
		SlotBar2.SetPosition(287, 95)
		SlotText2 = ui.TextLine()
		SlotText2.SetParent(SlotBar2)
		SlotText2.SetPosition(3, 3)
		SlotText2.SetSize(90, 18)
		SlotText2.SetText("%s" % str(nonplayer.GetMonsterName(int(self.GetBiyologInfo("dRewardMob")))))
		TextLayn2.Show()
		SlotBar2.Show()
		SlotText2.Show()
		self.component.append(TextLayn2)
		self.component.append(SlotBar2)
		self.component.append(SlotText2)

		count = 0
		yStart = 180
		for i in range(4):
			if int(self.GetBiyologInfo("szPointArr%d" % int(count))) == 0:
				continue
			TextLayn = ui.TextLine()
			TextLayn.SetParent(self.BBloodThinboard)
			TextLayn.SetPosition(207,yStart+3)
			TextLayn.SetText("Görev Bonusu %d:" % int(count+1))
			SlotBar = ui.SlotBar()
			SlotBar.SetParent(self.BBloodThinboard)
			SlotBar.SetSize(105,18)
			SlotBar.SetPosition(288,yStart)
			SlotText = ui.TextLine()
			SlotText.SetParent(SlotBar)
			SlotText.SetPosition(3,3)
			SlotText.SetSize(90,18)

			SlotText.SetText(self.ConvertPointOnApply(int(self.GetBiyologInfo("szPointArr%d" % int(count))), int(self.GetBiyologInfo("szValueArr%d" % int(count)))))

			TextLayn.Show()
			SlotBar.Show()
			SlotText.Show()

			self.component.append(TextLayn)
			self.component.append(SlotBar)
			self.component.append(SlotText)

			count += 1
			yStart += 20

	def ConvertTime(self, times):
		current_time_stamp = app.GetGlobalTimeStamp()
		future_time_stamp = current_time_stamp + times

		time_remaining = future_time_stamp - app.GetGlobalTimeStamp()

		if time_remaining <= 0:
			return "Verilebilir!"

		hour = int((time_remaining / 3600) % 24)
		minute = int((time_remaining / 60) % 60)
		seconds = int(time_remaining % 60)
		if hour == 0:
			return "%d Dakika %d Saniye" % (minute, seconds)
		else:
			return "%d Saat %d Dakika" % (hour, minute)

	def minute_to_hour_and_day(self,minutes):
		hours = minutes / 60
		days = hours / 24
		if days != 0:
			result = "{} dakika, {:.2f} saat veya {:.2f} gün.".format(minutes, hours, days)
		else:
			result = "{} dakika".format(minutes)

		return result

	def progress_info(self, given, max):
		return "{} / {}".format(given, max)

	def SerializeMissionName(self, text):
		text = text.replace("|", " ")
		text = text.replace("g", "ð")
		text = text.replace("s", "þ")
		return str(text)

	def OnUpdate(self):
		if self.biyolog_info:
			self.Mission_Name.SetText(self.SerializeMissionName(self.GetBiyologInfo("szMissionName")))
			self.upgrade_Slot.SetItemSlot(0, int(self.GetBiyologInfo("dwMissionItem")), int(self.GetBiyologInfo("bMissionItemCount")))
			self.upgrade_Slot2.SetItemSlot(0, int(self.GetBiyologInfo("dwMissionSoulItem")), 1)
			self.Cooldown_text.SetText(self.ConvertTime(int(self.GetBiyologInfo("lCoolDown"))))
			self.Periyod.SetText(self.minute_to_hour_and_day(int(self.GetBiyologInfo("iCoolDownMinute"))))
			self.Ilerleme.SetText(self.progress_info(int(self.GetBiyologInfo("szMissionGiven")),int(self.GetBiyologInfo("bMissionItemCount"))))

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
	def Close(self):
		self.Destroy()
		self.Hide()

