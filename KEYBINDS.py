if __name__ != "__main__":
    raise Exception("This file cannot be imported")

import sys
from pynput.mouse import Listener
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import QWidget,QMessageBox,QLabel,QApplication,QPushButton, QLineEdit
from PyQt5.QtGui import QFont,QIcon
from pynput.mouse import Listener
from pynput.mouse import Button
import keyboard
import time
import threading

app = QApplication(sys.argv)

whitelist = ["mouse1","mouse2","mouse3","m1","m2","m3"]

window = QWidget()
def Error(short:str,error:str):
    listner.stop()
    new = QMessageBox()
    new.setWindowIcon(QIcon("keybinds.ico"))
    new.setWindowTitle("Keybinds")
    new.setIcon(QMessageBox.Critical)
    new.setText(error)
    new.setStandardButtons(QMessageBox.StandardButton.Ok)
    new.exec()
    sys.exit(short)
def Warning(error:str):
    new = QMessageBox()
    new.setWindowIcon(QIcon("keybinds.ico"))
    new.setWindowTitle("Keybinds")
    new.setIcon(QMessageBox.Warning)
    new.setText(error)
    new.setStandardButtons(QMessageBox.StandardButton.Ok)
    new.exec()

try:
    f = open("keybinds.ico","r")
    f.close()
except FileNotFoundError:
    Warning("Not found icon","Error: couldn't find keybinds icon")
def on_clicked(*args):
    button = args[2].name
    pressed = args[3]
    for key in keyTable:
        key = key.lower()
        if button == "middle" and (key == "mouse3" or key == "m3"):
            label:QLabel = labels[key]
            label.setFont(font)
            label.setHidden(not pressed)
        elif button == "left" and (key == "mouse1" or key == "m1"):
            label:QLabel = labels[key]
            label.setFont(font)
            label.setHidden(not pressed)
        elif button == "right" and (key == "mouse2" or key == "m2"):
            label:QLabel = labels[key]
            label.setFont(font)
            label.setHidden(not pressed)
    
listner = Listener(on_click=on_clicked)
listner.start()

try:
    file = open("keys.txt","r")
    keys = file.readline().lower()
    if keys.endswith("\n"):
        keys = keys[:-1]
    displayNames = file.readline()
    file.close()
except Exception as ex:
    new = QMessageBox()
    new.setWindowIcon(QIcon("keybinds.ico"))
    new.setWindowTitle("Keybinds")
    new.setIcon(QMessageBox.Warning)
    new.setText("Failed to load keys")
    new.setInformativeText(type(ex) == OSError and "File is in use, press any button to continue" or "Do you want to create 'keys.txt'?")
    parsed = ""
    indx = 0
    for letter in type(ex).__name__:
        if letter.upper() == letter:
            if indx == 0: indx += 1; parsed += letter; continue
            parsed += " "
        parsed += letter
    new.setDetailedText(f"[{parsed}]: {ex.args[1]}")
    new.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    def Clicked(s):
        if s.text() == "&No":
            sys.exit(str(ex))
        else:
            if type(ex) == OSError:
                return
            global keys
            try:
                file = open("keys.txt","x")
                file.write("q,e")
                file.close()
            except:
                pass
            keys = "q,e"
    new.buttonClicked.connect(Clicked)
    x = new.exec()
    if x == 65536:
        sys.exit(1)

lenght = len(keys.split(","))
if lenght == 0:
    Error('No keys',"No keys set, please edit keys.txt")

labels = {}
font = QFont("Bahnschrift",60)
font.setBold(True)
isPressed = {}

# -- FUNCTIONS -- #

def isWhitelisted(key:str):
    try:
        whitelist.index(key)
        return True
    except:
        return False

# -- MAIN WINDOW -- #

window.__init__()

lastPos = 11
positionTable = {}
sizeTable = {}
keyTable = keys.split(",")
for key in keyTable:
    if key == "":
        Error('Invalid key',"Invalid key, please edit keys.txt")
    try:
       keyboard.hook_key(key,None)
       keyboard.unhook_key(key)
    except:
       if not isWhitelisted(key):
        Error("Key doesn't exist",f"Key \"{key}\" doesn't exist, please edit keys.txt")

# -- PROPERTIES WINDOW -- #
propwindow = QWidget()
propwindow.__init__()

index = -1
selected = None
multiSelect = False

