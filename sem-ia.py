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
    resposta = resposta = (
        f"Em {cidade}, o sol nasce às {resultados['sunrise']}. Sugestões para aproveitar esse momento:\n"
        f"- Caminhada leve ou uma corrida ao ar livre.\n"
        f"- Tomar um café observando o amanhecer.\n\n"
        f"O pôr do sol acontece às {resultados['sunset']}.\n"
        f"- Curtir um happy hour com os amigos ou familiares.\n"
        f"- Caminhar pela orla ou parque observando o pôr do sol."
    )

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