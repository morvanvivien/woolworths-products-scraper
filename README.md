# How to Scrape Woolworths Australia: Grocery Prices, Specials and Unit Prices

> **Run it now, no code: [woolworths-products-scraper on the Apify Store](https://apify.com/bibian/woolworths-products-scraper)** &nbsp;|&nbsp; $2.50 per 1,000 products &nbsp;|&nbsp; no browser, no login

Woolworths is Australia's largest supermarket chain, with well over 100,000 products listed online and no public export or official API for third parties. This guide shows how to get its catalogue as clean structured data: name, brand, department, category, price, unit (cup) price and special offers, with a free Apify Actor, from the console or from code.

Searches this page answers: woolworths scraper, australia grocery price scraper, woolworths product api, australian supermarket price tracker.

## What you get from the Woolworths scraper

- Every product Woolworths lists, discovered through its own product sitemap (over 100,000 products across three shards).
- Current price, previous ("was") price and exact savings amount for products on special.
- Woolworths' own per-unit comparison price (`cupPrice` / `cupString`, for example per 100 g or per litre).
- Department, category and sub-category, brand, package size, barcode and stock status.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, long texts untouched) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `sku`, `url` | Woolworths product id and public product page |
| `barcode` | EAN/UPC barcode, when the product carries one |
| `name`, `brand` | Product name as displayed and brand (`null` when Woolworths does not label one) |
| `department`, `category`, `subCategory` | Woolworths' own catalogue hierarchy |
| `packageSize` | Pack size or weight as displayed, for example `"165g"` |
| `currency`, `price` | Currency (always `AUD`) and current price |
| `onSpecial`, `wasPrice`, `savingsAmount` | Whether a previous price is shown, that previous price, and the exact discount |
| `cupPrice`, `cupString` | Woolworths' per-unit comparison price and its display string, for example `"$1.82 / 100G"` |
| `inStock` | Whether the site marks the product as available |
| `imageUrl` | Product image |

## Use cases

- **Track grocery prices.** Compare `price` and `cupString` across brands and categories to see what a litre of milk or a kilo of biscuits actually costs.
- **Find specials.** Set `onSpecialOnly` to keep only products that carry a previous ("was") price, with the exact `savingsAmount`.
- **Watch a brand's range.** Set `brand` to list every product Woolworths carries under a given label, with its current price and stock status.
- **Feed a price comparison site or a cost-of-living tracker.** The structured fields and the canonical `url` are enough to power a niche comparison tool for Australian shoppers.

## Input

| Field | What it does |
|---|---|
| `query` | Text matched against the product name, for example `"chocolate biscuits"`. Accents and case are ignored. Empty means no filter. |
| `brand` | Keep only this brand, for example `"Arnott's"`. Case is ignored. |
| `onSpecialOnly` | Keep only products that show a previous ("was") price. |
| `inStockOnly` | Keep only products the site marks as available. |
| `maxItems` | The run stops once this many products are saved (default 50). |
| `onlyNew` | For scheduled runs: skip products an earlier run already delivered, so each run returns, and charges, only what is new. |

Example input:

```json
{
  "query": "",
  "brand": "",
  "onSpecialOnly": false,
  "inStockOnly": false,
  "maxItems": 50
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/woolworths-products-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (search text, brand, filters and the maximum number of products) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily price watch, open **Schedules**, create a daily schedule for the Actor and turn on `onlyNew` so each run only returns products added or changed since the last one.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/woolworths-products-scraper').call({
    "query": "",
    "brand": "",
    "onSpecialOnly": false,
    "inStockOnly": false,
    "maxItems": 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.name} | ${item.brand ?? '-'} | ${item.category} | ${item.price} ${item.currency}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/woolworths-products-scraper").call(run_input={
    "query": "",
    "brand": "",
    "onSpecialOnly": False,
    "inStockOnly": False,
    "maxItems": 50,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['name']} | {item.get('brand')} | {item.get('category')} | {item.get('price')} {item.get('currency')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$2.50 per 1,000 products** (that is $0.0025 per product), plus a tiny start fee. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/woolworths-products-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- Only what Woolworths publishes is collected. No login or browser is needed: product pages are read directly, with an automatic retry through a datacenter proxy on the rare request the site blocks.
- A handful of sitemap entries are discontinued products still indexed by the site: `inStock` is `false` and `price` / `cupPrice` are `0` for those (visible in `sample-output.json`). Set `inStockOnly` to skip them.
- `wasPrice` and `savingsAmount` are empty for products that are not currently discounted. `onSpecial` is `true` only when a previous price is shown.
- This dataset is product catalogue data, not personal data: no customer or reviewer information is collected.
- This is an unofficial tool, not affiliated with Woolworths. Check the site terms that apply to your use.

## FAQ

**Does it need a browser or a proxy?**  
No. The Actor reads product pages directly, so runs are fast and cheap; a datacenter proxy is only used as an automatic retry on the rare blocked request.

**How do I track price changes over time?**  
Schedule the Actor daily or weekly and turn on `onlyNew`, or export each run's dataset and compare `price` by `sku` across runs.

**Can I limit the run to one brand or department?**  
Yes, set `brand` to filter by brand. There is currently no department filter; use `query` to narrow by product name instead.

**Can I get the data in Excel or Google Sheets?**  
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open woolworths-products-scraper on the Apify Store](https://apify.com/bibian/woolworths-products-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publisher.
