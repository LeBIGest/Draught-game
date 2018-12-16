#!/usr/bin/python3
import time

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, \
    QToolBar, QWidget, QDialog, QMessageBox, QAction, QListWidget, QStackedWidget, QCheckBox, QFrame, QSizePolicy
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer, QSize
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QPen, QImage, QIcon, QColor
from math import *
import sys


# Global variables to define used colors.

# Color linked to the player 1
g_color_player_one = QColor(0, 92, 232)

# Color linked to the player 2
g_color_player_two = QColor(12, 151, 8)

# Color linked to the king differentiation
g_color_king = QColor(255, 216, 0)

# Color linked to the selection
g_color_selected = QColor(0, 255, 102)

# Color linked to the possible moves for a player
g_color_selectable_case = QColor(255, 98, 164)


# Class linked to the player in the logical side
class Player:

    # Constructor where some parameters about a player like his score, his remaining pieces, id and his timer
    def __init__(self, id):
        self.score = 0
        self.remaining_pieces = 12
        self.id = id
        self.timerleft = 301


# Class about the player management
class Game:

    # Set a list of 2 players and the current player.
    def __init__(self):
        self.time = 0
        self.players = [Player(1), Player(2)]
        self.current_player = self.players[0]

    # Function to change the current player and reset the timer of the old current player.
    def change_player(self):
        if self.current_player.id == 1:
            self.current_player.timerleft = 301
            self.current_player = self.players[1]
        elif self.current_player.id == 2:
            self.current_player.timerleft = 301
            self.current_player = self.players[0]

    # Function to check the winner and return the player's id who win the game.
    def check_winner(self):
        if self.players[0].score == 12:
            return self.players[0].id
        elif self.players[1].score == 12:
            return self.players[1].id
        else:
            return 0

    # Reset the game, set both scores to 0 and timers to 5 minutes (300 seconds + 1 second of delay)
    # And set the current player to the player 1
    def reset(self):
        for player in self.players:
            player.score = 0
            player.timerleft = 301
            player.remaining_pieces = 12
        self.current_player = self.players[0]


# Set the game object in global to have access in other class without reference it
g_game = Game()


# This class corresponds to the graphical aspect of a player in the scoreboard
class GameOptionPlayer:

    # Link a logic player with his graphical aspect and a color
    def __init__(self, new_player, color):
        self.player = new_player

        # Create the title in a label composed of "player" and his id
        player = QLabel("Player " + str(self.player.id) + ":")

        # Create a larger font with a bold effect
        font = player.font()
        font.setBold(True)
        font.setPointSize(18)

        # Set the new font to the player label
        player.setFont(font)

        # Create a label for the timer
        self.time_passed = QLabel("Time left : 05:00")

        # Create a vertical layout and put the player label and the timer label in it
        self.title = QVBoxLayout()
        self.title.addWidget(player)
        self.title.addWidget(self.time_passed)

        # Create a horizontal layout for the header (player icon + title)
        self.header = QHBoxLayout()

        # Creation of a icon which represent the player piece color
        self.icon = QLabel()
        self.picture = QPixmap(50, 50)

        # Fill the icon in white
        self.picture.fill(Qt.white)
        self.paint = QPainter(self.picture)
        self.paint.setBrush(QBrush(color))
        self.paint.setPen(QPen(QBrush(color), 3, Qt.SolidLine, Qt.RoundCap))
        self.paint.drawEllipse(2, 2, 46, 46)
        self.icon.setPixmap(self.picture)
        self.paint.end()

        # Add the icon and the title in the header layout
        self.header.addWidget(self.icon)
        self.header.addLayout(self.title)

        # Creation of a label for remaining pieces of the player
        self.remaining_pieces = QLabel("Remaining pieces: " + str(self.player.remaining_pieces))

        # Creation of a label for score of the player
        self.score = QLabel("Score: " + str(self.player.score))

        # Creation of the graphical player's main layout (in vertical orientation)
        self.layout = QVBoxLayout()

        # Add all created layouts with spacing to have a clean display of information
        self.layout.addLayout(self.header)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.remaining_pieces)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.score)
        self.layout.addSpacing(10)

    # Function which update the timer label in MIN:SEC format or block it when it arrives to zero
    def updateTimer(self):
        self.player.timerleft -= 1
        min, sec = divmod(self.player.timerleft, 60)
        if min < 0:
            self.time_passed.setText("Time left : 00:00")
        else:
            self.time_passed.setText("Time left : {:02d}:{:02d}".format(min, sec))

    # Function which update information about the player passed in argument with a new color
    def update_player(self, player, new_color):

        # Recreate the player icon
        self.paint = QPainter(self.picture)
        self.paint.setBrush(QBrush(new_color))
        self.paint.setPen(QPen(QBrush(new_color), 3, Qt.SolidLine, Qt.RoundCap))
        self.paint.drawEllipse(2, 2, 46, 46)
        self.icon.setPixmap(self.picture)
        self.paint.end()

        # Set new score and new remaining pieces labels
        self.score.setText("Score: " + str(player.score))
        self.remaining_pieces.setText("Remaining pieces: " + str(player.remaining_pieces))


