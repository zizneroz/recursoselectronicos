import requests as rq
from bs4 import BeautifulSoup as bs
import numpy as np

def get_content(url_dir):
    source = rq.get(url_dir)
    content = bs(source.content, 'html.parser')
    return content

def get_table_links():
    links = []
    table_content = get_content("https://biblioteca.colmex.mx/index.php/recursos?palabra=&limIni=0&limReg=1495&ordenar=nom&tipoF=&accesoF=&proveedorF=&arbitradoF=&completoF=&centroF=&geograficaF=&tematicaF=&tipo_recF=")
    tabla = table_content.find(id="tabla")
    links_array = tabla.find_all('a')
    for link in links_array:
        if 'Más información' in link.text:
            links.append(link.get('href'))
    
    return links