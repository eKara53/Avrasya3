# DUMPED FROM LIVE COMPILE: uiItemShop.py (len=35571)
import ui
import uiToolTip
import uiCommon
import constInfo
import localeInfo
import wndMgr
import dbg
import os
import snd
import chat
import chr
import player
import item
import net
import app
import background
import chrmgr
import time

CATEGORY_COUNT = 3

FAKE_CATEGORY_DATA = {
    0 : {
        "categoryName" : "Genel",
        "subCategoryNameList" : ["Efsunlar", "Tüketilebilir Nesneler", "Premium Nesneler", "Tanrýlar"],
        "categoryColor" : "fosfor",
        "subcategoryColor" : ["turquiose","green","orange","orange"],
    },
    1 : {
        "categoryName" : "Hizmet",
        "subCategoryNameList" : ["Pot","Sular", "Þebnemler"],
        "categoryColor" : "yellow",
        "subcategoryColor" : ["orange","green","green"],
    },
    2 : {
        "categoryName" : "Arýndýrma",
        "subCategoryNameList" : ["EP Kuponlarý","Yardýmcý Nesneler"],
        "categoryColor" : "pink",
        "subcategoryColor" : ["lightblue","red"],
    },
    3 : {
        "categoryName" : "Stil",
        "subCategoryNameList" : ["Eþyalar","Saçlar"],
        "categoryColor" : "lightblue",
        "subcategoryColor" : ["red","red","turquiose"],
    },
}

ITEM_FLAG_STACKABLE = (1 << 2)
BLEND_AFFECT_UNLIMITED_DURATION = 100 * 60 * 60
def toLower(string):
	alphabetList = {
		'Ý' : 'i',
		'I' : 'ý',
		'Ö' : 'ö',
		'Ü' : 'ü',
		'Þ' : 'þ',
		'Ç' : 'ç',
		'Ð' : 'ð',
	}

	for (key, item) in alphabetList.iteritems():
		string = string.replace(key, item)

	return string.lower()

###################################################################################################

###################################################################################################
# Category Board
class CategoryButton(ui.Window):
	ARROWIMAGE_FILE_NAME = {
		"SELECT" : "d:/ymir work/ui/privatesearch/private_next_btn_02.sub",
		"UNSELECT" : "d:/ymir work/ui/privatesearch/private_next_btn_01.sub",
	}

	def __init__(self, parent, x, y, isSubItem = False):
		ui.Window.__init__(self)
		self.getParent = parent
		self.key = None
		self.isSubItem = isSubItem

		self.SetParent(parent)
		self.AddFlag("float")
		self.SetSize(96, 26)
		self.SetPosition(x, y)
		
		categoryButton = ui.RadioButton()
		categoryButton.SetParent(self)
		categoryButton.AddFlag("not_pick")
		
		if (isSubItem):
			categoryButton.SetUpVisual("d:/ymir work/ui/itemshop/subbutton.png")
			categoryButton.SetOverVisual("d:/ymir work/ui/itemshop/subbutton.png")
			categoryButton.SetDownVisual("d:/ymir work/ui/itemshop/subbuttonbasili.png")
		else:
			categoryButton.SetUpVisual("d:/ymir work/ui/itemshop/norm.png")
			categoryButton.SetOverVisual("d:/ymir work/ui/itemshop/norm1.png")
			categoryButton.SetDownVisual("d:/ymir work/ui/itemshop/norm1.png")

		categoryButton.SetPosition(0, 0)
		categoryButton.SetEvent(ui.__mem_func__(self.OnMouseLeftButtonDown))
		categoryButton.Show()
		self.categoryButton = categoryButton

		image = ui.ImageBox()
		image.SetParent(self)
		image.AddFlag("not_pick")
		image.LoadImage(self.ARROWIMAGE_FILE_NAME["UNSELECT"])
		image.SetPosition(6, 5)
		image.Hide()
		self.image = image

		name = ui.TextLine()
		name.SetParent(self)
		name.SetPosition(25, 5)
		name.Show()
		self.name = name

	def IsSubItem(self):
		return self.isSubItem
	
	def SetFontsName(self,fontname):
		self.name.SetFontName(str(fontname))
	
	def SetColor(self, color):
		self.name.SetPackedFontColor(0xffFFFFFF)
		pass
		if color == "red":
			self.name.SetPackedFontColor(0xffFF2B00)
		elif color == "purple":
			self.name.SetPackedFontColor(0xffFF00F0)
		elif color == "yellow":
			self.name.SetPackedFontColor(0xffFFE400)
		elif color == "orange":
			self.name.SetPackedFontColor(0xffFFB200)
		elif color == "blue":
			self.name.SetPackedFontColor(0xff0042FF)
		elif color == "turquiose":
			self.name.SetPackedFontColor(0xff00ECFF)
		elif color == "green":
			self.name.SetPackedFontColor(0xff00FF08)
		elif color == "brown":
			self.name.SetPackedFontColor(0xffA45C00)
		elif color == "white":
			self.name.SetPackedFontColor(0xffFFFFFF)
		elif color == "fosfor":
			self.name.SetPackedFontColor(0xffD4FF00)
		elif color == "lightblue":
			self.name.SetPackedFontColor(0xff5299FF)
		elif color == "pink":
			self.name.SetPackedFontColor(0xffFF52E7)
		else:
			self.name.SetPackedFontColor(0xffFFFFFF)

	def SetName(self, name):
		if self.isSubItem:
			self.name.SetPosition(22, 5)
		else:
			self.name.SetPosition(22, 5)

		self.name.SetText(name)

	def SetKey(self, key):
		self.key = key
		
	def GetKey(self):
		return self.key

	def IsSameKey(self, key):
		return self.key == key

	def Select(self):
		self.categoryButton.Down()
		self.image.LoadImage(self.ARROWIMAGE_FILE_NAME["SELECT"])

	def UnSelect(self):
		self.categoryButton.SetUp()
		self.image.LoadImage(self.ARROWIMAGE_FILE_NAME["UNSELECT"])

	def OnMouseLeftButtonDown(self):
		if not self.isSubItem:
			self.getParent.OnSelectItem(self)
		else:
			self.getParent.OnSubSelectItem(self)

