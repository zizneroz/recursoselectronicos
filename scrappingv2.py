from bs4 import BeautifulSoup as bs
import numpy as np
from utils import utils
import csv


def main():
    all_data = []
    # Obtener todos los campos para el Header del archivo excel
    head_content = utils.get_content("https://biblioteca.colmex.mx/index.php/editar-recurso/form/1/713919")
    dict_data = dict()
    dict_data.setdefault("Título", [])
    head_array = head_content.find_all(class_="fabrikLabel")
    for head_text in head_array:
        dict_data.setdefault("\"" + head_text.text + "\"", [])


    # Obtener los links de la tabla
    table_links = utils.get_table_links()

    count = 0
    total_links = len(table_links)
    #Obtener descripcion del recurso
    for link in table_links:
        recurso_content = utils.get_content("https://biblioteca.colmex.mx/" + link)
        titulo = recurso_content.find(id = 'tit')

        #Declarar un diccionario temporal
        tmp_dict = dict()
        tmp_dict.setdefault("Título",titulo.text)
        #Buscamos la tabla con la clase "tabledir"
        table = recurso_content.find('table', class_ = "tabledir")
        tr_row = table.find_all("tr")
        for tr in tr_row:
            label = tr.find("td", class_ = "label")
            if label :
                content = tr.find("td", class_ = "content")
                if(content):
                    tmp_dict.setdefault("\"" + label.text.split(":")[0] + "\"", content.text)
        #Pasar del temporal al general
        keys = dict_data.keys()
        for key in keys:
            #Si la llave se encuentra en el diccionario temporal obtiene el valor, si no, añade N/A
            if key in tmp_dict :
                value = tmp_dict[key]
                dict_data[key].append(value)
            else:
                dict_data[key].append("N/A")
        count+=1
        percent = ((count/total_links) * 100)
        print("Links procesados: " + str("{:.2f}".format(percent)) + "%")
    
    csv_file = "recursos_electronicos"
    csv_columns = list(dict_data.keys())
    dict_values = dict_data.values()
    csv_rows = []
    count = len(list(dict_values)[0])
    for i in range(len(list(dict_values)[0])):
        tmp_rows = []
        for rows in list(dict_values):
            #Reemplazamos todas las comillas existentes por un "pipe"
            row_text = rows[i].strip().replace("\"" , "|")
            tmp_rows.append("\"" + row_text + "\"")
        csv_rows.append(tmp_rows)
        percent = ((i/count) * 100)
        print("Registros procesados: " + str("{:.2f}".format(percent)) + "%")
    csv_rows.insert(0,csv_columns)

    try:
        
        np.savetxt('%s.csv'%(csv_file), csv_rows, delimiter=',', fmt='%s')

    except IOError:
        print("I/O error")

if __name__ == '__main__':
    main()
