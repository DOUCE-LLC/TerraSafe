from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()

url = 'https://www.data.jma.go.jp/multi/quake/index.html?lang=en'

r = session.get(url)

r.html.render(sleep=2, keep_page=True, scrolldown=3)

tbody = r.html.find('tbody tr')

data = []
for tr in tbody:
    row = [td.text for td in tr.find('td')]
    data.append(row)

df = pd.DataFrame(data)

df.to_csv('../Data/Raw data/japan_meteorologial_agency.csv', index=False)
print("Archivo CSV guardado exitosamente.")