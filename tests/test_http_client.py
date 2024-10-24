import logging

from job_recommendation.http_client import Client


def test_get_jobs_success(requests_mock):
    mock_job = {"title": "Software Developer", "location": "London"}
    requests_mock.get(f"{Client.BASE_URL}jobs.json", json=[mock_job])

    result = Client.get_jobs()
    assert repr(result[0]) == "Software Developer (London)"
    assert result[0].title == "Software Developer"
    assert result[0].location == "London"


def test_get_jobs_error(requests_mock, caplog):
    requests_mock.get(f"{Client.BASE_URL}jobs.json", status_code=404)
    error_message = (
        "HTTP error occurred: 404 Client Error: None for url: https://bn-hiring-challenge.fly.dev/jobs.json\n"
    )
    with caplog.at_level(logging.ERROR):
        Client.get_jobs()
    assert error_message in caplog.text


def test_get_candidates_success(requests_mock):
    mock_member = {"name": "Joe", "bio": "I`m a designer from London, UK"}
    requests_mock.get(f"{Client.BASE_URL}members.json", json=[mock_member])

    result = Client.get_candidates()
    assert str(result[0]) == "Joe"
    assert result[0].name == "Joe"
    assert result[0].bio == "I`m a designer from London, UK"


def test_get_candidates_error(requests_mock, caplog):
    requests_mock.get(f"{Client.BASE_URL}members.json", status_code=404)
    error_message = (
        "HTTP error occurred: 404 Client Error: None for url: https://bn-hiring-challenge.fly.dev/members.json\n"
    )
    with caplog.at_level(logging.ERROR):
        Client.get_candidates()
    assert error_message in caplog.text
