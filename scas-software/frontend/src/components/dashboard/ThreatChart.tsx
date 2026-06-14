import {
  LineChart,
  Line,
  ResponsiveContainer,
  XAxis,
  YAxis
} from "recharts";

const data = [
  { t: "1", threat: 20 },
  { t: "2", threat: 30 },
  { t: "3", threat: 50 },
  { t: "4", threat: 75 },
  { t: "5", threat: 92 }
];

export default function ThreatChart() {
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
      <h3 className="text-lg mb-4">
        Threat Evolution
      </h3>

      <ResponsiveContainer
        width="100%"
        height="90%"
      >
        <LineChart data={data}>
          <XAxis dataKey="t" />
          <YAxis />

          <Line
            type="monotone"
            dataKey="threat"
            stroke="#EF4444"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}