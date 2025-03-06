from src.business.scrapper import Scraper
from src.data_access.database import DatabaseManager

def main():
    try:
        scraper = Scraper()
        db_manager = DatabaseManager()

        result = scraper.upwork_scraper()
        if 'jobs' in result and len(result['jobs']) > 0:
            db_manager.save_jobs_to_db(result['jobs'])

    except RuntimeError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
