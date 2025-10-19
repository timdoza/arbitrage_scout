# ebay_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ====== TOGGLE ======
USE_MOCK_DATA = True   # 🔧 Switch to False when real eBay API access is approved
# =====================

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_OAUTH_TOKEN = os.getenv("EBAY_OAUTH_TOKEN")


def mock_data_example(search_term):
    """Temporary fake data for safe testing."""
    return [
        {
            "title": f"{search_term} Star Wars Mini Figure - Mock Data",
            "price": 12.99,
            "shipping": 4.0,
            "sold_date": "2024-08-02",
            "profit": 6.50,
        },
        {
            "title": f"{search_term} Collectible Set - Mock Data",
            "price": 22.50,
            "shipping": 5.0,
            "sold_date": "2024-08-01",
            "profit": 14.25,
        },
    ]


def fetch_from_ebay_api(search_term):
    """Fetch sold items from eBay's Buy Browse API."""
    try:
        url = (
            "https://api.ebay.com/buy/browse/v1/item_summary/search"
            f"?q={search_term}&filter=price:[1..1000]"
        )
        headers = {
            "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
            "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=US",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            items = data.get("itemSummaries", [])
            results = []
            for item in items:
                results.append(
                    {
                        "title": item.get("title", "No Title"),
                        "price": item.get("price", {}).get("value", "N/A"),
                        "shipping": item.get("shippingOptions", [{}])[0]
                        .get("shippingCost", {})
                        .get("value", 0),
                        "sold_date": item.get("itemEndDate", "Unknown"),
                    }
                )
            return results

        elif response.status_code == 403:
            return [{"error": "Access denied: Check your API credentials or token."}]
        elif response.status_code == 429:
            return [{"error": "Rate limit exceeded. Try again later."}]
        elif response.status_code == 500:
            return [{"error": "eBay server error. Try again later."}]
        else:
            return [{"error": f"Unexpected error: {response.text}"}]

    except Exception as e:
        return [{"error": str(e)}]


def fetch_sold_data(search_term):
    """Main function called by your app."""
    if USE_MOCK_DATA:
        print("[DEBUG] Using mock data.")
        return mock_data_example(search_term)
    else:
        print("[DEBUG] Using real eBay API.")
        return fetch_from_ebay_api(search_term)