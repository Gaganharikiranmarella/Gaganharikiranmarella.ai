import AnalyticsOverview from "./AnalyticsOverview";
import ThreatTrendChart from "./ThreatTrendChart";
import SwarmDensityChart from "./SwarmDensityChart";
import ResponseTimeline from "./ResponseTimeline";
import PerformanceMetrics from "./PerformanceMetrics";

export default function Analytics() {
  return (
    <div className="p-5 bg-background min-h-screen">
      <AnalyticsOverview />

      <div className="grid grid-cols-2 gap-5 mt-5">
        <ThreatTrendChart />
        <SwarmDensityChart />
      </div>

      <div className="grid grid-cols-2 gap-5 mt-5">
        <ResponseTimeline />
        <PerformanceMetrics />
      </div>
    </div>
  );
}