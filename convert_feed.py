# convert_feed.py
import requests
import xml.etree.ElementTree as ET
import json
import os

XML_FEED_URL = 'https://feeds.mergado.com/vercajk21-cz-heureka-cz-produktovy-cz-c76409029f601749502d19accee40f02.xml'
OUTPUT_FILENAME = 'heureka_products.json'


def convert_xml_to_json():
    print(f"Downloading XML feed from {XML_FEED_URL}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(XML_FEED_URL, headers=headers, timeout=60)
        response.raise_for_status()

        print("Parsing XML data...")
        root = ET.fromstring(response.content)

        products = []
        for item in root.findall('SHOPITEM'):
            item_id_element = item.find('ITEM_ID')
            product_name_element = item.find('PRODUCTNAME')

            if item_id_element is not None and product_name_element is not None:
                products.append(
                    {
                        'ITEM_ID': item_id_element.text,
                        'PRODUCTNAME': product_name_element.text,
                    }
                )

        print(f"Saving data to {OUTPUT_FILENAME}...")
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False)

        print(f"Successfully created {OUTPUT_FILENAME} with {len(products)} products.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the feed: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    convert_xml_to_json()
