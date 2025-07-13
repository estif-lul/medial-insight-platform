from dagster import Definitions, load_assets_from_modules, JobDefinition, ScheduleDefinition

from . import assets
from .jobs import medical_insight_job

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[medical_insight_job]
)
