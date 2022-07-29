import sys
from os import listdir
from os.path import isfile,join
from typing import Sequence
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSlot

from PIL import Image

from models.kitchen import Kitchen

ORIGINAL_IMAGES_PATH = "img/converted"
RESIZED_IMAGES_PATH = "img/resized"

WIDTH = 675


# Types
Kitchens = Sequence[Kitchen]


class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 button - pythonspot.com'
		self.left = 0
		self.top = 0
		self.width = 1366
		self.height = 768
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
		self.label1.move(338,0)
		
		self.button1 = QPushButton(self)
		# setting image to the button
		self.button1.setStyleSheet("background-image : url({});".format(self.leftObject.image_path))
		# setting geometry of button
		self.button1.setGeometry(5, 360 - self.leftObject.image_height//2, self.leftObject.image_width,self.leftObject.image_height)
		self.button1.clicked.connect(self.on_click_1)

		self.label2 = QLabel(self)
		self.label2.setText("{} %".format(self.rightObject.get_value()))
		self.label2.move(1013,0)
		
		self.button2 = QPushButton(self)
		# setting image to the button
		self.button2.setStyleSheet("background-image : url({});".format(self.rightObject.image_path))
		# setting geometry of button
		self.button2.setGeometry(685, 360 - self.rightObject.image_height//2, self.rightObject.image_width,self.rightObject.image_height)
		self.button2.clicked.connect(self.on_click_2)
		
		self.show()


	def prepare(self):
		with open("target/results","r") as results:
			lines = results.readlines()
			if len(lines)>0:
				for line in lines:
					path,width,heigth,points,views = line.split(":")
					self.results.add(Kitchen(path,int(width),int(heigth),int(points),int(views)))
			else:
				for file in listdir(ORIGINAL_IMAGES_PATH):
					if isfile(join(ORIGINAL_IMAGES_PATH, file)):
						image = Image.open("{}/{}".format(ORIGINAL_IMAGES_PATH, file))
						width, height = image.size
						newsize = (WIDTH, (height*WIDTH)//width)
						image = image.resize(newsize)
						image.save("{}/{}".format(RESIZED_IMAGES_PATH, file))
						self.results.add(Kitchen("{}/{}".format(RESIZED_IMAGES_PATH, file),WIDTH,(height*WIDTH)//width,0,0))
		self.get_images()
		

	def get_images(self)->Kitchens:
		"""escludendo le due già attive, ne sceglie un'altra a caso"""
		pool:Kitchens = list(self.results)

		values = sorted(pool, key=lambda x:(x.views,x.points))

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
		self.button1.setGeometry(5, 360 - self.leftObject.image_height//2, self.leftObject.image_width,self.leftObject.image_height)
		self.label1.setText("{} %".format(self.leftObject.get_value()))
		
		self.button2.setStyleSheet("background-image : url({});".format(self.rightObject.image_path))
		self.button2.setGeometry(685, 360 - self.rightObject.image_height//2, self.rightObject.image_width,self.rightObject.image_height)
		self.label2.setText("{} %".format(self.rightObject.get_value()))


	def closeEvent(self, a0: QCloseEvent) -> None:
		with open("target/results","w") as results:
			for kitchen in self.results:
				results.write("{}:{}:{}:{}:{}\n".format(kitchen.image_path,kitchen.image_width,kitchen.image_height,kitchen.points,kitchen.views))

		pool:Kitchens = list(self.results)
		values = sorted(pool, key=lambda x:(100-x.points))[0:5]
		print(values)
		return super().closeEvent(a0)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())