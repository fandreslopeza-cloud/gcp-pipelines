from google.cloud import bigquery

def query():
    client = bigquery.Client()

    with open("create_dataset.sql","r") as file:
        slq_query = file.read()

    results = client.query(slq_query)
    results.result()

    print("Se ha creado correctamente el esquema y tablas")

if __name__ == "__main__":
    query()