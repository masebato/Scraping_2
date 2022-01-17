from flask import  Flask,jsonify,request
from main import *
import json
app = Flask(__name__)

@app.route('/ping')
def ping():
    return "iniciar()"

@app.route('/')
def d():
    # Create Dictionary
    value = {
        "language": 'language',
        "company": 'company',
        "Itemid": 'Itemid',
        "price": 'price'
    }
 
    # Dictionary to JSON Object using dumps() method
    # Return JSON Object
    return json.dumps(value)

# @app.route('/prueba')
# def prueba1():
#     p1 = request.args.get('id','No contiene este parametro')
#     p2 = request.args.get('fecha', 'No contiene este parametro')
#     p3 = request.args.get('ciudad', 'No contiene este parametro')
#     p4 = request.args.get('entidad', 'No contiene este parametro')
#     print(p1,p2,p3,p4)
#     return iniciar2(p1,p2,p3,p4)   

@app.route('/proceso')
def prueba():
    p1 = request.args.get('id','No contiene este parametro')
    print(p1)
    # Create Dictionary
    value = {
        "Error": 'Carga',
    }
    try:
        return  jsonify(iniciar(p1))
    except:
        return json.dumps(value)

if __name__=='__main__':
    # app.run(host='0.0.0.0', port=9090)
    app.run(host='127.0.0.1')


