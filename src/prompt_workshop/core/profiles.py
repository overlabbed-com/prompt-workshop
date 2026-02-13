"""Profile registry for different prompt types."""

from typing import TypedDict


class ProfileWeights(TypedDict):
    """Weight distribution for PQI components."""
    pass


class Profile(TypedDict):
    """A prompt profile with its metrics and weights."""
    name: str
    description: str
    weights: ProfileWeights
    metrics: list[str]


PROFILES: dict[str, Profile] = {
    "coding": {
        "name": "coding",
        "description": "Agentic coding, tool-using assistants",
        "weights": {
            "tool_call_success": 0.30,
            "announcement_absence": 0.25,
            "non_verbose": 0.20,
            "no_menu": 0.15,
            "no_errors": 0.10,
        },
        "metrics": [
            "tool_call_success",
            "announcement_rate",
            "avg_token_count",
            "verbose_no_tools_rate",
            "menu_pattern_rate",
            "error_rate",
        ],
    },
    "support": {
        "name": "support",
        "description": "Customer support, help desk",
        "weights": {
            "accuracy": 0.35,
            "empathy": 0.20,
            "fast_response": 0.15,
            "resolution": 0.20,
            "no_escalation": 0.10,
        },
        "metrics": [
            "accuracy",
            "empathy_score",
            "response_time_ms",
            "resolution_rate",
            "escalation_rate",
        ],
    },
    "analysis": {
        "name": "analysis",
        "description": "Research, data analysis, reporting",
        "weights": {
            "factual_accuracy": 0.30,
            "citation_rate": 0.20,
            "low_bias": 0.15,
            "depth": 0.20,
            "conciseness": 0.15,
        },
        "metrics": [
            "factual_accuracy",
            "citation_rate",
            "bias_score",
            "depth_score",
            "conciseness",
        ],
    },
    "creative": {
        "name": "creative",
        "description": "Content creation, storytelling",
        "weights": {
            "originality": 0.25,
            "coherence": 0.20,
            "emotional_resonance": 0.20,
            "vocabulary_variety": 0.15,
            "length_appropriateness": 0.20,
        },
        "metrics": [
            "originality_score",
            "coherence",
            "emotional_resonance",
            "vocabulary_variety",
            "length_appropriateness",
        ],
    },
    "technical": {
        "name": "technical",
        "description": "Documentation, tutorials, explainers",
        "weights": {
            "accuracy": 0.30,
            "completeness": 0.20,
            "code_quality": 0.15,
            "explanation_clarity": 0.20,
            "example_count": 0.15,
        },
        "metrics": [
            "accuracy",
            "completeness",
            "code_quality",
            "explanation_clarity",
            "example_count",
        ],
    },
}


class ProfileRegistry:
    """Registry for prompt profiles."""

    def get_profile(self, name: str) -> Profile:
        """Get a profile by name."""
        if name not in PROFILES:
            raise ValueError(f"Unknown profile: {name}. Available profiles: {list(PROFILES.keys())}")
        return PROFILES[name]

    def list_profiles(self) -> list[str]:
        """List all available profile names."""
        return list(PROFILES.keys())

    def validate_metrics(self, profile: str, metrics: dict) -> bool:
        """Validate that metrics contain all required keys for a profile."""
        profile_def = self.get_profile(profile)
        required = set(profile_def["metrics"])
        provided = set(metrics.keys())
        return required.issubset(provided)
