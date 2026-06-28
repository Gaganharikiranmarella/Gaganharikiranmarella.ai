import { useState, useRef, useEffect, FormEvent } from "react";
import { Terminal, CornerDownLeft } from "lucide-react";

interface ConsoleLine {
  text: string;
  type: "input" | "output" | "error" | "success";
}

export default function CommandConsole() {
  const [input, setInput] = useState("");
  const [history, setHistory] = useState<ConsoleLine[]>([
    { text: "SCAS COGNITIVE COMMAND SHELL v1.4.2", type: "success" },
    { text: "type 'help' to view available tactical commands.", type: "output" },
    { text: "", type: "output" }
  ]);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  const handleCommand = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const cmd = input.trim().toLowerCase();
    const newHistory = [...history, { text: `> ${input}`, type: "input" as const }];
    
    setInput("");

    // Simulate terminal response
    setTimeout(() => {
      if (cmd === "help") {
        setHistory([
          ...newHistory,
          { text: "Available SCAS Commands:", type: "success" },
          { text: "  scan          - Run tactical airspace radar sweep", type: "output" },
          { text: "  jam [uav_id]  - Activate frequency jammer on target", type: "output" },
          { text: "  swarm-info    - Query telemetry on active threat swarms", type: "output" },
          { text: "  clear         - Clear terminal display buffer", type: "output" }
        ]);
      } else if (cmd === "scan") {
        setHistory([
          ...newHistory,
          { text: "Initiating radar sweep...", type: "output" },
          { text: "Scan complete. 31 targets correlated. 4 swarms tracking.", type: "success" },
          { text: "Cluster Alpha (Hostile) - bearing 142° - ETA 42s", type: "error" }
        ]);
      } else if (cmd.startsWith("jam")) {
        const target = cmd.split(" ")[1] || "all";
        setHistory([
          ...newHistory,
          { text: `Targeting jammer array on [${target.toUpperCase()}]...`, type: "output" },
          { text: "Frequency locked. Electromagnetic interference active.", type: "success" },
          { text: `[${target.toUpperCase()}] telemetry signal degraded by 85%.`, type: "success" }
        ]);
      } else if (cmd === "swarm-info") {
        setHistory([
          ...newHistory,
          { text: "Querying cognitive swarm database...", type: "output" },
          { text: "Active Swarms: 4", type: "output" },
          { text: " - CLUSTER ALPHA (Hostile): 12 drones, Speed 41km/h", type: "error" },
          { text: " - CLUSTER BETA (Hostile): 8 drones, Speed 30km/h", type: "error" },
          { text: " - CLUSTER GAMMA (Unknown): 5 drones, Speed 15km/h", type: "output" }
        ]);
      } else if (cmd === "clear") {
        setHistory([]);
      } else {
        setHistory([
          ...newHistory,
          { text: `Unknown command: '${cmd}'. Type 'help' for options.`, type: "error" }
        ]);
      }
    }, 400);
  };

  return (
    <div className="bg-black/95 border border-[#243244] rounded-xl p-5 h-[320px] flex flex-col justify-between shadow-[0_8px_32px_rgba(0,0,0,0.6)] font-mono text-xs text-green-400 relative overflow-hidden">
      {/* Scanline overlay */}
      <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[size:100%_4px,3px_100%] opacity-30" />

      {/* Header */}
      <div className="flex justify-between items-center mb-3 pb-2 border-b border-green-950">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-green-500 animate-pulse" />
          <span className="font-bold tracking-wider text-green-500">TACTICAL SHELL</span>
        </div>
        <span className="text-[10px] text-green-700 font-bold">NODE: SEC-SHELL-01</span>
      </div>

      {/* Output screen */}
      <div className="flex-1 overflow-y-auto space-y-1 mb-3 scrollbar-thin pr-1">
        {history.map((line, index) => {
          let colorClass = "text-green-400";
          if (line.type === "input") colorClass = "text-sky-400 font-semibold";
          else if (line.type === "error") colorClass = "text-red-500 font-semibold";
          else if (line.type === "success") colorClass = "text-emerald-400 font-semibold";

          return (
            <div key={index} className={`${colorClass} whitespace-pre-wrap leading-relaxed`}>
              {line.text}
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleCommand} className="flex items-center gap-2 border-t border-green-950 pt-2.5">
        <span className="text-green-500 font-bold font-mono">&gt;</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter tactical command..."
          className="flex-1 bg-transparent border-none text-green-400 focus:outline-none placeholder-green-850 font-mono text-xs caret-green-500"
          autoFocus
        />
        <button 
          type="submit" 
          className="p-1 rounded hover:bg-green-950/40 text-green-500 transition-colors"
        >
          <CornerDownLeft className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}