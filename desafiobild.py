from datetime import datetime
from pprint import pprint

import requests


def gera_info():
    url_lat_long = "https://nominatim.openstreetmap.org/search"

    cidade = input("Sobre qual cidade deseja saber sobre o clima?")

    parametros_lat_long = {"q": cidade, "format": "json", "limit": 1}

    headers = {"User-Agent": "bild-api"}

    response_lat_long = requests.get(
        url_lat_long, params=parametros_lat_long, headers=headers
    )

    dados_lat_long = response_lat_long.json()
    lat = dados_lat_long[0]["lat"]
    lng = dados_lat_long[0]["lon"]
    data_user = input("Qual data deseja saber?[DD-MM-YYYY]")
    data = datetime.strptime(data_user, "%d-%m-%Y")
    data_param = data.strftime("%Y-%m-%d")
    return data_param, lat, lng, cidade


data_param, lat, lng, cidade = gera_info()

parametros = {"lat": lat, "lng": lng, "tzid": "America/Sao_Paulo", "date": data_param}

url = "https://api.sunrise-sunset.org/json"

response = requests.get(url, params=parametros)
dados = response.json()
resultados = dados["results"]
pprint(f"Em {cidade} o sol nasce as {resultados['sunrise']}")
pprint(f"Em {cidade} o sol se põe as {resultados['sunset']}")
