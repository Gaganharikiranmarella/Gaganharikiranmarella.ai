import { Drone } from "../types/drone";

export const sampleDrones: Drone[] = [

  {
    id: "UAV-001",
    latitude: 17.3850,
    longitude: 78.4867,
    altitude: 120,
    velocity: 42,
    threat: 0.93,
    status: "hostile"
  },

  {
    id: "UAV-002",
    latitude: 17.3920,
    longitude: 78.4810,
    altitude: 95,
    velocity: 38,
    threat: 0.72,
    status: "unknown"
  }
];