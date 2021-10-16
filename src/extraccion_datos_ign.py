import requests
import csv
import pandas
from bs4 import BeautifulSoup

# Función descargaPaginaWeb que permite recuperar la información correspondiente a la respuesta de la petición. 
# url: corresponde con la url del sitio donde se hará el web scraping
def descargaPaginaWeb(url):
    respuesta = requests.get(
        url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
        }
    )
    return respuesta
    
        
# Función extraerDatos que extrae de una página web la información requerida. La función retorna una lista con la 
# información de todos los sismos producidos (cada sismo se almacena en un diccionario con los nombres de los campos y 
# sus valores).
# respuesta: respuesta obtenida al preguntar a una url específica
def extraerDatos(respuesta):
    contenido_web  = BeautifulSoup(respuesta.text, 'html.parser')
    sismos = []
    nombre_columnas = []
    tabla = contenido_web .find_all('table')[0]
    filas = tabla.find_all('tr')
    for fila in filas:
        cols = fila.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        nom_cols = fila.find_all('th')
        nom_cols = [ele.text.strip() for ele in nom_cols]
        if len(nom_cols) > 0:
            nombre_columnas = nom_cols
        if len(cols) > 0:
            sismos.append(cols) 

    sismos_df = pandas.DataFrame(sismos,columns=nombre_columnas)
    sismos_df.drop('Más Info', axis=1, inplace=True)
    sismos_df = sismos_df.rename(columns={'Localización': 'Localizacion'})
    convertirDatos(sismos_df)
    return sismos_df
    
# Función convertirDatos que convierte los datos de str al tipo correspondiente.
# dataframe : 
def convertirDatos(dataFrame):
    dataFrame['Fecha'] = pandas.to_datetime(dataFrame['Fecha'], format='%d/%m/%Y')
    dataFrame['Hora UTC'] = pandas.to_datetime(dataFrame['Hora UTC'], format='%H:%M:%S')
    dataFrame['Hora Local(*)'] = pandas.to_datetime(dataFrame['Hora Local(*)'], format='%H:%M:%S')
    dataFrame['Profundidad(km)'] = pandas.to_numeric(dataFrame['Profundidad(km)'])
    dataFrame['Magnitud'] = pandas.to_numeric(dataFrame['Magnitud'])
    dataFrame['Latitud'] = pandas.to_numeric(dataFrame['Latitud'])
    dataFrame['Longitud'] = pandas.to_numeric(dataFrame['Longitud'])
    
# Función crearArchivoCSVDesdeLista que crea un archivo csv a partir de una lista de diccionarios.
# lista: lista con los diccionarios
# nombreArchivo: nombre del archivo csv
def crearArchivoCSVDesdeLista(dataFrame, nombreArchivo):
    dataFrame.to_csv(nombreArchivo,index=False)