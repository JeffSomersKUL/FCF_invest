from datetime import datetime, date
import requests
from bs4 import BeautifulSoup
import re

from .base import StockInterface
from .historical_data import (
    populate_historical_data_from_csv,
    get_historical_price,
)

URL_KEY = "url"
TAG_TYPE = "tag"
CLASS_KEY = "class"
ID_KEY = "id"


def extract_price(div):
    price_text = div.text.strip()
    match = re.search(r"[\d.,]+", price_text)
    if match:
        price = match.group(0).replace(",", "")
        return price
    else:
        raise ValueError("Failed to extract the price from the available content.")


class Custom(StockInterface):
    def __init__(self, ticker, historical_data, meta_data=None):
        super().__init__(ticker)
        self.historical_data = historical_data
        self.meta_data = meta_data or {}
        self.set_to_scrape = URL_KEY in meta_data

    def scrape_site(self):
        response = requests.get(self.meta_data.get(URL_KEY))
        if response.status_code != 200:
            raise ConnectionError(
                f"Failed to fetch the site. Status code: {response.status_code}"
            )
        soup = BeautifulSoup(response.content, "html.parser")
        class_name = self.meta_data.get(CLASS_KEY)
        element_id = self.meta_data.get(ID_KEY)
        tag_type = self.meta_data.get(TAG_TYPE, "div")

        # Search based on class, ID, or both
        if class_name and element_id:
            price = soup.find(tag_type, {"class": class_name, "id": element_id})
        elif class_name:
            price = soup.find(tag_type, {"class": class_name})
        elif element_id:
            price = soup.find(tag_type, {"id": element_id})
        else:
            raise LookupError(
                "No class or ID provided in metadata for locating " "the price div."
            )
        if not price:
            raise LookupError(
                "Unable to locate the HTML tag containing the stock price."
            )
        return extract_price(price)

    def get_price(self, date_input=None):
        if date_input:
            if isinstance(date_input, datetime):
                date_input = date.date()

            return get_historical_price(self.historical_data, date_input)

        if self.set_to_scrape:
            try:
                return self.scrape_site()
            except Exception:
                pass

        return get_historical_price(self.historical_data)

    def can_live_track(self):
        if not self.set_to_scrape:
            return False
        try:
            self.scrape_site()
            return True
        except Exception:
            return False

    def process_model(self, form, model, _):
        if self.set_to_scrape:
            self.scrape_site()
        if form.csv_file.data:
            populate_historical_data_from_csv(form.csv_file.data, model.id)
