from flask import request, jsonify, Blueprint
from .basketball_stats import BasketballStats
from .utils import *
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType


bp = Blueprint('main', __name__)

@bp.route('/')
async def welcome():
    """API 가동 상태 확인 엔드포인트."""
    return jsonify({'message': 'Basketball Stats API에 오신 것을 환영합니다!'})
   
@bp.route('/basketball/player-stats', methods=['GET'])
async def get_player_stats():
    params, error, status = validate_request_params(request.args)

    if error:
        return jsonify(error), status

    query_date, player_name = params['query_date'], params.get('player')
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    
    if player_name:
        stats = stats_scraper.specific_player_stats(player_name)
    else:
        stats = stats_scraper.daily_player_stats()
    return jsonify(stats)

@bp.route('/basketball/team-stats', methods=['GET'])
async def get_team_stats():
    params, error, status = validate_request_params(request.args)
    if error:
        return jsonify(error), status

    query_date, team_name = params['query_date'], params.get('team')
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)

    if team_name:
        stats = stats_scraper.specific_team_stats(team_name)
    else:
        stats = stats_scraper.daily_team_stats()
    return jsonify(stats)

@bp.route('/basketball/season-standings', methods=['GET'])
async def get_season_standings():
    params, error, status = validate_request_params(request.args)
    if error:
        return jsonify(error), status

    query_date = params['query_date']
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    standings = stats_scraper.season_standings()
    return jsonify(standings)


@bp.route('/basketball/team-season-record', methods=['GET'])
async def get_team_season_record():
    params, error, status  = validate_request_params(request.args)
    if error:
        return jsonify(error), status

    query_date, team_name = params['query_date'], params.get('team')
    error, status = require_param(team_name, 'team')
    if error:
        return jsonify(error), status

    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    record = stats_scraper.team_season_record(team_name)
    return jsonify(record)
