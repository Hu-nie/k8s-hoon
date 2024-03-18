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

if __name__ == "__main__":
    stats_scraper = BasketballStats(client, OutputType.JSON, date.today())
    daily_stats = stats_scraper.scrape_daily_player_stats()
    print(daily_stats)
