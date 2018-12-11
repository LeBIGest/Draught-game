#!/usr/bin/python3
import time

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, \
    QToolBar, QWidget, QDialog, QMessageBox, QAction, QListWidget, QStackedWidget, QCheckBox
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QPen, QImage, QIcon, QColor
from math import *
import sys


g_color_player_one = QColor(0, 92, 232)
g_color_player_two = QColor(12, 151, 8)
g_color_king = QColor(255, 216, 0)
g_color_selected = QColor(0, 255, 102)
g_color_selectable_case = QColor(255, 98, 164)


class Player:

    def __init__(self, id):
        self.score = 0
        self.jumps = 0
        self.id = id
        self.timerleft = 301


class Game:

    def __init__(self):
        self.time = 0
        self.players = [Player(1), Player(2)]
        self.current_player = self.players[0]

    def change_player(self):
        if self.current_player.id == 1:
            self.current_player.timerleft = 301
            self.current_player = self.players[1]
        elif self.current_player.id == 2:
            self.current_player.timerleft = 301
            self.current_player = self.players[0]

    def check_winner(self):
        if self.players[0].score == 12:
            return self.players[0].id
        elif self.players[1].score == 12:
            return self.players[1].id
        else:
            return 0

    def reset(self):
        self.players[0].score = 0
        self.players[0].timerleft = 301
        self.players[1].score = 0
        self.players[1].timerleft = 301
        self.current_player = self.players[0]


g_game = Game()


class GameOptionPlayer:

    def __init__(self, new_player, color):
        self.player = new_player

        player = QLabel("Player " + str(self.player.id) + ":")
        font = player.font()
        font.setBold(True)
        font.setPointSize(18)
        player.setFont(font)

        self.time_passed = QLabel("Time left : 05:00")

        self.title = QVBoxLayout()
        self.title.addWidget(player)
        self.title.addWidget(self.time_passed)

        self.header = QHBoxLayout()

        self.icon = QLabel()
        self.picture = QPixmap(50, 50)
        self.picture.fill(Qt.white)
        self.paint = QPainter(self.picture)
        self.paint.setBrush(QBrush(color))
        self.paint.setPen(QPen(QBrush(color), 3, Qt.SolidLine, Qt.RoundCap))
        self.paint.drawEllipse(2, 2, 46, 46)
        self.icon.setPixmap(self.picture)

        self.header.addWidget(self.icon)
        self.header.addLayout(self.title)

        self.paint.end()

        self.score = QLabel("Score: " + str(self.player.score))
        self.jumps = QLabel("Jumps: " + str(self.player.jumps))

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.header)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.score)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.jumps)
        self.layout.addSpacing(10)

    def updateTimer(self):
        self.player.timerleft -= 1
        min, sec = divmod(self.player.timerleft, 60)
        if min < 0:
            self.time_passed.setText("Time left : 00:00")
        else:
            self.time_passed.setText("Time left : {:02d}:{:02d}".format(min, sec))

    def update_player(self, player, new_color):
        self.paint = QPainter(self.picture)
        self.paint.setBrush(QBrush(new_color))
        self.paint.setPen(QPen(QBrush(new_color), 3, Qt.SolidLine, Qt.RoundCap))
        self.paint.drawEllipse(2, 2, 46, 46)
        self.icon.setPixmap(self.picture)
        self.paint.end()
        self.score.setText("Score: " + str(player.score))
        self.jumps.setText("Jumps: " + str(player.jumps))


