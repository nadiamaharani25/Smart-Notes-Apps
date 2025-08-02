#File notes_txt.py:
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

import os

app = QApplication([])
notes = []


#App interface
#app window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)


#app window widgets
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')


button_note_create = QPushButton('Create note') #a window with field "Enter note name" appears
button_note_del = QPushButton('Delete note')
button_note_save = QPushButton('Save note')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')
field_text = QTextEdit()
button_tag_add = QPushButton('Add to note')
button_tag_del = QPushButton('Unpin from note')
button_tag_search = QPushButton('Search notes by tag')
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')


#arrangement of widgets by layouts
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


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)


#=============== (1) - App functionality ===============
def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])
            print('ini line 1 :', note[0])
            print('ini line 2 :', note[1])
            print('ini line 3 :', note[2])


def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    if ok and note_name != "":
        note = list()
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItems(note[2])
        print(notes)
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0]+'\n')


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index)+".txt", "w") as file:
                    file.write(note[0]+'\n')
                    file.write(note[1]+'\n')
                    for tag in note[2]:
                        file.write(tag+' ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print("Note to save is not selected!")
        

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for i in range(len(notes)):
            if notes[i][0] == key:
                # Hapus file fisik
                filename = str(i) + ".txt"
                if os.path.exists(filename):
                    os.remove(filename)

                # Hapus dari array notes
                del notes[i]

                # Refresh list_notes dan field_text
                list_notes.clear()
                list_tags.clear()
                field_text.clear()
                for note in notes:
                    list_notes.addItem(note[0])
                break
    else:
        print("Note to delete is not selected!")


#event handling
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
#=============== (1) - App functionality ===============

#app startup 
notes_win.show()

#=============== (2) - Looping Apps ===============
name = 0
note = []
while True:
    filename = str(name)+".txt"
    try:
        with open(filename, "r", encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '')
                note.append(line)
        tags = note[2].split(' ')
        note[2] = tags
        
        notes.append(note)
        note = []
        name += 1


    except IOError:
        break


print(notes)
for note in notes:
    list_notes.addItem(note[0])
#=============== (2) - Looping Apps ===============

app.exec_()
