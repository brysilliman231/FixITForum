from flask_app import app
from flask_app.controllers import home

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)