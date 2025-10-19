from statistics import mean, median

def parse_sold_items(raw_json):
    """
    Takes the raw eBay JSON from get_sold_items() and extracts
    title, price, currency, and URL for each sold listing.
    Returns a structured summary with average/median price.
    """
    try:
        items = (
            raw_json["findCompletedItemsResponse"][0]
            ["searchResult"][0]
            .get("item", [])
        )
    except (KeyError, IndexError, TypeError):
        return {"error": "Invalid or unexpected eBay response format"}

    parsed = []
    prices = []

    for it in items:
        try:
            title = it["title"][0]
            price = float(it["sellingStatus"][0]["currentPrice"][0]["__value__"])
            currency = it["sellingStatus"][0]["currentPrice"][0]["@currencyId"]
            url = it["viewItemURL"][0]

            parsed.append({
                "title": title,
                "price": price,
                "currency": currency,
                "url": url,
            })
            prices.append(price)
        except (KeyError, IndexError, ValueError):
            # Skip malformed entries
            continue

    if not prices:
        return {"message": "No valid sold items found", "items": []}

    summary = {
        "count": len(prices),
        "average_price": round(mean(prices), 2),
        "median_price": round(median(prices), 2),
        "currency": parsed[0]["currency"] if parsed else "USD",
        "items": parsed[:20],  # limit the list for readability
    }
    return summary