import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const data = [

  { time:"10", score:20 },

  { time:"20", score:40 },

  { time:"30", score:62 },

  { time:"40", score:88 },

  { time:"50", score:94 }
];

export default function ThreatTrendChart() {

  return (

    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-5
      h-[350px]
    "
    >

      <h3
        className="
        mb-4
        font-semibold
      "
      >
        Threat Escalation Trend
      </h3>

      <ResponsiveContainer
        width="100%"
        height="90%"
      >

        <LineChart data={data}>

          <XAxis dataKey="time" />

          <YAxis />

          <Tooltip />

          <Line
            dataKey="score"
            stroke="#EF4444"
            strokeWidth={3}
          />

        </LineChart>

      </ResponsiveContainer>

    </div>
  );
}