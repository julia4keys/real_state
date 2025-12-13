import idealista
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime as dt
from datetime import timezone
import os


# Configuración del entorno Jinja2 para cargar plantillas desde el directorio 'template'
env = Environment(
    loader=FileSystemLoader( searchpath="./template" ),
    autoescape=select_autoescape()
)

if __name__ == "__main__":
    # Ruta del directorio donde se almacenan las imágenes de propiedades
    folder = "./www/img/properties/"
    # Verificar si el directorio existe
    if os.path.exists(folder):
        # Iterar sobre los archivos en el directorio
        for filename in os.listdir(folder):
            file_path = os.path.join(folder,filename)
            # Obtener la extensión del archivo
            extension = os.path.splitext(file_path)[1]
            # Eliminar archivos con extensión .jpg
            if extension.lower() == '.jpg':
                os.remove(file_path)
    # Obtener datos de anuncios de venta y alquiler desde idealista
    sale_data = idealista.fetch_ads('cuatrokeys')
    rent_data = idealista.fetch_ads('cuatrokeys', rent=True)
    # Cargar la plantilla HTML
    template = env.get_template("index_temp.html")
    # Renderizar la plantilla con los datos de anuncios y la fecha actual
    with open('./www/index.html','w') as f:
                f.write(template.render(sale_ads=sale_data, rent_ads=rent_data, updated=dt.now(tz=timezone.utc).strftime('%d-%b-%Y %H:%M %Z')))