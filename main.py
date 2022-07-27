import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 button - pythonspot.com'
		self.left = 200
		self.top = 200
		self.width = 820
		self.height = 420
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		label = QLabel(self)
		label.setText("Image")
		label.move(205,0)
		
		button = QPushButton(self)
		button.setToolTip('This is an example button')
		# setting image to the button
		button.setStyleSheet("background-image : url(img/forced-resized/4R5N_01_2.jpg);")
		# setting geometry of button
		button.setGeometry(5, 20, 400,400)
		button.clicked.connect(self.on_click)

		label = QLabel(self)
		label.setText("Image")
		label.move(610,0)
		
		button = QPushButton(self)
		button.setToolTip('This is an example button')
		# setting image to the button
		button.setStyleSheet("background-image : url(img/forced-resized/66b3293bfb54242d487af9ce3ba6a853.jpg);")
		# setting geometry of button
		button.setGeometry(410, 20, 400,400)
		button.clicked.connect(self.on_click)
		
		self.show()

	@pyqtSlot()
	def on_click(self):
		print('PyQt5 button click')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())