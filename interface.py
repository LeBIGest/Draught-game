import sys

from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QMenuBar, QVBoxLayout, QSplitter, QFrame, QWidget, \
    QPushButton, QToolBar, QLabel, QSizePolicy, QAction, QDialog, QGridLayout


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
        picture = QPixmap(50, 50)
        picture.fill(Qt.white)
        paint = QPainter(picture)
        paint.setBrush(QBrush(color))
        paint.setPen(QPen(QBrush(color), 3, Qt.SolidLine, Qt.RoundCap))
        paint.drawEllipse(2, 2, 46, 46)
        self.icon.setPixmap(picture)

        self.header.addWidget(self.icon)
        self.header.addLayout(self.title)

        paint.end()

        self.score = QLabel("Score: " + str(self.player.score))
        self.jumps = QLabel("Jumps: " + str(self.player.jumps))

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.header)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.score)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.jumps)
        self.layout.addSpacing(10)

    def update_players(self, player):
        self.score.setText("Score: " + str(player.score))
        self.score.setText("Jumps: " + str(player.jumps))


    def updateTimer(self):

        self.player.timerleft -= 1
        min, sec = divmod(self.player.timerleft, 60)
        self.time_passed.setText("Time left : {:02d}:{:02d}".format(min, sec))


class GameOptions:
    def __init__(self):

        global g_game

        game = g_game

        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)

        self.player1_part = QWidget()
        self.player2_part = QWidget()

        self.player1 = GameOptionPlayer(game.players[0], Qt.darkMagenta)
        self.player1_part.setLayout(self.player1.layout)

        self.player2 = GameOptionPlayer(game.players[1], Qt.darkGreen)
        self.player2_part.setLayout(self.player2.layout)
        # player2_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.tool_bar.addWidget(self.player1_part)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.player2_part)

    def update_current_player(self, current_id):
        if current_id == 2:
            self.player2_part.setStyleSheet("background-color: #89e8f9")
            self.player1_part.setStyleSheet("background-color: #FFFFFF")
        else:
            self.player1_part.setStyleSheet("background-color: #89e8f9")
            self.player2_part.setStyleSheet("background-color: #FFFFFF")


class HowToPlay(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("How to play ?")

        self.show()


class GameToolBar:
    def __init__(self):

        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)

        self.board = QWidget()

        pm = QImage(800, 800, QImage.Format_RGB32)
        pm.fill(Qt.blue)
        lbl = QLabel()
        lbl.setPixmap(QPixmap(pm))
        self.tool_bar.addWidget(lbl)


class DraughtGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Draught Game")
        self.setGeometry(400, 400, 600, 400)
        self.move(500, 200)

        self.statusBar()

        self.menubar = self.menuBar()

        self.setMyMenuBar()

        global g_game
        self.game = g_game

        self.game_options = GameOptions()
        self.game_options.update_current_player(self.game.current_player.id)

        self.game_tool_bar = GameToolBar()

        self.addToolBar(Qt.RightToolBarArea, self.game_options.tool_bar)
        self.addToolBar(Qt.LeftToolBarArea, self.game_tool_bar.tool_bar)

        self.setFixedHeight(800)

        timer = QTimer(self)
        timer.setSingleShot(False)
        timer.timeout.connect(self.update_timer)
        timer.start(1000)

    def setMyMenuBar(self):
        fileMenu = self.menubar.addMenu("Game")

        quit_action = QAction(QIcon("../../cat.jpeg"), "Quit the game", self.menubar)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit the application  (Ctrl+Q)")
        quit_action.triggered.connect(self.quitGame)
        fileMenu.addAction(quit_action)

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

    def displayHowToPlay(self):
        self.how_to_play = HowToPlay()

    def mousePressEvent(self, event):
        self.game.change_player()

    def update_timer(self):
        if self.game.current_player.id == 1:
            self.game_options.player1.updateTimer()
        if self.game.current_player.id == 2:
            self.game_options.player2.updateTimer()
        self.game_options.update_current_player(self.game.current_player.id)
        self.update()

    def closeEvent(self, event):
        QApplication.closeAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = DraughtGameWindow()
    game.show()
    sys.exit(app.exec_())
