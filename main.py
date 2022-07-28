import sys
from os import listdir
from os.path import isfile,join
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSlot

from random import choice

IMAGES_PATH = "img/forced-resized"

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 button - pythonspot.com'
		self.left = 200
		self.top = 200
		self.width = 820
		self.height = 420
		self.path_1 = ""
		self.path_2 = ""
		self.results = dict()

		self.initUI()
	
	def initUI(self):
		# read the result table before choose which image show
		self.prepare()

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		label = QLabel(self)
		label.setText("Image")
		label.move(205,0)
		
		self.button1 = QPushButton(self)
		self.button1.setToolTip('This is an example button')
		# setting image to the button
		self.button1.setStyleSheet("background-image : url({});".format(self.path_1))
		# setting geometry of button
		self.button1.setGeometry(5, 20, 400,400)
		self.button1.clicked.connect(self.on_click_1)

		label = QLabel(self)
		label.setText("Image")
		label.move(610,0)
		
		self.button2 = QPushButton(self)
		self.button2.setToolTip('This is an example button')
		# setting image to the button
		self.button2.setStyleSheet("background-image : url({});".format(self.path_2))
		# setting geometry of button
		self.button2.setGeometry(410, 20, 400,400)
		self.button2.clicked.connect(self.on_click_2)
		
		self.show()


	def prepare(self):
		with open("target/results","r") as results:
			lines = results.readlines()
			if len(lines)>0:
				for line in lines:
					name,points = line.split(":")
					self.results[name] = int(points)
			else:
				pass 
				files = ["{}/{}".format(IMAGES_PATH, f) for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f))]
				for file in files:
					self.results[file] = 0
		self.path_1 = self.get_image()
		self.path_2 = self.get_image()
		print(self.path_1)
		print(self.path_2)
		

	
	
	def get_image(self):
		"""escludendo le due già attive, ne sceglie un'altra a caso"""
		pool = list(self.results.keys())
		pool = [x for x in pool if x != self.path_1]
		pool = [x for x in pool if x != self.path_2]
		return choice(pool)


	@pyqtSlot()
	def on_click_1(self):
		self.results[self.path_1] = self.results[self.path_1] + 1
		self.path_2 = self.get_image()
		self.button2.setStyleSheet("background-image : url({});".format(self.path_2))


	@pyqtSlot()
	def on_click_2(self):
		self.results[self.path_2] = self.results[self.path_2] + 1
		self.path_1 = self.get_image()
		self.button1.setStyleSheet("background-image : url({});".format(self.path_1))


	def closeEvent(self, a0: QCloseEvent) -> None:
		with open("target/results","w") as results:
			for name,points in self.results.items():
				results.write("{}:{}\n".format(name,points))
		return super().closeEvent(a0)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())