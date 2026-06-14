import MissionLogFeed from "../../components/console/MissionLogFeed";
import SystemHealth from "../../components/console/SystemHealth";
import CommandConsole from "../../components/console/CommandConsole";
import IntelTicker from "../../components/console/IntelTicker";
export default function CommandConsole() {

  return (

    <div
      className="
      bg-black
      text-green-400
      rounded-xl
      p-4
      font-mono
      h-[500px]
      overflow-auto
    "
    >

      <div>

        SCAS COMMAND SHELL

      </div>

      <div className="mt-4">

        >

        TRACKING UAV-017

      </div>

      <div>

        >

        CLUSTER ALPHA

      </div>

      <div>

        >

        THREAT SCORE 0.91

      </div>

      <div>

        >

        STATUS HOSTILE

      </div>

      <div>

        >

        AWAITING COMMAND

      </div>

    </div>
  );
}