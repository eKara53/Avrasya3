import localeInfo

WINDOW_WIDTH	= 627
WINDOW_HEIGHT	= 576

ROOT_PATH = "d:/ymir work/ui/offlineshop/scripts/offlineshop/"
ROOT = "d:/ymir work/ui/offlineshop/loading/"
LOCALE_PATH = "d:/ymir work/ui/game/shopsearchp2p/"
SEARCH_AND_FILTER_BACKGROUND = "d:/ymir work/ui/offlineshop/scripts/offlineshop/background_593_500.png"
SAFEBOX_WITHDRAW_BUTTON	= "d:/ymir work/ui/offlineshop/offlineshop/safebox/withdrawyang_%s.png"

window = {
	"name" : "OfflineshopBoard",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2  - WINDOW_WIDTH/2,
	"y" : SCREEN_HEIGHT/2  - WINDOW_HEIGHT/2,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "MainBoard",
			"type" : "shop_board",

			"style" : ("attach",),

			"x" : 0,
			"y" : 0,
			
			"width" 	: WINDOW_WIDTH,
			"height" 	: WINDOW_HEIGHT,
			
			"children" : 
			(
				# TITLEBAR
				{
					"name" : "TitleBar",
					"type" : "titlebar",

					"x" : 8,
					"y" : 7,

					"width"  : WINDOW_WIDTH - 15,
					"color"  : "red",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":"Offline Shop", "all_align":"center" },
					),
				},


				# MENU
				{
					"name": "Menu",
					"type": "window",

					"x": 18,
					"y": 26,

					"width" : 593,
					"height": 40,
					"children":
					(
						{
							"name": "MyShopButton",
							"type": "button",

							"x" : 0,
							"y" : 10.5,

							"default_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_skin_normal.dds",
							"over_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_skin_hover.dds",
							"down_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_skin_pressed.dds",

							"disable_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_skin_pressed.dds",
						},

						# {
							# "name": "MyAuctionButton",
							# "type": "button",

							# "x" : 48,
							# "y" : 10.5,

							# "default_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_log_normal.dds",
							# "over_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_log_hover.dds",
							# "down_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_log_active.dds",

							# "disable_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_log_active.dds",
						# },

						{
							"name": "ShopSafeboxButton",
							"type": "button",

							"x" : 48,
							"y" : 10.5,

							"default_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_safebox_normal.dds",
							"over_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_safebox_hover.dds",
							"down_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_safebox_pressed.dds",
						},

						{
							"name": "SearchFilterButton",
							"type": "button",

							"x" : 48*2,
							"y" : 10.5,

							"default_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_search_normal.dds",
							"over_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_search_hover.dds",
							"down_image" : "d:/ymir work/ui/game/shopsearchp2p/shop_btn_search_pressed.dds",
						},
					),
				},

				#MyShop_noShop
				{
					"name" : "MyShopBoardNoShop",
					"type" : "window",

					"width" :  621,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name" : "BackGroundCreate",
							"type" : "image",

							"x" : 15, "y" : 0,
							"image": ROOT_PATH + "background_593_500.png",
							"children" : (
								# SLOTBAR_NAME
								{
									"name" : "ShopNameSlot",
									"type" : "slotbar_rb",

									"x" : 147,
									"y" : 8,

									"width" : 297,
									"height" : 18,
									"color_left" : 0xff2A2522,
									"color_right" : 0xff433B38,
									"color_center" : 0xff000000,

									"children" :
									(
										{
											"name" : "ShopNameInput",
											"type" : "editline",
											"x" : 3,
											"y" : 3,
											"width" : 291,
											"height" : 15,
											"input_limit" : 35,
											"text" : "",
										},
									),
								},

								# DAYS
								{
									"name" : "DecreaseDaysButton",
									"type" : "button",

									"x" : 170,
									"y" : 34,

									"default_image" : ROOT_PATH + "decrease_flr.png",
									"over_image" 	: ROOT_PATH + "decrease_hover_flr.png",
									"down_image" 	: ROOT_PATH + "decrease_down_flr.png",
								},

								{
									"name" : "DaysSlot",
									"type" : "slotbar_rb",

									"x" : 187,
									"y" : 35,

									"width" : 38,
									"height" : 17,
									"color_left" : 0xff2A2522,
									"color_right" : 0xff433B38,
									"color_center" : 0xff000000,
									"children" : (
										{
											"name" : "DaysCountText",
											"type" : "text",
											"x" : 19,
											"y" : 2,
											"text" : "0",
											"text_horizontal_align" : "center",
										},
									),
								},

								{
									"name" : "IncreaseDaysButton",
									"type" : "button",


									"x" : 228,
									"y" : 34,

									"default_image" : ROOT_PATH + "increase_flr.png",
									"over_image" 	: ROOT_PATH + "increase_hover_flr.png",
									"down_image" 	: ROOT_PATH + "increase_down_flr.png",
								},

								# HOURS
								{
									"name" : "DecreaseHoursButton",
									"type" : "button",

									"x" : 349,
									"y" : 34,

									"default_image" : ROOT_PATH + "decrease_flr.png",
									"over_image" 	: ROOT_PATH + "decrease_hover_flr.png",
									"down_image" 	: ROOT_PATH + "decrease_down_flr.png",
								},

								{
									"name" : "HoursSlot",
									"type" : "slotbar_rb",

									"x" : 366,
									"y" : 35,

									"width" : 38,
									"height" : 17,
									"color_left" : 0xff2A2522,
									"color_right" : 0xff433B38,
									"color_center" : 0xff000000,
									"children" : (
										{
											"name" : "HoursCountText",
											"type" : "text",
											"x" : 19,
											"y" : 2,
											"text" : "0",
											"text_horizontal_align" : "center",
										},
									),
								},

								{
									"name" : "IncreaseHoursButton",
									"type" : "button",


									"x" : 407,
									"y" : 34,

									"default_image" : ROOT_PATH + "increase_flr.png",
									"over_image" 	: ROOT_PATH + "increase_hover_flr.png",
									"down_image" 	: ROOT_PATH + "increase_down_flr.png",
								},

								# MAX_DURATION
								{
									"name" : "MaxDurationText",
									"type" : "text",
									"text_horizontal_align" : "center",
									"text" : "Maksimum Süre: 8 Gün",
									"color" : 0xfff4ead5,
									"x" : 248+48, "y" :55,
								},

								# CREATE_BUTTON
								{
									"name" : "CreateShopButton",
									"type" : "button",

									"x" : 254.5,
									"y" : 450,

									"default_image" : LOCALE_PATH + "btn_save_normal.dds",
									"over_image" : LOCALE_PATH + "btn_save_hover.dds",
									"down_image" : LOCALE_PATH + "btn_save_pressed.dds",
								},
							),
						},
					),
				},


				#MyShop_Owner
				{
					"name" : "MyShopBoard",
					"type" : "window",

					"width" :  621,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name" : "BackgroundMySHop",
							"type" : "image",

							"x" : 15, "y" : 0,
							"image" : ROOT_PATH + "my_shop_bg.png",
							"children" : (
								# SLOTBAR_NAME
								{
									"name" : "ShopNameSlot",
									"type" : "slotbar_rb",

									"x" : 16,
									"y" : 8,

									"width" : 297,
									"height" : 18,
									"color_left" : 0xff2A2522,
									"color_right" : 0xff433B38,
									"color_center" : 0xff000000,

									"children" :
									(
										{
											"name" : "MyShopShopTitle",
											"type" : "text",
											"x" : 3,
											"y" : 3,
											# "text_horizontal_align" : "center",

											"text" : "",
										},
									),
								},

								# EditName Button
								{
									"name" : "MyShopEditTitleButton",
									"type" : "button",

									"x" : 319, "y" : 8,

									"tooltip_text"	: "Ýsim Düzenle",
									"tooltip_x" : 40,
									"tooltip_y" : 0,

									"default_image" : "d:/ymir work/ui/game/shopsearchp2p/checkbutton.dds",
									"over_image" : "d:/ymir work/ui/game/shopsearchp2p/checkbutton_over.dds",
									"down_image" : "d:/ymir work/ui/game/shopsearchp2p/checkbutton_down.dds",
								},

								# DURATION
								{
									"name" : "MyShopShopDuration",
									"type" : "text",

									"x" : 354,
									"y" : 10,

									"fontname" : "Arial:12",

									"text": "Remaining time: 1d 23h 59m / 3Days",
								},

								# CLOSE SHOP BUTTON
								{
									"name" : "MyShopCloseButton",
									"type" : "button",

									"x" : 535,
									"y" : 8,

									"default_image" : "d:/ymir work/ui/game/shopsearchp2p/closebutton.tga",
									"over_image" : "d:/ymir work/ui/game/shopsearchp2p/closebutton_over.tga",
									"down_image" : "d:/ymir work/ui/game/shopsearchp2p/closebutton_down.tga",

									"tooltip_text" : "Pazarý Kapat",
									"tooltip_x" : 40,
									"tooltip_y" : 0,
								},

								# GAUGE
								{
									"name":"Shop_Time_Gauge_Slot",
									"type":"image",
									"x" : 136.5,
									"y" : 358,

									# "vertical_align" : "bottom",
									"image" : "d:/ymir work/ui/game/shopsearchp2p/timegauge.dds",

									"children" :
									(
										{
											"name" : "Shop_Time_Gauge",
											"type" : "ani_image",

											"x" : 4,
											"y" : 0,

											"delay" : 6,

											"images" :
											(
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/01.tga",
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/02.tga",
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/03.tga",
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/04.tga",
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/05.tga",
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/06.tga",
												"D:/Ymir Work/UI/game/shopsearchp2p/timeGauge/07.tga",
											),
										},
									),
								},

							),
						},

						# BACKGROUND_OFFER
						{
							"name" : "BackgroundMyShopOffer",
							"type" : "image",

							"x" : 15,
							"y" : 383,

							"image" : ROOT_PATH + "background_593_110.png",
							"children" : (
								# OFFER
								{
									"name" : "OfferUserName",
									"type" : "text",

									"x" : 55+25,
									"y" : 5,
									"text_horizontal_align" : "center",
									
									"text" : "Satýcý:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "OfferItemName",
									"type" : "text",

									"x" : 217+21,
									"y" : 5,
									"text_horizontal_align" : "center",

									"text" : "Eþya Adý:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "OfferPrice",
									"type" : "text",

									"x" : 365+26,
									"y" : 5,
									"text_horizontal_align" : "center",

									"text" : "Yang:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "OfferAction",
									"type" : "text",

									"x" : 525+10,
									"y" : 5,
									"text_horizontal_align" : "center",

									"text" : "Hareketler",
									"color" : 0xfff4ead5,
								},
							),
						},
					),
				},

				#shoplist_open
				{
					"name" : "ListOfShop_OpenShop",
					"type" : "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name" : "BackgroundShopListOpen",
							"type" : "image",

							"x" : 15, "y" : 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								# BACK BUTTON
								{
									"name" : "OpenShopBackToListButton",
									"type" : "button",

									"x" : 16, "y" : 7,

									"default_image" : "d:/ymir work/ui/game/shopsearchp2p/btn_back_normal.dds",
									"over_image" : "d:/ymir work/ui/game/shopsearchp2p/btn_back_over.dds",
									"down_image" : "d:/ymir work/ui/game/shopsearchp2p/btn_back_down.dds",
								},

								# SLOT_SHOP_NAME
								{
									"name" : "ShopNameSlot",
									"type" : "slotbar_rb",

									"x" : 147,
									"y" : 7,

									"width" : 297,
									"height" : 18,
									"color_left" : 0xff2A2522,
									"color_right" : 0xff433B38,
									"color_center" : 0xff000000,

									"children" :
									(
										{
											"name" : "OpenShopShopTitle",
											"type" : "text",
											"x" : 3,
											"y" : 3,
											# "text_horizontal_align" : "center",

											"text" : "",
										},
									),
								},
								{
									"name" : "OpenShopShopDuration",
									"type" : "text",

									"x" : 300, "y" : 27,

									"text_horizontal_align" : "center",
									"text" : "99 days",
								},
							),
						},
					),
				},


				#shoplist_list
				{
					"name" : "ListOfShop_List",
					"type" : "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,
					"children":
					(
						{
							"name" : "BackgroundShopList",
							"type" : "image",

							"x" : 15, "y" : 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								{
									"name" : "ShopListName",
									"type" : "text",

									"x" : 30+19,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Satýcý Adý:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "OfferItemName",
									"type" : "text",

									"x" : 175+23,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Pazar Adý:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "OfferPrice",
									"type" : "text",

									"x" : 335+21,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Süre:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "OfferAction",
									"type" : "text",

									"x" : 485+24,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Eþya Sayýsý:",
									"color" : 0xfff4ead5,
								},
							),
						},
					),
				},


				#searchhistory
				{
					"name" : "SearchHistoryBoard",
					"type" : "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,
					"children":
					(
						{
							"name" : "BackgroundSearchHistory",
							"type" : "image",

							"x" : 15, "y" : 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								{
									"name" : "SearchHistoryDate",
									"type" : "text",

									"x" : 55+33,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Tarih:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "SearchHistoryTime",
									"type" : "text",

									"x" : 247+32,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Saat:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "SearchHistoryResult",
									"type" : "text",

									"x" : 475+13,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Eþya Sayýsý:",
									"color" : 0xfff4ead5,
								},
							),
						},
					),
				},


				#mypatterns
				{
					"name" : "MyPatternsBoard",
					"type" : "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,
					"children":
					(
						{
							"name" : "BackgroundMyPatterns",
							"type" : "image",

							"x" : 15, "y" : 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								{
									"name" : "MyPatternsName",
									"type" : "text",

									"x" : 48,
									"y" : 2,

									"text" : "Ýsim:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "MyPatternTime",
									"type" : "text",

									"x" : 397+33,
									"y" : 2,
									"text_horizontal_align" : "center",
									"text" : localeInfo.OFFLINESHOP_LAST_USE_TEXT,
									"color" : 0xfff4ead5,
								},
							),
						},
					),
				},

				#searchfilter
				{
					"name" : "SearchFilterBoard",
					"type" : "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,
					"children":
					(
						{
							"name" : "BackgroundSearchFilter",
							"type" : "image",

							"x" : 15, "y" : 0,

							"image" : SEARCH_AND_FILTER_BACKGROUND,
							"children" : (
								# TEXTS
								{
									"name" : "ItemNameText",
									"type" : "text",

									"x" : 5+7,
									"y" : 8,

									"text" : localeInfo.OFFLINESHOP_ITEM_NAME_TEXT,
									"color" : 0xfff4ead5,
								},

								{
									"name" : "RaceText",
									"type" : "text",

									"x" : 5+7,
									"y" : 8+69,

									"text" : localeInfo.OFFLINESHOP_RACE_TEXT,
									"color" : 0xfff4ead5,
								},

								# SLOT_INPUT_NAME
								{
									"name" : "ItemNameSlot",
									"type" : "image",
									"x" : 5,
									"y" : 22,
									"image" : LOCALE_PATH + "insert.dds",
									"children" :
									(
										{
											"name" : "SearchFilterItemNameInput",
											"type" : "editline",
											"x" : 5,
											"y" : 5,
											"width" : 149,
											"height" : 15,
											"input_limit" : 24,
											"text" : "",
											"children" :
											(
												{
													"name" : "SearchFilterItemNameInput_Hint",
													"type" : "text",

													"x" : 0,
													"y" : 0,

													# "color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.5),
												},
											),
										},

										{
											"name" : "ItemNameEraseBtn",
											"type" : "button",

											"x" : 154,
											"y" : 5,

											"default_image" : LOCALE_PATH + "x_btn_default.dds",
											"over_image" : LOCALE_PATH + "x_btn_hover.dds",
											"down_image" : LOCALE_PATH + "x_btn_down.dds",
										},
									),
								},

								# Main Board Scroll
								{
									"name" : "ContainerScrollBar",
									"type" : "slimscrollbar",

									"x" : 204+365+15,
									"y" : 19,
									"size" : 480,
								},

								# SLOT_RACES
								# {
									# "name" : "RacesSlot",
									# "type" : "image",

									# "x" : 5,
									# "y" : 82,

									# "image" : ROOT_PATH + "ss_races_bg.png",
								# },

								{
									"name" : "CategoryContainer",
									"type" : "window",

									"x" : 5,
									"y" : 135,

									"width" : 185,
									"height" : 377,

									# "image" : ROOT_PATH + "category_container_bg.png",
								},

								# Left Board Scroll
								{
									"name" : "CategoryScrollBar",
									"type" : "slimscrollbar",

									"x" : 185-5,
									"y" : 133,
									"size" : 369,
								},

								# BTN_RESET
								{
									"name" : "SearchFilterResetFilterButton",
									"type" : "button",

									"x" : 213, "y" : 477,

									"default_image" : LOCALE_PATH + "btn_reset_normal.dds",
									"over_image"	: LOCALE_PATH + "btn_reset_hover.dds",
									"down_image"	: LOCALE_PATH + "btn_reset_pressed.dds",
								},

								# BTN_SEARCH
								{
									"name" : "SearchFilterStartSearch",
									"type" : "button",

									"x" : 348, "y" : 477,

									"default_image" : LOCALE_PATH + "btn_search_normal.tga",
									"over_image"	: LOCALE_PATH + "btn_search_hover.tga",
									"down_image"	: LOCALE_PATH + "btn_search_pressed.tga",
								},

								# BTN_SAVE
								{
									"name" : "SearchFilterSavePatternButton",
									"type" : "button",

									"x" : 483, "y" : 477,

									"default_image" : LOCALE_PATH + "btn_save_normal.dds",
									"over_image"	: LOCALE_PATH + "btn_save_hover.dds",
									"down_image"	: LOCALE_PATH + "btn_save_pressed.dds",
								},

							),
						},
					),
				},

				#safebox
				{
					"name": "shopsafeboxpage",
					"type": "window",

					"width" : 622,
					"height" : 500,

					"x" : 3,
					"y" : 26+38,
					"children":
					(
						{
							"name": "BackgroundShopSafeboxPage",
							"type": "image",

							"x": 15,
							"y": 0,

							"image": ROOT_PATH + "background_593_500.png",
							"children" : 
							(
								{
									"name" : "SlotYang",
									"type" : "slotbar_rb",

									"x" : 198,
									"y" : 4,

									"width" : 194,
									"height" : 31,
									"color_left" : 0xff2A2522,
									"color_right" : 0xff433B38,
									"color_center" : 0xff000000,
									"children" : 
									(
										{
											"name" : "ShopSafeboxWithdrawYangButton",
											"type" : "button",

											"x" : 33-8,
											"y" : 7.5,

											"default_image" : SAFEBOX_WITHDRAW_BUTTON % "default",
											"over_image" : SAFEBOX_WITHDRAW_BUTTON % "over",
											"down_image" : SAFEBOX_WITHDRAW_BUTTON % "down",
										},
									),
								},
							),
						},
						{
							"name" : "ShopSafeboxValuteText",
							"type" : "text",

							"x" : 468-154,
							"y" : 22-8,

							"text_horizontal_align" : "center",
							"text" : "000000",
						},
					),
				},

				#my offers
				{
					"name": "MyOffersPage",
					"type": "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name": "BackgroundMyOffersPage",
							"type": "image",

							"x": 15, "y": 0,

							"image": ROOT_PATH + "background_593_500.png",
							"children" : (
								{
									"name" : "HeaderText",
									"type" : "text",

									"x" : 271,
									"y" : 10,

									"text" : localeInfo.OFFLINESHOP_TITLE_MY_OFFERS,
									"color" : 0xfff4ead5,
								},
							),
						},
					),
				},


				# my auction
				{
					"name": "MyAuction",
					"type": "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name": "BackgroundMyAuctionPage",
							"type": "image",

							"x": 15, "y": 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								{
									"name" : "OpenAuctionItemBG",
									"type" : "image",

									"x" : 146.5,
									"y" : 13,

									"image" : ROOT_PATH + "open_auction_.png",
									"children" : (
										# LEFT_DATA
										{
											"name" : "MyAuctionOwner",
											"type" : "text",

											"x" : 5,
											"y" : 17,

											"text" : "Satýcý Adý:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "MyAuctionDuration",
											"type" : "text",

											"x" : 5,
											"y" : 17+24,

											"text" : "Süre:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "MyAuctionBestOffer",
											"type" : "text",

											"x" : 5,
											"y" : 17+24*2,

											"text" : localeInfo.OFFLINESHOP_BEST_OFFER_TEXT,
											"color" : 0xfff4ead5,
										},

										{
											"name" : "MyAuctionMinRaise",
											"type" : "text",

											"x" : 5,
											"y" : 17+24*3,

											"text" : localeInfo.OFFLINESHOP_MIN_RAISE_TEXT,
											"color" : 0xfff4ead5,
										},

										# SLOTS_INPUTS
										{
											"name" : "OpenAuctionSlotOwner",
											"type" : "slotbar_rb",

											"x" : 88,
											"y" : 15,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "MyAuction_OwnerName",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													"text" : "",
												},
											),
										},

										{
											"name" : "OpenAuctionSlotDuration",
											"type" : "slotbar_rb",

											"x" : 88,
											"y" : 15+24,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "MyAuction_Duration",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													"text" : "",
												},
											),
										},

										{
											"name" : "OpenAuctionSlotBestOffer",
											"type" : "slotbar_rb",

											"x" : 88,
											"y" : 15+24*2,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "MyAuction_BestOffer",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													"text" : "",
												},
											),
										},

										{
											"name" : "OpenAuctionSlotMinRaise",
											"type" : "slotbar_rb",

											"x" : 88,
											"y" : 15+24*3,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "MyAuction_MinRaise",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													"text" : "",
												},
											),
										},
									),
								},

								{
									"name" : "DataTitle",
									"type" : "image",

									"x" : 0,
									"y" : 136,
									"image" : ROOT_PATH + "top_background.png",
									"children" : (
										{
											"name" : "DataTitleUser",
											"type" : "text",

											"x" : 173+13,
											"y" : 8,
											"text_horizontal_align" : "center",
											"text" : "Ýsim:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "DataTitleOffer",
											"type" : "text",

											"x" : 392+9,
											"y" : 8,
											"text_horizontal_align" : "center",
											"text" : localeInfo.OFFLINESHOP_OFFER_TEXT,
											"color" : 0xfff4ead5,
										},
									),
								},
							),
						},
					),
				},

				# open acution
				{
					"name": "OpenAuction",
					"type": "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name": "BackgroundOpenAuctionPage",
							"type": "image",

							"x": 15, "y": 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								# BACK BUTTON
								{
									"name" : "OpenAuctionBackToListButton",
									"type" : "button",

									"x" : 16, "y" : 13,

									"default_image" : "d:/ymir work/ui/game/shopsearchp2p/btn_back_normal.dds",
									"over_image" : "d:/ymir work/ui/game/shopsearchp2p/btn_back_over.dds",
									"down_image" : "d:/ymir work/ui/game/shopsearchp2p/btn_back_down.dds",
								},

								{
									"name" : "OpenAuctionItemBG",
									"type" : "image",

									"x" : 146.5,
									"y" : 13,

									"image" : ROOT_PATH + "open_auction_.png",
									"children" : (
										# LEFT_DATA
										{
											"name" : "OpenAuctionOwner",
											"type" : "text",

											"x" : 5,
											"y" : 17,

											"text" : "Satýcý Adý:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "OpenAuctionDuration",
											"type" : "text",

											"x" : 5,
											"y" : 17+24,

											"text" : "Süre:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "OpenAuctionBestOffer",
											"type" : "text",

											"x" : 5,
											"y" : 17+24*2,

											"text" : localeInfo.OFFLINESHOP_BEST_OFFER_TEXT,
											"color" : 0xfff4ead5,
										},

										{
											"name" : "OpenAuctionMinRaise",
											"type" : "text",

											"x" : 5,
											"y" : 17+24*3,

											"text" : localeInfo.OFFLINESHOP_MIN_RAISE_TEXT,
											"color" : 0xfff4ead5,
										},

										# SLOTS_INPUTS
										{
											"name" : "OpenAuctionSlotOwner",
											"type" : "slotbar_rb",

											"x" : 74,
											"y" : 15,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "OpenAuction_OwnerName",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													# "text_horizontal_align" : "center",

													"text" : "",
												},
											),
										},

										{
											"name" : "OpenAuctionSlotDuration",
											"type" : "slotbar_rb",

											"x" : 74,
											"y" : 15+24,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "OpenAuction_Duration",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													# "text_horizontal_align" : "center",

													"text" : "",
												},
											),
										},

										{
											"name" : "OpenAuctionSlotBestOffer",
											"type" : "slotbar_rb",

											"x" : 74,
											"y" : 15+24*2,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "OpenAuction_BestOffer",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													# "text_horizontal_align" : "center",

													"text" : "",
												},
											),
										},

										{
											"name" : "OpenAuctionSlotMinRaise",
											"type" : "slotbar_rb",

											"x" : 74,
											"y" : 15+24*3,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "OpenAuction_MinRaise",
													"type" : "text",
													"x" : 3,
													"y" : 3,
													# "text_horizontal_align" : "center",

													"text" : "",
												},
											),
										},
									),
								},
								{
									"name" : "DataTitle",
									"type" : "image",

									"x" : 0,
									"y" : 136,
									"image" : ROOT_PATH + "top_background.png",
									"children" : (
										{
											"name" : "DataTitleUser",
											"type" : "text",

											"x" : 173,
											"y" : 8,

											"text" : "Ýsim:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "DataTitleOffer",
											"type" : "text",

											"x" : 392,
											"y" : 8,

											"text" : localeInfo.OFFLINESHOP_OFFER_TEXT,
											"color" : 0xfff4ead5,
										},
									),
								},
							),
						},
					),
				},

				# acutionlist
				{
					"name": "AuctionList",
					"type": "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name": "BackgroundAuctionListPage",
							"type": "image",

							"x" : 15, "y" : 0,

							"image" : ROOT_PATH + "background_593_500.png",
							"children" : (
								{
									"name" : "AuctionListOwnerName",
									"type" : "text",

									"x" : 33+19,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Satýcý Adý:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "AuctionListBestOffer",
									"type" : "text",

									"x" : 180+22,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : localeInfo.OFFLINESHOP_BEST_OFFER_TEXT,
									"color" : 0xfff4ead5,
								},

								{
									"name" : "AuctionListDuration",
									"type" : "text",

									"x" : 335+20,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : "Süre:",
									"color" : 0xfff4ead5,
								},

								{
									"name" : "AuctionListNOffer",
									"type" : "text",

									"x" : 470+40,
									"y" : 3,
									"text_horizontal_align" : "center",
									"text" : localeInfo.OFFLINESHOP_OFFER_COUNT_TEXT,
									"color" : 0xfff4ead5,
								},
							),
						},
					),
				},

				#create auction
				{
					"name": "CreateAuction",
					"type": "window",

					"width" :  622,  "height" :  500,

					"x" : 3, "y" : 26+38,

					"children":
					(
						{
							"name": "BackgroundCreateAuctionPage",
							"type": "image",

							"x": 15, "y": 0,

							"image": ROOT_PATH + "my_shop_bg.png",
							"children" : (
								{
									"name" : "BackgroundCreateAuctionMain",
									"type" : "image",

									"x" : 146.5,
									"y" : 130.5,

									"image" : ROOT_PATH + "open_auction_.png",
									"children" : (

										{
											"name": "CreateAuctionDecreaseDaysButton",
											"type": "button",

											"x" : 181,
											"y" : 19,

											"default_image" : ROOT_PATH + "increase_flr.png",
											"over_image" 	: ROOT_PATH + "increase_hover_flr.png",
											"down_image" 	: ROOT_PATH + "increase_down_flr.png",
										},

										{
											"name" : "CreateAuctionIncreaseDaysButton",
											"type" : "button",

											"x": 85,
											"y": 19,

											"default_image" : ROOT_PATH + "decrease_flr.png",
											"over_image" 	: ROOT_PATH + "decrease_hover_flr.png",
											"down_image" 	: ROOT_PATH + "decrease_down_flr.png",
										},

										# SLOTS_INPUTS
										{
											"name" : "CreateAuctionSlotDays",
											"type" : "slotbar_rb",

											"x" : 102,
											"y" : 20,

											"width" : 76,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,
											"children" : (
												{
													"name": "CreateAuctionDaysInput",
													"type": "text",

													"width": 23, "height": 17,

													"text_horizontal_align" : "center",
													"text" : "0",
													"x": 37, "y": 2,
												},
											),
										},

										{
											"name" : "CreateAuctionDuration",
											"type" : "text",

											"x" : 142,
											"y" : 5,
											"text_horizontal_align" : "center",
											"text" : "Süre:",
											"color" : 0xfff4ead5,
										},

										{
											"name" : "CreateAuctionStartPrice",
											"type" : "text",

											"x" : 142,
											"y" : 45,
											"text_horizontal_align" : "center",
											"text" : localeInfo.OFFLINESHOP_STARTING_PRICE_TEXT,
											"color" : 0xfff4ead5,
										},

										{
											"name" : "CreateAuctionSlotPrice",
											"type" : "slotbar_rb",

											"x" : 65,
											"y" : 60,

											"width" : 150,
											"height" : 18,
											"color_left" : 0xff2A2522,
											"color_right" : 0xff433B38,
											"color_center" : 0xff000000,

											"children" :
											(
												{
													"name" : "CreateAuctionStartingPriceInput",
													"type" : "editline",

													"x" : 3,
													"y" : 3,

													"width" : 144,
													"height" : 15,


													"input_limit": 10,
													"only_number": 1,
												},
											),
										},

										# CREATE_AUCTION
										{
											"name" : "CreateAuctionCreateAuctionButton",
											"type" : "button",

											"x" : 98, "y" : 89,

											"default_image" : LOCALE_PATH + "btn_save_normal.dds",
											"over_image" : LOCALE_PATH + "btn_save_hover.dds",
											"down_image" : LOCALE_PATH + "btn_save_pressed.dds",
										},
									),
								},
							),

						},

					),
				},

				{
					"name" : "AnimationWindow",
					"type" : "ani_image",

					"x" : -27, "y" : -15,

					"vertical_align" : "center",
					"horizontal_align" : "center",

					"delay" : 2.5,

					"images" :
					(
						ROOT + "loading_image0.png",
						ROOT + "loading_image1.png",
						ROOT + "loading_image2.png",
						ROOT + "loading_image3.png",
						ROOT + "loading_image4.png",
						ROOT + "loading_image5.png",
						ROOT + "loading_image6.png",
						ROOT + "loading_image7.png",
						ROOT + "loading_image8.png",
						ROOT + "loading_image9.png",
						ROOT + "loading_image10.png",
						ROOT + "loading_image11.png",
						ROOT + "loading_image12.png",
						ROOT + "loading_image13.png",
						ROOT + "loading_image14.png",
						ROOT + "loading_image15.png",
						ROOT + "loading_image16.png",
						ROOT + "loading_image17.png",
					)
				},
			),
		},
	),
}