import requests
import logging

from pydantic import ValidationError
from typing import List, Any
from job_recommendation.models import Job, Member

logger = logging.getLogger("HTTP Client")


class Client:
    BASE_URL = "https://bn-hiring-challenge.fly.dev/"

    @classmethod
    def get_jobs(cls) -> List[Job] | None:
        try:
            jobs_response = cls._get("jobs.json")
            return [Job(**job) for job in jobs_response]
        except ValidationError as err:
            logger.error(f"Pydantic validation error: {err}")
            return None

    @classmethod
    def get_candidates(cls) -> List[Member] | None:
        try:
            members_response = cls._get("members.json")
            return [Member(**member) for member in members_response]
        except ValidationError as err:
            logger.error(f"Pydantic validation error: {err}")
            return None
    
    @classmethod
    def _get(cls, endpoint: str) -> Any:
        return cls._fetch_json_data(cls.BASE_URL + endpoint)
    
    @classmethod
    def _fetch_json_data(cls, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"Failed to fetch data.  Status Code: {response.status_code}")
                return dict()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return dict()
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
            return dict()
        except ValueError as json_err:
            logger.error(f"JSON decoding error: {json_err}")
            return dict()