# Class about the toolbar which display information about players and the game option
class GameOptions:
    def __init__(self):

        # Get global game object and player colors
        global g_game
        global g_color_player_one
        global g_color_player_two

        # Set a copy of the game object to be able to modify its information
        self.game = g_game

        # Creation of a toolBar and block it to the right side
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)

        # Creation of two widgets which represent players in the scoreboard
        self.player1_part = QWidget()
        self.player2_part = QWidget()

        # Creation of graphical players parts and place them in the widget
        self.player1 = GameOptionPlayer(self.game.players[0], g_color_player_one)
        self.player1_part.setLayout(self.player1.layout)

        self.player2 = GameOptionPlayer(self.game.players[1], g_color_player_two)
        self.player2_part.setLayout(self.player2.layout)

        # Placing all elements which are present in the scoreboard like players or game options
        self.tool_bar.addWidget(self.player1_part)

        # Add a separator to distinguish both players
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.player2_part)
        self.tool_bar.addSeparator()

        # Creation of the game options part with a checkbox
        # where the user can activate a blind color mode
        title = QLabel("Game options")
        font = title.font()
        font.setBold(True)
        font.setPointSize(16)
        title.setFont(font)
        checkBox_color = QCheckBox("Color blind Mode")
        checkBox_color.setChecked(True)

        # Set a callback to change all colors in the game
        checkBox_color.stateChanged.connect(self.change_color_mode)

        # Add the checkbox in the main layout
        self.tool_bar.addWidget(title)
        self.tool_bar.addWidget(checkBox_color)

    # Function to put the game colors in color blind mode
    def change_color_mode(self, state):

        # Get all colors
        global g_color_player_one
        global g_color_player_two
        global g_color_king
        global g_color_selected
        global g_color_selectable_case

        # If the checkbox is checked, go to color blind mode
        if state == Qt.Checked:
            g_color_player_one = QColor(0, 92, 232)
            g_color_player_two = QColor(12, 151, 8)
            g_color_king = QColor(255, 216, 0)
            g_color_selected = QColor(0, 255, 102)
            g_color_selectable_case = QColor(255, 98, 164)

        # Otherwise
        else:
            g_color_player_one = Qt.blue
            g_color_player_two = Qt.red
            g_color_king = Qt.yellow
            g_color_selected = Qt.green
            g_color_selectable_case = Qt.magenta

    # Update the background color to show who is the current player
    def update_current_player(self, current_id):
        if current_id == 2:
            self.player2_part.setStyleSheet("background-color: #89e8f9")
            self.player1_part.setStyleSheet("background-color: #FFFFFF")
        elif current_id == 1:
            self.player1_part.setStyleSheet("background-color: #89e8f9")
            self.player2_part.setStyleSheet("background-color: #FFFFFF")

    # Update both players
    def update(self):
        self.player1.update_player(self.game.players[0], g_color_player_one)
        self.player2.update_player(self.game.players[1], g_color_player_two)


