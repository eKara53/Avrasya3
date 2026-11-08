import localeInfo

window = {
	"name" : "OfflineShopInputDialog",
	
	"x" : 0,
	"y" : 0,
	
	"style" : ("movable", "float",),
	
	"width" : 300,
	"height" : 90,
	
	"children" :
	(
		# board
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 300,
			"height" : 90,
			
			"title" : localeInfo.OFFLINESHOP_INPUT_DIALOG_TITLE,
			
			"children":
			(	

				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : -3,
					"y" : 35,
					
					"width" : 235,
					"height" : 15,
					
					"horizontal_align" : "center",
					
					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "editline",

							"x" : 1,
							"y" : 1,

							"width" : 235,
							"height" : 15,
							"input_limit" : 32,
						},
					),
				},

				{
					"name" : "AgreeButton",
					"type" : "button",
					
					"x" : 79,
					"y" : 55,
					
					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					
					"text" : localeInfo.OFFLINESHOP_ACCEPT,
				},
				
				{
					"name" : "CancelButton",
					"type" : "button",
					
					"x" : 156,
					"y" : 55,
					
					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					
					"text" : localeInfo.OFFLINESHOP_CANCEL,
				},
			),
		},
	),
}