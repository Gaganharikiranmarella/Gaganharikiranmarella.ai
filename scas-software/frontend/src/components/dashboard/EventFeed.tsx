import { useState, useEffect, useRef } from "react";
import { Terminal, ShieldAlert, AlertTriangle, Info } from "lucide-react";

interface LogEvent {
  timestamp: string;
  message: string;
  type: "INFO" | "WARN" | "CRITICAL";
  sector?: string;
}

export default function EventFeed() {
  const [events, setEvents] = useState<LogEvent[]>([
    { timestamp: "19:54:12", message: "SYSTEM BOOTSTRAP COMPLETE", type: "INFO" },
    { timestamp: "19:55:05", message: "SECURE CONSOLE CONNECTION ESTABLISHED", type: "INFO" },
    { timestamp: "19:56:30", message: "RADAR DISPATCH: 12 TARGET CORRELATIONS", type: "INFO" },
    { timestamp: "19:57:15", message: "SIGNAL NOISE DETECTED - SECTOR G-9", type: "WARN", sector: "G-9" },
    { timestamp: "19:58:22", message: "THREAT ASSESSMENT: UAV-017 CLASSIFIED HOSTILE", type: "CRITICAL" },
    { timestamp: "19:59:01", message: "CLUSTER SIGMA FORMATION PREDICTED", type: "WARN" }
  ]);

  const feedRef = useRef<HTMLDivElement>(null);

  // Simulation of incoming tactical logs
  useEffect(() => {
    const logPool: Omit<LogEvent, "timestamp">[] = [
      { message: "Automatic jamming sweep triggered in Sector A-3", type: "INFO" },
      { message: "Telemetry link lost with Recon Drone 4", type: "WARN" },
      { message: "Telemetry link re-established: Signal strength 94%", type: "INFO" },
      { message: "High-density drone cluster detected near perimeter", type: "CRITICAL" },
      { message: "Countermeasures deployed: Sector B-1 decoy active", type: "INFO" },
      { message: "UAV-022 altitude spike detected: 340m", type: "WARN" },
      { message: "Thermal signature match: Class-3 Quadcopter", type: "INFO" },
      { message: "CRITICAL INTRUSION: Airspace breach in Sector C-2", type: "CRITICAL" },
      { message: "Signal jamming active: Hostile drone speed decreasing", type: "INFO" }
    ];

    const interval = setInterval(() => {
      const randomLog = logPool[Math.floor(Math.random() * logPool.length)];
      const now = new Date();
      const timeStr = now.toTimeString().split(" ")[0];
      
      setEvents((prev) => [
        { ...randomLog, timestamp: timeStr },
        ...prev.slice(0, 15) // keep last 16 logs
      ]);
    }, 4500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 h-[360px] flex flex-col justify-between shadow-[0_8px_32px_rgba(0,0,0,0.4)]">
      <div className="flex justify-between items-center mb-4 pb-2 border-b border-[#243244]/50">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-sky-400" />
          <h3 className="text-sm font-bold font-mono tracking-wider text-white uppercase">
            Tactical Log Feed
          </h3>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
          <span className="text-[10px] font-mono text-gray-400">BUFFER ACTIVE</span>
        </div>
      </div>

      <div 
        ref={feedRef}
        className="flex-1 overflow-y-auto space-y-3 font-mono text-xs pr-1 scrollbar-thin"
      >
        {events.map((event, index) => {
          let badgeColor = "bg-sky-500/10 text-sky-400 border-sky-500/20";
          let icon = <Info className="w-3 h-3" />;
          if (event.type === "WARN") {
            badgeColor = "bg-amber-500/10 text-amber-400 border-amber-500/20";
            icon = <AlertTriangle className="w-3 h-3" />;
          } else if (event.type === "CRITICAL") {
            badgeColor = "bg-red-500/10 text-red-400 border-red-500/20";
            icon = <ShieldAlert className="w-3 h-3 animate-pulse" />;
          }

          return (
            <div 
              key={index}
              className="group flex flex-col gap-1 p-2.5 rounded-lg bg-[#0B0F14]/30 border border-[#243244]/30 hover:border-[#243244] hover:bg-[#0B0F14]/60 transition-all duration-200"
            >
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-1.5">
                  <span className={`flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-bold border ${badgeColor}`}>
                    {icon}
                    {event.type}
                  </span>
                  {event.sector && (
                    <span className="px-1.5 py-0.5 rounded text-[9px] font-bold border border-gray-700 bg-gray-800/30 text-gray-400">
                      SEC: {event.sector}
                    </span>
                  )}
                </div>
                <span className="text-[10px] text-gray-500">{event.timestamp}</span>
              </div>
              <p className="text-gray-300 group-hover:text-white transition-colors mt-1 leading-relaxed">
                {event.message}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}