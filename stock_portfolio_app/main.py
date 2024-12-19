import os

from controller import StockController
from pymongo import MongoClient


def main():
    """
    Entry point for the Stock Portfolio Manager application.
    Initializes the StockController and runs the Flask app.
    """
    try:
        client = MongoClient("mongodb://mongodb:27017/")
        db = client["stock_portfolio"]
        stocks_collection = db[os.getenv("MONGO_COLLECTION")]

        controller = StockController(stocks_collection)

        # Run the Flask app
        port = int(os.getenv("FLASK_PORT"))
        controller.app.run(host='0.0.0.0', port=port)

    except Exception as e:
        print(f"Error starting the Stock Portfolio Manager: {str(e)}")


if __name__ == '__main__':
    main()