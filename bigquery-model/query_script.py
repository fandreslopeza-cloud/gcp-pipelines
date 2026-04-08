from google.cloud import bigquery

def query():
    client = bigquery.Client()

    query = """
    SELECT name, COUNT(order_id) AS total_pedidos, SUM(price) AS total_gastado
    FROM ecommerce_dataset.denormalized_view
    GROUP BY name
    ORDER BY total_gastado DESC;
    """
    results = client.query(query).to_dataframe()

    print(results)

if __name__ == "__main__":
    query()