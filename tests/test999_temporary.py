import sys
from PyQt5.QtWidgets import QDialog, QApplication
from  DemoButton import *


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.ui.autoDefaultButton.clicked.connect(self.autoDefault_onClicked)
        self.ui.defaultButton.clicked.connect(self.default_onClicked)
        self.ui.noneButton.clicked.connect(self.none_onClicked)
        self.ui.checkBox.stateChanged.connect(self.checkBox1_stateChanged)
        self.ui.radioButton_1.toggled.connect(self.radioButton_toggle)
        self.ui.radioButton_2.toggled.connect(self.radioButton_toggle)
        self.ui.radioButton_3.toggled.connect(self.radioButton_toggle)
    def updateLog(self,message): 
        self.ui.LogEdit.append(message)        
    def autoDefault_onClicked(self): 
        self.updateLog('call autoDefault onClicked')
    def default_onClicked(self): 
        self.updateLog('call default onClicked')
    def none_onClicked(self): 
        self.updateLog('call none onClicked')
    def checkBox1_stateChanged(self,state):
        self.updateLog('call checkBox1 stateChanged.state is'+str(state))
    def radioButton_toggle(self):
        state = self.radioButtonState()
        self.updateLog('Call radioButton_toggle.state is'+str(state))
    def radioButtonState(self):
        state = 0
        if self.ui.radioButton_1.isChecked() == True: 
            state = 0
        elif self.ui.radioButton_2.isChecked() == True:
            state = 1
        else:
            state = 2
        return state

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())