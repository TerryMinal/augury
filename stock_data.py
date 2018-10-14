import requests

def company_info(symbol):
    r = requests.get('https://api.iextrading.com/1.0/stock/{}/stats'.format(symbol))
    if r:
        d = r.json()
    else:
        return {"revenue": 0.0, "eps": 0.0, "roe": 0.0}

    return {
        'revenue': d['revenue'],
        'eps': d['latestEPS'],
        'roe': d['returnOnEquity']
    }

def main():
    print(company_info('aapl'))
    print(company_info('fb'))

if __name__ == '__main__':
    main()
