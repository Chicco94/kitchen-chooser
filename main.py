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
		
		self.button1 = QPushButton(self)
		# setting image to the button
		self.button1.setStyleSheet("background-image : url({});".format(self.path_1))
		# setting geometry of button
		self.button1.setGeometry(5, 20, 400,400)
		self.button1.clicked.connect(self.on_click_1)
		
		self.button2 = QPushButton(self)
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
				files = ["{}/{}".format(IMAGES_PATH, f) for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f))]
				for file in files:
					self.results[file] = 0
		self.path_1,self.path_2 = self.get_image()
		

	def get_images(self):
		"""escludendo le due già attive, ne sceglie un'altra a caso"""
		pool = self.results.copy()
		values = sorted(pool.items(), key=lambda x:x[1])
		return values[2][0],values[3][0]


	@pyqtSlot()
	def on_click_1(self):
		self.results[self.path_1] = self.results[self.path_1] + 1
		self.after_click()


	@pyqtSlot()
	def on_click_2(self):
		self.results[self.path_2] = self.results[self.path_2] + 1
		self.after_click()


	def after_click(self):
		self.path_1,self.path_2 = self.get_image()
		
		self.button1.setStyleSheet("background-image : url({});".format(self.path_1))
		self.button2.setStyleSheet("background-image : url({});".format(self.path_2))


	def closeEvent(self, a0: QCloseEvent) -> None:
		with open("target/results","w") as results:
			for name,points in self.results.items():
				results.write("{}:{}\n".format(name,points))
		return super().closeEvent(a0)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())