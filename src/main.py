
import extraccion_datos_ign as edi
# Función principal
def main():
    respuesta = edi.descargaPaginaWeb('https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/getAnio')
    lista = edi.extraerDatos(respuesta)
    edi.crearArchivoCSVDesdeLista(lista, '../csv/seismos_2021.csv')

if __name__ == '__main__':
	main()
