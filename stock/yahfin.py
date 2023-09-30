import yfinance as yf

def get_symbols_from_file(file_path):
    symbols = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            symbols.append(line)
    return symbols


symbols = get_symbols_from_file('nasdaq100-sp500.txt')
stats = yf.Tickers(symbols)
bad = []

for k, v in stats.tickers.items():
    try:
        formatted = ""
        formatted += f"{v.info['fiftyTwoWeekLow']}, "
        formatted += f"{v.info['fiftyTwoWeekHigh']}, "
        formatted += f"{v.info['currentPrice']}, "
        formatted += f"{v.info['shortName'].replace(',', '')}, "
        formatted += f"{v.info['sector'].replace(',', '')}, "
        formatted += f"{v.info['industry'].replace(',', '')}, "
        formatted += f"{v.info['symbol']}, "
        formatted += f"{v.info['trailingEps']}, "
        formatted += f"{v.info['marketCap']}"
        print(formatted)
    except Exception as ex:
        bad.append(ex)

# print(f'{i}, {", ".join(str(v) for k, v in s.items())}')
