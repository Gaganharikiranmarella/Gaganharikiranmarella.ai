const metrics = [

  {
    label:"Detection Accuracy",
    value:"96.8%"
  },

  {
    label:"Tracking Accuracy",
    value:"94.1%"
  },

  {
    label:"Threat Precision",
    value:"92.7%"
  },

  {
    label:"Response Time",
    value:"1.8s"
  }
];

export default function PerformanceMetrics() {

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
        AI Performance Metrics
      </h3>

      {

        metrics.map(metric=>(

          <div

            key={metric.label}

            className="
            flex
            justify-between
            py-3
          "
          >

            <span>

              {metric.label}

            </span>

            <span
              className="
              font-semibold
              text-info
            "
            >

              {metric.value}

            </span>

          </div>

        ))

      }

    </div>
  );
}