from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        stock = request.form['stock']
        return redirect(url_for('stockGraph', stock=stock))

    response = requests.get("http://localhost:8000/stocks_in_db")
    stocks = response.json()['stocks']

    return render_template('index.html', stocks=stocks)


@app.route('/company/<stock>')
def stockGraph(stock):
    nasdaqCompanies = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOG": "Alphabet Inc.",
        "AMZN": "Amazon.com, Inc.",
        "NVDA": "NVIDIA Corporation",
        "TSLA": "Tesla, Inc.",
        "META": "Meta Platforms, Inc.",
        "ASML": "ASML Holding N.V.",
        "AVGO": "Broadcom Inc.",
        "PEP": "PepsiCo, Inc.",
        "AZN": "AstraZeneca PLC",
        "COST": "Costco Wholesale Corporation",
        "CSCO": "Cisco Systems, Inc.",
        "TMUS": "T-Mobile US, Inc.",
        "ADBE": "Adobe Inc.",
        "TXN": "Texas Instruments Incorporated",
        "CMCSA": "Comcast Corporation",
        "NFLX": "Netflix, Inc.",
        "AMD": "Advanced Micro Devices, Inc.",
        "QCOM":  "QUALCOMM Incorporated"
    }
    # Fetch stock data for the selected symbol using an API
    response = requests.get(f'http://localhost:8000/get_stocks/{stock}')
    data = response.json()

    # Check if data is empty
    if not data['data']:
        return render_template('request_data.html', stock=stock,nasdaqCompanies=nasdaqCompanies)

    # Convert the data to a Pandas DataFrame and create a Plotly trace
    df = pd.DataFrame(data['data'])
    trace = go.Scatter(x=df['Date'], y=df['Close'], mode='lines')

    # Set up the Plotly layout and create a figure
    layout = go.Layout(
        title='',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Close Price'))
    fig = go.Figure(data=[trace], layout=layout)

    # Generate a Plotly div and render the stockInfo template
    div = pyo.plot(fig, output_type='div')
    return render_template('stockInfo.html', plot_div=div, stock=stock,nasdaqCompanies=nasdaqCompanies)


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
