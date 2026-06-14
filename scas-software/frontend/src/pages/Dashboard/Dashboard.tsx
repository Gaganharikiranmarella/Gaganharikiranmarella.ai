import MetricsGrid from "../../components/dashboard/MetricsGrid";
import EventFeed from "../../components/dashboard/EventFeed";
import ThreatChart from "../../components/dashboard/ThreatChart";

export default function Dashboard() {
  return (
    <div
      className="
      flex-1
      overflow-auto
      p-6
      bg-background
    "
    >
      <MetricsGrid />

      <div
        className="
        grid
        grid-cols-3
        gap-5
        mt-5
      "
      >
        <div className="col-span-2">
          <ThreatChart />
        </div>

        <div>
          <EventFeed />
        </div>
      </div>
    </div>
  );
}