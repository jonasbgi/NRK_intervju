
class NoFilter:
	def filter(self, screening):
		return True

class FilterOnYear:
	def __init__(self, year='2018'):
		self.year = year
		
	def filter(self, screening):
		return screening[1][:4] == self.year
class FilterOnType:
	def __init__(self, type='tv'):
		self.type = type
	
	def filter(self, screening):
		return screening[2] == self.type

class CombinedFilter:
	def __init__(self, *filters):
		self.filterList = filters[0]
	def filter(self, screening):
		passedFilter = True
		for subFilter in self.filterList:
			try:
				if not subFilter.filter(screening):
					passedFilter = False
			except:
				print("Combined filter got non-filter class object")
		return passedFilter