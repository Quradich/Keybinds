import sys
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtWidgets import QWidget,QMessageBox,QLabel,QApplication
from PyQt5.QtGui import QFont,QIcon
import keyboard
import time
import threading

app = QApplication(sys.argv)

window = QWidget()

file = open("keys.txt","r")
keys = file.read()
file.close()
labels = {}
font = QFont("Bahnschrift",60)
font.setBold(True)

def Error(key):
    QMessageBox.critical(None,"Keybind error",f"Invalid '{key}', please edit keys.txt",QMessageBox.StandardButton.Ok)
    sys.exit("Invalid key")
isPressed = {}

window.__init__()

index = -1

for key in keys.split(","):
    if key in isPressed:
        Error(key)
    index += 1

    label = QLabel(window)
    label.setText(key.upper())
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("background-color: #00ff00; border: 10px solid")
    label.setFont(font)
    label.setGeometry(11 + 131 * index,11,120,120)
    isPressed[key] = False
    back = QLabel(window)
    back.setText(key.upper())
    back.setStyleSheet("background-color: #ffffff; border: 10px solid")
    back.setGeometry(11 + 131 * index,11,120,120)
    back.setHidden(True)
    back.setFont(font)
    back.setAlignment(Qt.AlignmentFlag.AlignCenter)
    labels[key.upper()] = back
    label.setMouseTracking(False)
window.setWindowTitle("Keybinds")
window.setStyleSheet('background-color: #00ff00')
window.setWindowIcon(QIcon("keybinds.png"))
window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
window.setFixedSize(len(keys.split(",")) * 131 + 11,120 + 22)
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
        time.sleep(.003)
threading.Thread(target=main).start()
app.exec()
alive = False
