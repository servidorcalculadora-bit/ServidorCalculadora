from flask import Flask, request

app = Flask(__name__)

def get_all_params():
    params = {}
    params.update(request.args.to_dict())
    params.update(request.form.to_dict())

    if request.is_json:
        json_data = request.get_json()
        if json_data:
            params.update(json_data)

    return params

@app.route("/")
def hello():
    parametros = get_all_params()
    return {"parametros": parametros}

if __name__ == "__main__":
    app.run(debug=True)