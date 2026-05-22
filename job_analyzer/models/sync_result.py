from dataclasses import dataclass


@dataclass
class SyncResult:
    new_jobs: int
    updated_jobs: int
    inactive_jobs: int