import argparse
from google.cloud import bigquery

def query_top_products(limit=50, order="quantity"):
    client = bigquery.Client()

    order_mapping = {
        "quantity": "quantity DESC, revenue DESC",
        "revenue": "revenue DESC, quantity DESC"
    }

    order_by = order_mapping.get(order, "quantity")

    query = f"""
    SELECT
        products.id,
        products.name,
        products.category,
        products.brand,
        COUNT(*) AS quantity,
        ROUND(SUM(order_items.sale_price),2) AS revenue
    FROM `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
    JOIN `bigquery-public-data.thelook_ecommerce.products` AS products
    ON order_items.product_id = products.id
    WHERE order_items.status = 'Complete'
    GROUP BY
        products.id,
        products.name,
        products.category,
        products.brand
    ORDER BY {order_by}
    LIMIT @limit
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ]
    )

    results = client.query(query, job_config=job_config).to_dataframe()

    print(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Top productos más vendidos")

    parser.add_argument("--limit",type=int,default=50,help="Cantidad de registros")

    parser.add_argument("--order",choices=["quantity", "revenue"],default="quantity",help="Ordenar por cantidad o revenue")

    args = parser.parse_args()

    query_top_products(args.limit, args.order)