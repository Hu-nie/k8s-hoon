from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date

def main():
    today = date.today()
    year = today.year
    month = today.month
    day = today.day - 1
    
    client.player_box_scores(
        day=day, month=month, year=year, 
        output_type=OutputType.CSV, 
        output_file_path=f"./{day}_{month}_{year}_box_scores.csv"
    )

if __name__ == "__main__":
    main()