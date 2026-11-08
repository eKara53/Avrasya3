import ui
import app
import localeInfo
import constInfo
import player
import net
import chrmgr
import wndMgr
import mouseModule
import guild
import skill
import item
import chr
import uiToolTip
import time
import chat
import background

class AutoWindow(ui.ScriptWindow):
	AUTO_COOLTIME_POS_Y = 4
	AUTO_COOLTIME_POS_X = 6
	AUTO_COOLTIME_MAX = AUTO_COOLTIME_POS_Y * AUTO_COOLTIME_POS_X
	AUTO_ONOFF_START = 1
	AUTO_ONOFF_ATTACK = 2
	AUTO_ONOFF_SKILL = 3
	AUTO_ONOFF_POSITION = 4
	AUTO_ONOFF_AUTO_RANGE = 5
	AUTO_ONOFF_AUTO_RESTART = 6

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isloded = 0
		self.timer = 0
		self.isOpen = 0
		self.tooltipSkill = 0
		self.tooltipItem = 0
		self.autostartonoff = 0
		self.autoslotindex = {}
		# self.timeeditlist = {}
		self.autoonoffbuttonlist =[]
		self.autoonoffbuttonlist2 =[]
		# self.saveButton = 0
		self.autoslot = None
		# self.AutoSkillClearButton = None
		self.AutoPositionClearButton = None
		self.AutoAllClearButton = None
		self.AutoToolTipButton = None
		self.AutoToolTip = None
		for i in xrange(player.AUTO_SKILL_SLOT_MAX):
			self.autoslotindex[i] = 0

		for i in range(player.AUTO_POSITINO_SLOT_START,player.AUTO_POSITINO_SLOT_MAX):
			self.autoslotindex[i] = 0

		self.AutoSystemToolTipList = [localeInfo.AUTO_TOOLTIP_LINE1, 
		localeInfo.AUTO_TOOLTIP_LINE2, 
		localeInfo.AUTO_TOOLTIP_LINE3,
		localeInfo.AUTO_TOOLTIP_LINE4,
		localeInfo.AUTO_TOOLTIP_LINE5]
		self.closegame = False
		self.LoadAutoWindow()
		self.isFirstReadFile = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isloded = 0
		self.isOpen = 0
		self.tooltipSkill = 0
		self.tooltipItem = 0
		self.autostartonoff = 0
		self.autoslotindex = {}
		# self.timeeditlist = {}
		self.autoonoffbuttonlist =[]
		self.autoonoffbuttonlist2 =[]
		# self.saveButton = 0
		self.autoslot = None
		# self.AutoSkillClearButton = None
		self.AutoPositionClearButton = None
		self.AutoAllClearButton = None
		self.AutoToolTipButton = None
		self.AutoToolTip = None
		self.closegame = False
		self.isFirstReadFile = False

	def __LoadWindow(self):
		try:
			GetObject = self.GetChild
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AutoWindow.py")
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			# self.saveButton = self.GetChild("AutoSaveOnButton")
			# self.saveButton.SetEvent(ui.__mem_func__(self.SaveAutoInfo))

			autostartbutton = self.GetChild("AutoStartOnButton")
			autostartbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_START, 0)
			self.autoonoffbuttonlist.append(autostartbutton)

			autostartbutton = self.GetChild("AutoStartOffButton")
			autostartbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_START, 1)
			autostartbutton.Down()
			autostartbutton.Disable()
			self.autoonoffbuttonlist.append(autostartbutton)
			
			checkBox = ui.CheckBox()
			checkBox.SetParent(self)
			checkBox.SetPosition(78, 35)
			checkBox.SetWindowVerticalAlignBottom()
			checkBox.SetEvent(ui.__mem_func__(self.SetAutoLogin), "ON_CHECK", True)
			checkBox.SetEvent(ui.__mem_func__(self.SetAutoLogin), "ON_UNCKECK", False)
			checkBox.SetCheckStatus(constInfo.AUTO_LOGIN)
			checkBox.SetTextInfo("Otomatik Login")
			checkBox.Show()
			self.autoonoffbuttonlist2.append(checkBox)

			autoattackbutton = self.GetChild("AutoAttackButton")
			autoattackbutton.SetToggleUpEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_ATTACK, 2)
			autoattackbutton.SetToggleDownEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_ATTACK, 2)
			self.autoonoffbuttonlist.append(autoattackbutton)

			autorangebutton = self.GetChild("AutoRangeButton")
			autorangebutton.SetToggleUpEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_AUTO_RANGE, 3)
			autorangebutton.SetToggleDownEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_AUTO_RANGE, 3)
			self.autoonoffbuttonlist.append(autorangebutton)

			# autopositionbutton = self.GetChild("AutoPotionButton")
			# autopositionbutton.SetToggleUpEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_POSITION, 4)
			# autopositionbutton.SetToggleDownEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_POSITION, 4)
			# self.autoonoffbuttonlist.append(autopositionbutton)

			# autoskillbutton = self.GetChild("AutoSkillButton")
			# autoskillbutton.SetToggleUpEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_SKILL, 5)
			# autoskillbutton.SetToggleDownEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_SKILL, 5)
			# self.autoonoffbuttonlist.append(autoskillbutton)

			# autoresetbutton = self.GetChild("AutoRestartHereButton")
			# autoresetbutton.SetToggleUpEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_AUTO_RESTART, 6)
			# autoresetbutton.SetToggleDownEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_AUTO_RESTART, 6)
			# self.autoonoffbuttonlist.append(autoresetbutton)

			# self.AutoSkillClearButton = self.GetChild("AutoSkillClearButton")
			# self.AutoSkillClearButton.SetEvent(ui.__mem_func__(self.AutoSkillClear))
			# self.AutoPositionClearButton = self.GetChild("AutoPotionClearButton")
			# self.AutoPositionClearButton.SetEvent(ui.__mem_func__(self.AutoPositionClear))
			# self.AutoAllClearButton = self.GetChild("AutoAllClearButton")
			# self.AutoAllClearButton.SetEvent(ui.__mem_func__(self.AutoAllClear))

			# for x in xrange(self.AUTO_COOLTIME_MAX):
				# childname = "editline" + str(x)
				# self.timeeditlist[x] = self.GetChild(childname)
				# self.timeeditlist[x].SetEscapeEvent(ui.__mem_func__(self.Close))

			# if localeInfo.IsARABIC():
				# xPos = 22+160
				# yPos = 105
				# templist = {}
				# for x in xrange(self.AUTO_COOLTIME_POS_Y):
					# for i in xrange(self.AUTO_COOLTIME_POS_X):
						# tempchildimgname = "cool_time_Image" + str(i+(x*4))
						# templist[x] = self.GetChild(tempchildimgname)
						# templist[x].SetPosition( xPos, yPos )
						# xPos -= 40
					# if x == 1:
						# yPos = yPos+27
					# xPos = 22+160
					# yPos += 70
				# templist = {}

			# self.autoslot = self.GetChild("Auto_Active_Skill_Slot_Table")
			# self.autoslot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			# self.autoslot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectActiveSkillEmptySlot))
			# self.autoslot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectActiveSkillSlot))
			# self.autoslot.SetOverInItemEvent(ui.__mem_func__(self.OverActiveSkillSlot))
			# self.autoslot.SetOverOutItemEvent(ui.__mem_func__(self.OverSkillSlotOutitem))
			# self.autoslot.Show()

			self.AutoToolTipButton = self.GetChild("AutoToolTipButton")
			self.AutoToolTip = self.__CreateGameTypeToolTip(localeInfo.AUTO_TOOLTIP_TITLE,self.AutoSystemToolTipList)
			self.AutoToolTip.SetTop()
			self.AutoToolTipButton.SetToolTipWindow(self.AutoToolTip)

		except:
			import exception
			exception.Abort("AutoWindow.__LoadWindow.UIScript/AutoWindow.py")

	def __CreateGameTypeToolTip(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		toolTip.AppendSpace(5)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def AutoSkillClear(self):
		if self.GetAutoStartonoff() == False:
			player.ClearAutoSKillSlot()
			self.RefreshAutoSkillSlot()
			for i in xrange(player.AUTO_SKILL_SLOT_MAX):
				self.autoslotindex[i] = 0

	def AutoPositionClear(self):
		if self.GetAutoStartonoff() == False:
			player.ClearAutoPositionSlot()
			self.RefreshAutoPositionSlot()
			for i in range(player.AUTO_POSITINO_SLOT_START,player.AUTO_POSITINO_SLOT_MAX):
				self.autoslotindex[i] = 0

	def AutoAllClear(self):
		if self.GetAutoStartonoff() == False:
			player.ClearAutoAllSlot()
			self.RefreshAutoSkillSlot()
			self.RefreshAutoPositionSlot()
			for i in xrange(player.AUTO_SKILL_SLOT_MAX):
				self.autoslotindex[i] = 0
			for i in range(player.AUTO_POSITINO_SLOT_START,player.AUTO_POSITINO_SLOT_MAX):
				self.autoslotindex[i] = 0

	def IsNumberic(self, text) :
		try :
			int(text)
			return True
		except ValueError :
			return False

	def CheckCooltimeText(self, cooltime):
		if cooltime == "":
			return 0
		if not self.IsNumberic(cooltime):
			return 0
		return cooltime

	def SetAutoLogin(self, checkType, autoFlag):
		if str(background.GetCurrentMapName()) == "guild_war_map3":
			return
		if not item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
			chat.AppendChat(1,"Otomatik av özelliðine sahip deðilsiniz.")
			return
		self.doAll = autoFlag
		if autoFlag == True:
			constInfo.AUTO_LOGIN = True
			chat.AppendChat(1,"<Otomatik Av> Otomatik login sistemi aktif edilmiþtir.")
		else:
			constInfo.AUTO_LOGIN = False
			chat.AppendChat(1,"<Otomatik Av> Otomatik login sistemi inaktif edilmiþtir.")

	def OnUpdate(self):
		if str(background.GetCurrentMapName()) == "guild_war_map3":
			return
		if constInfo.AUTO_HUNT_STATE == True:
			return
		if constInfo.AUTO_LOGIN == False:
			return
		if not item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
			return
		self.AutoOnOff(1, self.AUTO_ONOFF_ATTACK, 2)
		self.AutoOnOff(1, self.AUTO_ONOFF_AUTO_RANGE, 3)
		self.AutoOnOff(1, self.AUTO_ONOFF_START, 0)
		constInfo.AUTO_HUNT_STATE = True
		self.Hide()

	def AutoOnOff(self, onoff,type,number,command = False):
		if not self.isloded:
			return

		if type == self.AUTO_ONOFF_START:
			if onoff == 1:
				if player.CanStartAuto() == False:
					return
				# for i in xrange(player.AUTO_SKILL_SLOT_MAX):
					# cooltime = self.timeeditlist[i].GetText()
					# cooltime = self.CheckCooltimeText(cooltime)
					# cooltime = player.CheckSkillSlotCoolTime(i,self.autoslotindex[i],int(cooltime))
					# if self.autoslotindex[i] == 0:
						# self.timeeditlist[i].SetText("")
					# if not cooltime == 0:
						# player.SetAutoSlotCoolTime(i,int(cooltime))
						# self.timeeditlist[i].SetText(str(cooltime))

				# for i in range(player.AUTO_POSITINO_SLOT_START,player.AUTO_POSITINO_SLOT_MAX):
					# cooltime = self.timeeditlist[i-1].GetText()
					# cooltime = self.CheckCooltimeText(cooltime)
					# cooltime = player.CheckPositionSlotCoolTime(i,self.autoslotindex[i],int(cooltime))
					# if not cooltime == 0:
						# player.SetAutoSlotCoolTime(i,int(cooltime))
						# self.timeeditlist[i-1].SetText(str(cooltime))
			else:
				for i in range(player.AUTO_POSITINO_SLOT_START,player.AUTO_POSITINO_SLOT_MAX):
					self.SetAutoCooltime(i,0)

			player.AutoStartOnOff(onoff,command)
			self.autostartonoff = onoff

			self.autoonoffbuttonlist[number].Down()
			self.autoonoffbuttonlist[number].Disable()
			if onoff == 1:
				number = number+1
			else:
				number = number-1
			self.autoonoffbuttonlist[number].SetUp()
			self.autoonoffbuttonlist[number].Enable()

		elif type == self.AUTO_ONOFF_ATTACK:
			player.AutoAttackOnOff(onoff)
			if onoff:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_ONN)
			else:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_OFF)
		elif type == self.AUTO_ONOFF_SKILL:
			player.AutoSkillOnOff(onoff)
			if onoff:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_ONN)
			else:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_OFF)
		elif type == self.AUTO_ONOFF_POSITION:
			player.AutoPositionOnOff(onoff)
			if onoff:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_ONN)
			else:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_OFF)
		elif type == self.AUTO_ONOFF_AUTO_RANGE:
			player.AutoRangeOnOff(onoff)
			if onoff:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_ONN)
			else:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_OFF)
		elif type == self.AUTO_ONOFF_AUTO_RESTART:
			if onoff:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_ONN)
				net.SendChatPacket("/res_auto " + str(1))
				player.SetAutoRestart(True)
			else:
				self.autoonoffbuttonlist[number].SetText(localeInfo.AUTOHUNT_STARER_OFF)
				net.SendChatPacket("/res_auto " + str(0))
				player.SetAutoRestart(False)

		if command == True:
			if onoff == False:
				self.Close()
				return

	def LoadAutoWindow(self):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
			self.SetCenterPosition()
			# self.ReadAutoInfo()

	def Show(self):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
			self.SetCenterPosition()

		self.SetTop()
		self.ReadAutoInfo()
		self.RefreshAutoPositionSlot()
		self.RefreshAutoSkillSlot()
		self.isOpen = 1

		if not item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
			for i in range(len(self.autoonoffbuttonlist)):
				self.autoonoffbuttonlist[i].Down()
				self.autoonoffbuttonlist[i].Disable()
			player.AutoSkillOnOff(0)
			player.AutoPositionOnOff(0)
		if str(background.GetCurrentMapName()) == "guild_war_map3" or  str(background.GetCurrentMapName()) == "metin2_map_t1":
			for i in range(len(self.autoonoffbuttonlist)):
				self.autoonoffbuttonlist[i].Down()
				self.autoonoffbuttonlist[i].Disable()

		# if not chrmgr.GetAutoOnOff():
			# return
		# else:
		ui.ScriptWindow.Show(self)

	def ReadAutoInfo(self):
		if (str)(chr.GetName()) == "0":
			return

		handle = "UserData/" +chr.GetName()

		import os
		if os.path.exists(handle):
			veriTokenler = open(handle, "r").read().split()
		else:
			return

		count = len(veriTokenler) / 2
		index = 0

		if count > 0:
			for slotindex in xrange(count):
				slotID = int(str(veriTokenler[index]))
				slotCD = int(str(veriTokenler[index+1]))
				if slotID != 0:
					if slotindex < player.AUTO_SKILL_SLOT_MAX:
						player.SetAutoSkillSlotIndex(slotindex, slotID)
					else:
						player.SetAutoPositionSlotIndex(slotindex, slotID)
				player.SetAutoSlotCoolTime(slotindex, slotCD)
				index += 2

		# app.CloseTextFile(handle)
		self.isFirstReadFile = True

		self.RefreshAutoPositionSlot()
		self.RefreshAutoSkillSlot()

	# def SlotKontrol(self):
		# for i in xrange(player.AUTO_SKILL_SLOT_MAX):
			# cooltime = self.timeeditlist[i].GetText()
			# cooltime = self.CheckCooltimeText(cooltime)
			# cooltime = player.CheckSkillSlotCoolTime(i,self.autoslotindex[i],int(cooltime))
			# if self.autoslotindex[i] == 0:
				# self.timeeditlist[i].SetText("")
			# if not cooltime == 0:
				# player.SetAutoSlotCoolTime(i,int(cooltime))
				# self.timeeditlist[i].SetText(str(cooltime))
		# for i in range(player.AUTO_POSITINO_SLOT_START+1, player.AUTO_POSITINO_SLOT_MAX):
			# cooltime = self.timeeditlist[i-1].GetText()
			# cooltime = self.CheckCooltimeText(cooltime)
			# cooltime = player.CheckSkillSlotCoolTime(i,self.autoslotindex[i],int(cooltime))
			# if not cooltime == 0:
				# player.SetAutoSlotCoolTime(i,int(cooltime))
				# self.timeeditlist[i-1].SetText(str(cooltime))

	def SaveAutoInfo(self):
		if (str)(chr.GetName()) == "0":
			return
		# self.SlotKontrol()
		import os
		if os.path.exists('UserData') is False:
			os.makedirs('UserData')

		output_AutoSystemFile = pack_open('UserData/'+player.GetName(), 'w')

		for slotindex in xrange(player.AUTO_POSITINO_SLOT_MAX):
			iPos = player.GetAutoSlotIndex(slotindex)
			if iPos != 0:
				linestr = str(iPos) + '\n'
				output_AutoSystemFile.write(linestr)
				dSure = player.GetAutoSlotCoolTime(slotindex)
				if dSure != 0: 
					linestr = str(dSure) + '\n'
					output_AutoSystemFile.write(linestr)
			else:
				output_AutoSystemFile.write('0\n')
				output_AutoSystemFile.write('0\n')

		output_AutoSystemFile.close()

	def Close(self):
		self.Hide()
		self.isOpen = 0
		# self.SaveAutoInfo()
		# self.EditLineKillFocus()

	def EditLineKillFocus(self):
		for x in xrange(self.AUTO_COOLTIME_MAX):
			self.timeeditlist[x].KillFocus()

	def Destroy(self):
		self.isloded = 0
		self.Hide()
		if 0 != self.tooltipSkill:
			self.tooltipSkill.HideToolTip()

	def OnActivateSkill(self):
		return
		if self.isOpen:
			self.RefreshAutoSkillSlot()

	def OnDeactivateSkill(self, slotindex):
		return
		if self.isOpen:
			for i in xrange(player.AUTO_SKILL_SLOT_MAX):
				(Position) = player.GetAutoSlotIndex(i)
				if slotindex == Position:
					self.autoslot.DeactivateSlot(i)

	def OnUseSkill(self, slotindex, coolTime):
		if self.isOpen:
			self.RefreshAutoSkillSlot()

	def SetSkillToolTip(self, tooltip):
		self.tooltipSkill = tooltip

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def SetAutoCooltime(self, slotindex, cooltime):
		return
		self.autoslot.SetSlotCoolTime(slotindex, cooltime, 0)

	def SetCloseGame(self):
		self.closegame = True

	def GetAutoStartonoff(self):
		return self.autostartonoff

	def RefreshAutoPositionSlot(self):
		# if not self.autoslot:
			# return

		# if self.closegame:
			# return

		for slotindex in range(player.AUTO_POSITINO_SLOT_START + 1,player.AUTO_POSITINO_SLOT_MAX):
			Position = player.GetAutoSlotIndex(slotindex)
			if Position == 0:
				# self.timeeditlist[slotindex-1].SetText("")
				self.autoslotindex[slotindex] = 0
				continue

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				itemIndex = player.GetitemIndex(player.SLOT_TYPE_INVENTORY, Position)
				itemCount = player.GetitemCount(player.SLOT_TYPE_INVENTORY, Position)
			else:
				itemIndex = player.GetitemIndex(Position)
				itemCount = player.GetitemCount(Position)

			if itemCount <= 1:
				itemCount = 0

			# self.autoslot.SetItemSlot(slotindex, itemIndex, itemCount)
			self.autoslotindex[slotindex] = Position

			# coolTime = player.GetAutoSlotCoolTime(slotindex)
			# if self.timeeditlist[slotindex-1].GetText() == "":
				# self.timeeditlist[slotindex-1].SetText(str(coolTime))

			if itemIndex == 0:
				# self.autoslot.ClearSlot(slotindex)
				# self.timeeditlist[slotindex-1].SetText("")
				player.SetAutoPositionSlotIndex(slotindex, 0)
				self.RefreshAutoPositionSlot()

		# self.autoslot.RefreshSlot()

		# if self.isFirstReadFile:
			# self.SaveAutoInfo()
		# else:
			# self.ReadAutoInfo()

	def RefreshAutoSkillSlot(self):
		for slotindex in xrange(player.AUTO_SKILL_SLOT_MAX):
			Position = player.GetAutoSlotIndex(slotindex)

			if Position == 0:
				# self.autoslot.ClearSlot(slotindex)
				# self.timeeditlist[slotindex].SetText("")
				self.autoslotindex[slotindex] = 0
				continue

			skillIndex = player.GetSkillIndex(Position)
			# if 0 == skillIndex:
				# self.autoslot.ClearSlot(slotindex)

			skillType = skill.GetSkillType(skillIndex)
			if skill.SKILL_TYPE_GUILD == skillType:
				import guild
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)
			else:
				skillGrade = player.GetSkillGrade(Position)
				skillLevel = player.GetSkillLevel(Position)

			# self.autoslot.SetSkillSlotNew(slotindex, skillIndex, skillGrade, skillLevel)
			# self.autoslot.SetSlotCountNew(slotindex, skillGrade, skillLevel)
			# self.autoslot.SetCoverButton(slotindex)

			# if player.IsSkillCoolTime(Position):
				# (coolTime, elapsedTime) = player.GetSkillCoolTime(Position)
				# self.autoslot.SetSlotCoolTime(slotindex, coolTime, elapsedTime)

			# if player.IsSkillActive(Position):
				# self.autoslot.ActivateSlot(slotindex)

			self.autoslotindex[slotindex] = Position

			coolTime = player.GetAutoSlotCoolTime(slotindex)
			# if self.timeeditlist[slotindex].GetText() == "":
				# self.timeeditlist[slotindex].SetText(str(coolTime))

		# self.autoslot.RefreshSlot()

	def AddAutoSlot(self, slotindex):
		AttachedSlotType = mouseModule.mouseController.GetAttachedType()
		AttachedSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
		AttachedItemIndex = mouseModule.mouseController.GetAttacheditemIndex()

		if slotindex <= player.AUTO_SKILL_SLOT_MAX:
			if player.SLOT_TYPE_SKILL == AttachedSlotType:
				player.SetAutoSkillSlotIndex(slotindex,AttachedSlotNumber)
				self.RefreshAutoSkillSlot()
			elif player.SLOT_TYPE_AUTO == AttachedSlotType:
				if slotindex == AttachedSlotNumber:
					return
				if AttachedSlotNumber >= player.AUTO_SKILL_SLOT_MAX:
					return
				player.SetAutoSkillSlotIndex(slotindex,AttachedItemIndex)
				self.RefreshAutoSkillSlot()
		else:
			if player.SLOT_TYPE_INVENTORY == AttachedSlotType:
				itemIndex = player.GetItemIndex(AttachedSlotNumber)
				item.SelectItem(itemIndex)
				itemType		= item.GetitemType()
				itemSubType	= item.GetitemSubType()
				itemRemaintime = 0

				if itemType == item.item_TYPE_USE:
					if itemSubType == item.USE_ABILITY_UP:
						itemRemaintime = item.GetValue(1)
					elif itemSubType == item.USE_AFFECT:
						itemRemaintime = item.GetValue(3)

					if itemSubType == item.USE_POTION \
					or itemSubType == item.USE_ABILITY_UP \
					or itemSubType == item.USE_POTION_NODELAY \
					or itemSubType == item.USE_AFFECT:
						if itemRemaintime < 9999:
							player.SetAutoPositionSlotIndex(slotindex,AttachedSlotNumber)
							self.RefreshAutoPositionSlot()

				elif itemType == item.item_TYPE_BLEND:
					itemRemaintime = 600
					if itemRemaintime < 9999:
						player.SetAutoPositionSlotIndex(slotindex,AttachedSlotNumber)
						self.RefreshAutoPositionSlot()

			elif player.SLOT_TYPE_AUTO == AttachedSlotType:
				if slotindex == AttachedSlotNumber:
					return
				if AttachedSlotNumber <= player.AUTO_SKILL_SLOT_MAX:
					return
				player.SetAutoPositionSlotIndex(slotindex,AttachedItemIndex)
				self.RefreshAutoPositionSlot()

		mouseModule.mouseController.DeattachObject()

	def SelectActiveSkillEmptySlot(self, slotindex):
		if self.autostartonoff:
			return

		if True == mouseModule.mouseController.isAttached():
			self.AddAutoSlot(slotindex)

	def SelectActiveSkillSlot(self,slotindex):
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_AUTO, slotindex, self.autoslotindex[slotindex])

	def OverActiveSkillSlot(self,slotindex):
		if mouseModule.mouseController.isAttached():
			return

		if slotindex <= player.AUTO_SKILL_SLOT_MAX:
			Position = player.GetAutoSlotIndex(slotindex)
			if Position == 0:
				return
			skillIndex = player.GetSkillIndex(Position)
			skillType = skill.GetSkillType(skillIndex)
			if skill.SKILL_TYPE_GUILD == skillType:
				import guild
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)
			else:
				skillGrade = player.GetSkillGrade(Position)
				skillLevel = player.GetSkillLevel(Position)
			self.tooltipSkill.SetSkillNew(Position, skillIndex, skillGrade, skillLevel)
		else:
			Position = player.GetAutoSlotIndex(slotindex)
			# if Position == player.item_SLOT_COUNT:
				# return
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				self.tooltipItem.SetInventoryitem(Position, player.SLOT_TYPE_INVENTORY)
				self.tooltipSkill.HideToolTip()
			else:
				self.tooltipItem.SetInventoryitem(Position)
				self.tooltipSkill.HideToolTip()

	def OverSkillSlotOutitem(self):
		if 0 != self.tooltipSkill:
			self.tooltipSkill.HideToolTip()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True
