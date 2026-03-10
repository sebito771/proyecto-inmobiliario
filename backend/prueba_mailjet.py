import os
from dotenv import load_dotenv
from mailjet_rest import Client

# Cargamos los datos del archivo donde tienes tus claves
load_dotenv()

# Extraemos las variables
api_key = os.getenv('MAILJET_USERNAME')
api_secret = os.getenv('MAILJET_PASSWORD')
sender_email = os.getenv('MAIL_FROM')

# Inicializamos el cliente
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

data = {
  'Messages': [
    {
      "From": {
        "Email": sender_email,
        "Name": "Prueba Inmobiliaria"
      },
      "To": [
        {
          "Email": sender_email, 
          "Name": "Sebas"
        }
      ],
      "Subject": "Verificación de Conexión 🚀",
      "HTMLPart": "<h3>¡Si ves esto, la API Key funciona!</h3>"
    }
  ]
}

result = mailjet.send.create(data=data)

print(f"Estado: {result.status_code}")
print(result.json())