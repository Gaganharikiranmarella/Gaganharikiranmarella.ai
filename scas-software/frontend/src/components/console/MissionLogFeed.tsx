import EventCard from "./EventCard";

const logs = [

  {
    timestamp:"22:41:03",
    level:"INFO",
    message:
      "UAV-012 DETECTED"
  },

  {
    timestamp:"22:41:07",
    level:"WARNING",
    message:
      "CLUSTER ALPHA FORMED"
  },

  {
    timestamp:"22:41:15",
    level:"CRITICAL",
    message:
      "HOSTILE TRAJECTORY DETECTED"
  },

  {
    timestamp:"22:41:22",
    level:"CRITICAL",
    message:
      "AIRSPACE INTRUSION PREDICTED"
  }
];

export default function MissionLogFeed() {

  return (

    <div
      className="
      flex
      flex-col
      gap-3
    "
    >

      {logs.map((log,index)=>(

        <EventCard

          key={index}

          timestamp={
            log.timestamp
          }

          level={
            log.level as any
          }

          message={
            log.message
          }

        />

      ))}

    </div>
  );
}