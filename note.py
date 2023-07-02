"""
Реализовать приложение для работы с заметками
Обязательные функции в приложении:
* Добавление, изменение, удаление заметок
* Сохранение времени добавления заметки и отслеживание времени до дэдлайна.
* Реализация хранения заметок остаётся на ваш выбор (БД, json и т.д.)."""

import json
import datetime
from PySide6 import QtWidgets

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()
        self.dict_ = {}
        self.last = None
        self.lastIndex = 0
        self.file = {
            "dict_": self.dict_,
            "last": self.last
        }

        # пробуем открыть файл, в котором храняться заметки, для чтения, если он уже существует
        try:
            with open("note.json", "r", encoding="utf8") as file:
                self.file = json.load(file)
                self.dict_ = self.file["dict_"]
                self.last = self.file["last"]
                self.create_list()
                self.choose_note(self.last)

        # если нет, создаем новый файл и открываем его для записи
        except:
            with open("note.json", "w", encoding="utf8") as file:
                self.file = {
                    "dict_": self.dict_,
                    "last": self.last
                }
                json.dump(self.file, file, indent=4)
                self.create_list()

    def initUi(self) -> None:
        """
        Создание интерфейса приложения "Заметки"
        :return: None
        """

        self.setWindowTitle('Заметки')
        self.setFixedSize(500, 700)

        self.newButton = QtWidgets.QPushButton('Создать')
        self.saveButton = QtWidgets.QPushButton('Сохранить')
        self.deleteButton = QtWidgets.QPushButton('Удалить')

        layoutButtons = QtWidgets.QHBoxLayout()
        layoutButtons.addWidget(self.newButton)
        layoutButtons.addWidget(self.saveButton)
        layoutButtons.addWidget(self.deleteButton)

        labelName = QtWidgets.QLabel("Наименование заметки")
        self.LEName = QtWidgets.QLineEdit()
        self.LEName.setPlaceholderText("Введите наименование заметки")

        layoutName = QtWidgets.QHBoxLayout()
        layoutName.addWidget(labelName)
        layoutName.addWidget(self.LEName)

        labelText = QtWidgets.QLabel('Текст заметки')
        self.noteText = QtWidgets.QPlainTextEdit()
        self.noteText.setPlaceholderText("Введите текст заметки")

        layoutText = QtWidgets.QVBoxLayout()
        layoutText.addWidget(labelText)
        layoutText.addWidget(self.noteText)

        labelDLine = QtWidgets.QLabel('Крайний срок выполнения:')
        self.DLine = QtWidgets.QDateTimeEdit()

        layoutDLine = QtWidgets.QHBoxLayout()
        layoutDLine.addWidget(labelDLine)
        layoutDLine.addWidget(self.DLine)

        labelNoteList = QtWidgets.QLabel('Перечень имеющихся заметок')
        self.noteList = QtWidgets.QTreeWidget()
        self.noteList.setColumnCount(3)
        self.noteList.setHeaderLabels(['Наименование заметки', 'Дата создания', 'Крайний срок'])
        self.noteList.setColumnWidth(0, 250)
        self.noteList.setColumnWidth(1, 110)
        self.noteList.setColumnWidth(2, 110)

        layoutNoteList = QtWidgets.QVBoxLayout()
        layoutNoteList.addWidget(labelNoteList)
        layoutNoteList.addWidget(self.noteList)

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutButtons)
        layoutMain.addLayout(layoutName)
        layoutMain.addLayout(layoutText)
        layoutMain.addLayout(layoutDLine)
        layoutMain.addLayout(layoutNoteList)

        self.setLayout(layoutMain)

    def initSignals(self):
        """
        Подключение сигналов
        :return: None
        """

        self.newButton.clicked.connect(self.new_note)
        self.saveButton.clicked.connect(self.save_note)
        self.deleteButton.clicked.connect(self.delete_note)
        self.noteList.currentItemChanged.connect(self.show_note)


    def new_note(self):
        """
        Создание новой заметки
        :return: None
        """

        self.LEName.setText("")
        self.noteText.setPlainText("")
        self.DLine.setDateTime(datetime.datetime.now())

    def save_note(self):
        """
        Сохранение заметки/изменений в заметке
        :return: None
        """

        if self.note_name() not in list(self.dict_.keys()):
            time_now = datetime.datetime.now()
            current_date_seconds_from_start = time_now.timestamp()
            current_date = str(time_now.strftime("%H:%M %d.%m.%Y"))

            if self.note_name().strip() == "":
                self.dict_["untitled"] = {
                    "name": self.note_name(),
                    "date": current_date,
                    "text": self.note_text(),
                    "date_to_seconds": current_date_seconds_from_start,
                    "dl_date": self.dl_date()
                }
            else:
                self.dict_[self.note_name()] = {
                    "name": self.note_name(),
                    "date": current_date,
                    "text": self.note_text(),
                    "date_to_seconds": current_date_seconds_from_start,
                    "dl_date": self.dl_date()
                }
        else:
            time_now = datetime.datetime.now()
            current_date_seconds_from_start = time_now.timestamp()
            current_date = str(time_now.strftime("%H:%M %d.%m.%Y"))
            self.dict_[self.note_name()] = {
                "name": self.note_name(),
                "date": current_date,
                "text": self.note_text(),
                "date_to_seconds": current_date_seconds_from_start,
                "dl_date": self.dl_date()
            }

        self.create_list()

        with open("note.json", "w", encoding="utf8") as file:
            self.file = {
                "dict_": self.dict_,
                "last": self.last
            }
            json.dump(self.file, file, indent=4)


    def delete_note(self):
        """
        Удаления заметки
        :return: None
        """

        self.last = None
        if len(self.noteList.selectedItems()) != 0:
            note_name = self.noteList.selectedItems()[0].text(0)
            if note_name.strip() == "":
                note_name = "untitled"
            self.noteList.takeTopLevelItem(
                self.noteList.indexOfTopLevelItem(
                self.noteList.selectedItems()[0]
            )
        )
            self.dict_.pop(note_name)

        self.LEName.setText("")
        self.noteText.setPlainText("")
        self.create_list()

        with open("note.json", "w", encoding="utf8") as file:
            self.file = {
                "dict_": self.dict_,
                "last": self.last
            }
            json.dump(self.file, file, indent=4)



    def create_list(self):
        """
        Формирование списка заметок
        :return: None
        """

        self.noteList.clear()
        for element in list(self.dict_.keys()):
            self.last = QtWidgets.QTreeWidgetItem(self.noteList,
                                                  [self.dict_[element]["name"],
                                                   self.dict_[element]["date"],
                                                   self.dict_[element]["dl_date"]]
                                                  ).text(0)


    def choose_note(self, n_name):
        """
        Выбор заметки из списка
        :return: None
        """

        if n_name != None:
            iterator = QTreeWidgetItemIterator(self.noteList, QTreeWidgetItemIterator.All)
            while iterator.value():
                n_num = iterator.value()
                if n_num.text(0) == n_name:
                    self.noteList.setCurrentItem(n_num, 1)
                    self.show_note(n_num, None)
                iterator += 1


    def show_note(self, n_num, last_num):
        """
        Загрузки выбранной заметки
        :return: None
        """

        if n_num != last_num and n_num != None:
            self.last = n_num.text(0)
            if n_num != None:
                current_note_name = n_num.text(0)
                if current_note_name == "":
                    current_note_name = "untitled"
                current_note = self.dict_[current_note_name]
                self.LEName.setText(current_note["name"])
                self.noteText.setPlainText(current_note["text"])


    def note_name(self):
        """
        Получение наименования заметки
        :return: None
        """

        return str(self.LEName.text())

    def note_text(self):
        """
        Получение текста заметки
        :return: None
        """

        return self.noteText.toPlainText()

    def dl_date(self):
        """
        Получение дедлайна для выполнения заметки
        :return: None
        """

        return self.DLine.text()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()