class CategoryListItem(CategoryButton):
	IMAGE_FILE_NAME = {
		"OPEN" : "d:/ymir work/ui/game/windows/btn_plus_dis.sub",
		"CLOSE" : "d:/ymir work/ui/game/windows/btn_minus_dis.sub",
	}

	def __init__(self, parent, x, y):
		self.getParent = parent
		self.isOpen = False
		self.subCategoryList = []

		CategoryButton.__init__(self, parent, x, y)

	def AppendSubCategory(self, key, name, color):
		(x, y) = self.GetLocalPosition()
		yPos = len(self.subCategoryList) * 30 + y + 30
		categoryButton = CategoryButton(self.getParent, 30, yPos, True)
		categoryButton.SetKey(key)
		categoryButton.SetName(name)
		# categoryButton.SetColor(color)
		self.subCategoryList.append(categoryButton)
		return categoryButton

	def GetCategoryList(self):
		return self.subCategoryList

	def FindCategory(self, key):
		list = filter(lambda argCategory, argKey=key: argCategory.IsSameKey(argKey), self.subCategoryList)
		if list:
			return list[0]

		return None

	def IsOpen(self):
		return self.isOpen

	def Open(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
		self.categoryButton.Down()
		self.categoryButton.Disable()
		self.isOpen = True

	def Close(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
		self.image.SetPosition(6, 5)
		self.categoryButton.SetUp()
		self.categoryButton.Enable()
		self.isOpen = False
		
		map(ui.Window.Hide, self.subCategoryList)

	def Select(self):
		self.Open()
		self.getParent.OnRefreshList()

	def UnSelect(self):
		self.Close()
		self.getParent.OnRefreshList()

class CategoryBoard(ui.Window):
	def __init__(self, parentFirst, parentSecond, scrollBar):
		ui.Window.__init__(self)
		
		self.SetParent(parentSecond)
		self.getParent = parentFirst

		self.scrollBar = scrollBar
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.selectCategory = None
		self.selectSubCategory = None
		self.categoryListItems = []
		self.showingItemList = []
		self.startLine = 0

	def Destroy(self):
		self.selectCategory = None
		self.selectSubCategory = None
		self.categoryListItems = []
		self.showingItemList = []

	def OnScroll(self):
		return
		scrollLineCount = len(self.showingItemList) - 13
		startLine = int(scrollLineCount * self.scrollBar.GetPos())

		if startLine != self.startLine:
			self.startLine = startLine
			self.__LocateMember()

	def OnSelectItem(self, item):
		if self.selectCategory:
			self.selectCategory.UnSelect()
			self.getParent.ClearItemBoard()

			if item == self.selectCategory:
				item = None

		self.selectCategory = item

		if self.selectCategory:
			self.selectCategory.Select()
			
			self.OnSubSelectItem(self.selectCategory.GetCategoryList()[0])

		self.scrollBar.SetPos(0.0)

		buttonList = filter(lambda argSelf: argSelf.IsOpen(), self.categoryListItems)
		if buttonList:
			(x, y) = buttonList[0].GetLocalPosition()

			if y >= 385:
				y += 24

			startPos = 1.0 / (385.0 / float(y - 24))
			self.scrollBar.SetPos(startPos)
	
	def OnSubSelectItem(self, item):
		if self.selectSubCategory:
			if item != self.selectSubCategory:
				self.selectSubCategory.UnSelect()
				
		self.selectSubCategory = item
		
		if self.selectSubCategory:
			self.selectSubCategory.Select()

			self.getParent.ChangeCategory(self.selectCategory.GetKey(), self.selectSubCategory.GetKey())

	def __LocateMember(self):
		if self.showingItemList:
			stepSize = 1.0 / (len(self.showingItemList) - CATEGORY_COUNT)
			self.scrollBar.SetScrollStep(stepSize)

			if stepSize <= 0.8:
				stepSize += 0.2

			self.scrollBar.SetMiddleBarSize(stepSize)

		self.scrollBar.Show()

		#####

		yPos = 25
		heightLimit = self.GetHeight() - 30

		map(ui.Window.Hide, self.showingItemList)

		for item in self.showingItemList[self.startLine:]:
			xPos = 10
			if item.IsSubItem():
				xPos = 30
			item.SetPosition(xPos, yPos)
			item.SetTop()
			item.Show()

			yPos += 30
			if yPos > heightLimit:
				break
				
	def OnRefreshList(self):
		self.showingItemList = []
		
		for items in self.categoryListItems:
			self.showingItemList.append(items)
			subItems = items.GetCategoryList()

			if items.IsOpen() and subItems:
				for item in subItems:
					self.showingItemList.append(item)

		self.__LocateMember()
	
	def firstOpenBoard(self):
		self.OnSelectItem(self.categoryListItems[0])
		self.OnSubSelectItem(self.categoryListItems[0].GetCategoryList()[0])

	def RefreshProcess(self):
		self.categoryListItems = []
		for i in xrange(len(FAKE_CATEGORY_DATA)):
				categoryData = FAKE_CATEGORY_DATA[i]
				category = CategoryListItem(self, 10, 25 + i * 30)
				category.SetKey(i)
				category.SetName(categoryData["categoryName"])
				# category.SetFontsName("Tahoma:15")
				# category.SetColor(categoryData["categoryColor"])
				category.Close()
				category.Show()

				for j in xrange(len(categoryData["subCategoryNameList"])):
					category.AppendSubCategory(j, categoryData["subCategoryNameList"][j],categoryData["subcategoryColor"][j])

				self.categoryListItems.append(category)
		
		self.OnRefreshList()


	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()
			
			
# Category Board
###################################################################################################

###################################################################################################
# Item Stackable Buy Dialog
class ItemStackableBuyDialog(ui.BoardWithTitleBar):

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		
		self.getParent = None
		self.itemID = 0
		self.itemVnum = 0
		self.itemPrice = -1
		self.maxCount = 0
		self.coins = 0
		self.mark = 0
		
		self.__LoadDialog()
	
	def __LoadDialog(self):
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetSize(200, 160)
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		countTextFirst = ui.TextLine()
		countTextFirst.SetParent(self)
		countTextFirst.SetFontName("Tahoma:14")
		countTextFirst.SetText("Alýnacak toplam miktar: 1")
		countTextFirst.SetPosition(self.GetWidth() / 2, 40)
		countTextFirst.SetHorizontalAlignCenter()
		countTextFirst.Show()
		self.countTextFirst = countTextFirst
		
		countArrowUp = ui.Button()
		countArrowUp.SetParent(self)
		countArrowUp.SetPosition(self.GetWidth() / 2 - 44, self.GetHeight() / 2 - 9)
		countArrowUp.SetUpVisual("d:/ymir work/ui/itemshop/arrow_up_default.sub")
		countArrowUp.SetOverVisual("d:/ymir work/ui/itemshop/arrow_up_over.sub")
		countArrowUp.SetDownVisual("d:/ymir work/ui/itemshop/arrow_up_down.sub")
		countArrowUp.SetEvent(ui.__mem_func__(self.__ArrowButton), 0)
		countArrowUp.Show()
		self.countArrowUp = countArrowUp

		countArrowDown = ui.Button()
		countArrowDown.SetParent(self)
		countArrowDown.SetPosition(self.GetWidth() / 2 - 44, self.GetHeight() / 2 + 3)
		countArrowDown.SetUpVisual("d:/ymir work/ui/itemshop/arrow_down_default.sub")
		countArrowDown.SetOverVisual("d:/ymir work/ui/itemshop/arrow_down_over.sub")
		countArrowDown.SetDownVisual("d:/ymir work/ui/itemshop/arrow_down_down.sub")
		countArrowDown.SetEvent(ui.__mem_func__(self.__ArrowButton), 1)
		countArrowDown.Show()
		self.countArrowDown = countArrowDown

		countSlotBar = ui.SlotBar()
		countSlotBar.SetParent(self)
		countSlotBar.SetSize(50, 18)
		countSlotBar.SetPosition(self.GetWidth() / 2 - 30, self.GetHeight() / 2 - 10)
		countSlotBar.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)
		countSlotBar.Show()
		self.countSlotBar = countSlotBar

		countEditline = ui.EditLine()
		countEditline.SetParent(countSlotBar)
		countEditline.SetSize(24, 18)
		countEditline.SetMax(3)
		countEditline.SetPosition(3, 2)
		countEditline.SetNumberMode()
		countEditline.SetText("1")
		countEditline.SetFocus()
		countEditline.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		countEditline.OnIMEReturn = ui.__mem_func__(self.__OnValueReturn)
		countEditline.Show()
		self.countEditline = countEditline
		
		countTextSecond = ui.TextLine()
		countTextSecond.SetParent(countSlotBar)
		countTextSecond.SetFontName("Tahoma:14")
		countTextSecond.SetText("/0")
		countTextSecond.SetPosition(55, 0)
		countTextSecond.Show()
		self.countTextSecond = countTextSecond
		
		ammoutText = ui.TextLine()
		ammoutText.SetParent(self)
		ammoutText.SetFontName("Tahoma:14")
		ammoutText.SetText("Tutar : 0 Ep")
		ammoutText.SetPosition(self.GetWidth() / 2, self.GetHeight() / 2 + 15)
		ammoutText.SetHorizontalAlignCenter()
		ammoutText.Show()
		self.ammoutText = ammoutText
		
		acceptButton = ui.Button()
		acceptButton.SetParent(self)
		acceptButton.SetPosition(self.GetWidth() / 2 - 70, self.GetHeight() - 35)
		acceptButton.SetUpVisual("d:/ymir work/ui/Public/acceptbutton00.sub")
		acceptButton.SetOverVisual("d:/ymir work/ui/Public/acceptbutton01.sub")
		acceptButton.SetDownVisual("d:/ymir work/ui/Public/acceptbutton02.sub")
		acceptButton.SetToolTipText("Satýn Al")
		acceptButton.SetEvent(ui.__mem_func__(self.acceptButtonEvent))
		acceptButton.Show()
		self.acceptButton = acceptButton
		
		cancelButton = ui.Button()
		cancelButton.SetParent(self)
		cancelButton.SetPosition(self.GetWidth() / 2 + 8, self.GetHeight() - 35)
		cancelButton.SetUpVisual("d:/ymir work/ui/Public/canclebutton00.sub")
		cancelButton.SetOverVisual("d:/ymir work/ui/Public/canclebutton01.sub")
		cancelButton.SetDownVisual("d:/ymir work/ui/Public/canclebutton02.sub")
		cancelButton.SetToolTipText("Ýptal")
		cancelButton.SetEvent(ui.__mem_func__(self.Close))
		cancelButton.Show()
		self.cancelButton = cancelButton
	
	def SetParent2(self, parent):
		self.getParent = parent
	
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		ui.BoardWithTitleBar.Show(self)

	def Close(self):
		self.itemPrice = -1
		self.maxCount = 0
		self.countEditline.SetText("1")
		self.countTextFirst.SetText("Alýnacak toplam miktar: 1")
		self.Hide()

	def acceptButtonEvent(self):
		itemName = self.titleName.GetText()
		itemCount = self.countEditline.GetText()
		price = self.itemPrice * int(itemCount)

		if self.getParent:
			self.getParent.buyQuestionDialog(self.itemID, self.itemVnum, itemName, int(itemCount), price)
		
		self.Close()

	def __ClickValueEditLine(self):
		self.countEditline.SetFocus()
	
	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.countEditline)

		text = self.countEditline.GetText()

		count = 1
		if text and text.isdigit():
			try:
				count = int(text)
				
				if count <= 0:
					count = 1

				if count > self.maxCount:
					count = self.maxCount
					self.countEditline.SetText("%d" % count)

			except ValueError:
				pass

		self.countTextFirst.SetText("Alýnacak toplam miktar: %d" % count)

		price = self.itemPrice * count
		self.SetItemPrice(price)

	def __OnValueReturn(self):
		self.countEditline.KillFocus()

		text = self.countEditline.GetText()

		count = 1
		if text and text.isdigit():
			try:
				count = int(text)

				if count <= 0:
					count = 1

			except ValueError:
				count = 1

		self.countEditline.SetText("%d" % count)
		self.countTextFirst.SetText("Alýnacak toplam miktar: %d" % count)
		price = self.itemPrice * count
		self.SetItemPrice(price)

	def __ArrowButton(self, type):
		self.countEditline.KillFocus()

		text = self.countEditline.GetText()

		count = 0

		if not text or not text.isdigit():
			count = 1
		else:
			count = int(text)

		if type == 0:
			count += 1
		else:
			count -= 1

		if count <= 0:
			count = 1
		elif count >= self.maxCount:
			count = self.maxCount

		self.countEditline.SetText("%d" % count)
		self.countTextFirst.SetText("Alýnacak toplam miktar: %d" % count)
		price = self.itemPrice * count
		self.SetItemPrice(price)

	def SetItemPrice(self, price):
		text = ("Tutar : %d EP" % (price))
		self.ammoutText.SetText(text)

	def SetCountText(self, price, playerTotalCoin):
		self.itemPrice = price
		self.maxCount = playerTotalCoin / price
		self.countTextSecond.SetText("/%d" % self.maxCount)

		if self.maxCount > 200:
			self.maxCount = 200

		self.SetItemPrice(price)

	def SetItem(self, itemID, itemVnum):
		self.itemID = itemID
		self.itemVnum = itemVnum

