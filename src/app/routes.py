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
   
@bp.route('/basketball/player-stats', methods=['GET'])
async def get_player_stats():
    
    query_date_str = request.args.get('date', date.today().isoformat())
    player_name = request.args.get('player', None) 
    query_date = date.fromisoformat(query_date_str)
    
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    if player_name:
        stats = stats_scraper.specific_player_stats(player_name)
    else:
        stats = stats_scraper.daily_player_stats()
    return jsonify(stats)

@bp.route('/basketball/team-stats', methods=['GET'])
async def get_team_stats():
    query_date_str = request.args.get('date', date.today().isoformat())
    team_name = request.args.get('team', None)  
    query_date = date.fromisoformat(query_date_str)
    
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    if team_name:
        stats = stats_scraper.specific_team_stats(team_name)
    else:
        stats = stats_scraper.daily_team_stats()
    return jsonify(stats)