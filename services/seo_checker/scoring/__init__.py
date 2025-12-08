# services/seo_checker/scoring/__init__.py

from .recommendation import Issue, IssueSeverity, ScoreBreakdown

__all__ = [
    'Issue',
    'IssueSeverity',
    'ScoreBreakdown'
]