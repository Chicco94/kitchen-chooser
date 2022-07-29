import sys
from os import listdir
from os.path import isfile,join
from typing import Sequence
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSlot

from models.kitchen import Kitchen

IMAGES_PATH = "img/forced-resized"

# Types
Kitchens = Sequence[Kitchen]


class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 button - pythonspot.com'
		self.left = 200
		self.top = 200
		self.width = 820
		self.height = 420
		self.leftObject:Kitchen = None
		self.rightObject:Kitchen = None
		self.results = set()

		self.initUI()
	
	def initUI(self):
		# read the result table before choose which image show
		self.prepare()

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.label1 = QLabel(self)
		self.label1.setText("{} %".format(self.leftObject.get_value()))
		self.label1.move(205,0)
		
		self.button1 = QPushButton(self)
		# setting image to the button
		self.button1.setStyleSheet("background-image : url({});".format(self.leftObject.image_path))
		# setting geometry of button
		self.button1.setGeometry(5, 20, 400,400)
		self.button1.clicked.connect(self.on_click_1)

		self.label2 = QLabel(self)
		self.label2.setText("{} %".format(self.rightObject.get_value()))
		self.label2.move(610,0)
		
		self.button2 = QPushButton(self)
		# setting image to the button
		self.button2.setStyleSheet("background-image : url({});".format(self.rightObject.image_path))
		# setting geometry of button
		self.button2.setGeometry(410, 20, 400,400)
		self.button2.clicked.connect(self.on_click_2)
		
		self.show()


	def prepare(self):
		with open("target/results","r") as results:
			lines = results.readlines()
			if len(lines)>0:
				for line in lines:
					path,points,views = line.split(":")
					self.results.add(Kitchen(path,int(points),int(views)))
			else:
				files = ["{}/{}".format(IMAGES_PATH, f) for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f))]
				for file in files:
					self.results.add(Kitchen(file,int(0),int(0)))
		self.get_images()
		

	def get_images(self)->Kitchens:
		"""escludendo le due già attive, ne sceglie un'altra a caso"""
		pool:Kitchens = list(self.results)

		values = sorted(pool, key=lambda x:(x.views,x.points))
		print(len(pool))
		print(values)

		self.leftObject = values[0]
		self.rightObject = values[1]
		
		self.leftObject.views += 1
		self.rightObject.views += 1



	@pyqtSlot()
	def on_click_1(self):
		self.leftObject.points += 1
		self.after_click()


	@pyqtSlot()
	def on_click_2(self):
		self.rightObject.points += 1
		self.after_click()


	def after_click(self):
		self.get_images()
		
		self.button1.setStyleSheet("background-image : url({});".format(self.leftObject.image_path))
		self.label1.setText("{} %".format(self.leftObject.get_value()))
		
		self.button2.setStyleSheet("background-image : url({});".format(self.rightObject.image_path))
		self.label2.setText("{} %".format(self.rightObject.get_value()))


	def closeEvent(self, a0: QCloseEvent) -> None:
		with open("target/results","w") as results:
			for kitchen in self.results:
				results.write("{}:{}:{}\n".format(kitchen.image_path,kitchen.points,kitchen.views))
		return super().closeEvent(a0)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())