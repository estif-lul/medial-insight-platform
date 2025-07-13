from dagster import job
from medical_insight_pipeline.ops.scrape import scrape_telegram_data
from medical_insight_pipeline.ops.load import load_raw_to_postgres
from medical_insight_pipeline.ops.transform import run_dbt_transformations
from medical_insight_pipeline.ops.enrich import run_yolo_enrichement

@job
def medical_insight_job():
    data = scrape_telegram_data()
    loaded = load_raw_to_postgres(data)
    run_dbt_transformations()
    run_yolo_enrichement()

# # Expose at module level
# medical_insight_job = medical_insight_job