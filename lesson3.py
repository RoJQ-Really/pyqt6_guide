import os, sys, pathlib, hashlib, winreg, copy, random
from flowmodule import winactions, styleactions

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFrame,
                             QLineEdit)
from PyQt6.QtCore import (Qt, QPoint, QEvent, QPropertyAnimation, QVariantAnimation)
from PyQt6.QtGui import (QMouseEvent, QIcon, QFontDatabase)


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
        self.setWindowTitle('MD5')
    
        
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
        cap.setMinimumHeight(20)
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
        animation = QVariantAnimation(self)
        animation.setDuration(1000)
        animation.setProperty('indexed_list', [])
        def doAnimation(val: int):
            indexed_list = animation.property('indexed_list')
            if len(indexed_list) == 0:
                indexed_list = [i for i in range(17)]
                indexed_list.pop(8)
                
             
                animation.setProperty('indexed_list', indexed_list)
            rndIndex=  random.choice(indexed_list)
            oldText = list(rootText.text())
            cho = random.choice(list("qwertyuiopa[]dffjb..,m<>*&%^$\|"))
            oldText[rndIndex] =cho
            rootText.setText("".join(oldText))
        def doEnd():
            print(animation.property('hashed'))
            rootText.setText(animation.property('hashed'))

        animation.valueChanged.connect(doAnimation)
        animation.finished.connect(doEnd)
        def doEncode():
            if animation.state() == animation.State.Running:
                return
            counts_of_random_integers = random.choice([2**8, 2**9, 2**10])
            animation.setStartValue(0)
            animation.setEndValue(counts_of_random_integers)
            hashed = hashlib.md5(line_edit.text().encode()).hexdigest()
            rootText.setText(hashed[:8] + "\n" + hashed[8:16])
            animation.setProperty('hashed', hashed[:8] + "\n" + hashed[8:16])
            animation.start()
        self.mainframe = QFrame()
        self.mainframe.setProperty('class', 'theMainFrame')
        mlay = QVBoxLayout(self.mainframe)
        mlay.setContentsMargins(5,0,5,0)

        line_edit=  QLineEdit(self)
        line_edit.setMaxLength(32)
        line_edit.setPlaceholderText('Введите текст')

        rootText = QLabel('0'*8 + "\n" + "0"*8)
        rootText.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard | Qt.TextInteractionFlag.TextSelectableByMouse)
        oldFont = rootText.font()
        oldFont.setBold(True)
        rootText.setFont(oldFont)

        buttEncode = QPushButton(QIcon("./icons/Группа.png"), "Закодировать")
        buttEncode.clicked.connect(doEncode)
        mlay.addStretch(1)
        mlay.addWidget(line_edit)
        mlay.addWidget(rootText, alignment=Qt.AlignmentFlag.AlignCenter)
        mlay.addStretch(1)
        mlay.addWidget(buttEncode, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout().addWidget(self.mainframe, stretch=1000)


def stylizerWindows(data: str):
    accent_color_hex = winactions.read_registry_value(winreg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Accent' , 'AccentColorMenu')
    accent_color_hex = hex(accent_color_hex)
    print(accent_color_hex)
    basicColorList = [int(accent_color_hex[-2:], 16), int(accent_color_hex[-4:-2], 16), int(accent_color_hex[-6:-4], 16), int(accent_color_hex[-8:-6], 16)]
    
    basicColor = styleactions.relative_change_color(basicColorList, matrix=[1, 1, 1, 1])
    lightColor = styleactions.relative_change_color(basicColorList, matrix=[1.2, 1.2, 1.2, 1])
    darkenColor = styleactions.relative_change_color(basicColorList, matrix=[0.8, 0.8, 0.8, 1])
    inputLineBG = styleactions.relative_change_color(basicColorList, matrix=[0.8, 0.5, 0.8, 1])

    color_vars = {}
    color_vars['basicColor'] = basicColor
    color_vars['lightColor'] = lightColor
    color_vars['darkenColor'] = darkenColor
    color_vars['inputLineBG'] = inputLineBG
    for k, v in color_vars.items():
        data = data.replace(f"var({k})", v)
    return data



if __name__ =="__main__":
    app = QApplication(sys.argv)
    fontid = QFontDatabase.addApplicationFont('./data/OCRA LT.ttf')
    print(QFontDatabase.applicationFontFamilies(fontid))
    oFont = app.font()
    oFont.setFamily('OCRA LT')
    app.setFont(oFont)
    screen_size = app.primaryScreen().size()
    styles = pathlib.Path('./lesson3.css')
    styles = styles.read_text()
    if sys.platform == 'win32':
        styles = stylizerWindows(styles)
    
    win = WinMain()
    win.setMaximumSize(screen_size*0.7)
    win.setMinimumSize(screen_size*0.3)
    win.setStyleSheet(styles)
    win.show()
    sys.exit(app.exec())
