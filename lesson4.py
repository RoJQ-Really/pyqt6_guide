import sys, textwrap, typing, pathlib
from PyQt6.QtWidgets import (QApplication, QMainWindow, QAbstractButton, QLayout,
                             QLabel, QWidget, QPushButton, QFrame)
from PyQt6.QtCore import (Qt, QPoint)
from PyQt6.QtGui import (QSurface, QIcon, QPixmap)



class QuadroButton(QFrame):
    
    class AligmentIcon:
        Left    = 0b0001
        Right   = 0b0010
        Top     = 0b0100
        Bottom  = 0b1000
        CenterH = 0b0011
        CenterV = 0b1100
    # Left | Top == 0b0011
    # Right | Bottom == 0b1100
    class AligmentText:
        Left  = 0b01
        Right = 0b10
        Center = 0b11

    def __init__(self, parent = None, max_width: int = 128):
        super().__init__(parent)
        #self.setStyleSheet('background-color: red;')
        
        self.iconAlign = self.AligmentIcon.Left | self.AligmentIcon.Top
        self.textAlign = self.AligmentText.Left
        self.iconSizeCoeficent = 1/4
        self.__constSize = 0
        self.__curentIconPosition = (0,0,0)
        self.constSize = max_width
        self.horizontalMargin = 5
        self.label = None
        self.icon = None
        
        
    def setStyleSheet(self, style: str | None):
        print('STYLES!!!')
        return super().setStyleSheet(style)
    
    def calclulate_size(self, text: str):
        metric = self.fontMetrics()
        maxCharsInLine = self.constSize//metric.averageCharWidth()
        maxLines = (self.constSize - self.__curentIconPosition[2])//metric.height()
        wrapedText = textwrap.wrap(text, maxCharsInLine, max_lines=maxLines, placeholder='...')
        print(maxLines, maxCharsInLine)
        return "\n".join(wrapedText)
    
    @property
    def constSize(self):
        return self.__constSize
    
    @constSize.setter
    def constSize(self, v: int):
        margins = self.contentsMargins()
        self.__constSize = v
        self.setFixedSize(self.constSize + margins.left() + margins.right(), self.constSize + margins.top() + margins.bottom())
        self.calculatePositions(self.iconAlign)

    def setContentsMargins(self, left:int=5, top:int=5, right:int=5, bottom:int=5):
        r = super().setContentsMargins(left, top, right, bottom)
        self.constSize = self.constSize
        self.updateIconData()
        return r
    
    def updateIconData(self):
        self.calculatePositions(self.iconAlign)
        if self.icon is not None:
            pos_x, pos_y, scaleSize = self.__curentIconPosition
            pixmap = self.icon.pixmap().scaled(scaleSize, scaleSize, Qt.AspectRatioMode.IgnoreAspectRatio)
            self.icon.setPixmap(pixmap)
            self.icon.move(pos_x, pos_y)
            
    def calculatePositions(self, position: AligmentIcon):
        
        scaleSize = int(self.constSize * self.iconSizeCoeficent)
        pos_y = 0
        pos_x = 0

        margins = self.contentsMargins()
        if position & self.AligmentIcon.Left:
            pos_x = 0 + margins.left()
            
        elif position & self.AligmentIcon.Right:
            pos_x = self.constSize - scaleSize - margins.right()
        elif (position & self.AligmentIcon.CenterH) or (position ^ self.AligmentIcon.CenterH):
            pos_x = self.constSize//2 - scaleSize//2 + (margins.left() - margins.right())
        if position & self.AligmentIcon.Top:
            pos_y = 0 + margins.top()
        elif position & self.AligmentIcon.Bottom:
            pos_y = self.constSize - scaleSize - margins.bottom()
        elif (position & self.AligmentIcon.CenterV) or (position ^ self.AligmentIcon.CenterV):
            pos_y = self.constSize//2 - scaleSize//2 + (margins.top() - margins.bottom())
            
        self.__curentIconPosition = (pos_x, pos_y, scaleSize)
        return self.__curentIconPosition
        

    def setIcon(self, path: str, position: AligmentIcon = AligmentIcon.Left | AligmentIcon.Top):
        print()
        a = self.property('styleSheet')
        pixmap = QPixmap(path)
        if pixmap.isNull(): return
        if self.icon is None:
            self.icon = QLabel(self)
        self.icon.setPixmap(pixmap)
        self.iconAlign = position
        self.updateIconData()
        
    


    def setText(self, text: str, position: AligmentText = AligmentText.Left):
        
        wrapedText = self.calclulate_size(text)
        if self.label is None:
            self.label = QLabel(self)
        self.label.setText(wrapedText)
        margin = self.contentsMargins()

        if position & self.AligmentText.Left:
            pos_x = 0 + margin.left()
        elif position & self.AligmentText.Right:
            pos_x = self.constSize - self.label.width() - margin.right()
        elif (position & self.AligmentText.Center) or (position ^ self.AligmentText.Center):
            pos_x = self.constSize//2 - self.label.width()//2 + (margin.left() - margin.right())

        if self.iconAlign & self.AligmentIcon.Top:
            pos_y = self.constSize - self.label.height() - margin.bottom()
        elif self.iconAlign & self.AligmentIcon.Bottom:
            pos_y = margin.top()

        self.textAlign = position
        self.label.move(pos_x, pos_y)
        
        
    

class WinMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Windows 10 Buttons')
        self.setAnimated(True)
        b = QuadroButton(self, 64)
        b.move(10,10)
        b.setContentsMargins(20,5,20,5)
        b.show()
        b.setText('Привет, как твои дела Что ты делаешь')
        b.setIcon('./icons/Группа.png')
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    styles=  pathlib.Path('./lesson4.css').read_text()
    app.setStyleSheet(styles)
    win =WinMain()
    win.show()
    
    sys.exit(app.exec())
        
        