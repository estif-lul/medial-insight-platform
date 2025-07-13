from dagster import op

@op
def run_dbt_transformations():
    import subprocess
    subprocess.run(['cd', '..', '&&', 'cd', 'medical_insight_dbt', '&&', 'dbt', 'run'], check=True)
    return 'DBT run complete'