import argparse
from google.cloud import storage, bigquery, spanner

def create_bucket(bucket_name, location="US"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    client.create_bucket(bucket, location=location)
    print(f"✅ Bucket creado: {bucket.name}")

def create_bigquery_dataset(dataset_id, location="US"):
    client = bigquery.Client()
    dataset = bigquery.Dataset(f"{client.project}.{dataset_id}")
    dataset.location = location
    client.create_dataset(dataset, exists_ok=True)
    print(f"✅ Dataset creado: {dataset.dataset_id}")

def create_spanner_instance(instance_id, config="regional-us-central1", display_name=None):
    client = spanner.Client()
    instance = client.instance(
        instance_id,
        configuration_name=f"projects/{client.project}/instanceConfigs/{config}",
        display_name=display_name or instance_id
    )
    operation = instance.create()
    operation.result()
    print(f"✅ Instancia Spanner creada: {instance_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crear recursos en Google Cloud.")
    parser.add_argument("resource", choices=["bucket", "dataset", "spanner"], help="Recurso a crear")
    parser.add_argument("--name", required=True, help="Nombre del recurso (bucket, dataset o instancia)")
    parser.add_argument("--location", default="US", help="Ubicación (para bucket/dataset)")
    parser.add_argument("--config", default="regional-us-central1", help="Configuración de Spanner")
    parser.add_argument("--display_name", help="Nombre visible de la instancia Spanner")

    args = parser.parse_args()

    if args.resource == "bucket":
        create_bucket(args.name, args.location)
    elif args.resource == "dataset":
        create_bigquery_dataset(args.name, args.location)
    elif args.resource == "spanner":
        create_spanner_instance(args.name, args.config, args.display_name)
