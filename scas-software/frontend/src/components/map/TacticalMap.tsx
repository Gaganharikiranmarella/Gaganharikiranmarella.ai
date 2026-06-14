import Map, {
  Marker
} from "react-map-gl";

import "mapbox-gl/dist/mapbox-gl.css";

import DroneMarker from "./DroneMarker";
import SwarmMarker from "./SwarmMarker";

import { useDroneStore }
  from "../../store/droneStore";

import { useSwarmStore }
  from "../../store/swarmStore";

const TOKEN =
  import.meta.env.VITE_MAPBOX_TOKEN;

export default function TacticalMap() {

  const { drones } =
    useDroneStore();

  const { swarms } =
    useSwarmStore();

  return (
    <div
      className="
      h-[85vh]
      rounded-xl
      overflow-hidden
      border
      border-border
    "
    >
      <Map
        mapboxAccessToken={TOKEN}
        initialViewState={{
          latitude: 17.3850,
          longitude: 78.4867,
          zoom: 10
        }}
        mapStyle=
          "mapbox://styles/mapbox/dark-v11"
      >

        {drones.map((drone) => (

          <Marker
            key={drone.id}
            latitude={drone.latitude}
            longitude={drone.longitude}
          >
            <DroneMarker
              drone={drone}
            />
          </Marker>
        ))}

        {swarms.map((swarm) => (

          <Marker
            key={swarm.id}
            latitude={swarm.latitude}
            longitude={swarm.longitude}
          >
            <SwarmMarker
              swarm={swarm}
            />
          </Marker>
        ))}

      </Map>
    </div>
  );
}