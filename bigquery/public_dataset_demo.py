import sys
from google.cloud import bigquery

def query_demo(limit=50):
    client = bigquery.Client()

    query = f"""
    SELECT order_items.id, order_id, product_id, products.name
    FROM `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
    JOIN `bigquery-public-data.thelook_ecommerce.products` AS products
    ON order_items.product_id = products.id
    LIMIT {limit}
    """
    results = client.query(query).to_dataframe()

    print(results)

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    query_demo(limit)