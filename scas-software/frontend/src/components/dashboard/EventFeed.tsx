const events = [
  "UAV-017 DETECTED",
  "CLUSTER ALPHA FORMED",
  "THREAT LEVEL HIGH",
  "INTRUSION PREDICTED",
  "TRACKING ACTIVE"
];

export default function EventFeed() {
  return (
    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-5
      h-full
    "
    >
      <h3
        className="
        text-lg
        font-semibold
        mb-4
      "
      >
        Live Event Feed
      </h3>

      <div className="space-y-4">
        {events.map((event, index) => (
          <div
            key={index}
            className="
            border-b
            border-border
            pb-2
          "
          >
            <div
              className="
              text-xs
              text-gray-500
            "
            >
              22:41:{10 + index}
            </div>

            <div>{event}</div>
          </div>
        ))}
      </div>
    </div>
  );
}