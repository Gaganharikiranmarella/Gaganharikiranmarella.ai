import { Drone } from "../../types/drone";

interface Props {
  drone: Drone;
}

export default function DroneMarker({
  drone
}: Props) {

  const color =
    drone.status === "hostile"
      ? "#EF4444"
      : drone.status === "unknown"
      ? "#F59E0B"
      : "#10B981";

  return (
    <div
      style={{
        width: 18,
        height: 18,
        borderRadius: "50%",
        background: color,
        border: "2px solid white"
      }}
    />
  );
}