# Class to build the right part of the how to play dialog with a title, a picture, and a description
class HowToPlayFragment:
    def __init__(self, title, desc, icon_path):
        self.widget = QWidget()

        # Create the main layout of the component
        layout = QVBoxLayout()

        # Create the picture which show the explication
        self.logo = QLabel()
        if icon_path is not "":
            self.picture = QPixmap(icon_path)
            self.logo.setPixmap(self.picture.scaled(400, 400))

        # Create the title with a larger font and in bold
        self.title = QLabel(title)
        font = self.title.font()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        # Create a label with the description
        self.description = QLabel(desc)

        # Add the title to the main layout with a spacing after it
        layout.addWidget(self.title)
        layout.addSpacing(5)

        # If an icon_path is given in parameter, it will add the picture to the layout
        if icon_path is not "":
            layout.addWidget(self.logo)
            layout.addSpacing(5)

        # Add the description in the layout
        layout.addWidget(self.description)

        # Set the main layout to the widget
        self.widget.setLayout(layout)


# Class which represents the 'How to play' dialog
# which explain all rules and possible moves allowed in the game
class HowToPlay(QDialog):
    def __init__(self):
        super().__init__()

        # Set a title to the dialog
        self.setWindowTitle("How to play ?")

        # Create a list with all parts with a minimal width
        self.left_list = QListWidget()
        self.left_list.setMinimumWidth(200)
        self.left_list.insertItems(0, ["Presentation & Goal", "Selection", "Movement", "Capture", "King", "Win condition"])

        # Create  all fragments which explain all parts like rules or movement allowed
        self.rules_part = HowToPlayFragment("Presentation & Goal", "Draught game is a two players game. \nThe goal is to capture all pieces of your openent",
                                            "")

        self.selection_part = HowToPlayFragment("Selection",
                                            "The player can select one piece when he clicks on it. One piece can be selected at the time.\nThe game will show him all possibilities he can do.",
                                                "./img/selection.png")

        self.movement_part = HowToPlayFragment("Movement",
                                               "When a piece is selected (i.e selection part) the player can select between all possibilities (colored cases)\nand select one to place the piece on this case.\nPieces can move forward by a single diagonal square",
                                               "./img/movement.png")

        self.capture_part = HowToPlayFragment("Capture",
                                               "When the piece is diagonally in front of an oponent, the player can capture it.\nTo do this, the player can just click on the colored square behind the piece\nHe will score and if he can capture a piece again, his turn continues and he can capture another piece.",
                                               "./img/capture.png")

        self.king_part = HowToPlayFragment("King",
                                              "A piece can be a King when it reach the oponent board side.\nThis piece is very important because he can move and capture behind him.",
                                              "./img/king.png")

        self.win_part = HowToPlayFragment("Win condition",
                                              "When a player reach 12 point at score. He wins the game. \nThen players can restart a new game or quit it.",
                                              "")

        # Create a widget to display correctly all parts
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.rules_part.widget)
        self.stack.addWidget(self.selection_part.widget)
        self.stack.addWidget(self.movement_part.widget)
        self.stack.addWidget(self.capture_part.widget)
        self.stack.addWidget(self.king_part.widget)
        self.stack.addWidget(self.win_part.widget)

        # Creation of the main layout with the list and all stacked parts
        layout = QHBoxLayout()
        layout.addWidget(self.left_list)
        layout.addWidget(self.stack)

        # Set the main layut to the dialog
        self.setLayout(layout)

        # Define a listener when the user clicks on an element in th list
        self.left_list.currentRowChanged.connect(self.display)

        # Define a size for the dialog
        self.setGeometry(800, 100, 500, 200)

        # Show the dialog
        self.show()

    # When the user clicks on a element in the list, it displays the correct part in the right
    def display(self, i):
        self.stack.setCurrentIndex(i)


