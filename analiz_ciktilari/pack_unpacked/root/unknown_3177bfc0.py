import localeInfo
import app

WINDOW_WIDTH    = 624
WINDOW_HEIGHT    = 595

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
            "type" : "board",

            "style" : ("attach",),

            "x" : 0,
            "y" : 0,

            "width"     : WINDOW_WIDTH,
            "height"     : WINDOW_HEIGHT,

            "children" :
            (
                {
                    "name" : "TitleBar",
                    "type" : "titlebar",

                    "x" : 8,
                    "y" : 7,

                    "width"  : WINDOW_WIDTH - 16,

                    "children" :
                    (
                        {
                            "name" : "TitleName",
                            "type" : "text",

                            "x" : 0,
                            "y" : 3,

                            "text" : "",

                            "text_horizontal_align":"center",
                            "horizontal_align":"center",
                        },
                    ),
                },

                {
                    "name" : "MyShopBoardNoShop",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name" : "BackGroundCreate",
                        #    "type" : "image",

                        #    "x" : 0, "y" : 0,
                        #    "image": "D:/ymir work/ui/offlineshop/createshop/base_image_1.png",

                        #},

                        {
                            "name" : "MyShopBoardNoShopChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (

                                {
                                    "name" : "ShopNameInputContainer",
                                    "type" : "image",

                                    "x" : 212, "y" : 23,

                                    "image" : "D:/ymir work/ui/offlineshop/input.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "ShopNameInput",
                                            "type" : "editline",

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "width" : 170, "height" : 15,

                                            "input_limit" : 35,
                                            "x" : 6, "y" : 5,
                                        },
                                    )
                                },

                                {
                                    "name" : "DaysCountTextContainer",
                                    "type" : "image",

                                    "x" : 255 - 28, "y" : 80,

                                    "image" : "D:/ymir work/ui/offlineshop/input_small.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "DaysCountText",
                                            "type" : "text",

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "text" : "0",
                                            "text_horizontal_align" : "center",
                                            "x" : 22, "y" :4,
                                        },
                                    )
                                },

                                {
                                    "name" : "HoursCountTextContainer",
                                    "type" : "image",

                                    "x" : 356 - 28, "y" : 80,

                                    "image" : "D:/ymir work/ui/offlineshop/input_small.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "HoursCountText",
                                            "type" : "text",

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "text" : "0",
                                            "text_horizontal_align" : "center",
                                            "x" : 22, "y" : 4,
                                        },
                                    )
                                },

                                {
                                    "name" : "IncreaseDaysButton",
                                    "type" : "button",


                                    "x" : 285-10,
                                    "y" : 91 - 30 + 20,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button_scroll_right.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/button_scroll_right_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/button_scroll_right_active.tga",
                                },

                                {
                                    "name" : "DecreaseDaysButton",
                                    "type" : "button",

                                    "x" : 208,
                                    "y" : 91 - 30 + 20,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button_scroll_left.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/button_scroll_left_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/button_scroll_left_active.tga",
                                },

                                {
                                    "name" : "IncreaseHoursButton",
                                    "type" : "button",

                                    "x" : 400 - 8 - 16,
                                    "y" : 91 - 30 + 20,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button_scroll_right.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/button_scroll_right_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/button_scroll_right_active.tga",
                                },

                                {
                                    "name" : "DecreaseHoursButton",
                                    "type" : "button",

                                    "x" : 330-3 - 18,
                                    "y" : 91 - 30 + 20,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button_scroll_left.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/button_scroll_left_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/button_scroll_left_active.tga",
                                },

                                {
                                    "name" : "CreateShopButton",
                                    "type" : "button",

                                    "x" : 249 + 40 - 45,
                                    "y" : 482 - 8 - 30 + 21,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                                    "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                                    "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                                    "text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CREATE_TEXT,
                                },

        ## FLR_CHANGES
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 298 - 12,
                                    "y" : 15 - 8,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 291 - 7,
                                    "y" : 53,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 241,
                                    "y" : 66,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_DAYS_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 341,
                                    "y" : 66,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_HOURS_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 262 - 10,
                                    "y" : 455 - 30 + 21,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_MAX_DURATION_TEXT,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_MYSHOP, "text_horizontal_align":"center", "horizontal_align":"center" },
