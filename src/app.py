from flask import Flask
from controller.document_controller import document_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(document_bp, url_prefix="/api")


@app.route("/")
def health_check():
    return "API RAG está online!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
