import ThreatCard from "./ThreatCard";
import { ShieldAlert, Radar, Cpu, Bell } from "lucide-react";
import { useDroneStore } from "../../store/droneStore";
import { useSwarmStore } from "../../store/swarmStore";
import { useAlertStore } from "../../store/alertStore";
import { useThreatStore } from "../../store/threatStore";

export default function MetricsGrid() {
  const { drones } = useDroneStore();
  const { swarms } = useSwarmStore();
  const { alerts } = useAlertStore();
  const { threats } = useThreatStore();

  // Determine threat level string
  const maxThreatScore = threats.length > 0 
    ? Math.max(...threats.map(t => t.score)) 
    : 0.85;

  let threatLevel = "LOW";
  let threatColor = "#10B981";
  if (maxThreatScore > 0.8) {
    threatLevel = "CRITICAL";
    threatColor = "#EF4444";
  } else if (maxThreatScore > 0.5) {
    threatLevel = "HIGH";
    threatColor = "#F59E0B";
  } else if (maxThreatScore > 0.25) {
    threatLevel = "MEDIUM";
    threatColor = "#38BDF8";
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
      <ThreatCard
        title="System Threat Level"
        value={threatLevel}
        color={threatColor}
        icon={<ShieldAlert className="w-5 h-5" />}
        trend={maxThreatScore > 0.8 ? "+4.2%" : "-1.8%"}
        trendType={maxThreatScore > 0.8 ? "up" : "down"}
      />

      <ThreatCard
        title="Tracked UAVs"
        value={drones.length}
        color="#38BDF8"
        icon={<Radar className="w-5 h-5" />}
        trend="+2 new"
        trendType="up"
      />

      <ThreatCard
        title="Active Swarms"
        value={swarms.length}
        color="#F59E0B"
        icon={<Cpu className="w-5 h-5" />}
        trend="Stable"
        trendType="neutral"
      />

      <ThreatCard
        title="Total Alerts"
        value={alerts.length > 0 ? alerts.length : 8}
        color="#F59E0B"
        icon={<Bell className="w-5 h-5" />}
        trend={`+${alerts.filter(a => a.severity === "CRITICAL").length} critical`}
        trendType="up"
      />
    </div>
  );
}