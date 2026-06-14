export default function SystemHealth() {

  const systems = [

    {
      name:"YOLO Engine",
      status:"ONLINE"
    },

    {
      name:"DeepSORT",
      status:"ONLINE"
    },

    {
      name:"Threat Engine",
      status:"ONLINE"
    },

    {
      name:"Telemetry",
      status:"ONLINE"
    },

    {
      name:"WebSocket",
      status:"ONLINE"
    }
  ];

  return (

    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-5
    "
    >

      <h3
        className="
        text-lg
        mb-4
      "
      >
        System Health
      </h3>

      {

        systems.map(system=>(

          <div

            key={system.name}

            className="
            flex
            justify-between
            py-2
          "
          >

            <span>
              {system.name}
            </span>

            <span
              className="
              text-green-500
            "
            >
              {system.status}
            </span>

          </div>

        ))
      }

    </div>
  );
}