class SwarmDetector:

    @staticmethod
    def detect(
        drones
    ):

        count = len(drones)

        if count >= 3:
            return True

        return False