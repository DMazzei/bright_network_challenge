import pytest

from job_recommendation.matching_algorithm import MatchingAlgorithm
from job_recommendation.models import Job, Member


@pytest.fixture
def candidate():
    return Member(name="Marta", bio="I'm looking for an internship in London")


@pytest.fixture
def jobs():
    job_list = [
        {"title": "Marketing Internship", "location": "York"},
        {"title": "Data Scientist", "location": "London"},
        {"title": "Legal Internship", "location": "London"},
        {"title": "Project Manager", "location": "Manchester"},
    ]
    return [Job(**job) for job in job_list]


def test_recommendations_success(jobs, candidate):
    matching_tool = MatchingAlgorithm(jobs=jobs)
    result = matching_tool.get_recommendations(candidate=candidate)

    assert len(result) == 2
    assert result[0].title == "Legal Internship"
    assert result[0].location == "London"
    assert result[1].title == "Marketing Internship"
    assert result[1].location == "York"


def test_recommendations_all_jobs(jobs, candidate):
    matching_tool = MatchingAlgorithm(jobs=jobs)
    result = matching_tool.get_recommendations(candidate=candidate, all_jobs=True)

    assert len(result) == 4
    assert result[0].title == "Legal Internship"
    assert result[0].location == "London"
    assert result[3].title == "Project Manager"
    assert result[3].location == "Manchester"


def test_recommendations_no_available_jobs(candidate):
    matching_tool = MatchingAlgorithm(jobs=[])
    result = matching_tool.get_recommendations(candidate=candidate)

    assert len(result) == 0


def test_recommendations_no_bio(jobs):
    matching_tool = MatchingAlgorithm(jobs=jobs)
    candidate = Member(name="Marta", bio="")
    result = matching_tool.get_recommendations(candidate=candidate)

    assert len(result) == 0
