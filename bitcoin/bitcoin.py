import sys
import requests

def main():
    # 1. Ensure a command-line argument was provided
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")

    # 2. Ensure the argument is a valid number (float)
    try:
        bitcoin_count = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")

    # 3. Query the CoinCap v3 API
    try:
        # Note: Remember to replace 'YourApiKey' with the actual API key from your dashboard
        url = "https://rest.coincap.io/v3/assets/bitcoin?apiKey=YourApiKey"
        response = requests.get(url)
        response.raise_for_status()

        # 4. Parse JSON and extract the price
        json_data = response.json()
        price_per_bitcoin = float(json_data["data"]["priceUsd"])

    except requests.RequestException:
        sys.exit("API request failed.")
    except (KeyError, ValueError, TypeError):
        sys.exit("Failed to parse API response structure.")

    # 5. Calculate total cost and format output to 4 decimal places
    total_cost = bitcoin_count * price_per_bitcoin
    print(f"${total_cost:,.4f}")

if __name__ == "__main__":
    main()