# Item Stackable Buy Dialog
###################################################################################################

###################################################################################################
# Item Shop Window
class ItemShopWindow(ui.ScriptWindow):
	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)
		
		self.searchEditline = None
		self.searchButton = None
		self.boardFirst = None
		self.scrollBar = None
		self.prevButton = None
		self.pageText = None
		self.nextButton = None
		self.popup = None

		self.categoryGroupBoard = None
		self.wndItemList = {}
		self.itemList = []
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		
		self.itemStackalbeBuyDialog = None
		
		self.pageMaxNum = 0
		self.pageNum = 0
		self.itemShopTime = 0
		self.coinxd = int(player.GetDragonCoin())
		
		# self.itemToolTip = None
		self.questionDialog = None
		self.interface = interface

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		if self.categoryGroupBoard:
			self.categoryGroupBoard.Destroy()
		self.categoryGroupBoard = None
		self.itemStackalbeBuyDialog = None
		self.questionDialog = None
		self.interface = None

	def LoadWindow(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/item_shop.py")
		except:
			import exception
			exception.Abort("ItemShopWindow.LoadDialog.LoadObject")
		try:
			self.GetChild("TitleBar").SetCloseEvent(self.Close)

			self.searchEditline = self.GetChild("search_editline")
			self.searchButton = self.GetChild("search_button")

			self.boardFirst = self.GetChild("board_first")
			self.scrollBar = self.GetChild("ScrollBar")

			self.prevButton = self.GetChild("prev_button")
			self.pageText = self.GetChild("page_text")
			self.nextButton = self.GetChild("next_button")

			self.dragoncoin = self.GetChild("dragon_coin_text")
			self.coinBuyButton = self.GetChild("coin_buy_button")
			self.coinEpButton = self.GetChild("coin_ep_button")
			
			self.hapyHourButton = self.GetChild("logo")

			# self.hapyHourButton.Hide()

			for i in xrange(1, 10):
				number = "0%d" % i # number = "0%d" % i if i < 10 else "%d" % i (python 2.7 version)

				if i >= 10:
					number = "%d" % i

				wndItemSlot = self.GetChild("itemSlot_%s" % number)
				
				# wndItemSlot.ArrangeSlot(0, 1, 3, 32, 64, 0, 0)
				wndItemSlot.SetSlotBaseImage(str(self.GetImage(FAKE_CATEGORY_DATA[constInfo.LAST_CATEG_ID]["subcategoryColor"][constInfo.LAST_SUBCATEG_ID])), 1.0, 1.0, 1.0, 1.0)
				# self.ItemSlot.SetSlotBaseImage("")
				wndItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				wndItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
				wndItemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.selectItemSlotEvent))
				wndItemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.selectItemSlotEvent))

				itemName = self.GetChild("itemName_%s" % number)
				itemName.SetMax(15)
				itemName.SetLimitWidth(95)
				itemName.SetMultiLine()
				itemName.SetFontName("Tahoma:13")
				itemName.SetPackedFontColor(0xFFFEE3AE)
				# self.itemName = itemName
				itemOldPrice = self.GetChild("itemOldPrice_%s" % number)
				itemOldPrice.SetMax(15)
				itemOldPrice.SetLimitWidth(95)
				itemOldPrice.SetMultiLine()
				itemOldPrice.SetPackedFontColor(0xff47e4d7)
				itemOldPrice.SetFontName("Tahoma:11")

				itemSelectAttrAndStoneButton = self.GetChild("itemSelectAttrAndStoneButton_%s" % number)
				itemSelectAttrAndStoneButton.Hide()
				
				itemBuyButton = self.GetChild("itemBuyButton_%s" % number)
				itemBuyButton.ButtonText.SetFontName("Tahoma:13")
				itemBuyButton.Disable()
				#itemBuyButton.ButtonText.SetFontColor(1.00,0.69,0.29)
				
				self.wndItemList[i] = (wndItemSlot, itemName, itemOldPrice, itemSelectAttrAndStoneButton, itemBuyButton)
		except:
			import exception
			exception.Abort("ItemShopWindow.LoadDialog.BindObject")
		
		self.searchEditline.OnIMEReturn = ui.__mem_func__(self.searchButtonEvent)
		self.searchButton.SetEvent(ui.__mem_func__(self.searchButtonEvent))
		self.prevButton.SetEvent(ui.__mem_func__(self.prevButtonEvent))
		self.nextButton.SetEvent(ui.__mem_func__(self.nextButtonEvent))
		self.coinBuyButton.SetEvent(ui.__mem_func__(self.coinButtonEvent))
		self.coinEpButton.SetEvent(ui.__mem_func__(self.coinEpEvent))

		if self.categoryGroupBoard:
			self.categoryGroupBoard.Destroy()
		categoryGroupBoard = CategoryBoard(self, self.boardFirst, self.scrollBar)
		categoryGroupBoard.SetSize(self.boardFirst.GetWidth() - 25, self.boardFirst.GetHeight())
		categoryGroupBoard.Show()
		self.categoryGroupBoard = categoryGroupBoard

		itemStackalbeBuyDialog = ItemStackableBuyDialog()
		itemStackalbeBuyDialog.SetParent2(self)
		itemStackalbeBuyDialog.SetCenterPosition()
		itemStackalbeBuyDialog.Hide()
		self.itemStackalbeBuyDialog = itemStackalbeBuyDialog

		self.questionDialog = uiCommon.QuestionDialog2()
		self.questionDialog.SetAcceptEvent(lambda arg = True: self.QuestionDialogEvent(arg))
		self.questionDialog.SetCancelEvent(lambda arg = False: self.QuestionDialogEvent(arg))
		self.questionDialog.Hide()

		self.coinBuyButton.ButtonText.SetPackedFontColor(0xFFFEE3AE)
		self.coinEpButton.ButtonText.SetPackedFontColor(0xFFFEE3AE)

		self.dragoncoin.SetText("%d EP" % (self.coinxd))

	def GetImage(self,color):
		return "d:/ymir work/ui/slotimage/base_image_2.png"
		if color == "red":
			return "d:/ymir work/ui/slotimage/base_image_red_2.png"
		elif color == "purple":
			return "d:/ymir work/ui/slotimage/base_image_purple_2.png"
		elif color == "yellow":
			return "d:/ymir work/ui/slotimage/base_image_yellow_2.png"
		elif color == "orange":
			return "d:/ymir work/ui/slotimage/base_image_orange_2.png"
		elif color == "blue":
			return "d:/ymir work/ui/slotimage/base_image_blue_2.png"
		elif color == "turquiose":
			return "d:/ymir work/ui/slotimage/base_image_turquiose_2.png"
		elif color == "green":
			return "d:/ymir work/ui/slotimage/base_image_green_2.png"
		elif color == "brown":
			return "d:/ymir work/ui/slotimage/base_image_brown_2.png"
		elif color == "white":
			return "d:/ymir work/ui/slotimage/base_image_white_2.png"
		elif color == "fosfor":
			return "d:/ymir work/ui/slotimage/base_image_fosfor_2.png"
		elif color == "lightblue":
			return "d:/ymir work/ui/slotimage/base_image_lightblue_2.png"
		elif color == "pink":
			return "d:/ymir work/ui/slotimage/base_image_pink_2.png"
		else:
			return "d:/ymir work/ui/slotimage/base_image_2.png"

	def OnScrollWheel(self, nLen):
		if self.scrollBar:
			if int(nLen) < 0:
				self.scrollBar.OnDown()
			else:
				self.scrollBar.OnUp()
		
	def SetItemToolTip(self, itemToolTip):
		self.itemToolTip = itemToolTip

	def Open(self):
		self.max_pos_x = wndMgr.GetScreenWidth() - self.GetWidth()
		self.max_pos_y = wndMgr.GetScreenHeight() - self.GetHeight()
		self.SetCenterPosition()
		self.categoryGroupBoard.RefreshProcess()
		self.categoryGroupBoard.firstOpenBoard()
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Close(self):
		ui.ScriptWindow.Hide(self)
		if self.itemStackalbeBuyDialog:
			self.itemStackalbeBuyDialog.Close()
		
		if self.questionDialog:
			self.questionDialog.Close()
		
		return True

	def ClearItemBoard(self):
		for i in xrange(1, 10):
			(wndItemSlot, itemName, itemOldPrice,itemSelectAttrAndStoneButton, itemBuyButton) = self.wndItemList[i]
			wndItemSlot.ClearSlot(i)
			wndItemSlot.RefreshSlot()

			itemName.SetText("")
			itemOldPrice.SetText("")
			itemSelectAttrAndStoneButton.Hide()
			itemBuyButton.SetText("")
			itemBuyButton.Disable()

		self.prevButton.Hide()
		self.nextButton.Hide()
		self.pageText.SetText("0/0")

	def ChangeCategory(self, categoryID, subCategoryID):
		self.ClearItemBoard()

		if not constInfo.ITEM_DATA.has_key(categoryID):
			return

		category = constInfo.ITEM_DATA[categoryID]

		if not category.has_key(subCategoryID):
			return
		
		constInfo.LAST_CATEG_ID = categoryID
		constInfo.LAST_SUBCATEG_ID = subCategoryID

		category = category[subCategoryID]
		self.itemList = [item for item in category]
		self.pageMaxNum = len(self.itemList) / 9
		
		if len(self.itemList) % 9 > 0:
			self.pageMaxNum += 1
		
		self.pageNum = 0

		self.RefreshProcess()
	
	def prevButtonEvent(self):
		if self.pageNum - 1 < 0:
			return

		self.pageNum -= 1
		self.RefreshProcess()

	def nextButtonEvent(self):
		if self.pageNum + 1 >= self.pageMaxNum:
			return

		self.pageNum += 1
		self.RefreshProcess()

	def __PopupMessage(self, text):
		if self.popup:
			return

		popup = uiCommon.PopupDialog()
		popup.SetText(text)
		popup.SetWidth(popup.GetTextSize()[0] + 30)
		popup.SetAcceptEvent(self.__OnClosePopupDialog)
		popup.Open()
		self.popup = popup

	def __OnClosePopupDialog(self):
		self.popup = None

	def OnUpdate(self):
		self.dragoncoin.SetText("%d EP" % (self.coinxd))

	def UpdateDragonCoin(self, coin):
		self.coinxd = int(coin)
		self.dragoncoin.SetText("%d EP" % (int(coin)))

	def coinButtonEvent(self):
		#time limit
		if time.clock() > self.itemShopTime:
			self.coinxd = int(player.GetDragonCoin())
			self.dragoncoin.SetText("%d EP" % (int(self.coinxd)))
			self.itemShopTime = time.clock() + 3
		else:
			chat.AppendChat(1," Bu kadar hýzlý yenilenemez. ")

	def coinEpEvent(self):
		net.SendChatPacket("/ep_yukleyecem")

	def GetColor(self,color):
		return 0xffFFFFFF
		if color == "red":
			return 0xffFF2B00
		elif color == "purple":
			return 0xffFF00F0
		elif color == "yellow":
			return 0xffFFE400
		elif color == "orange":
			return 0xffFFB200
		elif color == "blue":
			return 0xff0042FF
		elif color == "turquiose":
			return 0xff00ECFF
		elif color == "green":
			return 0xff00FF08
		elif color == "brown":
			return 0xffA45C00
		elif color == "white":
			return 0xffFFFFFF
		elif color == "fosfor":
			return 0xffD4FF00
		elif color == "lightblue":
			return 0xff5299FF
		elif color == "pink":
			return 0xffFF52E7
		else:
			return 0xffFFFFFF
	
	def RefreshProcess(self):
		self.ClearItemBoard()

		self.pageText.SetText("%d/%d" % (self.pageNum + 1, self.pageMaxNum))
		if self.pageNum == 0:
			self.prevButton.Hide()
		else:
			self.prevButton.Show()
			
		if self.pageNum + 1 == self.pageMaxNum:
			self.nextButton.Hide()
		else:
			self.nextButton.Show()

		for i in xrange(1, 10):
			itemPos = (self.pageNum * 9) + (i - 1)
			
			if len(self.itemList) <= itemPos:
				return
			
			(empty, itemID, itemVnum, itemPrice,itemPriceOld, itemCount, itemSocketZero, itemMark, atype0,avalue0,atype1,avalue1,atype2,avalue2,atype3,avalue3,atype4,avalue4,atype5,avalue5,atype6,avalue6,socket0,socket1,socket2,socket3) = self.itemList[itemPos]
			(wndItemSlot, itemName, itemOldPrice,itemSelectAttrAndStoneButton, itemBuyButton) = self.wndItemList[i]

			wndItemSlot.SetSlotBaseImage(str(self.GetImage(FAKE_CATEGORY_DATA[constInfo.LAST_CATEG_ID]["subcategoryColor"][constInfo.LAST_SUBCATEG_ID])), 1.0, 1.0, 1.0, 1.0)
			
			wndItemSlot.SetItemSlot(i, itemVnum, itemCount)
			wndItemSlot.RefreshSlot()
			
			item.SelectItem(itemVnum)
			
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemVnum >= 53000 and itemVnum <= 53030:
				itemValue = item.GetValue(1)
			elif itemVnum >= 71124 and itemVnum <= 71128:
				itemValue = item.GetValue(1)
			elif itemVnum >= 71248 and itemVnum <= 71260 or itemVnum == 88932 or itemVnum == 71256:
				itemValue = item.GetValue(1)
			else:
				itemValue = item.GetValue(0)
			itemHair = item.GetValue(3)
			(affectTypem, affectValuem) = item.GetAffect(0)
			race = player.GetRace()
			job = chr.RaceToJob(race)
			sex = chr.RaceToSex(race)
			MALE = 1
			FEMALE = 0
			
			isItemSelectAttr = False
			
			if itemType == item.ITEM_TYPE_WEAPON and not itemVnum == 8000:
				isItemSelectAttr = True
			if itemType == item.ITEM_TYPE_ARMOR:
				isItemSelectAttr = True
			
			if itemPrice >= itemMark:
				priceType = "%d Ep" % itemPrice
			else:
				priceType = "%d EM" % itemMark
			
			ANTI_FLAG_DICT = {
				0 : item.ITEM_ANTIFLAG_WARRIOR,
				1 : item.ITEM_ANTIFLAG_ASSASSIN,
				2 : item.ITEM_ANTIFLAG_SURA,
				3 : item.ITEM_ANTIFLAG_SHAMAN,
			}
			if app.ENABLE_WOLFMAN_CHARACTER:
				ANTI_FLAG_DICT.update({
					4 : item.ITEM_ANTIFLAG_WOLFMAN,
				})

			if isItemSelectAttr:
				itemSelectAttrAndStoneButton.Show()

			itemName.SetText(item.GetItemName())
			
			itemName.SetPackedFontColor(self.GetColor(FAKE_CATEGORY_DATA[constInfo.LAST_CATEG_ID]["subcategoryColor"][constInfo.LAST_SUBCATEG_ID]))

			itemOldPrice.SetText("Eski Fiyat:%d EP" % itemPriceOld)
			itemOldPrice.Hide()
			itemSelectAttrAndStoneButton.SetEvent(ui.__mem_func__(self.selectAttrAndStoneEvent), itemID, itemVnum, itemPrice, itemCount, itemMark)
			# itemSelectAttrAndStoneButton.SetUseSlotEvent(ui.__mem_func__(self.selectAttrAndStoneEvent), itemID, itemVnum)
			itemBuyButton.SetText(priceType)
			itemBuyButton.SetEvent(ui.__mem_func__(self.buyButtonEvent), itemID, itemVnum, itemPrice, itemCount, itemMark)
			itemBuyButton.Enable()

	def searchButtonEvent(self):
		searchText = self.searchEditline.GetText()
		if len(searchText) < 3:
			chat.AppendChat(5, "Aranacak kelime çok kýsa")
			return True
		
		self.SearchItem(searchText)
		return True
	
	def selectAttrAndStoneEvent(self, itemID, itemVnum, itemPrice, itemCount, itemMark):
		# chat.AppendChat(1,"test")
		import uiItemShopSelectAttr
		# item.SelectItem(itemVnum)
		# item.GetItemLocalPos(itemVnum)
		self.itemshopattr = uiItemShopSelectAttr.ItemShopSelectAttr(self)
		self.itemshopattr.Open(itemID,itemVnum,itemPrice,itemCount,itemMark)
		

	def SearchItem(self, itemName):
		searchItemList = filter(lambda item: item[0].find(toLower(itemName)) != -1, constInfo.ITEM_SEARCH_DATA)
		
		if not searchItemList:
			chat.AppendChat(1, "%s içeren nesne bulunamadý." % itemName)
			return

		self.itemList = [item for item in searchItemList]
		self.pageMaxNum = len(self.itemList) / 9

		if len(self.itemList) % 9 > 0:
			self.pageMaxNum += 1

		self.pageNum = 0

		self.RefreshProcess()

	def buyButtonEvent(self, itemID, itemVnum, itemPrice, itemCount, itemMark):
		if itemVnum == 0:
			return

		item.SelectItem(itemVnum)
		if item.IsFlag(ITEM_FLAG_STACKABLE) and itemCount <= 1:
			self.itemStackalbeBuyDialog.SetItem(itemID, itemVnum)
			self.itemStackalbeBuyDialog.SetCountText(itemPrice, int(self.coinxd))#player total coin
			self.itemStackalbeBuyDialog.SetTitleName(item.GetItemName())
			self.itemStackalbeBuyDialog.Open()
		else:
			if itemPrice >= itemMark:
				self.buyQuestionDialog(itemID, itemVnum, item.GetItemName(), 1, itemPrice)
			else:
				self.buyQuestionDialog2(itemID, itemVnum, item.GetItemName(), 1, itemMark)

	def buyQuestionDialog(self, itemID, itemVnum, itemName, itemCount, itemPrice):
		self.questionDialog.SetText1(localeInfo.ASK_BUY_ITEM_TEXT % itemName)
		self.questionDialog.SetText2(localeInfo.DO_YOU_BUY_ITEM_COINS(itemCount, itemPrice))
		self.questionDialog.itemID = itemID
		self.questionDialog.itemVnum = itemVnum
		self.questionDialog.itemCount = itemCount
		self.questionDialog.SetWidth(385)
		self.questionDialog.SetTop()
		self.questionDialog.Open()
		
	def buyQuestionDialog2(self, itemID, itemVnum, itemName, itemCount, itemMark):
		self.questionDialog.SetText1(localeInfo.ASK_BUY_ITEM_TEXT % itemName)
		self.questionDialog.SetText2(localeInfo.DO_YOU_BUY_ITEM_MARK(itemCount, itemMark))
		self.questionDialog.itemID = itemID
		self.questionDialog.itemVnum = itemVnum
		self.questionDialog.itemCount = itemCount
		self.questionDialog.SetWidth(385)
		self.questionDialog.SetTop()
		self.questionDialog.Open()

	def QuestionDialogEvent(self, arg):
		if not self.questionDialog:
			return
		
		if arg:
			itemID = self.questionDialog.itemID
			itemCount = self.questionDialog.itemCount
			net.SendChatPacket("/nesne_market %d %d" % (itemID, itemCount))

		self.questionDialog.Close()
	
	def selectItemSlotEvent(self, itemIndex):
		global esyapos
		
		itemPos = (self.pageNum * 9) + (itemIndex - 1)

		if len(self.itemList) <= itemPos:
			return
		esyapos = itemPos
		(empty, itemID, itemVnum, itemPrice,itemPriceOld, itemCount, itemSocketZero, itemMark, atype0,avalue0,atype1,avalue1,atype2,avalue2,atype3,avalue3,atype4,avalue4,atype5,avalue5,atype6,avalue6,socket0,socket1,socket2,socket3) = self.itemList[itemPos]

		if itemVnum == 0:
			return

		self.buyButtonEvent(itemID, itemVnum, itemPrice, itemCount, itemMark)

	def OverInItem(self, itemIndex):
		if not self.tooltipItem:
			return
		self.tooltipItem.ClearToolTip()
		itemPos = (self.pageNum * 9) + (itemIndex - 1)

		if len(self.itemList) <= itemPos:
			# chat.AppendChat(1,"caaa2")
			return

		(empty, itemID, itemVnum, itemPrice,itemPriceOld, itemCount, itemSocketZero, itemMark , atype0,avalue0,atype1,avalue1,atype2,avalue2,atype3,avalue3,atype4,avalue4,atype5,avalue5,atype6,avalue6,socket0,socket1,socket2,socket3) = self.itemList[itemPos]

		if itemVnum == 0:
			# chat.AppendChat(1,"caaa3")
			return

		item.SelectItem(itemVnum)
		atypeList = [atype0,atype1,atype2,atype3,atype4,atype5,atype6]
		avalueList = [avalue0,avalue1,avalue2,avalue3,avalue4,avalue5,avalue6]
		socketList = [socket0,socket1,socket2,socket3]
		
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(socketList[i])

		attrSlot = []
		for a in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append([atypeList[a],avalueList[a]])
		
		# for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			# attrSlot = [atypeList[x], avalueList[x]]
		# for a in xrange(player.METIN_SOCKET_MAX_NUM):
			# metinSlot = [socketList[a]]
		itemSocketZeros=itemSocketZero

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_BELT):
			itemSocketZero = itemSocketZero+app.GetGlobalTimeStamp()
			metinSlot = [itemSocketZero,0,0,0]

		if item.GetItemType() == item.ITEM_TYPE_RING:
			itemSocketZero = 0
			metinSlot = [0,0,0,0]
			
		if 27996 == int(itemVnum):
			metinSlot = [0,0,0,0]
		
		if 27989 == int(itemVnum):
			metinSlot = [6,0,0,0]
		
		# if item.ITEM_TYPE_COSTUME == item.GetItemType() and item.GetItemSubType() == item.COSTUME_TYPE_SASH:
		if item.ITEM_TYPE_COSTUME == item.GetItemType():
			itemSocketZerox = itemSocketZeros+0
			metinSlot = [itemSocketZerox,0,0,0]

		self.tooltipItem.AddItemData(itemVnum, metinSlot, attrSlot)
		self.tooltipItem.Show()

	def OnOverOutItem(self):
		if not self.tooltipItem:
			return
		self.tooltipItem.ClearToolTip()
		self.tooltipItem.Hide()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()
			
# Item Shop Window
###################################################################################################
