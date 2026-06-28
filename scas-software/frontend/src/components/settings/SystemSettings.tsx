import { useState } from "react";

export default function SystemSettings() {
  const [apiUrl, setApiUrl] = useState("http://localhost:8000");
  const [wsUrl, setWsUrl] = useState("ws://localhost:8000/ws");
  const [threshold, setThreshold] = useState(70);

  return (
    <div className="bg-card border border-border p-5 rounded-xl text-gray-200">
      <h3 className="text-lg font-semibold text-white mb-4">System Configurations</h3>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">API Endpoint</label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            className="w-full bg-background border border-border rounded px-3 py-1.5 text-sm text-white focus:outline-none focus:border-sky-400 font-mono"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">WebSocket Endpoint</label>
          <input
            type="text"
            value={wsUrl}
            onChange={(e) => setWsUrl(e.target.value)}
            className="w-full bg-background border border-border rounded px-3 py-1.5 text-sm text-white focus:outline-none focus:border-sky-400 font-mono"
          />
        </div>

        <div>
          <div className="flex justify-between text-sm font-medium text-gray-400 mb-1">
            <span>Threat Detection Threshold</span>
            <span className="text-sky-400 font-mono">{threshold}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value={threshold}
            onChange={(e) => setThreshold(Number(e.target.value))}
            className="w-full accent-sky-400 cursor-pointer"
          />
        </div>
      </div>
    </div>
  );
}
