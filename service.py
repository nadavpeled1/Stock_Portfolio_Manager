# service.py
# service.py
import self

from stock import Stock
import requests
NINJA_API_KEY = "" #TODO: Add your API key here
#TODO: test the ninja api functionality
class StockService:
    def __init__(self):
        # dict since we need to support CRUD operations for specific stocks by id
        self.portfolio = {}
        self.nextid = 1

    '''
    If the ‘name’ or ‘purchase date’ is not supplied for a stock on the POST
    request, the JSON representation for those fields is the string ‘NA’ (Not
    Available). E.g., that is what the server returns for those fields in a GET
    request.
    The validity is checked in the controller layer.
    '''
    def add_stock(self, symbol: str, purchase_price: float, shares: int, name: str = 'NA', purchase_date: str = 'NA') -> Stock:
        stock_id = str(self.nextid)
        self.nextid += 1
        new_stock = Stock(stock_id, name, symbol, purchase_price, purchase_date, shares)
        self.portfolio[stock_id] = new_stock
        return new_stock

    def get_stock(self, stock_id: str) -> Stock:
        if stock_id in self.portfolio:
            return self.portfolio[stock_id]
        else:
            raise ValueError("Stock not found")

    def remove_stock(self, stock_id: str) -> None:
        if stock_id in self.portfolio:
            del self.portfolio[stock_id]
        else:
            raise ValueError("Stock not found")

    def fetch_stock_current_price(self, symbol: str) -> float:
            # for more info: https://api-ninjas.com/api/stockprice
            api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
            response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
            if response.status_code == requests.codes.ok:
                price = response.json()['price']
                return round(price, 2)
            else:
                raise ValueError("API response code " + str(response.status_code))

    def get_stock_value(self, symbol: str) -> float:
        #TODO: what about stocks not in the portfolio? should we return 404? or consider 0 value?
        if symbol not in [stock.symbol for stock in self.portfolio.values()]:
            return 0
        for stock in self.portfolio.values():
            if stock.symbol == symbol:
                try:
                    current_price = self.fetch_stock_current_price(symbol)
                    return stock.shares * current_price
                except ValueError as e:
                    raise ValueError("server error: " + str(e))
        raise ValueError("Not found")

    # OLD VERSION
    # def get_stocks(self) -> dict: OLD VERSION
    #     # return a list of stock objects as dictionaries
    #     # for easy serialization to JSON
    #     return {stock_id: stock.to_dict() for stock_id, stock in self.portfolio.items()}

    def get_stocks(self) -> list:
        # return a list of stock objects as dictionaries
        # for easy serialization to JSON
        return [stock.to_dict() for stock in self.portfolio.values()]

    def get_portfolio_value(self) -> float:
        total_value = 0
        for stock in self.portfolio.values():
            current_price = self.fetch_stock_current_price(stock.symbol)
            if current_price:
                total_value += stock.shares * current_price
            else:
                raise ValueError(f"Price for stock {stock.symbol} not available")
        return total_value

