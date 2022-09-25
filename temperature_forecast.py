import requests as req
import os
from bs4 import BeautifulSoup as bs
from random import random
from time import sleep
import numpy as np
def s():
    sleep(random())

from fake_useragent import UserAgent
ua = UserAgent(cache=True)

fp = "temperature_forecast"
if not os.path.exists(fp):
    os.makedirs(fp)

my_headers = {
    'user-agent':ua.random
}

url = "https://www.cwb.gov.tw/V8/C/W/County/MOD/wf7dayNC_NCSEI/ALL_Week.html?t=2022062314-0"
res = req.get(url, headers=my_headers) # response = request.get
soup = bs(res.text,"lxml")

# 抓縣市名稱當作表格的index, 存成 city
city_element = soup.select('tr.day span.heading_3')
city = []
for e in city_element:
    city.append(e.get_text())
city = np.array(city).reshape(22,1)

# 抓各縣市早晚的溫度, 存成 temp_2d_np_day, temp_2d_np_night
temp_element_day = soup.select('tr.day span[class="tem-C is-active"]')
temp_element_night = soup.select('tr.night span[class="tem-C is-active"]')

temp_day = []
temp_night = []
for ed,en in zip(temp_element_day, temp_element_night):
    temp_day.append(ed.get_text()[:2]+'~'+ed.get_text()[-2:])
    temp_night.append(en.get_text()[:2]+'~'+en.get_text()[-2:])
    
temp_2d_day = np.array(temp_day).reshape(22,7)
temp_2d_night = np.array(temp_night).reshape(22,7)
# print(temp_2d_day)
# print(temp_2d_night)


# 合併 city 和 temp_2d_np, 存成 table_city_temp
table_city_temp_day = np.hstack([city,temp_2d_day])
table_city_temp_night = np.hstack([city,temp_2d_night])


# 抓最新的七天當作 header, 存成header
header = ['城市']
for i in range(1,8):
    str = 'tr.table_top th#day{} span'.format(i)
    header.append( soup.select(str)[0].get_text() )
# print(header)

# 將早晚溫度分別匯出成 day_weather.csv 與 night_weather.csv
import pandas as pd
pd.DataFrame(table_city_temp_day).to_csv("temperature_forecast/day_temperature.csv",header=header,index=False)
pd.DataFrame(table_city_temp_night).to_csv("temperature_forecast/night_temperature.csv",header=header,index=False)
print('day_temperature.csv and night_temperature.csv exported successfully.')



