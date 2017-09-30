from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QDesktopWidget,
                             QVBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog)
from PyQt5.QtCore import Qt
import sys
from enum import Enum
import struct
from floatdata import FloatData

UiFloatTest, BaseType = loadUiType("floattest.ui")

class ClickEditLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, event):
        event.accept()
        self.onclick()

    def onclick(self):
        pass


class MoveSelectButton(QPushButton):
    index = None
    curMouseDown = False
    curToggled = False
    prgmWidget = None

    def __init__(self, index, prgmWidget):
        super().__init__("0")
        self.setCheckable(True)
        self.index = index
        self.toggled.connect(self._self_toggled)
        self.setMouseTracking(True)
        self.prgmWidget = prgmWidget

    def mouseDown(self):
        self.curMouseDown = True

    def mouseUp(self):
        self.curMouseDown = False
        self.curToggled = False

    def mouseMove(self):
        if self.curMouseDown and not self.curToggled and self.isEnabled():
            self.curToggled = True
            self.toggle()

    def mouseMoveEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        event.ignore()
        self.toggle()
        self.curToggled = True

    def mouseReleaseEvent(self, event):
        event.ignore()

    def _self_toggled(self, b):
        sender = self.sender()
        sender.setText("1" if b else "0")
        self.prgmWidget.data.setBit(self.index, b)


class MoveSelectWidget(QWidget):
    def __init__(self, prgmWidget):
        super().__init__()

        self.prgmWidget = prgmWidget

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 0, 20, 20)
        self.setLayout(layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
                margin: 0px;
                padding: 0px;
            }
        """)

        index = 64
        self.binbtn = []
        self.binlab = []

        for _ in range(4):
            hbox = QHBoxLayout()
            hbox.setSpacing(10)
            for _ in range(16):
                index -= 1
                btn = MoveSelectButton(index, self.prgmWidget)
                self.binbtn.append(btn)

                lab = QLabel(str(index))
                lab.index = index
                lab.setAlignment(Qt.AlignCenter)
                self.binlab.append(lab)

                vbox = QVBoxLayout()
                vbox.setSpacing(0)
                vbox.addWidget(lab)
                vbox.addWidget(btn)
                hbox.addLayout(vbox)
            layout.addLayout(hbox)

    def mousePressEvent(self, event):
        event.accept()
        for btn in self.binbtn:
            btn.mouseDown()

    def mouseReleaseEvent(self, event):
        event.accept()
        for btn in self.binbtn:
            btn.mouseUp()

    def mouseMoveEvent(self, event):
        for btn in self.binbtn:
            if btn.geometry().contains(event.pos()):
                btn.mouseMove()
                break

    def setFloat(self):
        for btn in self.binbtn:
            if btn.index >= 32:
                btn.setEnabled(False)

    def setDouble(self):
        for btn in self.binbtn:
            if btn.index >= 32:
                btn.setEnabled(True)
                btn.setChecked(False)

class FloatTestWidget(QWidget, UiFloatTest):

    data = None
    updating = False
    labelHex = None
    labelValue = None

    def editValue(self):
        val, avi = QInputDialog.getText(self, "", "请输入数值", text = str(self.data.floatValue))
        if avi:
            try:
                val = float(val)
                self.data.floatValue = val
            except Exception:
                pass

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.labelHex = ClickEditLabel()
        self.labelValue = ClickEditLabel()
        self.labelValue.onclick = self.editValue

        self.radioFloat.clicked.connect(self._radioFloat_clicked)
        self.radioDouble.clicked.connect(self._radioDouble_clicked)

        self.widget = MoveSelectWidget(self)

        self.layout().addWidget(self.labelHex)
        self.layout().addWidget(self.labelValue)
        self.layout().addWidget(self.widget)
        self.setFixedSize(self.minimumSize())

        self.data = FloatData()
        self.data.updateWidget = self.updateWidget

    def _radioFloat_clicked(self, _):
        self.radioFloat.setChecked(True)
        self.radioDouble.setChecked(False)
        self.data.type = FloatData.FloatDataType.float
        self.widget.setFloat()

    def _radioDouble_clicked(self, _):
        self.radioFloat.setChecked(False)
        self.radioDouble.setChecked(True)
        self.data.type = FloatData.FloatDataType.double
        self.widget.setDouble()

    def _labelValue_clicked(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _updateInfo(self):
        self.labelValue.setText(str(self.data.floatValue))
        self.labelHex.setText(str(self.data.hexString))
    
    def updateWidget(self):
        if self.updating:
            return

        self.updating = True

        self.labelValue.setText(str(self.data.floatValue))
        self.labelHex.setText(self.data.hexString)

        if self.data.type == FloatData.FloatDataType.float:
            pass
        else:
            pass

        length = FloatData._typelength[self.data.type] * 8
        for i in range(length):
            self.widget.binbtn[63 - i].setChecked(self.data.getBit(i))

        self.updating = False

def main():
    app = QApplication(sys.argv)
    widget = FloatTestWidget()
    widget.show()
    widget.center()


    widget.widget.setFloat()

    app.exec_()

if __name__ == '__main__':
    main()