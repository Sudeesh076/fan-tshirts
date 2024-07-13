from flask import Flask
from flask_cors import CORS
from coredb.init import startDb
from routes.product import product_api
from routes.user import user_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_api)
app.register_blueprint(product_api)

if __name__ == '__main__':
    #startDb()
    app.run(debug=False, port=5000)





