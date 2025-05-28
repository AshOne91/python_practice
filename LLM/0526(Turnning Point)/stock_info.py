import yfinance as yf
import pandas as pd

class Stock:
    def __init__(self, symbol):  # ✅ 생성자 이름 수정
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)

    def get_basic_info(self):
        basic_info = pd.DataFrame.from_dict(self.ticker.info, orient="index", columns=["Values"])
        return basic_info.loc[
            ['longName', 'industry', 'sector', 'marketCap', 'sharesOutstanding']
        ].to_markdown()

    def get_financial_statement(self):
        return f"""
### Quarterly Income Statement
{self.ticker.quarterly_income_stmt.loc[
    ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']
].to_markdown()}

### Quarterly Balance Sheet
{self.ticker.quarterly_balance_sheet.loc[
    ['Total Assets', 'Total Liabilities Net Minority Interest', 'Stockholders Equity']
].to_markdown()}

### Quarterly Cash Flow
{self.ticker.quarterly_cash_flow.loc[
    ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow']
].to_markdown()}
"""

def main():
    stock = Stock("AAPL")  # ✅ 클래스가 이제 인자 받을 수 있음
    print(stock.get_basic_info())
    print(stock.get_financial_statement())

if __name__ == "__main__":  # ✅ 위치 옮김 (Python 관례)
    main()
