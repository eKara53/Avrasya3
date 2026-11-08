import uiScriptLocale
import app

if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
	# 오토 UI
	AUTO_UI_BOARD_WIDTH					= 254
	AUTO_UI_BOARD_HIGHT					= 200
	
	# 액티브 스킬 셋팅
	ACTIVE_SKILL_SETTING_BAR_X			= 14
	ACTIVE_SKILL_SETTING_BAR_Y			= 14
	ACTIVE_SKILL_SETTING_BAR_WIDTH		= 223
	
	CLEAR_BUTTON_X						= 207
	CLEAR_BUTTON_Y						= 1
	
	ACTIVE_SKILL_SETTING_TEXT_X			= 9
	ACTIVE_SKILL_SETTING_TEXT_Y			= 2
	
	ACTIVE_SKILL_SETTING_SLOT_X			= 15
	ACTIVE_SKILL_SETTING_SLOT_Y			= 57
	
	ACTIVE_SKILL_SETTING_SLOT_WIDTH		= 221
	ACTIVE_SKILL_SETTING_SLOT_HEIGHT	= 241
	
	# 액티브 슬롯 인덱스
	SLOT_INDEX_INTERVAL_X				= 38
	SLOT_INDEX_INTERVAL_Y				= 54
	SLOT_INTERVAL_Y						= 29
	
	SLOT_INDEX_WIDTH					= 32
	SLOT_INDEX_HEIGHT					= 32
	
	# 쿨타임
	SLOT_COOL_TIME_BASE_X				= 15
	SLOT_COOL_TIME_INTERVAL_X			= 38
	
	SLOT_COOL_TIME_BASE_Y				= 89
	SLOT_COOL_TIME_INTERVAL_Y			= 54
	SLOT_COOL_TIME_LINE_INTERVAL_Y		= 83
	
	# 에디트 라인
	SLOT_EDIT_LINE_X					= 3
	SLOT_EDIT_LINE_Y					= 3
	SLOT_EDIT_LINE_INPUT_LIMIT			= 4
	SLOT_EDIT_LINE_ONLY_NUMBER			= 1
	SLOT_EDIT_LINE_WIDTH				= 90
	SLOT_EDIT_LINE_HEIGHT				= 20
	
	# 물약 셋팅 바
	POTION_SETTING_BAR_X				= 14
	POTION_SETTING_BAR_Y				= 171
	POTION_SETTING_BAR_WIDTH			= 223
	
	# 물약 셋팅 텍스트
	POTION_SETTING_TEXT_X				= 9
	POTION_SETTING_TEXT_Y				= 2
	
	# 설정 바
	SETTING_BAR_X						= 14
	SETTING_BAR_Y						= 308
	SETTING_BAR_WIDTH					= 223
	
	# 설정 텍스트
	SETTING_AUTO_SETTING_TEXT_X			= 9
	SETTING_AUTO_SETTING_TEXT_Y			= 2
	
	SETTING_AUTO_BAR_X					= 3
	
	SETTING_AUTO_ATTACK_BAR_Y			= 20
	SETTING_AUTO_RANGE_BAR_Y			= 47
	SETTING_AUTO_POTION_BAR_Y			= 74
	SETTING_AUTO_SKILL_BAR_Y			= 101
	SETTING_AUTO_RESTART_BAR_Y			= 128
	
	# 버튼 (자동 공격, 자동 스킬, 자동 물약, 사냥 범위, 자동 부활)
	AUTO_BUTTON_X						= 194
	AUTO_BUTTON_BASE_Y					= 67
	AUTO_BUTTON_ADD_Y					= 27
	
	# 저장 버튼
	AUTO_SAVE_BUTTON_X					= 10
	AUTO_SAVE_BUTTON_Y					= 459
	
	# 시작 버튼
	AUTO_START_BUTTON_X					= 88
	AUTO_START_BUTTON_Y					= 459
	
	# 종료 버튼
	AUTO_END_BUTTON_X					= 166
	AUTO_END_BUTTON_Y					= 459
	
	# 툴팁 버튼
	AUTO_TOOLTIP_BUTTON_X				= 155
	AUTO_TOOLTIP_BUTTON_Y				= 8
	
	window = {
		"name" : "AutoWindow",
		
		"x" : 0,
		"y" : 0,
		
		"style" : ("movable", "float",),
		
		"width"		: AUTO_UI_BOARD_WIDTH,
		"height"	: AUTO_UI_BOARD_HIGHT,
		
		"children" :
		(
			{
				"name" : "board",
				"type" : "board_with_titlebar",
				
				"x" : 0,
				"y" : 0,
				
				"width"		: AUTO_UI_BOARD_WIDTH,
				"height"	: AUTO_UI_BOARD_HIGHT,
				
				"title" : uiScriptLocale.AUTO_TITLE,
				
				"children" :
				(
					## 설정 Bar
					{
						"name" : "HorizontalBar1",
						"type" : "horizontalbar",
						
						"x" : SETTING_BAR_X,
						"y" : 50,
						
						"width" : SETTING_BAR_WIDTH,
					
						"children":
						(
							## 셋팅 Text
							{ "name" : "BaseInfo", "type" : "text", "x" : SETTING_AUTO_SETTING_TEXT_X,	"y" : SETTING_AUTO_SETTING_TEXT_Y,	"text" : uiScriptLocale.AUTO_SETTING, },
							
							# 자동 공격
							{
								"name"	: "attack_text_bar", "type" : "image", "x" : SETTING_AUTO_BAR_X, "y" : SETTING_AUTO_ATTACK_BAR_Y,
								"image" : "d:/ymir work/ui/game/windows/auto_system_text_bar_01.sub",
								"children":
								(
									{ "name" : "BaseInfo", "type" : "text", "x" : 2, "y" : 0, "all_align" : "center", "text" : uiScriptLocale.AUTO_AUTO_ATTACK, },
								),
							},
							# 사냥 범위
							{
								"name"	: "range_text_bar", "type" : "image", "x" : SETTING_AUTO_BAR_X, "y" : SETTING_AUTO_RANGE_BAR_Y,
								"image" : "d:/ymir work/ui/game/windows/auto_system_text_bar_01.sub",
								"children":
								(
									{ "name" : "BaseInfo", "type" : "text", "x" : 2, "y" : 0, "all_align" : "center", "text" : uiScriptLocale.AUTO_AUTO_RANGE, },
								),
							},
						),
					},
					
					## AutoAttack Button
					{
						"name" : "AutoAttackButton",
						"type" : "toggle_button",
						
						"x" : AUTO_BUTTON_X,
						"y" : AUTO_BUTTON_BASE_Y,
						
						"text" : uiScriptLocale.AUTO_OFF,
						
						"default_image"	: "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image"	: "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image"	: "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					
					## AutoRangeButton
					{
						"name" : "AutoRangeButton",
						"type" : "toggle_button",
						
						"x" : AUTO_BUTTON_X,
						"y" : AUTO_BUTTON_BASE_Y + AUTO_BUTTON_ADD_Y,
						
						"text" : uiScriptLocale.AUTO_OFF,
						
						"default_image"	: "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image"	: "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image"	: "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					
					# {
						# "name" : "AutoSaveOnButton",
						# "type" : "button",
						
						# "x" : AUTO_SAVE_BUTTON_X,
						# "y" : AUTO_SAVE_BUTTON_Y,
						
						# "text" : uiScriptLocale.AUTO_SAVE,
						
						# "default_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_01.sub",
						# "over_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_02.sub",
						# "down_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_03.sub",
					# },
					
					## Start Button
					{
						"name" : "AutoStartOnButton",
						"type" : "button",
						
						"x" : AUTO_SAVE_BUTTON_X,
						"y" : 130,
						
						"text" : uiScriptLocale.AUTO_START,
						
						"default_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_01.sub",
						"over_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_02.sub",
						"down_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_03.sub",
					},
					
					## End Button
					{
						"name" : "AutoStartOffButton",
						"type" : "button",
						
						"x" : AUTO_END_BUTTON_X,
						"y" : 130,
						
						"text" : uiScriptLocale.AUTO_END,
						
						"default_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_01.sub",
						"over_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_02.sub",
						"down_image"	: "d:/ymir work/ui/game/windows/auto_system_bottom_button_03.sub",
					},
					
					## __auto_tooltip_button
					{
						"name" : "AutoToolTipButton",
						"type" : "button",
						
						"x" : AUTO_TOOLTIP_BUTTON_X,
						"y" : AUTO_TOOLTIP_BUTTON_Y,
						
						"default_image"	: "d:/ymir work/ui/pattern/q_mark_01.tga",
						"over_image"	: "d:/ymir work/ui/pattern/q_mark_02.tga",
						"down_image"	: "d:/ymir work/ui/pattern/q_mark_01.tga",
					},
					
					## __auto_all_clear_button
					# {
						# "name" : "AutoAllClearButton",
						# "type" : "button",
						
						# "x" : SETTING_BAR_X + CLEAR_BUTTON_X,
						# "y" : SETTING_BAR_Y + CLEAR_BUTTON_Y,
						
						# "default_image"	: "d:/ymir work/ui/game/windows/auto_system_clear_button_01.sub",
						# "over_image"	: "d:/ymir work/ui/game/windows/auto_system_clear_button_02.sub",
						# "down_image"	: "d:/ymir work/ui/game/windows/auto_system_clear_button_03.sub",
					# },
				),
			},
		),
	}
else:
	BOARD_WIDTH = 200
	BOARD_HIGHT = 520
	BAR_WIDTH = 400
	GOLD_COLOR	= 0xFFFEE3AE

	window = {
		"name" : "AutoWindow",

		"x" : 0,
		"y" : 0,

		"style" : ("movable", "float",),

		"width" : BOARD_WIDTH,
		"height" : BOARD_HIGHT,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board_with_titlebar",

				"x" : 0,
				"y" : 0,

				"width" : BOARD_WIDTH,
				"height" : BOARD_HIGHT,
				
				"title" : uiScriptLocale.AUTO_TITLE,
			
				"children" :
				(
					## 액티브 스킬셋팅.Bar
					{
						"name" : "HorizontalBar1",
						"type" : "horizontalbar",
						"x" : 20,
						"y" : 40,
						"width" : BAR_WIDTH / 2 -40,

						"children":
						(
							## 액티브 스킬셋팅 Text
							{
								"name" : "BaseInfo", "type" : "text", "x" : 8, "y" : 2, "text" : uiScriptLocale.AUTO_SKILL_SETTING,
							},
							## AutoSkillClearButton
							{
								"name" : "AutoSkillClearButton",
								"type" : "button",

								"x" : BOARD_WIDTH/2+20,
								"y" : 0,

								"text" : uiScriptLocale.AUTO_CLEAR,

								"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
								"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
								"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
							},
						),
					},
					## 액티브 스킬 셋팅 Slot
					{
						"name" : "Auto_Active_Skill_Slot_Table",
						"type" : "slot",

						"x" : 25,
						"y" : 65,

						"width" : 200,
						"height" : 400,
						"image" : "d:/ymir work/ui/public/Slot_Base.sub",

						"slot" :	(
										## Active SKill
										{"index": 0, "x": 1,"y":  4, "width":32, "height":32},
										{"index": 1, "x":38+3,"y":  4, "width":32, "height":32},
										{"index": 2, "x":75+6,"y":  4, "width":32, "height":32},
										{"index": 3, "x":113+8,"y":  4, "width":32, "height":32},
										{"index": 4, "x": 1,"y": 70, "width":32, "height":32},
										{"index": 5, "x":38+3,"y": 70, "width":32, "height":32},
										{"index": 6, "x":75+6,"y": 70, "width":32, "height":32},
										{"index": 7, "x":113+8,"y": 70, "width":32, "height":32},
										## Position
										{"index": 9, "x": 1,"y":  170, "width":32, "height":32},
										{"index": 10, "x":38+3,"y":  170, "width":32, "height":32},
										{"index": 11, "x":75+6,"y":  170, "width":32, "height":32},
										{"index": 12, "x":113+8,"y":  170, "width":32, "height":32},
										{"index": 13, "x": 1,"y": 240, "width":32, "height":32},
										{"index": 14, "x":38+3,"y": 240, "width":32, "height":32},
										{"index": 15, "x":75+6,"y": 240, "width":32, "height":32},
										{"index": 16, "x":113+8,"y": 240, "width":32, "height":32},
									),

					},
					# editline 추가.
					# Line1
					{
						"name" : "cool_time_Image0", "type" : "image", "x" : 22, "y" : 108,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline0", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image1", "type" : "image", "x" : 22+40, "y" : 108,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline1", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image2", "type" : "image", "x" : 22+80, "y" : 108,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline2", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image3", "type" : "image", "x" : 22+120, "y" : 108,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline3", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					# Line2
					{
						"name" : "cool_time_Image4", "type" : "image", "x" : 22, "y" : 108+66,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline4", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image5", "type" : "image", "x" : 22+40, "y" : 108+66,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline5", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image6", "type" : "image", "x" : 22+80, "y" : 108+66,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline6", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image7", "type" : "image", "x" : 22+120, "y" : 108+66,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline7", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					# Line3
					{
						"name" : "cool_time_Image8", "type" : "image", "x" : 22, "y" : 108+(66*2)+35,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline8", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image9", "type" : "image", "x" : 22+40, "y" : 108+(66*2)+35,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline9", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image10", "type" : "image", "x" : 22+80, "y" : 108+(66*2)+35,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline10", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image11", "type" : "image", "x" : 22+120, "y" : 108+(66*2)+35,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline11", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					
					# Line4
					{
						"name" : "cool_time_Image12", "type" : "image", "x" : 22, "y" : 108+(66*3)+38,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline12", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image13", "type" : "image", "x" : 22+40, "y" : 108+(66*3)+38,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline13", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image14", "type" : "image", "x" : 22+80, "y" : 108+(66*3)+38,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline14", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},
					{
						"name" : "cool_time_Image15", "type" : "image", "x" : 22+120, "y" : 108+(66*3)+38,
						"image" : "d:/ymir work/ui/public/parameter_slot_00.sub",
						"children":
						(
							{
							"name" : "editline15", "type" : "editline","x" : 3, "y" : 3,
							"input_limit" : 4, "only_number" : 1, "width" : 90, "height" : 20,
							},
						),
					},

					
					## 물약 셋팅.Bar
					{
						"name" : "HorizontalBar1",
						"type" : "horizontalbar",
						"x" : 20,
						"y" : 210,
						"width" : BAR_WIDTH / 2 -40,

						"children":
						(
							## 액티브 스킬셋팅 Text
							{
								"name" : "BaseInfo", "type" : "text", "x" : 8, "y" : 2, "text" : uiScriptLocale.AUTO_POSITION_SETTING,
							},				
							## AutoPositionClearButton
							{
								"name" : "AutoPositionClearButton",
								"type" : "button",

								"x" : BOARD_WIDTH/2+20,
								"y" : 0,

								"text" : uiScriptLocale.AUTO_CLEAR,

								"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
								"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
								"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
							},
						),
					},
			
					## 설정 Bar
					{
						"name" : "HorizontalBar1",
						"type" : "horizontalbar",
						"x" : 20,
						"y" : 370,
						"width" : BAR_WIDTH / 2-40,
					
						"children":
						(
							## 셋팅 Text
							{ "name" : "BaseInfo", "type" : "text", "x" : 8, "y" : 2, "text" : uiScriptLocale.AUTO_SETTING, },
							{ "name" : "BaseInfo", "type" : "text", "x" : 1, "y" : 25, "text" : uiScriptLocale.AUTO_AUTO_ATTACK, },
							# { "name" : "BaseInfo", "type" : "text", "x" : 1, "y" : 45, "text" : uiScriptLocale.AUTO_AUTO_SKILL, },
							{ "name" : "BaseInfo", "type" : "text", "x" : 1, "y" : 65, "text" : uiScriptLocale.AUTO_AUTO_POSITION, },
							{ "name" : "BaseInfo", "type" : "text", "x" : 1, "y" : 85, "text" : uiScriptLocale.AUTO_AUTO_RANGE, },
							## AutoAllClearButton
							{
								"name" : "AutoAllClearButton",
								"type" : "button",

								"x" : BOARD_WIDTH/2+20,
								"y" : 0,

								"text" : uiScriptLocale.AUTO_CLEAR,

								"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
								"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
								"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
							},
						),
					},
					## AutoAttackOn Button
					{
						"name" : "AutoAttackOnButton",
						"type" : "button",

						"x" : 90,
						"y" : 320+23+50,

						"text" : uiScriptLocale.AUTO_ON,

						"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					## AutoAttackOff Button
					{
						"name" : "AutoAttackOffButton",
						"type" : "button",

						"x" : 90+45,
						"y" : 320+23+50,

						"text" : uiScriptLocale.AUTO_OFF,

						"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					## AutoSkillOn Button
					{
						"name" : "AutoSkillOnButton",
						"type" : "button",

						"x" : 90,
						"y" : 320+43+50,

						"text" : uiScriptLocale.AUTO_ON,

						"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					## AutoSkillOff Button
					{
						"name" : "AutoSkillOffButton",
						"type" : "button",

						"x" : 90+45,
						"y" : 320+43+50,

						"text" : uiScriptLocale.AUTO_OFF,

						"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					## AutoPositionlOn Button
					{
						"name" : "AutoPositionlOnButton",
						"type" : "button",

						"x" : 90,
						"y" : 320+63+50,

						"text" : uiScriptLocale.AUTO_ON,

						"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					},
					## AutoPositionlOff Button
					{
						"name" : "AutoPositionlOffButton",
						"type" : "button",

						"x" : 90+45,
						"y" : 320+63+50,

						"text" : uiScriptLocale.AUTO_OFF,

						"default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						"over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						"down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					},				
					## AutoRangeOnButton
					 {
						 "name" : "AutoRangeOnButton",
						 "type" : "button",

						 "x" : 90,
						 "y" : 320+83+50,

						 "text" : uiScriptLocale.AUTO_ON,

						 "default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						 "over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						 "down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					 },
					## AutoRangeOffButton
					 {
						 "name" : "AutoRangeOffButton",
						 "type" : "button",

						 "x" : 90+45,
						 "y" : 320+83+50,

						 "text" : uiScriptLocale.AUTO_OFF,

						 "default_image" : "d:/ymir work/ui/public/Small_Button_01.sub",
						 "over_image" : "d:/ymir work/ui/public/Small_Button_02.sub",
						 "down_image" : "d:/ymir work/ui/public/Small_Button_03.sub",
					 },

					## Save Button
					{
						"name" : "AutoSaveOnButton",
						"type" : "button",

						"x" : 10,
						"y" : 420+50+10,

						"text" : uiScriptLocale.AUTO_SAVE,

						"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
						"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
						"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					},				
					## Start Button
					{
						"name" : "AutoStartOnButton",
						"type" : "button",

						"x" : 70,
						"y" : 420+50+10,

						"text" : uiScriptLocale.AUTO_START,

						"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
						"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
						"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					},
					## End Button
					{
						"name" : "AutoStartOffButton",
						"type" : "button",

						"x" : 130,
						"y" : 420+50+10,

						"text" : uiScriptLocale.AUTO_END,

						"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
						"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
						"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
					},
					## AutoToolTip Button
					{
						"name" : "AutoToolTIpButton",
						"type" : "button",

						"x" : 155,
						"y" : 8,

						"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
						"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
						"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
					},					
				),
			},
		),
	}
