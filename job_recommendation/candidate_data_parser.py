from typing import Dict, List, Any
import spacy
from spacy.matcher import Matcher

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
        
    def extract_job_location(self):
        positive_location_matcher = self._set_matcher("LocationPositive", self.POSITIVE_LOCATION_PATTERNS)
        negative_location_matcher = self._set_matcher("LocationNegative", self.NEGATIVE_LOCATION_PATTERNS)
        positive_matches = positive_location_matcher(self.doc)
        negative_matches = negative_location_matcher(self.doc)

        positive_locations = self._get_original_token(positive_matches)
        negative_locations = self._get_original_token(negative_matches)
        return {
            "positive": positive_locations,
            "negative": negative_locations
        }
        
    def extract_job_title(self):
        job_title_matcher = self._set_matcher("JobTitle", self.JOB_TITLE_PATTERNS)
        title_matches = job_title_matcher(self.doc)
        sorted_matches = sorted(title_matches, key=lambda x: x[2] - x[1], reverse=True)
        
        return self._get_original_span(sorted_matches)
        
    def _set_matcher(self, key: str, patterns: List[List[Dict[str, Any]]]):
        matcher = Matcher(self.nlp.vocab)
        matcher.add(key, patterns)
        return matcher
    
    def _get_original_token(self, matches: List):
        result_list = []
        for _, _, end in matches:
            result_list.append(self.doc[end - 1].text.lower())
            
        return result_list
    
    def _get_original_span(self, matches: List):
        result_list = []
        for _, start, end in matches:
            result_list.append(self.doc[start:end].text.lower())
            
        return result_list
