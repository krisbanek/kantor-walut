from flask import Flask
from flask import render_template
from flask import request, redirect
import requests
import csv
import json

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

with open('rates.csv', 'w', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';')
    csvwriter.writerow(data[0]['rates'][0].keys())
    for rate in data[0]["rates"]:
        csvwriter.writerow(rate.values())

app = Flask(__name__)

@app.route('/kantor', methods=['GET', 'POST'])
def kantor():
    if request.method == 'GET':
        print("GET")
        return render_template("kantor.html")
    elif request.method == 'POST':
        print("POST")
        data = request.form
        code = data.get('code')
        value = data.get('value')
        with open('rates.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=';')
            for row in csvreader:
                if code == row["code"]:
                    bid = float(row["bid"])
                    result = float(value)*bid
                    results = [f"{result}"]
                    return render_template("kantor.html", results = results)