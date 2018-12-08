#!/usr/bin/python3
import time

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPixmap, QBrush, QPen, QImage
from math import *
import sys, random


# represent a case object
class CaseGame(QMainWindow):
    def __init__(self, x, y, color):
        super().__init__()

        self.posX = x
        self.posY = y
        self.color = color
        self.isPlayer = 0
        self.isSelected = False
        self.isSelectable = False
        self.isKing = False
        self.isLock = False

    def set_isSelected(self):
        self.isSelected = not self.isSelected

    def get_color(self):
        if self.isSelectable is True:
            return Qt.magenta
        elif self.color is True:
            return Qt.black
        else:
            return Qt.white


# Create the game area
class GameBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_game_array()
        self.resize(800, 800)
        self.setWindowTitle('Draught Game')

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.fillColor = Qt.white
        self.image.fill(self.fillColor)

        self.current_select = []
        self.caseIsSelected = False
        self.turnContinue = False
        self.current_player = 1
        self.show()

    # Initialize an array which represent our board
    def init_game_array(self):
        self.gameList = []
        color = False
        for y in range(0, 8):
            self.caseList = []
            for x in range(0, 8):
                if x != 0:
                    color = not color
                self.case = CaseGame(x, y, color)
                if y in range(0, 3) and color:
                    self.case.isPlayer = 1
                elif y in range(5, 8) and color:
                    self.case.isPlayer = 2
                self.caseList.append(self.case)
            self.gameList.append(self.caseList)

    # print our board
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect())
        posY = 0
        posX = 0
        i = 0
        for y in range(0, 8):
            for x in range(0, 8):
                painter = QPainter(self.image)
                color = self.gameList[y][x].get_color()
                painter.setPen(QPen(color, 1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
                brush = QBrush(color, Qt.SolidPattern)
                rect = QRect(posX, posY, 100, 100)
                painter.drawRect(rect)
                painter.fillRect(rect, brush)
                if self.gameList[y][x].isPlayer != 0: #if there is something on the case
                    if self.gameList[y][x].isPlayer == 1: #if it's the first team we choose blue
                        color_player = Qt.blue
                    else: #else we choose red for the second team
                        color_player = Qt.red
                    painter.setBrush(QBrush(color_player))
                    if self.gameList[y][x].isSelected: #if the pawn is selected we draw a green circle around it
                        painter.setPen(QPen(QBrush(Qt.green), 3, Qt.SolidLine, Qt.RoundCap))
                    else:
                        painter.setPen(QPen(QBrush(color_player), 1, Qt.SolidLine, Qt.RoundCap))
                    painter.drawEllipse(posX, posY, 98, 98)
                    if self.gameList[y][x].isKing: #if it's a king we draw a yellow "crown" on it
                        painter.setPen(QPen(Qt.yellow, 5, Qt.SolidLine, Qt.RoundCap))
                        painter.drawEllipse(posX + 25, posY + 25, 50, 50)
                posX += 100
                painter.end()
            posY += 100
            posX = 0
        self.update()

    # Trigger when there is a mouse event
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.point = event.pos()
            self.pointX = floor(event.x() / 100)
            self.pointY = floor(event.y() / 100)
            new_point = QPoint(self.pointY, self.pointX) #get the point where we clicked
            if (self.caseIsSelected and new_point in self.FuturPositionList) or self.turnContinue: #if it's a potential position of the selected pawn
                if new_point in self.FuturPositionList: #if it's a new valid position we change our pawn for his new position
                    self.gameList[self.current_select[0]][self.current_select[1]].isPlayer = 0
                    self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False
                    if self.gameList[self.current_select[0]][self.current_select[1]].isKing:
                        self.gameList[self.current_select[0]][self.current_select[1]].isKing = False
                        self.gameList[self.pointY][self.pointX].isKing = True
                    self.gameList[self.pointY][self.pointX].isPlayer = self.current_player
                    if self.check_is_new_king(self.pointY): #we check if the new position of our pawn transform it to a king
                        self.gameList[self.pointY][self.pointX].isKing = True
                    old_point = QPoint(self.current_select[0], self.current_select[1])

                    enemy_point = self.check_if_ennemy(new_point, old_point) #we check if we eat an enemy or not

                    if enemy_point is None: #if we don't eat anybody the turn ended
                        if self.current_player == 1:
                            self.current_player = 2
                        else:
                            self.current_player = 1
                        self.clear_selectable()
                        self.caseIsSelected = False
                        self.turnContinue = False
                    else: # else we recheck if our new position give us the possibility of eating another enemy
                        self.gameList[enemy_point.x()][enemy_point.y()].isPlayer = 0
                        if self.check_enemy_position(self.current_player, self.pointX, self.pointY) is True:
                            self.turnContinue = True
                        else:
                            if self.current_player == 1:
                                self.current_player = 2
                            else:
                                self.current_player = 1
                            self.clear_selectable()
                            self.caseIsSelected = False
                            self.turnContinue = False

                else:
                    return
            #this part is to select a new pawn and find what is possible to do with it
            if self.gameList[self.pointY][self.pointX].isPlayer == self.current_player:
                self.caseIsSelected = True
                if self.current_select:
                    self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False
                    self.current_select.pop(0)
                    self.current_select.pop(0)
                    self.clear_selectable()
                self.gameList[self.pointY][self.pointX].isSelected = True
                self.current_select.append(self.pointY)
                self.current_select.append(self.pointX)
                self.find_futur_postition(self.pointX, self.pointY)
                if self.check_selectable() is False and self.turnContinue is True:
                    self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False
                    self.current_select.pop(0)
                    self.current_select.pop(0)
                    if self.current_player == 1:
                        self.current_player = 2
                    else:
                        self.current_player = 1
                    self.clear_selectable()
                    self.caseIsSelected = False
                    self.turnContinue = False

    #used to find our futur potential positions and enemies
    def find_futur_postition(self, x, y):
        self.FuturPositionList = []
        tmp_player = self.gameList[y][x].isPlayer
        for i in range(0, 4):
            self.check_position(i, x, y, self.FuturPositionList, tmp_player)

    #used to check cases around the selected pawn
    def check_position(self, i, x, y, futur_position, tmp_player):
        tmp_x = x
        tmp_y = y
        if self.gameList[y][x].isKing:
            if i == 0:
                x -= 1
                y -= 1
            if i == 1:
                x += 1
                y -= 1
            if i == 2:
                x -= 1
                y += 1
            if i == 3:
                x += 1
                y += 1
        else:
            if i == 0:
                x -= 1
                y -= 1
            elif i == 1:
                x += 1
                y -= 1
            elif i == 2:
                x -= 1
                y += 1
            elif i == 3:
                x += 1
                y += 1
        if x in range(0, 8) and y in range(0, 8):
            if self.gameList[y][x].isPlayer != tmp_player:
                if (tmp_player == 1 and i > 1 or tmp_player == 2 and i <= 1) or self.gameList[tmp_y][tmp_x].isKing:
                    if self.gameList[y][x] and self.gameList[y][x].isPlayer == 0:
                        new_pos = QPoint(y, x)
                        self.gameList[y][x].isSelectable = True
                        futur_position.append(new_pos)
                    elif self.gameList[y][x].isPlayer != 0:
                        ennemie_pos = QPoint(y, x)
                        list_pos = []
                        self.check_empty_position(i, x, y, ennemie_pos, list_pos)

    # when we find an enemy around of our pawn we check if there is an empty case to eat it
    def check_empty_position(self, i, x, y, ennemie_pos, list_pos):
        if i == 0:
            x -= 1
            y -= 1
            i = 3
        elif i == 1:
            x += 1
            y -= 1
            i = 2
        elif i == 2:
            x -= 1
            y += 1
            i = 1
        elif i == 3:
            x += 1
            y += 1
            i = 0
        if x in range(0, 8) and y in range(0, 8):
            if self.gameList[y][x].isPlayer == 0:
                self.gameList[y][x].isSelectable = True
                if list_pos:
                    list_pos[0] = QPoint(y, x)
                else:
                    list_pos.append(QPoint(y, x))
                self.FuturPositionList.append(QPoint(y, x))
                list_pos.append(ennemie_pos)

    #used when we just eat an enemy and the turn continue, we check here if there is again an enemy to eat around our new position
    def check_enemy_position(self, player, x, y):
        tmp_x = x
        tmp_y = y
        if self.gameList[y][x].isKing:
            x -= 1
            y += 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(0, x, y):
                        return True
            x = tmp_x + 1
            y = tmp_y + 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(1, x, y):
                        return True
            x = tmp_x - 1
            y = tmp_y - 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(2, x, y):
                        return True
            x = tmp_x + 1
            y = tmp_y - 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(3, x, y):
                        return True
        elif player == 1:
            x -= 1
            y += 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(0, x, y):
                        return True
            x = tmp_x + 1
            y = tmp_y + 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(1, x, y):
                        return True
        elif player == 2:
            x -= 1
            y -= 1
            if x in range(0, 8) and y in range(0, 8):
                if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                    if self.check_futur_empty_position(2, x, y):
                        return True
            x = tmp_x + 1
            y = tmp_y - 1
            if x in range(0, 8) and y in range(0, 8):
                    if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
                        if self.check_futur_empty_position(3, x, y):
                            return True
        return False

    # if check_enemy_position find an enemy we check here if we can eat it
    def check_futur_empty_position(self, i, x, y):
        if i == 0:
            x -= 1
            y += 1
        elif i == 1:
            x += 1
            y += 1
        elif i == 2:
            x -= 1
            y -= 1
        elif i == 3:
            x += 1
            y -= 1
        if x in range(0, 8) and y in range(0, 8):
            if self.gameList[y][x].isPlayer == 0:
                return True
        return False

    #clear all selectable cases
    def clear_selectable(self):
        for i in range(0, len(self.FuturPositionList)):
            y = self.FuturPositionList[i].x()
            x = self.FuturPositionList[i].y()
            self.gameList[y][x].isSelectable = False

    #check if there are cases which are selectable
    def check_selectable(self):
        for y in range(0, 8):
            for x in range(0, 8):
                if self.gameList[y][x].isSelectable:
                    return True
        return False

    #if we pass through an enemy during our deplacement we eat it
    def check_if_ennemy(self, new_point, old_point):
        x = new_point.y()
        y = new_point.x()
        old_x = old_point.y()
        old_y = old_point.x()
        if old_y > y and old_x < x:
            y += 1
            x -= 1
        elif old_y > y and old_x > x:
            y += 1
            x += 1
        elif old_y < y and old_x < x:
            y -= 1
            x -= 1
        elif old_y < y and old_x > x:
            y -= 1
            x += 1
        if self.gameList[y][x].isPlayer != 0 and self.gameList[y][x].isPlayer != self.current_player:
            return QPoint(y, x)
            #augmenter le score du current player
        else:
            return None

    #check if the new position of our selected pawn transform it to a king
    def check_is_new_king(self, y):
        if self.current_player == 1 and y == 7:
            return True
        elif self.current_player == 2 and y == 0:
            return True
        return False


if __name__ == '__main__':
    app = QApplication([])
    draught = GameBoard()
    sys.exit(app.exec_())
