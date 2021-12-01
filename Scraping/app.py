from flask import  Flask,jsonify,request
from main import *

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "iniciar()"

@app.route('/')
def d():
    return jsonify({"message": "pong!"})

@app.route('/prueba')
def prueba():
    p1 = request.args.get('id','No contiene este parametro')
    p2 = request.args.get('fecha', 'No contiene este parametro')
    p3 = request.args.get('ciudad', 'No contiene este parametro')
    p4 = request.args.get('entidad', 'No contiene este parametro')
    print(p1,p2,p3,p4)
    return iniciar(p1,p2,p3,p4)


@app.route('/proceso/<string:id>/<string:fecha>/<string:ciudad>/<string:entidad_especialidad>')
def getProduct(id,fecha,ciudad,entidad_especialidad):
    #print(id," ",fecha," ",ciudad," ",entidad_especialidad)
    return iniciar(id,fecha,ciudad,entidad_especialidad)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)

