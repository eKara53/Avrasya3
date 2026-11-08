# DUMPED FROM LIVE COMPILE: uiMaintenance.py (len=1484)
import app
import exception
import wndMgr
import saimibagplinmata as ui
import localeInfo

class MaintenanceBoard(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.timeEnd = 0
		self.duration = 0

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MaintenanceWindow.py")
		except:
			exception.Abort("MaintenanceBoard.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.desc = GetObject("desc")
		except:
			exception.Abort("MaintenanceBoard.LoadDialog.BindObject")

	def Open(self, timeLeft, duration):
		self.timeEnd = app.GetTime() + timeLeft
		self.duration = duration
		self.Refresh(True)
		self.Show()

	def Close(self):
		self.Hide()
		# self.Destroy()

	def Refresh(self, new_size = False):
		self.desc.SetText(localeInfo.MAINTENANCE_DESCRIPTION % (localeInfo.SecondToDHMS(max(0, int(self.timeEnd - app.GetTime()))), localeInfo.SecondToDHMS(self.duration)))

		if new_size == True or self.desc.GetWidth() + 30 > self.GetWidth():
			self.SetSize(self.desc.GetWidth() + 30, self.GetHeight())
			self.board.SetSize(self.GetWidth(), self.GetHeight())
			self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2, self.GetTop())
			self.desc.UpdateRect()

	def OnUpdate(self):
		self.Refresh()