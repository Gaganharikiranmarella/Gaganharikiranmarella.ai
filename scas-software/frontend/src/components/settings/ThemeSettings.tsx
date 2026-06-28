import { useState } from "react";

export default function ThemeSettings() {
  const [theme, setTheme] = useState("dark");
  const [contrast, setContrast] = useState("normal");
  const [mapStyle, setMapStyle] = useState("dark");

  return (
    <div className="bg-card border border-border p-5 rounded-xl text-gray-200">
      <h3 className="text-lg font-semibold text-white mb-4">Display & Theme</h3>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">Color Theme</label>
          <div className="flex gap-2">
            {["dark", "light", "cyberpunk"].map((t) => (
              <button
                key={t}
                onClick={() => setTheme(t)}
                className={`px-3 py-1.5 rounded text-xs font-medium capitalize border transition-colors ${
                  theme === t 
                    ? "bg-sky-500/10 border-sky-400 text-sky-400" 
                    : "border-border hover:bg-gray-800"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">Contrast</label>
          <div className="flex gap-2">
            {["normal", "high"].map((c) => (
              <button
                key={c}
                onClick={() => setContrast(c)}
                className={`px-3 py-1.5 rounded text-xs font-medium capitalize border transition-colors ${
                  contrast === c 
                    ? "bg-sky-500/10 border-sky-400 text-sky-400" 
                    : "border-border hover:bg-gray-800"
                }`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">Map Layer Style</label>
          <div className="flex gap-2">
            {["dark", "light", "satellite", "streets"].map((s) => (
              <button
                key={s}
                onClick={() => setMapStyle(s)}
                className={`px-3 py-1.5 rounded text-xs font-medium capitalize border transition-colors ${
                  mapStyle === s 
                    ? "bg-sky-500/10 border-sky-400 text-sky-400" 
                    : "border-border hover:bg-gray-800"
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
