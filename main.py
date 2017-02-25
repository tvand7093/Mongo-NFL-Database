
from crawlers.nfl_crawler import NFLCrawler
from crawlers.scraper import Scraper
from crawlers.coach_scraper import CoachScraper
from pymongo import MongoClient, TEXT
from config import Config

import urllib
import os

def mongoConnect(params):
    password = urllib.quote_plus(params.MONGO_PASS)

    uri = "mongodb://{0}:{1}@{2}/{3}".format(params.MONGO_USER, 
        password,
        params.MONGO_HOST,
        params.MONGO_DB)

    return MongoClient(host=uri)[params.MONGO_DB]

def reset(db):
    """ Resets the database by deleting every record in every table. """
    
    print "Resetting database state..."
    db.teams.drop()
    print "Database reset"

def insertTeams(db, teams):
    db.teams.insert_many(teams)
    db.teams.create_index([('$**', TEXT)], default_language='english')
    
def scrape(db):
    """ Main method for scraping all relevant data. """

    print "Scraping data..."
    nfl = NFLCrawler()
    team = Scraper()

    html = nfl.getClubsHtml()
    teams = team.scrape(html)
    insertTeams(db, teams)

    print "Done scraping data..."

def main():
    # Get environment variables
    config = Config()
    if not config.wasLoaded:
        return

    # Got variables, continue to process.
    db = mongoConnect(config)
    reset(db)
    scrape(db)

if __name__ == "__main__":
    main()