## END
                    ),
                },

                {
                    "name" : "MyShopBoard",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name" : "BackgroundMySHop",
                        #    "type" : "image",

                        #    "x" : 0, "y" : 0,

                        #    "image" : "D:/ymir work/ui/offlineshop/myshop/base_image_0.png",
                        #},

                        {
                            "name" : "MyShopBoardChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 384,

                            "children" :
                            (
                                {
                                    "name" : "MyShopShopTitleContainer",
                                    "type" : "image",

                                    "x" : 195, "y" : 5,

                                    "image" : "D:/ymir work/ui/offlineshop/input.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "MyShopShopTitle",
                                            "type" : "text",

                                            "x" : 88, "y" : 4,

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "text" : "title",
                                            "text_horizontal_align" : "center",
                                        },
                                    )
                                },

                                {
                                    "name" : "MyShopEditTitleButton",
                                    "type" : "button",

                                    "x" : 386, "y" : 9,

                                    "tooltip_text"    : localeInfo.OFFLINESHOP_EDIT_SHOPNAME_TOOLTIP,

                                    "default_image" : "D:/ymir work/ui/offlineshop/myshop/editname_default.png",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/myshop/editname_over.png",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/myshop/editname_down.png",
                                },
								
								
								 {
                                    "name" : "MyShopIncreaseTime",
                                    "type" : "button",

                                    "x" : 446, "y" : 9,
									
									"text": localeInfo.OFFLINESHOP_INCREASE_TIME,
									
                                    #"tooltip_text"    : localeInfo.OFFLINESHOP_EDIT_SHOPNAME_TOOLTIP,

									"default_image" : "D:/ymir work/ui/offlineshop/button.tga",
									"over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
									"down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",
                                },
								
								
                                {
                                    "name" : "MyShopShopDurationContainer",
                                    "type" : "image",

                                    "x" : 195, "y" : 30,

                                    "image" : "D:/ymir work/ui/offlineshop/input.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "MyShopShopDuration",
                                            "type" : "text",

                                            "x" : 88, "y" : 4,

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "text" : "99 days",
                                            "text_horizontal_align" : "center",
                                        },
                                    )
                                },

                                {
                                    "name" : "MyShopCloseButton",
                                    "type" : "button",

                                    "x" : 15, "y" : 10,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                                    "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                                    "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                                    "text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CLOSE_SHOP_TEXT,
                                },


        ## FLR_CHANGES
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 144,
                                    "y" : 9,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_TITLE_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 144,
                                    "y" : 34,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },
                            )
                        },

                        {
                            "name" : "MyShopBoardChild2",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46 + 384 + 15,

                            "width"     : 600,
                            "height"     : 108,

                            "children" :
                            (
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 65,
                                    "y" : 9,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 245,
                                    "y" : 9,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_ITEM_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 410,
                                    "y" : 9,

                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451,

                                    "text" : localeInfo.OFFLINESHOP_OFFER_TEXT,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                         { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_MYSHOP, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name" : "ListOfShop_OpenShop",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name" : "BackgroundShopListOpen",
                        #    "type" : "image",

                        #    "x" : 0, "y" : 0,

                        #    "image" : "D:/ymir work/ui/offlineshop/shoplist/base_image_open.png",
                        #},

                        {
                            "name" : "CreateAuctionChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (
                                {
                                    "name" : "OpenShopShopTitleContainer",
                                    "type" : "image",

                                    "x" : 187, "y" : 5,

                                    "image" : "D:/ymir work/ui/offlineshop/input.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "OpenShopShopTitle",
                                            "type" : "text",

                                            "x" : 88, "y" : 4,

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "text_horizontal_align" : "center",
                                            "text" : "title",
                                        },
                                    )
                                },


                                {
                                    "name" : "OpenShopShopDurationContainer",
                                    "type" : "image",

                                    "x" : 187, "y" : 30,

                                    "image" : "D:/ymir work/ui/offlineshop/input.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "OpenShopShopDuration",
                                            "type" : "text",

                                            "x" : 88, "y" : 4,

                                            "r": 0.525,
                                            "g": 0.475,
                                            "b": 0.451,

                                            "text_horizontal_align" : "center",
                                            "text" : "99 days",
                                        },
                                    )
                                },

                                {
                                    "name" : "OpenShopShopOwnerButton",
                                    "type" : "button",

                                    "x" : 420, "y" : 5,

                                    "default_image" : "D:/ymir work/ui/offlineshop/input.tga",
                                    "over_image" : "D:/ymir work/ui/offlineshop/input.tga",
                                    "down_image" : "D:/ymir work/ui/offlineshop/input.tga",

                                    "text" : "title",
                                    "text_horizontal_align" : "center",
                                    "r": 0.525,
                                    "g": 0.475,
                                    "b": 0.451
                                },
        ## FLR_CHANGES
                                {
                                    "name" : "OpenShopBackToListButton",
                                    "type" : "button",

                                    "x" : 15, "y" : 10,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                                    "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                                    "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                                    "text" : localeInfo.OFFLINESHOP_BACK_TO_LIST_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 144,
                                    "y" : 9,

                                    "text" : localeInfo.OFFLINESHOP_TITLE_TEXT,
                                },

                                {
                                    "name" : "FlrText2",
                                    "type" : "text",

                                    "x" : 144,
                                    "y" : 34,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText3",
                                    "type" : "text",

                                    "x" : 372,
                                    "y" : 9,

                                    "text" : localeInfo.OFFLINESHOP_OWNER_NAME_TEXT2,
                                },
                            )
                        },

## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_LIST_OF_SHOPS, "text_horizontal_align":"center", "horizontal_align":"center" },
## END
                    ),
                },

                {
                    "name" : "ListOfShop_List",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,
                    "children":
                    (
                        #{
                        #    "name" : "BackgroundShopList",
                        #    "type" : "image",

                        #    "x" : 0, "y" : 0,

                        #    "image" : "D:/ymir work/ui/offlineshop/shoplist/base_image_list.png",
                        #},

## FLR_CHANGES
                        {
                            "name" : "ListOfShop_ListChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 375 + 111,

                            "children" :
                            (
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 45,
                                    "y" : 11,

                                    "text" : localeInfo.OFFLINESHOP_OWNER_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 196,
                                    "y" : 11,

                                    "text" : localeInfo.OFFLINESHOP_SHOPS_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 362,
                                    "y" : 11,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 480,
                                    "y" : 11,

                                    "text" : localeInfo.OFFLINESHOP_ITEMS_COUNT_TEXT_1,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_LIST_OF_SHOPS, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name" : "SearchHistoryBoard",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,
                    "children":
                    (
                        #{
                        #    "name" : "BackgroundSearchHistory",
                        #    "type" : "image",

                        #    "x" : 0, "y" : 0,

                        #    "image" : "D:/ymir work/ui/offlineshop/searchhistory/base_image.png",
                        #},

## FLR_CHANGES
                        {
                            "name" : "SearchHistoryBoardChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 92,
                                    "y" : 12,

                                    "text" : localeInfo.OFFLINESHOP_DATE_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 282,
                                    "y" : 12,

                                    "text" : localeInfo.OFFLINESHOP_TIME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 473,
                                    "y" : 12,

                                    "text" : localeInfo.OFFLINESHOP_ITEMS_COUNT_TEXT_1,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_SEARCH_HISTORY, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name" : "MyPatternsBoard",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,
                    "children":
                    (
                        #{
                        #    "name" : "BackgroundMyPatterns",
                        #    "type" : "image",
                        #
                        #    "x" : 0, "y" : 0,
                        #
                        #    "image" : "D:/ymir work/ui/offlineshop/mypatterns/base_image.png",
                        #},

## FLR_CHANGES
                        {
                            "name" : "SearchHistoryBoardChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 35,
                                    "y" : 12,

                                    "text" : localeInfo.OFFLINESHOP_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 393,
                                    "y" : 12,

                                    "text" : localeInfo.OFFLINESHOP_LAST_USE_TEXT,
                                },
                            )
                        },

## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_MY_PATTERNS, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name" : "SearchFilterBoard",
                    "type" : "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,
                    "children":
                    (
                        #{
                        #    "name" : "BackgroundSearchFilter",
                        #    "type" : "image",
                        #
                        #    "x" : 0, "y" : 0,
                        #
                        #    "image" : "D:/ymir work/ui/offlineshop/searchfilter/base_image.png",
                        #},

                        {
                            "name" : "SearchFilterBoardChild01",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 204,
                            "height"     : 75
                        },

                        {
                            "name" : "SearchFilterBoardChild02",
                            "type" : "thinboard",

                            "x" : 9 + 205,
                            "y" : 46,

                            "width"     : 113,
                            "height"     : 75
                        },

                        {
                            "name" : "SearchFilterBoardChild03",
                            "type" : "thinboard",

                            "x" : 9 + 205 + 114,
                            "y" : 46,

                            "width"     : 74,
                            "height"     : 75
                        },

                        {
                            "name" : "SearchFilterBoardChild04",
                            "type" : "thinboard",

                            "x" : 9 + 205 + 114 + 75,
                            "y" : 46,

                            "width"     : 198,
                            "height"     : 147
                        },

                        {
                            "name" : "SearchFilterBoardChild05",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46 + 76,

                            "width"     : 204,
                            "height"     : 71
                        },

                        {
                            "name" : "SearchFilterBoardChild06",
                            "type" : "thinboard",

                            "x" : 9 + 205,
                            "y" : 46 + 76,

                            "width"     : 188,
                            "height"     : 71
                        },

                        {
                            "name" : "SearchFilterBoardChild07",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46 + 187 - 39,

                            "width"     : 592,
                            "height"     : 331
                        },

                        {
                            "name" : "SearchFilterItemNameInputContainer",
                            "type" : "image",

                            "x" : 75, "y" : 31 + 43,

                            "image" : "D:/ymir work/ui/offlineshop/input_search_item.tga",

                            "children" :
                            (
                                {
                                    "name" : "SearchFilterItemNameInput",
                                    "type" : "editline",

                                    "width" : 126, "height" : 15,

                                    "input_limit" : 24,
                                    "x" : 5, "y" : 3,
                                },
                            )
                        },

                        {
                            "name" : "SearchFilterItemNameInputContainer",
                            "type" : "image",

                            "x" : 75, "y" : 31 + 43 + 21,

                            "image" : "D:/ymir work/ui/offlineshop/input_search_item.tga"
                        },

                        {
                            "name" : "SearchFilterTypeContainer",
                            "type" : "image",

                            "x" : 220, "y" : 29 + 45,

                            "image" : "D:/ymir work/ui/offlineshop/input_search_type.tga"
                        },

                        {
                            "name" : "SearchFilterSubtypeContainer",
                            "type" : "image",

                            "x" : 220, "y" : 50 + 45,

                            "image" : "D:/ymir work/ui/offlineshop/input_search_type.tga"
                        },

                        {
                            "name" : "SearchFilterItemLevelStartContainer",
                            "type" : "image",

                            "x" : 334 + 31, "y" : 32 + 42,

                            "image" : "D:/ymir work/ui/offlineshop/input_search_level.tga",

                            "children" :
                            (
                                {
                                    "name" : "SearchFilterItemLevelStart",
                                    "type" : "editline",

                                    "width" : 26, "height" : 15,

                                    "input_limit" : 3,
                                    "only_number" : 1,
                                    "x" : 5, "y" : 3,
                                },
                            )
                        },

                        {
                            "name" : "SearchFilterItemLevelEndContainer",
                            "type" : "image",

                            "x" : 334 + 31, "y" : 52 + 43,

                            "image" : "D:/ymir work/ui/offlineshop/input_search_level.tga",

                            "children" :
                            (
                                {
                                    "name" : "SearchFilterItemLevelEnd",
                                    "type" : "editline",

                                    "width" : 26, "height" : 15,

                                    "input_limit" : 3,
                                    "only_number" : 1,
                                    "x" : 5, "y" : 3,
                                },
                            )
                        },

                        {
                            "name" : "SearchFilterItemYangMinContainer",
                            "type" : "image",

                            "x" : 258, "y" : 105 + 41,

                            "image" : "D:/ymir work/ui/offlineshop/input_price.tga",

                            "children" :
                            (
                                {
                                    "name" : "SearchFilterItemYangMin",
                                    "type" : "editline",

                                    "width" : 124, "height" : 12,

                                    "input_limit" : len("99999999999999999"), #topatch
                                    "only_number" : 0,
                                    "x" : 6, "y" : 3,
                                },
                            )
                        },

                        {
                            "name" : "SearchFilterItemYangMaxContainer",
                            "type" : "image",

                            "x" : 258, "y" : 127 + 42,

                            "image" : "D:/ymir work/ui/offlineshop/input_price.tga",

                            "children" :
                            (
                                {
                                    "name" : "SearchFilterItemYangMax",
                                    "type" : "editline",

                                    "width" : 124, "height" : 12,

                                    "input_limit" : len("99999999999999999"), #topatch
                                    "only_number" : 0,
                                    "x" : 6, "y" : 3,
                                },
                            )
                        },

                        {
                            "name" : "SearchFilterResetFilterButton",
                            "type" : "button",

                            "x" : 400 - 19, "y" : 487 + 45 - 2,

                            "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                            "text" : localeInfo.OFFLINESHOP_SCRIPTFILE_RESET_FILTER_TEXT,
                        },

                        {
                            "name" : "SearchFilterSavePatternButton",
                            "type" : "button",

                            "x" : 136 - 19, "y" : 487 + 45 - 2,

                            "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                            "text" : localeInfo.OFFLINESHOP_SCRIPTFILE_SAVE_AS_PATTERN_TEXT,
                        },

                        {
                            "name" : "SearchFilterStartSearch",
                            "type" : "button",

                            "x" : 268 - 19, "y" : 487 + 45 - 2,

                            "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                            "text" : localeInfo.OFFLINESHOP_SCRIPTFILE_START_SEARCH_TEXT,
                        },

                        {
                            "name" : "SearchFilterAttributeButton1",
                            "type" : "button",

                            "x" : 417, "y" : 35 + 45,

                            "default_image" : "D:/ymir work/ui/offlineshop/searchfilter/attribute_default.png",
                            "over_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_over.png",
                            "down_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_down.png",
                        },

                        {
                            "name" : "SearchFilterAttributeButton2",
                            "type" : "button",

                            "x" : 417, "y" : 35+22 + 45,

                            "default_image" : "D:/ymir work/ui/offlineshop/searchfilter/attribute_default.png",
                            "over_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_over.png",
                            "down_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_down.png",
                        },

                        {
                            "name" : "SearchFilterAttributeButton3",
                            "type" : "button",

                            "x" : 417, "y" : 35+22*2 + 45,

                            "default_image" : "D:/ymir work/ui/offlineshop/searchfilter/attribute_default.png",
                            "over_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_over.png",
                            "down_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_down.png",
                        },

                        {
                            "name" : "SearchFilterAttributeButton4",
                            "type" : "button",

                            "x" : 417, "y" : 35+22*3 + 45,

                            "default_image" : "D:/ymir work/ui/offlineshop/searchfilter/attribute_default.png",
                            "over_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_over.png",
                            "down_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_down.png",
                        },

                        {
                            "name" : "SearchFilterAttributeButton5",
                            "type" : "button",

                            "x" : 417, "y" : 35+22*4 + 45,

                            "default_image" : "D:/ymir work/ui/offlineshop/searchfilter/attribute_default.png",
                            "over_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_over.png",
                            "down_image"     : "D:/ymir work/ui/offlineshop/searchfilter/attribute_down.png",
                        },

                        # Main Board Scroll
                        {
                            "name" : "ContainerScrollBar",
                            "type" : "slimscrollbar",

                            "x" : 595,
                            "y" : 195,
                            "size" : 332,
                        },

## FLR_CHANGES
                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 33,
                            "y" : 6 + 45,

                            "text" : localeInfo.OFFLINESHOP_ITEM_NAME_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 238,
                            "y" : 6 + 45,

                            "text" : localeInfo.OFFLINESHOP_TYPE_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 352,
                            "y" : 6 + 45,

                            "text" : "Level:",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 334,
                            "y" : 31 + 45,

                            "text" : "Min:",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 334,
                            "y" : 52 + 45,

                            "text" : "Max:",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 427,
                            "y" : 6 + 45,

                            "text" : localeInfo.OFFLINESHOP_ATTR_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 17,
                            "y" : 31 + 45,

                            "text" : localeInfo.OFFLINESHOP_INPUT_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 17,
                            "y" : 52 + 45,

                            "text" : localeInfo.OFFLINESHOP_SUGGESTIONS_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 33,
                            "y" : 82 + 45,

                            "text" : localeInfo.OFFLINESHOP_RACE_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 110 - 17,
                            "y" : 94 + 45 - 1,

                            "text" : "Savaþçý",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 110 + 63 - 8,
                            "y" : 94 + 45 - 1,

                            "text" : "Sura",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 110 - 17,
                            "y" : 94 + 26 + 45 - 1,

                            "text" : "Ninja",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 110 + 63 - 8,
                            "y" : 94 + 26 + 45 - 1,

                            "text" : "Þaman",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 238,
                            "y" : 82 + 45,

                            "text" : localeInfo.OFFLINESHOP_PRICE_TEXT,
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 110 + 117,
                            "y" : 103 + 45,

                            "text" : "Min:",
                        },

                        {
                            "name" : "FlrText",
                            "type" : "text",

                            "x" : 110 + 117,
                            "y" : 103 + 23 + 45,

                            "text" : "Max:",
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_SEARCH, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name": "shopsafeboxpage",
                    "type": "window",

                    "width" :  622,
                    "height" :  567,

                    "x" : 3,
                    "y" : 28,

                    "children":
                    (
                        #{
                        #    "name": "BackgroundShopSafeboxPage",
                        #    "type": "image",
                        #
                        #    "x": 0, "y": 0,
                        #
                        #    "image": "D:/ymir work/ui/offlineshop/safebox/safebox_base_image.png",
                        #},

                        {
                            "name" : "ShopSafeboxPageChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 375 + 111,

                            "children" :
                            (
                                {
                                    "name" : "ShopSafeboxWithdrawItemsButton",
                                    "type" : "button",

                                    "x" : 15, "y" : 10,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                                    "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                                    "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                                    "text" : localeInfo.OFFLINESHOP_WITHDRAW_ALL_ITEMS,
                                },

                                {
                                    "name" : "ShopSafeboxWithdrawYangButton",
                                    "type" : "button",

                                    "x" : 447-205 - 30,
                                    "y" : 16-4 + 2,

                                    "default_image" : "D:/ymir work/ui/offlineshop/input_money.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/input_money_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/input_money.tga",

                                    "children" :
                                    (
                                        {
                                            "name" : "ShopSafeboxValuteText",
                                            "type" : "text",

                                            "x" : 98,
                                            "y" : 3,

                                            "text_horizontal_align" : "center",
                                            "text" : "000000",
                                        },
                                    )
                                },
                            )
                        },

## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        {
                            "name" : "TitleName",
                            "type" : "text",

                            "x" : 0,
                            "y" : -18,

                            "text" : localeInfo.OFFLINESHOP_TITLE_SAFEBOX,

                            "text_horizontal_align":"center",
                            "horizontal_align":"center",
                        },
## END
                    ),
                },

                {
                    "name": "MyOffersPage",
                    "type": "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name": "BackgroundMyOffersPage",
                        #    "type": "image",

                        #    "x": 0, "y": 0,

                        #    "image": "D:/ymir work/ui/offlineshop/myoffers/base_image.png",
                        #},
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_MY_OFFERS, "text_horizontal_align":"center", "horizontal_align":"center" },
## END
                    ),
                },

                {
                    "name": "MyAuction",
                    "type": "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name": "BackgroundMyAuctionPage",
                        #    "type": "image",

                        #    "x": 0, "y": 0,

                        #    "image": "D:/ymir work/ui/offlineshop/myauction/base_image.png",
                        #},

                        {
                            "name" : "MyAuctionChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (
                                {
                                    "name" : "MyAuction_OwnerName",
                                    "type" : "text",

                                    "x" : 235+67, "y" : 100-70,
                                    "text_horizontal_align" : "center",
                                    "text" : " noname ",
                                },

                                {
                                    "name" : "MyAuction_Duration",
                                    "type" : "text",

                                    "x" : 235+67, "y" : 145-91,
                                    "text_horizontal_align" : "center",
                                    "text" : " noname ",
                                },

                                {
                                    "name" : "MyAuction_BestOffer",
                                    "type" : "text",

                                    "x" : 235+67, "y" : 197-123,
                                    "text_horizontal_align" : "center",
                                    "text" : " noname ",
                                },

                                {
                                    "name": "MyAuction_MinRaise",
                                    "type": "text",

                                    "x": 235+67, "y": 243-147,
                                    "text_horizontal_align": "center",
                                    "text": " noname ",
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 29,

                                    "text" : localeInfo.OFFLINESHOP_OWNER_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 25 + 27,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 25 + 49,

                                    "text" : localeInfo.OFFLINESHOP_BEST_OFFER_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 25 + 72,
                                    "text" : localeInfo.OFFLINESHOP_MIN_RAISE_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 191,
                                    "y" : 145,

                                    "text" : localeInfo.OFFLINESHOP_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 410,
                                    "y" : 145,

                                    "text" : localeInfo.OFFLINESHOP_OFFER_TEXT,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_MY_AUCTION, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name": "OpenAuction",
                    "type": "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name": "BackgroundOpenAuctionPage",
                        #    "type": "image",

                        #    "x": 0, "y": 0,

                        #    "image": "D:/ymir work/ui/offlineshop/openauction/base_image.png",
                        #},

                        {
                            "name" : "OpenAuctionChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (
                                {
                                    "name": "OpenAuction_OwnerName",
                                    "type": "text",

                                    "x" : 235+67, "y" : 100-70,
                                    "text_horizontal_align": "center",
                                    "text": " noname ",
                                },

                                {
                                    "name": "OpenAuction_Duration",
                                    "type": "text",

                                    "x" : 235+67, "y" : 145-91,
                                    "text_horizontal_align": "center",
                                    "text": " noname ",
                                },

                                {
                                    "name": "OpenAuction_BestOffer",
                                    "type": "text",

                                    "x": 235+67, "y": 197-123,
                                    "text_horizontal_align": "center",
                                    "text": " noname ",
                                },

                                {
                                    "name": "OpenAuction_MinRaise",
                                    "type": "text",

                                    "x": 235+67, "y": 243-147,
                                    "text_horizontal_align": "center",
                                    "text": " noname ",
                                },

        ## FLR_CHANGES
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 29,

                                    "text" : localeInfo.OFFLINESHOP_OWNER_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 25 + 27,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 25 + 49,

                                    "text" : localeInfo.OFFLINESHOP_BEST_OFFER_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 165,
                                    "y" : 25 + 72,
                                    "text" : localeInfo.OFFLINESHOP_MIN_RAISE_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 191,
                                    "y" : 145,

                                    "text" : localeInfo.OFFLINESHOP_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 410,
                                    "y" : 145,

                                    "text" : localeInfo.OFFLINESHOP_OFFER_TEXT,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_AUCTION_LIST, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name": "AuctionList",
                    "type": "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        #{
                        #    "name": "BackgroundAuctionListPage",
                        #    "type": "image",

                        #    "x": 0, "y": 0,

                        #    "image": "D:/ymir work/ui/offlineshop/auctionlist/base_image.png",
                        #},

## FLR_CHANGES
                        {
                            "name" : "AuctionListChild",
                            "type" : "thinboard",

                            "x" : 9,
                            "y" : 46,

                            "width"     : 600,
                            "height"     : 507,

                            "children" :
                            (
                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 76,
                                    "y" : 15,

                                    "text" : localeInfo.OFFLINESHOP_OWNER_NAME_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 218,
                                    "y" : 15,

                                    "text" : localeInfo.OFFLINESHOP_BEST_OFFER_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 347,
                                    "y" : 15,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x" : 477,
                                    "y" : 15,

                                    "text" : localeInfo.OFFLINESHOP_OFFER_COUNT_TEXT,
                                },
                            )
                        },
## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                           "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_AUCTION_LIST, "text_horizontal_align":"center", "horizontal_align":"center" },
## END

                    ),
                },

                {
                    "name": "CreateAuction",
                    "type": "window",

                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 28,

                    "children":
                    (
                        {
                            "name" : "RulesBoard",
                            "type" : "thinboard",

                            "x" : 138,
                            "y" : 133,

                            "width"     : 342,
                            "height"     : 165,

                            "children" :
                            (
                                {
                                    "name" : "AuctionRulesText_1",
                                    "type" : "multi_text",

                                    "x": 20,
                                    "y": 20,

                                    "text" : localeInfo.OFFLINESHOP_AUCTION_CREATE_RULES_SET,
                                    "width" : 302,
                                },
                            )
                        },
                        {
                            "name" : "CreateAuctionChild",
                            "type" : "thinboard",

                            "x" : 138,
                            "y" : 306,

                            "width"     : 342,
                            "height"     : 165,

                            "children" :
                            (
                                {
                                    "name" : "CreateAuctionDaysInputContainer",
                                    "type" : "image",

                                    "x" : 130, "y" : 41,

                                    "image" : "D:/ymir work/ui/offlineshop/input_small.tga",

                                    "children" :
                                    (
                                        {
                                            "name": "CreateAuctionDaysInput",
                                            "type": "text",

                                            "text_horizontal_align" : "center",
                                            "text" : "0",
                                            "x": 22, "y": 4,
                                        },
                                    )
                                },

                                {
                                    "name" : "CreateAuctionStartingPriceInputContainer",
                                    "type" : "image",

                                    "x" : 115, "y" : 67,

                                    "image" : "D:/ymir work/ui/offlineshop/input_medium.tga",

                                    "children" :
                                    (
                                        {
                                            "name": "CreateAuctionStartingPriceInput",
                                            "type": "editline",

                                            "width": 170, "height": 17,

                                            "input_limit": 15,
                                            "only_number": 1,
                                            "x": 6, "y": 5,
                                        },
                                    )
                                },

                                {
                                    "name": "CreateAuctionDecreaseDaysButton",
                                    "type": "button",

                                    "x": 182,
                                    "y": 41,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button_scroll_right.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/button_scroll_right_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/button_scroll_right_active.tga",
                                },

                                {
                                    "name" : "CreateAuctionIncreaseDaysButton",
                                    "type" : "button",

                                    "x" : 115,
                                    "y" : 41,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button_scroll_left.tga",
                                    "over_image"     : "D:/ymir work/ui/offlineshop/button_scroll_left_hover.tga",
                                    "down_image"     : "D:/ymir work/ui/offlineshop/button_scroll_left_active.tga",
                                },

                                {
                                    "name" : "CreateAuctionCreateAuctionButton",
                                    "type" : "button",

                                    "x" : 115, "y" : 142-33,

                                    "default_image" : "D:/ymir work/ui/offlineshop/button.tga",
                                    "over_image" : "D:/ymir work/ui/offlineshop/button_hover.tga",
                                    "down_image" : "D:/ymir work/ui/offlineshop/button_active.tga",

                                    "text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CREATE_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x": 148, "y": 27,

                                    "text" : localeInfo.OFFLINESHOP_DAYS_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x": 31, "y": 44,

                                    "text" : localeInfo.OFFLINESHOP_DURATION_TEXT,
                                },

                                {
                                    "name" : "FlrText",
                                    "type" : "text",

                                    "x": 31, "y": 70,

                                    "text" : localeInfo.OFFLINESHOP_STARTING_PRICE_TEXT,
                                },
                            )
                        },

## END
## FLR_CHANGES_BUTTONS
                        {
                            "name" : "my_shop_btn",
                            "type" : "button",

                            "x" : 16, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_shop.tga",

                            "text" : "",
                        },

                        {
                            "name" : "list_of_shops_btn",
                            "type" : "button",

                            "x" : 19*2 + 50, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/list_of_shops.tga",

                            "text" : "",
                        },

                        {
                            "name" : "safebox_btn",
                            "type" : "button",

                            "x" : 19*3 + 50*2, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/safebox.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/safebox.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_offers_btn",
                            "type" : "button",

                            "x" : 19*4 + 50*3, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_offers.tga",

                            "text" : "",
                        },

                        {
                            "name" : "search_btn",
                            "type" : "button",

                            "x" : 19*5 + 50*4, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/search.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/search.tga",

                            "text" : "",
                        },

                        {
                            "name" : "history_btn",
                            "type" : "button",

                            "x" : 19*6 + 50*5, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/history.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/history.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_patterns_btn",
                            "type" : "button",

                            "x" : 19*7 + 50*6, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_patterns.tga",

                            "text" : "",
                        },

                        {
                            "name" : "my_auction_btn",
                            "type" : "button",

                            "x" : 19*8 + 50*7, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/my_auction.tga",

                            "text" : "",
                        },

                        {
                            "name" : "auction_list_btn",
                            "type" : "button",

                            "x" : 19*9 + 50*8, "y" : 14,

                            "default_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "over_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",
                            "down_image" : "D:/ymir work/ui/offlineshop/auction_list.tga",

                            "text" : "",
                        },
## END
## FLR_CHANGES_TEXTS
                        { "name":"TitleName", "type":"text", "x":0, "y":-18, "text" : localeInfo.OFFLINESHOP_TITLE_CREATE_AUCTION, "text_horizontal_align":"center", "horizontal_align":"center" },
## END
                    ),
                },

                {
                    "name": "Menu",
                    "type": "window",

                    "x": 5,
                    "y": WINDOW_HEIGHT-35 - 495 - 23,

                    "width" : WINDOW_WIDTH,
                    "height": 35,
                    "children":
                    (
                        {
                            "name": "MyShopButton",
                            "type": "button",

                            "x": 3, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_MYSHOP,
                        },

                        {
                            "name": "ListOfShopButton",
                            "type": "button",

                            "x": 3 + 50 + 18, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_LIST_OF_SHOPS,
                        },

                        {
                            "name": "ShopSafeboxButton",
                            "type": "button",

                            "x": 3 + 100 + 18*2, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_SAFEBOX,
                        },

                        {
                            "name": "MyOffersPageButton",
                            "type": "button",

                            "x": 3 + 150 + 18*3, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_MY_OFFERS,
                        },

                        {
                            "name": "SearchFilterButton",
                            "type": "button",

                            "x": 3 + 200 + 18*4, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_SEARCH,
                        },

                        {
                            "name": "SearchHistoryButton",
                            "type": "button",

                            "x": 3+ 250 + 18*5, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_SEARCH_HISTORY,
                        },

                        {
                            "name": "MyPatternsButton",
                            "type": "button",

                            "x": 3+ 300 + 18*6, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_MY_PATTERNS,
                        },

                        {
                            "name": "MyAuctionButton",
                            "type": "button",

                            "x": 3 + 350 + 18*7, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_MY_AUCTION,
                        },

                        {
                            "name": "ListOfAuctionsButton",
                            "type": "button",

                            "x": 3 + 400 + 18*8, "y": 7,

                            "width" : 50,
                            "height": 21,
							"tooltip_text": localeInfo.OFFLINESHOP_TITLE_AUCTION_LIST,
                        },
                    ),
                },

                {
                    "name" : "RefreshSymbol",
                    "type" : "ani_image",

                    "x" : 3, "y" : 28,
                    "delay" : 2.5,

                    "images" :
                    (
                        "D:/ymir work/ui/offlineshop/loading/loading_image0.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image1.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image2.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image3.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image4.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image5.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image6.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image7.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image8.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image9.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image10.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image11.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image12.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image13.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image14.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image15.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image16.png",
                        "D:/ymir work/ui/offlineshop/loading/loading_image17.png",
                    )
                },
            ),
        },
    ),
}