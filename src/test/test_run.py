import pytest
import sys
sys.path.insert(0, '/home/hoon/k8s-hoon/src')

from run import app

@pytest.fixture
def client():
    """테스트 클라이언트 설정."""
    with app.test_client() as client:
        yield client

def test_welcome(client):
    """기본 엔드포인트 테스트."""
    response = client.get('/')
    assert response.status_code == 200

def test_player_stats(client):
    """선수 통계 엔드포인트 테스트."""
    response = client.get('/basketball/player-stats?date=2022-01-01')
    assert response.status_code == 200
 
def test_team_stats(client):
    """팀 통계 엔드포인트 테스트."""
    response = client.get('/basketball/team-stats?date=2022-01-01&team=Lakers')
    assert response.status_code == 200

def test_season_standings(client):
    """시즌 순위 엔드포인트 테스트."""
    response = client.get('/basketball/season-standings?date=2022-01-01')
    assert response.status_code == 200

def test_team_season_record(client):
    """팀 시즌 기록 엔드포인트 테스트."""
    response = client.get('/basketball/team-season-record?date=2022-01-01&team=Lakers')
    assert response.status_code == 200