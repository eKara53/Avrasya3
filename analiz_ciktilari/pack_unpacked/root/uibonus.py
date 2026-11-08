#Made By © PMA
import ui 
import wndMgr
import player
import locale


class BonusWindow(ui.ScriptWindow):

	def __init__(self): 
		ui.ScriptWindow.__init__(self) 
		self.isLoaded = 0
		self.BonusUpdate = 0
		self.RefreshBonus()
		self.__Initialize()
		self.__LoadWindow()

	def OnUpdate(self): 
		self.BonusUpdate+=1 
		if self.BonusUpdate==25: 
			self.BonusUpdate=0 
			self.RefreshBonus()

	def __Initialize(self):
		self.tabButtonDict = None
		self.tabPvpPageButtonDict = None
		self.pageDict = None
		self.pagePvpDict = None
		self.titleBarDict = None

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			#if locale.IsARABIC() or locale.IsVIETNAM() or locale.IsJAPAN():
			#self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "bonus.py")
			#else:
			self.__LoadScript("UIScript/bonus.py")
				
			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("bonus.__LoadWindow - b³¹d ³adowania okna Bonusów") 

		self.SetState("BonusPvP")
		self.SetBonusPvPState("I")

	def __BindObject(self):

		self.tabButtonDict = {
			"BonusPvP"	: self.GetChild("Tabb_Button_01"),
			"BonusPvM"	: self.GetChild("Tabb_Button_02"),
			"Inne"		: self.GetChild("Tabb_Button_03"),
		}

		self.tabPvpPageButtonDict = {
			"I"			: self.GetChild("I_Button"),
			"II"		: self.GetChild("II_Button"),
			}

		self.pageDict = {
			"BonusPvP"	: self.GetChild("BonusPvP_Page"),
			"BonusPvM"	: self.GetChild("BonusPvM_Page"),
			"Inne"		: self.GetChild("Inne_Page"),
		}

		self.pagePvpDict = {
			"I"			: self.GetChild("I_Page"),
			"II"		: self.GetChild("II_Page"),
			}

		self.titleBarDict = {
			"BonusPvP"	: self.GetChild("BonusPvP_TitleBar"),
			"BonusPvM"	: self.GetChild("BonusPvM_TitleBar"),
			"Inne"		: self.GetChild("Inne_TitleBar"),
		}

	def __BindEvent(self):
		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

		for (tabKey1, tabPvpPageButton) in self.tabPvpPageButtonDict.items():
			tabPvpPageButton.SetEvent(ui.__mem_func__(self.__OnClickTabPvpPageButton), tabKey1)

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Hide))

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def __OnClickTabPvpPageButton(self, stateKey1):
		self.SetBonusPvPState(stateKey1)

	def SetState(self, stateKey):
		
		self.state = stateKey

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey==tabKey:
				tabButton.Down()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.Hide()

		self.titleBarDict[stateKey].Show()
		self.pageDict[stateKey].Show()

	def SetBonusPvPState(self, stateKey1):

		self.state1 = stateKey1

		for (tabKey1, tabPvpPageButton) in self.tabPvpPageButtonDict.items():
			if stateKey1==tabKey1:
				tabPvpPageButton.Down()

		for (tabKey1, tabPvpPageButton) in self.tabPvpPageButtonDict.items():
			if stateKey1!=tabKey1:
				tabPvpPageButton.SetUp()

		for pageValue in self.pagePvpDict.itervalues():
			pageValue.Hide()
			
		self.pagePvpDict[stateKey1].Show()

	def GetState(self):
		return self.state

	def GetState1(self):
		return self.state1

	def RefreshBonus(self):
		if self.isLoaded==0:
			return

		try:
			self.GetChild("OM_Value").SetText(str(self.miecze()))
			self.GetChild("ODM_Value").SetText(str(self.dwureka()))
			self.GetChild("OS_Value").SetText(str(self.sztylety()))
			self.GetChild("OD_Value").SetText(str(self.dzwony()))
			self.GetChild("OW_Value").SetText(str(self.wachlarze()))
			self.GetChild("OST_Value").SetText(str(self.strzaly()))
			self.GetChild("OMG_Value").SetText(str(self.odpmagia()))
			self.GetChild("OOG_Value").SetText(str(self.odpogien()))
			self.GetChild("OBL_Value").SetText(str(self.odpblyskawice()))
			self.GetChild("OWI_Value").SetText(str(self.odpwiatr()))
			self.GetChild("OTR_Value").SetText(str(self.odptrucie()))
			self.GetChild("OUS_Value").SetText(str(self.ustrzaly()))
			self.GetChild("BC_Value").SetText(str(self.blokciosow()))
			self.GetChild("OC_Value").SetText(str(self.odbicieciosow()))
			self.GetChild("NNO_Value").SetText(self.nnotaknie())
			self.GetChild("NNU_Value").SetText(self.nnutaknie())
			self.GetChild("NNS_Value").SetText(self.nnstaknie())
			self.GetChild("Sanex_Copyright").SetText(self.sanex())
			self.GetChild("OWOJ_Value").SetText(str(self.odpwoj()))
			self.GetChild("ONINJA_Value").SetText(str(self.odpninja()))
			self.GetChild("OSURA_Value").SetText(str(self.odpsura()))
			self.GetChild("OSZAMAN_Value").SetText(str(self.odpszaman()))
			self.GetChild("LUD_Value").SetText(str(self.ludzie()))
			self.GetChild("KRYT_Value").SetText(str(self.kryt()))
			self.GetChild("PRZESZYWA_Value").SetText(str(self.przeszywa()))
			self.GetChild("OTRUCIE_Value").SetText(str(self.otrucie()))
			self.GetChild("OMDLENIE_Value").SetText(str(self.omdlenie()))
			self.GetChild("SPOWOLNIENIE_Value").SetText(str(self.spowolnienie()))
			self.GetChild("SREDNIE_Value").SetText(str(self.srednie()))
			self.GetChild("UMKI_Value").SetText(str(self.umki()))
			self.GetChild("SZAKLECIA_Value").SetText(str(self.szaklecia()))
			self.GetChild("WA_Value").SetText(str(self.wartoscataku()))

			self.GetChild("SWOJ_Value").SetText(str(self.silnywoj()))
			self.GetChild("SNINJA_Value").SetText(str(self.silnyninja()))
			self.GetChild("SSURA_Value").SetText(str(self.silnysura()))
			self.GetChild("SSZAMAN_Value").SetText(str(self.silnyszaman()))
			
			self.GetChild("POTWORY_Value").SetText(str(self.potwory()))
			self.GetChild("DIABLY_Value").SetText(str(self.diably()))
			self.GetChild("NIEUMARLI_Value").SetText(str(self.nieumarli())) 
			self.GetChild("MISTYKI_Value").SetText(str(self.mistyki()))
			self.GetChild("ORKI_Value").SetText(str(self.orki()))
			self.GetChild("REGPZ_Value").SetText(str(self.regpz()))
			self.GetChild("REGPE_Value").SetText(str(self.regpe()))
			self.GetChild("SZBONUSDOS_Value").SetText(str(self.szbonusdos()))
			self.GetChild("SZPYANG_Value").SetText(str(self.szpyang()))
			self.GetChild("SZPP_Value").SetText(str(self.szpp()))
			self.GetChild("KRYT2_Value").SetText(str(self.kryt2()))
			self.GetChild("PRZESZYWA2_Value").SetText(str(self.przeszywa2()))
			self.GetChild("ZWIERZETA_Value").SetText(str(self.zwierzeta()))
			self.GetChild("BC2_Value").SetText(str(self.blokciosow2()))
			self.GetChild("OC2_Value").SetText(str(self.odbicieciosow2()))
			self.GetChild("OBRONA_Value").SetText(str(self.obrona()))
			self.GetChild("WIT_Value").SetText(str(self.wit()))
			self.GetChild("INT_Value").SetText(str(self.int()))
			self.GetChild("SILA_Value").SetText(str(self.sila()))
			self.GetChild("ZRE_Value").SetText(str(self.zre()))
			self.GetChild("MINPZ_Value").SetText(str(self.minpz()))
			self.GetChild("MAXPZ_Value").SetText(str(self.maxpz()))
			self.GetChild("MINPE_Value").SetText(str(self.minpe()))
			self.GetChild("MAXPE_Value").SetText(str(self.maxpe()))
			self.GetChild("MINATK_Value").SetText(str(self.minatk()))
			self.GetChild("MAXATK_Value").SetText(str(self.maxatk()))
			self.GetChild("BOBRONY_Value").SetText(str(self.bonusobrony()))
			self.GetChild("OBRONA2_Value").SetText(str(self.obrona2()))

		except:
			import exception
			exception.Abort("B³¹d odœwie¿ania bonusów.")

	def miecze(self):
		bonusid = 69
		return player.GetStatus(bonusid)

	def dwureka(self):
		bonusid = 70
		return player.GetStatus(bonusid)	

	def sztylety(self):
		bonusid = 71
		return player.GetStatus(bonusid)	

	def dzwony(self):
		bonusid = 72
		return player.GetStatus(bonusid)	

	def wachlarze(self):
		bonusid = 73
		return player.GetStatus(bonusid)	

	def strzaly(self):
		bonusid = 74
		return player.GetStatus(bonusid)

	def odpmagia(self):
		bonusid = 77
		return player.GetStatus(bonusid)

	def odpogien(self):
		bonusid = 75
		return player.GetStatus(bonusid)

	def odpblyskawice(self):
		bonusid = 76
		return player.GetStatus(bonusid)

	def odpwiatr(self):
		bonusid = 78
		return player.GetStatus(bonusid)

	def odptrucie(self):
		bonusid = 81
		return player.GetStatus(bonusid)

	def blokciosow(self):
		bonusid = 67
		return player.GetStatus(bonusid)
		
	def odbicieciosow(self):
		bonusid = 79
		return player.GetStatus(bonusid)

	def ustrzaly(self):
		bonusid = 68
		return player.GetStatus(bonusid)

	def nno(self):
		bonusid = 88
		return player.GetStatus(bonusid)

	def sanex(self):
		self.GetChild("Sanex_Copyright").SetText("Metin2 ©")

	def nnotaknie(self):
		if self.nno() >= 1:
			self.GetChild("NNO_Value").SetText("Var")
		else:
			self.GetChild("NNO_Value").SetText("Yok")

	def nns(self):
		bonusid = 89
		return player.GetStatus(bonusid)

	def nnstaknie(self):
		if self.nns() >= 1:
			self.GetChild("NNS_Value").SetText("Var")
		else:
			self.GetChild("NNS_Value").SetText("Yok")

	def nnu(self):
		bonusid = 90
		return player.GetStatus(bonusid)

	def nnutaknie(self):
		if self.nnu() >= 1:
			self.GetChild("NNU_Value").SetText("Var")
		else:
			self.GetChild("NNU_Value").SetText("Yok")

	def odpwoj(self):
		bonusid = 59
		return player.GetStatus(bonusid)

	def odpninja(self):
		bonusid = 60
		return player.GetStatus(bonusid)

	def odpsura(self):
		bonusid = 61
		return player.GetStatus(bonusid)

	def odpszaman(self):
		bonusid = 62
		return player.GetStatus(bonusid)
		
	def ludzie(self):
		bonusid = 43
		return player.GetStatus(bonusid)

	def kryt(self):
		bonusid = 40
		return player.GetStatus(bonusid)

	def przeszywa(self):
		bonusid = 41
		return player.GetStatus(bonusid)

	def otrucie(self):
		bonusid = 37
		return player.GetStatus(bonusid)

	def omdlenie(self):
		bonusid = 38
		return player.GetStatus(bonusid)
		
	def spowolnienie(self):
		bonusid = 39
		return player.GetStatus(bonusid)

	def srednie(self):
		bonusid = 122
		return player.GetStatus(bonusid)

	def umki(self):
		bonusid = 121
		return player.GetStatus(bonusid)

	def szaklecia(self):
		x = player.GetStatus(player.CASTING_SPEED)
		y = x - 100
		return y
	
	def wartoscataku(self):
		return player.GetStatus(player.ATT_BONUS)

	def silnywoj(self):
		bonusid = 54
		return player.GetStatus(bonusid)

	def silnyninja(self):
		bonusid = 55
		return player.GetStatus(bonusid)

	def silnysura(self):
		bonusid = 56
		return player.GetStatus(bonusid)

	def silnyszaman(self):
		bonusid = 57
		return player.GetStatus(bonusid)

	def potwory(self):
		bonusid = 53
		return player.GetStatus(bonusid)

	def diably(self):
		bonusid = 48
		return player.GetStatus(bonusid)

	def nieumarli(self):
		bonusid = 47
		return player.GetStatus(bonusid)

	def mistyki(self):
		bonusid = 46
		return player.GetStatus(bonusid)

	def orki(self):
		bonusid = 45
		return player.GetStatus(bonusid)

	def regpz(self):
		bonusid = 32
		return player.GetStatus(bonusid)

	def regpe(self):
		bonusid = 33
		return player.GetStatus(bonusid)

	def szbonusdos(self):
		bonusid = 83
		return player.GetStatus(bonusid)

	def szpyang(self):
		bonusid = 84
		return player.GetStatus(bonusid)

	def szpp(self):
		bonusid = 85
		return player.GetStatus(bonusid)

	def kryt2(self):
		bonusid = 40
		return player.GetStatus(bonusid)

	def przeszywa2(self):
		bonusid = 41
		return player.GetStatus(bonusid)

	def zwierzeta(self):
		bonusid = 44
		return player.GetStatus(bonusid)

	def blokciosow2(self):
		bonusid = 67
		return player.GetStatus(bonusid)

	def odbicieciosow2(self):
		bonusid = 79
		return player.GetStatus(bonusid)

	def obrona(self):
		x=player.GetStatus(player.DEF_GRADE)
		return x

#Bonusy inne
	def wit(self):
		bonusid = 13
		return player.GetStatus(bonusid)

	def int(self):
		bonusid = 15
		return player.GetStatus(bonusid)

	def sila(self):
		bonusid = 12
		return player.GetStatus(bonusid)

	def zre(self):
		bonusid = 14
		return player.GetStatus(bonusid)

	def minpz(self):
		return player.GetStatus(player.HP)

	def maxpz(self):
		return player.GetStatus(player.MAX_HP)

	def minpe(self):
		return player.GetStatus(player.SP)

	def maxpe(self):
		return player.GetStatus(player.MAX_SP)

	def minatk(self):
		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)
		return minAtk+atkBonus+attackerBonus

	def maxatk(self):
		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)
		return maxAtk+atkBonus+attackerBonus

	def bonusobrony(self):
		return player.GetStatus(player.DEF_BONUS)

	def obrona2(self):
		x=player.GetStatus(player.DEF_GRADE)
		return x

	def OnPressEscapeKey(self):
		self.Hide()
		return TRUE

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __del__(self): 
		ui.ScriptWindow.__del__(self) 
