import MissionLogFeed
from "../../components/console/MissionLogFeed";

import SystemHealth
from "../../components/console/SystemHealth";

import CommandConsole
from "../../components/console/CommandConsole";

import IntelTicker
from "../../components/console/IntelTicker";

export default function MissionLogs() {

  return (

    <div
      className="
      p-5
      bg-background
      h-full
    "
    >

      <IntelTicker />

      <div
        className="
        grid
        grid-cols-3
        gap-5
        mt-5
      "
      >

        <div>

          <MissionLogFeed />

        </div>

        <div>

          <SystemHealth />

        </div>

        <div>

          <CommandConsole />

        </div>

      </div>

    </div>
  );
}