import os
import requests
from datetime import date

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api = Flask(__name__)
API_NASA_URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/"


@api.after_request
def permitir_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@api.get("/api/apod")
def obtener_apod():
    parametros = {"api_key": os.getenv("API_NASA_KEY")}
    fechaRecibida = request.args.get("date")
    if fechaRecibida:
        fechHoy=date.fromisoformat(fechaRecibida).strftime("%y%m%d")

    else:
        fechHoy=date.today().strftime("%y%m%d")  #Obtiene la fecha actual y la formatea a YYMMDD
        print(fechHoy)

    if not parametros["api_key"]:
        return jsonify({"error": "No se ha configurado API_NASA_KEY."}), 500
    try:
        respuesta = requests.get(API_NASA_URL+fechHoy, params=parametros, timeout=15)
        return BeautifulSoup(respuesta.text, "html.parser").get_text()
        
        datos = respuesta.json()
    except requests.RequestException:
        return jsonify({"error": "No se pudo conectar con la API de NASA."}), 502
    return jsonify(datos), respuesta.status_code


@api.get("/translate")
def traducir():
    texto = request.args.get("text")
    gkey = os.getenv("GCLOUD_KEY")
    if texto:
        try:
            print("texto recibido: " + texto)
            respuesta = requests.post(
                "https://translation.googleapis.com/language/translate/v2",
                params="q=" + texto + "&target=es&format=text&key=" + gkey,
            ).json()
            return respuesta, 200
        except:
            return "error al realizar la petición", 400
    else:
        return "Debe proporcionar texto", 400


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000, debug=True)
