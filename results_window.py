from PyQt5.QtWidgets import QLabel,QWidget
from PyQt5.QtGui import QPixmap
from typing import Sequence
from models.kitchen import Kitchen
from PyQt5.QtGui import QCloseEvent

# Types
Kitchens = Sequence[Kitchen]

class ResultsWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Results")
		self.left = 0
		self.top = 0
		self.width = 1366
		self.height = 768


	def initUI(self,results:Kitchens,results_needed:int):
		self.results = results
		sorted_results = sorted(filter(lambda x: x.unchoosen<results_needed,results), key=lambda x:(100-x.points))

		
		step = 30
		for result in sorted_results:

			photo = QLabel(self)
			photo.setGeometry(step, (self.height-int(result.image_height*0.36))//2, 244, int(result.image_height*0.36))
			photo.setText("")
			photo.setPixmap(QPixmap(result.image_path))
			photo.setScaledContents(True)
			photo.setObjectName(result.get_value())

			label = QLabel(self)
			label.setText("{} %".format(result.get_value()))
			label.move(step+82,(self.height+int(result.image_height*0.36))//2+10)
			step += 264
		self.show()
	
	def before_end(self) -> None:
		with open("target/results","w") as results:
			for kitchen in self.results:
				results.write("{}:{}:{}:{}:{}:{}\n".format(kitchen.image_path,kitchen.image_width,kitchen.image_height,kitchen.points,kitchen.views,kitchen.unchoosen))


	def closeEvent(self, a0: QCloseEvent) -> None:
		self.before_end()
		return super().closeEvent(a0)