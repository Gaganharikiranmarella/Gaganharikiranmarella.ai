import { useEffect } from "react";

import { createSocket }
from "../services/websocket/socket";

import {
  useThreatStore
} from "../store/threatStore";

import {
  useAlertStore
} from "../store/alertStore";

export function useWebSocket() {

  const addThreat =
    useThreatStore(
      state => state.addThreat
    );

  const addAlert =
    useAlertStore(
      state => state.addAlert
    );

  useEffect(() => {

    const socket =
      createSocket();

    socket.onmessage =
      (event) => {

        const data =
          JSON.parse(
            event.data
          );

        if (
          data.type === "threat"
        ) {

          addThreat(
            data.payload
          );
        }

        if (
          data.type === "alert"
        ) {

          addAlert(
            data.payload
          );
        }
      };

  }, []);
}