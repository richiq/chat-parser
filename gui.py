# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import Qt, QSize, QRect, QCoreApplication, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor
from PyQt5.QtWidgets import (
                                QVBoxLayout, QSizePolicy, QTreeWidget,  QGridLayout, QHBoxLayout, QWidget,
                                QComboBox, QSpinBox, QCheckBox, QLabel, QSpacerItem, QPushButton, QTabWidget,
                                QLineEdit, QAbstractItemView, QToolButton, QLayout, QFrame, QAbstractScrollArea,
                                QScrollArea
                            )


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1116, 690)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.testButton = QPushButton(self.centralwidget)
        self.testButton.setObjectName("testButton")
        self.verticalLayout_2.addWidget(self.testButton, 0, Qt.AlignBottom)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 1, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_tabWidget = QTabWidget(self.centralwidget)
        self.main_tabWidget.setAutoFillBackground(True)
        self.main_tabWidget.setTabShape(QTabWidget.Rounded)
        self.main_tabWidget.setObjectName("main_tabWidget")
        self.messagesTab = QWidget()
        self.messagesTab.setObjectName("messagesTab")
        self.gridLayout_5 = QGridLayout(self.messagesTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.exact_searchCheckbox = QCheckBox(self.messagesTab)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exact_searchCheckbox.sizePolicy().hasHeightForWidth())
        self.exact_searchCheckbox.setSizePolicy(sizePolicy)
        self.exact_searchCheckbox.setObjectName("exact_searchCheckbox")
        self.gridLayout_9.addWidget(self.exact_searchCheckbox, 8, 0, 1, 1)
        self.searchLine = QLineEdit(self.messagesTab)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLine.sizePolicy().hasHeightForWidth())
        self.searchLine.setSizePolicy(sizePolicy)
        self.searchLine.setClearButtonEnabled(True)
        self.searchLine.setObjectName("searchLine")
        self.gridLayout_9.addWidget(self.searchLine, 6, 0, 1, 1)
        self.linkLine = QLineEdit(self.messagesTab)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linkLine.sizePolicy().hasHeightForWidth())
        self.linkLine.setSizePolicy(sizePolicy)
        self.linkLine.setEchoMode(QLineEdit.Normal)
        self.linkLine.setReadOnly(True)
        self.linkLine.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.linkLine.setClearButtonEnabled(False)
        self.linkLine.setObjectName("linkLine")
        self.gridLayout_9.addWidget(self.linkLine, 6, 9, 1, 1, Qt.AlignRight)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem2, 6, 2, 1, 1)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem3, 6, 4, 1, 1)
        self.total_messagesLabel = QLabel(self.messagesTab)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_messagesLabel.sizePolicy().hasHeightForWidth())
        self.total_messagesLabel.setSizePolicy(sizePolicy)
        self.total_messagesLabel.setObjectName("total_messagesLabel")
        self.gridLayout_9.addWidget(self.total_messagesLabel, 6, 3, 1, 1)
        self.messageTree = QTreeWidget(self.messagesTab)
        self.messageTree.setMouseTracking(True)
        self.messageTree.setAlternatingRowColors(True)
        self.messageTree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.messageTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.messageTree.setExpandsOnDoubleClick(True)
        self.messageTree.setObjectName("messageTree")
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        self.messageTree.headerItem().setForeground(0, brush)
        self.gridLayout_9.addWidget(self.messageTree, 5, 0, 1, 10)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.hideButton = QToolButton(self.messagesTab)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideButton.sizePolicy().hasHeightForWidth())
        self.hideButton.setSizePolicy(sizePolicy)
        self.hideButton.setText("")
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout_5.addWidget(self.hideButton, 0, Qt.AlignHCenter)
        self.undoButton = QToolButton(self.messagesTab)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.undoButton.sizePolicy().hasHeightForWidth())
        self.undoButton.setSizePolicy(sizePolicy)
        self.undoButton.setMinimumSize(QSize(28, 22))
        self.undoButton.setLayoutDirection(Qt.LeftToRight)
        self.undoButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.undoButton.setObjectName("undoButton")
        self.horizontalLayout_5.addWidget(self.undoButton, 0, Qt.AlignHCenter)
        self.gridLayout_9.addLayout(self.horizontalLayout_5, 6, 6, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_9, 0, 3, 1, 1)
        self.main_tabWidget.addTab(self.messagesTab, "")
        self.photoTab = QWidget()
        self.photoTab.setLayoutDirection(Qt.LeftToRight)
        self.photoTab.setObjectName("photoTab")
        self.gridLayout_2 = QGridLayout(self.photoTab)
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 5, 1, 1)
        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem5, 2, 4, 1, 1)
        self.main_tabWidget.addTab(self.photoTab, "")
        self.videoTab = QWidget()
        self.videoTab.setObjectName("videoTab")
        self.main_tabWidget.addTab(self.videoTab, "")
        self.documentsTab = QWidget()
        self.documentsTab.setObjectName("documentsTab")
        self.main_tabWidget.addTab(self.documentsTab, "")
        self.analysisTab = QWidget()
        self.analysisTab.setObjectName("analysisTab")
        self.gridLayout_7 = QGridLayout(self.analysisTab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.analysis_stickers_amountLabel = QLabel(self.analysisTab)
        self.analysis_stickers_amountLabel.setObjectName("analysis_stickers_amountLabel")
        self.gridLayout_7.addWidget(self.analysis_stickers_amountLabel, 4, 0, 1, 1)
        self.analysis_symbols_amountLabel = QLabel(self.analysisTab)
        self.analysis_symbols_amountLabel.setObjectName("analysis_symbols_amountLabel")
        self.gridLayout_7.addWidget(self.analysis_symbols_amountLabel, 3, 0, 1, 1)
        self.analysis_emoji_amountLabel = QLabel(self.analysisTab)
        self.analysis_emoji_amountLabel.setObjectName("analysis_emoji_amountLabel")
        self.gridLayout_7.addWidget(self.analysis_emoji_amountLabel, 5, 0, 1, 1)
        spacerItem6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem6, 6, 0, 1, 1)
        self.label_9 = QLabel(self.analysisTab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_7.addWidget(self.label_9, 7, 0, 1, 1)
        self.analysis_words_amountLabel = QLabel(self.analysisTab)
        self.analysis_words_amountLabel.setObjectName("analysis_words_amountLabel")
        self.gridLayout_7.addWidget(self.analysis_words_amountLabel, 2, 0, 1, 1)
        self.label_2 = QLabel(self.analysisTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem7, 1, 0, 1, 1)
        self.analysis_tabWidget = QTabWidget(self.analysisTab)
        self.analysis_tabWidget.setObjectName("analysis_tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.analysis_wordsTree = QTreeWidget(self.tab)
        self.analysis_wordsTree.setObjectName("analysis_wordsTree")
        self.verticalLayout.addWidget(self.analysis_wordsTree)
        self.analysis_tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.analysis_tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.analysis_emojisTree = QTreeWidget(self.tab_3)
        self.analysis_emojisTree.setStyleSheet("background-color: #1F1F1F")
        self.analysis_emojisTree.setObjectName("analysis_emojisTree")
        self.verticalLayout_3.addWidget(self.analysis_emojisTree)
        self.analysis_tabWidget.addTab(self.tab_3, "")
        self.gridLayout_7.addWidget(self.analysis_tabWidget, 9, 0, 1, 1)
        self.main_tabWidget.addTab(self.analysisTab, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.settings_tabWidget = QTabWidget(self.tab_4)
        self.settings_tabWidget.setMaximumSize(QSize(16777215, 162))
        self.settings_tabWidget.setTabPosition(QTabWidget.North)
        self.settings_tabWidget.setTabShape(QTabWidget.Rounded)
        self.settings_tabWidget.setObjectName("settings_tabWidget")
        self.textTab = QWidget()
        self.textTab.setObjectName("textTab")
        self.horizontalLayout_2 = QHBoxLayout(self.textTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.symbLayout = QGridLayout()
        self.symbLayout.setObjectName("symbLayout")
        self.and_orCombobox = QComboBox(self.textTab)
        self.and_orCombobox.setMinimumSize(QSize(49, 20))
        self.and_orCombobox.setMaximumSize(QSize(66, 20))
        self.and_orCombobox.setObjectName("and_orCombobox")
        self.and_orCombobox.addItem("")
        self.and_orCombobox.addItem("")
        self.symbLayout.addWidget(self.and_orCombobox, 1, 1, 1, 1)
        self.min_symbolsCombobox = QComboBox(self.textTab)
        self.min_symbolsCombobox.setMinimumSize(QSize(49, 20))
        self.min_symbolsCombobox.setMaximumSize(QSize(66, 20))
        self.min_symbolsCombobox.setObjectName("min_symbolsCombobox")
        self.min_symbolsCombobox.addItem("")
        self.min_symbolsCombobox.addItem("")
        self.symbLayout.addWidget(self.min_symbolsCombobox, 3, 1, 1, 1, Qt.AlignBottom)
        self.min_symbolsSpinbox = QSpinBox(self.textTab)
        self.min_symbolsSpinbox.setWrapping(True)
        self.min_symbolsSpinbox.setMinimum(1)
        self.min_symbolsSpinbox.setMaximum(9999)
        self.min_symbolsSpinbox.setProperty("value", 1)
        self.min_symbolsSpinbox.setObjectName("min_symbolsSpinbox")
        self.symbLayout.addWidget(self.min_symbolsSpinbox, 3, 2, 1, 1)
        self.min_wordsCheckbox = QCheckBox(self.textTab)
        self.min_wordsCheckbox.setText("")
        self.min_wordsCheckbox.setChecked(False)
        self.min_wordsCheckbox.setObjectName("min_wordsCheckbox")
        self.symbLayout.addWidget(self.min_wordsCheckbox, 0, 0, 1, 1)
        self.min_symbolsLabel = QLabel(self.textTab)
        self.min_symbolsLabel.setObjectName("min_symbolsLabel")
        self.symbLayout.addWidget(self.min_symbolsLabel, 3, 3, 1, 1)
        self.min_wordsLabel = QLabel(self.textTab)
        self.min_wordsLabel.setObjectName("min_wordsLabel")
        self.symbLayout.addWidget(self.min_wordsLabel, 0, 3, 1, 1)
        self.min_symbolsCheckbox = QCheckBox(self.textTab)
        self.min_symbolsCheckbox.setText("")
        self.min_symbolsCheckbox.setChecked(False)
        self.min_symbolsCheckbox.setObjectName("min_symbolsCheckbox")
        self.symbLayout.addWidget(self.min_symbolsCheckbox, 3, 0, 1, 1)
        self.min_wordsCombobox = QComboBox(self.textTab)
        self.min_wordsCombobox.setMinimumSize(QSize(49, 20))
        self.min_wordsCombobox.setMaximumSize(QSize(66, 20))
        self.min_wordsCombobox.setObjectName("min_wordsCombobox")
        self.min_wordsCombobox.addItem("")
        self.min_wordsCombobox.addItem("")
        self.symbLayout.addWidget(self.min_wordsCombobox, 0, 1, 1, 1)
        self.min_wordsSpinbox = QSpinBox(self.textTab)
        self.min_wordsSpinbox.setWrapping(True)
        self.min_wordsSpinbox.setMinimum(1)
        self.min_wordsSpinbox.setMaximum(9999)
        self.min_wordsSpinbox.setProperty("value", 1)
        self.min_wordsSpinbox.setObjectName("min_wordsSpinbox")
        self.symbLayout.addWidget(self.min_wordsSpinbox, 0, 2, 1, 1)
        self.horizontalLayout_2.addLayout(self.symbLayout)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        spacerItem9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.settings_tabWidget.addTab(self.textTab, "")
        self.dateTab = QWidget()
        self.dateTab.setObjectName("dateTab")
        self.settings_tabWidget.addTab(self.dateTab, "")
        self.usersTab = QWidget()
        self.usersTab.setObjectName("usersTab")
        self.settings_tabWidget.addTab(self.usersTab, "")
        self.verticalLayout_5.addWidget(self.settings_tabWidget)
        self.main_tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.main_tabWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem11, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 69, 666))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.fileButton = QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileButton.sizePolicy().hasHeightForWidth())
        self.fileButton.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/file.svg"), QIcon.Normal, QIcon.Off)
        self.fileButton.setIcon(icon)
        self.fileButton.setIconSize(QSize(24, 24))
        self.fileButton.setCheckable(False)
        self.fileButton.setAutoRaise(True)
        self.fileButton.setObjectName("fileButton")
        self.verticalLayout_7.addWidget(self.fileButton, 0, Qt.AlignHCenter|Qt.AlignTop)
        spacerItem12 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem12)
        self.settingsButton = QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsButton.sizePolicy().hasHeightForWidth())
        self.settingsButton.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("icons/settings.svg"), QIcon.Normal, QIcon.Off)
        self.settingsButton.setIcon(icon1)
        self.settingsButton.setIconSize(QSize(24, 24))
        self.settingsButton.setCheckable(True)
        self.settingsButton.setAutoRaise(True)
        self.settingsButton.setObjectName("settingsButton")
        self.verticalLayout_7.addWidget(self.settingsButton, 0, Qt.AlignHCenter|Qt.AlignVCenter)
        spacerItem13 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem13)
        self.settingsWidget = QFrame(self.scrollAreaWidgetContents)
        self.settingsWidget.setObjectName("settingsWidget")
        self.settingsLayout = QVBoxLayout(self.settingsWidget)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout.setSpacing(6)
        self.settingsLayout.setObjectName("settingsLayout")
        self.hastextButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hastextButton.sizePolicy().hasHeightForWidth())
        self.hastextButton.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("icons/hastext.svg"), QIcon.Normal, QIcon.Off)
        self.hastextButton.setIcon(icon2)
        self.hastextButton.setIconSize(QSize(24, 24))
        self.hastextButton.setCheckable(True)
        self.hastextButton.setAutoRaise(True)
        self.hastextButton.setObjectName("hastextButton")
        self.settingsLayout.addWidget(self.hastextButton, 0, Qt.AlignHCenter|Qt.AlignTop)
        self.notextButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notextButton.sizePolicy().hasHeightForWidth())
        self.notextButton.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addPixmap(QPixmap("icons/notext.svg"), QIcon.Normal, QIcon.Off)
        self.notextButton.setIcon(icon3)
        self.notextButton.setIconSize(QSize(24, 24))
        self.notextButton.setCheckable(True)
        self.notextButton.setAutoRaise(True)
        self.notextButton.setObjectName("notextButton")
        self.settingsLayout.addWidget(self.notextButton, 0, Qt.AlignHCenter|Qt.AlignTop)
        self.emojiButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emojiButton.sizePolicy().hasHeightForWidth())
        self.emojiButton.setSizePolicy(sizePolicy)
        self.emojiButton.setLayoutDirection(Qt.LeftToRight)
        icon4 = QIcon()
        icon4.addPixmap(QPixmap("icons/emoji-enabled.svg"), QIcon.Normal, QIcon.Off)
        self.emojiButton.setIcon(icon4)
        self.emojiButton.setIconSize(QSize(24, 24))
        self.emojiButton.setCheckable(True)
        self.emojiButton.setAutoExclusive(False)
        self.emojiButton.setAutoRaise(True)
        self.emojiButton.setObjectName("emojiButton")
        self.settingsLayout.addWidget(self.emojiButton, 0, Qt.AlignHCenter|Qt.AlignTop)
        self.lengthButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lengthButton.sizePolicy().hasHeightForWidth())
        self.lengthButton.setSizePolicy(sizePolicy)
        self.lengthButton.setLayoutDirection(Qt.LeftToRight)
        icon5 = QIcon()
        icon5.addPixmap(QPixmap("icons/length.svg"), QIcon.Normal, QIcon.Off)
        self.lengthButton.setIcon(icon5)
        self.lengthButton.setIconSize(QSize(24, 24))
        self.lengthButton.setCheckable(True)
        self.lengthButton.setAutoExclusive(False)
        self.lengthButton.setAutoRaise(True)
        self.lengthButton.setObjectName("lengthButton")
        self.settingsLayout.addWidget(self.lengthButton, 0, Qt.AlignHCenter|Qt.AlignTop)
        spacerItem14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.settingsLayout.addItem(spacerItem14)
        self.forwardButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forwardButton.sizePolicy().hasHeightForWidth())
        self.forwardButton.setSizePolicy(sizePolicy)
        self.forwardButton.setLayoutDirection(Qt.LeftToRight)
        icon6 = QIcon()
        icon6.addPixmap(QPixmap("icons/forward-enabled.svg"), QIcon.Normal, QIcon.Off)
        self.forwardButton.setIcon(icon6)
        self.forwardButton.setIconSize(QSize(24, 24))
        self.forwardButton.setCheckable(True)
        self.forwardButton.setAutoExclusive(False)
        self.forwardButton.setAutoRaise(True)
        self.forwardButton.setObjectName("forwardButton")
        self.settingsLayout.addWidget(self.forwardButton, 0, Qt.AlignHCenter)
        self.attachmentButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachmentButton.sizePolicy().hasHeightForWidth())
        self.attachmentButton.setSizePolicy(sizePolicy)
        self.attachmentButton.setLayoutDirection(Qt.LeftToRight)
        icon7 = QIcon()
        icon7.addPixmap(QPixmap("icons/attachment-enabled.svg"), QIcon.Normal, QIcon.Off)
        self.attachmentButton.setIcon(icon7)
        self.attachmentButton.setIconSize(QSize(24, 24))
        self.attachmentButton.setCheckable(True)
        self.attachmentButton.setAutoExclusive(False)
        self.attachmentButton.setAutoRaise(True)
        self.attachmentButton.setObjectName("attachmentButton")
        self.settingsLayout.addWidget(self.attachmentButton, 0, Qt.AlignHCenter|Qt.AlignTop)
        spacerItem15 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.settingsLayout.addItem(spacerItem15)
        self.voiceButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voiceButton.sizePolicy().hasHeightForWidth())
        self.voiceButton.setSizePolicy(sizePolicy)
        self.voiceButton.setLayoutDirection(Qt.LeftToRight)
        icon8 = QIcon()
        icon8.addPixmap(QPixmap("icons/voice-enabled.svg"), QIcon.Normal, QIcon.Off)
        self.voiceButton.setIcon(icon8)
        self.voiceButton.setIconSize(QSize(24, 24))
        self.voiceButton.setCheckable(True)
        self.voiceButton.setAutoExclusive(False)
        self.voiceButton.setAutoRaise(True)
        self.voiceButton.setObjectName("voiceButton")
        self.settingsLayout.addWidget(self.voiceButton, 0, Qt.AlignHCenter)
        self.graffitiButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graffitiButton.sizePolicy().hasHeightForWidth())
        self.graffitiButton.setSizePolicy(sizePolicy)
        self.graffitiButton.setLayoutDirection(Qt.LeftToRight)
        icon9 = QIcon()
        icon9.addPixmap(QPixmap("icons/graffiti-enabled.svg"), QIcon.Normal, QIcon.Off)
        self.graffitiButton.setIcon(icon9)
        self.graffitiButton.setIconSize(QSize(24, 24))
        self.graffitiButton.setCheckable(True)
        self.graffitiButton.setAutoExclusive(False)
        self.graffitiButton.setAutoRaise(True)
        self.graffitiButton.setObjectName("graffitiButton")
        self.settingsLayout.addWidget(self.graffitiButton, 0, Qt.AlignHCenter)
        self.stickerButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stickerButton.sizePolicy().hasHeightForWidth())
        self.stickerButton.setSizePolicy(sizePolicy)
        self.stickerButton.setLayoutDirection(Qt.LeftToRight)
        icon10 = QIcon()
        icon10.addPixmap(QPixmap("icons/sticker-enabled.png"), QIcon.Normal, QIcon.Off)
        self.stickerButton.setIcon(icon10)
        self.stickerButton.setIconSize(QSize(24, 24))
        self.stickerButton.setCheckable(True)
        self.stickerButton.setAutoExclusive(False)
        self.stickerButton.setAutoRaise(True)
        self.stickerButton.setObjectName("stickerButton")
        self.settingsLayout.addWidget(self.stickerButton, 0, Qt.AlignHCenter)
        spacerItem16 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.settingsLayout.addItem(spacerItem16)
        self.applyButton = QToolButton(self.settingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applyButton.sizePolicy().hasHeightForWidth())
        self.applyButton.setSizePolicy(sizePolicy)
        self.applyButton.setLayoutDirection(Qt.LeftToRight)
        icon11 = QIcon()
        icon11.addPixmap(QPixmap("icons/apply.svg"), QIcon.Normal, QIcon.Off)
        self.applyButton.setIcon(icon11)
        self.applyButton.setIconSize(QSize(24, 24))
        self.applyButton.setCheckable(False)
        self.applyButton.setAutoExclusive(False)
        self.applyButton.setAutoRaise(True)
        self.applyButton.setObjectName("applyButton")
        self.settingsLayout.addWidget(self.applyButton, 0, Qt.AlignHCenter)
        spacerItem17 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.settingsLayout.addItem(spacerItem17)
        self.verticalLayout_7.addWidget(self.settingsWidget)
        spacerItem18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.verticalLayout_7.addItem(spacerItem18)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.scrollArea, 0, Qt.AlignLeft)
        MainWindow.setCentralWidget(self.centralwidget)
        self.analysis_stickers_amountLabel.setBuddy(self.settingsWidget)
        self.min_symbolsLabel.setBuddy(self.min_symbolsSpinbox)
        self.min_wordsLabel.setBuddy(self.min_wordsSpinbox)

        self.retranslateUi(MainWindow)
        self.main_tabWidget.setCurrentIndex(0)
        self.analysis_tabWidget.setCurrentIndex(0)
        self.settings_tabWidget.setCurrentIndex(0)
        self.and_orCombobox.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "фимоз"))
        self.testButton.setText(_translate("MainWindow", "ТЕСТ КНОПКА"))
        self.exact_searchCheckbox.setText(_translate("MainWindow", "Точный поиск"))
        self.searchLine.setPlaceholderText(_translate("MainWindow", "поиск"))
        self.linkLine.setPlaceholderText(_translate("MainWindow", "ссылка"))
        self.total_messagesLabel.setText(_translate("MainWindow", "Показано 0 из 0 сообщений"))
        self.messageTree.headerItem().setText(0, _translate("MainWindow", "Сообщения"))
        self.messageTree.headerItem().setText(1, _translate("MainWindow", ">"))
        self.messageTree.headerItem().setText(2, _translate("MainWindow", "&"))
        self.messageTree.headerItem().setText(3, _translate("MainWindow", "Дата"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.messagesTab), _translate("MainWindow", "Сообщения"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.photoTab), _translate("MainWindow", "Фото"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.videoTab), _translate("MainWindow", "Видео"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.documentsTab), _translate("MainWindow", "Документы"))
        self.analysis_stickers_amountLabel.setText(_translate("MainWindow", "Всего стикеров"))
        self.analysis_symbols_amountLabel.setText(_translate("MainWindow", "Всего символов"))
        self.analysis_emoji_amountLabel.setText(_translate("MainWindow", "Всего эмоджи"))
        self.label_9.setText(_translate("MainWindow", "Самые используемые:"))
        self.analysis_words_amountLabel.setText(_translate("MainWindow", "Всего слов:"))
        self.label_2.setText(_translate("MainWindow", "В диалоге:"))
        self.analysis_wordsTree.headerItem().setText(0, _translate("MainWindow", "Слово"))
        self.analysis_wordsTree.headerItem().setText(1, _translate("MainWindow", "Количество"))
        self.analysis_tabWidget.setTabText(self.analysis_tabWidget.indexOf(self.tab), _translate("MainWindow", "Слова"))
        self.analysis_tabWidget.setTabText(self.analysis_tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Стикеры"))
        self.analysis_emojisTree.headerItem().setText(0, _translate("MainWindow", "Эмоджи"))
        self.analysis_emojisTree.headerItem().setText(1, _translate("MainWindow", "Количество"))
        self.analysis_tabWidget.setTabText(self.analysis_tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Эмоджи"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.analysisTab), _translate("MainWindow", "Статистика"))
        self.and_orCombobox.setItemText(0, _translate("MainWindow", "или"))
        self.and_orCombobox.setItemText(1, _translate("MainWindow", "и"))
        self.min_symbolsCombobox.setItemText(0, _translate("MainWindow", "от"))
        self.min_symbolsCombobox.setItemText(1, _translate("MainWindow", "только"))
        self.min_symbolsLabel.setText(_translate("MainWindow", " символа"))
        self.min_wordsLabel.setText(_translate("MainWindow", " слова"))
        self.min_wordsCombobox.setItemText(0, _translate("MainWindow", "от"))
        self.min_wordsCombobox.setItemText(1, _translate("MainWindow", "только"))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.textTab), _translate("MainWindow", "Текст"))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.dateTab), _translate("MainWindow", "Дата"))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.usersTab), _translate("MainWindow", "Отправители"))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Page"))
        self.hastextButton.setToolTip(_translate("MainWindow", "Сообщения с текстом"))
        self.emojiButton.setToolTip(_translate("MainWindow", "Сообщения со смайликами"))
        self.lengthButton.setToolTip(_translate("MainWindow", "Длина сообщений"))
        self.forwardButton.setToolTip(_translate("MainWindow", "Пересланные сообщения"))
        self.attachmentButton.setToolTip(_translate("MainWindow", "Сообщения со вложениями"))
        self.voiceButton.setToolTip(_translate("MainWindow", "Голосовые сообщения"))
        self.graffitiButton.setToolTip(_translate("MainWindow", "Граффити"))
        self.stickerButton.setToolTip(_translate("MainWindow", "Стикеры"))
