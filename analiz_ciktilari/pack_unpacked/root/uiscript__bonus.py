#Made By ©Sanki POLAND 2013
import uiScriptLocale

SMALL_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_00.sub"
MIDDLE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
ROOT_PATH = "d:/ymir work/ui/game/windows/"
LOCALE_PATH = uiScriptLocale.WINDOWS_PATH

window = {
	"name" : "BonusWindow",
	"style" : ("movable", "float",),

	"x" : 24,
	"y" : (SCREEN_HEIGHT - 37 - 420) / 2,

	"width" : 335,
	"height" : 460,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 335,
			"height" : 460,

			"children" :
			(
				## Page Area
				{
					"name" : "Bonus_Page",
					"type" : "window",
					"style" : ("attach",),

					"x" : 0,
					"y" : 0,

					"width" : 345,
					"height" : 460,

					"children" :
					(
						## Zak³adki
						{
							"name" : "BonusPvP_Page",
							"type" : "window",
							"style" : ("attach",),

							"x" : 0,
							"y" : 0,

							"width" : 345,
							"height" : 430,

							"children" :
							(
								
								## Tytu³ zak³adki
								{
									"name" : "BonusPvP_TitleBar", "type" : "titlebar", "style" : ("attach",), "x" : 8, "y" : 7, "width" : 320, "color" : "red",
									"children" :
									(
										{ "name" : "TitleName", "type":"text", "x":0, "y":-1, "text":"Bonus Bilgisi - PvP", "all_align":"center" },
									),
								},
								##Bonusy odpornosciowe 
								{
									"name" : "I_Page",
									"type" : "window",
									"style" : ("attach",),

									"x" : 0,
									"y" : 35,

									"width" : 335,
									"height" : 395,

									"children" :
									(
										#Bonusy odpornosciowe Horizontalbar
										{ "name":"BonusPvP_Bar_01", "type":"horizontalbar", "x":12, "y":0, "width":308, },
										{ "name":"BonusPvP_Bar_01_Text", "type" : "text", "x" : 15, "y" : 1, "text" : "Savunma Bonuslarý", },
										
										#1
										{ "name":"Odpornosc_Miecze", "type":"text", "x":20, "y":20, "text":"Kýlýç Savunmasý:" },
										{
											"name":"Odpornosc_Miecze", "type":"window", "x":20, "y":35, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_Miecze_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OM_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#2
										{ "name":"Odpornosc_bron_2reczna", "type":"text", "x":20, "y":55, "text":"Çift-El Savunma:" },
										{
											"name":"Odpornosc_bron_2reczna", "type":"window", "x":20, "y":70, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_Miecze_2reczne_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"ODM_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#3
										{ "name":"Odpornosc_sztylety", "type":"text", "x":20, "y":90, "text":"Býçak Savunmasý:" },
										{
											"name":"Odpornosc_sztylety", "type":"window", "x":20, "y":105, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_sztylety_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OS_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#4
										{ "name":"Odpornosc_dzwony", "type":"text", "x":20, "y":125, "text":"Çan Savunmasý:" },
										{
											"name":"Odpornosc_dzwony", "type":"window", "x":20, "y":140, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_dzwony_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OD_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#5
										{ "name":"Odpornosc_wachlarze", "type":"text", "x":20, "y":160, "text":"Yelpaze Savunmasý:" },
										{
											"name":"Odpornosc_wachlarze", "type":"window", "x":20, "y":175, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_wachlarze_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OW_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#6
										{ "name":"Odpornosc_strzaly", "type":"text", "x":180, "y":20, "text":"Oka karþý dayanýklýlýk:" },
										{
											"name":"Odpornosc_strzaly", "type":"window", "x":180, "y":35, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_strzaly_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OST_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#7
										{ "name":"Odpornosc_magia", "type":"text", "x":180, "y":55, "text":"Büyüye karþý dayanýklýlýk:" },
										{
											"name":"Odpornosc_magia", "type":"window", "x":180, "y":70, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_magia_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OMG_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#8
										{ "name":"Odpornosc_ogien", "type":"text", "x":180, "y":90, "text":"Ateþe karþý dayanýklýlýk:" },
										{
											"name":"Odpornosc_ogien", "type":"window", "x":180, "y":105, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_ogien_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OOG_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#9
										{ "name":"Odpornosc_blyskawice", "type":"text", "x":180, "y":125, "text":"Þimþeðe karþý dayanýklýlýk:" },
										{
											"name":"Odpornosc_blyskawice", "type":"window", "x":180, "y":140, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_blyskawice_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OBL_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#10
										{ "name":"Odpornosc_wiatr", "type":"text", "x":180, "y":160, "text":"Rüzgar dayanýklýlýðý:" },
										{
											"name":"Odpornosc_wiatr", "type":"window", "x":180, "y":175, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_wiatr_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OWI_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#Bonusy Odpornoœciowe ogólne
										{ "name":"BonusPvP_Bar_02", "type":"horizontalbar", "x":12, "y":200, "width":151, },
										{ "name":"BonusPvP_Bar_02_Text", "type" : "text", "x" : 15, "y" : 201, "text" : "Diðer savunmalar", },
										{ "name":"BonusPvP_Bar_02", "type":"horizontalbar", "x":168, "y":200, "width":154, },
										{ "name":"BonusPvP_Bar_03_Text", "type" : "text", "x" : 174, "y" : 201, "text" : "Karakter savunmalarý", },
										#1
										{ "name":"Odpornosc_trucizna", "type":"text", "x":20, "y":220, "text":"Zehre karþý koyma:" },
										{
											"name":"Odpornosc_trucizna", "type":"window", "x":20, "y":235, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_trucizna_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OTR_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#2
										{ "name":"Blok_ciosu", "type":"text", "x":20, "y":255, "text":"Yakýn dövüþ bloklama þansý:" },
										{
											"name":"Blok_ciosu", "type":"window", "x":20, "y":270, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Blok_ciosu_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"BC_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#3
										{ "name":"Odbicie_ciosu", "type":"text", "x":20, "y":290, "text":"Yakýn dövüþ yansýtma þansý:" },
										{
											"name":"Odbicie_ciosu", "type":"window", "x":20, "y":305, "width":50, "height":20, 
											"children" :
											(
												{ "name":"odbicie_ciosow_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OC_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#4
										{ "name":"Szansa_na_unikniecie_strzaly", "type":"text", "x":20, "y":325, "text":"Oklardan korunma þansý:" },
										{
											"name":"Szansa_na_unikniecie_strzaly", "type":"window", "x":20, "y":340, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Szan_ustrzaly_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OUS_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#6
										{ "name":"Odpornosc_woj", "type":"text", "x":180, "y":220, "text":"Savaþçýlara karþý savunma:" },
										{
											"name":"Odpornosc_woj", "type":"window", "x":180, "y":235, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_woj_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OWOJ_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#7
										{ "name":"Odpornosc_ninja", "type":"text", "x":180, "y":255, "text":"Ninjalara karþý savunma:" },
										{
											"name":"Odpornosc_ninja", "type":"window", "x":180, "y":270, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_ninja_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"ONINJA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#8
										{ "name":"Odpornosc_sura", "type":"text", "x":180, "y":290, "text":"Suralara karþý savunma:" },
										{
											"name":"Odpornosc_sura", "type":"window", "x":180, "y":305, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_sura_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OSURA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#9
										{ "name":"Odpornosc_szaman", "type":"text", "x":180, "y":325, "text":"Þamanlara karþý savunma:" },
										{
											"name":"Odpornosc_szaman", "type":"window", "x":180, "y":340, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Odp_szaman_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OSZAMAN_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
									),
								},
								#Bonusy Atakuj¹ce
								{
									"name" : "II_Page",
									"type" : "window",
									"style" : ("attach",),

									"x" : 0,
									"y" : 35,

									"width" : 335,
									"height" : 395,

									"children" :
									(
										#Bonusy atakuj¹ce Horizontalbar
										{ "name":"BonusPvP_Bar_04", "type":"horizontalbar", "x":12, "y":0, "width":308, },
										{ "name":"BonusPvP_Bar_04_Text", "type" : "text", "x" : 15, "y" : 1, "text" : "Saldýrý Bonuslarý", },
										#1
										{ "name":"Silny_ludzie", "type":"text", "x":20, "y":20, "text":"Yarý insanlara karþý güçlü:" },
										{
											"name":"Silny_ludzie", "type":"window", "x":20, "y":35, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Silny_ludzie_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"LUD_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#2
										{ "name":"Krytyk", "type":"text", "x":20, "y":55, "text":"Kritik Vuruþ Þansý:" },
										{
											"name":"Krytyk", "type":"window", "x":20, "y":70, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Krytyk_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"KRYT_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#3
										{ "name":"Przeszywa", "type":"text", "x":20, "y":90, "text":"Delici Vuruþ için þans:" },
										{
											"name":"Przeszywa", "type":"window", "x":20, "y":105, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Przeszywa_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"PRZESZYWA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#4
										{ "name":"Otrucie", "type":"text", "x":20, "y":125, "text":"Zehirleme þansý:" },
										{
											"name":"Otrucie", "type":"window", "x":20, "y":140, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Otrucie_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OTRUCIE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#5
										{ "name":"Omdlenie", "type":"text", "x":20, "y":160, "text":"Sersemleme þansý:" },
										{
											"name":"Omdlenie", "type":"window", "x":20, "y":175, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Omdlenie_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"OMDLENIE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#6
										{ "name":"Spowolnienie", "type":"text", "x":180, "y":20, "text":"Yavaþlama þansý:" },
										{
											"name":"Spowolnienie", "type":"window", "x":180, "y":35, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Spowolnienie_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SPOWOLNIENIE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#7
										{ "name":"Srednie", "type":"text", "x":180, "y":55, "text":"ŒOrtalama Zarar:" },
										{
											"name":"Srednie", "type":"window", "x":180, "y":70, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Srednie_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SREDNIE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#8
										{ "name":"Umki", "type":"text", "x":180, "y":90, "text":"Beceri Hasarý:" },
										{
											"name":"Umki", "type":"window", "x":180, "y":105, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Umki_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"UMKI_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#9
										{ "name":"Szybkosc_zaklecia", "type":"text", "x":180, "y":125,  "text":"Büyü Hýzý:" },
										{
											"name":"Szybkosc_zaklecia", "type":"window", "x":180, "y":140, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Szybkosc_zaklecia_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SZAKLECIA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#10
										{ "name":"Wartosc_ataku", "type":"text", "x":180, "y":160, "text":"Saldýrý Deðeri:" },
										{
											"name":"Wartosc_ataku", "type":"window", "x":180, "y":175, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Wartosc_ataku_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"WA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#Niewrazliwki
										{ "name":"BonusPvP_Bar_05", "type":"horizontalbar", "x":12, "y":200, "width":151, },
										{ "name":"BonusPvP_Bar_05_Text", "type" : "text", "x" : 15, "y" : 201, "text" : "Baðýþýklýlýk", },
										#1
										{ "name":"NNO", "type":"text", "x":20, "y":220, "text":"Sersemlik karþýsýnda baðýþýklýlýk:" },
										{
											"name":"NNO", "type":"window", "x":20, "y":235, "width":50, "height":20, 
											"children" :
											(
												{ "name":"NNO_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"NNO_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#2
										{ "name":"NNU", "type":"text", "x":20, "y":255, "text":"Düþme karþýsýnda baðýþýklýlýk:" },
										{
											"name":"NNU", "type":"window", "x":20, "y":270, "width":50, "height":20, 
											"children" :
											(
												{ "name":"NNU_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"NNU_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#3
										{ "name":"NNS", "type":"text", "x":20, "y":290, "text":"Yavaþlama karþýsýnda baðýþýklýlýk:" },
										{
											"name":"NNS", "type":"window", "x":20, "y":305, "width":50, "height":20, 
											"children" :
											(
												{ "name":"NNS_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"NNS_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#Silny na klasy 
										{ "name":"BonusPvP_Bar_06", "type":"horizontalbar", "x":168, "y":200, "width":154, },
										{ "name":"BonusPvP_Bar_06_Text", "type" : "text", "x" : 174, "y" : 201, "text" : "Karakter saldýrýlarý", },
										#6
										{ "name":"Silny_woj", "type":"text", "x":180, "y":220, "text":"Savaþçýlara karþý güçlü:" },
										{
											"name":"Silny_woj", "type":"window", "x":180, "y":235, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Silny_woj_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SWOJ_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#7
										{ "name":"Silny_ninja", "type":"text", "x":180, "y":255, "text":"Ninjalara karþý güçlü:" },
										{
											"name":"Silny_ninja", "type":"window", "x":180, "y":270, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Silny_ninja_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SNINJA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#8
										{ "name":"Silny_sura", "type":"text", "x":180, "y":290, "text":"Suralara karþý güçlü:" },
										{
											"name":"Silny_sura", "type":"window", "x":180, "y":305, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Silny_sura_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SSURA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
										#9
										{ "name":"Silny_szaman", "type":"text", "x":180, "y":325, "text":"Þamanlara karþý güçlü:" },
										{
											"name":"Silny_szaman", "type":"window", "x":180, "y":340, "width":50, "height":20, 
											"children" :
											(
												{ "name":"Silny_szaman_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
												{ "name":"SSZAMAN_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											)
										},
									),
								},
										
								#Przyciski
								{
									"name" : "I_Button",
									"type" : "radio_button",

									"x" : 75,
									"y" : 400,

									"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
									"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
									"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
									"children" :
									(
										{
											"name" : "I_Button_Print",
											"type" : "text",

												"x" : 0,
												"y" : 0,

												"all_align" : "center",

												"text" : "I",
										},
									),
								},
								{
									"name" : "II_Button",
									"type" : "radio_button",

									"x" : 185,
									"y" : 400,

									"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
									"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
									"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

									"children" :
									(
										{
											"name" : "II_Button_Print",
											"type" : "text",

											"x" : 0,
											"y" : 0,

											"all_align" : "center",

											"text" : "II",
										},
									),
								},
							),
						},
						{
							"name" : "BonusPvM_Page",
							"type" : "window",
							"style" : ("attach",),

							"x" : 0,
							"y" : 0,

							"width" : 335,
							"height" : 430,

							"children" :
							(
								{
									"name" : "BonusPvM_TitleBar",
									"type" : "titlebar",
									"style" : ("attach",),

									"x" : 8,
									"y" : 7,

									"width" : 320,
									"color" : "red",

									"children" :
									(
										{ "name":"TitleName", "type":"text", "x":0, "y":-1, "text":"Bonus Bilgisi - PvM", "all_align":"center" },
									),
								},
								#Bonusy PvM Horizontalbar
								{ "name":"BonusPvM_Bar_01", "type":"horizontalbar", "x":12, "y":35, "width":308, },
								{ "name":"BonusPvM_Bar_01_Text", "type" : "text", "x" : 15, "y": 36, "text" : "Saldýrý bonuslarý", },
								#1
								{ "name":"Silny_potwory", "type":"text", "x":20, "y":55, "text":"Canavarlara karþý güçlü:" },
								{
									"name":"Silny_potwory", "type":"window", "x":20, "y":70, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Silny_potwory_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"POTWORY_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#2
								{ "name":"Diably", "type":"text", "x":20, "y":90, "text":"Þeytanlara karþý güçlü:" },
								{
									"name":"Diably", "type":"window", "x":20, "y":105, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Diably_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"DIABLY_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#3
								{ "name":"Nieumarli", "type":"text", "x":20, "y":125, "text":"Ölümsüzlere karþý güçlü:" },
								{
									"name":"Nieumarli", "type":"window", "x":20, "y":140, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Nieumarli_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"NIEUMARLI_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#4
								{ "name":"Mistyki", "type":"text", "x":20, "y":160, "text":"Mistiklere karþý güçlü:" },
								{
									"name":"Mistyki", "type":"window", "x":20, "y":175, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Mistyki_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MISTYKI_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#5
								{ "name":"Orki", "type":"text", "x":20, "y":195, "text":"Orklara karþý güçlü:" },
								{
									"name":"Orki", "type":"window", "x":20, "y":210, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Orki_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"ORKI_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#6
								{ "name":"REGPZ", "type":"text", "x":180, "y":55, "text":"HP Üretimi:" },
								{
									"name":"REGPZ", "type":"window", "x":180, "y":70, "width":50, "height":20, 
									"children" :
									(
										{ "name":"REGPZ_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"REGPZ_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#7
								{ "name":"REGPE", "type":"text", "x":180, "y":90, "text":"SP Üretimi:" },
								{
									"name":"REGPE", "type":"window", "x":180, "y":105, "width":50, "height":20, 
									"children" :
									(
										{ "name":"REGPE_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"REGPE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#8
								{ "name":"Szansa_Bonus_Dos", "type":"text", "x":180, "y":125, "text":"EXP Bonus þansý:" },
								{
									"name":"Szansa_Bonus_Dos", "type":"window", "x":180, "y":140, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Szansa_Bonus_Dos", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"SZBONUSDOS_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#9
								{ "name":"Szansa_podwojna_YANG", "type":"text", "x":180, "y":160, "text":"Yang düþürme þansý:" },
								{
									"name":"Szansa_podwojna_YANG", "type":"window", "x":180, "y":175, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Szansa_podwojna_YANG_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"SZPYANG_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									),
								},
								#10
								{ "name":"Szansa_podwojne_przedmioty", "type":"text", "x":180, "y":195, "text":"Eþya düþürme þansý:" },
								{
									"name":"Szansa_podwojne_przedmioty", "type":"window", "x":180, "y":210, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Szansa_podwojne_przedmioty_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"SZPP_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#Bonusy PvM ogolne
								{ "name":"BonusPvM_Bar_02", "type":"horizontalbar", "x":12, "y":235, "width":151, },
								{ "name":"BonusPvM_Bar_02_Text", "type" : "text", "x" : 15, "y" : 236, "text" : "Genel:", },
								#1
								{ "name":"Krytyk", "type":"text", "x":20, "y":255, "text":"Kritik vuruþ þansý:" },
								{
									"name":"Krytyk", "type":"window", "x":20, "y":270, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Krytyk_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"KRYT2_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#2
								{ "name":"Przeszywa", "type":"text", "x":20, "y":290, "text":"Delici Vuruþ için þans:" },
								{
									"name":"Przeszywa", "type":"window", "x":20, "y":305, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Przeszywa_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"PRZESZYWA2_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#3
								{ "name":"Zwierzeta", "type":"text", "x":20, "y":325, "text":"Hayvanlara karþý güçlü:" },
								{
									"name":"Zwierzeta", "type":"window", "x":20, "y":340, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Zwierzeta_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"ZWIERZETA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#4
								#5
								#Obronne PvM 
								{ "name":"BonusPvM_Bar_03", "type":"horizontalbar", "x":168, "y":235, "width":154, },
								{ "name":"BonusPvM_Bar_03_Text", "type" : "text", "x" : 174, "y" : 236, "text" : "Savunma bonuslarý", },
								#6
								{ "name":"Blok_ciosu", "type":"text", "x":180, "y":255, "text":"Yakýn dövüþ bloklama þansý:" },
								{
									"name":"Blok_ciosu", "type":"window", "x":180, "y":270, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Blok_ciosow", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"BC2_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#7
								{ "name":"Odbicie_ciosu", "type":"text", "x":180, "y":290, "text":"Yakýn dövüþ yansýtma þansý:" },
								{
									"name":"Odbicie_ciosu", "type":"window", "x":180, "y":305, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Odbicie_ciosow_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"OC2_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#8
								{ "name":"Obrona", "type":"text", "x":180, "y":325, "text":"Savunma:" },
								{
									"name":"Obrona", "type":"window", "x":180, "y":340, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Obrona_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"OBRONA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
							),
						},
						{
							"name" : "Inne_Page",
							"type" : "window",
							"style" : ("attach",),

							"x" : 0,
							"y" : 0,

							"width" : 335,
							"height" : 430,

							"children" :
							(
								{
									"name" : "Inne_TitleBar",
									"type" : "titlebar",
									"style" : ("attach",),

									"x" : 8,
									"y" : 7,

									"width" : 320,
									"color" : "red",

									"children" :
									(
										{ "name":"TitleName", "type":"text", "x":0, "y":-1, "text":"Diðer Bonuslar", "all_align":"center" },
										
									),
								},
								#Inne Bonusy Horizontalbar
								{ "name":"Inne_Bar_01", "type":"horizontalbar", "x":12, "y":35, "width":308, },
								{ "name":"Inne_Bar_01_Text", "type" : "text", "x" : 15, "y" : 36, "text" : "Diðer bonuslar", },
								#1
								{ "name":"Wit", "type":"text", "x":40, "y":55, "text":"Canlýlýk:" },
								{
									"name":"Wit", "type":"window", "x":40, "y":70, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Wit", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"WIT_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#2
								{ "name":"Int", "type":"text", "x":40, "y":90, "text":"Zeka:" },
								{
									"name":"Int", "type":"window", "x":40, "y":105, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Int_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"INT_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#3
								{ "name":"Sil", "type":"text", "x":40, "y":125, "text":"Güç:" },
								{
									"name":"Sil", "type":"window", "x":40, "y":140, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Sil_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"SILA_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#4
								{ "name":"Zre", "type":"text", "x":40, "y":160, "text":"Çeviklik:" },
								{
									"name":"Zre", "type":"window", "x":40, "y":175, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Zre_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"ZRE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#6
								{ "name":"MINPZ", "type":"text", "x":140, "y":55, "text":"Mevcut HP:" },
								{
									"name":"MINPZ", "type":"window", "x":140, "y":70, "width":50, "height":20, 
									"children" :
									(
										{ "name":"MINPZ_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MINPZ_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#7
								{ "name":"MINPE", "type":"text", "x":140, "y":90, "text":"Mevcut SP:" },
								{
									"name":"MINPE", "type":"window", "x":140, "y":105, "width":50, "height":20, 
									"children" :
									(
										{ "name":"MINPE_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MINPE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#8
								{ "name":"MINATK", "type":"text", "x":140, "y":125, "text":"Min. atak:" },
								{
									"name":"MINATK", "type":"window", "x":140, "y":140, "width":50, "height":20, 
									"children" :
									(
										{ "name":"MINATK_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MINATK_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#9
								{ "name":"BonusObrony", "type":"text", "x":140, "y":160, "text":"Bonus savunma:" },
								{
									"name":"BonusObrony", "type":"window", "x":140, "y":175, "width":50, "height":20, 
									"children" :
									(
										{ "name":"BonusObrony_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"BOBRONY_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#10
								{ "name":"MAXPZ", "type":"text", "x":240, "y":55, "text":"Max HP:" },
								{
									"name":"MAXPZ", "type":"window", "x":240, "y":70, "width":50, "height":20, 
									"children" :
									(
										{ "name":"MAXPZ_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MAXPZ_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#11
								{ "name":"MAXPE", "type":"text", "x":240, "y":90, "text":"Max SP:" },
								{
									"name":"MAXPE", "type":"window", "x":240, "y":105, "width":50, "height":20, 
									"children" :
									(
										{ "name":"MAXPE_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MAXPE_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#12
								{ "name":"MAXATK", "type":"text", "x":240, "y":125, "text":"Max. atak:" },
								{
									"name":"MAXATK", "type":"window", "x":240, "y":140, "width":50, "height":20, 
									"children" :
									(
										{ "name":"MAXATK_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"MAXATK_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
								#13
								{ "name":"Obrona", "type":"text", "x":240, "y":160, "text":"Toplam savunma:" },
								{
									"name":"Obrona", "type":"window", "x":240, "y":175, "width":50, "height":20, 
									"children" :
									(
										{ "name":"Obrona_Miejsce", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
										{ "name":"OBRONA2_Value", "type":"text", "x":26, "y":3, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
									)
								},
							),
						},
						## RadioButton
						{
							"name" : "Tabb_Button_01",
							"type" : "radio_button",

							"x" : 20,
							"y" : 430,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
							"children" :
							(
								{
									"name" : "Bonus_Tab_01_Print",
									"type" : "text",

										"x" : 0,
										"y" : 0,

										"all_align" : "center",

										"text" : "PvP",
								},
							),
						},
						{
							"name" : "Tabb_Button_02",
							"type" : "radio_button",

							"x" : 128,
							"y" : 430,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

							"children" :
							(
								{
									"name" : "Bonus_Tab_02_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "PvM",
								},
							),
						},
						{
							"name" : "Tabb_Button_03",
							"type" : "radio_button",

							"x" : 235,
							"y" : 430,

							"width" : 76,
							"height" : 17,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",

							"children" :
							(
								{
									"name" : "Bonus_Tab_03_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "Diðer",
								},
							),
						},
					{ "name":"Sanex_Copyright", "type":"text", "x":280, "y":36, "text":"", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
					),
				},
			),
		},
	),
}