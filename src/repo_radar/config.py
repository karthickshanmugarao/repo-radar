from pydantic import BaseModel
from typing import Dict, List


class AuditConfig(BaseModel):
    teams: Dict[str, List[str]]
    start_date: str
    end_date: str
    output_format: str = "json"
    output_path: str = "audit_output.json"
