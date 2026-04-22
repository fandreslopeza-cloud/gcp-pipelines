# Portafolio de Ingeniería de Datos en GCP

Colección de proyectos prácticos sobre Google Cloud Platform, cubriendo los servicios principales en flujos de trabajo de ingeniería de datos modernos: procesamiento batch con Dataflow, orquestación con Cloud Composer, consultas analíticas con BigQuery, y aprovisionamiento de infraestructura con Cloud Storage y Spanner.

---

## Proyectos

### 1. Pipeline Word Count con Apache Beam — Cloud Dataflow
**`Dataflow/pipeline_wordcount.py`**

Pipeline batch construido con Apache Beam que lee *King Lear* de Shakespeare desde Cloud Storage, tokeniza y normaliza el texto, cuenta frecuencias de palabras y escribe los resultados de vuelta a GCS con rutas de salida marcadas por timestamp.

- Ejecuta en `DataflowRunner` con escalado configurable de workers (`e2-standard-2`, 1–2 workers)
- Usa Runner v2 para mayor rendimiento
- Salida particionada por timestamp de ejecución para trazabilidad

**Stack:** Apache Beam · Cloud Dataflow · Cloud Storage · Python

<details>
<summary>Ver output de ejemplo</summary>

Muestra de las palabras más frecuentes en *King Lear* (output real del pipeline, archivo completo en [`Dataflow/OutputClean.txt`](Dataflow/OutputClean.txt)):

```
('and', 738)
('to', 582)
('that', 363)
('king', 311)
('not', 282)
('his', 210)
('him', 198)
('gloucester', 179)
('for', 156)
('no', 154)
('will', 130)
('are', 128)
('fool', 120)
('sir', 115)
('our', 115)
('all', 109)
```

</details>

---

### 2. Orquestación de Template Dataflow — Cloud Composer
**`Composer/wordcount_dag_new.py` · `Composer/create_dataflow_template.sh`**

DAG de Airflow desplegado en Cloud Composer que dispara un template de Dataflow pre-compilado con una frecuencia horaria. Demuestra cómo desacoplar el empaquetado del pipeline (template) de su ejecución (orquestación).

- Template compilado y almacenado en GCS mediante script shell
- DAG usa `DataflowTemplatedJobStartOperator` para una separación limpia de responsabilidades
- Ruta de salida incluye la macro `{{ ts_nodash }}` de Airflow para ejecuciones idempotentes

**Stack:** Cloud Composer · Apache Airflow · Cloud Dataflow · Cloud Storage · Python

---

### 3. Análisis de E-commerce — BigQuery Dataset Público
**`bigquery/public_dataset_demo.py`**

Script Python parametrizable que consulta el dataset `bigquery-public-data.thelook_ecommerce` para obtener los productos más vendidos por cantidad o revenue. Diseñado como herramienta CLI reutilizable.

- Join entre `order_items` y `products`, filtrando pedidos completados
- Usa consultas parametrizadas (`QueryJobConfig`) para prevenir SQL injection
- Flags CLI: `--limit` y `--order {quantity|revenue}`
- Devuelve resultados como DataFrame de Pandas

**Stack:** BigQuery · Python · Pandas

<details>
<summary>Ver output de ejemplo</summary>

**Top 20 por revenue** (`--order revenue`):

```
       id                                               name  quantity  revenue
0   24201         Mens Nike AirJordan Varsity Hoodie Jacket         4  3612.00
1   20171         Robert Graham Men's Minstrel Dinner Jacket         5  2990.00
2    8429             The North Face Women's S-XL Oso Jacket         3  2709.00
3   17094       The North Face Apex Bionic Soft Shell Jacket         3  2709.00
4    3810                 Parker Women's V-Neck Beaded Dress         7  2618.00
5   23803              Canada Goose Men's The Chateau Jacket         3  2445.00
6   23811                     Arc'teryx Men's Beta AR Jacket         5  2375.00
7   24179                    Arc'teryx Men's Diplomat Jacket         5  2250.00
8    8777        Bergama Natural Raccoon Hooded Stroller Muu         3  2249.97
9   24195       Marc New York Andrew Marc Men's Nucky Jacket         5  2145.00
```

