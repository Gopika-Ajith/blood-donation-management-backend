from flask import Flask
from routes.donor_routes import donor_bp  # import the blueprint
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.register_blueprint(donor_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def home():
    return "Backend is running!"

if __name__ == "__main__":
   app.run(debug=True)
