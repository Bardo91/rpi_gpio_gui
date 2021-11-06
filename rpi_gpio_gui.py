from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
import RPi.GPIO as gpio
from PyQt5.QtGui import QPixmap

class GpioWidget(QtWidgets.QWidget):
    def __init__(self, _pin, invert=False):
        super().__init__()
        self.pin_ = _pin
        gpio.setup(self.pin_, gpio.IN, pull_up_down=gpio.PUD_UP)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(1,2,1,2)
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        
        layout.addWidget(QtWidgets.QLabel("Pin {}".format(_pin)))

        self.selectModeBox = QtWidgets.QComboBox()
        self.selectModeBox.setFixedHeight(25)
        self.selectModeBox.addItem("Input")
        self.selectModeBox.addItem("Output")
        self.selectModeBox.currentIndexChanged.connect(self.modeChanged)
        layout.addWidget(self.selectModeBox)

        self.selectPullupBox = QtWidgets.QComboBox()
        self.selectPullupBox.setFixedHeight(25)
        self.selectPullupBox.addItem("Pull-up")
        self.selectPullupBox.addItem("Pull-Down")
        self.selectPullupBox.addItem("None")
        layout.addWidget(self.selectPullupBox)
        self.selectModeBox.currentIndexChanged.connect(self.pullupChanged)

        self.button = QtWidgets.QPushButton("OFF", self)
        self.button.setFixedHeight(25)
        self.button.setCheckable(True)
        self.button.setEnabled(False)
        self.button.clicked.connect(self.toggleButton)
        layout.addWidget(self.button)

        self.value = QtWidgets.QLabel("----")
        layout.addWidget(self.value)

        self.timer=QTimer()
        self.timer.timeout.connect(self.observeGpio)
        self.timer.start(100)

        self.setLayout(layout)
        if invert:
            self.setLayoutDirection(QtCore.Qt.RightToLeft)

    def toggleButton(self):
        if self.button.isChecked():
            self.button.setText("ON")
            gpio.output(self.pin_, True)
        else:
            self.button.setText("OFF")
            gpio.output(self.pin_, False)

    def modeChanged(self,i):
        if(i == 0):
            gpio.setup(self.pin_, gpio.IN)
            self.timer.start(100)
            self.button.setEnabled(False)
            self.selectPullupBox.setEnabled(True)
        elif(i == 1):
            gpio.setup(self.pin_, gpio.OUT)
            self.timer.stop()
            self.button.setChecked(False)
            self.button.setEnabled(True)
            self.selectPullupBox.setEnabled(False)

    def pullupChanged(self, i):
        if(self.selectModeBox.currentIndex() == 0):
            if(i == 0):
                gpio.setup(self.pin_, gpio.IN, pull_up_down=gpio.PUD_UP)
            elif(i==1):
                gpio.setup(self.pin_, gpio.IN, pull_up_down=gpio.PUD_DOWN)
            elif(i==2):
                pass 

    def observeGpio(self):
        if gpio.input(self.pin_) == gpio.LOW:
            self.value.setText("LOW")
        elif gpio.input(self.pin_) == gpio.HIGH:
            self.value.setText("HIGH")

class VerticalSpacer(QtWidgets.QWidget):
    def __init__(self, _space):
        super().__init__()
        layout = QtWidgets.QHBoxLayout();
        layout.setSpacing(0);
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.setLayout(layout);
        self.label = QtWidgets.QLabel("");
        self.label.setFixedHeight(_space)
        layout.addWidget(self.label)

class GpioApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumSize(700,600)
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        mainLayout.setAlignment(Qt.AlignTop)
        
        leftCol = QtWidgets.QVBoxLayout()
        leftCol.setAlignment(Qt.AlignTop)
        leftCol.setSpacing(0)
        leftCol.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        mainLayout.addLayout(leftCol)

        pixmap = QPixmap('pinout.png')
        pinoutPng = QtWidgets.QLabel(self)
        pinoutPng.setPixmap(pixmap.scaledToHeight(600))
        mainLayout.addWidget(pinoutPng)

        rightCol = QtWidgets.QVBoxLayout()
        rightCol.setAlignment(Qt.AlignTop)
        rightCol.setSpacing(0)
        rightCol.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        mainLayout.addLayout(rightCol)
        self.setLayout(mainLayout)


        unusedPinSize = 7
        initialPad = 7
        ## Populate left
        leftCol.addWidget(VerticalSpacer(initialPad))
        leftCol.addWidget(VerticalSpacer(unusedPinSize))
        leftCol.addWidget(GpioWidget(3))
        leftCol.addWidget(GpioWidget(5))
        leftCol.addWidget(GpioWidget(7))
        leftCol.addWidget(VerticalSpacer(unusedPinSize))
        leftCol.addWidget(GpioWidget(11))
        leftCol.addWidget(GpioWidget(13))
        leftCol.addWidget(GpioWidget(15))
        leftCol.addWidget(VerticalSpacer(unusedPinSize))
        leftCol.addWidget(GpioWidget(19))
        leftCol.addWidget(GpioWidget(21))
        leftCol.addWidget(GpioWidget(23))
        leftCol.addWidget(VerticalSpacer(unusedPinSize))
        leftCol.addWidget(GpioWidget(29))
        leftCol.addWidget(GpioWidget(31))
        leftCol.addWidget(GpioWidget(33))
        leftCol.addWidget(GpioWidget(35))
        leftCol.addWidget(GpioWidget(37))


        ## Populate Right
        rightCol.addWidget(VerticalSpacer(initialPad))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(GpioWidget(8, True))
        rightCol.addWidget(GpioWidget(10, True))
        rightCol.addWidget(GpioWidget(12, True))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(GpioWidget(16, True))
        rightCol.addWidget(GpioWidget(18, True))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(GpioWidget(22, True))
        rightCol.addWidget(GpioWidget(24, True))
        rightCol.addWidget(GpioWidget(26, True))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(GpioWidget(32, True))
        rightCol.addWidget(VerticalSpacer(unusedPinSize))
        rightCol.addWidget(GpioWidget(36, True))
        rightCol.addWidget(GpioWidget(38, True))
        rightCol.addWidget(GpioWidget(40, True))

        # verticalSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    font = QtGui.QFont("Courier New")
    font.setStyleHint(QtGui.QFont.Monospace);
    app.setFont(font)
    
    gpio.setmode(gpio.BOARD)

    win = GpioApp()
    win.show()

    app.exec()

