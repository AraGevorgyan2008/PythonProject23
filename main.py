from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

app = QApplication([])

window = QWidget()
window.setWindowTitle("PyQt ծրագիր")

layout = QVBoxLayout()

label = QLabel("Բարև!")
button = QPushButton("Սեղմիր")

def on_click():
    label.setText("Սեղմվեց!")

button.clicked.connect(on_click)

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)
window.show()

app.exec()  