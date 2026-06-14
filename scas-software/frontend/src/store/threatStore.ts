import { create } from "zustand";

export interface Threat {

  id: string;

  cluster: string;

  score: number;

  eta: number;

  classification:
    | "LOW"
    | "MEDIUM"
    | "HIGH"
    | "CRITICAL";
}

interface ThreatStore {

  threats: Threat[];

  setThreats: (
    threats: Threat[]
  ) => void;

  addThreat: (
    threat: Threat
  ) => void;
}

export const useThreatStore =
  create<ThreatStore>((set) => ({

    threats: [],

    setThreats: (threats) =>
      set({ threats }),

    addThreat: (threat) =>
      set((state) => ({
        threats: [
          threat,
          ...state.threats
        ]
      }))
  }));