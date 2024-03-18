from flask import jsonify
from datetime import date
import re

def validate_date(date_str):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return None, {'error': 'Date must be in YYYY-MM-DD format'}, 400
    try:
        return date.fromisoformat(date_str), None, None
    except ValueError:
        return None, {'error': 'Invalid date'}, 400

def require_param(param_value, param_name):
    if not param_value:
        return {'error': f'{param_name} is required'}, 400
    return None, None

def validate_request_params(args):
    query_date_str = args.get('date', date.today().isoformat())
    player_name = args.get('player', None)
    team_name = args.get('team', None)
    
    query_date, error, status = validate_date(query_date_str)
    if error:
        return error, status

    return {"query_date": query_date, "player": player_name, "team": team_name}, None
