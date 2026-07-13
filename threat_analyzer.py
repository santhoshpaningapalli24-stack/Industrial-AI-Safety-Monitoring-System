"""
Threat Analyzer
Calculates overall danger level
"""


class ThreatAnalyzer:

    def __init__(self, settings):

        self.settings = settings

    def evaluate(
        self,
        fire_results,
        smoke_results,
        scene_info
    ):

        fire_count = len(fire_results)

        smoke_count = len(smoke_results)

        # ============================================
        # THREAT SCORE
        # ============================================

        score = 0.0

        score += fire_count * 0.6

        score += smoke_count * 0.3

        # Clamp
        score = min(score, 1.0)

        # ============================================
        # LEVELS
        # ============================================

        if score >= 0.8:

            level = "CRITICAL"

        elif score >= 0.5:

            level = "HIGH"

        elif score >= 0.2:

            level = "MEDIUM"

        elif score > 0:

            level = "LOW"

        else:

            level = "NONE"

        return {

            "level": level,

            "score": score

        }