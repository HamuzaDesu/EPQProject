from flask import Flask

from auth import auth
from index import index
from api import api

app = Flask(__name__)
app.secret_key = 'TEMP_SdECRET_KEY'

app.register_blueprint(auth)
app.register_blueprint(index)
app.register_blueprint(api)
