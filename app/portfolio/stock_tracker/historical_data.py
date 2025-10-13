from datetime import timedelta
import pandas as pd

from app import db

DATE_COLUMNS = ["Date", "Datum"]
PRICE_COLUMNS = ["Price", "Laatste"]
DATE_FORMATS = {"Date": "%d/%m/%Y", "Datum": "%d-%m-%Y"}


def _get_colum_name(data, options):
    date_column = None
    for col in options:
        if col in data.columns:
            date_column = col
            return date_column
    if not date_column:
        raise ValueError(f"No valid date column found in the CSV file for {options}.")


def populate_historical_data_from_csv(csv_path, stock_id):
    from ..stock_models import HistoricalData

    data = pd.read_csv(csv_path)

    date_column = _get_colum_name(data, DATE_COLUMNS)
    price_column = _get_colum_name(data, PRICE_COLUMNS)
    date_format = DATE_FORMATS[date_column]

    for index, row in data.iterrows():
        try:
            date = pd.to_datetime(row[date_column], format=date_format).date()
            price = float(str(row[price_column]).replace(",", "."))
            HistoricalData.add_or_update_data(stock_id, date, price)

        except Exception as e:
            raise Exception(f"Error processing csv on row {index}: {e}")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error committing csv to database: {e}")


def get_historical_price(historical_data, date=None):
    if not historical_data:
        raise Exception("No historical data found")

    sorted_data = sorted(historical_data, key=lambda x: x.date, reverse=True)

    if date is None:
        return sorted_data[0].price

    closest_data = min(sorted_data, key=lambda x: abs(x.date - date))

    if abs(closest_data.date - date) > timedelta(days=1):
        raise Exception(f"No data available within 1 days of {date}")

    return closest_data.price
