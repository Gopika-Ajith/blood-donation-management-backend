from flask import Flask
from flask_cors import CORS
from routes.donor_routes import donor_bp  # import the blueprint
from routes.auth_routes import auth_bp
from routes.request_routes import request_bp 
from routes.admin_routes import admin_bp

app = Flask(__name__)
CORS(app)  
app.register_blueprint(donor_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(request_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def home():
    return "Backend is running!"

if __name__ == "__main__":
   app.run(debug=True)
