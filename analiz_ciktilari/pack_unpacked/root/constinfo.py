import app
import chrmgr
import item
import net
import player

CLIENT_YOL = "lib/"
CONFIG_YOL = "locale/tr/ui/config/"

CHAT_TEXT_HOVER = False
CHAT_TEXT_HOVER_PLACEHOLDER = False

SVSIDE_ONLINE = True

# OFFLINE_SHOPS
shop_cost=[]
gift_items={}
MyShops=[]
SHOPNAMES_RANGE = 5000

channelidx=0
COSTUME_SYSTEM = False
TIKTOK_PANEL = False
if TIKTOK_PANEL:
	CACHED_SEC = 30
	tiktok_tikmer = 0
	cache_duration = 0
	cached_time = None
	TIKTOK_DATA = []
SOUNDSVOL = 0

fiveminutes_notice = True
textInfoToGame = [
	"Hesap güvenliðiniz için ücretsiz olarak sunulan güvenli bilgisayar ve eþya kilitleme sistemini aktif ediniz.",
	"TL ile eþya ve yang satmak yasaktýr.",
	"Oyun içi baðýrma kanalý üzerinden legalden eþya veya yang satýþýna yönelik ilan vermek yasaktýr."
]
notice_timer = 0

if app.ENABLE_SECURITY_COMPUTER_REDVEGAS:
	SECURE_PC = False

if app.ENABLE_SPECIAL_MISSION_SYSTEM:
	LVL_MISSION_DATA = []

if app.ENABLE_TARGET_INFORMATION_SYSTEM:
	MONSTER_INFO_DATA = {}

if app.ENABLE_ITEM_DELETE_SYSTEM:
	silme = 0
	ITEM_DELETE_LIST = {}

if app.ENABLE_AUTO_SYSTEM:
	AUTO_LOGIN = False
	AUTO_HUNT_STATE = False
	CMD_FIRST = False
	AUTO_HUNT_RELOAD_LOGIN_TIMER = 120
	AUTO_LAST_SLOT = 0
	TRY_CONNECT_COUNT = 0
	REQUEST_STATE = False
	AUTO_LOGIN_ID = ""
	AUTO_LOGIN_PW = ""

if app.ENABLE_ITEM_SHOP_SYSTEM:
	ITEM_DATA = {}
	ITEM_SEARCH_DATA = []
	LAST_CATEG_ID = 0
	LAST_SUBCATEG_ID = 0
	NEW_MARKET = 1
else:
	NEW_MARKET = 0

AUTO_CHAT = 0
AUTO_CHAT_INFO = 0
LAST_CHAT_MESSAGE = ""
LAST_CHAT_MESSAGE_TRADE = ""
chat_wait_because_teleport = 0
wait_chat_auto = 0
wait_chat_auto2 = 0
AUTO_CHAT_CLOSE_REASON_WARP = 0

if app.ENABLE_NEW_FONT_CHANGER:
	import systemSetting
	OPTION_FONT = int(systemSetting.GetFontMode())
	UI_DEF_FONT = "Tahoma:12"
	UI_DEF_FONT_LARGE = "Tahoma:14"
	UI_DEF_FONT_SMALL = "Tahoma:9"

	UI_OLD_DEF_FONT = "Arial:12"
	UI_OLD_DEF_FONT_LARGE = "Arial:14"
	UI_OLD_DEF_FONT_SMALL = "Arial:9"

# NEW BEGIN
ENABLE_SIMYA_SYSTEM = False
LastBuyItemPrice = 0
SatinAlOkey = 0
MINIMAP_DATE_SYSTEM = True
# NEW END

# EXTRA BEGIN
ENABLE_NEW_LEVELSKILL_SYSTEM = False # loads 5 (B,M,G,P,F) skills .mse
ENABLE_RANDOM_CHANNEL_SEL = False # don't set a random channel when you open the client
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = False # don't remove id and password if the login attempt fails
ENABLE_PASTE_FEATURE = True # ctrl+v will now work
ENABLE_FULLSTONE_DETAILS = True # display all the bonuses added by a stone instead of the first one
ENABLE_REFINE_PCT = False # enable successfulness % in the refine dialog
EXTRA_UI_FEATURE = True # enable extra ui features
NEW_678TH_SKILL_ENABLE = False # load 6th warrior / ninja skills (instead of app.NEW_678TH_SKILL_ENABLE)
SELECT_CHAR_NO_DELAY = 0.5 # change the 3sec delay while choosing a character in the select phase
ENABLE_ACTIVE_PET_SEAL_EFFECT = True # enable active effect on pet seals
# EXTRA END

