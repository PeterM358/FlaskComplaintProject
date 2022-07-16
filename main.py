from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
api = Api(app)
migrate = Migrate(app, db)


@app.after_request
def return_response(response):
    db.session.commit()
    return response


[api.add_resource(*route_data) for route_data in routes]

db.init_app(app)

if __name__ == "__main__":
    app.run()
