import ssl
from urllib import request


class Date:
	def __init__(self, rep: str) -> None:
		self.year, self.month, self.day = rep.split("-")
	
	
	def __repr__(self) -> str:
		return super().__repr__()


class Attendance:
	def __init__(self, receipt, dateOfBirth, reading, writing, listening):
		self.receipt = receipt
		pass


class Clawer:
	url = "https://www.copetest.com/results/"
	
	
	def __fetch_content(self):
		context = ssl._create_unverified_context()
		print("Connecting To Server...", end=" ")
		print(Clawer.url)
		r = request.urlopen(Clawer.url, context=context)
		html = str(r.read(), encoding="UTF-8")
		return html
	
	
	def __analysis(self, html):
		pass
	
	
	def __sort(self, result_table):
		return sorted(result_table, key=lambda each: each.video_view, reverse=True)
	
	
	def __print_rank_table(self, result_table):
		pass
	
	
	def start(self):
		html = self.__fetch_content()
		result = self.__sort(self.__analysis(html))
		self.__print_rank_table(result)


if __name__ == '__main__':
	clawer = Clawer()
	clawer.start()
