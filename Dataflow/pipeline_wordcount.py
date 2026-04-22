from datetime import datetime
import apache_beam as beam
import re
from apache_beam.options.pipeline_options import PipelineOptions

def run():
    # Configuración del pipeline
    options = PipelineOptions(
        runner="DataflowRunner",  # Cambiar a DirectRunner para local
        project="project-520e2962-bfa4-4d55-832",
        region="europe-west1",
        num_workers=1,
        max_num_workers=2,
        machine_type="e2-standard-2",
        experiments=["use_runner_v2"]
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_path = f"gs://create-bucket-example/outputClean/wordcount/{timestamp}/result"

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Leer archivo" >> beam.io.ReadFromText("gs://dataflow-samples/shakespeare/kinglear.txt")
            | "Separar palabras" >> beam.FlatMap(lambda line: re.findall(r'\b[a-zA-Z]+\b', line.lower()))
            #Limites de palabras, solo letras y evita duplicados por case sensitive
            | "Contar palabras" >> beam.combiners.Count.PerElement()
            | "Guardar resultados" >> beam.io.WriteToText(output_path)
        )
    print(f"\nPipeline ejecutado exitosamente.Output en: {output_path}")

if __name__ == "__main__":
    run()