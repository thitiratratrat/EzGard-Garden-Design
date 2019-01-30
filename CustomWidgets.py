from PyQt5 import QtCore, QtGui, QtWidgets, uic
from abc import ABC, abstractmethod, ABCMeta
from PIL import Image
from PIL.ImageQt import ImageQt

class Base(type(QtCore.QObject), ABCMeta):
    pass

class DragDrop(QtWidgets.QLabel, metaclass = Base):
    def __init__(self, filename, parent):
        super().__init__(parent)
        filename = "Pictures/" + filename + '.png'
        self.pic = Image.open(filename)
        picture = ImageQt(self.pic)
        self.picture = QtGui.QPixmap.fromImage(picture)
        self.setPixmap(self.picture)
    @abstractmethod
    def mousePressEvent(self, event):
        pass

#label that generates the draggable plant and shape image once clicked
class CustomImageLabel(DragDrop):
    def __init__(self, filename, parent, image, imageParent, sceneMenu = None, landscapeMenu = None, type = 'plant'):
        super().__init__(filename, parent)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background : transparent;")
        self.type = type
        self.image = image
        self.imageParent = imageParent
        self.sceneMenu = sceneMenu
        self.landscapeMenu = landscapeMenu
        self.name = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.type == 'plant':
                if self.sceneMenu != None:
                    if self.sceneMenu.frame_flower.isVisible():
                        price = float(self.sceneMenu.lbl_price.text())
                        self.sceneMenu.tabPage.currentWidget().addCost(price)
                    elif self.sceneMenu.frame_tree.isVisible():
                        price = float(self.sceneMenu.lbl_price_2.text())
                        self.sceneMenu.tabPage.currentWidget().addCost(price)
                    else:
                        price = float(self.sceneMenu.lbl_price_3.text())
                        self.sceneMenu.tabPage.currentWidget().addCost(price)
                    self.sceneMenu.lbl_cost.setText(str(self.sceneMenu.tabPage.currentWidget().shapeCost))
                    DragImage(self.image, self.imageParent, self.sceneMenu, price)
                else:
                    DragImage(self.image, self.imageParent)
            else:
                self.name = shapeName(self)
                self.name.show()

