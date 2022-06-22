import csv
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

def html_csv():
	global list_match
	list_match = []

	with open('data/tips/zulu_tips-14-06-2022.html', 'r', encoding='UTF8') as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		global title
		title = soup.title.text.split(' - ')[-1]

# Список всех матчей на странице``и создаем словарь по каждому матчу`
		list_matches = soup.find_all('tr', bgcolor=('#EFEFEF','#FFFFFF'))
		for match in list_matches:
			global match_detail
			match_detail = {}

# получаем даты матчей и заносим в словарь для каждого матча ````````
			date_match = match.find_all('td')[0]
			date_match = date_match.get_text()
			date_match = datetime.strptime(date_match, '%d-%m, %H:%M')
			date_match = date_match.strftime('%d-%m %H:%M')
			match_detail['date_match'] = date_match

# Название лиги `````````````````````````````````````````````````````
			ligue_name = match.find('img').get('title').strip().lower()
			match_detail['ligue_name'] = ligue_name
			
# Имя команд в матче`````````````````````````````````````````````````
			team_name = match.find_all('td')[1]
			team_name = team_name.get_text()
			team_name = team_name.lower().strip().split(' - ')
			home_team = team_name[0]
			away_team = team_name[1]
			match_detail['home_team'] = home_team
			match_detail['away_team'] = away_team

# Шансы на домашнюю на ничью на выездную`````````````````````````````
			chance_home = match.find_all('td', class_='prob2 prediction_full')[0].get_text()
			chance_home = float(chance_home.replace('%','').strip())

			chance_draw = match.find_all('td', class_='prob2 prediction_full')[1].get_text()
			chance_draw = float(chance_draw.replace('%','').strip())
			    
			chance_away = match.find_all('td', class_='prob2 prediction_full')[2].get_text()
			chance_away = float(chance_away.replace('%','').strip())

			match_detail['chance_home'] = chance_home
			match_detail['chance_draw'] = chance_draw
			match_detail['chance_away'] = chance_away

# Tips на победу`````````````````````````````````````````````````````
			try:
				tips = match.find('font', color='green').get_text()
				if tips == '':
					match_detail['tips'] = 'none'
				else:
					match_detail['tips'] = tips
			except:
				continue

# Получаем коэффициенты букмекеров на матч```````````````````````````
			kef_home = match.find_all('td', class_='aver_odds_full')[0].get_text()
			kef_home = float(kef_home.replace('%','').strip())

			kef_draw = match.find_all('td', class_='aver_odds_full')[1].get_text()
			kef_draw = float(kef_draw.replace('%','').strip())
			    
			kef_away = match.find_all('td', class_='aver_odds_full')[2].get_text()
			kef_away = float(kef_away.replace('%','').strip())

			match_detail['home_odds'] = kef_home
			match_detail['draw_odds'] = kef_draw
			match_detail['away_odds'] = kef_away

# Добавляем итоговый результат ``````````````````````````````````````
			ft_result = match.find_all('td', align='center')[-1].get_text()
			match_detail['final_result'] = ft_result
			try:
				goal_result = ft_result.split(':')
				goal_result_home = int(goal_result[0])
				goal_result_away = int(goal_result[1])
			except:
				continue
			match_detail['goal_result_home'] = goal_result_home
			match_detail['goal_result_away'] = goal_result_away

# Производим расчет Value````````````````````````````````````````````
			value_home = round((chance_home * kef_home) / 100, 4)
			value_draw = round((chance_draw * kef_draw) / 100, 4)
			value_away = round((chance_away * chance_away) / 100, 4)
			match_detail['value_home'] = value_home
			match_detail['value_draw'] = value_draw
			match_detail['value_away'] = value_away

# Все матчи в список добавляем```````````````````````````````````````
			list_match.append(match_detail)

# использую функцию библиотеки Pandas для сохранения результата в csv
def pandas_writer():
	df = pd.DataFrame.from_dict(list_match) 
	df.to_csv('data/data_tips/zulu_tips-' + title + '.csv', index = False)

if __name__ == '__main__':
	html_csv()
	pandas_writer()
