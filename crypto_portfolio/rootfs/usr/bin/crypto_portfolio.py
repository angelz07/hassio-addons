import json
import requests
from datetime import datetime
import logging
from db import add_transaction, get_transactions, delete_transaction, update_transaction, get_crypto_transactions

# Configure logging
logging.basicConfig(level=logging.INFO)

# Flag to enable/disable test transactions
ENABLE_TEST_TRANSACTIONS = True

def get_crypto_id(name):
    url = f"https://api.coingecko.com/api/v3/search?query={name}"
    response = requests.get(url)
    data = response.json()
    for coin in data['coins']:
        if coin['name'].lower() == name.lower():
            return coin['id']
    return None

def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]['usd']

def get_historical_price(crypto_id, date):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/history?date={date}"
    response = requests.get(url)
    data = response.json()
    try:
        return data['market_data']['current_price']['usd']
    except KeyError:
        return None

def add_new_transaction():
    crypto_name = input("Enter the name of the cryptocurrency: ")
    transactions = get_crypto_transactions(crypto_name)
    if transactions:
        crypto_id = transactions[0][2]
    else:
        crypto_id = get_crypto_id(crypto_name)
        if not crypto_id:
            logging.error("Cryptocurrency not found")
            return

    quantity = float(input("Enter the quantity: "))
    price_usd = float(input("Enter the price in USD: "))
    transaction_type = input("Enter the transaction type (buy/sell): ")
    location = input("Enter the location (e.g., Binance, Coinbase): ")
    date = input("Enter the date (YYYY-MM-DD): ")

    historical_price = get_historical_price(crypto_id, datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y"))
    if not historical_price:
        historical_price = price_usd / quantity

    add_transaction(crypto_name, crypto_id, quantity, price_usd, transaction_type, location, date, historical_price)
    logging.info(f"Added transaction: {crypto_name}, {quantity}, {price_usd}, {transaction_type}, {location}, {date}, {historical_price}")

def add_test_transactions():
    test_transactions = [
        ('Polygon', 'matic-network', 244.862, 130.346, 'buy', 'Bitget', '2023-09-18', 0.5323243296223996),
        ('Polygon', 'matic-network', 227.913, 127.461, 'buy', 'Bitget', '2023-10-01', 0.5592528728067289),
        ('Ethereum', 'ethereum', 0.0188939, 30.77, 'buy', 'Kucoin', '2023-10-21', 1628.567950502543),
        ('Ethereum', 'ethereum', 0.01, 18.17, 'sell', 'Kucoin', '2023-10-25', 1817),
        ('Ethereum', 'ethereum', 0.0199527, 41.47, 'buy', 'Bitget', '2023-11-25', 2078.41545254527)
    ]
    for tx in test_transactions:
        add_transaction(*tx)
        logging.info(f"Added test transaction: {tx}")

def calculate_profit_loss():
    transactions = get_transactions()
    crypto_groups = {}
    for transaction in transactions:
        crypto_id = transaction[2]
        if crypto_id not in crypto_groups:
            crypto_groups[crypto_id] = []
        crypto_groups[crypto_id].append(transaction)

    total_investment = 0
    total_value = 0

    for crypto_id, transactions in crypto_groups.items():
        current_price = get_crypto_price(crypto_id)
        investment = 0
        quantity_held = 0
        for transaction in transactions:
            if transaction[5] == 'buy':
                investment += transaction[4]
                quantity_held += transaction[3]
            elif transaction[5] == 'sell':
                investment -= transaction[4]
                quantity_held -= transaction[3]

        current_value = quantity_held * current_price
        total_investment += investment
        total_value += current_value
        profit_loss = current_value - investment
        profit_loss_percent = (profit_loss / investment) * 100 if investment != 0 else 0
        logging.info(f"Crypto: {crypto_id}, Investment: {investment:.2f}, Current Value: {current_value:.2f}, Profit/Loss: {profit_loss:.2f}, Profit/Loss %: {profit_loss_percent:.2f}%")

    total_profit_loss = total_value - total_investment
    total_profit_loss_percent = (total_profit_loss / total_investment) * 100 if total_investment != 0 else 0
    logging.info(f"Total Investment: {total_investment:.2f}, Total Value: {total_value:.2f}, Total Profit/Loss: {total_profit_loss:.2f}, Total Profit/Loss %: {total_profit_loss_percent:.2f}%")

def main():
    if ENABLE_TEST_TRANSACTIONS:
        add_test_transactions()

    while True:
        print("1. Add a new transaction")
        print("2. View transactions")
        print("3. Delete a transaction")
        print("4. Update a transaction")
        print("5. Calculate profit/loss")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_new_transaction()
        elif choice == '2':
            transactions = get_transactions()
            for transaction in transactions:
                print(transaction)
        elif choice == '3':
            transaction_id = int(input("Enter the ID of the transaction to delete: "))
            delete_transaction(transaction_id)
            logging.info(f"Deleted transaction with ID: {transaction_id}")
        elif choice == '4':
            transaction_id = int(input("Enter the ID of the transaction to update: "))
            crypto_name = input("Enter the new name of the cryptocurrency: ")
            transactions = get_crypto_transactions(crypto_name)
            if transactions:
                crypto_id = transactions[0][2]
            else:
                crypto_id = get_crypto_id(crypto_name)
                if not crypto_id:
                    logging.error("Cryptocurrency not found")
                    continue

            quantity = float(input("Enter the new quantity: "))
            price_usd = float(input("Enter the new price in USD: "))
            transaction_type = input("Enter the new transaction type (buy/sell): ")
            location = input("Enter the new location (e.g., Binance, Coinbase): ")
            date = input("Enter the new date (YYYY-MM-DD): ")

            historical_price = get_historical_price(crypto_id, datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y"))
            if not historical_price:
                historical_price = price_usd / quantity

            update_transaction(transaction_id, crypto_name, crypto_id, quantity, price_usd, transaction_type, location, date, historical_price)
            logging.info(f"Updated transaction with ID: {transaction_id}")
        elif choice == '5':
            calculate_profit_loss()
        elif choice == '6':
            break
        else:
            logging.error("Invalid choice")

if __name__ == "__main__":
    main()
