import AnalyticsOverview
  from "../../components/analytics/AnalyticsOverview";

import ThreatTrendChart
  from "../../components/analytics/ThreatTrendChart";

import SwarmDensityChart
  from "../../components/analytics/SwarmDensityChart";

import ResponseTimeline
  from "../../components/analytics/ResponseTimeline";

import PerformanceMetrics
  from "../../components/analytics/PerformanceMetrics";

export default function Analytics() {

  return (

    <div
      className="
      p-5
      bg-background
      min-h-screen
    "
    >

      <AnalyticsOverview />

      <div
        className="
        grid
        grid-cols-2
        gap-5
        mt-5
      "
      >

        <ThreatTrendChart />

        <SwarmDensityChart />

      </div>

      <div
        className="
        grid
        grid-cols-2
        gap-5
        mt-5
      "
      >

        <ResponseTimeline />

        <PerformanceMetrics />

      </div>

    </div>
  );
}