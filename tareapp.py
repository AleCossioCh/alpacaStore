from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask (__name__)
client =MongoClient("mongodb://127.0.0.1:27017")
db=client.proyecto
prendas= db.Prendas
carrito = db.carrito
t="AlpacaStore"

def redirect_url():
    return request.args.get('next') or \
        request.referrer or \
        url_for('index')

@app.route("/")
@app.route("/list")
def lists():
    prendas_1= prendas.find()
    return render_template('index.html', prendas=prendas_1,tittle=t)

@app.route("/verCarrito")
def verCarrito():
    prendas_carrito = carrito.find({"_id":"1.0"}, {"_id":0})
    lista = prendas_carrito[0]
    prenditas = lista["prendas"]
    totalPagar = 0
    for i in prenditas:
        totalPagar = totalPagar + i["Precio"] 
    return render_template('verCarrito.html',prendas=prenditas,tittle=t, totalPagar = totalPagar)

@app.route("/search", methods=["GET"])
def search():
    key=request.values.get("key")
    refer=request.values.get("refer")
    if(key=="_id"):
        prendas_1=prendas.find({refer:ObjectId(key)})
    else:
        prendas_1=prendas.find({refer:key})
    return render_template('searchlist.html',prendas=prendas_1,t=t)

@app.route("/CategoriaGorras")
def tasks ():
    prendas_l = prendas.find({"categoria":"1.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/CategoriaCalcetines")
def tasks1 ():
    prendas_l = prendas.find({"categoria":"2.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)


@app.route("/CategoriaChalecos")
def tasks3 ():
    prendas_l = prendas.find({"categoria":"3.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)



@app.route("/CategoriaPullovers")
def tasks4 ():
    prendas_l = prendas.find({"categoria":"4.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/CategoriaPonchos")
def tasks5 ():
    prendas_l = prendas.find({"categoria":"5.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/Categoriachalinas")
def tasks6 ():
    prendas_l = prendas.find({"categoria":"6.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/CategoriaMantas")
def tasks7 ():
    prendas_l = prendas.find({"categoria":"7.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/CategoriaJerseys")
def tasks8 ():
    prendas_l = prendas.find({"categoria":"8.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/prendasMasVendidas")
def tasks10 ():
    # db.Prendas.find({}).sort({Numero_de_Ventas:-1}).limit(5) 
    prendas_l = prendas.find({})
    prendas_2 = sorted(prendas_l, key=lambda prenda: prenda['Numero_de_Ventas'], reverse=True)
    return render_template('index.html',prendas=prendas_2,tittle=t)

@app.route("/prendasMasVistas")
def tasks11 ():
    # db.Prendas.find({}).sort({Numero_de_Ventas:-1}).limit(5) 
    prendas_l = prendas.find({})
    prendas_2 = sorted(prendas_l, key=lambda prenda: prenda['Numero_de_Vistas'])
    return render_template('index.html',prendas=prendas_2,tittle=t)

if __name__=="__main__":
    app.run()