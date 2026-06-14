import ThreatCard from "./ThreatCard";

export default function MetricsGrid() {
  return (
    <div
      className="
      grid
      grid-cols-4
      gap-4
    "
    >
      <ThreatCard
        title="Threat Level"
        value="CRITICAL"
        color="#EF4444"
      />

      <ThreatCard
        title="Tracked UAVs"
        value="31"
        color="#38BDF8"
      />

      <ThreatCard
        title="Active Swarms"
        value="4"
        color="#F59E0B"
      />

      <ThreatCard
        title="Alerts"
        value="7"
        color="#10B981"
      />
    </div>
  );
}