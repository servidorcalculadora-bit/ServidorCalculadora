from flask import Flask, request
import operator
import re

app = Flask(__name__)

operacoes = {
    # soma
    r"^(?:\+|soma|sum)$": {'executar' : operator.add, 'operadorString' : '+'},
    # subtração
    r"^(?:\-|subtracao|sub)$": {'executar' : operator.sub, 'operadorString' : '-'},
    # multiplicação
    r"^(?:\*|x|·|multiplicacao|mul)$": {'executar' : operator.mul, 'operadorString' : 'x'},
    # divisão
    r"^(?:/|:|÷|divisao|div)$": {'executar' : operator.truediv, 'operadorString' : '/'}
}

def todosParamtros():
    params = {}
    params.update(request.args.to_dict())
    params.update(request.form.to_dict())

    if request.is_json:
        json_data = request.get_json()
        if json_data:
            params.update(json_data)

    return params

def executaCalculo(valor1, valor2, operacao):
    for pattern, funcoes in operacoes.items():
        if re.match(pattern, operacao):
            resultado = funcoes['executar'](int(valor1), int(valor2))
            operacaoString = funcoes['operadorString']
            return {
                'resposta' : resultado,
                'calculoString' : f'{valor1} {operacaoString} {valor2} = {resultado}'
            }
    return {
        'resposta' : 'Operador Inválido',
        'calculoString' : f'{valor1} {operacao} {valor2}'
    }
    

@app.route("/")
def hello():
    parametros = todosParamtros()
    return executaCalculo(parametros['valor1'], parametros['valor2'], parametros['operacao'])

if __name__ == "__main__":
    app.run(debug=True)