# Represents a case object
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

    # Update the variable 'isSelected'
    def set_isSelected(self):
        self.isSelected = not self.isSelected

    # Return the color of the case
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

        # Get all colors
        global g_color_player_one
        global g_color_player_two
        global g_color_king
        global g_color_selected
        global g_color_selectable_case

        # Set a title to the window and a default size to the game board
        self.resize(1005, 800)
        self.setWindowTitle('Draught Game')

        # Init the logic game board
        self.init_game_array()

        # Create the game board background and fill it with the white color
        self.image = QImage(QSize(800, 800), QImage.Format_RGB32)
        self.fillColor = Qt.white
        self.image.fill(self.fillColor)

        # Place the image in a label
        self.board = QLabel()
        self.setMinimumSize(1, 1)
        self.board.setPixmap(QPixmap(self.image))

        # Set the board in the central of the window
        self.setCentralWidget(self.board)

        # Set a status bar to display some information about the menu
        self.statusBar()

        # Create the menuBar to display menus like 'File' or 'Help'
        self.menubar = self.menuBar()

        # Create all menus
        self.setMyMenuBar()

        # Get the global game object and make a copy to able to modify it
        global g_game
        self.game = g_game

        # Set the score board at the right and set the current player to the first one
        self.game_options = GameOptions()
        self.addToolBar(Qt.RightToolBarArea, self.game_options.tool_bar)
        self.game_options.update_current_player(self.game.current_player.id)

        # Create a timer to make a countdown for the player turn duration
        timer = QTimer(self)
        timer.setSingleShot(False)

        # Call this function when the timer reaches 0
        timer.timeout.connect(self.update_timer)

        # Set the timer duration (here just one second)
        timer.start(1000)

        # Set some useful variables and the current player in the logic part
        self.FuturPositionList = []
        self.current_select = []
        self.caseIsSelected = False
        self.turnContinue = False
        self.current_player = 1

        # Show the window
        self.show()

    # Crate and set all menus contained in the menuBar
    def setMyMenuBar(self):

        # Create two menus
        fileMenu = self.menubar.addMenu("Game")
        helpMenu = self.menubar.addMenu("Help")

        # Add the 'Quit the game' menu with a shortcut and a callback function
        quit_action = QAction(QIcon("../../cat.jpeg"), "&Quit the game", self.menubar)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the application  (Ctrl+Q)")
        quit_action.triggered.connect(self.quitGame)
        fileMenu.addAction(quit_action)

        # Add the 'Reset the game' menu with a shortcut and a callback function
        reset_action = QAction(QIcon("../../cat.jpeg"), "&Reset the game", self.menubar)
        reset_action.setShortcut("Ctrl+R")
        reset_action.setStatusTip("Reset the game   (Ctrl+R)")
        reset_action.triggered.connect(self.resetGame)
        fileMenu.addAction(reset_action)

        # Add the 'How to play' menu with a shortcut and a callback function
        how_to_play = QAction(QIcon("../../cat.jpeg"), "How to play &?", self.menubar)
        how_to_play.setShortcut("Ctrl+?")
        how_to_play.setStatusTip("Display the game manual   (Ctrl+?)")
        how_to_play.triggered.connect(self.displayHowToPlay)
        helpMenu.addAction(how_to_play)

    # Function called when the user select 'Quit the game' in proposed menus
    # It will close the game
    def quitGame(self):
        self.close()

    # Function called when the user select 'Reset the game' in proposed menus
    # It will reset the board and reset all players information and set the player 1 as the current player
    def resetGame(self):
        self.init_game_array()
        self.current_player = 1
        self.game.reset()
        self.update()

    # Function called when the user select 'How to play ?' in proposed menus
    # It will show the How to play dialog
    def displayHowToPlay(self):
        self.how_to_play = HowToPlay()

    # Initialize an array which represent our board
    # Set all players pieces
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

    # Update the current player
    def update_current_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        self.game.change_player()

        # Clear all selectable cases
        self.clear_selectable()
        self.caseIsSelected = False
        self.turnContinue = False

    # Function when a player's timer reached zero, it will display a pop-up to quit the game or restart another one
    def update_timer(self):
        if self.game.current_player.timerleft <= 0:

            # Create the popup with buttons and texts
            ret = QMessageBox.question(self, "The game is finihed !",
                                       "Player" + str(
                                           self.game.current_player.id) + " takes too longer to play ! So you loose this game\n\n You can restart the restart the game of quit it",
                                       QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
            # If the user clicks one the Close button, it will close the game
            if ret == QMessageBox.Close:
                self.close()

            # If the user clicks on the Retry, it will reset the game and all graphic elements
            if ret == QMessageBox.Retry:
                self.FuturPositionList = []
                self.current_select = []
                self.caseIsSelected = False
                self.turnContinue = False
                self.current_player = 1
                self.init_game_array()
                self.game.reset()
                self.game_options.update_current_player(self.current_player)
                self.update()
            return

        # Update timers of all players
        if self.game.current_player.id == 1:
            self.game_options.player1.updateTimer()
        if self.game.current_player.id == 2:
            self.game_options.player2.updateTimer()
        self.game_options.update_current_player(self.game.current_player.id)
        self.update()

    # Prints all elements of the board
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        self.boardHeight = self.board.height()
        self.boardWidth = self.board.width()
        self.board.clear()

        # Update the size of the board according to the size of the board container
        self.board.setPixmap(QPixmap.fromImage(self.image.scaled(self.boardWidth, self.boardHeight, Qt.IgnoreAspectRatio)))
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect())
        posY = 0
        posX = 0

        for y in range(0, 8):
            for x in range(0, 8):
                painter = QPainter(self.board.pixmap())
                color = self.gameList[y][x].get_color()
                painter.setPen(QPen(color, 1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
                brush = QBrush(color, Qt.SolidPattern)
                rect = QRect(posX, posY, int(self.boardWidth / 8), int(self.boardHeight / 8))
                painter.drawRect(rect)
                painter.fillRect(rect, brush)

                # if there is something on the case
                if self.gameList[y][x].isPlayer != 0:
                    if self.gameList[y][x].isPlayer == 1:  # if it's the first team we choose blue
                        color_player = g_color_player_one

                    # else we choose red for the second team
                    else:
                        color_player = g_color_player_two
                    painter.setBrush(QBrush(color_player))

                    # if the pawn is selected we draw a green circle around it
                    if self.gameList[y][x].isSelected:
                        painter.setPen(QPen(QBrush(g_color_selected), 3, Qt.SolidLine, Qt.RoundCap))
                    else:
                        painter.setPen(QPen(QBrush(color_player), 1, Qt.SolidLine, Qt.RoundCap))
                    painter.drawEllipse(posX, posY, int(self.boardWidth / 8 - 2/100), int(self.boardHeight / 8 - 2/100))

                    # if it's a king we draw a yellow "crown" on it
                    if self.gameList[y][x].isKing:
                        painter.setPen(QPen(g_color_king, 5, Qt.SolidLine, Qt.RoundCap))
                        painter.drawEllipse(posX + int(self.boardWidth / 8 / 4), posY + int(self.boardHeight / 8 / 4),
                                            int(self.boardWidth / 8 / 2), int(self.boardHeight / 8 / 2))
                posX += int(self.boardWidth / 8)
                painter.end()
            posY += int(self.boardHeight / 8)
            posX = 0

        # Update the board and the game
        self.update()
        self.game_options.update()
        self.game_options.update_current_player(self.game.current_player.id)

    # Trigger when there is a mouse event
    def mousePressEvent(self, event):

        # Checks if the pressed button if the left button
        if event.button() == Qt.LeftButton:
            self.point = event.pos()

            # Set coordinates of the click in the data array
            self.pointX = floor(event.x() / (self.board.pixmap().width() / 8))
            self.pointY = floor((event.y() - 20) / (self.board.pixmap().height() / 8))
            new_point = QPoint(self.pointY, self.pointX)  # get the point where we clicked

            # if it's a potential position of the selected pawn
            if (
                    self.caseIsSelected and new_point in self.FuturPositionList) or self.turnContinue:

                # if it's a new valid position we change our pawn for its new position
                if new_point in self.FuturPositionList:
                    self.gameList[self.current_select[0]][self.current_select[1]].isPlayer = 0
                    self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False

                    # If the case has a King piece we set the old one to false and the new one to true
                    if self.gameList[self.current_select[0]][self.current_select[1]].isKing:
                        self.gameList[self.current_select[0]][self.current_select[1]].isKing = False
                        self.gameList[self.pointY][self.pointX].isKing = True
                    self.gameList[self.pointY][self.pointX].isPlayer = self.current_player

                    # we check if the new position of our pawn transform it to a king
                    if self.check_is_new_king(self.pointY):
                        self.gameList[self.pointY][self.pointX].isKing = True
                    old_point = QPoint(self.current_select[0], self.current_select[1])

                    # we check if we capture an enemy or not (the function return coordinates of the enemy in asked direction)
                    enemy_point = self.check_if_ennemy(new_point, old_point)

                    # if we don't capture anybody the turn ended
                    if enemy_point is None:
                        self.update_current_player()

                    # Otherwise we recheck if our new position give us the possibility of capturing another enemy
                    else:
                        self.gameList[enemy_point.x()][enemy_point.y()].isPlayer = 0
                        self.gameList[enemy_point.x()][enemy_point.y()].isKing = False

                        # We update the score of the current player and remaining pieces of the other one
                        self.game.current_player.score += 1
                        if self.game.current_player.id == 1:
                            self.game.players[1].remaining_pieces -= 1
                        else:
                            self.game.players[0].remaining_pieces -= 1

                        # We check if the current player can play again
                        if self.check_enemy_position(self.current_player, self.pointX, self.pointY) is True:
                            self.turnContinue = True
                        else:
                            self.update_current_player()
                else:
                    return

            # This part is to select a new pawn and find what is possible to do with it
            if self.pointX in range(0, 8) and self.pointY in range(0, 8):
                if self.gameList[self.pointY][self.pointX].isPlayer == self.current_player:
                    self.caseIsSelected = True

                    # We update our selected selected piece and check where it can go
                    if self.current_select:
                        self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False
                        self.current_select.pop(0)
                        self.current_select.pop(0)
                        self.clear_selectable()
                    self.gameList[self.pointY][self.pointX].isSelected = True
                    self.current_select.append(self.pointY)
                    self.current_select.append(self.pointX)
                    self.find_futur_postition(self.pointX, self.pointY)

                    # If a piece can't capture another one again we change the turn
                    if self.check_selectable() is False and self.turnContinue is True:
                        self.gameList[self.current_select[0]][self.current_select[1]].isSelected = False
                        self.current_select.pop(0)
                        self.current_select.pop(0)
                        self.update_current_player()

        # Display a pop-up to display the winner and the possibility to close or restart the game
        if self.game.check_winner() == 1:
            ret = QMessageBox.question(self, "The game is finihed !",
                                       "The winner is the Player 1 !\n\n You can restart the restart the game of quit it",
                                       QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
            if ret == QMessageBox.Close:
                self.close()
            if ret == QMessageBox.Retry:
                self.game_options.update_current_player(self.current_player)
                self.init_game_array()
                self.game.reset()
                self.current_player = 1
                self.update()
            return
        elif self.game.check_winner() == 2:
            ret = QMessageBox.question(self, "The game is finihed !",
                                       "The winner is the Player 2s !\n\n You can restart the restart the game of quit it",
                                       QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
            if ret == QMessageBox.Close:
                self.close()
            if ret == QMessageBox.Retry:
                self.game_options.update_current_player(self.current_player)
                self.init_game_array()
                self.game.reset()
                self.current_player = 1
                self.update()
            return

    # Override the close event to close all opened windows
    def closeEvent(self, event):
        QApplication.closeAllWindows()

    # used to find our future potential positions and enemies
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

    # when we find an enemy around of our pawn we check if there is an empty case to capture it
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

    # used when we just capture an enemy and continue the turn,
    # we check here if there is again an enemy to capture around our new position
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

    # if check_enemy_position find an enemy we check here if we can capture it
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

    # if we pass through an enemy during our movement we capture it
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
        else:
            return None

    # check if the new position of our selected pawn transform it to a king
    def check_is_new_king(self, y):
        if self.current_player == 1 and y == 7:
            return True
        elif self.current_player == 2 and y == 0:
            return True
        return False


# Main function of the application
# It will start the game bord class
if __name__ == '__main__':
    app = QApplication([])
    draught = GameBoard()
    sys.exit(app.exec_())
