"""
SEO Checker Models
"""

from .seo_schemas import (
    IssueSeverity,
    IssueSchema,
    ScoreBreakdownSchema,
    BonusSchema,
    StatsSchema,
    SEOCheckerRequest,
    SEOCheckerResponse
)

from .fix_schemas import (
    FixTask,
    FixTarget,
    FixScope,
    FixTaskSeverity,
    PatchOperation,
    AutoFixRequest,
    AutoFixResponse
)

__all__ = [
    'IssueSeverity',
    'IssueSchema',
    'ScoreBreakdownSchema', 
    'BonusSchema',
    'StatsSchema',
    'SEOCheckerRequest',
    'SEOCheckerResponse'
]

__all__ = [
    'FixTask', 
    'FixTarget', 
    'FixScope', 
    'FixTaskSeverity', 
    'PatchOperation', 
    'AutoFixRequest', 
    'AutoFixResponse'
]