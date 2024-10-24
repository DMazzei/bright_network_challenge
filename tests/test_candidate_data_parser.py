import pytest

from job_recommendation.candidate_data_parser import CandidateDataParser
from job_recommendation.models import JobLocationPreferences, JobPreferences


def test_extract_job_preferences():
    bio = "I'm a designer from London, UK"

    parser = CandidateDataParser(bio=bio)
    result = parser.extract_job_preferences()

    assert isinstance(result, JobPreferences)
    assert result.locations.positive == ["london"]
    assert result.locations.negative == []
    assert result.titles == ["designer"]


def test_extract_job_locations_excluding_geo():
    bio = "I'm looking for a job in marketing outside of London"

    parser = CandidateDataParser(bio=bio)
    result = parser.extract_job_locations()

    assert isinstance(result, JobLocationPreferences)
    assert result.positive == []
    assert result.negative == ["london"]


def test_extract_job_locations_including_geo():
    bio = "I'm a designer from London, UK"

    parser = CandidateDataParser(bio=bio)
    result = parser.extract_job_locations()

    assert isinstance(result, JobLocationPreferences)
    assert result.positive == ["london"]
    assert result.negative == []


def test_extract_job_locations_empty():
    bio = "I'm looking for a design job"

    parser = CandidateDataParser(bio=bio)
    result = parser.extract_job_locations()

    assert isinstance(result, JobLocationPreferences)
    assert result.positive == []
    assert result.negative == []


@pytest.mark.parametrize(
    "bio, expected_result",
    [
        (
            "I'm a software developer currently in Edinburgh but looking to relocate to London",
            ["software developer", "developer"],
        ),
        ("I'm an engineering manager in Edinburgh", ["engineering manager", "manager"]),
        (
            "I'm looking for a marketing internship in Portsmouth",
            ["marketing internship", "internship", "marketing"],
        ),
    ],
)
def test_extract_job_titles_composed_title(bio, expected_result):
    parser = CandidateDataParser(bio=bio)
    result = parser.extract_job_titles()

    assert result == expected_result


def test_extract_job_titles_empty():
    bio = "I'm looking for any job"
    parser = CandidateDataParser(bio=bio)
    result = parser.extract_job_titles()

    assert result == []
