class ThreatAssessor:

    @staticmethod
    def assess(
        drone
    ):

        score = 0

        if drone.altitude > 100:
            score += 25

        if drone.altitude > 200:
            score += 15

        if drone.velocity > 50:
            score += 25

        if drone.velocity > 100:
            score += 15

        if score >= 70:
            return "CRITICAL"

        if score >= 50:
            return "HIGH"

        if score >= 25:
            return "MEDIUM"

        return "LOW"