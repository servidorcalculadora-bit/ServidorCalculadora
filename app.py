from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    nome = request.args.get("nome", "Mundo")
    return {'resposta' : nome}

if __name__ == "__main__":
    app.run(debug=True)