class GameOptions:
    def __init__(self):

        global g_game
        global g_color_player_one
        global g_color_player_two

        self.game = g_game

        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)

        self.player1_part = QWidget()
        self.player2_part = QWidget()

        self.player1 = GameOptionPlayer(self.game.players[0], g_color_player_one)
        self.player1_part.setLayout(self.player1.layout)

        self.player2 = GameOptionPlayer(self.game.players[1], g_color_player_two)
        self.player2_part.setLayout(self.player2.layout)
        # player2_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.tool_bar.addWidget(self.player1_part)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.player2_part)
        self.tool_bar.addSeparator()
        checkBox_color = QCheckBox("Color blindness Mode")
        checkBox_color.setChecked(True)
        checkBox_color.stateChanged.connect(self.change_color_mode)

        self.tool_bar.addWidget(checkBox_color)

    def change_color_mode(self, state):

        global g_color_player_one
        global g_color_player_two
        global g_color_king
        global g_color_selected
        global g_color_selectable_case

        if state == Qt.Checked:
            g_color_player_one = QColor(0, 92, 232)
            g_color_player_two = QColor(12, 151, 8)
            g_color_king = QColor(255, 216, 0)
            g_color_selected = QColor(0, 255, 102)
            g_color_selectable_case = QColor(255, 98, 164)
        else:
            g_color_player_one = Qt.blue
            g_color_player_two = Qt.red
            g_color_king = Qt.yellow
            g_color_selected = Qt.green
            g_color_selectable_case = Qt.magenta

    def update_current_player(self, current_id):
        if current_id == 2:
            self.player2_part.setStyleSheet("background-color: #89e8f9")
            self.player1_part.setStyleSheet("background-color: #FFFFFF")
        elif current_id == 1:
            self.player1_part.setStyleSheet("background-color: #89e8f9")
            self.player2_part.setStyleSheet("background-color: #FFFFFF")

    def update(self):
        self.player1.update_player(self.game.players[0], g_color_player_one)
        self.player2.update_player(self.game.players[1], g_color_player_two)

       # player2_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


class HowToPlayFragment:
    def __init__(self, title, desc, icon_path):
        self.widget = QWidget()

        layout = QVBoxLayout()
        self.logo = QLabel()
        self.picture = QPixmap(icon_path)
        self.logo.setPixmap(self.picture.scaled(400, 400))
        self.title = QLabel(title)
        font = self.title.font()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        self.description = QLabel(desc)

        layout.addWidget(self.title)
        layout.addSpacing(5)
        if icon_path is not "":
            layout.addWidget(self.logo)
            layout.addSpacing(5)
        layout.addWidget(self.description)

        self.widget.setLayout(layout)


class HowToPlay(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("How to play ?")

        self.left_list = QListWidget()
        self.left_list.setMinimumWidth(200)
        self.left_list.insertItems(0, ["Presentation & Goal", "Selection", "Movement", "Capture", "King", "Win condition"])

        self.rules_part = HowToPlayFragment("Presentation & Goal", "Draught game is a two players game. \nThe goal is to capture all pieces of your openent",
                                            "")

        self.selection_part = HowToPlayFragment("Selection",
                                            "The player can select one piece when he clickes on it. One piece can be selected at the time.\nThe game will show him all possibilities he can do.",
                                                "./img/selection.png")

        self.movement_part = HowToPlayFragment("Movement",
                                               "When a piece is selected (i.e selection part) the player can select between all possibilities (colored cases)\nand select one to place the piece on this case.",
                                               "./img/movement.png")

        self.capture_part = HowToPlayFragment("Capture",
                                               "When the piece is diagonally in front of an oponent one, the player can capture it.\nTo do this, the player can just click on the colored square behind the piece\nHe will score and if he can capture a piece again, his turn contnues and he can capture another piece.",
                                               "./img/movement.png")

        self.king_part = HowToPlayFragment("King",
                                              "A piece can be a King when it reach the oponent board side.\nThis piece is very important because he can move and capture behind him.",
                                              "./img/king.png")

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.rules_part.widget)
        self.stack.addWidget(self.selection_part.widget)
        self.stack.addWidget(self.movement_part.widget)
        self.stack.addWidget(self.capture_part.widget)
        self.stack.addWidget(self.king_part.widget)

        layout = QHBoxLayout()
        layout.addWidget(self.left_list)
        layout.addWidget(self.stack)

        self.setLayout(layout)
        self.left_list.currentRowChanged.connect(self.display)

        self.setGeometry(800, 100, 500, 200)

        self.show()

    def display(self, i):
        self.stack.setCurrentIndex(i)


# represent a case object
class CaseGame:
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
            return g_color_selectable_case
        elif self.color is True:
            return Qt.black
        else:
            return Qt.white


