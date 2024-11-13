import idealista
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime as dt
from datetime import timezone
import os


env = Environment(
    loader=FileSystemLoader( searchpath="./template" ),
    autoescape=select_autoescape()
)

if __name__ == "__main__":
    folder = "./www/img/properties/"
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder,filename)
            extension = os.path.splitext(file_path)[1]
            if extension.lower() == '.jpg':
                os.remove(file_path)
    sale_data = idealista.fetch_ads('cuatrokeys')
    rent_data = idealista.fetch_ads('cuatrokeys', rent=True)
    template = env.get_template("index_temp.html")
    with open('./www/index.html','w') as f:
                f.write(template.render(sale_ads=sale_data, rent_ads=rent_data, updated=dt.now(tz=timezone.utc).strftime('%d-%b-%Y %H:%M %Z')))