#draggable plant image
class DragImage(DragDrop):
    def __init__(self, filename,  parent, sceneMenu = None, price = None):
        if isinstance(parent, QtWidgets.QTabWidget):
            parent = parent.currentWidget()
        super().__init__(filename, parent)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background : transparent;")
        self.setGeometry(QtCore.QRect(330, 170, 161, 131))
        self.maxWidth = self.picture.width()
        self.maxHeight = self.picture.height()
        self.resize(self.picture.width(), self.picture.height())
        self.style = self.styleSheet()
        self.setVisible(True)
        self.price = price
        self.note = ""
        self.sceneMenu = sceneMenu
        #delete button
        self.btn_delete = QtWidgets.QPushButton(self)
        self.btn_delete.setStyleSheet("background-color:#fa9f0f;")
        self.btn_delete.setText("X")
        self.btn_delete.setGeometry(QtCore.QRect(0, 20, 20, 17))
        self.btn_delete.clicked.connect(self.delete)
        self.btn_delete.setVisible(False)
        #decrease size button
        self.btn_minus = QtWidgets.QPushButton(self)
        self.btn_minus.setStyleSheet("background-color:#cfcdcd")
        self.btn_minus.setText("-")
        self.btn_minus.setGeometry(QtCore.QRect(self.width() - 40, 20, 20, 14))
        self.btn_minus.setVisible(False)
        self.btn_minus.clicked.connect(self.decrease)
        #increase size button
        self.btn_plus = QtWidgets.QPushButton(self)
        self.btn_plus.setStyleSheet("background-color:#cfcdcd")
        self.btn_plus.setText("+")
        self.btn_plus.setGeometry(QtCore.QRect(self.width() - 20, 20, 20, 14))
        self.btn_plus.setVisible(False)
        self.btn_plus.clicked.connect(self.increase)

    def mousePressEvent(self, event):
        self.__mouseMoved = None
        if event.button() == QtCore.Qt.LeftButton:
            #self.keyPressedEvent(event)
            self.update()
            self.__mouseMoved = event.globalPos()
            self.btn_delete.setVisible(False)
            self.btn_minus.setVisible(False)
            self.btn_plus.setVisible(False)
        if event.button() == QtCore.Qt.RightButton:
            self.btn_delete.setVisible(True)
            self.btn_minus.setVisible(True)
            self.btn_plus.setVisible(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMoved
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.__mouseMoved = globalPos

    def mouseDoubleClickEvent(self, event):
        if self.sceneMenu != None:
            self.memo = plantNote(self)

    def delete(self):
        if self.sceneMenu != None:
            self.sceneMenu.tabPage.currentWidget().subtractCost(self.price)
            self.sceneMenu.lbl_cost.setText(str(self.sceneMenu.tabPage.currentWidget().shapeCost))
        self.deleteLater()

    def increase(self):
        if (self.picture.width() + 20) > self.maxWidth and (self.picture.height() + 20) > self.maxHeight:
            return
        width, height = self.pic.size
        width += 20
        wpercent = (width / float(self.pic.size[0]))
        hsize = int((float(self.pic.size[1]) * float(wpercent)))
        self.pic = self.pic.resize((width, hsize), Image.ANTIALIAS)
        picture = ImageQt(self.pic)
        self.picture = QtGui.QPixmap.fromImage(picture)
        self.setPixmap(self.picture)
        self.resize(self.picture.width(), self.picture.height())
        self.btn_delete.setGeometry(QtCore.QRect(0, 20, 20, 17))
        self.btn_minus.setGeometry(QtCore.QRect(self.width() - 40, 20, 20, 14))
        self.btn_plus.setGeometry(QtCore.QRect(self.width() - 20, 20, 20, 14))

    def decrease(self):
        if self.picture.width() - 20 < 80:
            return
        width, height = self.pic.size
        width -= 20
        wpercent = (width / float(self.pic.size[0]))
        hsize = int((float(self.pic.size[1]) * float(wpercent)))
        self.pic = self.pic.resize((width, hsize), Image.ANTIALIAS)
        picture = ImageQt(self.pic)
        self.picture = QtGui.QPixmap.fromImage(picture)
        self.setPixmap(self.picture)
        self.resize(self.picture.width(), self.picture.height())
        self.btn_delete.setGeometry(QtCore.QRect(0, 20, 20, 17))
        self.btn_minus.setGeometry(QtCore.QRect(self.width() - 40, 20, 20, 14))
        self.btn_plus.setGeometry(QtCore.QRect(self.width() - 20, 20, 20, 14))


#draggable basic shapes that once right clicked will open tab widget
class DragShape(DragImage):
    def __init__(self, filename,  parent, sceneMenu, landscapeMenu, tabTag):
        super().__init__(filename, parent)
        self.sceneMenu = sceneMenu
        self.landscapeMenu = landscapeMenu
        self.tab = customTabLabel()
        bg = QtGui.QPixmap('Default')
        self.tab.setPixmap(bg)
        self.tabTag = tabTag
        self.sceneMenu.tabPage.addTab(self.tab, self.tabTag)
        self.setToolTip(self.tabTag)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.landscapeMenu.hide()
            self.sceneMenu.show()
            index = self.sceneMenu.tabPage.indexOf(self.tab)
            self.sceneMenu.tabPage.setCurrentIndex(index)

    def delete(self):
        cost = float(self.landscapeMenu.lbl_totalcost.text())
        index = self.sceneMenu.tabPage.indexOf(self.tab)
        tab = self.sceneMenu.tabPage.widget(index)
        cost -= tab.shapeCost
        self.landscapeMenu.lbl_totalcost.setText(str(cost))
        self.sceneMenu.tabPage.removeTab(index)
        self.sceneMenu.tabnameList.remove(self.tabTag)
        self.deleteLater()


class customTabLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.screen = QtWidgets.QApplication.primaryScreen()
        self.shapeCost = 0
    def addCost(self, price):
        self.shapeCost += price
    def subtractCost(self,price):
        self.shapeCost -= price


class shapeName(QtWidgets.QDialog):
    def __init__(self, label):
        super().__init__()
        form = uic.loadUi('shapeName.ui', self)
        self.setFixedSize(self.size())
        self.label = label

        #initialize line edit and labels
        self.line_name = form.findChild(QtWidgets.QLineEdit, "line_name")
        self.lbl_warning = form.findChild(QtWidgets.QLabel, "lbl_warning")

        #initialize button
        self.btn_ok = form.findChild(QtWidgets.QPushButton, "btn_ok")
        self.btn_cancel = form.findChild(QtWidgets.QPushButton, "btn_cancel")

        #connect buttons with functions
        self.btn_ok.clicked.connect(self.getName)
        self.btn_cancel.clicked.connect(self.cancel)

    def getName(self):
        self.name = self.line_name.text()
        if self.name.strip(" ") == "":
            self.lbl_warning.setText("Error! Shape tags should contain at least one character.")
        elif self.name.strip(" ") in self.label.sceneMenu.tabnameList:
            self.lbl_warning.setText("Error! This tag has already been used.")
        else:
            self.label.sceneMenu.tabnameList.append(self.name)
            self.line_name.setText(None)
            DragShape(self.label.image, self.label.imageParent, self.label.sceneMenu, self.label.landscapeMenu, self.name)
            self.deleteLater()

    def cancel(self):
        self.line_name.setText(None)
        self.deleteLater()


class plantNote(QtWidgets.QDialog):
    def __init__(self, label):
        super().__init__()
        form = uic.loadUi('plantMemo.ui', self)
        self.label = label
        self.textEdit_note.setText(self.label.note)
        self.btn_ok.clicked.connect(self.addNote)
        self.show()

    def addNote(self):
        text = self.textEdit_note.toPlainText()
        self.label.note = text
        self.label.setToolTip(self.label.note)
        self.hide()