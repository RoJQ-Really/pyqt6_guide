import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QFrame, QHBoxLayout, QVBoxLayout,
                             QBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import (Qt, pyqtSignal,QEvent)




class WinMain(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.installEventFilter(self)

    def eventFilter(self, a0, a1):
        
        if a1.type() == QEvent.Type.MouseButtonPress:
            print('\nКликнуто в eventFilter')

        return super().eventFilter(a0, a1)
    
    def mousePressEvent(self, a0):
        print('Кликнуто в mousePressEvent')
        return super().mousePressEvent(a0)
    
    

    def initUi(self):
        def func():
            print('YOU CLIKCKED')
        l = QVBoxLayout(self)
        label = QLabel('TEXT1')
        label2 = QLabel('TEXT2')
        
        butt = QPushButton()
        butt.pressed
        butt.released
        
       
        hl = QHBoxLayout()
        hl.addWidget(butt)

        l.addWidget(label)
        l.addWidget(label2)
        l.addLayout(hl)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WinMain()
    win.show()

    sys.exit(app.exec())