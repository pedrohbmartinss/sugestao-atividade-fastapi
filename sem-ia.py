from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ActivityRequest(BaseModel):
    latitude: float
    longitude: float
    data: str
    cidade: str


def atividades(cidade, resultados):
    resposta = f'''Em {cidade}, o sol nasce às {resultados['sunrise']}. Aqui vão duas sugestões para aproveitar esse momento:\n
            Caminhada leve ou uma corrida ao ar livre.\n
            Tomar um café observando o amanhecer.\n\n
        
            O pôr do sol acontece às {resultados['sunset']}.\n
            Curtir um happy hour com os amigos ou familiares.\n
            Caminhar pela orla ou parque observando o por do sol.'''

    return resposta


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

    atividade = atividades(req.cidade, resultados)

    return {
        "sunrise": resultados["sunrise"],
        "sunset": resultados["sunset"],
        "activities": atividade
    }