**Top 20 por cantidad vendida** (`--order quantity`):

```
       id                                               name  quantity  revenue
0    5251                  Everyday Favorite Pants / Regular         8   632.00
1    2166   Tri-Mountain Womens 100% polyester mesh fleece          8   553.60
2   27368      Tommy Hilfiger Solid Black & Red Pajama Pants         8   320.00
3   25523          Calvin Klein Men's Prostretch Boxer Brief         8   192.00
4   24473                      Original Penguin Men's Stripe         8   120.00
5    3810                 Parker Women's V-Neck Beaded Dress         7  2618.00
6   11718         Airblaster Expedition Weight Ninja Suit W's         7  1119.65
7   19964       Kenneth Cole Reaction Mens Grey Stripe Suit         7   699.93
8   10333                       Hanro Women's Taitu Babydoll         7   686.00
9   15660          Under Armour Igniter Pro Sport Sunglasses         7   664.93
```

</details>

---

### 4. Modelo de Datos Desnormalizado — BigQuery Dataset Propio
**`bigquery-model/`**

Ejemplo end-to-end de creación de un dataset en BigQuery y consulta sobre una vista desnormalizada para agregar el gasto por cliente.

- `create_dataset_script.py`: aprovisionamiento programático del dataset vía cliente de BigQuery
- `create_dataset.sql`: DDL de la vista desnormalizada
- `query_script.py`: consulta de agregación — total de pedidos y gasto por cliente, ordenado por revenue

**Stack:** BigQuery · SQL · Python

<details>
<summary>Ver output de ejemplo</summary>

```
            name  total_pedidos  total_gastado
0  Javier Valdes              2    1226.25
1  Agustin Tapia              1     300.00
2  Arturo Coello              2      55.00
```

</details>

---

### 5. CLI de Aprovisionamiento de Recursos GCP
**`cloud-storage/create_storage.py`**

Script CLI de entrada única para aprovisionar tres tipos de recursos GCP sin salir de la terminal.

```bash
python create_storage.py bucket  --name mi-bucket   --location EU
python create_storage.py dataset --name mi_dataset  --location US
python create_storage.py spanner --name mi-instancia --config regional-us-central1
```

- Cubre Cloud Storage, BigQuery y Cloud Spanner en una única interfaz unificada
- Localización y configuración de instancia Spanner configurables por argumento

**Stack:** Cloud Storage · BigQuery · Cloud Spanner · Python

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                Cloud Composer (Airflow)                  │
│          DAG horario disparando templates               │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Cloud Dataflow (Apache Beam)                │
│       Leer GCS → Transformar → Escribir GCS (batch)     │
└──────────────────────────┬──────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│   Cloud Storage     │   │         BigQuery             │
│  Datos crudos y     │   │  Analítica y modelado        │
│  resultados         │   │  de datos                    │
└─────────────────────┘   └─────────────────────────────┘
```

---

## Stack Tecnológico

| Servicio | Uso |
|---|---|
| Cloud Dataflow | Procesamiento batch gestionado (Apache Beam) |
| Cloud Composer | Orquestación de pipelines (Apache Airflow) |
| BigQuery | Consultas analíticas y modelado de datos |
| Cloud Storage | Data lake / staging / almacenamiento de templates |
| Cloud Spanner | Demo de aprovisionamiento (base de datos distribuida globalmente) |
| Python 3 | Lenguaje principal en todos los módulos |

---

## Prerrequisitos

- Google Cloud SDK (`gcloud`) configurado con un proyecto activo
- Python 3.8+
- Cuenta de servicio con roles: `Dataflow Admin`, `BigQuery Data Editor`, `Storage Admin`

```bash
pip install apache-beam[gcp] google-cloud-bigquery google-cloud-storage google-cloud-spanner pandas
```

---

## Sobre el autor

**Felipe López** — Ingeniero de Datos con experiencia en pipelines ETL y modelado relacional de datos, actualmente profundizando en ingeniería de datos cloud-native sobre GCP.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Felipe%20López-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/fandreslopez/)
