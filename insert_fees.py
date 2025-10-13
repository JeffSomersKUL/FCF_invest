from datetime import datetime
from app import app, db  # Import your app and db instances
from app.portfolio.platform_models import Fee

# Data to insert
data = [
    ("2023-01-13", "Short CFD Interest for 13-JAN-2023", -0.06, "USD"),
    ("2023-01-14", "CFD Borrow Fee for EWI for 14-JAN-2023", 0.15, "USD"),
    ("2023-01-14", "CFD Borrow Fee for TAN for 14-JAN-2023", 0.09, "USD"),
    ("2023-01-14", "Short CFD Interest for 14-JAN-2023", -0.06, "USD"),
    ("2023-01-15", "CFD Borrow Fee for EWI for 15-JAN-2023", 0.15, "USD"),
    ("2023-01-15", "CFD Borrow Fee for TAN for 15-JAN-2023", 0.09, "USD"),
    ("2023-01-15", "Short CFD Interest for 15-JAN-2023", -0.06, "USD"),
    ("2023-01-16", "CFD Borrow Fee for EWI for 16-JAN-2023", 0.15, "USD"),
    ("2023-01-16", "CFD Borrow Fee for TAN for 16-JAN-2023", 0.09, "USD"),
    ("2023-01-16", "Short CFD Interest for 16-JAN-2023", -0.06, "USD"),
    ("2023-01-17", "CFD Borrow Fee for EWI for 17-JAN-2023", 0.17, "USD"),
    ("2023-01-17", "CFD Borrow Fee for TAN for 17-JAN-2023", 0.09, "USD"),
    ("2023-01-17", "Short CFD Interest for 17-JAN-2023", -0.06, "USD"),
    ("2023-01-18", "CFD Borrow Fee for EWI for 18-JAN-2023", 0.15, "USD"),
    ("2023-01-18", "CFD Borrow Fee for TAN for 18-JAN-2023", 0.09, "USD"),
    ("2023-01-18", "Short CFD Interest for 18-JAN-2023", -0.06, "USD"),
    ("2023-01-19", "CFD Borrow Fee for EWI for 19-JAN-2023", 0.14, "USD"),
    ("2023-01-19", "CFD Borrow Fee for TAN for 19-JAN-2023", 0.08, "USD"),
    ("2023-01-19", "Short CFD Interest for 19-JAN-2023", -0.06, "USD"),
    ("2023-01-20", "CFD Borrow Fee for EWI for 20-JAN-2023", 0.14, "USD"),
    ("2023-01-20", "CFD Borrow Fee for TAN for 20-JAN-2023", 0.08, "USD"),
    ("2023-01-20", "Short CFD Interest for 20-JAN-2023", -0.06, "USD"),
    ("2023-01-21", "CFD Borrow Fee for EWI for 21-JAN-2023", 0.14, "USD"),
    ("2023-01-21", "CFD Borrow Fee for TAN for 21-JAN-2023", 0.08, "USD"),
    ("2023-01-21", "Short CFD Interest for 21-JAN-2023", -0.06, "USD"),
    ("2023-01-22", "CFD Borrow Fee for EWI for 22-JAN-2023", 0.14, "USD"),
    ("2023-01-22", "CFD Borrow Fee for TAN for 22-JAN-2023", 0.08, "USD"),
    ("2023-01-22", "Short CFD Interest for 22-JAN-2023", -0.06, "USD"),
    ("2023-01-23", "CFD Borrow Fee for EWI for 23-JAN-2023", 0.14, "USD"),
    ("2023-01-23", "CFD Borrow Fee for TAN for 23-JAN-2023", 0.09, "USD"),
    ("2023-01-23", "Short CFD Interest for 23-JAN-2023", -0.06, "USD"),
    ("2023-01-24", "CFD Borrow Fee for EWI for 24-JAN-2023", 0.14, "USD"),
    ("2023-01-24", "CFD Borrow Fee for TAN for 24-JAN-2023", 0.08, "USD"),
    ("2023-01-24", "Short CFD Interest for 24-JAN-2023", -0.06, "USD"),
    ("2023-01-25", "CFD Borrow Fee for EWI for 25-JAN-2023", 0.15, "USD"),
    ("2023-01-25", "CFD Borrow Fee for TAN for 25-JAN-2023", 0.08, "USD"),
    ("2023-01-25", "Short CFD Interest for 25-JAN-2023", -0.06, "USD"),
    ("2023-01-26", "CFD Borrow Fee for EWI for 26-JAN-2023", 0.15, "USD"),
    ("2023-01-26", "CFD Borrow Fee for TAN for 26-JAN-2023", 0.09, "USD"),
    ("2023-01-26", "Short CFD Interest for 26-JAN-2023", -0.06, "USD"),
    ("2023-01-27", "CFD Borrow Fee for EWI for 27-JAN-2023", 0.14, "USD"),
    ("2023-01-27", "CFD Borrow Fee for TAN for 27-JAN-2023", 0.08, "USD"),
    ("2023-01-27", "Short CFD Interest for 27-JAN-2023", -0.06, "USD"),
    ("2023-01-28", "CFD Borrow Fee for EWI for 28-JAN-2023", 0.14, "USD"),
    ("2023-01-28", "CFD Borrow Fee for TAN for 28-JAN-2023", 0.08, "USD"),
    ("2023-01-28", "Short CFD Interest for 28-JAN-2023", -0.06, "USD"),
]


def insert_fees():
    with app.app_context():  # Access the application context
        for entry in data:
            date, description, amount, currency = entry
            fee = Fee(
                platform_id=2,  # Set platform_id as 2
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                description=description,
                amount=amount,
                currency=currency,
            )
            db.session.add(fee)
        db.session.commit()
        print("Data inserted successfully!")


# Run the insert function
if __name__ == "__main__":
    insert_fees()
