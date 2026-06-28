import { X } from "lucide-react";
import { Drone } from "../../types/drone";

interface Props {
  open: boolean;
  onClose: () => void;
  drone: Drone | null;
}

export default function DroneDetailsDrawer({ open, onClose, drone }: Props) {
  if (!open || !drone) return null;

  return (
    <div className="fixed top-0 right-0 h-full w-[450px] bg-card border-l border-border z-50 p-5 text-gray-200">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold text-white">UAV Intelligence</h2>
        <button onClick={onClose} className="hover:text-white transition-colors">
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="mt-5 space-y-3">
        <div className="flex justify-between border-b border-border pb-2">
          <span className="text-gray-400">ID</span>
          <span className="font-mono font-bold text-white">{drone.id}</span>
        </div>
        <div className="flex justify-between border-b border-border pb-2">
          <span className="text-gray-400">Threat Level</span>
          <span className={`font-bold ${
            drone.status === "hostile" ? "text-red-500" : drone.status === "unknown" ? "text-amber-500" : "text-emerald-500"
          }`}>{drone.status.toUpperCase()} ({Math.round(drone.threat * 100)}%)</span>
        </div>
        <div className="flex justify-between border-b border-border pb-2">
          <span className="text-gray-400">Altitude</span>
          <span className="font-mono">{drone.altitude}m</span>
        </div>
        <div className="flex justify-between border-b border-border pb-2">
          <span className="text-gray-400">Velocity</span>
          <span className="font-mono">{drone.velocity}km/h</span>
        </div>
        <div className="flex justify-between border-b border-border pb-2">
          <span className="text-gray-400">Coordinates</span>
          <span className="font-mono">{drone.latitude.toFixed(5)}, {drone.longitude.toFixed(5)}</span>
        </div>
      </div>
    </div>
  );
}