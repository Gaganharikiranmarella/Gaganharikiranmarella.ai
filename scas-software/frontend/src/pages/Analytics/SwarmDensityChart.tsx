import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const data = [

  {
    cluster:"Alpha",
    density:14
  },

  {
    cluster:"Bravo",
    density:9
  },

  {
    cluster:"Charlie",
    density:22
  }
];

export default function SwarmDensityChart() {

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
      "
      >
        Swarm Density
      </h3>

      <ResponsiveContainer
        width="100%"
        height="90%"
      >

        <BarChart data={data}>

          <XAxis dataKey="cluster" />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="density"
            fill="#38BDF8"
          />

        </BarChart>

      </ResponsiveContainer>

    </div>
  );
}