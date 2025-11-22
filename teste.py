
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
import requests

app = FastAPI()

class ActivityRequest(BaseModel):
    latitude: float
    longitude: float
    data: str
    cidade: str


def gemini_ia(cidade, resultados):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    client = genai.Client(api_key=api_key)
    sugestao = f'''
    Baseado nos horários que o sol nasce e se põe, me dê sugestões de atividades.
    O sol em {cidade} nasce às {resultados['sunrise']} e se põe às {resultados['sunset']}.
    Apenas liste 4 possíveis atividades baseados na cidade com horário, sem detalhes extras.
    '''

    response_ia = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=sugestao
    )

    return response_ia.text


@app.post("/plan-activity")
def plan_activity(req: ActivityRequest):

    parametros = {
        "lat": req.latitude,
        "lng": req.longitude,
        "tzid": "America/Sao_Paulo",
        "date": req.data
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parametros)
    dados = response.json()
    resultados = dados["results"]

    atividades = gemini_ia(req.cidade, resultados)

    return {
        "sunrise": resultados["sunrise"],
        "sunset": resultados["sunset"],
        "activities": atividades
    }