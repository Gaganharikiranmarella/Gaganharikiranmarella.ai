import { Swarm } from "../../types/swarm";

interface Props {
  swarm: Swarm;
}

export default function SwarmMarker({
  swarm
}: Props) {

  return (
    <div
      className="
      flex
      items-center
      justify-center
      rounded-full
      border
      border-red-500
      bg-red-500/20
    "
      style={{
        width: 60,
        height: 60
      }}
    >
      {swarm.droneCount}
    </div>
  );
}