styleSheet = "QPushButton {background-color: #00ff00; border: 5px solid} QPushButton::hover { background-color: #FFFFFF; border: 5px solid }"

propfont = QFont("Bahnschrift",20)
editfont = QFont("Cascadia Code",12)

labelfont = QFont("Bahnschrift")
labelfont.setBold(True)
labelfont.setPixelSize(30)

def Current(Label:QPushButton):
    def Selection():
        global selected
        if selected:
            selected.setStyleSheet(styleSheet)
        selected = Label
        UpdateSelection()
    Label.clicked.connect(Selection)
textLabels = {}
propLabels = {}

keyEdit = QLineEdit(propwindow)
keyEdit.setPlaceholderText("Name")
keyEdit.setFont(editfont)

nameTable = {}
split = displayNames.split(",")
for name in split:
    pos = name.find(";;")
    nameTable[name[:pos]] = name[pos + 3:]

def Update(lastPos):
    index = -1
    for i in labels:
        label = propLabels[i.upper()]
        label.deleteLater()
        label = labels[i]
        label.deleteLater()
        label = textLabels[i]
        label.deleteLater()
    isPressed.clear()
    labels.clear()
    positionTable.clear()
    sizeTable.clear()
    textLabels.clear()
    propLabels.clear()
    for key in keyTable:
        index += 1
        isPressed[key.lower()] = False
        label = QLabel(window)
        text = key.upper()
        try:
            text = nameTable[key].upper()
        except:
            pass
        label.setText(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("border: 10px solid")
        label.setFont(font)
        label.setHidden(False)
        label.adjustSize()
        label.setGeometry(lastPos,11,max(label.width() + 11,120),120)
        textLabels[key] = label
        back = QLabel(window)
        back.setText(text)
        back.setStyleSheet("background-color: #ffffff; border: 10px solid")
        back.setGeometry(lastPos,11,max(len(text) * 60 + 11,120),120)
        back.setHidden(True)
        back.setFont(font)
        back.setAlignment(Qt.AlignmentFlag.AlignCenter)
        labels[key] = back
        label.setMouseTracking(False)
        positionTable[index] = lastPos
        sizeTable[index] = label.width()
        lastPos += label.width() + 11
        label = QPushButton(propwindow)
        label.setHidden(False)
        label.setFont(labelfont)
        label.setText(text)
        label.setStyleSheet(styleSheet)
        label.setGeometry(int(positionTable[index] / 2),10,int(sizeTable[index] / 2),60)
        propLabels[key.upper()] = label
        Current(label)
    try:
        file = open("keycrop.txt","x")
    except:
        file = open("keycrop.txt","w+")
    result = ""
    for i in positionTable:
        v = positionTable[i]
        result += f"KEY \"{keyTable[i].upper()}\":\nStart position: {v - 1}\nEnd position: {lastPos - (v + sizeTable[i]) + 10}\n"
    file.write(result)
    file.close()
    keybinds = open("keys.txt","w")
    result = ""
    for val in keyTable:
        result += val.lower() + ","
    result = result[:-1]
    result += "\n"
    for name in nameTable:
        val = nameTable[name]
        try:
            keyTable.index(key)
        except:
            continue
        result += name.lower() + ";; " + val.lower() + ","
    result = result[:-1]
    keybinds.write(result)
    keybinds.close()
    return lastPos

lastPos = Update(lastPos)
offsetX = int(lastPos / 2) + 10

nameLabel = QLabel(propwindow)
nameLabel.setText("Display Name")
nameLabel.setFont(propfont)

nameEdit = QLineEdit(propwindow)
nameEdit.setPlaceholderText("Name")
nameEdit.setFont(editfont)

def GetSelectionKey():
    for name in nameTable:
        val = nameTable[name]
        if selected.text() == val.upper():
            return name
    return selected.text()

def UpdateSelection():
    global selected
    doesExist = selected != None
    if doesExist:
        nameEdit.setText(GetSelectionKey() != selected.text() and selected.text() or "")
        keyEdit.setText(GetSelectionKey().upper())
        keyEdit.setPlaceholderText(GetSelectionKey().upper())
        selected.setStyleSheet("QPushButton {background-color: #0055ff; border: 5px solid} QPushButton::hover { background-color: #00FFFF; border: 5px solid }")
    else:
        Update(11)
    updateButton.setEnabled(doesExist)
    nameEdit.setEnabled(doesExist)
    keyEdit.setEnabled(doesExist)
    remove.setEnabled(doesExist and len(keyTable) > 1)

def New(event):
    try:
        keyTable.index("q")
        Warning("Duplicate key \"Q\", please change the key before creating a new one")
        return
    except:
        pass
    keyTable.append("q")
    global lastPos,selected,offsetX
    lastPos = 11
    lastPos = Update(lastPos)
    offsetX = int(lastPos / 2) + 10
    AdjustSizes()
    selected = labels["q"]
    UpdateSelection()
def Destroy(event):
    global lastPos,offsetX,selected
    key = GetSelectionKey()
    keyTable.remove(key.lower())
    lastPos = Update(11)
    offsetX = max(int(lastPos / 2),240) + 10
    AdjustSizes()
    selected = None
    UpdateSelection()
create = QPushButton(propwindow)
create.setText("New")
create.setFont(propfont)
create.setGeometry(11,90,90,50)
create.clicked.connect(New)

remove = QPushButton(propwindow)
remove.setText("Remove")
remove.setFont(propfont)
remove.setGeometry(11,180,120,50)
remove.clicked.connect(Destroy)

keyLabel = QLabel(propwindow)
keyLabel.setText("Key Name")
keyLabel.setFont(propfont)

updateButton = QPushButton(propwindow)
updateButton.setText("Apply changes")
updateButton.setFont(propfont)
updateButton.adjustSize()
def AdjustSizes():
    nameLabel.setGeometry(offsetX,0,100,20)
    nameLabel.adjustSize()
    nameEdit.setGeometry(offsetX + 10,40,250,30)
    keyLabel.setGeometry(offsetX,70,40,20)
    keyLabel.adjustSize()
    keyEdit.setGeometry(offsetX + 10,110,250,30)
    updateButton.setGeometry(offsetX,200,193,40)
    window.setFixedSize(lastPos + 11,144)
    propwindow.setFixedSize(max(lastPos + 11,500),250)
UpdateSelection()
def clicked(event):
    key = keyEdit.text()
    try:
        keyboard.hook_key(key,None)
        keyboard.unhook_key(key)
    except:
        if not isWhitelisted(key.lower()):
            Warning(f"Key \"{key}\" doesn't exist")
            return
    try:
        labels[key]
        Warning(f"Duplicate key \"{key}\"")
        return
    except:
        pass
    global selected
    keyTable[keyTable.index(GetSelectionKey().lower())] = key.lower()
    global lastPos,offsetX
    lastPos = 11
    if len(nameEdit.text()) > 0:
        nameTable[key.lower()] = nameEdit.text()
    else:
        try:
            nameTable.pop(key.lower())
        except:
            pass
    lastPos = Update(lastPos)
    offsetX = int(lastPos / 2) + 10
    AdjustSizes()
    selected = propLabels[key.upper()]
    UpdateSelection()
updateButton.clicked.connect(clicked)

# -- SETUP -- #

def closeevent(event):
    window.close()
    propwindow.close()
    app.quit()

window.setWindowTitle("Keybinds")
window.setStyleSheet('background-color: #00ff00')
window.setWindowIcon(QIcon("keybinds.ico"))
window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
window.setFixedSize(lastPos + 11,144)
window.closeEvent = closeevent
window.show()

def click(event):
    if keyEdit.hasFocus():
        keyEdit.clearFocus()
    elif nameEdit.hasFocus():
        nameEdit.clearFocus()
    global selected
    selected = None
    UpdateSelection()

propwindow.closeEvent = closeevent
propwindow.setGeometry(window.x(),window.y() + window.height() + 31,lastPos + 11,200)
propwindow.setFixedSize(lastPos + 11,250)
propwindow.setWindowFlags(window.windowFlags())
propwindow.setWindowTitle("Keybinds: Properties")
propwindow.setWindowIcon(QIcon("keybinds.ico"))
propwindow.mousePressEvent = click
propwindow.show()

AdjustSizes()

# -- MAIN -- #

alive = True
def main():
    while alive:
        for nam in labels:
            if isWhitelisted(nam.lower()): continue
            Bool = keyboard.is_pressed(nam)
            if isPressed[nam.lower()] == Bool: continue
            label:QLabel = labels[nam]
            isPressed[nam.lower()] = Bool
            label.setFont(font)
            label.setHidden(not Bool)
        time.sleep(.006)
threading.Thread(target=main).start()
app.exec()
alive = False
