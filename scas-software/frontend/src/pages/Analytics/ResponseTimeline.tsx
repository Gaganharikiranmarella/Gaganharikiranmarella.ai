const timeline = [

  "UAV Detection",

  "Swarm Formation",

  "Threat Classification",

  "Trajectory Prediction",

  "Alert Generation"
];

export default function ResponseTimeline() {

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
        mb-4
      "
      >
        Response Timeline
      </h3>

      {

        timeline.map((step,index)=>(

          <div
            key={index}
            className="
            py-3
            border-b
            border-border
          "
          >

            T+{index*5}s

            {" — "}

            {step}

          </div>

        ))

      }

    </div>
  );
}