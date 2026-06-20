class ThreatAssessor:

    @staticmethod
    def assess(
        drone
    ):

        score = 0

        if drone.altitude > 100:
            score += 30

        if drone.velocity > 50:
            score += 30

        if score >= 60:
            return "HIGH"

        if score >= 30:
            return "MEDIUM"

        return "LOW"