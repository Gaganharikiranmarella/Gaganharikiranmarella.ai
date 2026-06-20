class SwarmDetector:

    @staticmethod
    def detect(
        drones
    ):

        if len(drones) < 3:
            return False

        first = drones[0]

        nearby_count = 0

        for drone in drones:

            lat_diff = abs(
                drone.latitude -
                first.latitude
            )

            lon_diff = abs(
                drone.longitude -
                first.longitude
            )

            if (
                lat_diff < 0.01 and
                lon_diff < 0.01
            ):
                nearby_count += 1

        return nearby_count >= 3