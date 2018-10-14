import requests

def company_info(symbol):
    r = requests.get('https://api.iextrading.com/1.0/stock/{}/stats'.format(symbol))

    d = r.json()

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
