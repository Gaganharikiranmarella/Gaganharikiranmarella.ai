interface Props {

  timestamp: string;

  level:
    | "INFO"
    | "WARNING"
    | "CRITICAL";

  message: string;
}

export default function EventCard({

  timestamp,

  level,

  message

}: Props) {

  const color =
    level === "CRITICAL"
      ? "#EF4444"
      : level === "WARNING"
      ? "#F59E0B"
      : "#38BDF8";

  return (

    <div
      className="
      border-l-4
      p-3
      bg-card
      rounded-r-lg
    "
      style={{
        borderColor: color
      }}
    >

      <div
        className="
        flex
        justify-between
      "
      >

        <span
          style={{
            color
          }}
        >
          {level}
        </span>

        <span
          className="
          text-gray-400
          text-sm
        "
        >
          {timestamp}
        </span>

      </div>

      <p className="mt-2">

        {message}

      </p>

    </div>
  );
}