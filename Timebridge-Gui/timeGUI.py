#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
import gc
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#######################################
class poker:
    def __init__(self, w, number):
        self.number = number
        self.L = QLabel(w)
        self.card = QPixmap('cards\\'+str(self.number)+'.png')
        self.L.setPixmap(self.card)
        self.L.resize(57,87)
        self.x = 0
        self.y = 0
        

    def cardMove(self,x,y):
        self.x = x
        self.y = y
        self.L.move(self.x,self.y)

    def cardMoveY(y):
        self.y = self.y + y
        self.L.move(self.x,self.y)

    def delete(self):
        self.L.deleteLater()


class player:
    def __init__(self):
        self.cardlist = []
        self.numberlist = []
        self.bpx = 0
        self.bpy = 0
        self.px = 0
        self.py = 0
        self.delcard = 0 #出牌后需要将相应的牌删除
        self.playcardnumber = 0

    def initial(self, w, numberlist, beginpointx, 
    beginpointy, playpointx,playpointy):
        self.numberlist = numberlist
        self.bpx = beginpointx
        self.bpy = beginpointy
        self.px = playpointx
        self.py = playpointy
        self.interval = 20
        self.delcard = poker(w,[1])
        for i in range( 0,len(self.numberlist) ):
            self.cardlist.append(poker( w, self.numberlist[i] ) )


    def move_(self):#把牌移动到显示区域
        for i in range(0,len(self.cardlist)):
            self.cardlist[i].cardMove(self.bpx + self.interval*i , self.bpy)

    def play(self, number): #出牌，返回值为当前出牌的编号
        self.cardlist[number].cardMove(self.px, self.py)
        self.delcard = self.cardlist.pop(number)
        self.move_()
        return self.numberlist.pop(number)

    def delete(self):
        self.delcard.delete() 
#######################################

class welcomePage(QMainWindow):
    

    close_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):  
        self.setWindowTitle('时光桥牌')
        #设置窗口的图标，引用当前目录下的time.png图片
        self.setWindowIcon(QIcon('time.png'))        
        self.setGeometry(300, 300, 600, 600) 

        self.btn = QToolButton(self)
        self.btn.setText("开始游戏")
        self.btn.resize(100, 60)
        self.btn.move(250, 400)
        self.show()

    def closeEvent(self, event):
        #是否确认退出
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
 
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class TimeBridgeGUI(QWidget):
    def __init__(self, parent=None):
        super(TimeBridgeGUI, self).__init__(parent)
        #坐标指示器
        grid = QGridLayout()
        x = 0
        y = 0
        
        self.text = "x: {0},  y: {1}".format(x, y)
        #self.setMouseTracking(True)
        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)
        self.setLayout(grid)

        #player
        self.player = player()

        
        self.resize(800, 700)
        #self.setStyleSheet("background: black")

    def getplayer(self, numberlist):
        self.player.initial(self,numberlist, 240, 612, 371.5, 520)
        self.player.move_()

    #配合highlight_quest使用
    quest_state_0 = 0
    quest_state_1 = 0
    quest_state_2 = 0

    def mousePressEvent(self, e):
        
        x = int((e.x()-200)/80) 
        y = int((e.y()-180)/48) 
        
        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)

        if (e.x() >= 200 and e.x() <= 600) and (e.y() >=180 and e.y() <= 520):
        	quest_state_0 = 10 * y + x
        

        #出牌判断
        if e.button() == Qt.LeftButton:
            condition1 = (e.x()>= self.player.bpx)
            condition2 = (e.x() <= (self.player.bpx + (len(self.player.cardlist)-1)*self.player.interval) + 57)
            condition3 = (e.y() >= self.player.bpy)
            condition4 = (e.y()<= (self.player.bpy + 87))

            if condition1 and condition2 and condition3 and condition4:
                clicklength = e.x() - self.player.bpx
                if clicklength <= self.player.interval*len(self.player.cardlist):
                    number = int( clicklength / self.player.interval )
                    #print(number)
                    self.player.delete()
                    card = self.player.play(number)
                    print(card)
                elif clicklength > self.player.interval*len(self.player.cardlist):
                    #print(len(self.player.cardlist)-1)
                    self.player.delete()
                    card = self.player.play(len(self.player.cardlist)-1)
                    print(card)
                


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_player_area(qp)
        qp.end()

    def draw_player_area(self, qp):
      
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(col)
		#基础区域
        qp.setBrush(QColor(180, 180, 180))
        qp.drawRect(240, 0, 297, 87)
        qp.drawRect(371.5, 93, 57, 87)
        qp.drawRect(371.5, 520, 57, 87)
        qp.drawRect(240, 612, 297, 87)
        qp.drawRect(0, 190, 87, 297)
        qp.drawRect(709, 190, 87, 297)
        qp.drawRect(100, 306.5, 57, 87)
        qp.drawRect(643, 306.5, 57, 87)
        #叫牌区域
        qp.drawRect(200, 180, 400, 340)
        qp.setPen(pen)
        qp.drawLine(200, 228, 600, 228)
        qp.drawLine(200, 276, 600, 276)
        qp.drawLine(200, 324, 600, 324)
        qp.drawLine(200, 372, 600, 372)
        qp.drawLine(200, 420, 600, 420)
        qp.drawLine(200, 468, 600, 468)
        qp.drawLine(200, 516, 600, 516)
        qp.drawLine(280, 180, 280, 520)
        qp.drawLine(360, 180, 360, 520)
        qp.drawLine(440, 180, 440, 520)
        qp.drawLine(520, 180, 520, 520)
    


        
    def bid_map(xb, yb):
    #将叫牌区格位映射到坐标
    	return (80 * x + 200, 48 * y + 180, 80, 48)

    def bid_update(self, BidPlayer, BidResult):
    	xb = BidResult % 10
    	yb = BidResult / 10
    	qp = QPainter()
    	qp.begin(self)
    	qp.setBrush(Qcolor(BidPlayer * 20, 100 + BidPlayer * 10, 230 - BidPlayer * 15))#皮这一下就很开心
    	qp.drawRect(bid_map(xb, yb))
    	qp.setBrush(Qcolor(200, 200, 200))#把失效区域涂灰
    	for x in range(0, 4):
    		for y in range(0, 6):
    			if (y < yb or (y == yb and x < xb)):
    				qp.drawRect(bid_map(x, y))

    def highlight_quest(self, area):
        if area == 0:
            return self.quest_state_0
   
    def handle_click(self):
        if not self.isVisible():
            self.show()
            

    def handle_close(self):
        self.close()
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = welcomePage()
    s = TimeBridgeGUI()
    s.getplayer([0,1,2,3,4,5,6,7,8,9,10,11,12])

    ex.btn.clicked.connect(s.handle_click)
    ex.btn.clicked.connect(ex.hide)
    ex.close_signal.connect(ex.close)
    ex.show()
    sys.exit(App.exec_())