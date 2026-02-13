"""PQI (Prompt Quality Index) calculator."""

from typing import Any

from prompt_workshop.core.profiles import ProfileRegistry, ProfileWeights


class PQICalculator:
    """Calculate PQI from prompt metrics."""

    def __init__(self, profile: str):
        """
        Initialize PQI calculator for a specific profile.

        Args:
            profile: Profile name (coding, support, analysis, creative, technical)
        """
        self.profile = profile
        self.registry = ProfileRegistry()
        self.profile_def = self.registry.get_profile(profile)
        self.weights = self.profile_def["weights"]

    def calculate(self, metrics: dict[str, Any]) -> tuple[float, dict]:
        """
        Calculate PQI from raw metrics.

        Args:
            metrics: Dictionary of metric values

        Returns:
            Tuple of (pqi_score, component_scores_dict)
        """
        components = {}

        for metric_name, weight in self.weights.items():
            raw_value = self._extract_metric(metrics, metric_name)
            normalized = self._normalize_metric(metric_name, raw_value)
            contribution = normalized * weight
            components[metric_name] = {
                "raw": raw_value,
                "normalized": normalized,
                "contribution": contribution,
            }

        pqi = sum(c["contribution"] for c in components.values())
        return pqi, components

    def _extract_metric(self, metrics: dict, metric_name: str) -> float:
        """Extract raw metric value from metrics dict."""
        # Handle compound metric names
        if metric_name == "announcement_absence":
            return 100 - metrics.get("announcement_rate", 0)
        if metric_name == "non_verbose":
            return 100 - metrics.get("verbose_no_tools_rate", 0)
        if metric_name == "no_menu":
            return 100 - metrics.get("menu_pattern_rate", 0)
        if metric_name == "no_errors":
            return 100 - metrics.get("error_rate", 0)
        if metric_name == "fast_response":
            # Lower response time = better, invert
            return 100 - min(100, metrics.get("response_time_ms", 0) / 50)
        if metric_name == "low_bias":
            return 100 - metrics.get("bias_score", 0)
        if metric_name == "length_appropriateness":
            return metrics.get("length_appropriateness", 50)  # Already 0-100

        return metrics.get(metric_name, 0)

    def _normalize_metric(self, metric_name: str, value: float) -> float:
        """
        Normalize metric to 0-100 scale.

        Higher values = better quality for all metrics.
        """
        # Binary metrics (already 0-1 when scaled)
        if metric_name in ["tool_call_success", "accuracy", "factual_accuracy"]:
            return value * 100 if value <= 1.0 else value

        # Percentage metrics (already 0-100)
        if metric_name.endswith("_rate"):
            return value

        # Inverted metrics (already inverted in extraction)
        if metric_name in [
            "announcement_absence",
            "non_verbose",
            "no_menu",
            "no_errors",
            "fast_response",
            "low_bias",
        ]:
            return value

        # Direct 0-100 scores
        if metric_name in [
            "empathy",
            "depth",
            "coherence",
            "originality",
            "emotional_resonance",
            "vocabulary_variety",
            "length_appropriateness",
            "completeness",
            "code_quality",
            "explanation_clarity",
        ]:
            return value

        # Count metrics - normalize based on expected range
        if metric_name == "example_count":
            return min(100, (value / 10) * 100)

        # Default: assume already 0-100
        return value