if app.ENABLE_OFFLINESHOP_SYSTEM:
	SHOPNAMES_RANGE = 2500
	MAX_SHOP_TYPE = 13
	MAX_SHOP_TITLE = 6
	def NumberToString(n) :
		if n <= 0 :
			return "0"
		return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

	_interface_instance = None
	def GetInterfaceInstance():
		global _interface_instance
		return _interface_instance
	def SetInterfaceInstance(instance):
		global _interface_instance
		if _interface_instance:
			del _interface_instance
		_interface_instance = instance

	_game_instance = None
	def GetGameInstance():
		global _game_instance
		return _game_instance
	def SetGameInstance(instance):
		global _game_instance
		if _game_instance:
			del _game_instance
		_game_instance = instance
	
	def IS_SET(value, flag):
		return (value & flag) == flag
	def SET_BIT(value, bit):
		return value | (bit)
	def REMOVE_BIT(value, bit):
		return value & ~(bit)
	def getFlagValue(value):
		return 1 << value
	
	def getInjectCheck(text):
		words = ["SELECT", "TRUNCATE", "INSERT", "REPLACE", "DELETE", "ALTER", "DROP",";", ":", "*", "'", '"', "="]
		characters = []
		for word in words:
			if text.find(word) != -1:
				return True
		return False

if MINIMAP_DATE_SYSTEM == True:
	def GetTimeDate():
		import time
		gc=time.strftime("%d")
		aycek=time.strftime("%B")
		yilx=time.strftime("%Y")
		gun=time.strftime("%A")
		b= " "

		aylar={"January":"Ocak","February":"Sub","March":"Mart","April":"Nis","May":"May","June":"Haz","July":"Tem","August":"Agus","September":"Eylul","October":"Ekim","November":"Kasim","December":"Aralik"}
		ayx=aylar[aycek]

		gunler={"Monday":"Ptesi","Tuesday":"Sali","Wednesday":"Cars","Thursday":"Per","Friday":"Cuma","Saturday":"Ctesi","Sunday":"Paz"}
		g=gunler[gun]
		baglad=gc+b+ayx+b+yilx+b+g+b
		return baglad

if app.__ENABLE_NEW_OFFLINESHOP__:
	import re
	def ConvertMoneyText(text, powers = dict(k = 10**3, m = 10**6, b = 10**9)):
		match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
		if match:
			moneyValue, suffixName = match.groups()
			moneyValue = int(moneyValue)
			if not suffixName:
				return moneyValue

			return moneyValue * (powers[suffixName[0]] ** len(suffixName))

		return 0

# enable save account
ENABLE_TWO_SERVER_SELECT = False
ENABLE_SAVE_ACCOUNT = True
if ENABLE_SAVE_ACCOUNT:
	class SAB:
		ST_CACHE, ST_FILE, ST_REGISTRY = xrange(3)
		slotCount = 5
		storeType = ST_REGISTRY # 0 cache, 1 file, 2 registry
		btnName = {
			"Save": "SaveAccountButton_Save_%02d",
			"Access": "SaveAccountButton_Access_%02d",
			"Remove": "SaveAccountButton_Remove_%02d",
		}
		accData = {}
		if ENABLE_TWO_SERVER_SELECT:
			regPathKale = r"SOFTWARE\Kuzey2"
			regPathFetih = r"SOFTWARE\Fetih"
			regPath = regPathKale
			activeServerType = "KALE"
		else:
			regPath = r"SOFTWARE\Avrasya2"
		regName = "slot%02d_%s"
		regValueId = "id"
		regValuePwd = "pwd"
		fileExt = ".do.not.share.it.txt"
if ENABLE_TWO_SERVER_SELECT:
	def SAB_SetServerType(serverType):
		if not ENABLE_SAVE_ACCOUNT:
			return

		if serverType == "FETIH":
			SAB.activeServerType = "FETIH"
			SAB.regPath = SAB.regPathFetih
		else:
			SAB.activeServerType = "KALE"
			SAB.regPath = SAB.regPathKale

		SAB.accData = {}


	def SAB_GetServerTypeByServerID(serverID):
		if int(serverID) == 2:
			return "FETIH"

		return "KALE"
