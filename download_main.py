from fs.osfs import OSFS
from lxml import html
import requests
import random
import time
import csv


#````````````````первоначальные переменные```````````````````````````
jan = list(range(1,32))
feb = list(range(1,29))
mar = list(range(1,32))
apr = list(range(1,31))
may = list(range(1,32))
jun = list(range(1,32))
jul = list(range(1,31))
aug = list(range(1,32))
sep = list(range(1,31))
okt = list(range(1,32))
nov = list(range(1,31))
dec = list(range(1,32))

YEAR = (jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, dec)
link_list = []
html_tips = []
csv_tips = []
#````````````````````````````````````````````````````````````````````

#````функция генерации ссылок на страницу и сохранение в список``````
def link_builder():
	m = input('Номер месяца для парсинга и анализа: ')
	m_index = int(m) - 1
	for i in YEAR[m_index]:
		lnk = f'https://www.zulubet.com/tips-{i}-{m}-2022.html'
		link_list.append(lnk)

	link_file = open(f'settings/link_zulu.csv', 'a')
	for l in link_list:
	 	link_file.write(l + '\n')
	link_file.close()
#````````````````````````````````````````````````````````````````````

#````функция сохранения web-страниц на диск``````````````````````````
def link_download():
	r_file = open('settings/link_zulu.csv', 'r')

	for url_link in r_file:
		url_link = url_link.strip()
		page_name =	url_link[24:]

		req = requests.get(url_link)
			
		file = open(f'zulu_{page_name}', 'w', encoding='UTF8')
		new_record = req.text
		file.write(str(new_record))
		file.close()

		print(f'Страница: {url_link} успешна сохранена\n')
		time.sleep(random.randint(1,10))
#````````````````````````````````````````````````````````````````````

#````проверка наличия файлов в каталоге``````````````````````````````
def control_files():
	with OSFS(".") as myfs:
		work_dir = []

		for path in myfs.walk.dirs():
			work_dir.append(path)

		print(f' Поиск необходимых файлов для преобразования '.center(50,'*'))
		for path in myfs.walk.files(filter=['*.html']):
			html_tips.append(path)
		print(f'В наличии: {len(html_tips)} файлов\n')

		link_file = open(f'settings/tips_html.csv', 'a')
		for l in html_tips:
	 		link_file.write(l + '\n')
		link_file.close()

		print(f' Поиск обработанных файлов '.center(50,'*'))
		for path in myfs.walk.files(filter=['*.csv']):
			csv_tips.append(path)
		print(f'В наличии: {len(csv_tips)} файлов\n')

		delta = len(html_tips) - len(csv_tips)
		print(f' Для обработки доступно {delta} файлов '.center(50,'*'))
#````````````````````````````````````````````````````````````````````

if __name__ == '__main__':
	link_builder()
	link_download()
	control_files()