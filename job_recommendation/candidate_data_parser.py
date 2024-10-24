from typing import Dict, List, Any
import spacy
from spacy.matcher import Matcher

from job_recommendation.models import JobPreferences, JobLocationPreferences

class CandidateDataParser():
    POSITIVE_LOCATION_PATTERNS = [
        [{"LOWER": "from"}, {"ENT_TYPE": "GPE"}],
        [{"LOWER": "in"}, {"ENT_TYPE": "GPE"}],
        [{"LOWER": "relocate"}, {"LOWER": "to"}, {"ENT_TYPE": "GPE"}],
    ]
    NEGATIVE_LOCATION_PATTERNS = [
        [{"LOWER": "outside"}, {"ENT_TYPE": "GPE"}],
        [{"LOWER": "outside"}, {"LOWER": "of"}, {"ENT_TYPE": "GPE"}],
        [{"LOWER": "away"}, {"LOWER": "from"}, {"ENT_TYPE": "GPE"}],
    ]
    JOB_TITLE_PATTERNS = [
        [{"LOWER": "software"}, {"LOWER": {"IN": ["developer", "engineer"]}}],
        [{"LOWER": "data"}, {"LOWER": {"IN": ["scientist", "analyst"]}}],
        [{"LOWER": {"IN": ["ux", "graphic"]}}, {"LOWER": "designer"}],
        [{"POS": "NOUN"}, {"LOWER": "internship"}],
        [{"POS": "NOUN"}, {"LOWER": "manager"}],
        [{"LOWER": "marketing"}],
        [{"LOWER": "internship"}],
        [{"LOWER": "manager"}],
        [{"LOWER": "engineer"}],
        [{"LOWER": "developer"}],
        [{"LOWER": {"IN": ["design", "designer"]}}],
    ]
        
    def __init__(self, bio: str) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(bio)
        
    def extract_job_preferences(self) -> JobPreferences:
        locations = self.extract_job_locations()
        titles = self.extract_job_titles()
        
        return JobPreferences(locations=locations, titles=titles)
        
    def extract_job_locations(self) -> JobLocationPreferences:
        """Extracts job location preferences from text based on pattern matching
        The result is divided into 'positive' for locations where it was inferred 
        that the candidate wishes to work; And 'negative' for locations inferred
        as undesirable.
        """
        positive_location_matcher = self._set_matcher(
            key="LocationPositive", 
            patterns=self.POSITIVE_LOCATION_PATTERNS
        )
        negative_location_matcher = self._set_matcher(
            key="LocationNegative", 
            patterns=self.NEGATIVE_LOCATION_PATTERNS
        )
        positive_matches = positive_location_matcher(self.doc)
        negative_matches = negative_location_matcher(self.doc)

        positive_locations = self._get_original_token(matches=positive_matches)
        negative_locations = self._get_original_token(matches=negative_matches)
        return JobLocationPreferences(
            positive=positive_locations, 
            negative=negative_locations
        )
        
    def extract_job_titles(self) -> List:
        """Extracts job titles from text based on pattern matching
        The result is ordered to bring longer strings first as they are more accurate matches
        """
        job_title_matcher = self._set_matcher(key="JobTitle", patterns=self.JOB_TITLE_PATTERNS)
        title_matches = job_title_matcher(self.doc)
        unique_matches = self._get_original_span(matches=title_matches)
        
        return sorted(unique_matches, key=len, reverse=True)
        
    def _set_matcher(self, key: str, patterns: List[List[Dict[str, Any]]]) -> Matcher:
        matcher = Matcher(self.nlp.vocab)
        matcher.add(key, patterns)
        return matcher
    
    def _get_original_token(self, matches: List) -> List:
        result_list = set()
        for _, _, end in matches:
            result_list.add(self.doc[end - 1].text.lower())
            
        return list(result_list)
    
    def _get_original_span(self, matches: List) -> List:
        result_list = set()
        for _, start, end in matches:
            result_list.add(self.doc[start:end].text.lower())
            
        return list(result_list)
