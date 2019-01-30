import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from CustomWidgets import *
from Items import *

class Start(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        form = uic.loadUi('start.ui', self)
        self.setFixedSize(self.size())
        #self.setStyleSheet("background-image: url(coverBG.png);")
        bg = QtGui.QPixmap('Pictures/coverBG')
        self.lbl_bg.setPixmap(bg)
        btn_create = form.findChild(QtWidgets.QPushButton, "btn_create")
        btn_create.setAutoDefault(False)
        btn_create.clicked.connect(self.openLandscape)

    def openLandscape(self):
        self.hide()
        landscapeMenu.show()


class Landscape(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        form = uic.loadUi('landscape.ui', self)
        self.setFixedSize(self.size())
        bg = QtGui.QPixmap('Pictures/woodBG')
        self.lbl_bg.setPixmap(bg)

        #initialize buttons from UI
        self.btn_menu = form.findChild(QtWidgets.QPushButton, "btn_menu")
        self.btn_shapes = form.findChild(QtWidgets.QPushButton, "btn_shapes")
        self.btn_icons = form.findChild(QtWidgets.QPushButton, "btn_icons")
        self.btn_shapeback = form.findChild(QtWidgets.QPushButton, "btn_shapeback")
        self.btn_iconback = form.findChild(QtWidgets.QPushButton, "btn_iconback")

        #initialize frame menus from UI
        self.frame_icons = form.findChild(QtWidgets.QFrame, "frame_icons")
        self.frame_shapes = form.findChild(QtWidgets.QFrame, "frame_shapes")
        self.frame_items = form.findChild(QtWidgets.QFrame, "frame_items")
        self.frame_icons.setVisible(False)
        self.frame_shapes.setVisible(False)

        #connect functions with buttons
        self.btn_menu.clicked.connect(self.openStart)
        self.btn_shapes.clicked.connect(self.shapeItems)
        self.btn_icons.clicked.connect(self.iconItems)
        self.btn_shapeback.clicked.connect(self.mainItems)
        self.btn_iconback.clicked.connect(self.mainItems)

        #initialize frame
        self.lbl_frame = form.findChild(QtWidgets.QLabel, "lbl_frame")

        # initialize comboBox
        self.comboBox_shape = form.findChild(QtWidgets.QComboBox, "comboBox_shape")
        self.comboBox_icon =  form.findChild(QtWidgets.QComboBox, "comboBox_icon")

        #connect comboBox with functions
        self.comboBox_shape.currentIndexChanged.connect(lambda: self.itemChosen(self.shapeList, self.comboBox_shape))
        self.comboBox_icon.currentIndexChanged.connect(lambda: self.itemChosen(self.iconMenuList, self.comboBox_icon))

        #initialize labels on frame_shapes
        self.shapeList = []
        self.shapeIcon_circle = CustomImageLabel('shapeIcon_circle', self.frame_shapes, 'shape_circle', self.lbl_frame, sceneMenu, self, 'shape')
        self.shapeIcon_parallelogram = CustomImageLabel('shapeIcon_parallelogram', self.frame_shapes,'shape_parallelogram', self.lbl_frame,  sceneMenu, self, 'shape')
        self.shapeIcon_rectangle = CustomImageLabel('shapeIcon_rectangle', self.frame_shapes, 'shape_rectangle', self.lbl_frame, sceneMenu, self, 'shape')
        self.shapeIcon_square = CustomImageLabel('shapeIcon_square', self.frame_shapes, 'shape_square', self.lbl_frame, sceneMenu, self, 'shape')
        self.shapeIcon_triangle = CustomImageLabel('shapeIcon_triangle', self.frame_shapes, 'shape_triangle', self.lbl_frame, sceneMenu, self, 'shape')
        self.shapeList.append(self.shapeIcon_circle)
        self.shapeList.append(self.shapeIcon_parallelogram)
        self.shapeList.append(self.shapeIcon_rectangle)
        self.shapeList.append(self.shapeIcon_square)
        self.shapeList.append(self.shapeIcon_triangle)
        for shape in self.shapeList:
            shape.setGeometry(QtCore.QRect(20, 130, 161, 131))
            shape.setVisible(False)
        self.shapeList[0].setVisible(True)

        #initialize labels on frame icons
        self.iconMenuList = []
        self.iconMenu_flower = CustomImageLabel('iconMenu_flower', self.frame_icons,'icon_flower', self.lbl_frame)
        self.iconMenu_grass = CustomImageLabel('iconMenu_grass', self.frame_icons, 'icon_grass', self.lbl_frame)
        self.iconMenu_tree = CustomImageLabel('iconMenu_plant', self.frame_icons, 'icon_plant', self.lbl_frame)
        self.iconMenuList.append(self.iconMenu_flower)
        self.iconMenuList.append(self.iconMenu_grass)
        self.iconMenuList.append(self.iconMenu_tree)
        for icon in self.iconMenuList:
            icon.setGeometry(QtCore.QRect(20, 130, 161, 131))
            icon.setVisible(False)
        self.iconMenu_flower.setVisible(True)

    def openStart(self):
        self.hide()
        startMenu.show()

    def mainItems(self):
        self.frame_icons.setVisible(False)
        self.frame_shapes.setVisible(False)
        self.frame_items.setVisible(True)

    def shapeItems(self):
        self.frame_items.setVisible(False)
        self.frame_icons.setVisible(False)
        self.frame_shapes.setVisible(True)

    def iconItems(self):
        self.frame_items.setVisible(False)
        self.frame_shapes.setVisible(False)
        self.frame_icons.setVisible(True)

    def itemChosen(self, list, comboBox):
        comboBoxIndex = comboBox.currentIndex()
        list[comboBoxIndex].setVisible(True)
        for index in range(len(list)):
            if index != comboBoxIndex:
                list[index].setVisible(False)


class SceneVisualization(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        form = uic.loadUi('specific.ui', self)
        self.setFixedSize(self.size())
        self.tabnameList = []
        self.tree = []
        self.flower = []
        self.ground = []
        self.flowerNameList = []
        self.treeNameList = []
        self.groundNameList = []
        self.treeLabel = []
        self.flowerLabel = []
        self.groundLabel = []
        bg = QtGui.QPixmap('Pictures/woodBG')
        self.lbl_bg.setPixmap(bg)

        #initialize tab
        self.tabPage = form.findChild(QtWidgets.QTabWidget, "tabPage")
        self.tabPage.setTabsClosable(False)
        self.tabPage.currentChanged.connect(self.setCost)

        #initialize buttons
        self.btn_smenu = form.findChild(QtWidgets.QPushButton, "btn_smenu")
        self.btn_flowers = form.findChild(QtWidgets.QPushButton, "btn_flowers")
        self.btn_ground = form.findChild(QtWidgets.QPushButton, "btn_ground")
        self.btn_tree = form.findChild(QtWidgets.QPushButton, "btn_tree")
        self.radiobtn_default.setAutoExclusive(False)
        self.radiobtn_hotel.setAutoExclusive(False)
        self.radiobtn_beach.setAutoExclusive(False)

        #initialize frames
        self.frame_items = form.findChild(QtWidgets.QFrame, "frame_items")
        self.frame_tree.setVisible(False)
        self.frame_flower.setVisible(False)
        self.frame_ground.setVisible(False)

        #initialize comboBox
        self.comboBox_tree = form.findChild(QtWidgets.QComboBox, "comboBox_tree")
        self.comboBox_flower = form.findChild(QtWidgets.QComboBox, "comboBox_flower")
        self.comboBox_ground = form.findChild(QtWidgets.QComboBox, "comboBox_ground")

        #connect buttons with functions
        self.btn_smenu.clicked.connect(self.openLandscape)
        self.btn_flowers.clicked.connect(self.flowersItem)
        self.btn_tree.clicked.connect(self.treesItem)
        self.btn_ground.clicked.connect(self.groundItem)
        self.btn_flowerback.clicked.connect(self.mainItems)
        self.btn_treeback.clicked.connect(self.mainItems)
        self.btn_groundback.clicked.connect(self.mainItems)
        self.btn_uploadbg.clicked.connect(self.setBackground)
        #self.btn_save.clicked.connect(self.saveImage)

        #link with tree, flower, and ground data file
        treeList = open("plant_info_files/treeList.txt", "r")
        for tree in treeList:
            treeInfo = str(tree).split(',')
            name = treeInfo[0]
            region = treeInfo[1]
            spacing = treeInfo[2]
            water = treeInfo[3]
            price = treeInfo[4]
            imageParent = treeInfo[5]
            image = treeInfo[6]
            self.tree.append(Plant(name, region, spacing, water, price, imageParent, image))
            self.treeNameList.append(name)
        treeList.close()

        flowerList = open("plant_info_files/flowerList.txt", "r")
        for flower in flowerList:
            flowerInfo = str(flower).split(',')
            name = flowerInfo[0]
            region = flowerInfo[1]
            spacing = flowerInfo[2]
            water = flowerInfo[3]
            price = flowerInfo[4]
            imageParent = flowerInfo[5]
            image = flowerInfo[6]
            self.flower.append(Plant(name, region, spacing, water, price, imageParent, image))
            self.flowerNameList.append(name)
        flowerList.close()

        groundList = open("plant_info_files/groundList.txt", "r")
        for ground in groundList:
            groundInfo = str(ground).split(',')
            name = groundInfo[0]
            region = groundInfo[1]
            spacing = groundInfo[2]
            water = groundInfo[3]
            price = groundInfo[4]
            imageParent = groundInfo[5]
            image = groundInfo[6]
            self.ground.append(Plant(name, region, spacing, water, price, imageParent, image))
            self.groundNameList.append(name)
        groundList.close()

        #add tree list to comboBox
        self.comboBox_tree.addItems(self.treeNameList)
        self.comboBox_flower.addItems(self.flowerNameList)
        self.comboBox_ground.addItems(self.groundNameList)

        #create customLabel from tree, flower, and ground list
        for tree in self.tree:
            tree.image = tree.image.replace('\n', '')
            label = CustomImageLabel(tree.imageParent, self.frame_tree, tree.image, self.tabPage, self)
            label.setVisible(False)
            label.setGeometry(QtCore.QRect(20, 190, 141, 121))
            self.treeLabel.append(label)
        self.treeLabel[0].setVisible(True)

        for flower in self.flower:
            flower.image = flower.image.replace('\n', '')
            label = CustomImageLabel(flower.imageParent, self.frame_flower, flower.image, self.tabPage, self)
            label.setGeometry(QtCore.QRect(20, 190, 141, 121))
            label.setVisible(False)
            self.flowerLabel.append(label)
        self.flowerLabel[0].setVisible(True)

        for ground in self.ground:
            ground.image = ground.image.replace('\n', '')
            label = CustomImageLabel(ground.imageParent, self.frame_ground, ground.image, self.tabPage, self)
            label.setGeometry(QtCore.QRect(20, 190, 141, 121))
            label.setVisible(False)
            self.groundLabel.append(label)
        self.groundLabel[0].setVisible(True)

        # connect comboBox with functions
        self.comboBox_tree.currentIndexChanged.connect(lambda: self.itemChosen(self.comboBox_tree, self.tree, self.treeLabel))
        self.comboBox_flower.currentIndexChanged.connect(lambda: self.itemChosen(self.comboBox_flower, self.flower, self.flowerLabel))
        self.comboBox_ground.currentIndexChanged.connect(lambda: self.itemChosen(self.comboBox_ground, self.ground, self.groundLabel))

        #connect radio buttons with functions
        self.radiobtn_default.toggled.connect(self.setBgDefault)
        self.radiobtn_hotel.toggled.connect(self.setBgHotel)
        self.radiobtn_beach.toggled.connect(self.setBgBeach)

        #initialize info
        self.lbl_region.setText(self.flower[0].region)
        self.lbl_spacing.setText(self.flower[0].spacing)
        self.lbl_water.setText(self.flower[0].water)
        self.lbl_price.setText(self.flower[0].price)

        self.lbl_region_2.setText(self.tree[0].region)
        self.lbl_spacing_2.setText(self.tree[0].spacing)
        self.lbl_water_2.setText(self.tree[0].water)
        self.lbl_price_2.setText(self.tree[0].price)

        self.lbl_region_3.setText(self.ground[0].region)
        self.lbl_spacing_3.setText(self.ground[0].spacing)
        self.lbl_water_3.setText(self.ground[0].water)
        self.lbl_price_3.setText(self.ground[0].price)

    def openLandscape(self):
        self.mainItems()
        self.hide()
        tabIndex = 0
        totalcost = 0
        while True:
            if self.tabPage.widget(tabIndex) == None:
                break
            tab = self.tabPage.widget(tabIndex)
            totalcost += tab.shapeCost
            tabIndex += 1
        landscapeMenu.lbl_totalcost.setText(str(totalcost))
        landscapeMenu.show()

    def mainItems(self):
        self.frame_items.setVisible(True)
        self.frame_tree.setVisible(False)
        self.frame_flower.setVisible(False)
        self.frame_ground.setVisible(False)

    def flowersItem(self):
        self.frame_items.setVisible(False)
        self.frame_flower.setVisible(True)
        self.comboBox_flower.setCurrentIndex(0)

    def treesItem(self):
        self.frame_items.setVisible(False)
        self.frame_tree.setVisible(True)
        self.comboBox_tree.setCurrentIndex(0)
        self.treeLabel[0].setVisible(True)

    def groundItem(self):
        self.frame_items.setVisible(False)
        self.frame_ground.setVisible(True)
        self.comboBox_ground.setCurrentIndex(0)

    def itemChosen(self, comboBox, infoList, objectList):
        comboBoxIndex = comboBox.currentIndex()
        plant = infoList[comboBoxIndex]
        if comboBox == self.comboBox_flower:
            self.lbl_region.setText(plant.region)
            self.lbl_spacing.setText(plant.spacing)
            self.lbl_water.setText(plant.water)
            self.lbl_price.setText(plant.price)
        elif comboBox == self.comboBox_tree:
            self.lbl_region_2.setText(plant.region)
            self.lbl_spacing_2.setText(plant.spacing)
            self.lbl_water_2.setText(plant.water)
            self.lbl_price_2.setText(plant.price)
        else:
            self.lbl_region_3.setText(plant.region)
            self.lbl_spacing_3.setText(plant.spacing)
            self.lbl_water_3.setText(plant.water)
            self.lbl_price_3.setText(plant.price)
        objectList[comboBoxIndex].setVisible(True)
        for index in range(len(objectList)):
            if index != comboBoxIndex:
                objectList[index].setVisible(False)

    def setBackground(self):
        askFile = QtWidgets.QFileDialog.Options()
        askFile |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options = askFile)
        try:
            bg = QtGui.QPixmap(fileName)
            self.tabPage.currentWidget().setPixmap(bg)
        except FileNotFoundError:
            return

    def setBgDefault(self):
        bg = QtGui.QPixmap('Pictures/Default')
        self.tabPage.currentWidget().setPixmap(bg)
        self.radiobtn_default.setChecked(False)

    def setBgHotel(self):
        bg = QtGui.QPixmap('Pictures/Hotel')
        self.tabPage.currentWidget().setPixmap(bg)
        self.radiobtn_hotel.setChecked(False)

    def setBgBeach(self):
        bg = QtGui.QPixmap('Pictures/Beach')
        self.tabPage.currentWidget().setPixmap(bg)
        self.radiobtn_beach.setChecked(False)

    def setCost(self):
        try:
            self.lbl_cost.setText(str(self.tabPage.currentWidget().shapeCost))
        except AttributeError:
            pass
    '''
    def saveImage(self):
        self.originalPixmap = self.tabPage.currentWidget().screen.grabWindow(0,0,self.tabPage.currentWidget().width(), self.tabPage.currentWidget().height())
        format = 'png'
        initialPath = QtCore.QDir.currentPath() + "/untitled." + format
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", initialPath,  "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
        if fileName:
            self.originalPixmap.save(fileName, format)
        #######################
        saveFile = QtWidgets.QFileDialog.getSaveFileName(self, "Type file to save", ".jpg","JPEG Image (*.jpg);;PNG Image (*.png)" )
        QtWidgets.QFile f(saveFile)
        askFile |= QtWidgets.QFileDialog.DontUseNativeDialog
        file = open(fileName, 'w')
    '''

if __name__ == '__main__':
    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    startMenu = Start()
    sceneMenu = SceneVisualization()
    landscapeMenu = Landscape()
    startMenu.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")