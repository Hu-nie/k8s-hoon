from flask import request, jsonify, Blueprint
from .basketball_stats import BasketballStats
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date

bp = Blueprint('main', __name__)


@bp.route('/')
async def welcome():
    """Endpoint to check if the API is running."""
    return jsonify({'message': 'Welcome to the Basketball Stats API!'})
   
@bp.route('/basketball/stats', methods=['GET'])
async def get_daily_player_stats():
    """Endpoint to retrieve basketball player stats for a given date."""
    query_date_str = request.args.get('date', date.today().isoformat())
    query_date = date.fromisoformat(query_date_str)
    
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    daily_stats = stats_scraper.daily_player_stats()

    return jsonify(daily_stats)