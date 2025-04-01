# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chord_uidfXEdX.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QLayout, QMainWindow, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
                               QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(862, 558)
        MainWindow.setStyleSheet(u"""
            background-color: rgb(38, 28, 44);
            color: rgb(255, 255, 255);
            border-color: rgb(110, 133, 178);
        """)

        # Central widget and main layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Main vertical layout
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Central container widget
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Chords Frame
        self.chords_frame = QFrame()
        self.chords_frame.setObjectName(u"chords_frame")
        self.chords_frame.setStyleSheet(u"")
        self.chords_frame.setFrameShape(QFrame.Shape.NoFrame)

        # Horizontal layout for chords
        self.horizontalLayout_15 = QHBoxLayout(self.chords_frame)
        self.horizontalLayout_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Chord 1 Layout
        self.lyout_1_chord = QVBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.label_name = QLabel(self.chords_frame)
        font = QFont()
        font.setFamilies([u"MS Sans Serif"])
        font.setPointSize(6)
        font.setBold(True)
        self.label_name.setFont(font)
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label_name)

        self.label_conf = QLabel(self.chords_frame)
        self.label_conf.setFont(font)
        self.label_conf.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label_conf)
        self.lyout_1_chord.addLayout(self.verticalLayout)

        # Chord image 1 with fixed size
        self.chord_and_text = QVBoxLayout()
        self.chord_pic = QLabel(self.chords_frame)
        self.chord_pic.setObjectName(u"chord_pic")
        # self.chord_pic.setMinimumSize(QSize(160, 400))
        # self.chord_pic.setMaximumSize(QSize(160, 400))
        self.chord_pic.setPixmap(QPixmap(u":/chord_positions/chord_positions/chart_tiny.png"))
        self.chord_pic.setScaledContents(True)
        self.chord_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chord_and_text.addWidget(self.chord_pic)
        self.lyout_1_chord.addLayout(self.chord_and_text)

        # Navigation buttons 1
        self.lyout_1_chord_btns_2 = QHBoxLayout()
        self.bck_btn_1_chord = QPushButton(self.chords_frame)
        self.bck_btn_1_chord.setStyleSheet(u"border-color: rgb(110, 133, 178);")
        icon = QIcon()
        icon.addFile(u":/newPrefix/arrow_left.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bck_btn_1_chord.setIcon(icon)
        self.lyout_1_chord_btns_2.addWidget(self.bck_btn_1_chord)

        self.fwd_btn_1_chord = QPushButton(self.chords_frame)
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix/arrow_right.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fwd_btn_1_chord.setIcon(icon1)
        self.lyout_1_chord_btns_2.addWidget(self.fwd_btn_1_chord)
        self.lyout_1_chord.addLayout(self.lyout_1_chord_btns_2)
        self.horizontalLayout_15.addLayout(self.lyout_1_chord)

        # Repeat similar structure for Chord 2 and 3 with fixed sizes
        # Chord 2
        self.lyout_2_chord = QVBoxLayout()
        self.verticalLayout_2 = QVBoxLayout()
        self.label_name_2 = QLabel(self.chords_frame)
        self.label_name_2.setFont(font)
        self.label_name_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_name_2)

        self.label_conf_2 = QLabel(self.chords_frame)
        font1 = QFont()
        font1.setFamilies([u"MS Sans Serif"])
        font1.setPointSize(9)
        font1.setBold(True)
        self.label_conf_2.setFont(font1)
        self.label_conf_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_conf_2)
        self.lyout_2_chord.addLayout(self.verticalLayout_2)

        # Chord image 2
        self.chord_and_text_2 = QVBoxLayout()
        self.chord_pic_2 = QLabel(self.chords_frame)
        # self.chord_pic_2.setMinimumSize(QSize(160, 400))
        # self.chord_pic_2.setMaximumSize(QSize(160, 400))
        self.chord_pic_2.setPixmap(QPixmap(u":/chord_positions/chord_positions/chart_tiny.png"))
        self.chord_pic_2.setScaledContents(True)
        self.chord_pic_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chord_and_text_2.addWidget(self.chord_pic_2)
        self.lyout_2_chord.addLayout(self.chord_and_text_2)

        # Navigation buttons 2
        self.lyout_2_chord_btns_2 = QHBoxLayout()
        self.bck_btn_2_chord = QPushButton(self.chords_frame)
        self.bck_btn_2_chord.setIcon(icon)
        self.lyout_2_chord_btns_2.addWidget(self.bck_btn_2_chord)

        self.fwd_btn_2_chord = QPushButton(self.chords_frame)
        self.fwd_btn_2_chord.setIcon(icon1)
        self.lyout_2_chord_btns_2.addWidget(self.fwd_btn_2_chord)
        self.lyout_2_chord.addLayout(self.lyout_2_chord_btns_2)
        self.horizontalLayout_15.addLayout(self.lyout_2_chord)

        # Chord 3
        self.lyout_3_chord = QVBoxLayout()
        self.verticalLayout_3 = QVBoxLayout()
        self.label_name_3 = QLabel(self.chords_frame)
        font2 = QFont()
        font2.setFamilies([u"MS Sans Serif"])
        font2.setBold(True)
        self.label_name_3.setFont(font2)
        self.label_name_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3.addWidget(self.label_name_3)

        self.label_conf_3 = QLabel(self.chords_frame)
        self.label_conf_3.setFont(font2)
        self.label_conf_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3.addWidget(self.label_conf_3)
        self.lyout_3_chord.addLayout(self.verticalLayout_3)

        # Chord image 3
        self.chord_and_text_3 = QVBoxLayout()
        self.chord_pic_3 = QLabel(self.chords_frame)
        # self.chord_pic_3.setMinimumSize(QSize(160, 400))
        # self.chord_pic_3.setMaximumSize(QSize(160, 400))
        self.chord_pic_3.setPixmap(QPixmap(u":/chord_positions/chord_positions/chart_tiny.png"))
        self.chord_pic_3.setScaledContents(True)
        self.chord_pic_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chord_and_text_3.addWidget(self.chord_pic_3)
        self.lyout_3_chord.addLayout(self.chord_and_text_3)

        # Navigation buttons 3
        self.lyout_3_chord_btns = QHBoxLayout()
        self.bck_btn_3_chord = QPushButton(self.chords_frame)
        self.bck_btn_3_chord.setIcon(icon)
        self.lyout_3_chord_btns.addWidget(self.bck_btn_3_chord)

        self.fwd_btn_3_chord = QPushButton(self.chords_frame)
        self.fwd_btn_3_chord.setIcon(icon1)
        self.lyout_3_chord_btns.addWidget(self.fwd_btn_3_chord)
        self.lyout_3_chord.addLayout(self.lyout_3_chord_btns)
        self.horizontalLayout_15.addLayout(self.lyout_3_chord)

        # Add chords frame to container
        self.container_layout.addWidget(self.chords_frame)

        # Functions Frame
        self.funct_frame = QFrame()
        self.verticalLayout_16 = QVBoxLayout(self.funct_frame)
        self.verticalLayout_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Function buttons
        self.rtime_btn = QPushButton(self.funct_frame)
        font3 = QFont()
        font3.setFamilies([u"MS Sans Serif"])
        font3.setPointSize(10)
        font3.setBold(True)
        self.rtime_btn.setFont(font3)
        icon2 = QIcon()
        icon2.addFile(u":/newPrefix/graphic_eq.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rtime_btn.setIcon(icon2)
        self.verticalLayout_16.addWidget(self.rtime_btn)

        self.imp_btn = QPushButton(self.funct_frame)
        self.imp_btn.setFont(font3)
        icon3 = QIcon()
        icon3.addFile(u":/newPrefix/file_open.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.imp_btn.setIcon(icon3)
        self.verticalLayout_16.addWidget(self.imp_btn)

        self.rec_btn = QPushButton(self.funct_frame)
        self.rec_btn.setFont(font3)
        icon4 = QIcon()
        icon4.addFile(u":/newPrefix/radio_button_unchecked.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rec_btn.setIcon(icon4)
        self.verticalLayout_16.addWidget(self.rec_btn)

        self.exp_btn = QPushButton(self.funct_frame)
        self.exp_btn.setFont(font3)
        icon5 = QIcon()
        icon5.addFile(u":/newPrefix/file_export.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exp_btn.setIcon(icon5)
        self.verticalLayout_16.addWidget(self.exp_btn)

        self.play_btn = QPushButton(self.funct_frame)
        self.play_btn.setFont(font3)
        icon6 = QIcon()
        icon6.addFile(u":/newPrefix/play_circle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.play_btn.setIcon(icon6)
        self.verticalLayout_16.addWidget(self.play_btn)

        # Add functions frame to container
        self.container_layout.addWidget(self.funct_frame)
        self.main_layout.addWidget(self.container)

        # Menu bar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 862, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Guitar Chord Detector", None))
        self.label_name.setText(QCoreApplication.translate("MainWindow", u"Chord", None))
        self.label_conf.setText(QCoreApplication.translate("MainWindow", u"(Unknown confidence)", None))
        self.label_name_2.setText(QCoreApplication.translate("MainWindow", u"Chord", None))
        self.label_conf_2.setText(QCoreApplication.translate("MainWindow", u"(Unknown confidence)", None))
        self.label_name_3.setText(QCoreApplication.translate("MainWindow", u"Chord", None))
        self.label_conf_3.setText(QCoreApplication.translate("MainWindow", u"(Unknown confidence)", None))
        self.rtime_btn.setText(QCoreApplication.translate("MainWindow", u"Start Realtime Detection", None))
        self.imp_btn.setText(QCoreApplication.translate("MainWindow", u"Import Audio", None))
        self.rec_btn.setText(QCoreApplication.translate("MainWindow", u"Record Audio", None))
        self.exp_btn.setText(QCoreApplication.translate("MainWindow", u"Export Recording", None))
        self.play_btn.setText(QCoreApplication.translate("MainWindow", u"Play", None))