# DUMPED FROM LIVE COMPILE: uiHelp.py (len=5001)
import app
import ui
import localeInfo
import uiScriptLocale
import uiCommon

ENABLE_HELP_MULTIPAGE = 0

# Yardým seçim penceresi
HELP_CHOICE_TEXT = "Nasýl yardýmcý olalým?"
HELP_CHOICE_LIVE = "Canlý Destek"
HELP_CHOICE_HELP = "Yardým Ekraný"

class HelpWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "TOP_MOST")
		self.eventClose = 0
		self.dlgChoice = None
		self.eventChooseHelp = None
		self.eventChooseLive = None
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		if ENABLE_HELP_MULTIPAGE:
			self.LoadDialogMultiPage()
		else:
			self.LoadDialogSinglePage()

	def LoadDialogSinglePage(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()

			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "HelpWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/HelpWindow.py")
		except:
			import exception
			exception.Abort("HelpWindow.LoadDialogSinglePage.LoadScript")

		try:
			GetObject=self.GetChild
			self.btnClose = GetObject("close_button")
		except:
			import exception
			exception.Abort("DialogWindow.LoadDialogSinglePage.BindObject")


	def LoadDialogMultiPage(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/HelpWindow2.py")
		except:
			import exception
			exception.Abort("HelpWindow.LoadDialogMultiPage.LoadScript")

		try:
			GetObject=self.GetChild
			self.btnClose = GetObject("close_button")
			self.pages = {}
			self.btnPages = {}
			self.pages[0] = GetObject("page_1")
			self.pages[1] = GetObject("page_2")
			self.btnPages[0] = GetObject("page_1_button")
			self.btnPages[1] = GetObject("page_2_button")
			self.btnPages[0].SAFE_SetEvent(self.__OnClickPage1)
			self.btnPages[1].SAFE_SetEvent(self.__OnClickPage2)

			self.__SelectPage(0)

		except:
			import exception
			exception.Abort("DialogWindow.LoadDialogMultiPage.BindObject")

	def __OnClickPage1(self):
		self.__SelectPage(0)

	def __OnClickPage2(self):
		self.__SelectPage(1)

	def Destroy(self):
		self.eventClose = 0
		self.closeButton = 0
		self.pages = {}
		self.btnPages = {}
		if self.dlgChoice:
			self.dlgChoice.Close()
			self.dlgChoice = None
		self.eventChooseHelp = None
		self.eventChooseLive = None

	def SetCloseEvent(self, event):
		self.eventClose = event
		self.btnClose.SetEvent(event)

	# Yardim acilinca ilk gosterilen secim: 1) Canli Destek  2) Yardim Ekrani (normal yardim penceresi).
	# ESC secim penceresini yalniz kapatir (hicbir sey acilmaz).
	def OpenChooser(self, eventHelp, eventLive):
		self.eventChooseHelp = eventHelp
		self.eventChooseLive = eventLive

		if not self.dlgChoice:
			dlgChoice = uiCommon.QuestionDialog()
			dlgChoice.SetText(HELP_CHOICE_TEXT)
			# metinler 61 px'lik butona sigmaz: 88 px'lik buyuk buton gorseli
			for (button, x) in ((dlgChoice.acceptButton, -50), (dlgChoice.cancelButton, 50)):
				button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
				button.SetPosition(x, 63)
				# buton yaziyi ilk olusturuldugu (61 px) genislige gore ortalamisti: yeni genislige gore yeniden ortala
				if button.ButtonText:
					button.ButtonText.SetPosition(button.GetWidth() / 2, button.GetHeight() / 2)
			dlgChoice.SetAcceptText(HELP_CHOICE_LIVE)
			dlgChoice.SetCancelText(HELP_CHOICE_HELP)
			dlgChoice.SAFE_SetAcceptEvent(self.__OnChooseLive)
			dlgChoice.SAFE_SetCancelEvent(self.__OnChooseHelp)
			self.dlgChoice = dlgChoice

		self.dlgChoice.Open()

	def __OnChooseLive(self):
		self.dlgChoice.Close()
		if self.eventChooseLive:
			self.eventChooseLive()

	def __OnChooseHelp(self):
		self.dlgChoice.Close()
		if self.eventChooseHelp:
			self.eventChooseHelp()

	def Open(self):
		self.Lock()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def OnKeyDown(self, key):
		if app.DIK_H == key and 0 != self.eventClose:
			self.eventClose()

		return True

	def OnIMEReturn(self):
		return True

	def OnPressEscapeKey(self):
		if 0 != self.eventClose:
			self.eventClose()
		return True

	def OnPressExitKey(self):
		if 0 != self.eventClose:
			self.eventClose()
		return True

	def __SelectPage(self, pageIndex):
		for page in self.pages.values():
			page.Hide()
		for btn in self.btnPages.values():
			btn.SetUp()

		self.pages[pageIndex].Show()
		self.btnPages[pageIndex].Down()

if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	wnd = HelpWindow()
	wnd.LoadDialog()
	wnd.Open()
	app.Loop()
	wnd = None

