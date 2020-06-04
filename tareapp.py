from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask (__name__)
client =MongoClient("mongodb://127.0.0.1:27017")
db=client.proyecto
prendas= db.Prendas
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


@app.route("/search", methods=["GET"])

def search():
    key=request.values.get("key")
    refer=request.values.get("refer")
    if(key=="_id"):
        prendas_1=prendas.find({refer:ObjectId(key)})
    else:
        prendas_1=prendas.find({refer:key})
    return render_template('searchlist.html',prendas=prendas_1,t=t)

@app.route("/CategoriasGorras")
def tasks ():
    
    prendas_l = prendas.find({"categoria":"2.0"})
    return render_template('index.html',prendas=prendas_l,tittle=t)

# @app.route("/action", methods=["POST"])
# def action():
#     name=request.values.get("name")
#     desc=request.values.get("desc")
#     date=request.values.get("date")
#     pr=request.values.get("pr")
#     todos.insert({"name":name,"desc":desc,"date":date,"pr":pr,"done":"no"})
#     return redirect("/list")

if __name__=="__main__":
    app.run()