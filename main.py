import sys
import ssl
import time
import urllib.request
import parser_core as parser
import gui
import gui_res
import icons_res

from PyQt5.QtCore import QTextStream, QFile, Qt, QSize, QPropertyAnimation, QTimer, pyqtSignal, pyqtSlot, QObject, QRect, QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
                                QDialog, QGraphicsOpacityEffect, QVBoxLayout, QTextEdit, QSizePolicy, QMainWindow,
                                QTreeWidgetItem, QGridLayout, QWidget, QComboBox, QSpinBox, QCheckBox, QLabel,
                                QApplication, QFileDialog, QButtonGroup, QMenu
                            )

ssl._create_default_https_context = ssl._create_unverified_context


class LengthDialog(QDialog):
    def __init__(self, *args):
        super().__init__()
        self.setMinimumSize(QSize(0, 0))
        self.setModal(False)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("QDialog{background: #363B44; border-radius: 3ex; border: 1px solid #49515A} QPushButton{border: none}")

        if args:
            self.setParent(args[0])

        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)

        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(100)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(200)
        self.hide_timer.timeout.connect(lambda: self.hide())

        self.hide()

    def showEvent(self, event):
        self.opacity_anim.setDirection(self.opacity_anim.Forward)
        self.opacity_anim.start()

    def hide_with_anim(self):
        self.opacity_anim.setDirection(self.opacity_anim.Backward)
        self.opacity_anim.start()
        self.hide_timer.start()


class PreviewDialog(QDialog):
    def __init__(self, *args):
        super().__init__()
        self.setModal(False)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)
        style = """
                QDialog{background: #363B44; border-radius: 2ex; border: 0.5px solid #49515A}
                QTextEdit{border-radius: 2ex;}
                """
        self.setStyleSheet(style)

        if args:
            self.setParent(args[0])

        self.layout = QVBoxLayout(self)
        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)

        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(100)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(200)
        self.hide_timer.timeout.connect(lambda: self.hide())

        self.hide()

    def showEvent(self, event):
        self.opacity_anim.setDirection(self.opacity_anim.Forward)
        self.opacity_anim.start()

    def hide_with_anim(self):
        self.opacity_anim.setDirection(self.opacity_anim.Backward)
        self.opacity_anim.start()
        self.hide_timer.start()


class MessageItem(QTreeWidgetItem):
    def info(self):
        return self.data(0, 32)


class Worker(QObject):
    userpic_data_dict: dict = {}
    parsed = pyqtSignal(list, dict, dict)
    done = pyqtSignal()
    forward_icon = pyqtSignal(tuple)

    @pyqtSlot(str)
    def parse_file(self, path):
        t3 = time.perf_counter()

        parsed_file = parser.parse_file(path, 2500)

        for parsed_list, parsed_userpic_dict, analysis_dict in parsed_file:
            at1 = time.perf_counter()
            for item in parsed_userpic_dict.items():
                user = item[0]
                url = item[1]
                if user not in self.userpic_data_dict:
                    data = urllib.request.urlopen(url).read()
                    self.userpic_data_dict[user] = data
            at2 = time.perf_counter()
            print(f"Загрузил авы за {round(at2 - at1, 3)} секунд")
            print(f"Загружено ав: {len(self.userpic_data_dict)}")
            self.parsed.emit(parsed_list, self.userpic_data_dict, analysis_dict)

        t4 = time.perf_counter()
        print(f"Пропарсил файл за  {t4 - t3} секунд \n")
        self.done.emit()

    @pyqtSlot(tuple)
    def load_userpic(self, user_url_tuple):
        user, url = user_url_tuple  # user_id, user_pic
        data = urllib.request.urlopen(url).read()
        self.forward_icon.emit((user, data))


