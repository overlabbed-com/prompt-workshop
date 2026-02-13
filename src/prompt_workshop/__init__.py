"""
Prompt Workshop - Open-source prompt engineering toolkit with time series forecasting.

A self-improving prompt engineering system that measures, forecasts, and optimizes
prompt performance across different roles and use cases.
"""

__version__ = "0.1.0"

from prompt_workshop.core.profiles import ProfileRegistry
from prompt_workshop.core.pqi import PQICalculator
from prompt_workshop.core.heuristics import HeuristicsAnalyzer

__all__ = [
    "ProfileRegistry",
    "PQICalculator",
    "HeuristicsAnalyzer",
]
