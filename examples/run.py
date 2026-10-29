"""Minimal example: run the woolworths-products-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "query": "",
    "brand": "",
    "onSpecialOnly": False,
    "inStockOnly": False,
    "maxItems": 50,
}

run = client.actor("bibian/woolworths-products-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    was = f" (was {item.get('wasPrice')})" if item.get("onSpecial") else ""
    print(f"{item['name']} | {item.get('brand') or '-'} | {item.get('category')} | {item.get('price')} {item.get('currency')}{was}")
print(f"{count} results")
