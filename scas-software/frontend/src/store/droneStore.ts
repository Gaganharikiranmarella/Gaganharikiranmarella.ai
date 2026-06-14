import { create } from "zustand";

import { Drone } from "../types/drone";

import { sampleDrones } from "../data/sampleDrones";

interface DroneStore {

  drones: Drone[];

  setDrones: (
    drones: Drone[]
  ) => void;
}

export const useDroneStore =
  create<DroneStore>((set) => ({

    drones: sampleDrones,

    setDrones: (drones) =>
      set({ drones })
  }));