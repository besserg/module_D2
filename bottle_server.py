from bottle import Bottle, response
from sentry_sdk.integrations.bottle import BottleIntegration
import sentry_sdk
import os
from dotenv import load_dotenv


load_dotenv()
# интеграция с Sentry
sentry_sdk.init(
    dsn=os.environ['SENTRY'],
    integrations=[BottleIntegration()]
)

app = Bottle()


@app.route('/')
def index():
    # определение где запущен сервер, локально или на Heroku
    if os.environ.get('APP_LOCATION') == 'heroku':
        host = "https://bsbottle.herokuapp.com"
        port = ""
    else:
        host = "localhost"
        port = "8080"
    href1 = f"http://{host}:{port}/success" if port else f"{host}/success"
    href2 = f"http://{host}:{port}/fail" if port else f"{host}/fail"
    html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Heroku test bottle server</title>
        </head>
        <body>
            <h1>Select test:</h1>
            <h2><a href='{href1}'>SUCCESS</a></h2>
            <h2><a href='{href2}'>FAIL</a></h2>
        </body>
    </html>
        """
    return html


@app.route('/success')  # Выполняется на ссылке success
def index():
    return f'HTTP status {response.status}'


@app.route('/fail')  # Выполняется на ссылке fail
def index():
    raise RuntimeError("There is an error!")


# определение где запущен сервер, локально или на Heroku
if os.environ.get('APP_LOCATION') == 'heroku':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)
