from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import random
import os

app = Flask (__name__)
client =MongoClient("mongodb://127.0.0.1:27017")
db=client.proyecto
prendas= db.Prendas
carrito = db.carrito
cliente =db.Cliente

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

@app.route("/cliente")
def clientes():
    cliente_1= cliente.find()
    return render_template('cliente.html', prendas=cliente_1,tittle=t)

@app.route("/verCarrito")
def verCarrito():
    prendas_carrito = carrito.find({"_id":"1.0"}, {"_id":0})
    lista = prendas_carrito[0]
    prenditas = lista["prendas"]
    cliente_1=cliente.find()
    totalPagar = 0
    for i in prenditas:
        totalPagar = totalPagar + i["Precio"] 
    return render_template('verCarrito.html',cliente=cliente_1, prendas=prenditas,tittle=t, totalPagar = totalPagar)

@app.route("/clasificacionNina")
def clasificacion1():
    prendas_1 = prendas.find({'Clasificaciones':{'$in':["001"]}})
    return render_template('index.html',prendas=prendas_1,tittle=t)

@app.route("/clasificacionNino")
def clasificacion2():
    prendas_1 = prendas.find({'Clasificaciones':{'$in':["002"]}})
    return render_template('index.html',prendas=prendas_1,tittle=t)

@app.route("/clasificacionDama")
def clasificacion3():
    prendas_1 = prendas.find({'Clasificaciones':{'$in':["003"]}})
    return render_template('index.html',prendas=prendas_1,tittle=t)

@app.route("/clasificacionVaron")
def clasificacion4():
    prendas_1 = prendas.find({'Clasificaciones':{'$in':["004"]}})
    return render_template('index.html',prendas=prendas_1,tittle=t)

@app.route("/agregarCarrito", methods=["POST"])
def agregarCarrito():
    #obtiene la informacion de la prenda que le dio agregar al carrito
    Codigo =request.values.get("Codigo")
    Nombre=request.values.get("Nombre")
    Precio=request.values.get("Precio")
    Color=request.values.get("Color")
    Numero_de_Ventas=request.values.get("Numero_de_Ventas")
    Numero_de_Vistas=request.values.get("Numero_de_Vistas")
    Stock=request.values.get("Stock")
    Descripcion=request.values.get("Descripcion")
    categoria=request.values.get("categoria")
    URL_de_imagen=request.values.get("URL_de_imagen")
    Clasificaciones=request.values.get("Clasificaciones")
    Estilo_de_Fabricacion=request.values.get("Estilo_de_Fabricacion")
    #inserta la prenda en el carrito    
    prendaAinsertar={'Codigo':Codigo, 'Nombre':Nombre, 'Precio':float(Precio), 'Color':Color, 'Numero_de_Ventas':float(Numero_de_Ventas), 
     'Numero_de_Vistas':float(Numero_de_Vistas), 'Stock':float(Stock),'Descripcion':Descripcion, 'categoria':categoria, 'URL_de_imagen':URL_de_imagen,
      'Clasificaciones':Clasificaciones, 'Estilo_de_Fabricacion':Estilo_de_Fabricacion}
    carrito.update({"_id":"1.0"}, {'$push':{'prendas':prendaAinsertar}})    
    #disminuye el stock en 1 por la reserva de la prenda
    #db.Prendas.update({"Codigo" : 'Alpaca.P.001'},{"$inc":{"Stock":-1}})
    prendas.update({"Codigo":Codigo},{'$inc':{'Stock':-1}})
    return redirect("/list")

@app.route("/quitarCarrito", methods=["POST"])
def quitarCarrito():
    #obtiene la informacion de la prenda que le dio agregar al carrito
    Codigo =request.values.get("Codigo")
    
    #elimina la prenda en el carrito
    #db.carrito.update({_id : 1.0},{$pull:{"prendas":{"Codigo":"Alpaca.P.001"}}})
    carrito.update({"_id":"1.0"},{'$pull':{"prendas":{"Codigo":Codigo}}})
        
    #aumenta el stock en 1 por la reserva de la prenda
    #db.Prendas.update({"Codigo" : 'Alpaca.P.001'},{"$inc":{"Stock":1}})
    prendas.update({"Codigo":Codigo},{'$inc':{'Stock':1}})
    return redirect("/verCarrito")

@app.route("/resetearCarrito")
def resetearCarrito():
    # db.carrito.update({"_id":"1.0"}, {"prendas":[]})
    carrito.update({"_id":"1.0"},{'prendas':[]})
    return redirect("/verCarrito")

@app.route("/pagar")
def pagarPaypal():
    #obtiene el total de precio de las prendas del carrito
    prendas_carrito = carrito.find({"_id":"1.0"}, {"_id":0})
    lista = prendas_carrito[0]
    prenditas = lista["prendas"]
    totalPagar = 0
    for i in prenditas:
        totalPagar = totalPagar + i["Precio"]
        totalPagar = totalPagar
    totalPagar = totalPagar* -1
    #obtiene los datos del form cliente que va a pagar
    pago=request.values.get("pago")
    Nombre=request.values.get("refer")
    
    #se descuenta el monto en de la tarjeta
    # db.Cliente.update({"_id" : 20001.0},{"$inc":{"Saldo_de_Paypal":-100}})
    if(random.random()<0.8):
        if(pago=="Paypal"):
            cliente.update({"Nombre":Nombre},{'$inc':{"Saldo_de_Paypal":totalPagar}})
        else:
            cliente.update({"Nombre":Nombre},{'$inc':{"Saldo_de_tarjeta":totalPagar}})
    resetearCarrito()
    return redirect("/list")

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

@app.route("/fabricacionManual")
def estilo_1():
    prendas_l = prendas.find({"Estilo_de_Fabricacion":"Manual"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

@app.route("/fabricacionMaquina")
def estilo_2():
    prendas_l = prendas.find({"Estilo_de_Fabricacion":"Maquina"})
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