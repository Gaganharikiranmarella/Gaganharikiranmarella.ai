import { create } from "zustand";

export interface Alert {

  id: string;

  message: string;

  severity:
    | "LOW"
    | "MEDIUM"
    | "HIGH"
    | "CRITICAL";

  timestamp: string;
}

interface AlertStore {

  alerts: Alert[];

  addAlert: (
    alert: Alert
  ) => void;
}

export const useAlertStore =
  create<AlertStore>((set) => ({

    alerts: [],

    addAlert: (alert) =>
      set((state) => ({
        alerts: [
          alert,
          ...state.alerts
        ]
      }))
  }));