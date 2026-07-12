from dataclasses import dataclass


@dataclass(frozen=True)
class LeagueCalibration:
    competition_code: str
    goal_environment: float
    home_advantage_multiplier: float
    elo_home_advantage: float


DEFAULT_CALIBRATION = LeagueCalibration(
    competition_code="DEFAULT",
    goal_environment=1.00,
    home_advantage_multiplier=1.08,
    elo_home_advantage=65.0,
)


LEAGUE_CALIBRATIONS: dict[str, LeagueCalibration] = {
    "PL": LeagueCalibration(
        competition_code="PL",
        goal_environment=1.02,
        home_advantage_multiplier=1.07,
        elo_home_advantage=60.0,
    ),
    "PD": LeagueCalibration(
        competition_code="PD",
        goal_environment=0.98,
        home_advantage_multiplier=1.08,
        elo_home_advantage=65.0,
    ),
    "BL1": LeagueCalibration(
        competition_code="BL1",
        goal_environment=1.07,
        home_advantage_multiplier=1.06,
        elo_home_advantage=58.0,
    ),
    "SA": LeagueCalibration(
        competition_code="SA",
        goal_environment=0.96,
        home_advantage_multiplier=1.07,
        elo_home_advantage=62.0,
    ),
    "FL1": LeagueCalibration(
        competition_code="FL1",
        goal_environment=0.97,
        home_advantage_multiplier=1.08,
        elo_home_advantage=65.0,
    ),
    "CL": LeagueCalibration(
        competition_code="CL",
        goal_environment=1.01,
        home_advantage_multiplier=1.05,
        elo_home_advantage=50.0,
    ),
}


def get_league_calibration(
    competition_code: str | None,
) -> LeagueCalibration:
    if not competition_code:
        return DEFAULT_CALIBRATION

    return LEAGUE_CALIBRATIONS.get(
        competition_code.upper(),
        DEFAULT_CALIBRATION,
    )