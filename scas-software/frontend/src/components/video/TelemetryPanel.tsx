export default function TelemetryPanel() {

  const cards = [

    {
      title: "FPS",
      value: "31"
    },

    {
      title: "Latency",
      value: "42 ms"
    },

    {
      title: "Detected Objects",
      value: "17"
    },

    {
      title: "Tracked UAVs",
      value: "9"
    },

    {
      title: "Active Swarms",
      value: "2"
    },

    {
      title: "Threat Level",
      value: "HIGH"
    }
  ];

  return (

    <div
      className="
      flex
      flex-col
      gap-3
    "
    >

      {cards.map(card => (

        <div
          key={card.title}
          className="
          bg-card
          border
          border-border
          rounded-xl
          p-4
        "
        >

          <p className="text-gray-400">

            {card.title}

          </p>

          <h3
            className="
            text-2xl
            font-bold
            mt-2
          "
          >
            {card.value}
          </h3>

        </div>

      ))}

    </div>
  );
}