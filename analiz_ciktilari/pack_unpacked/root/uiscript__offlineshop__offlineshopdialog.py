import localeInfo

ROOT = "d:/ymir work/ui/game/offlineshop/"
ROOT_PRIVATESHOP = "d:/ymir work/ui/game/privatesearch/"
window = {
	"name" : "OfflineShopDialog",
	"x" : 0,
	"y" : 0,
	"style" : ("float","movable"),
	"width" : 184*2-15+195,
	"height" : 295+26+30,
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 184*2-15+195,
			"height" : 295+26+30,
			"title" : localeInfo.OFFLINE_SHOP_TITLE,
			"children" :
			(
				{
					"name" : "MainWindow",
					"type" : "thinboard",
					"x" : 10,
					"y" : 30,
					"width" : 184*2-15+175,
					"height" : 295+15,
					"children" :
					(
						{
							"name" : "RenderTarget",
							"type" : "render_target",
							"x" : 5,
							"y" : 5,
							"width" : 196,
							"height" : 8*32,
							"index" : 1,
						},

					## Item Slot
						{
							"name" : "ItemSlot",
							"type" : "grid_table",
							"x" : 5+196,
							"y" : 5,
							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 8,
							"x_step" : 32,
							"y_step" : 32,
							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},
						{
							"name" : "ItemSlot2",
							"type" : "grid_table",
							"x" : 5+196+(32*5),
							"y" : 5,
							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 8,
							"x_step" : 32,
							"y_step" : 32,
							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},

						{
							"name" : "See_Slot",
							"type" : "slotbar",
							"x" : 120,
							"y" : 270,
							"width" : 300,
							"height" : 25,
							"children" :
							(
								{
									"name":"see_icon",
									"type":"image",
									"x":3,
									"y":3,
									"image":"d:/ymir work/ui/game/offlineshop/eyes.tga",
								},
								{
									"name" : "see",
									"type" : "text",
									"x" : 23,
									"y" : 5,
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									"text" : "0",
									"fontname" : "Tahoma:15",
								},
							),
						},

						#{
						#	"name" : "slot",
						#	"type" : "image",
						#	"x" : 130,
						#	"y" : 263,
						#	"image" : ROOT+"slot.tga",
						#	"children":
						#	(
						#		{
						#			"name" : "real_time_image",
						#			"type" : "image",
						#			"x" : 50,
						#			"y" : 7,
						#			"image" : ROOT+"real_time.tga",
						#		},
						#
						#		{
						#			"name" : "see",
						#			"type" : "text",
						#			"x" : 80,
						#			"y" : 2,
						#			"text" : "3432",
						#			"fontname" : "Tahoma:32",
						#		},
						#
						#		{
						#			"name" : "all_count_image",
						#			"type" : "image",
						#			"x" : 150,
						#			"y" : 10,
						#			"image" : ROOT+"eyes.tga",
						#		},
						#
						#		{
						#			"name" : "see_all",
						#			"type" : "text",
						#			"x" : 185,
						#			"y" : 2,
						#			"text" : "3432",
						#			"fontname" : "Tahoma:32",
						#		},
						#
						#	),
						#},
					),
				},
			),
		},
	),
}