from flask import Flask
from routes.item_routes import item_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(item_routes, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
