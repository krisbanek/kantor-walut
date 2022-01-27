from flask import Flask
from flask import render_template
from flask import request, redirect
import requests
import csv
import json

def getdata_csvwriter():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    with open('rates.csv', 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(data[0]['rates'][0].keys())
        for rate in data[0]["rates"]:
            csvwriter.writerow(rate.values())

def getdata():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data


app = Flask(__name__)

@app.route('/kantor', methods=['GET', 'POST'])
def kantor():
    #getdata_csvwriter()              #Avaiable on request.
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    code_list = []
    for rate in data[0]["rates"]:
        code_list.append(rate['code'])
    if request.method == 'GET':
        print("GET")
        return render_template("kantor.html", myData=code_list)
    elif request.method == 'POST':
        print("POST")
        data_html = request.form
        code = data_html.get('code')
        value = data_html.get('value')
        for rate in data[0]["rates"]:
            if code == rate['code']:
                result = float(value)*float(rate['bid'])
                results = [f"{result}"]
                return render_template("kantor.html", results = results, myData=code_list)
        