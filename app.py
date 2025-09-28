from flask import Flask
from routes.donor_routes import donor_bp  # import the blueprint

app = Flask(__name__)
app.register_blueprint(donor_bp)

@app.route('/')
def home():
    return "Backend is running!"

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
