import os, sys, pathlib 
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFrame)
from PyQt6.QtCore import (Qt, QPoint, QEvent)
from PyQt6.QtGui import (QMouseEvent)


class WinMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        mlay = QVBoxLayout()
        mlay.setContentsMargins(0,0,0,0)
        mlay.setSpacing(0)
        self.setLayout(mlay)
        self.initCustomCap()
        self.initUi()
        self.setWindowTitle('TEST')

    def initCustomCap(self):
        def capMouseMove(event: QMouseEvent):
            if cap.property('capMoved'):
                toPos = event.globalPosition().toPoint() - cap.property('pressedOn')
                self.move(toPos)
        def capMousePress(event: QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                cap.setProperty('pressedOn', event.pos())
                cap.setProperty('capMoved', True)

        def capMouseRelease(event: QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                cap.setProperty('capMoved', False)

        cap = QFrame(self)
        cap.mouseMoveEvent = capMouseMove
        cap.mousePressEvent = capMousePress
        cap.mouseReleaseEvent = capMouseRelease

        cap.setProperty('class', 'theCustomCap')
        lcap = QHBoxLayout(cap)
        lcap.setContentsMargins(0,0,0,0)

        title = QLabel()
        self.windowTitleChanged.connect(lambda: title.setText(self.windowTitle()))

        closebutt= QPushButton('x')
        closebutt.clicked.connect(self.close)
        hidebutt = QPushButton('-')
        hidebutt.clicked.connect(self.showMinimized)
        lcap.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        lcap.addStretch(1)
        lcap.addWidget(hidebutt, alignment=Qt.AlignmentFlag.AlignRight)
        lcap.addWidget(closebutt, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout().addWidget(cap, stretch=1)

    def initUi(self):
        self.mainframe = QFrame()
        self.layout().addWidget(self.mainframe, stretch=1000)

if __name__ =="__main__":
    app = QApplication(sys.argv)
    screen_size = app.primaryScreen().size()
    styles = pathlib.Path('./lesson2.css')
    win = WinMain()
    win.setMaximumSize(screen_size*0.7)
    win.setMinimumSize(screen_size*0.3)
    win.setStyleSheet(styles.read_text())
    win.show()
    sys.exit(app.exec())
