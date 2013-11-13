import json
import pandas
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    print 'request.form:', request.form
    if 'data' not in request.form:
        return json.dumps({})
        
    data = json.loads(request.form['data'])

    short_span_data = pandas.ewma(pandas.Series(data), span=12)
    long_span_data = pandas.ewma(pandas.Series(data), span=26)
    macd = short_span_data - long_span_data
    ewma_macd9 = pandas.ewma(macd, span=9)
    histogram = macd - ewma_macd9

    result = {
        'ewma12': list(short_span_data),
        'ewma26': list(long_span_data),
        'macd': list(macd),
        'ewma_macd9': list(ewma_macd9),
        'histogram': list(histogram)
    }

    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)


