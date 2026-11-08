import localeInfo
import app

GOLD_COLOR	= 0xFFFEE3AE
ROOT = "d:/ymir work/ui/game/privatesearch/"
if app.ENABLE_SHOP_SEARCH_SYSTEM:
	BOARD_WIDTH = 810
	BOARD_HEIGHT = 400
	window = {
		"name" : "PrivateShopSearchDialog",
		"x" : 0,
		"y" : 0,
		"style" : ("movable", "float",),
		"width" : BOARD_WIDTH,
		"height" : BOARD_HEIGHT,
		"children" :
		(
			{
				"name" : "board",
				"type" : "board_with_titlebar",
				"x" : 0,
				"y" : 0,
				"width" : BOARD_WIDTH,
				"height" : BOARD_HEIGHT,
				"title" : localeInfo.PRIVATESHOPSEARCH_SEARCH_BAR,
				"children":
				(
					## ItemNameEditLine
					{
						"name" : "ItemNameSlot",
						"type" : "image",
						"x" : 12,
						"y" : 35,
						"image" : ROOT + "name_slot.dds",
						"children" :
						(
							{
								"name" : "itemNameSearchText",
								"type" : "text",
								"x" : 2,
								"y" : 3,
								"text" : "",
								"color" : 0xff075102,
							},
							{
								"name" : "ItemNameValue",
								"type" : "editline",
								"x" : 2,
								"y" : 3,
								"width" : 136,
								"height" : 15,
								"input_limit" : 35,
								"text" : "",
								"outline":1,
							},
							
							
							{
								"name" : "Clearbutton",
								"type" : "button",
								"x" : 185-30,
								"y" : 5,
								"default_image" : ROOT+"clear_button_1.tga", 
								"over_image" : ROOT+"clear_button_2.tga", 
								"down_image" : ROOT+"clear_button_1.tga", 
							},
						),
					},

					{
						"name" : "ListBox",
						"type" : "listbox_new",

						"x" : 200,
						"y" : 58,

						"width" : 600,
						"height" : BOARD_HEIGHT-50,
						"viewcount" : 21,
					},

####################################################################################################
####################################################################################################
####################################################################################################
					## tab_menu_01
					{
						"name" : "ItemTypeImg",
						"type" : "expanded_image",
						"x" : 200,
						"y" : 34,
						"width" : 10,
						"image" : "d:/ymir work/ui/tab_menu_02.tga",
						"x_scale" : 1.22, 
						#"y_scale" : 1.0,
						"children" :
						(
							## Text
							{ "name" : "ResultNameText1", "type" : "text", "x" : 115, "y" : 4,  "text" : localeInfo.PRIVATESHOPSEARCH_ITEMNAME, },
							{ "name" : "ResultNameText2", "type" : "text", "x" : 250, "y" : 4, "text" : localeInfo.PRIVATESHOPSEARCH_SELLER, },
							{ "name" : "ResultNameText3", "type" : "text", "x" : 315, "y" : 4, "text" : localeInfo.PRIVATESHOPSEARCH_COUNT, },

							{
								"name" : "reverse_count", "type" : "button",
								"x" : 315+30, "y" : 4,
								"default_image" : ROOT + "down_1.tga",
								"over_image" 	: ROOT + "down_0.tga",
								"down_image" 	: ROOT + "down_1.tga",
							},

							{ "name" : "ResultNameText5", "type" : "text", "x" : 400, "y" : 4, "text" : "Price", },
							{ "name" : "ResultNameText6", "type" : "text", "x" : 470, "y" : 4, "text" : "Wiki/Shop/Whisper", },
						),
					},
					{
						"name" : "first_prev_button", "type" : "button",
						"x" : 230+100, "y" : BOARD_HEIGHT-28,

						"default_image" : ROOT + "private_first_prev_btn_01.sub",
						"over_image" 	: ROOT + "private_first_prev_btn_02.sub",
						"down_image" 	: ROOT + "private_first_prev_btn_01.sub",
					},
					{
						"name" : "prev_button", "type" : "button",
						"x" : 260+100, "y" : BOARD_HEIGHT-28,
	
						"default_image" : ROOT + "private_prev_btn_01.sub",
						"over_image" 	: ROOT + "private_prev_btn_02.sub",
						"down_image" 	: ROOT + "private_prev_btn_01.sub",
					},
					{
						"name" : "page1_button", "type" : "radio_button",
						"x" : 275+110, "y" : BOARD_HEIGHT-30,
	
						"text" : "10000",
	
						"default_image" : ROOT + "private_pagenumber_00.sub",
						"over_image" 	: ROOT + "private_pagenumber_01.sub",
						"down_image" 	: ROOT + "private_pagenumber_02.sub",
					},
					{
						"name" : "page2_button", "type" : "radio_button",
						"x" : 310+110, "y" : BOARD_HEIGHT-30,
	
						"text" : "2000",
	
						"default_image" : ROOT + "private_pagenumber_00.sub",
						"over_image" 	: ROOT + "private_pagenumber_01.sub",
						"down_image" 	: ROOT + "private_pagenumber_02.sub",
					},
					{
						"name" : "page3_button", "type" : "radio_button",
						"x" : 345+110, "y" : BOARD_HEIGHT-30,
						
						"text" : "300",
	
						"default_image" : ROOT + "private_pagenumber_00.sub",
						"over_image" 	: ROOT + "private_pagenumber_01.sub",
						"down_image" 	: ROOT + "private_pagenumber_02.sub",
					},
					{
						"name" : "page4_button", "type" : "radio_button",
						"x" : 380+110, "y" : BOARD_HEIGHT-30,
	
						"text" : "4",
	
						"default_image" : ROOT + "private_pagenumber_00.sub",
						"over_image" 	: ROOT + "private_pagenumber_01.sub",
						"down_image" 	: ROOT + "private_pagenumber_02.sub",
					},
					{
						"name" : "page5_button", "type" : "radio_button",
						"x" : 415+110, "y" : BOARD_HEIGHT-30,
	
						"text" : "50000",
	
						"default_image" : ROOT + "private_pagenumber_00.sub",
						"over_image" 	: ROOT + "private_pagenumber_01.sub",
						"down_image" 	: ROOT + "private_pagenumber_02.sub",
					},
					{
						"name" : "next_button", "type" : "button",
						"x" : 453+120, "y" : BOARD_HEIGHT-28,
	
						"default_image" : ROOT + "private_next_btn_01.sub",
						"over_image" 	: ROOT + "private_next_btn_02.sub",
						"down_image" 	: ROOT + "private_next_btn_01.sub",
					},
					{
						"name" : "last_next_button", "type" : "button",
						"x" : 483+120, "y" : BOARD_HEIGHT-28,
						"default_image" : ROOT + "private_last_next_btn_01.sub",
						"over_image" 	: ROOT + "private_last_next_btn_02.sub",
						"down_image" 	: ROOT + "private_last_next_btn_01.sub",
					},
					{
						"name" : "FilterButton",
						"type" : "button",
						"x" : 200,
						"y" : 35,
						"default_image" : ROOT+"filter_01.tga", 
						"over_image" : ROOT+"filter_02.tga", 
						"down_image" : ROOT+"filter_03.tga", 
					},
				),
			},

			{
				"name" : "new_table",
				"type" : "board_with_titlebar",
				"x" : 220,
				"y" : 35,
				"width" : 200,
				"height" : 380,
				"title" : "Filter",
				"children":
				(

					{
						"name" : "input_image_3",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45,
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline2", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},

					{
						"name" : "input_image_4",
						"type" : "expanded_image",
						"x" : 105,
						"y" : 45,
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline3", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					
					{
						"name" : "input_image_5",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*1),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline4", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "input_image_6",
						"type" : "expanded_image",
						"x" : 105,
						"y" : 45+(35*1),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline5", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					
					{
						"name" : "input_image_7",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*2),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline6", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "input_image_8",
						"type" : "expanded_image",
						"x" : 105,
						"y" : 45+(35*2),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline7", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					
					{
						"name" : "input_image_9",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*3),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline8", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "input_image_10",
						"type" : "expanded_image",
						"x" : 105,
						"y" : 45+(35*3),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline9", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					
					{
						"name" : "input_image_11",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*4),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline10", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "input_image_12",
						"type" : "expanded_image",
						"x" : 105,
						"y" : 45+(35*4),
						"image": ROOT+"filter_input.tga",
						"children":
						(
							{
								"name" : "editline11", "type" : "editline","x" : 3, "y" : 5,
								"input_limit" : 3, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},

					{
						"name" : "class_image_2",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*5),
						"image": ROOT+"class_image.tga",
					},
					{
						"name" : "class_image_3",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*6),
						"image": ROOT+"class_image.tga",
					},
					{
						"name" : "class_image_4",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*7),
						"image": ROOT+"class_image.tga",
					},
					{
						"name" : "class_image_5",
						"type" : "expanded_image",
						"x" : 10,
						"y" : 45+(35*8),
						"image": ROOT+"class_image.tga",
					},
				),
			},
		),
	}
