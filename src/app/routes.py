from flask import request, jsonify, Blueprint
from .basketball_stats import BasketballStats  # ExtendedBasketballStats로 변경 가능
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date
import re

bp = Blueprint('main', __name__)

@bp.route('/')
async def welcome():
    """API 가동 상태 확인 엔드포인트."""
    return jsonify({'message': 'Basketball Stats API에 오신 것을 환영합니다!'})
   
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

# 시즌 순위 조회 엔드포인트 추가
@bp.route('/basketball/season-standings', methods=['GET'])
async def get_season_standings():
    query_date_str = request.args.get('date', date.today().isoformat())
    query_date = date.fromisoformat(query_date_str)
    
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    standings = stats_scraper.season_standings()
    return jsonify(standings)

# 특정 팀의 시즌 기록 조회 엔드포인트 추가
@bp.route('/basketball/team-season-record', methods=['GET'])
async def get_team_season_record():
    query_date_str = request.args.get('date', date.today().isoformat())
    team_name = request.args.get('team')

    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not date_pattern.match(query_date_str):
        return jsonify({'error': 'Date must be in YYYY-MM-DD format'}), 400

    try:
        query_date = date.fromisoformat(query_date_str)
    except ValueError:
        # 형식은 맞지만 유효하지 않은 날짜 예: 2022-02-30
        return jsonify({'error': 'Invalid date'}), 400
    
    if not team_name:
        return jsonify({'error': 'Team name is required'}), 400
    
    stats_scraper = BasketballStats(client, OutputType.JSON, query_date)
    record = stats_scraper.team_season_record(team_name)
    return jsonify(record)
