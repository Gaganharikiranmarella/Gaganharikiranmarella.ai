const logs = [

"TRACKING HOSTILE UAV",

"SWARM FORMATION DETECTED",

"THREAT SCORE UPDATED",

"PREDICTIVE TRAJECTORY GENERATED",

"AIRSPACE INTRUSION ALERT"
];

export default function IntelFeed() {

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

      <h3
        className="
        text-lg
        mb-4
      "
      >

        Intelligence Feed

      </h3>

      {

        logs.map((log,index) => (

          <div
            key={index}
            className="
            py-2
            border-b
            border-border
          "
          >

            {log}

          </div>

        ))
      }

    </div>
  );
}