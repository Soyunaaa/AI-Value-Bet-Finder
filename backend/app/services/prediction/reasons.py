from app.models.fixture_analysis import TeamFormSummary
from app.models.team_strength import TeamStrengthRating


def build_reasons(
    *,
    home_form: TeamFormSummary,
    away_form: TeamFormSummary,
    home_strength: TeamStrengthRating,
    away_strength: TeamStrengthRating,
    home_expected_goals: float,
    away_expected_goals: float,
) -> list[str]:
    stronger_team = (
        home_strength
        if home_strength.overall_rating
        >= away_strength.overall_rating
        else away_strength
    )

    return [
        (
            f"{home_form.team_name} have an attack rating of "
            f"{home_strength.attack_rating:.1f}/100."
        ),
        (
            f"{away_form.team_name} have a defensive rating of "
            f"{away_strength.defence_rating:.1f}/100."
        ),
        (
            f"{stronger_team.team_name} have the stronger recent "
            f"overall rating at "
            f"{stronger_team.overall_rating:.1f}/100."
        ),
        (
            "The model projects a combined expected-goals total of "
            f"{home_expected_goals + away_expected_goals:.2f}."
        ),
        (
            f"{home_form.team_name} recent points per game: "
            f"{home_form.points_per_game:.2f}."
        ),
        (
            f"{away_form.team_name} recent points per game: "
            f"{away_form.points_per_game:.2f}."
        ),
    ]