import { useState } from "react";
import MetricsGrid from "../../components/dashboard/MetricsGrid";
import EventFeed from "../../components/dashboard/EventFeed";
import ThreatChart from "../../components/dashboard/ThreatChart";
import CommandConsole from "../../components/console/CommandConsole";
import { Shield, Zap, Radio, ShieldAlert } from "lucide-react";
import { useAlertStore } from "../../store/alertStore";

export default function Dashboard() {
  const addAlert = useAlertStore((state) => state.addAlert);
  const [activeCountermeasure, setActiveCountermeasure] = useState<string | null>(null);

  const triggerCountermeasure = (name: string, severity: "HIGH" | "CRITICAL" | "MEDIUM") => {
    setActiveCountermeasure(name);
    
    // Add to alert store
    addAlert({
      id: Math.random().toString(),
      message: `TACTICAL COUNTERMEASURE ACTIVATED: ${name}`,
      severity: severity,
      timestamp: new Date().toLocaleTimeString()
    });

    setTimeout(() => {
      setActiveCountermeasure(null);
    }, 3000);
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 bg-background space-y-6">
      {/* Title section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-wider font-mono text-white">
            TACTICAL MONITORING DASHBOARD
          </h1>
          <p className="text-xs text-gray-400 mt-1 font-mono">
            COGNITIVE THREAT MITIGATION & AIRSPACE DENSITY ANALYSIS
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-gray-400">THREAT STATUS:</span>
          <span className="px-3 py-1 bg-red-500/10 border border-red-500/30 text-red-500 text-xs font-mono font-bold rounded-lg animate-pulse">
            HIGH RISK
          </span>
        </div>
      </div>

      {/* Stats Cards */}
      <MetricsGrid />

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (Charts and Console) */}
        <div className="lg:col-span-2 space-y-6">
          <ThreatChart />
          <CommandConsole />
        </div>

        {/* Right Column (Logs and Quick Actions) */}
        <div className="space-y-6">
          <EventFeed />

          {/* Countermeasures Quick Action Panel */}
          <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 shadow-[0_8px_32px_rgba(0,0,0,0.4)]">
            <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[#243244]/50">
              <Zap className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold font-mono tracking-wider text-white uppercase">
                Active Countermeasures
              </h3>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {[
                { name: "SIGNAL JAMMER", icon: <Radio className="w-3 h-3" />, severity: "HIGH" as const, color: "hover:border-red-500 hover:bg-red-500/10 text-red-400 border-red-500/30" },
                { name: "DECOY FLARES", icon: <ShieldAlert className="w-3 h-3" />, severity: "CRITICAL" as const, color: "hover:border-amber-500 hover:bg-amber-500/10 text-amber-400 border-amber-500/30" },
                { name: "GPS SPOOFING", icon: <Shield className="w-3 h-3" />, severity: "MEDIUM" as const, color: "hover:border-sky-500 hover:bg-sky-500/10 text-sky-400 border-sky-500/30" },
                { name: "EMP WAVE", icon: <Zap className="w-3 h-3" />, severity: "CRITICAL" as const, color: "hover:border-emerald-500 hover:bg-emerald-500/10 text-emerald-400 border-emerald-500/30" }
              ].map((item) => (
                <button
                  key={item.name}
                  onClick={() => triggerCountermeasure(item.name, item.severity)}
                  disabled={activeCountermeasure !== null}
                  className={`flex items-center justify-center gap-1.5 py-3 px-2.5 rounded-lg border text-[10px] font-mono font-bold transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${item.color}`}
                >
                  {item.icon}
                  {item.name}
                </button>
              ))}
            </div>

            {/* Action Feedback */}
            {activeCountermeasure && (
              <div className="mt-4 p-2.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono text-[10px] text-center animate-pulse">
                DEPLOYING {activeCountermeasure}... TRANSMITTING INTERFERENCE
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}