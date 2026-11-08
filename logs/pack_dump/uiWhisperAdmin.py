# DUMPED FROM LIVE COMPILE: uiWhisperAdmin.py (len=7547)
import ui
import dbg, app, net, ime, player

class AdminWhisperManager(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.MaxChar = 512

		self.SelectedColor = ""
		self.Colors = [
			"Normal", "Mavi", "Yesil", "Kirmizi", "Pembe"
		]
		self.ColorCodes = [
			"|h|r", "|cFF0080FF|H|h", "|cFF00FF00|H|h", "|cFFFF0000|H|h", "|cFFFF00FF|H|h"
		]

		self.SelectedReadyMadeMessage = ""
		self.ReadyMadeMessages = [
			"Mesaj1", "Mesaj2", "Mesaj3", "Mesaj4", "Mesaj5"
		]
		self.ReadyMadeMessagesContents = [
			"Bu bir hazir mesaj 1", "Bu bir hazir mesaj 2", "Bu bir hazir mesaj 3", "Bu bir hazir mesaj 4", "Bu bir hazir mesaj 5"
		]


		self.UI_Elements = { }
		self.__CreateUI()

		self.__BuildKeyDict()

	def __del__(self):
		ui.Window.__del__(self)

	def __CreateUI(self):
		self.UI_Elements["MainBoard"] = ui.BoardWithTitleBar()
		self.UI_Elements["MainBoard"].SetSize(500, 220)
		self.UI_Elements["MainBoard"].SetCenterPosition()
		self.UI_Elements["MainBoard"].AddFlag('movable')
		self.UI_Elements["MainBoard"].AddFlag('float')
		self.UI_Elements["MainBoard"].SetTitleName('Toplu mesaj paneli')
		self.UI_Elements["MainBoard"].SetCloseEvent(self.Close)
		self.UI_Elements["MainBoard"].Show()

		self.UI_Elements["Char_Counter_Text"] = ui.TextLine()
		self.UI_Elements["Char_Counter_Text"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Char_Counter_Text"].SetPosition(458, 195)
		self.UI_Elements["Char_Counter_Text"].SetText("0/%d" % (self.MaxChar))
		self.UI_Elements["Char_Counter_Text"].Show()

		self.UI_Elements["Message_Slotbar"] = ui.SlotBar()
		self.UI_Elements["Message_Slotbar"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Message_Slotbar"].SetSize(478, 90)
		self.UI_Elements["Message_Slotbar"].SetPosition(10, 35)
		self.UI_Elements["Message_Slotbar"].Show()
		
		self.UI_Elements["Message_Editline"] = ui.EditLine()
		self.UI_Elements["Message_Editline"].SetParent(self.UI_Elements["Message_Slotbar"])
		self.UI_Elements["Message_Editline"].SetSize(478, 90)
		self.UI_Elements["Message_Editline"].SetPosition(7, 3)
		self.UI_Elements["Message_Editline"].SetMax(self.MaxChar)
		self.UI_Elements["Message_Editline"].SetLimitWidth(469)
		self.UI_Elements["Message_Editline"].SetMultiLine()
		self.UI_Elements["Message_Editline"].SetText("")
		self.UI_Elements["Message_Editline"].Show()
		self.UI_Elements["Message_Editline"].OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

		self.UI_Elements["Send_Button"] = ui.Button()
		self.UI_Elements["Send_Button"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Send_Button"].SetPosition(210, 190)
		self.UI_Elements["Send_Button"].SetUpVisual('d:/ymir work/ui/public/large_button_01.sub')
		self.UI_Elements["Send_Button"].SetOverVisual('d:/ymir work/ui/public/large_button_02.sub')
		self.UI_Elements["Send_Button"].SetDownVisual('d:/ymir work/ui/public/large_button_03.sub')
		self.UI_Elements["Send_Button"].SetText("Gonder")
		self.UI_Elements["Send_Button"].SetEvent(self.__SendFunc)
		self.UI_Elements["Send_Button"].Show()

		self.UI_Elements["Clear_Button"] = ui.Button()
		self.UI_Elements["Clear_Button"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Clear_Button"].SetPosition(self.UI_Elements["MainBoard"].GetWidth() - 50, 8)
		self.UI_Elements["Clear_Button"].SetUpVisual("d:/ymir work/ui/game/guild/Refresh_Button_01.sub")
		self.UI_Elements["Clear_Button"].SetOverVisual("d:/ymir work/ui/game/guild/Refresh_Button_02.sub")
		self.UI_Elements["Clear_Button"].SetDownVisual("d:/ymir work/ui/game/guild/Refresh_Button_03.sub")
		self.UI_Elements["Clear_Button"].SetToolTipText("Temizle")
		self.UI_Elements["Clear_Button"].SetEvent(self.__RefreshFunc)
		self.UI_Elements["Clear_Button"].Show()

		for i in self.Colors:
			self.UI_Elements["Color_%s_Button" % (i)] = ui.Button()

			self.UI_Elements["Color_%s_Button" % (i)].SetParent(self.UI_Elements["MainBoard"])
			self.UI_Elements["Color_%s_Button" % (i)].SetPosition(10 + self.Colors.index(i) * 55, 135)

			self.UI_Elements["Color_%s_Button" % (i)].SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
			self.UI_Elements["Color_%s_Button" % (i)].SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
			self.UI_Elements["Color_%s_Button" % (i)].SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")

			self.UI_Elements["Color_%s_Button" % (i)].SetText(str(i))
			self.UI_Elements["Color_%s_Button" % (i)].SetEvent(lambda x = i: self.__SetColor(x))

			self.UI_Elements["Color_%s_Button" % (i)].Show()

		for i in self.ReadyMadeMessages:
			self.UI_Elements["Msg_%s_Button" % (i)] = ui.Button()

			self.UI_Elements["Msg_%s_Button" % (i)].SetParent(self.UI_Elements["MainBoard"])
			self.UI_Elements["Msg_%s_Button" % (i)].SetPosition(10 + self.ReadyMadeMessages.index(i) * 55, 160)

			self.UI_Elements["Msg_%s_Button" % (i)].SetUpVisual("d:/ymir work/ui/public/xsmall_button_01.sub")
			self.UI_Elements["Msg_%s_Button" % (i)].SetOverVisual("d:/ymir work/ui/public/xsmall_button_02.sub")
			self.UI_Elements["Msg_%s_Button" % (i)].SetDownVisual("d:/ymir work/ui/public/xsmall_button_03.sub")

			self.UI_Elements["Msg_%s_Button" % (i)].SetText(str(i))
			self.UI_Elements["Msg_%s_Button" % (i)].SetToolTipText(str( self.ReadyMadeMessagesContents[self.ReadyMadeMessages.index(i)] ))
			self.UI_Elements["Msg_%s_Button" % (i)].SetEvent(lambda x = i: self.__SetMessage(x))

			self.UI_Elements["Msg_%s_Button" % (i)].Show()
	
	# def __LoadReadyMessageFromFile(self, idx):
		# try:
			# fileName = self.ReadyMadeMessagesFiles[idx]
			# f = open(fileName, "r")
			# self.UI_Elements["Message_Editline"].SetText(str(f.read()))
			# f.close()
		# except:
			# pass

	def __SetColor(self, newColor):
		self.SelectedColor = newColor
		self.UI_Elements["Message_Editline"].SetText("%s" % (self.ColorCodes[self.Colors.index(self.SelectedColor)]))

	def __SetMessage(self, newMessage):
		self.SelectedReadyMadeMessage = newMessage
		# self.__LoadReadyMessageFromFile(self.ReadyMadeMessages.index(self.SelectedReadyMadeMessage))
		# self.UI_Elements["Message_Editline"].SetText("%s" % (self.ReadyMadeMessagesContents[self.ReadyMadeMessages.index(self.SelectedReadyMadeMessage)]))

	def __RefreshFunc(self):
		self.UI_Elements["Message_Editline"].SetText("")
		self.UI_Elements["Char_Counter_Text"].SetText("0/%d" % (self.MaxChar))

	def __SendFunc(self):
		text = self.UI_Elements["Message_Editline"].GetText()
		text = text.replace(" ", "$")

		net.SendBulkWhisperPacket(str(text))

	def __PasteFunc(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			from ui import EnablePaste
			EnablePaste(True)

			ime.PasteTextFromClipBoard()

			EnablePaste(False)

	def __BuildKeyDict(self):
		onPressKeyDict = {}
		onPressKeyDict[app.DIK_V] = lambda : self.__PasteFunc()
		self.onPressKeyDict = onPressKeyDict
	
	def OnKeyDown(self, key):
		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise
		return True

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.UI_Elements["Message_Editline"])
	
		text = self.UI_Elements["Message_Editline"].GetText()
		self.UI_Elements["Char_Counter_Text"].SetText("%d/%d" % (len(text), self.MaxChar))

	def OpenWindow(self):
		if not "[" in player.GetName():
			return

		if self.UI_Elements["MainBoard"].IsShow():
			self.UI_Elements["MainBoard"].Hide()
		else:
			self.UI_Elements["MainBoard"].Show()
	
	def Close(self):
		self.UI_Elements["MainBoard"].Hide()
	def Destroy(self):
		self.onPressKeyDict = None
		self.UI_Elements = {}

