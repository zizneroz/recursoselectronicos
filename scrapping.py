import requests
from bs4 import BeautifulSoup
import numpy as np

pages = []
gral_page = requests.get("https://biblioteca.colmex.mx/index.php/induccion")
content = BeautifulSoup(gral_page.content, 'html.parser')
div_colums = content.find(id="ja-slideshow")
links = div_colums.find_all("a")
for link in links: 
    page = requests.get("https://biblioteca.colmex.mx" + link.get('href'))
    soup = BeautifulSoup(page.content, 'html.parser')

    tabla = soup.find(id="tabla")

    all_texts = []
    td_texts = []

    th_array = tabla.find_all('th')
    for th_cell in th_array:
        td_texts.append("\"" + th_cell.text.strip() + "\"")
    all_texts.append(td_texts)
    td_texts = []

    tr_array = tabla.find_all('tr')
    for tr_row in tr_array:
        td_array = tr_row.find_all('td')
        td_texts = []
        for td_cell in td_array:
            td_texts.append("\"" + td_cell.text.strip() + "\"")
        if(len(td_texts) != 0):
            all_texts.append(td_texts)
    
    np.savetxt('csv/%s.csv'%(link.get_text()), all_texts, delimiter=',', fmt='%s')
