from datetime import datetime
from fastapi import FastAPI
from google import genai
from dotenv import load_dotenv
import os
import requests



def gemini_ia(cidade, resultados):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    client = genai.Client(api_key=api_key)
    sugestao = f'''Baseado nos horários que o sol nasce e se poe, me de sugestões de atividades:
            O sol em {cidade} nasce as {resultados['sunrise']} e se poe as {resultados['sunset']}
            Apenas liste 4 possíveis atividades baseado na cidade mostrando o horário, não precisa dar detalhes sobre'''

    response_ia = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=sugestao
    )
    print(response_ia.text)



def gera_info():
    url_lat_long = "https://nominatim.openstreetmap.org/search"

    cidade = input("Sobre qual cidade deseja saber sobre o clima?\n")

    parametros_lat_long = {"q": cidade, "format": "json", "limit": 1}

    headers = {"User-Agent": "bild-api"}

    response_lat_long = requests.get(
        url_lat_long, params=parametros_lat_long, headers=headers
    )

    dados_lat_long = response_lat_long.json()
    lat = dados_lat_long[0]["lat"]
    lng = dados_lat_long[0]["lon"]
    data_user = input("Qual data deseja saber?[DD-MM-YYYY]\n")
    data = datetime.strptime(data_user, "%d-%m-%Y")
    data_param = data.strftime("%Y-%m-%d")
    return data_param, lat, lng, cidade



def main(lat, lng, data_param, cidade):
    parametros = {"lat": lat, "lng": lng, "tzid": "America/Sao_Paulo", "date": data_param}

    url = "https://api.sunrise-sunset.org/json"

    response = requests.get(url, params=parametros)
    dados = response.json()
    resultados = dados["results"]
    print(f"Em {cidade} o sol nasce as {resultados['sunrise']}")
    print(f"Em {cidade} o sol se põe as {resultados['sunset']}")
    print('Atividades:\n')

    return resultados



data_param, lat, lng, cidade = gera_info()
resultados = main(lat, lng, data_param, cidade)
gemini_ia(cidade, resultados)