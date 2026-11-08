import localeInfo

ROOT = "d:/ymir work/ui/game/offlineshop/"
ROOT_PRIVATESHOP = "d:/ymir work/ui/game/privatesearch/"
window = {
	"name" : "OfflineShopBuilder",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 184*2-15+209,
	"height" : 295+26+20+60,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 184*2-15+209,
			"height" : 295+26+20+60,
			"title" : localeInfo.OFFLINE_SHOP_TITLE,
			"children" :
			(
				{
					"name" : "MainWindow",
					"type" : "thinboard",
					"x" : 10,
					"y" : 30,
					"width" : 184*2-15+191,
					"height" : 295+26+20+20,
					"children" :
					(
						{
							"name" : "ItemSlot",
							"type" : "grid_table",
							"x" : 196+17,
							"y" : 34 + 30-20,
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
							"x" : 196+17+(32*5),
							"y" : 34 + 30-20,
							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 8,
							"x_step" : 32,
							"y_step" : 32,
							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},

						{
							"name" : "RenderTarget",
							"type" : "render_target",
							"x" : 10,
							"y" : 34 + 30-20,
							"width" : 196,
							"height" : 8*32, #306
							"index" : 1,
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
									#"default_image" : ROOT+"right_direction_0.tga",
									#"over_image" : ROOT+"right_direction_1.tga",
									#"down_image" : ROOT+"right_direction_0.tga",
									
									"default_image" : ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									"over_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_02.sub",
									"down_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
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
									#"default_image" : ROOT+"right_direction_0.tga",
									#"over_image" : ROOT+"right_direction_1.tga",
									#"down_image" : ROOT+"right_direction_0.tga",
									
									"default_image" : ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									"over_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_02.sub",
									"down_image" 	: ROOT_PRIVATESHOP + "private_last_next_btn_01.sub",
									
								},
								
								{
									"name" : "refresh_render",
									"type" : "button",
									"x" : 155,
									"y": 210,
									
									"default_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_up.sub",
									"over_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_over.sub",
									"down_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_down.sub",
									#"default_image" : ROOT+"refresh_big_0.tga",
									#"over_image" : ROOT+"refresh_big_1.tga",
									#"down_image" : ROOT+"refresh_big_0.tga",
								},
							),
						},

						{
							"name" : "time_slot",
							"type" : "slotbar",
							"x" : 10+300+10,
							"y" : 315,
							"width" : 200,
							"height" : 25,
							"children" :
							(
								{
									"name" : "time_icon",
									"type" : "image",
									"x" : 5,
									"y": 5,
									"image" : ROOT+"time.tga",
									#"default_image" : ROOT+"refresh_big_0.tga",
									#"over_image" : ROOT+"refresh_big_1.tga",
									#"down_image" : ROOT+"refresh_big_0.tga",
								},
								{
									"name" : "time_btn",
									"type" : "button",
									"x" : 25,
									"y": 5,
									"default_image" : ROOT+"time_0.tga",
									"over_image" : ROOT+"time_1.tga",
									"down_image" : ROOT+"time_2.tga",
									#"default_image" : ROOT+"refresh_big_0.tga",
									#"over_image" : ROOT+"refresh_big_1.tga",
									#"down_image" : ROOT+"refresh_big_0.tga",
								},
								{
									"name" : "time",
									"type" : "text",
									"x" : 30,
									"y" : 5,
									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
									"text" : "0",
									"fontname" : "Tahoma:15",
								},
							),
						},
						
						{
							"name" : "See_Slot",
							"type" : "slotbar",
							"x" : 10,
							"y" : 315,
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
						#	"x" : 10,
						#	"y" : 310,
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

				{
					"name" : "LogsWindow",
					"type" : "window",
					"x" : 5,
					"y" : 40,
					"width" : 545,
					"height" : 295+26+20+50,
					"children" :
					(
						#{
						#	"name" : "log_text_0",
						#	"type" : "text",
						#	"x" : 12+10,
						#	"y" : 25,
						#	"text" : localeInfo.OFFLINESHOP_ITEM_NAME+" - "+localeInfo.OFFLINESHOP_YANG+" - "+localeInfo.OFFLINESHOP_RECEIVER+" - "+localeInfo.OFFLINESHOP_HISTORY+" - Whisper",
						#},

						{
							"name" : "ListBox",
							"type" : "listboxex",
							"x" : 5,
							"y" : 43,
							"width" : 184*2-15,
							"height" : 38*40,
							"viewcount" : 10,
						},
						
						{
							"name" : "ScrollBar",
							"type" : "scrollbar_new",
							"x" : 12+520,
							"y" : 35,
							"size" : 315,
						},
					),
				},
				{
					"name" : "NameSlot",
					"type" : "slotbar",
					"x" : 17,
					"y" : 35,
					"width" : 280,
					"height" : 25,
					"children" :
					(
						{
							"name" : "NameLine",
							"type" : "editline",
							"x" : 3,
							"y" : 5,
							"width" : 280,
							"height" : 20,
							"input_limit" : 35,
							"text" : "NULL",
						},

						{
							"name" : "refresh_title",
							"type" : "button",
							"x" : 90+67+96,
							"y": 3,
							"default_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_up.sub",
							"over_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_over.sub",
							"down_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_down.sub",

							#"default_image" : ROOT+"refresh_0.tga",
							#"over_image" : ROOT+"refresh_1.tga",
							#"down_image" : ROOT+"refresh_0.tga",
						},
					),
				},
				
				
				{
					"name" : "Money_Slot",
					"type" : "slotbar",
					"x" : 17+280+5,
					"y" : 35,
					"width" : 90 + 75,
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
							"name" : "refresh_yang",
							"type" : "button",
							"x" : 27,
							"y": 3,
							
							"default_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_up.sub",
							"over_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_over.sub",
							"down_image" : "d:/ymir work/ui/gemshop/gemshop_refreshbutton_down.sub",
							
							#"default_image" : ROOT+"refresh_0.tga",
							#"over_image" : ROOT+"refresh_1.tga",
							#"down_image" : ROOT+"refresh_0.tga",
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
					"x" : 50+90+67+307-35,
					"y": 35,
					"width" : 61,
					"height" : 21,
					
					"default_image" : ROOT+"close_shop_0.tga",
					"over_image" : ROOT+"close_shop_0.tga",
					"down_image" : ROOT+"close_shop_1.tga",
					
					#"default_image" : ROOT+"close_0.tga",
					#"over_image" : ROOT+"close_1.tga",
					#"down_image" : ROOT+"close_0.tga",
					"tooltip_text" : localeInfo.OFFLINESHOP_CLOSE,
				},

				{
					"name" : "SecondButton",
					"type" : "button",
					"x" : 50+90+67+307,
					"y": 35,
					"width" : 61,
					"height" : 21,
					
					"default_image" : ROOT+"history_shop_0.tga",
					"over_image" : ROOT+"history_shop_0.tga",
					"down_image" : ROOT+"history_shop_1.tga",
					
					#"default_image" : ROOT+"log_open_0.tga",
					#"over_image" : ROOT+"log_open_1.tga",
					#"down_image" : ROOT+"log_open_0.tga",
					"tooltip_text" : localeInfo.OFFLINESHOP_LOGS,
				},
			),
		},
	),
}

