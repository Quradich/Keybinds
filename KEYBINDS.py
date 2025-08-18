import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QMessageBox,QLabel,QApplication
from PyQt5.QtGui import QFont,QIcon
import keyboard
import time
import threading

app = QApplication(sys.argv)

window = QWidget()
def Error(short:str,error:str):
    new = QMessageBox()
    new.setWindowIcon(QIcon("keybinds.ico"))
    new.setWindowTitle("Keybinds")
    new.setIcon(QMessageBox.Critical)
    new.setText(error)
    new.setStandardButtons(QMessageBox.StandardButton.Ok)
    new.exec()
    sys.exit(short)

try:
    file = open("keys.txt","r")
    keys = file.read()
    file.close()
except:
    try:
        argv = sys.argv[0].split("\\")
        result = ""
        last = len(argv)
        i = 0
        for index in argv:
            i += 1
            if i == last: break
            result += argv[i - 1] + "/"
        file = open(f"{result}keys.txt","r")
        keys = file.read()
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

window.__init__()

index = -1

def clamp(x:float|int,minimum:float|int,maximum:float|int):
    return min(maximum,max(x,minimum))
lastPos = 11
positionTable = {}
sizeTable = {}
keyTable = keys.split(",")
for key in keyTable:
    if key == "":
        Error('Invalid key',"Invalid format, please edit keys.txt")
    if key in isPressed:    
        Error('Invalid key',f"Duplicate key '{key}', please edit keys.txt")
    index += 1
    
    try:
       keyboard.hook_key(key,None)
       keyboard.unhook_all()
    except:
       Error("Key doesn't exist","Key doesn't exist, please edit keys.txt")

    label = QLabel(window)
    label.setText(key.upper())
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("background-color: #00ff00; border: 10px solid")
    label.setFont(font)
    label.setGeometry(lastPos,11,max(len(key.upper()) * 60 + 11,120),120)
    isPressed[key] = False
    back = QLabel(window)
    back.setText(key.upper())
    back.setStyleSheet("background-color: #ffffff; border: 10px solid")
    back.setGeometry(label.x(),11,label.width(),120)
    back.setHidden(True)
    back.setFont(font)
    back.setAlignment(Qt.AlignmentFlag.AlignCenter)
    labels[key.upper()] = back
    label.setMouseTracking(False)
    positionTable[index] = lastPos
    sizeTable[index] = label.width()
    lastPos += label.width() + 11
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
window.setWindowTitle("Keybinds")
window.setStyleSheet('background-color: #00ff00')
window.setWindowIcon(QIcon("keybinds.ico"))
window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
window.setFixedSize(lastPos + 11,144)
window.show()
alive = True
def main():
    while alive:
        for nam in labels:
            label:QLabel = labels[nam]
            Bool = keyboard.is_pressed(nam)
            if isPressed[nam.lower()] == Bool: continue
            isPressed[nam.lower()] = Bool
            label.setHidden(not Bool)
        time.sleep(.006)
threading.Thread(target=main).start()
app.exec()
alive = False
