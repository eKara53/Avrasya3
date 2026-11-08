import app
import net
import chat
import ui
import uiCommon
import player
import item

ROOT = "d:/ymir work/ui/new/horse/"

class NewHorsePanel(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load_LoadScript()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE NewHorsePanel DIALOG"

	def __Initialize(self):
		self.popup = None
		self.horse_level = 0
		self.skill_level = 0
		self.horse_name = ""
		self.hungry = 0
		self.st = 0
		self.dx = 0
		self.ht = 0
		self.iq = 0
		self.defence = 0
		self.health = 0
		self.stamina = 0
		self.grade = 0
		self.canuseskill = 0
		self.mindam = 0
		self.maxdam = 0

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY NewHorsePanel DIALOG"

	def __Load_LoadScript(self):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, "uiscript/new/horsepanel.py")
			
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.horseImage = GetObject("horse_image")
			self.horseImageTable = GetObject("horse_image2")
			self.horseHT = GetObject("Ss1_Value")
			self.horseHT.SetText(str(self.ht))
			
			self.plus1 = GetObject("Status_Plus_Label1")
			self.plus2 = GetObject("Status_Plus_Label2")
			self.plus3 = GetObject("Status_Plus_Label3")
			if self.horse_level < 11:
				self.plus2.Hide()
				self.plus3.Hide()
			if self.horse_level >= 11 and self.horse_level < 21:
				self.plus3.Hide()
			
			self.popup = uiCommon.PopupDialog()
			self.popup.Hide()
			self.CreateSlotButton()
			self.horseImage.SetEvent(self.Execute)
			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.SetCenterPosition()
		except:
			import exception
			exception.Abort("ui.NewHorsePanel.__Load_LoadScript")
	def CreateSlotButton(self):
		self.slotImage = ui.ExpandedImageBox()
		self.slotImage.SetParent(self)
		self.slotImage.LoadImage(ROOT+"item_slots_bg.jpg")
		self.slotImage.SetPosition(-65, 230)
		self.slotImage.SetWindowHorizontalAlignCenter()
		self.slotImage.Show()
		
		self.itemSlot1 = ui.GridSlotWindow()
		self.itemSlot1.SetParent(self.slotImage)
		self.itemSlot1.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlot1.SetPosition(50+7, 10)
		self.itemSlot1.Show()
		self.itemSlot2 = ui.GridSlotWindow()
		self.itemSlot2.SetParent(self.slotImage)
		self.itemSlot2.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlot2.SetPosition(50+51, 10)
		self.itemSlot2.Show()
		self.itemSlot3 = ui.GridSlotWindow()
		self.itemSlot3.SetParent(self.slotImage)
		self.itemSlot3.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlot3.SetPosition(50+95, 10)
		self.itemSlot3.Show()
		
		self.plus1.SetPosition(70,213)
		self.plus2.SetPosition(120,285)
		self.plus3.SetPosition(164,213)
	def SetInformation(self, level, skilllevel, name, hungry, st,dx,ht,iq,defence,health,stamina,grade,canuseskill,mindam,maxdam):
		self.horse_level = int(level)
		self.skill_level = int(skilllevel)
		self.horse_name = str(name)
		self.hungry = int(hungry)
		self.st = int(st)
		self.dx = int(dx)
		self.ht = int(ht)
		self.iq = int(iq)
		self.defence = int(defence)
		self.health = int(health)
		self.stamina = int(stamina)
		self.grade = int(grade)
		self.canuseskill = int(canuseskill)
		self.mindam = int(mindam)
		self.maxdam = int(maxdam)
	def Execute(self):
		self.__NotifyPopUp("At Seviyesi: %s " % str(player.GetSkillLevel(32)), None)
	def __NotifyPopUp(self, message, event):
		self.popup.SetText(str(message))
		if event != None:
			self.popup.SetAcceptEvent(event)
		self.popup.Open()
	def __OnClosePopupDialog(self):
		self.popup.Close()
		self.popup = None
	def OnPressEscapeKey(self):
		self.Close()
		return True
	
	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()