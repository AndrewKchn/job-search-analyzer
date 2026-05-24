from loguru import logger

from job_analyzer.bootstrap import create_services

sync_service, _ = create_services()

logger.info("Starting job sync...")
result = sync_service.sync_jobs_from_all_pages()

logger.info(
    "Job sync finished | new={} updated={} inactive={}",
    result.new_jobs,
    result.updated_jobs,
    result.inactive_jobs
)