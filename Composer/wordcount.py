import apache_beam as beam
import re
from apache_beam.options.pipeline_options import PipelineOptions


class CustomOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--input', type=str)
        parser.add_value_provider_argument('--output', type=str)


def run():
    # Configuración base
    options = PipelineOptions(
        runner="DataflowRunner",
        project="flopeza-demo-composer",
        region="us-central1",
        num_workers=1,
        max_num_workers=2,
        machine_type="e2-standard-2",
        experiments=["use_runner_v2"]
    )

    custom_options = options.view_as(CustomOptions)

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Leer archivo" >> beam.io.ReadFromText(custom_options.input)
            | "Separar palabras" >> beam.FlatMap(
                lambda line: re.findall(r'\b[a-zA-Z]+\b', line.lower())
            )
            | "Contar palabras" >> beam.combiners.Count.PerElement()
            | "Guardar resultados" >> beam.io.WriteToText("gs://flopeza-composer-demo/wordcount/test/result")
        )

    print("Pipeline ejecutado exitosamente.")


if __name__ == "__main__":
    run()