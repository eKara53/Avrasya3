import uiScriptLocale
import localeInfo
window = {
	"name" : "HorseMenu",

	"x" : SCREEN_WIDTH/2-(380/2),
	"y" : SCREEN_HEIGHT - 37 - 563,

	"style" : ("movable", "float",),

	"width" : 380,
	"height" : 397,

	"children" :
	(
		## Board and buttons
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 380,
			"height" : 397,

			"children" :
			(
				{
					"name" : "InputName",
					"type" : "text",

					"x" : 15,
					"y" : 40,

					"text" : "Mevcut At Seviyeniz:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 37,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_Level",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName2",
					"type" : "text",

					"x" : 15,
					"y" : 65,

					"text" : "Binme Durumu:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 62,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_Ride",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName3",
					"type" : "text",

					"x" : 15,
					"y" : 90,

					"text" : "Stamina:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 87,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_Stamina",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName4",
					"type" : "text",

					"x" : 15,
					"y" : 115,

					"text" : "HP ve Max HP:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 112,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_HP_and_MAXHP",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},
				{
					"name" : "InputName4",
					"type" : "text",

					"x" : 15,
					"y" : 140,

					"text" : "Yaþam Süresi(Binilirken):",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 137,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_Time",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName4",
					"type" : "text",

					"x" : 15,
					"y" : 165,

					"text" : "Statü STR Gücü:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 162,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_STR",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName5",
					"type" : "text",

					"x" : 15,
					"y" : 190,

					"text" : "Statü DEX Gücü:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 187,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_DX",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName5",
					"type" : "text",

					"x" : 15,
					"y" : 215,

					"text" : "Statü HP Gücü:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 212,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_HT",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},

				{
					"name" : "InputName5",
					"type" : "text",

					"x" : 15,
					"y" : 240,

					"text" : "Statü INT Gücü:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 237,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_IQ",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},
				{
					"name" : "InputName5",
					"type" : "text",

					"x" : 15,
					"y" : 265,

					"text" : "Statü DEF:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 262,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_DEF",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},
				{
					"name" : "InputName5",
					"type" : "text",

					"x" : 15,
					"y" : 290,

					"text" : "At Ýsmi:",
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 130,
					"y" : 287,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "Horse_Name",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,
							"text" : "Bilgi alýnýyor...",
						},
					),
				},


				{
					"name" : "horse_board","type" : "image","style" : ("attach",),"x" : 210,"y" : 240,"image" : "d:/ymir work/systems/horse_menu/horse.png"
				},
				{
					"name" : "horse_madalyon","type" : "image","style" : ("attach",),"x" : 20,"y" : 310,"image" : "d:/ymir work/systems/horse_menu/50050.tga"
				},
				{"name": "Horse_Upgrade_Button", "type": "button", "x": 45, "y": 337,
				 "default_image": "d:/ymir work/ui/game/windows/btn_plus_up.sub", "over_image": "d:/ymir work/ui/game/windows/btn_plus_over.sub",
				 "down_image": "d:/ymir work/ui/game/windows/btn_plus_down.sub", },
				{
					"name" : "Ara_TEXT",
					"type" : "text",

					"x" : 60,
					"y" : 323,
					"fontsize":"LARGE",
					"text" : " => ",
				},
				{
					"name" : "upgrade_Slot", "type" : "grid_table", "x" : 85, "y" : 310, "start_index" : 0,
					"x_count" : 1, "y_count" : 1, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
					"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
				},
				{
					"name":"Money_Slot",
					"type":"button",

					"x":10,
					"y":65,

					"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
					"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
					"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

					"children" :
					(
						{
							"name":"Money_Icon",
							"type":"image",

							"x":-18,
							"y":0,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},

						{
							"name" : "Money",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "123456789",
						},
					),
				},


				# TitleBar
				{"name" : "TitleBar","type" : "titlebar","style" : ("attach",),"x" : 8,"y" : 8,"width" : 380 - 15,"color" : "gray",
					"children" :
					(
						{
							"name":"TitleName", "type":"text", "x" : (380 - 15) / 2, "y":4, "text":"At Geliþtirme Menüsü", "text_horizontal_align":"center"
						},
					),
				},
				
			),
		},
	),
}