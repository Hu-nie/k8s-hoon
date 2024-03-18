from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date
import json

class BasketballStats:
    def __init__(self, client, output_format, current_date):
        self.client = client
        self.output_format = output_format
        self.current_date = current_date

    def daily_player_stats(self):
        daily_stats_raw = self.client.player_box_scores(
            day=self.current_date.day, 
            month=self.current_date.month, 
            year=self.current_date.year, 
            output_type=self.output_format
        )

        return json.loads(daily_stats_raw)

    def daily_team_stats(self):
        team_stats_raw = self.client.team_box_scores(
            day=self.current_date.day,
            month=self.current_date.month,
            year=self.current_date.year,
            output_type=self.output_format
        )
        return json.loads(team_stats_raw)

    def specific_player_stats(self, player_name):

        all_players_stats = self.daily_player_stats()
        return [stat for stat in all_players_stats if player_name in stat['name']]


    def specific_team_stats(self, team_name):
        all_teams_stats = self.daily_team_stats()
        return [stat for stat in all_teams_stats if team_name in stat['team']]

if __name__ == "__main__":
    stats_scraper = BasketballStats(client, OutputType.JSON, date.today())
    player_daily_stats = stats_scraper.daily_player_stats()
    print("Player Stats:", player_daily_stats)
    
    team_daily_stats = stats_scraper.daily_team_stats()
    print("Team Stats:", team_daily_stats)
