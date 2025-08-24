from flask import Flask, request, render_template
import operator
import re
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
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

def validar_parametros(parametros):
    obrigatorios = ['valor1', 'valor2', 'operacao']
    faltando = [p for p in obrigatorios if p not in parametros or parametros[p] in [None, '']]
    
    if faltando:
        return {
            'erro': f"Parâmetros obrigatórios ausentes: {', '.join(faltando)}",
            'exemplo': {
                'valor1': 10,
                'valor2': 5,
                'operacao': '+'
            }
        }
    return None

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

@app.route("/exemploJs")
def exemploJs():
    dominio = request.host_url

    codigo_js = f'''
fetch("{dominio}calculadora", {{
    method: "POST",
    headers: {{"Content-Type": "application/json"}},
    body: JSON.stringify({{valor1: 10, valor2: 5, operacao: "+"}})
}})
.then(res => res.json())
.then(console.log);
    '''
    return render_template("index.html", titulo='JS(Puro)', codigo=codigo_js, img='js-icon.png')

@app.route("/exemploJsJquery")
def exemploJsJquery():
    dominio = request.host_url
    
    codigo_jquery = f'''
$.ajax({{
    url: "{dominio}calculadora",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({{ valor1: 10, valor2: 5, operacao: "+" }}),
    success: function(res) {{
        console.log(res);
    }}
}});
    '''
    return render_template("index.html", titulo='JS(Jquery)', codigo=codigo_jquery, img='js-icon.png')

@app.route("/exemploJava")
def exemploJava():
    dominio = request.host_url

    codigo_java = f'''
    import java.io.OutputStream;
    import java.net.HttpURLConnection;
    import java.net.URL;

    public class CalculadoraRequest {{
        public static void main(String[] args) {{
            try {{
                URL url = new URL("{dominio}calculadora");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);

                String jsonInputString = "{{\\"valor1\\":10,\\"valor2\\":5,\\"operacao\\":\\"+\\"}}";

                try(OutputStream os = conn.getOutputStream()) {{
                    byte[] input = jsonInputString.getBytes("utf-8");
                    os.write(input, 0, input.length);
                }}

                int code = conn.getResponseCode();
                System.out.println("Response Code: " + code);

            }} catch (Exception e) {{
                e.printStackTrace();
            }}
        }}
    }}
    '''
    return render_template("index.html", titulo='JS(Puro)', codigo=codigo_java, img='javaIcon.jpg')

@app.route("/", methods=['GET'])
def hello():
    """
    Calculo Simples
    ---
    description: | 
        <div>
            <h1>Exemplos de código:</h1>
            <h2><a href="/exemploJs" target="_blank">JavaScript</a></h2>
            <h2><a href="/exemploJsJquery" target="_blank">JavaScript(Jquery)</a></h2>
            <h2><a href="/exemploJava" target="_blank">Java</a></h2>
        </div>
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
    x-extra-info: "<p>Conteúdo HTML extra aqui</p>"
    """
    parametros = todosParamtros()
    erro = validar_parametros(parametros)
    if erro:
        return erro, 400
    return executaCalculo(parametros['valor1'], parametros['valor2'], parametros['operacao'])

if __name__ == "__main__":
    app.run(debug=True)