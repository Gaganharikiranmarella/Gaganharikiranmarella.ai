import { ReactNode } from "react";

interface Props {
  title: string;
  value: string | number;
  color?: string;
  icon?: ReactNode;
  trend?: string;
  trendType?: "up" | "down" | "neutral";
}

export default function ThreatCard({ title, value, color, icon, trend, trendType = "neutral" }: Props) {
  const glowColor = color ? `${color}20` : "rgba(56, 189, 248, 0.1)";

  return (
    <div 
      className="relative overflow-hidden bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 p-5 rounded-xl transition-all duration-300 hover:-translate-y-1 hover:border-sky-500/30 group"
      style={{
        boxShadow: `0 8px 32px 0 rgba(0, 0, 0, 0.37), 0 0 12px 0 ${glowColor}`
      }}
    >
      {/* Decorative top glow bar */}
      <div 
        className="absolute top-0 left-0 right-0 h-[2px] opacity-70 group-hover:opacity-100 transition-opacity"
        style={{ backgroundColor: color || "#38BDF8" }}
      />

      <div className="flex justify-between items-start">
        <div>
          <span className="text-xs font-mono tracking-widest text-gray-400 uppercase">
            {title}
          </span>
          <h3 
            className="text-2xl font-bold font-mono mt-2 tracking-tight group-hover:scale-102 transition-transform origin-left"
            style={{ color: color || "#F8FAFC" }}
          >
            {value}
          </h3>
        </div>
        <div 
          className="p-2 rounded-lg border border-[#243244] bg-[#0B0F14]/40 transition-colors group-hover:border-sky-500/20"
          style={{ color: color || "#38BDF8" }}
        >
          {icon}
        </div>
      </div>

      {trend && (
        <div className="mt-4 flex items-center gap-1.5 text-xs font-mono">
          <span 
            className={`font-semibold ${
              trendType === "up" 
                ? "text-red-400" 
                : trendType === "down" 
                ? "text-emerald-400" 
                : "text-gray-400"
            }`}
          >
            {trend}
          </span>
          <span className="text-gray-500">vs last check</span>
        </div>
      )}
    </div>
  );
}
