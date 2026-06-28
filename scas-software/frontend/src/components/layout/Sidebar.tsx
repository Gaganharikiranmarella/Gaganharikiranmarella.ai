import { Link, useLocation } from "react-router-dom";
import { 
  LayoutDashboard, 
  Map, 
  Video, 
  ShieldAlert, 
  BarChart2, 
  Settings,
  BookOpen
} from "lucide-react";

const items = [
  {
    label: "Dashboard",
    route: "/",
    icon: LayoutDashboard
  },
  {
    label: "System Idea",
    route: "/overview",
    icon: BookOpen
  },
  {
    label: "Airspace",
    route: "/airspace",
    icon: Map
  },
  {
    label: "Video Intel",
    route: "/video-intel",
    icon: Video
  },
  {
    label: "Threat Intel",
    route: "/threat-intel",
    icon: ShieldAlert
  },
  {
    label: "Analytics",
    route: "/analytics",
    icon: BarChart2
  },
  {
    label: "Settings",
    route: "/settings",
    icon: Settings
  }
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <div className="w-64 bg-card border-r border-border flex flex-col h-full text-gray-300">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <span className="text-xl font-bold text-white tracking-wider font-mono">SCAS SYSTEM</span>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {items.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.route;
          return (
            <Link
              key={item.route}
              to={item.route}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                isActive 
                  ? "bg-sky-500/10 text-sky-400 border-l-2 border-sky-400" 
                  : "hover:bg-gray-800 hover:text-white"
              }`}
            >
              <Icon className="w-5 h-5" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}