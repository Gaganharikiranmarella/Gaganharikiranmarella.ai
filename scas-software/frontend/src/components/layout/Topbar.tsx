import { useState, useEffect } from "react";
import { Shield, Bell, Wifi } from "lucide-react";

export default function Topbar() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="h-16 border-b border-border bg-card/50 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-sky-500/10 rounded-lg border border-sky-500/20 text-sky-400">
          <Shield className="w-5 h-5 animate-pulse" />
        </div>
        <div>
          <h2 className="text-sm font-bold text-white tracking-wider uppercase font-mono">
            SCAS Command Center
          </h2>
          <p className="text-[10px] text-gray-400 font-mono">SWARM COGNITIVE ANALYSIS SYSTEM</p>
        </div>
      </div>

      <div className="flex items-center gap-6 text-sm font-mono">
        {/* System Status */}
        <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full text-emerald-400 text-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
          <span>SYS OPERATIONAL</span>
        </div>

        {/* Network status */}
        <div className="flex items-center gap-1 text-gray-400">
          <Wifi className="w-4 h-4 text-sky-400" />
          <span className="text-xs">SECURE NODE</span>
        </div>

        {/* Live Clock */}
        <div className="text-white font-bold tracking-widest bg-gray-800/40 border border-border px-3 py-1 rounded-lg">
          {time.toLocaleTimeString()}
        </div>

        {/* Alerts Button */}
        <button className="relative p-1.5 rounded-lg border border-border hover:bg-gray-800 text-gray-400 hover:text-white transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-red-500" />
        </button>
      </div>
    </div>
  );
}