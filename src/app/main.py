from flask import Flask ,jsonify
from data_scraper import *
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

app = Flask(__name__)

data_scraper = DataScraper(client, OutputType.JSON, date.today())

@app.route('/data')
def hello():
    data = data_scraper.data_scrap()

    return jsonify(data)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5004, debug=True)