from pydantic import BaseModel, Field


class DatabaseStatus(BaseModel):
    connected: bool
    database_type: str
    matches_stored: int


class FixtureSyncResult(BaseModel):
    competition_code: str

    fixtures_received: int = Field(ge=0)
    fixtures_inserted: int = Field(ge=0)
    fixtures_updated: int = Field(ge=0)
    fixtures_unchanged: int = Field(ge=0)

    total_matches_stored: int = Field(ge=0)