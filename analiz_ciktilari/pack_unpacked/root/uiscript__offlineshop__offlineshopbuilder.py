import localeInfo

ROOT = "d:/ymir work/ui/game/offlineshop/"
ROOT_PRIVATESHOP = "d:/ymir work/ui/game/privatesearch/"
window = {
	"name" : "OfflineShopBuilder",

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
							"name" : "NameSlot",
							"type" : "slotbar",
							"x" : 5,
							"y" : 5,
							"width" : 250,
							"height" : 25,
							"children" :
							(
								{
									"name" : "NameLine",
									"type" : "editline",
									"x" : 3,
									"y" : 5,
									"width" : 250,
									"height" : 20,
									"input_limit" : 35,
									"text" : "....",
								},
							),
						},
						
						{
							"name" : "Money_Slot",
							"type" : "slotbar",
							"x" : 5+250+10,
							"y" : 5,
							"width" : 90 + 97,
							"height" : 25,
							"children" :
							(
								{
									"name":"Money_Icon",
									"type":"image",
									"x":3,
									"y":3,
									"image":"d:/ymir work/ui/game/windows/money_icon.tga",
								},
								{
									"name" : "Money",
									"type" : "text",
									"x" : 3,
									"y" : 5,
									"horizontal_align" : "right",
									"text_horizontal_align" : "right",
									"text" : "0",
									"fontname" : "Tahoma:15",
								},
							),
						},
						{
							"name" : "FirstButton",
							"type" : "button",
							"x" : 5+250+10+90+97+40,
							"y": 5,
							"width" : 61,
							"height" : 21,
							"default_image" : ROOT+"decoration_0.tga",
							"over_image" : ROOT+"decoration_0.tga",
							"down_image" : ROOT+"decoration_1.tga",
							#"default_image" : ROOT+"ok_0.tga",
							#"over_image" : ROOT+"ok_1.tga",
							#"down_image" : ROOT+"ok_0.tga",
							"tooltip_text" : localeInfo.OK,
						},
						
						{
							"name" : "SecondButton",
							"type" : "button",
							"x" : 5+250+10+90+97+5,
							"y": 5,
							"width" : 61,
							"height" : 21,
							
							"default_image" : ROOT+"close_shop_0.tga",
							"over_image" : ROOT+"close_shop_0.tga",
							"down_image" : ROOT+"close_shop_1.tga",

							#"default_image" : ROOT+"cancel_0.tga",
							#"over_image" : ROOT+"cancel_1.tga",
							#"down_image" : ROOT+"cancel_0.tga",
							"tooltip_text" : localeInfo.CANCEL,
						},
						{
							"name" : "RenderTarget",
							"type" : "render_target",
							"x" : 10,
							"y" : 34 + 30-20,
							"width" : 196,
							"height" : 8*32, #306
							"index" : 10,
							"children" :
							(
								{
									"name" : "title_back_btn",
									"type" : "button",
									"x" : 5,
									"y" : 30,
									"default_image" : ROOT_PRIVATESHOP + "private_first_prev_btn_01.sub",
									"over_image" 	: ROOT_PRIVATESHOP + "private_first_prev_btn_02.sub",
									"down_image" 	: ROOT_PRIVATESHOP + "private_first_prev_btn_01.sub",
									#"default_image" : ROOT+"left_direction_0.tga",
									#"over_image" : ROOT+"left_direction_1.tga",
									#"down_image" : ROOT+"left_direction_0.tga",
								},
								{
									"name" : "title_next_btn",
									"type" : "button",
									"x" : 175,
									"y" : 32,
									"default_image" : ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									"over_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_02.sub",
									"down_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									#"default_image" : ROOT+"right_direction_0.tga",
									#"over_image" : ROOT+"right_direction_1.tga",
									#"down_image" : ROOT+"right_direction_0.tga",
								},

								{
									"name" : "shop_back_btn",
									"type" : "button",
									"x" : 10,
									"y" : 150,
									"default_image" : ROOT_PRIVATESHOP + "private_first_prev_btn_01.sub",
									"over_image" 	: ROOT_PRIVATESHOP + "private_first_prev_btn_02.sub",
									"down_image" 	: ROOT_PRIVATESHOP + "private_first_prev_btn_01.sub",
									#"default_image" : ROOT+"left_direction_0.tga",
									#"over_image" : ROOT+"left_direction_1.tga",
									#"down_image" : ROOT+"left_direction_0.tga",
								},
								{
									"name" : "shop_next_btn",
									"type" : "button",
									"x" : 165,
									"y" : 150,
									"default_image" : ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									"over_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_02.sub",
									"down_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									#"default_image" : ROOT+"right_direction_0.tga",
									#"over_image" : ROOT+"right_direction_1.tga",
									#"down_image" : ROOT+"right_direction_0.tga",
								},
							),
						},
						{
							"name" : "ItemSlot",
							"type" : "grid_table",
							"x" : 5+196,
							"y" : 34 + 25-20,
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
							"y" : 34 + 25-20,
							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 8,
							"x_step" : 32,
							"y_step" : 32,
							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},
					),
				},
			),
		},
	),
}

