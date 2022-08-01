from dataclasses import dataclass

@dataclass
class Kitchen:
	image_path:str
	image_width:int
	image_height:int
	points:int
	views:int
	unchoosen:int

	def get_value(self):
		if (self.views == 0): return 0
		return 100*self.points/self.views

	def __hash__(self):
		return hash(self.image_path)

	def __repr__(self) -> str:
		return "{} - {} - {}\n".format(self.views,self.points,self.image_path)