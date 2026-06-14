export interface Drone {

  id: string;

  latitude: number;

  longitude: number;

  altitude: number;

  velocity: number;

  threat: number;

  status:
    | "friendly"
    | "unknown"
    | "hostile";
}