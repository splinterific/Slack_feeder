from flask import Flask
from api.main import api
from api.oauth_flow import oauth
from web.main import web
import os


app = Flask(__name__)


app.register_blueprint(api)
app.register_blueprint(oauth)
app.register_blueprint(web)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
