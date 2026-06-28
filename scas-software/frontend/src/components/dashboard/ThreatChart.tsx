import { useState, useEffect } from "react";
import {
  AreaChart,
  Area,
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";
import { Activity } from "lucide-react";

export default function ThreatChart() {
  const [data, setData] = useState([
    { time: "19:50:00", threat: 45 },
    { time: "19:51:00", threat: 52 },
    { time: "19:52:00", threat: 49 },
    { time: "19:53:00", threat: 62 },
    { time: "19:54:00", threat: 58 },
    { time: "19:55:00", threat: 74 },
    { time: "19:56:00", threat: 71 },
    { time: "19:57:00", threat: 85 },
    { time: "19:58:00", threat: 82 },
    { time: "19:59:00", threat: 91 },
  ]);

  // Simulate real-time threat data fluctuations
  useEffect(() => {
    const interval = setInterval(() => {
      setData((prevData) => {
        const now = new Date();
        const timeStr = now.toTimeString().split(" ")[0];
        const lastThreat = prevData[prevData.length - 1].threat;
        
        // Random walk with boundaries
        const fluctuation = (Math.random() - 0.5) * 12;
        let newThreat = Math.round(lastThreat + fluctuation);
        newThreat = Math.max(30, Math.min(98, newThreat)); // clamp between 30% and 98%

        const nextData = [...prevData.slice(1), { time: timeStr, threat: newThreat }];
        return nextData;
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 h-[360px] flex flex-col justify-between shadow-[0_8px_32px_rgba(0,0,0,0.4)]">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-red-500 animate-pulse" />
          <h3 className="text-sm font-bold font-mono tracking-wider text-white uppercase">
            Threat Level Evolution
          </h3>
        </div>
        <span className="text-[10px] bg-red-500/10 border border-red-500/20 text-red-400 font-mono px-2 py-0.5 rounded-full animate-pulse">
          LIVE FEED
        </span>
      </div>

      <div className="flex-1 min-h-0 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="threatGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#EF4444" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#243244" opacity={0.3} />
            <XAxis 
              dataKey="time" 
              stroke="#94A3B8" 
              fontSize={10} 
              fontFamily="monospace"
              tickLine={false}
            />
            <YAxis 
              stroke="#94A3B8" 
              fontSize={10} 
              fontFamily="monospace"
              tickLine={false}
              domain={[0, 100]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#121A22",
                borderColor: "#243244",
                borderRadius: "8px",
                color: "#F8FAFC",
                fontFamily: "monospace",
                fontSize: "12px",
                boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
              }}
              labelClassName="text-gray-400 font-bold"
            />
            <Area
              type="monotone"
              dataKey="threat"
              stroke="#EF4444"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#threatGrad)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}