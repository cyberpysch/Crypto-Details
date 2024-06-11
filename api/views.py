# views.py
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CryptoSearchForm
from .models import SearchRecord
from django.conf import settings

# Your API key (ensure to keep it safe, it's good practice to use environment variables for sensitive data)
api_key=settings.API_KEY

def index(request):
    if request.method == 'GET':
        form = CryptoSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query'].strip()
            if not query:
                return HttpResponse("Query (name or symbol) is required", status=400)
            
            url_list = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
            params_list = {
                'start': '1',
                'limit': '5000',  # Fetch a large number to ensure we cover all popular cryptocurrencies
                'convert': 'INR'
            }
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': api_key,
            }

            response_list = requests.get(url_list, params=params_list, headers=headers)
            if response_list.status_code == 200:
                json_list = response_list.json()
                coins = json_list['data']

                # Find the cryptocurrency with the matching name or symbol
                coin = next((coin for coin in coins if coin['name'].lower() == query.lower() or coin['symbol'].lower() == query.lower()), None)

                if coin:
                    symbol = coin['symbol']
                    url_quote = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
                    params_quote = {
                        'symbol': symbol,
                        'convert': 'INR'
                    }
                    response_quote = requests.get(url_quote, params=params_quote, headers=headers)
                    if response_quote.status_code == 200:
                        json_quote = response_quote.json()
                        if symbol in json_quote['data']:
                            coin_data = json_quote['data'][symbol]
                            context = {
                                'name': coin_data['name'],
                                'symbol': coin_data['symbol'],
                                'price': f"₹{coin_data['quote']['INR']['price']:.2f}",
                                'volume_24h': f"{coin_data['quote']['INR']['volume_24h']}",
                                'volume_change_24h': f"{coin_data['quote']['INR']['volume_change_24h']}",
                                'circulating_supply': coin_data['circulating_supply'],
                                'total_supply': coin_data['total_supply'],
                                'max_supply': coin_data['max_supply'],
                                'fully_diluted_market_cap': f"₹{coin_data['quote']['INR']['fully_diluted_market_cap']:.2f}",
                            }
                            print(context)
                            
                            return render(request, 'api/index.html', context)
                        else:
                            return HttpResponse("Cryptocurrency not found.", status=404)
                    else:
                        return HttpResponse(f"Error {response_quote.status_code}: {response_quote.reason}", status=response_quote.status_code)
                else:
                    return HttpResponse("Cryptocurrency not found.", status=404)
            else:
                return HttpResponse(f"Error {response_list.status_code}: {response_list.reason}", status=response_list.status_code)
    else:
        form = CryptoSearchForm()

    return render(request, 'api/index.html', {'form': form})