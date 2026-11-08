import uiScriptLocale
import localeInfo

ROOT = "d:/ymir work/ui/new/horse/"
LOCALE_PATH = uiScriptLocale.WINDOWS_PATH
SMALL_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_00.sub"
ROOT_PATH = "d:/ymir work/ui/game/windows/"

BOARD_WITH = 375
TITLE_WITH = 375-10
BOARD_HEIGHT = 425

window = {
	"name" : "HorsePanel",
	"x" : SCREEN_WIDTH - 50,
	"y" : SCREEN_HEIGHT - 37 - 300,
	"style" : ("movable", "float",),
	"width" : BOARD_WITH,
	"height" : BOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : BOARD_WITH,
			"height" : BOARD_HEIGHT,
			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 6,
					"y" : 6,
					"width" : TITLE_WITH,
					"color" : "yellow",
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":(TITLE_WITH/2), "y":3, "text": localeInfo.HORSE_PANEL_TITLE, "text_horizontal_align":"center" },
					),
				},
				
				{
					"name" : "horse_image",
					"type" : "button",

					"x" : 168,
					"y" : 218,

					"default_image" : ROOT + "horse_image_default.tga",
					"over_image" : ROOT + "horse_image_over.tga",
					"down_image" : ROOT + "horse_image_down.tga",
				},
				
				{
					"name" : "horse_image2",
					"type" : "image",

					"x" : 2,
					"y" : 11,

					"image" : ROOT + "table.png",
					"children" :
					(
						{ "name":"Ss1_Text", "type":"text", "x":20, "y":3, "text":"HT: ", "r":1.0, "g":1.0, "b":1.0, "a":1.0, },
						{ "name":"Ss1_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
						{ "name":"Ss1_Value", "type":"text", "x":40, "y":3, "text":"11", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
						
						{ "name":"Ss2_Text", "type":"text", "x":20, "y":18, "text":"ST: ", "r":1.0, "g":1.0, "b":1.0, "a":1.0, },
						{ "name":"Ss2_Slot", "type":"image", "x":0, "y":15, "image":SMALL_VALUE_FILE },
						{ "name":"Ss2_Value", "type":"text", "x":40, "y":18, "text":"11", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
					),
				},
				
				## HTH
				{
					"name":"Status_Plus_Label1", "type":"window", "x":50, "y":32, "width":60, "height":20,
					"children" :
					(
						{ "name":"S1_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
						{ "name":"S1_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
						{ "name":"S1_Plus", "type" : "button", "x":41, "y":3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
					),
				},
				
				## HTH
				{
					"name":"Status_Plus_Label2", "type":"window", "x":50, "y":32, "width":60, "height":20,
					"children" :
					(
						{ "name":"S2_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
						{ "name":"S2_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
						{ "name":"S2_Plus", "type" : "button", "x":41, "y":3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
					),
				},
				
				## HTH
				{
					"name":"Status_Plus_Label3", "type":"window", "x":50, "y":32, "width":60, "height":20,
					"children" :
					(
						{ "name":"S3_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
						{ "name":"S3_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
						{ "name":"S3_Plus", "type" : "button", "x":41, "y":3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
					),
				},
				
			),
		},
	),
}

