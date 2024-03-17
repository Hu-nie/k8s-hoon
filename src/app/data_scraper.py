from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date
import pandas as pd
import json

class DataScraper:
    def __init__(self, client, output_type,today):
        self.client = client
        self.output_type = output_type
        self.today = today

    def data_scrap(self):
        year = self.today.year
        month = self.today.month
        day = self.today.day - 2

        raw_data = self.client.player_box_scores(
            day=day, month=month, year=year, 
            output_type=self.output_type
        )

        return json.loads(raw_data)

if __name__ == "__main__":

    data_scraper = DataScraper(client, OutputType.JSON, date.today())
    data = data_scraper.data_scrap()
    print(data)
