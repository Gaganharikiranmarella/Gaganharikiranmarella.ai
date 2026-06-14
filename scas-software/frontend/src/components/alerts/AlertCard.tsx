import AlertBadge
from "./AlertBadge";

interface Props {

  message: string;

  severity: string;

  timestamp: string;
}

export default function AlertCard({

  message,

  severity,

  timestamp

}: Props) {

  return (

    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-4
    "
    >

      <div
        className="
        flex
        justify-between
      "
      >

        <AlertBadge
          severity={severity}
        />

        <span
          className="
          text-gray-400
        "
        >
          {timestamp}
        </span>

      </div>

      <div
        className="
        mt-3
      "
      >
        {message}
      </div>

    </div>
  );
}