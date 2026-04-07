import apache_beam as beam
import re
from apache_beam.options.pipeline_options import PipelineOptions

def run():
    # Configuración del pipeline
    options = PipelineOptions(
        runner="DataflowRunner",  # Cambiar a DirectRunner para local
        project="flopeza-dataflow",
        region="us-central1",
        num_workers=1,
        max_num_workers=2,
        machine_type="e2-standard-2",
        experiments=["use_runner_v2"]
    )

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Leer archivo" >> beam.io.ReadFromText("gs://dataflow-samples/shakespeare/kinglear.txt")
            | "Separar palabras" >> beam.FlatMap(lambda line: re.findall(r'\b[a-zA-Z]+\b', line.lower()))
            #Limites de palabras, solo letras y evita duplicados por case sensitive
            | "Contar palabras" >> beam.combiners.Count.PerElement()
            | "Guardar resultados" >> beam.io.WriteToText("gs://gcs-bucket-flopeza-dataflow/outputClean/wordcount")
        )
    print("Pipeline ejecutado exitosamente.")

if __name__ == "__main__":
    run()