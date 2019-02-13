import datetime
import re
import ssl
from urllib import request

import numpy as np
from tabulate import tabulate


watch_list = []

registration_info = None


class PersonalInfo:
	def __init__(self, familyName, GivenName, dataOfBirth, receipt):
		pass


class Attendance:
	def __init__(self, receipt, dateOfBirth, reading, writing, listening, total, TOP):
		self.receipt = receipt
		year, month, day = dateOfBirth.split("-")
		self.dateOfBirth = datetime.date(int(year), int(month), int(day))
		self.reading = float(reading)
		self.writing = float(writing)
		self.listening = float(listening)
		self.total = float(total)
		self.TOP = float(TOP) if TOP is not None else None


def create_attendance(data):
	return Attendance(data[0], data[1], data[2], data[3], data[4], data[5], None if data[6].__len__() == 0 else data[6])


class Clawer:
	result_url = "https://www.copetest.com/results/"
	
	
	@staticmethod
	def __fetch_content(url):
		context = ssl._create_unverified_context()
		print("Connecting To Server...", end=" ")
		print(url)
		r = request.urlopen(url, context=context)
		html = str(r.read(), encoding="UTF-8")
		return html
	
	
	def __analysis(self, html):
		test_date = re.findall('<div id="text-block-3"[\\d\\D]*?Marks for the ([\\d\\D]*?) COPE test</h3>', html)[0]
		test_result = re.findall('<tbody>([\\d\\D]*?)</tbody>', html)[0]
		attendance_list = self.__analysis_result(test_result)
		min_reading = 22
		min_writing = 32
		min_listening = 22
		min_total = 86
		passed = [attendance for attendance in attendance_list if
		          attendance.reading >= min_reading and
		          attendance.writing >= min_writing and
		          attendance.listening >= min_listening and
		          attendance.total >= min_total
		          ]
		not_passed = [attendance for attendance in attendance_list if
		              attendance.reading < min_reading or
		              attendance.writing < min_writing or
		              attendance.listening < min_listening or
		              attendance.total < min_total
		              ]
		self.__print_rank_table(attendance_list, test_date, passed, not_passed, sort_method=self.sort_by_total)
	
	
	def __analysis_result(self, test_result):
		attendances_data = re.findall("<tr>([\\d\\D]*?)</tr>", test_result)
		return [create_attendance(re.findall("<td>([\\d\\D]*?)</td>", data)) for data in attendances_data[1:]]
	
	
	def sort_by_age(self, list):
		return sorted(list, key=lambda attendance: attendance.dateOfBirth, reverse=True)
	
	
	def sort_by_total(self, list):
		return sorted(list, key=lambda attendance: attendance.total, reverse=True)
	
	
	def sort_by_reading(self, list):
		return sorted(list, key=lambda attendance: attendance.reading, reverse=True)
	
	
	def sort_by_writing(self, list):
		return sorted(list, key=lambda attendance: attendance.writing, reverse=True)
	
	
	def sort_by_listening(self, list):
		return sorted(list, key=lambda attendance: attendance.listening, reverse=True)
	
	
	def __print_rank_table(self, data, test_date, passed, not_passed, sort_method):
		passed = sort_method(passed)
		not_passed = sort_method(not_passed)
		total = data.__len__()
		passed_people = passed.__len__()
		passRate = passed_people / total
		average_reading = np.mean([attendance.reading for attendance in data])
		average_listening = np.mean([attendance.listening for attendance in data])
		average_writing = np.mean([attendance.writing for attendance in data])
		average_total = np.mean([attendance.total for attendance in data])
		average_top = np.mean([attendance.TOP for attendance in data if attendance.TOP is not None])
		std_reading = np.std([attendance.reading for attendance in data])
		std_listening = np.std([attendance.listening for attendance in data])
		std_writing = np.std([attendance.writing for attendance in data])
		std_total = np.std([attendance.total for attendance in data])
		std_top = np.std([attendance.TOP for attendance in data if attendance.TOP is not None])
		print("\nTest Date : {}\n"
		      "Total attendance : {}\n"
		      "Total attendance passed: {}\n"
		      "Rate For passing : {:3.2f}%\n"
		      "Average Reading Score : {:3.2f} (std: {:3.2f})\n"
		      "Average Listening Score : {:3.2f} (std: {:3.2f})\n"
		      "Average Writing Score : {:3.2f} (std: {:3.2f})\n"
		      "Average Total Score : {:3.2f} (std: {:3.2f})\n"
		      "Average TOP Score : {:3.2f} (std: {:3.2f})\n".format(
				test_date,
				total,
				passed_people,
				passRate * 100,
				average_reading, std_reading,
				average_listening, std_listening,
				average_writing, std_writing,
				average_total, std_total,
				average_top, std_top,
		)
		)
		print("=================== Passed ===================")
		self.__print_by_tabulate(passed)
		print("\n================= Not Passed =================")
		self.__print_by_tabulate(not_passed)
	
	
	def __print_by_tabulate(self, list):
		tabulate_data = [
			[attendance.receipt, attendance.dateOfBirth, attendance.reading, attendance.listening, attendance.writing,
			 attendance.total, attendance.TOP] for attendance in list]
		print(tabulate(tabulate_data, ("Receipt", "DateOfBirth", "Reading", "Listening", "Writing", "Total", "Top")))
	
	
	def start(self):
		html = self.__fetch_content(Clawer.result_url)
		self.__analysis(html)


if __name__ == '__main__':
	clawer = Clawer()
	clawer.start()