def CreateSABDataFolder(filePath):
	import os
	folderPath = os.path.split(filePath)[0]
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)
def IsExistSABDataFile(filePath):
	import os
	return os.path.exists(filePath)
def GetSABDataFile(idx):
	import os
	filePath = "%s\\Kuzey2\\" % os.getenv('appdata')
	filePath += SAB.regName % (idx, SAB.regValueId)
	filePath += SAB.fileExt
	return filePath
def DelJsonSABData(idx):
	import os
	filePath = GetSABDataFile(idx)
	if IsExistSABDataFile(filePath):
		os.remove(filePath)
def GetJsonSABData(idx):
	(id, pwd) = ("", "")
	filePath = GetSABDataFile(idx)
	if not IsExistSABDataFile(filePath):
		return (id, pwd)
	with old_open(filePath) as data_file:
		try:
			import json
			(id, pwd) = json.load(data_file)
			id = str(id) # unicode to ascii
			pwd = str(pwd) # unicode to ascii
		except ValueError:
			pass
	return (id, pwd)
def SetJsonSABData(idx, slotData):
	filePath = GetSABDataFile(idx)
	CreateSABDataFolder(filePath)
	with old_open(filePath, "w") as data_file:
		import json
		json.dump(slotData, data_file)
def DelWinRegKeyValue(keyPath, keyName):
	try:
		import _winreg
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyPath)
		_tmpKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyPath, 0, _winreg.KEY_WRITE)
		_winreg.DeleteValue(_tmpKey, keyName)
		_winreg.CloseKey(_tmpKey)
		return True
	except WindowsError:
		return False
def GetWinRegKeyValue(keyPath, keyName):
	try:
		import _winreg
		_tmpKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyPath, 0, _winreg.KEY_READ)
		keyValue, keyType = _winreg.QueryValueEx(_tmpKey, keyName)
		_winreg.CloseKey(_tmpKey)
		return str(keyValue) # unicode to ascii
	except WindowsError:
		return None
def SetWinRegKeyValue(keyPath, keyName, keyValue):
	try:
		import _winreg
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyPath)
		_tmpKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyPath, 0, _winreg.KEY_WRITE)
		_winreg.SetValueEx(_tmpKey, keyName, 0, _winreg.REG_SZ, keyValue)
		_winreg.CloseKey(_tmpKey)
		return True
	except WindowsError:
		return False

# classic minmax def
def minmax(tmin, tmid, tmax):
	if tmid < tmin:
		return tmin
	elif tmid > tmax:
		return tmax
	return tmid
# EXTRA END

# TRADE_GOLD_WITH_THOUSANDS_SEPARATORS BEGIN
def intWithCommas(x, commasign='.'):
	# alternative of
	# return '{0:,}'.format(x).replace(',', commasign)
	if type(x) not in [type(0), type(0L)]:
		raise TypeError("Parameter must be an integer.")
	if x < 0:
		return '-' + intWithCommas(-x, commasign)
	result = ''
	while x >= 1000:
		x, r = divmod(x, 1000)
		result = "%s%03d%s" % (commasign, r, result)
	return "%d%s" % (x, result)
# TRADE_GOLD_WITH_THOUSANDS_SEPARATORS END

def Emoji(path):
	return "|E{}|e".format(path)

def Color(hexString):
	return "|cff{}|h".format(hexString)

def TextColor(text, hexString):
	return "|cff{}|h{}|r".format(hexString, text)

# option
IN_GAME_SHOP_ENABLE = 1
CONSOLE_ENABLE = 0

PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 15

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

# constant
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1

isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639]
JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ],
		[ 50635,	14500,	16500,	17500 ],
		[ 50636,	14520,	16520,	17520 ],
		[ 50637,	14540,	16540,	17540 ],
		[ 50638,	14560,	16560,	17560 ],
		[ 50639,	14570,	16570,	17570 ],
	]
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

##################################################################

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900

##################################################################

def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:
		return 1
	elif itemVnum == 79013:
		return 1

	return 0

def IS_PET_SEAL(itemVnum):
	if not app.ENABLE_PET_SYSTEM_EX:
		return False
	item.SelectItem(itemVnum)
	itemType = item.GetItemType()
	# itemSubType = item.GetItemSubType()
	return item.ITEM_TYPE_PET == itemType