# Create the game area
class GameBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        global g_color_player_one
        global g_color_player_two
        global g_color_king
        global g_color_selected
        global g_color_selectable_case


        self.init_game_array()
        self.resize(1005, 820)
        self.setWindowTitle('Draught Game')
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.fillColor = Qt.white
        self.image.fill(self.fillColor)

        self.statusBar()

        self.menubar = self.menuBar()

        self.setMyMenuBar()

        global g_game
        self.game = g_game

        self.game_options = GameOptions()
        self.game_options.update_current_player(self.game.current_player.id)

        self.addToolBar(Qt.RightToolBarArea, self.game_options.tool_bar)

        timer = QTimer(self)
        timer.setSingleShot(False)
        timer.timeout.connect(self.update_timer)
        timer.start(1000)

        self.current_select = []
        self.caseIsSelected = False
        self.turnContinue = False
        self.current_player = 1
        self.show()

    def setMyMenuBar(self):
        fileMenu = self.menubar.addMenu("Game")

        quit_action = QAction(QIcon("../../cat.jpeg"), "&Quit the game", self.menubar)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the application  (Ctrl+Q)")
        quit_action.triggered.connect(self.quitGame)
        fileMenu.addAction(quit_action)

        reset_action = QAction(QIcon("../../cat.jpeg"), "&Reset the game", self.menubar)
        reset_action.setShortcut("Ctrl+R")
        reset_action.setStatusTip("Reset the game   (Ctrl+R)")
        reset_action.triggered.connect(self.resetGame)
        fileMenu.addAction(reset_action)

        viewMenu = self.menubar.addMenu("View")

        blindness_color_action = QAction(QIcon("../../cat.jpeg"), "&Blindness Mode", self.menubar)
        blindness_color_action.setShortcut("Ctrl+B")
        blindness_color_action.setStatusTip("Set the game in a blindness colour mode    (Ctrl+B)")
        viewMenu.addAction(blindness_color_action)

        helpMenu = self.menubar.addMenu("Help")
        how_to_play = QAction(QIcon("../../cat.jpeg"), "How to play", self.menubar)
        how_to_play.setShortcut("Ctrl+?")
        how_to_play.setStatusTip("Display the game manual   (Ctrl+?)")
        how_to_play.triggered.connect(self.displayHowToPlay)
        helpMenu.addAction(how_to_play)

    def quitGame(self):
        self.close()

    def resetGame(self):
        self.init_game_array()
        self.current_player = 1
        self.game.reset()
        self.update()

    def displayHowToPlay(self):
        self.how_to_play = HowToPlay()

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

    def update_current_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        self.game.change_player()
        self.clear_selectable()
        self.caseIsSelected = False
        self.turnContinue = False

    def update_timer(self):
        if self.game.current_player.timerleft <= 0:
            ret = QMessageBox.question(self, "The game is finihed !",
                                       "Player" + str(
                                           self.game.current_player.id) + "takes too longer to play  !\n\n You can restart the restart the game of quit it",
                                       QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
            if ret == QMessageBox.Close:
                self.close()
            if ret == QMessageBox.Retry:
                self.init_game_array()
                self.game.reset()
                self.update_current_player()
                self.game_options.update_current_player(self.current_player)
                self.update()
            return
        if self.game.current_player.id == 1:
            self.game_options.player1.updateTimer()
        if self.game.current_player.id == 2:
            self.game_options.player2.updateTimer()
        self.game_options.update_current_player(self.game.current_player.id)
        self.update()

    # print our board
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect())
        posY = 20
        posX = 0

        for y in range(0, 8):
            for x in range(0, 8):
                painter = QPainter(self.image)
                color = self.gameList[y][x].get_color()
                painter.setPen(QPen(color, 1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
                brush = QBrush(color, Qt.SolidPattern)
                rect = QRect(posX, posY, 100, 100)
                painter.drawRect(rect)
                painter.fillRect(rect, brush)
                if self.gameList[y][x].isPlayer != 0:  # if there is something on the case
                    if self.gameList[y][x].isPlayer == 1:  # if it's the first team we choose blue
                        color_player = g_color_player_one
                    else:  # else we choose red for the second team
                        color_player = g_color_player_two
                    painter.setBrush(QBrush(color_player))
                    if self.gameList[y][x].isSelected:  # if the pawn is selected we draw a green circle around it
                        painter.setPen(QPen(QBrush(g_color_selected), 3, Qt.SolidLine, Qt.RoundCap))
                    else:
                        painter.setPen(QPen(QBrush(color_player), 1, Qt.SolidLine, Qt.RoundCap))
                    painter.drawEllipse(posX, posY, 98, 98)
                    if self.gameList[y][x].isKing:  # if it's a king we draw a yellow "crown" on it
                        painter.setPen(QPen(g_color_king, 5, Qt.SolidLine, Qt.RoundCap))
                        painter.drawEllipse(posX + 25, posY + 25, 50, 50)
                posX += 100
                painter.end()
            posY += 100
            posX = 0
        self.update()
        self.game_options.update()
        self.game_options.update_current_player(self.game.current_player.id)

    # Trigger when there is a mouse event
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.point = event.pos()
            self.pointX = floor(event.x() / 100)
            self.pointY = floor(event.y() / 100)
            new_point = QPoint(self.pointY, self.pointX)  # get the point where we clicked
            if (
                    self.caseIsSelected and new_point in self.FuturPositionList) or self.turnContinue:  # if it's a potential position of the selected pawn
                if new_point in self.FuturPositionList:  # if it's a new valid position we change our pawn for his new position
                    self.gameList[self.current_select[0]][self.current_select[1]].isPlayer = 0
                    self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False
                    if self.gameList[self.current_select[0]][self.current_select[1]].isKing:
                        self.gameList[self.current_select[0]][self.current_select[1]].isKing = False
                        self.gameList[self.pointY][self.pointX].isKing = True
                    self.gameList[self.pointY][self.pointX].isPlayer = self.current_player
                    if self.check_is_new_king(
                            self.pointY):  # we check if the new position of our pawn transform it to a king
                        self.gameList[self.pointY][self.pointX].isKing = True
                    old_point = QPoint(self.current_select[0], self.current_select[1])

                    enemy_point = self.check_if_ennemy(new_point, old_point)  # we check if we eat an enemy or not

                    if enemy_point is None:  # if we don't eat anybody the turn ended
                        self.update_current_player()
                    else:  # else we recheck if our new position give us the possibility of eating another enemy
                        self.gameList[enemy_point.x()][enemy_point.y()].isPlayer = 0
                        self.gameList[enemy_point.x()][enemy_point.y()].isKing = False
                        self.game.current_player.score += 1
                        if self.check_enemy_position(self.current_player, self.pointX, self.pointY) is True:
                            self.turnContinue = True
                        else:
                            self.update_current_player()
                else:
                    return
            # this part is to select a new pawn and find what is possible to do with it
            if self.pointX in range(0, 8) and self.pointY in range(0, 8):
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
                        self.update_current_player()
        if self.game.check_winner() == 1:
            ret = QMessageBox.question(self, "The game is finihed !",
                                       "The winner is the Player 1 !\n\n You can restart the restart the game of quit it",
                                       QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
            if ret == QMessageBox.Close:
                self.close()
            if ret == QMessageBox.Retry:
                self.init_game_array()
                self.game.reset()
                self.game_options.update_current_player(self.current_player)
                self.update()
            return
        elif self.game.check_winner() == 2:
            ret = QMessageBox.question(self, "The game is finihed !",
                                       "The winner is the Player 2s !\n\n You can restart the restart the game of quit it",
                                       QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
            if ret == QMessageBox.Close:
                self.close()
            if ret == QMessageBox.Retry:
                self.init_game_array()
                self.game.reset()
                self.game_options.update_current_player(self.current_player)
                self.update()
            return

    def closeEvent(self, event):
        QApplication.closeAllWindows()

    # used to find our futur potential positions and enemies
    def find_futur_postition(self, x, y):
        self.FuturPositionList = []
        tmp_player = self.gameList[y][x].isPlayer
        for i in range(0, 4):
            self.check_position(i, x, y, self.FuturPositionList, tmp_player)

    # used to check cases around the selected pawn
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
            if self.gameList[y][x].isPlayer == 0:
                self.gameList[y][x].isSelectable = True
                if list_pos:
                    list_pos[0] = QPoint(y, x)
                else:
                    list_pos.append(QPoint(y, x))
                self.FuturPositionList.append(QPoint(y, x))
                list_pos.append(ennemie_pos)

    # used when we just eat an enemy and the turn continue, we check here if there is again an enemy to eat around our new position
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

    # clear all selectable cases
    def clear_selectable(self):
        for i in range(0, len(self.FuturPositionList)):
            y = self.FuturPositionList[i].x()
            x = self.FuturPositionList[i].y()
            self.gameList[y][x].isSelectable = False

    # check if there are cases which are selectable
    def check_selectable(self):
        for y in range(0, 8):
            for x in range(0, 8):
                if self.gameList[y][x].isSelectable:
                    return True
        return False

    # if we pass through an enemy during our deplacement we eat it
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
            # augmenter le score du current player
        else:
            return None

    # check if the new position of our selected pawn transform it to a king
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
