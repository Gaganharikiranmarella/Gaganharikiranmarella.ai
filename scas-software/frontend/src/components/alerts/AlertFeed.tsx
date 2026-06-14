import {
  useAlertStore
} from "../../store/alertStore";

import AlertCard
from "./AlertCard";

export default function AlertFeed() {

  const alerts =
    useAlertStore(
      state => state.alerts
    );

  return (

    <div
      className="
      flex
      flex-col
      gap-3
    "
    >

      {alerts.map(alert => (

        <AlertCard

          key={alert.id}

          message={
            alert.message
          }

          severity={
            alert.severity
          }

          timestamp={
            alert.timestamp
          }

        />

      ))}

    </div>
  );
}