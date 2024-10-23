import pytest
import logging

from requests import HTTPError

from job_recommendation.http_client import Client
from job_recommendation.models import Job, Member

def test_get_jobs_success(requests_mock):
    mock_job = {'title': 'Software Developer', 'location': 'London'}
    requests_mock.get(f'{Client.BASE_URL}jobs.json', json = [mock_job])
    
    result = Client.get_jobs()
    assert repr(result[0]) == 'Software Developer (London)'
    assert result[0].title == 'Software Developer'
    assert result[0].location == 'London'
    
def test_get_jobs_error(requests_mock, caplog):
    requests_mock.get(f'{Client.BASE_URL}jobs.json', status_code=404)
    with caplog.at_level(logging.ERROR):
        Client.get_jobs()
    assert caplog.text == 'ERROR    HTTP Client:http_client.py:49 HTTP error occurred: 404 Client Error: None for url: https://bn-hiring-challenge.fly.dev/jobs.json\n'

def test_get_members_success(requests_mock):
    mock_member = {'name': 'Joe', 'bio': 'I`m a designer from London, UK'}
    requests_mock.get(f'{Client.BASE_URL}members.json', json = [mock_member])
    
    result = Client.get_members()
    assert str(result[0]) == 'Joe'
    assert result[0].name == 'Joe'
    assert result[0].bio == 'I`m a designer from London, UK'
    
def test_get_members_error(requests_mock, caplog):
    requests_mock.get(f'{Client.BASE_URL}members.json', status_code=404)
    with caplog.at_level(logging.ERROR):
        Client.get_members()
    assert caplog.text == 'ERROR    HTTP Client:http_client.py:49 HTTP error occurred: 404 Client Error: None for url: https://bn-hiring-challenge.fly.dev/members.json\n'
    