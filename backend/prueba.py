import requests
respuesta=requests.post("https://translation.googleapis.com/language/translate/v2", params="q=La buena vida del pescador&target=en&format=html&key=AIzaSyAuXSQB2IGAmLzJ_F6Zf_2vj0wPIoLmWtg").json()
print(type(respuesta))
for n in respuesta.values():
    print(n)

texto=respuesta.get('translatedText')

print(type(texto))

print(texto)