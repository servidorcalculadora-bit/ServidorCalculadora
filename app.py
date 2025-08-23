from flask import Flask, request
import operator

app = Flask(__name__)

operacoes = {
    #soma
    '+' : operator.add,
    #subtração
    '-' : operator.sub,
    #multiplicação
    '*' : operator.mul,
    'x' : operator.mul,
    '·' : operator.mul,
    #divisão
    '/' : operator.truediv,
    ':' : operator.truediv,
    '÷' : operator.truediv
}

def get_all_params():
    params = {}
    params.update(request.args.to_dict())
    params.update(request.form.to_dict())

    if request.is_json:
        json_data = request.get_json()
        if json_data:
            params.update(json_data)

    return params

def executaCalculo(valor1, valor2, operacao):
    return {
        'calculo' : operacoes[operacao](valor1, valor2),
        'calculoString' : f'{valor1} {operacao} {valor2}'
    }

@app.route("/")
def hello():
    parametros = get_all_params()
    return executaCalculo(parametros['valor1'], parametros['valor2'], parametros['operacao'])

if __name__ == "__main__":
    app.run(debug=True)