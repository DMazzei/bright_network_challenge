from operator import itemgetter
from typing import List
from fuzzywuzzy import fuzz

from job_recommendation.candidate_data_parser import CandidateDataParser
from job_recommendation.models import Job, Member, JobPreferences, JobLocationPreferences


class MatchingAlgorithm:
    LOCATION_MATCHING_SCORE = 0.5
    MIN_SCORE_FOR_RECOMMENDATION = 0.6
    MIN_MATCHING_RATIO = 60
    
    def __init__(self, jobs: List):
        self.jobs = jobs

    def get_recommendations(self, candidate: Member, all_jobs: bool = False, **kwargs) -> List[Job]:
        """Lists recomended jobs for a given candidate, based on their preferences
        extracted from their bio.

        Args:
            candidate (Member): candidate requesting job recomendations
            all_jobs (bool, optional): flag that allows the algorithm to recomend 
            all jobs with matching score above 0 instead of the default threshold. Defaults to False.
        """
        job_preferences = self._get_candidate_preferences(candidate.bio)
        scored_matches = self._get_scored_matches(job_preferences=job_preferences)
        min_score = 0 if all_jobs else self.MIN_SCORE_FOR_RECOMMENDATION
        
        recommendations = self._filter_matching_result(
            scored_matches=scored_matches,
            min_score=min_score,
            **kwargs
        )
        return [recommendation['job'] for recommendation in recommendations]

    def _get_candidate_preferences(self, bio: str) -> JobPreferences:
        parser = CandidateDataParser(bio=bio)
        return parser.extract_job_preferences()
        
    def _get_scored_matches(self, job_preferences: JobPreferences) -> List:
        scored_jobs = []
        for job in self.jobs:
            score = self._get_job_matching_score(
                job=job,
                location_preferences=job_preferences.locations,
                job_title_preferences=job_preferences.titles,
            )
            scored_jobs.append({'job': job, 'score': score})
        
        return scored_jobs

    def _get_job_matching_score(self, 
            job: Job, 
            location_preferences: JobLocationPreferences, 
            job_title_preferences: List
        ) -> float:
        """Calculates a matching score for a given listed job to a candidate, 
        based on the candidate`s preferences
        """
        score = 0
        job_title = job.title.lower()
        job_location = job.location.lower()
        
        for title in job_title_preferences:
            if title == job_title:
                score = 1
                break    
            if (keyword_score := self._keyword_fuzzy_ratio(job_title, title)):
                score = max(score, keyword_score)
        
        if not location_preferences.positive:
            score += self.LOCATION_MATCHING_SCORE
        elif job_location in location_preferences.positive:
            score += self.LOCATION_MATCHING_SCORE
            
        if job_location in location_preferences.negative:
            score -= self.LOCATION_MATCHING_SCORE
        return score

    def _keyword_fuzzy_ratio(self, s1: str, s2: str) -> float:
        """Returns a simple ration from fuzzy matching two strings
        """
        if (ratio := fuzz.ratio(s1, s2)) > self.MIN_MATCHING_RATIO:
            return ratio / 100
        return 0
    
    
    def _filter_matching_result(
            self,
            scored_matches: List,
            min_score: float = 0.5,
            recomendation_limit: int = 10,
            **kwargs
    ) -> List:
        """Filters and sorts the matching result based on score to generate a recomendation list 

        Args:
            scored_matches: list of matching jobs alongside with matching score
            min_score: minimum acceptable matching score
            recomendation_limit: max number of job recomendations
        """
        result = sorted(scored_matches, key=itemgetter('score'), reverse=True)
        recommendations = filter(lambda x: x['score'] >= min_score, result)
        return list(recommendations)[:recomendation_limit]
