import json

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog,QHBoxLayout, QVBoxLayout, QFormLayout)

app = QApplication([])
'''Інтерфейс програми'''

notes_win = QWidget()
notes_win.setWindowTitle('Умні замєтки')
notes_win.resize(900, 600)
list_notes = QListWidget()
list_notes_label = QLabel('Спісок замєток')
button_note_del = QPushButton('Удалить замєтку')
button_note_create = QPushButton('Создать замєтку')
button_note_save = QPushButton('Сохранить замєтку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіті тєг...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить до замєтки')
button_tag_del = QPushButton('Удалить тєг')
button_tag_search = QPushButton('Іскать замєтку по тєгу')
list_tags = QListWidget()
list_tags_label = QLabel('Спісок тєгов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)
layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить замєтку', "Імя замєткі")
    if ok and note_name != '':
        notes[note_name] = {"текст": "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)
button_note_create.clicked.connect(add_note)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])
list_notes.itemClicked.connect(show_note)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заміткв для сохрарєнія не вибрана!')
button_note_save.clicked.connect(save_note)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Замітка для удалення не вибрана!')
button_note_del.clicked.connect(del_note)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open ("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замєтка для добавлєнія тєгі не вибрана!")
button_tag_add.clicked.connect(add_tag)
def del_tags():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_notes.selectedItems()[0].text()
        notes[key]["теги"].renove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open ("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Тєг дня удалення не вибран!")
button_note_del.clicked.connect(del_tags)

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() =="Іскать замєтку по тєгу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Очистить поіск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Очистить поіск":
        field_tag.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Іскать замєтку по тєгу")
    else:
        pass
button_tag_search.clicked.connect(search_tag)


notes_win.show()

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()