from django.shortcuts import render
from django.http import HttpResponse
import requests

def home(request):
    return render(request, 'index.jinja')

def get_balance(request):
    if request.method == 'POST' and len(request.POST['address']) == 42:
        address = request.POST['address']
        key = ""
        api_url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={key}'

        response = requests.get(api_url)
        data = response.json()
        balance = int(data['result']) / 10**18

        api_transactions_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=5&sort=desc&apikey={key}'
        transactions_response = requests.get(api_transactions_url)
        transactions_data = transactions_response.json()
        transactions = transactions_data['result']

        context = {
            'address': address,
            'balance': balance,
            'transactions': transactions
        }
    else:
        context = {}

    return render(request, 'index.jinja', context)
