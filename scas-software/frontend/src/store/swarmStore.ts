import { create } from "zustand";

import { Swarm } from "../types/swarm";

import { sampleSwarms } from "../data/sampleSwarms";

interface SwarmStore {

  swarms: Swarm[];

  setSwarms: (
    swarms: Swarm[]
  ) => void;
}

export const useSwarmStore =
  create<SwarmStore>((set) => ({

    swarms: sampleSwarms,

    setSwarms: (swarms) =>
      set({ swarms })
  }));