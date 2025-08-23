from flask import Flask, request
import operator
import re
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # ativa o Swagger

operacoes = {
    r"^(?:\+|soma|sum)$": {'executar': operator.add, 'operadorString': '+'},
    r"^(?:\-|subtracao|sub)$": {'executar': operator.sub, 'operadorString': '-'},
    r"^(?:\*|x|·|multiplicacao|mul)$": {'executar': operator.mul, 'operadorString': 'x'},
    r"^(?:/|:|÷|divisao|div)$": {'executar': operator.truediv, 'operadorString': '/'}
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
        if re.match(pattern, operacao.lower()):
            resultado = funcoes['executar'](int(valor1), int(valor2))
            operacaoString = funcoes['operadorString']
            return {
                'resposta': resultado,
                'calculoString': f'{valor1} {operacaoString} {valor2} = {resultado}'
            }
    return {
        'resposta': 'Operador Inválido',
        'calculoString': f'{valor1} {operacao} {valor2}'
    }

@app.route("/", methods=['GET'])
def hello():
    """
    This is the summary defined in yaml file
    First line is the summary
    All following lines until the hyphens is added to description
    the format of the first lines until 3 hyphens will be not yaml compliant
    but everything below the 3 hyphens should be.
    ---
    tags:
      - calculo
    consumes:
      - application/json
      - application/x-www-form-urlencoded
    parameters:
      - name: valor1
        in: query
        type: integer
        required: true
        description: Primeiro valor
      - name: valor2
        in: query
        type: integer
        required: true
        description: Segundo valor
      - name: operacao
        in: query
        type: string
        required: true
        description: Operação a ser realizada
        enum: ["+", "soma", "sum", "-", "subtracao", "sub", "*", "x", "·", "multiplicacao", "mul", "/", ":", "÷", "divisao", "div"]
    responses:
      200:
        description: Resultado do cálculo
        schema:
          type: object
          properties:
            resposta:
              type: number
            calculoString:
              type: string
    """
    parametros = todosParamtros()
    return executaCalculo(parametros['valor1'], parametros['valor2'], parametros['operacao'])

if __name__ == "__main__":
    app.run(debug=True)