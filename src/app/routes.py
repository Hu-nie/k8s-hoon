from flask import jsonify, Blueprint
from .data_scraper import DataScraper
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return jsonify({'message': 'Hello, Flask!'})
   
@bp.route('/data_collect', methods=['GET'])
async def bsketball_data_scrape():
    data_scraper = DataScraper(client, OutputType.JSON, date.today())
    data = data_scraper.data_scrap()

    return jsonify(data)