class ChatParser(QMainWindow, gui.Ui_MainWindow):

    request_parsing = pyqtSignal(str)
    request_loadpic = pyqtSignal(tuple)

    def closeEvent(self, *args, **kwargs):
        self.previewDialog.close()
        self.worker_thread.exit()

    def showEvent(self, event):
        tx, ty, tw, th = self.testButton.geometry().getRect()
        self.testButton.setGeometry(self.main_tabWidget.width() - 210, ty, tw, th)

        self.show_anim = QPropertyAnimation(self, b"windowOpacity")
        self.show_anim.setStartValue(0)
        self.show_anim.setEndValue(1)
        self.show_anim.setDuration(200)
        self.show_anim.start()

    def resizeEvent(self, event):
        lx = self.lengthButton.mapTo(self, self.lengthButton.pos()).x()-200
        ly = self.lengthButton.mapTo(self, self.lengthButton.pos()).y()-120
        px = self.messageTree.mapTo(self, self.messageTree.geometry().bottomRight()).x()-200-30
        py = self.messageTree.mapTo(self, self.messageTree.geometry().bottomRight()).y()-130-30
        tx, ty, tw, th = self.testButton.geometry().getRect()

        self.testButton.setGeometry(self.main_tabWidget.width() - 210, ty, tw, th)

        if not self.lengthDialog.isHidden():
            self.lengthDialog.setGeometry(lx, ly, 163, 90)
        if not self.previewDialog.isHidden():
            self.previewDialog.setGeometry(QRect(px, py, 200, 130))


    def __init__(self):

        def init(self):
            # -- инициализация --#
            super().__init__()
            self.setupUi(self)
            self.resize(1116, 690)
            gui_res.qInitResources()
            icons_res.qInitResources()

            self.flag = parser.flag  # флаги
            self.filterflags = self.flag.no_flags
            self.previewDialog = PreviewDialog(self)
            self.lengthDialog = LengthDialog(self)
            self.previewDialog.setParent(self)

            setup_icons(self)
            setup_widgets(self)
            connect_widgets(self)
            set_vars(self)
            start_worker(self)

            self.widgets_enabled(False)
            self.min_wordsCheckbox.setChecked(False)
            self.min_symbolsCheckbox.setChecked(False)

        def setup_icons(self):
            file_icon = QIcon()
            # иконка устанавливается через stylesheet
            self.fileButton.setIcon(file_icon)
            self.fileButton.setIconSize(QSize(30, 30))
            self.fileButton.setToolTip("Открыть файл")

            apply_icon = QIcon()
            # иконка устанавливается через stylesheet
            self.applyButton.setIcon(apply_icon)
            self.applyButton.setIconSize(QSize(30, 30))
            self.applyButton.setToolTip("Применить")

            settings_icon = QIcon()
            settings_icon.addPixmap(QPixmap(":/icons/settings-pressed.svg"), 0, 0)
            settings_icon.addPixmap(QPixmap(":/icons/settings.svg"), 0, 1)
            self.settingsButton.setIcon(settings_icon)
            self.settingsButton.setToolTip("Настройки")
            self.settingsButton.setIconSize(QSize(30, 30))

            hastext_icon = QIcon()
            hastext_icon.addPixmap(QPixmap(":/icons/hastext-enabled-pressed.svg"), 0, 0)
            hastext_icon.addPixmap(QPixmap(":/icons/hastext-enabled.svg"), 0, 1)
            hastext_icon.addPixmap(QPixmap(":/icons/hastext-disabled.svg"), 1, 0)
            hastext_icon.addPixmap(QPixmap(":/icons/hastext-disabled.svg"), 1, 1)
            self.hastextButton.setIcon(hastext_icon)
            self.hastextButton.setToolTip("Сообщения с текстом")

            notext_icon = QIcon()
            notext_icon.addPixmap(QPixmap(":/icons/notext-enabled-pressed.svg"), 0, 0)
            notext_icon.addPixmap(QPixmap(":/icons/notext-enabled.svg"), 0, 1)
            notext_icon.addPixmap(QPixmap(":/icons/notext-disabled.svg"), 1, 0)
            notext_icon.addPixmap(QPixmap(":/icons/notext-disabled.svg"), 1, 1)
            self.notextButton.setIcon(notext_icon)
            self.notextButton.setToolTip("Сообщения без текста")

            emoji_icon = QIcon()
            emoji_icon.addPixmap(QPixmap(":/icons/emoji-enabled-pressed.svg"), 0, 0)
            emoji_icon.addPixmap(QPixmap(":/icons/emoji-enabled.svg"), 0, 1)
            emoji_icon.addPixmap(QPixmap(":/icons/emoji-disabled-pressed.svg"), 1, 0)
            emoji_icon.addPixmap(QPixmap(":/icons/emoji-disabled.svg"), 1, 1)
            self.emojiButton.setIcon(emoji_icon)
            self.emojiButton.setToolTip("Смайлики")

            length_icon = QIcon()
            length_icon.addPixmap(QPixmap(":/icons/length-enabled-pressed.svg"), 0, 0)
            length_icon.addPixmap(QPixmap(":/icons/length-enabled.svg"), 0, 1)
            length_icon.addPixmap(QPixmap(":/icons/length-disabled.svg"), 1, 0)
            length_icon.addPixmap(QPixmap(":/icons/length-disabled.svg"), 1, 1)
            self.lengthButton.setIcon(length_icon)
            self.lengthButton.setToolTip("Длина сообщений")

            forward_icon = QIcon()
            forward_icon.addPixmap(QPixmap(":/icons/forward-enabled-pressed.svg"), 0, 0)
            forward_icon.addPixmap(QPixmap(":/icons/forward-enabled.svg"), 0, 1)
            forward_icon.addPixmap(QPixmap(":/icons/forward-disabled.svg"), 1, 0)
            forward_icon.addPixmap(QPixmap(":/icons/forward-disabled.svg"), 1, 1)
            self.forwardButton.setIcon(forward_icon)
            self.forwardButton.setToolTip("Пересланные сообщения")

            attachment_icon = QIcon()
            attachment_icon.addPixmap(QPixmap(":/icons/attachment-enabled-pressed.svg"), 0, 0)  # ВКЛ    и НАЖАТО
            attachment_icon.addPixmap(QPixmap(":/icons/attachment-enabled.svg"), 0, 1)  # ВКЛ    и НЕ НАЖАТО
            attachment_icon.addPixmap(QPixmap(":/icons/attachment-disabled.svg"), 1, 0)  # ВЫКЛ   и НАЖАТО
            attachment_icon.addPixmap(QPixmap(":/icons/attachment-disabled.svg"), 1, 1)  # ВЫКЛ   и НЕ НАЖАТО
            self.attachmentButton.setIcon(attachment_icon)
            self.attachmentButton.setToolTip("Вложения")

            voice_icon = QIcon()
            voice_icon.addPixmap(QPixmap(":/icons/voice-enabled-pressed.svg"), 0, 0)
            voice_icon.addPixmap(QPixmap(":/icons/voice-enabled.svg"), 0, 1)
            voice_icon.addPixmap(QPixmap(":/icons/voice-disabled.svg"), 1, 0)
            voice_icon.addPixmap(QPixmap(":/icons/voice-disabled.svg"), 1, 1)
            self.voiceButton.setIcon(voice_icon)
            self.voiceButton.setToolTip("Голосовые сообщения")

            self.graffiti_icon = QIcon()
            self.graffiti_icon.addPixmap(QPixmap(":/icons/graffiti-enabled-pressed.svg"), 0, 0)
            self.graffiti_icon.addPixmap(QPixmap(":/icons/graffiti-enabled.svg"), 0, 1)
            self.graffiti_icon.addPixmap(QPixmap(":/icons/graffiti-disabled.svg"), 1, 0)
            self.graffiti_icon.addPixmap(QPixmap(":/icons/graffiti-disabled.svg"), 1, 1)
            self.graffitiButton.setIcon(self.graffiti_icon)
            self.graffitiButton.setToolTip("Граффити")

            sticker_icon = QIcon()
            sticker_icon.addPixmap(QPixmap(":/icons/sticker-enabled-pressed.png"), 0, 0)
            sticker_icon.addPixmap(QPixmap(":/icons/sticker-enabled.png"), 0, 1)
            sticker_icon.addPixmap(QPixmap(":/icons/sticker-disabled-pressed.png"), 1, 0)
            sticker_icon.addPixmap(QPixmap(":/icons/sticker-disabled.png"), 1, 1)
            self.stickerButton.setIcon(sticker_icon)
            self.stickerButton.setToolTip("Стикеры")

            hide_icon = QIcon()
            hide_icon.addPixmap(QPixmap(":/icons/hide.svg"))
            self.hideButton.setIcon(hide_icon)
            self.hideButton.setToolTip("Скрыть выделенные сообщения")

            undo_icon = QIcon()
            undo_icon.addPixmap(QPixmap(":/icons/undo.svg"))
            self.undoButton.setIcon(undo_icon)
            self.undoButton.setToolTip("Показать последнее скрытое")

            att_header_pixmap = QPixmap()
            att_header_pixmap.load(":/icons/attachment-enabled-pressed.svg")
            att_header_pixmap = att_header_pixmap.scaled(10, 10, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation)
            self.att_header_icon = QIcon()
            self.att_header_icon.addPixmap(att_header_pixmap, QIcon.Selected, QIcon.On)
            self.messageTree.headerItem().setText(1, "")
            self.messageTree.headerItem().setIcon(1, self.att_header_icon)
            self.messageTree.headerItem().setToolTip(1, "Содержит вложения")

            fwd_header_pixmap = QPixmap()
            fwd_header_pixmap.load(":/icons/forward-enabled-pressed.svg")
            fwd_header_pixmap = fwd_header_pixmap.scaled(10, 10, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation)
            self.fwd_header_icon = QIcon()
            self.fwd_header_icon.addPixmap(fwd_header_pixmap, QIcon.Selected, QIcon.On)
            self.messageTree.headerItem().setText(2, "")
            self.messageTree.headerItem().setIcon(2, self.fwd_header_icon)
            self.messageTree.headerItem().setToolTip(2, "Содержит пересланные сообщения")

        def setup_widgets(self):
            # -- настройки виджетов  --#

            # виджет сообщений
            self.messageTree.setColumnWidth(0, 330)
            self.messageTree.setColumnWidth(1, 1)
            self.messageTree.setColumnWidth(2, 1)
            self.messageTree.setIconSize(QSize(20, 20))
            self.messageTree.setRootIsDecorated(False)
            self.messageTree.setUniformRowHeights(True)

            self.messageTreeItem = QTreeWidgetItem
            self.messageTreeRoot = self.messageTree.invisibleRootItem()

            # вкладка Анализ
            self.analysis_wordsTree.setRootIsDecorated(False)
            self.analysis_wordsTree.setUniformRowHeights(True)
            self.analysis_wordsTreeItem = QTreeWidgetItem
            self.analysis_wordsTreeRoot = self.analysis_wordsTree.invisibleRootItem()

            self.analysis_emojisTree.setRootIsDecorated(False)
            self.analysis_emojisTree.setUniformRowHeights(True)
            self.analysis_emojiTreeItem = QTreeWidgetItem
            self.analysis_emojiTreeRoot = self.analysis_emojisTree.invisibleRootItem()

            # кнопки
            self.testButton.setParent(self.main_tabWidget)
            self.testButton.setMaximumHeight(17)

            self.undo_menu = QMenu()
            self.undo_menu.addAction("Вернуть все")
            self.undoButton.setMenu(self.undo_menu)
            self.undoButton.setEnabled(False)
            self.hideButton.setEnabled(False)

            self.hastextButton.setProperty("flag", self.flag.hastext)
            self.notextButton.setProperty("flag", self.flag.notext)
            self.emojiButton.setProperty("flag", self.flag.hasemoji)
            self.forwardButton.setProperty("flag", self.flag.hasforward)
            self.attachmentButton.setProperty("flag", self.flag.hasattachment)
            self.voiceButton.setProperty("flag", self.flag.voice)
            self.graffitiButton.setProperty("flag", self.flag.graffiti)
            self.stickerButton.setProperty("flag", self.flag.sticker)

            self.settings_group = QButtonGroup()
            self.settings_group.setExclusive(False)
            self.settings_group.addButton(self.hastextButton, 0)
            self.settings_group.addButton(self.notextButton, 1)
            self.settings_group.addButton(self.emojiButton, 2)
            self.settings_group.addButton(self.forwardButton, 3)
            self.settings_group.addButton(self.attachmentButton, 4)
            self.settings_group.addButton(self.stickerButton, 5)
            self.settings_group.addButton(self.voiceButton, 6)
            self.settings_group.addButton(self.graffitiButton, 7)

            self.attachmentMenu = QMenu()
            self.attachmentMenu.setWindowFlags(self.attachmentMenu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
            self.attachmentMenu.setAttribute(Qt.WA_TranslucentBackground)
            self.attachmentMenu.setObjectName("attachmentMenu")
            self.attachmentMenu.setStyleSheet("QMenu#attachmentMenu{background: transparent;}")
            self.settingsWidget.setMaximumHeight(0)

            # виджет настроек длины сообщений
            self.lengthWidget = QWidget(self.lengthDialog)
            self.lengthLayout = QGridLayout(self.lengthWidget)
            self.lengthLayout.setObjectName("lengthLayout")

            self.and_orCombobox = QComboBox(self.lengthWidget)
            self.and_orCombobox.setMinimumSize(QSize(49, 20))
            self.and_orCombobox.setMaximumSize(QSize(66, 20))
            self.and_orCombobox.setObjectName("and_orCombobox")
            self.and_orCombobox.addItem("или")
            self.and_orCombobox.addItem("и")
            self.lengthLayout.addWidget(self.and_orCombobox, 1, 1, 1, 1)

            self.min_symbolsCombobox = QComboBox(self.lengthWidget)
            self.min_symbolsCombobox.setMinimumSize(QSize(49, 20))
            self.min_symbolsCombobox.setMaximumSize(QSize(66, 20))
            self.min_symbolsCombobox.setObjectName("min_symbolsCombobox")
            self.min_symbolsCombobox.addItem("от")
            self.min_symbolsCombobox.addItem("только")
            self.lengthLayout.addWidget(self.min_symbolsCombobox, 3, 1, 1, 1, Qt.AlignBottom)

            self.min_symbolsSpinbox = QSpinBox(self.lengthWidget)
            self.min_symbolsSpinbox.setWrapping(True)
            self.min_symbolsSpinbox.setMinimum(1)
            self.min_symbolsSpinbox.setMaximum(9999)
            self.min_symbolsSpinbox.setProperty("value", 1)
            self.min_symbolsSpinbox.setObjectName("min_symbolsSpinbox")
            self.lengthLayout.addWidget(self.min_symbolsSpinbox, 3, 2, 1, 1)

            self.min_wordsCheckbox = QCheckBox(self.lengthWidget)
            self.min_wordsCheckbox.setText("")
            self.min_wordsCheckbox.setChecked(False)
            self.min_wordsCheckbox.setObjectName("min_wordsCheckbox")
            self.lengthLayout.addWidget(self.min_wordsCheckbox, 0, 0, 1, 1)

            self.min_symbolsLabel = QLabel(self.lengthWidget)
            self.min_symbolsLabel.setObjectName("min_symbolsLabel")
            self.lengthLayout.addWidget(self.min_symbolsLabel, 3, 3, 1, 1)

            self.min_wordsLabel = QLabel(self.lengthWidget)
            self.min_wordsLabel.setObjectName("min_wordsLabel")
            self.lengthLayout.addWidget(self.min_wordsLabel, 0, 3, 1, 1)

            self.min_symbolsCheckbox = QCheckBox(self.lengthWidget)
            self.min_symbolsCheckbox.setText("")
            self.min_symbolsCheckbox.setChecked(False)
            self.min_symbolsCheckbox.setObjectName("min_symbolsCheckbox")
            self.lengthLayout.addWidget(self.min_symbolsCheckbox, 3, 0, 1, 1)

            self.min_wordsCombobox = QComboBox(self.lengthWidget)
            self.min_wordsCombobox.setMinimumSize(QSize(49, 20))
            self.min_wordsCombobox.setMaximumSize(QSize(66, 20))
            self.min_wordsCombobox.setObjectName("min_wordsCombobox")
            self.min_wordsCombobox.addItem("от")
            self.min_wordsCombobox.addItem("только")
            self.lengthLayout.addWidget(self.min_wordsCombobox, 0, 1, 1, 1)

            self.min_wordsSpinbox = QSpinBox(self.lengthWidget)
            self.min_wordsSpinbox.setWrapping(True)
            self.min_wordsSpinbox.setMinimum(1)
            self.min_wordsSpinbox.setMaximum(9999)
            self.min_wordsSpinbox.setProperty("value", 1)
            self.min_wordsSpinbox.setObjectName("min_wordsSpinbox")
            self.lengthLayout.addWidget(self.min_wordsSpinbox, 0, 2, 1, 1)

        def connect_widgets(self):

            # виджет сообщений
            self.messageTree.itemEntered.connect(self.on_hover)
            self.messageTree.itemSelectionChanged.connect(self.on_select)
            self.messageTree.itemDoubleClicked.connect(self.on_doubleclick)
            self.messageTree.itemExpanded.connect(self.on_expand)

            # боксы
            self.and_orCombobox.currentIndexChanged.connect(self.boxes_handling)

            self.min_symbolsCombobox.currentIndexChanged.connect(self.boxes_handling)
            self.min_symbolsSpinbox.valueChanged.connect(self.boxes_handling)
            self.min_symbolsCheckbox.stateChanged.connect(self.boxes_handling)

            self.min_wordsCombobox.currentIndexChanged.connect(self.boxes_handling)
            self.min_wordsSpinbox.valueChanged.connect(self.boxes_handling)
            self.min_wordsCheckbox.stateChanged.connect(self.boxes_handling)

            # кнопки
            self.testButton.clicked.connect(self.test_function)
            self.applyButton.clicked.connect(self.refresh)
            self.fileButton.clicked.connect(self.browse_file)
            self.hideButton.clicked.connect(self.hide_item)
            self.undoButton.clicked.connect(self.undo_last)
            self.undo_menu.triggered.connect(self.undo_all)
            self.settingsButton.clicked.connect(self.settings)
            self.lengthButton.clicked.connect(self.length_settings)
            self.settings_group.buttonReleased.connect(self.buttons_handling)

            # поиск по словам
            self.searchLine.textChanged.connect(self.refresh)
            self.exact_searchCheckbox.stateChanged.connect(self.refresh)

        def set_vars(self):
            # -- переменные --#

            self.doubleclicked = ()  # даблкликнутый айтем
            self.hovered = ()  # наведенный айтем
            self.selected = ()  # выбранные айтемы
            self.lastchecked = ()
            self.notext_prevstate = self.notextButton.isChecked()

            self.hidden = []  # скрытые пользователем айтемы
            self.selected = []  # выделенные айтемы
            self.requested_forwards = []  # форварды, которым необходимо установить иконку

            self.messages_dict = {}  # словарь со всеми сообщениями
            self.userpic_icon_dict = {}  # словарь со всеми иконками пользователей
            self.analysis_dict = {}  # словарь с анализом всего диалога

            self.total = 0  # Количество всех сообщений
            self.shown = 0  # Количество показанных сообщений

            self.min_words = self.min_wordsSpinbox.value()
            self.min_symbols = self.min_symbolsSpinbox.value()

            # -- словари для склонения --#
            self.endings_dict = {"0": (" слов", " символов"),  # словарь для склонения слов
                                 "1": (" слово", " символ"),  # (1 слово, 2 символа)
                                 "2": (" слова", " символа"),
                                 "3": (" слова", " символа"),
                                 "4": (" слова", " символа"),
                                 "5": (" слов", " символов"),
                                 "6": (" слов", " символов"),
                                 "7": (" слов", " символов"),
                                 "8": (" слов", " символов"),
                                 "9": (" слов", " символов")}

            self.min_endings_dict = {"0": (" слов", " символов"),  # словарь для склонения слов
                                     "1": (" слова", " символа"),  # (Показывать: от 1 слова, 2 символов)
                                     "2": (" слов", " символов"),
                                     "3": (" слов", " символов"),
                                     "4": (" слов", " символов"),
                                     "5": (" слов", " символов"),
                                     "6": (" слов", " символов"),
                                     "7": (" слов", " символов"),
                                     "8": (" слов", " символов"),
                                     "9": (" слов", " символов")}

        def start_worker(self):
            self.worker = Worker()
            self.worker_thread = QThread()
            self.request_parsing.connect(self.worker.parse_file)
            self.worker.parsed.connect(self.insert_item)
            self.worker.done.connect(self.parsing_done)
            self.request_loadpic.connect(self.worker.load_userpic)
            self.worker.forward_icon.connect(self.load_forwardicon)

            self.worker.moveToThread(self.worker_thread)
            self.worker_thread.start()

        init(self)

    def settings(self):
        self.settings_anim = QPropertyAnimation(self.settingsWidget, b"maximumHeight")
        self.settings_anim.setDuration(100)
        self.settings_anim.setStartValue(0)
        self.settings_anim.setEndValue(485)

        if self.settingsWidget.geometry().getRect()[3] == 0:
            self.settings_anim.setDirection(self.settings_anim.Forward)
            self.settings_anim.start()
        else:
            self.lengthDialog.hide_with_anim()
            self.lengthButton.setChecked(False)
            self.settings_anim.setDirection(self.settings_anim.Backward)
            self.settings_anim.start()

    def length_settings(self):
        lengthx = self.lengthButton.mapTo(self, self.lengthButton.pos()).x() - 200
        lengthy = self.lengthButton.mapTo(self, self.lengthButton.pos()).y() - 120
        self.lengthDialog.setGeometry(lengthx, lengthy, 163, 90)

        if self.lengthDialog.isHidden():
            self.lengthDialog.show()
        else:
            self.lengthDialog.hide_with_anim()

    def browse_file(self):
        # вызывается при нажатии на кнопку Открыть файл
        file_path = QFileDialog.getOpenFileName(self, "Выберите файл", filter="*.html") # окно с выбором файла
        if len(file_path[0]):
            file_path, extension = file_path
            self.clear_everything()
            self.request_parsing.emit(file_path)

    def parsing_done(self):
        # вызывается после окончания парсинга
        self.widgets_enabled(True)
        #self.press_buttons(True)
        self.boxes_handling()
        self.buttons_setchecked(True)
        self.filterflags = self.flag.notext | self.flag.hastext | self.flag.hasemoji | self.flag.hasattachment | self.flag.graffiti | self.flag.sticker | self.flag.voice | self.flag.hasforward
        self.refresh()

    def widgets_enabled(self, state: bool):
        self.and_orCombobox.setEnabled(state)
        self.min_wordsCombobox.setEnabled(state)
        self.min_wordsSpinbox.setEnabled(state)
        self.min_wordsCheckbox.setEnabled(state)
        self.min_wordsSpinbox.setEnabled(state)
        self.min_symbolsCombobox.setEnabled(state)
        self.min_symbolsSpinbox.setEnabled(state)
        self.min_symbolsCheckbox.setEnabled(state)
        self.min_symbolsSpinbox.setEnabled(state)
        self.min_wordsLabel.setEnabled(state)
        self.min_symbolsLabel.setEnabled(state)

        self.exact_searchCheckbox.setEnabled(state)
        self.searchLine.setEnabled(state)
        self.linkLine.setEnabled(state)

        self.hastextButton.setEnabled(state)
        self.notextButton.setEnabled(state)
        self.emojiButton.setEnabled(state)
        self.lengthButton.setEnabled(state)

        self.attachmentButton.setEnabled(state)
        self.forwardButton.setEnabled(state)

        self.stickerButton.setEnabled(state)
        self.graffitiButton.setEnabled(state)
        self.voiceButton.setEnabled(state)


    def clear_everything(self):
        self.messageTree.clear()
        self.analysis_wordsTree.clear()
        self.analysis_emojisTree.clear()
        self.analysis_dict.clear()
        self.searchLine.clear()
        self.linkLine.clear()
        self.selected.clear()
        self.doubleclicked = ()

    def insert_item(self, messages_list, userpic_data_dict, analysis_dict):

        def message_handling(obj, item):
            tooltip_text = f"{obj.user_info.user_name}"

            if obj.text_info:
                text = obj.text_info.text

                length_words = obj.text_info.length_words
                length_symbols = obj.text_info.length_symbols_no_spaces
                tooltip_text += f"\n{length_words} {self.endings_dict.get(str(length_words)[-1])[0]}," \
                                f" {length_symbols} {self.endings_dict.get(str(length_symbols)[-1])[1]}"
            else:
                text = ""

            if obj.attachments:
                item.setIcon(1, self.att_header_icon)
                item.setToolTip(1, "Содержит вложения")
                for attachment in obj.attachments:
                    att_child = MessageItem()
                    att_child.setText(0, f"{attachment.att_type}")
                    att_child.setData(0, 32, attachment)
                    item.addChild(att_child)

            if obj.forwards:
                item.setIcon(2, self.fwd_header_icon)
                item.setToolTip(2, "Содержит пересланные сообщения")
                for forward in obj.forwards:
                    child = MessageItem()
                    message_handling(forward, child)
                    item.addChild(child)

            item.setToolTip(0, tooltip_text)

            date = f"{obj.date_info.time}\t{obj.date_info.date}"

            item.setText(0, text)
            item.setText(3, date)
            item.setData(0, 32, obj)
            if obj.msgid != "fwd":
                item.setIcon(0, self.userpic_icon_dict.get(obj.user_info.user_id))

        for item in userpic_data_dict.items():
            user = item[0]
            pixmap = QPixmap()
            pixmap.loadFromData(item[1])
            icon = QIcon()
            icon.addPixmap(QPixmap(pixmap), QIcon.Selected, QIcon.On)
            if user not in self.userpic_icon_dict:
                self.userpic_icon_dict[user] = QIcon(icon)

        for message in messages_list:
            item = MessageItem(self.messageTree)
            message_handling(message, item)
            self.total = self.messageTreeRoot.childCount()
            self.total_messagesLabel.setText(f"Показано {self.total} из {self.total} сообщений")

        self.analysis_handling(analysis_dict)

    def analysis_handling(self, analysis):

        for item, value in analysis.items():
            if item in ("words_amount", "symbols_amount", "stickers_amount", "emojis_amount",):
                if item in self.analysis_dict:
                    self.analysis_dict[item] = self.analysis_dict[item] + value
                else:
                    self.analysis_dict[item] = value

            elif item in ("most_words", "most_emojis"):
                if item in self.analysis_dict:
                    self.analysis_dict[item].update(value)
                else:
                    self.analysis_dict[item] = value

        words_amount = self.analysis_dict["words_amount"]
        self.analysis_words_amountLabel.setText(f"Всего слов: {words_amount:,}")
        symbols_amount = self.analysis_dict["symbols_amount"]
        self.analysis_symbols_amountLabel.setText(f"Всего символов: {symbols_amount:,}")
        stickers_amount = self.analysis_dict["stickers_amount"]
        self.analysis_stickers_amountLabel.setText(f"Всего стикеров: {stickers_amount:,}")
        emojis_amount = self.analysis_dict["emojis_amount"]
        self.analysis_emoji_amountLabel.setText(f"Всего эмоджи: {emojis_amount:,}")

        self.analysis_wordsTree.clear()
        for word, amount in self.analysis_dict["most_words"].most_common(100):
            item = QTreeWidgetItem(self.analysis_wordsTree)
            item.setText(0, word)
            item.setText(1, str(amount))

        self.analysis_emojisTree.clear()
        for emoji, amount in self.analysis_dict["most_emojis"].most_common(100):
            item = QTreeWidgetItem(self.analysis_emojisTree)
            item.setText(0, emoji)
            item.setText(1, str(amount))

    def boxes_handling(self, *args):
        # логика настроек текста
        if not self.min_wordsCheckbox.isChecked():
            self.min_wordsCombobox.setEnabled(False)
            self.min_wordsSpinbox.setEnabled(False)
            self.and_orCombobox.setEnabled(False)
            self.min_words = False
        elif self.min_wordsCheckbox.isChecked():
            self.min_wordsCombobox.setEnabled(True)
            self.min_wordsSpinbox.setEnabled(True)
            self.min_words = self.min_wordsSpinbox.value()

        if not self.min_symbolsCheckbox.isChecked():
            self.min_symbolsCombobox.setEnabled(False)
            self.min_symbolsSpinbox.setEnabled(False)
            self.and_orCombobox.setEnabled(False)
            self.min_symbols = False
        elif self.min_symbolsCheckbox.isChecked():
            self.min_symbolsCombobox.setEnabled(True)
            self.min_symbolsSpinbox.setEnabled(True)
            self.min_symbols = self.min_symbolsSpinbox.value()

        if self.min_wordsCheckbox.isChecked() and self.min_symbolsCheckbox.isChecked():
            self.and_orCombobox.setEnabled(True)
        else:
            self.and_orCombobox.setEnabled(False)

        if not self.min_wordsSpinbox.value() == 11 and not self.min_symbolsSpinbox.value() == 11:
            self.min_wordsLabel.setText(self.min_endings_dict[str(self.min_wordsSpinbox.value())[-1]][0])
            self.min_symbolsLabel.setText(self.min_endings_dict[str(self.min_symbolsSpinbox.value())[-1]][1])
        else:
            if self.min_wordsSpinbox.value() == 11:
                self.min_wordsLabel.setText(" слов")
            if self.min_symbolsSpinbox.value() == 11:
                self.min_symbolsLabel.setText(" символов")

    def buttons_setchecked(self, state):
        self.notextButton.setChecked(state)
        self.hastextButton.setChecked(state)
        self.emojiButton.setChecked(state)
        self.attachmentButton.setChecked(state)
        self.forwardButton.setChecked(state)
        self.graffitiButton.setChecked(state)
        self.stickerButton.setChecked(state)
        self.voiceButton.setChecked(state)

    def buttons_handling(self, button):
        if button.isChecked():
            self.filterflags = self.filterflags | button.property("flag")
        else:
            self.filterflags = self.filterflags - button.property("flag")

    def refresh(self):
        self.shown = 0

        for item_index in range(self.messageTreeRoot.childCount()):
            item = self.messageTreeRoot.child(item_index)

            if item not in self.hidden:
                if self.filterflags & item.info().flags:
                    item.setHidden(False)
                    self.shown += 1
                else:
                    item.setHidden(True)

        self.showntotal_update()

    # TODO: РЕАЛИЗОВАТЬ ОБНОВЛЕНИЕ ПО ФЛАГАМ, А НЕ IF
    # какой нибудь словарь или список с флагами и совпадение с этим списком (назначать флаги при вставке?)
    def _refresh(self):

        self.shown = 0

        state_dict = {0: "min", 1: "only"}
        words_box = state_dict.get(self.min_wordsCombobox.currentIndex())
        symbols_box = state_dict.get(self.min_symbolsCombobox.currentIndex())

        for item_index in range(self.messageTreeRoot.childCount()):
            item = self.messageTreeRoot.child(item_index)
            if item not in self.hidden:
                item_data = item.data(0, 32)
                if item_data.text_info:
                    length_words = item_data.text_info.length_words
                    length_symbols = item_data.text_info.length_symbols_no_spaces

                    # Слова _ИЛИ_ символы
                    if self.and_orCombobox.currentIndex() == 0 and self.min_words and self.min_symbols:
                        if words_box == "min" and symbols_box == "min":
                            if length_words >= self.min_words or length_symbols >= self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "min" and symbols_box == "only":
                            if length_words >= self.min_words or length_symbols == self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "only" and symbols_box == "min":
                            if length_words == self.min_words or length_symbols >= self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "only" and symbols_box == "only":
                            if length_words == self.min_words or length_symbols == self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)

                    # Слова _И_ символы
                    if self.and_orCombobox.currentIndex() == 1 and self.min_words and self.min_symbols:
                        if words_box == "min" and symbols_box == "min":
                            if length_words >= self.min_words and length_symbols >= self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "min" and symbols_box == "only":
                            if length_words >= self.min_words and length_symbols == self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "only" and symbols_box == "min":
                            if length_words == self.min_words and length_symbols >= self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "only" and symbols_box == "only":
                            if length_words == self.min_words and length_symbols == self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)

                    # Только слова
                    if not self.min_symbols:
                        if words_box == "min":
                            if length_words >= self.min_words:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif words_box == "only":
                            if length_words == self.min_words:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)

                    # Только символы
                    if not self.min_words:
                        if symbols_box == "min":
                            if length_symbols >= self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)
                        elif symbols_box == "only":
                            if length_symbols == self.min_symbols:
                                item.setHidden(False)
                            else:
                                item.setHidden(True)


                # Поиск по словам
                if self.searchLine.text():
                    if not self.exact_searchCheckbox.isChecked():
                        if item_data.text_info and self.searchLine.text() in item_data.text_info.text.lower():
                            item.setHidden(False)
                        else:
                            item.setHidden(True)
                    else:
                        if item_data.text_info and \
                                self.searchLine.text() in item_data.text_info.text.lower().lower().split():
                            item.setHidden(False)
                        else:
                            item.setHidden(True)

                if not item.isHidden():
                    self.shown += 1

        self.showntotal_update()

    def on_select(self):
        self.selected = self.messageTree.selectedItems()
        if self.selected:
            self.hideButton.setEnabled(True)
            if self.doubleclicked:
                if self.selected[0] != self.doubleclicked and self.messageTree.itemWidget(self.doubleclicked, 0):
                    self.messageTree.removeItemWidget(self.doubleclicked, 0)
                    self.doubleclicked.setText(0, self.doubleclicked.data(0, 32).text_info.text)
                    self.doubleclicked = ()
                    self.refresh()

    def on_doubleclick(self, item, column):
        self.doubleclicked = item

    def on_expand(self, item):

        # если содержит форварды
        if item.data(0, 32).forwards:
            forwards_count = item.childCount()

            for i in range(forwards_count):
                forward = item.child(i)
                forward_user = forward.info().user_info.user_id
                forward_url = forward.info().user_info.user_pic

                # если юзерпик для юзера не был загружен загружен ранее
                if forward_user not in self.userpic_icon_dict:
                    # добавить айтем с форвардом в очередь на установку иконок
                    self.requested_forwards.append(forward)
                    # загрузить юзерпик в другом потоке (метод Worker.load_userpic)
                    self.request_loadpic.emit((forward_user, forward_url))

                # если юзерпик был загружен ранее
                else:
                    forward.setIcon(0, self.userpic_icon_dict[forward_user])

    def on_hover(self, item):
        if item.info().type() in ("Message", "Forward"):
            if self.flag.hastext in item.info().flags:
                self.previewDialog.textEdit.setText(item.info().text_info.text)
            if self.flag.hasattachment in item.info().flags:
                print(item.info().__dir__)
                #self.previewDiagog.textEdit.setText(item.info().text_info.text)

        """
        сообщ = есть текст, есть смайлик, нет форвардов, нет аттачментов
        
        
        """

    def load_forwardicon(self, user_data_tuple):
        user, data = user_data_tuple  # (user_id, user_pic(bytes))

        #  дополнительная проверка, был ли юзерпик загружен ранее
        if user not in self.userpic_icon_dict:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            icon = QIcon()
            icon.addPixmap(QPixmap(pixmap), QIcon.Selected, QIcon.On)
            self.userpic_icon_dict[user] = icon

        # если нужно загрузить авы
        if self.requested_forwards:
            for forward in self.requested_forwards:
                forward_user = forward.data(0, 32).user_info.user_id
                forward.setIcon(0, self.userpic_icon_dict[forward_user])
                self.requested_forwards.remove(forward)

    def hide_item(self):
        if self.selected:
            for item in self.selected:
                item.setHidden(True)
                item.setSelected(False)
                self.hidden.append(item)
                self.shown -= 1
            self.showntotal_update()
            self.hideButton.setEnabled(False)
            self.undoButton.setEnabled(True)

    def undo_all(self):
        if self.hidden:
            for item in self.hidden:
                item.setHidden(False)
                self.shown += 1
            self.showntotal_update()
            self.hidden.clear()
            self.undoButton.setEnabled(False)

    def undo_last(self):
        if self.hidden:
            self.hidden[-1].setHidden(False)
            self.hidden.pop()
            self.shown += 1
            self.showntotal_update()
            print(str(len(self.hidden)))
            if not self.hidden:
                self.undoButton.setEnabled(False)

    def showntotal_update(self):
        self.total_messagesLabel.setText(f"Показано {self.shown} из {self.total} сообщений")

    def test_function(self):
        self.lengthButton.setCheckable(False)
        if self.previewDialog.isHidden():
            self.previewDialog.show()
            x = self.messageTree.mapTo(self, self.messageTree.geometry().bottomRight()).x()-200-30
            y = self.messageTree.mapTo(self, self.messageTree.geometry().bottomRight()).y()-130-30
            self.previewDialog.setGeometry(QRect(x, y, 200, 130))
            self.attachmentButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.graffitiButton.setEnabled(True)
            self.emojiButton.setEnabled(True)
            self.voiceButton.setEnabled(True)
            self.notextButton.setEnabled(True)
            self.stickerButton.setEnabled(True)
            self.hastextButton.setEnabled(True)
            self.lengthButton.setEnabled(True)
        else:
            self.previewDialog.hide_with_anim()
            self.attachmentButton.setEnabled(False)
            self.forwardButton.setEnabled(False)
            self.graffitiButton.setEnabled(False)
            self.emojiButton.setEnabled(False)
            self.voiceButton.setEnabled(False)
            self.notextButton.setEnabled(False)
            self.stickerButton.setEnabled(False)
            self.lengthButton.setEnabled(False)
            self.hastextButton.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = ChatParser()
    window.show()

    stylesheet = QFile("style.qss")
    stylesheet.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(stylesheet)
    app.setStyleSheet(stream.readAll())

    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()

"""
******** TODO ********
* Разделить отправителей цветами
* Ссылки на профили
* Повторяющиеся сообщения
* Выбор отправителей / профиль отправителя
* Выбор даты или промежутка времени
* Сортировка вложений
* Получение переписки через VKApi
* Восстанавливать удаленные сообщения
* Сохранять переписки (для быстрой загрузки)
**********************
"""