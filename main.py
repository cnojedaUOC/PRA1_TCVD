
import extraccion_datos_ign as edi
# Función principal
def main():
    respuesta = edi.descargaPaginaWeb('https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/get30dias')
    lista = edi.extraerDatos(respuesta)
    edi.crearArchivoCSVDesdeLista(lista, 'dataset2.csv')

if __name__ == '__main__':
	main()
