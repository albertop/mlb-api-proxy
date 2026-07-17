"""Guards for the stat translation dictionaries (correctness + consistency)."""

import pytest

from stats_translations import (
    STAT_TRANSLATIONS,
    abbrev_description_spanish,
    metric_abbreviation,
    validate_translations,
)


def test_abbrev_and_spanish_dicts_are_consistent():
    """Every abbreviation has Spanish; no orphan Spanish keys (typos)."""
    assert validate_translations() is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("homeRuns", "HR"),
        ("baseOnBalls", "BB"),
        ("walks", "BB"),
        ("strikeOuts", "K"),
        ("balks", "BK"),  # not WP
        ("wildPitches", "WP"),
        ("earnedRunAverage", "ERA"),
        ("putOuts", "PO"),  # was wrongly "Outs"
        ("runsBattedIn", "RBI"),
        ("battingAverage", "AVG"),
    ],
)
def test_known_field_abbreviations(field, expected):
    assert metric_abbreviation(field) == expected


def test_putouts_and_outs_no_longer_collide():
    """putOuts -> PO, outs -> Outs: distinct stats, distinct abbreviations."""
    assert STAT_TRANSLATIONS["putOuts"] == "PO"
    assert STAT_TRANSLATIONS["outs"] == "Outs"


def test_generic_structural_keys_are_not_translated():
    """Bare section keys must pass through untouched (no accidental renames)."""
    for key in ("batting", "fielding", "baseRunning", "streak", "positional", "replacement"):
        assert key not in STAT_TRANSLATIONS
        assert metric_abbreviation(key) == key  # returns input unchanged


@pytest.mark.parametrize(
    ("abbrev", "expected_present"),
    [
        ("HR", "Jonrones"),
        ("AB", "Turnos al Bate"),
        ("ER", "Carreras Limpias"),
        ("RBI", "Carreras Impulsadas"),
        ("WP", "Lanzamiento Descontrolado"),
        ("PO", "Outs Registrados"),
    ],
)
def test_basic_spanish_descriptions_present(abbrev, expected_present):
    assert abbrev_description_spanish(abbrev) == expected_present
