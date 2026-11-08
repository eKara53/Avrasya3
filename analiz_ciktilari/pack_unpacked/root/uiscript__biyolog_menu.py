import uiScriptLocale
import localeInfo
window = {
	"name" : "HorseMenu",

	"x" : SCREEN_WIDTH/2-(380/2),
	"y" : SCREEN_HEIGHT - 37 - 563,

	"style" : ("movable", "float",),

	"width" : 420,
	"height" : 392,

	"children" :
	(
		## Board and buttons
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 420,
			"height" : 392,

			"children" :
			(

				{
					"name":"MissionName", "type":"text", "x" : 248, "y":43, "text":"Mevcut Görev Adý:", "text_horizontal_align":"center"
				},
				{
					"name": "NameOfMission",
					"type": "slotbar",

					"x" : 290,
					"y" : 40,
					"width": 105,
					"height": 18,

					"children":
						(
							{
								"name": "Mission_Name",
								"type": "text",

								"x": 3,
								"y": 3,

								"width": 90,
								"height": 18,
								"text": "Bilgi alýnýyor...",
							},
						),
				},

				{
					"name":"MissionName", "type":"text", "x" : 248, "y":63, "text":"Bekleme Süresi:", "text_horizontal_align":"center"
				},
				{
					"name": "NameOfMission",
					"type": "slotbar",

					"x" : 290,
					"y" : 60,
					"width": 105,
					"height": 18,

					"children":
						(
							{
								"name": "Cooldown_text",
								"type": "text",

								"x": 3,
								"y": 3,

								"width": 90,
								"height": 18,
								"text": "Bilgi alýnýyor...",
							},
						),
				},

				{
					"name":"MissionName", "type":"text", "x" : 248, "y":83, "text":"Verilme Periyodu:", "text_horizontal_align":"center"
				},
				{
					"name": "NameOfMission",
					"type": "slotbar",

					"x" : 290,
					"y" : 80,
					"width": 105,
					"height": 18,

					"children":
						(
							{
								"name": "Periyod",
								"type": "text",

								"x": 3,
								"y": 3,

								"width": 90,
								"height": 18,
								"text": "Bilgi alýnýyor...",
							},
						),
				},

				{
					"name":"MissionName", "type":"text", "x" : 248, "y":103, "text":"Ýlerleme:", "text_horizontal_align":"center"
				},
				{
					"name": "NameOfMission",
					"type": "slotbar",

					"x" : 290,
					"y" : 100,
					"width": 105,
					"height": 18,

					"children":
						(
							{
								"name": "Ilerleme",
								"type": "text",

								"x": 3,
								"y": 3,

								"width": 90,
								"height": 18,
								"text": "Bilgi alýnýyor...",
							},
						),
				},

				{
					"name" : "biyolog_board","type" : "image","style" : ("attach",),"x" : 3,"y" : 25,"image" : "d:/ymir work/systems/biyolog_menu/biyolog_chaeigrap.png"
				},
				{
					"name" : "upgrade_Slot", "type" : "grid_table", "x" : 25, "y" : 210, "start_index" : 0,
					"x_count" : 1, "y_count" : 1, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
					"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
				},
				{
					"name" : "wnd_item_slot", "type" : "grid_table", "x" : 278, "y" : 190, "start_index" : 0,
					"x_count" : 1, "y_count" : 3, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
					"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
				},
				{
					"name" : "upgrade_Slot2", "type" : "grid_table", "x" : 175, "y" : 160, "start_index" : 0,
					"x_count" : 1, "y_count" : 1, "x_step" : 32, "y_step" : 32, "x_blank" : 0, "y_blank" : 0,
					"image" : "d:/ymir work/ui/Public/Slot_Base.sub", "horizontal_align" : "center",
				},

				{
					"name" : "VerButton",
					"type" : "button",

					"x" : 215,
					"y" : 289,

					"text" : "Biyolog Ver",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
				},

				# TitleBar
				{"name" : "TitleBar","type" : "titlebar","style" : ("attach",),"x" : 8,"y" : 8,"width" : 420 - 15,"color" : "gray",
					"children" :
					(
						{
							"name":"TitleName", "type":"text", "x" : (420 - 15) / 2, "y":4, "text":"Biyolog Chaegirap'ýn görevleri serisi", "text_horizontal_align":"center"
						},
					),
				},
				
			),
		},
	),
}