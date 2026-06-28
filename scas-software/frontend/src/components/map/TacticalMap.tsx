import { useState, useEffect, FormEvent } from "react";
import { Globe, Compass, RefreshCw, Layers, ShieldAlert, Radio, Search, ArrowUp, ArrowDown, ArrowLeft, ArrowRight } from "lucide-react";

export default function TacticalMap() {
  const [rotation, setRotation] = useState(0);
  const [activeLayer, setActiveLayer] = useState<"satellite" | "terrain">("satellite");
  const [isLoading, setIsLoading] = useState(false);
  const [coords, setCoords] = useState({ lat: 17.3850, lng: 78.4867 });
  const [gpsStatus, setGpsStatus] = useState("SEARCHING");
  const [searchQuery, setSearchQuery] = useState("");

  // Get machine's current location on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCoords({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
          setGpsStatus("LOCK_OK");
        },
        (error) => {
          console.warn("Geolocation access denied, using fallback coordinates.", error);
          setGpsStatus("FALLBACK");
        },
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    } else {
      setGpsStatus("UNSUPPORTED");
    }
  }, []);

  // Rotate the global radar ring
  useEffect(() => {
    const interval = setInterval(() => {
      setRotation((prev) => (prev + 0.5) % 360);
    }, 30);
    return () => clearInterval(interval);
  }, []);

  // Geocode location search using OpenStreetMap Nominatim API (Free, no keys needed)
  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsLoading(true);
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}`
      );
      const data = await response.json();
      if (data && data.length > 0) {
        const first = data[0];
        setCoords({
          lat: parseFloat(first.lat),
          lng: parseFloat(first.lon),
        });
        setGpsStatus("MANUAL_SEARCH");
      } else {
        alert("Location not found. Please try another search term.");
      }
    } catch (err) {
      console.error("Error geocoding location:", err);
      alert("Error connecting to geocoding server.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = () => {
    setIsLoading(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCoords({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
          setGpsStatus("LOCK_OK");
          setIsLoading(false);
        },
        () => {
          setIsLoading(false);
        }
      );
    } else {
      setIsLoading(false);
    }
  };

  // Nudge coordinates manually (moving the pin)
  const nudgeCoords = (direction: "N" | "S" | "E" | "W") => {
    const step = 0.0015; // roughly 150 meters
    setCoords((prev) => {
      let lat = prev.lat;
      let lng = prev.lng;
      if (direction === "N") lat += step;
      if (direction === "S") lat -= step;
      if (direction === "E") lng += step;
      if (direction === "W") lng -= step;
      return { lat, lng };
    });
    setGpsStatus("MANUAL_NUDGE");
  };

  // Google Maps Satellite Embed URL using dynamic coordinates
  const mapUrl = activeLayer === "satellite"
    ? `https://maps.google.com/maps?q=${coords.lat},${coords.lng}&t=k&z=16&ie=UTF8&iwloc=&output=embed`
    : `https://maps.google.com/maps?q=${coords.lat},${coords.lng}&t=p&z=15&ie=UTF8&iwloc=&output=embed`;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[82vh]">
      
      {/* Google Earth Local Tactical View (2/3 width) */}
      <div className="lg:col-span-2 bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 flex flex-col justify-between shadow-[0_8px_32px_rgba(0,0,0,0.4)] relative overflow-hidden group">
        
        {/* HUD Header */}
        <div className="flex flex-col md:flex-row justify-between items-stretch md:items-center gap-3 mb-3 pb-2 border-b border-[#243244]/50 z-10">
          <div className="flex items-center gap-2">
            <Compass className="w-4 h-4 text-sky-400 animate-spin-slow" />
            <h3 className="text-sm font-bold font-mono tracking-wider text-white uppercase">
              Google Earth Sector Control
            </h3>
          </div>

          {/* Search bar */}
          <form onSubmit={handleSearch} className="flex items-center gap-1 bg-[#0B0F14]/80 border border-[#243244] rounded px-2 py-1 flex-1 md:max-w-xs">
            <Search className="w-3.5 h-3.5 text-gray-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search location (e.g. London)..."
              className="bg-transparent border-none text-xs text-white focus:outline-none w-full font-mono placeholder-gray-600"
            />
          </form>

          <div className="flex items-center gap-2">
            {/* Layer Toggle */}
            <button
              onClick={() => setActiveLayer(activeLayer === "satellite" ? "terrain" : "satellite")}
              className="p-1.5 rounded bg-[#0B0F14]/60 border border-[#243244] text-gray-400 hover:text-white transition-colors cursor-pointer text-xs font-mono flex items-center gap-1"
            >
              <Layers className="w-3.5 h-3.5" />
              <span className="capitalize">{activeLayer}</span>
            </button>
            
            {/* Refresh */}
            <button
              onClick={handleRefresh}
              className="p-1.5 rounded bg-[#0B0F14]/60 border border-[#243244] text-gray-400 hover:text-white transition-colors cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
            </button>
          </div>
        </div>

        {/* Embedded Google Earth Iframe */}
        <div className="flex-1 rounded-lg overflow-hidden border border-[#243244]/60 relative bg-black">
          {isLoading ? (
            <div className="absolute inset-0 flex items-center justify-center bg-black/80 z-20 font-mono text-xs text-sky-400">
              RE-CALIBRATING SATELLITE LINK...
            </div>
          ) : null}
          
          <iframe
            title="Google Earth Airspace View"
            width="100%"
            height="100%"
            src={mapUrl}
            frameBorder="0"
            scrolling="no"
            marginHeight={0}
            marginWidth={0}
            className="filter grayscale-[15%] contrast-[110%] brightness-[90%]"
          />

          {/* Compass HUD Overlay */}
          <div className="absolute bottom-4 right-4 pointer-events-none bg-[#0B0F14]/80 border border-[#243244] p-3 rounded-lg flex flex-col items-center gap-1 shadow-lg font-mono text-[9px] text-sky-400">
            <div 
              className="w-10 h-10 rounded-full border border-sky-500/40 flex items-center justify-center relative"
              style={{ transform: `rotate(${rotation}deg)` }}
            >
              <span className="absolute top-0.5 text-[8px] font-bold text-red-400">N</span>
              <span className="absolute bottom-0.5 text-[8px] font-bold">S</span>
              <span className="absolute left-0.5 text-[8px] font-bold">W</span>
              <span className="absolute right-0.5 text-[8px] font-bold">E</span>
              <div className="w-0.5 h-6 bg-sky-400/50 absolute" />
            </div>
            <span>HDG: {(rotation).toFixed(1)}°</span>
          </div>

          {/* Tactical Overlay & Manual Inputs */}
          <div className="absolute top-4 left-4 bg-[#0B0F14]/85 border border-[#243244] p-4 rounded-lg shadow-lg font-mono text-[9px] text-gray-400 space-y-3 w-44">
            <div className="space-y-1.5 border-b border-border/45 pb-2">
              <div className="flex items-center justify-between">
                <span>LAT:</span>
                <input 
                  type="number" 
                  step="0.0001" 
                  value={coords.lat} 
                  onChange={(e) => {
                    const val = parseFloat(e.target.value);
                    if (!isNaN(val)) {
                      setCoords(prev => ({ ...prev, lat: val }));
                      setGpsStatus("MANUAL_LAT");
                    }
                  }}
                  className="bg-[#0B0F14] border border-[#243244] text-white px-1.5 py-0.5 rounded w-24 text-[10px] focus:outline-none focus:border-sky-500 font-mono"
                />
              </div>
              <div className="flex items-center justify-between">
                <span>LON:</span>
                <input 
                  type="number" 
                  step="0.0001" 
                  value={coords.lng} 
                  onChange={(e) => {
                    const val = parseFloat(e.target.value);
                    if (!isNaN(val)) {
                      setCoords(prev => ({ ...prev, lng: val }));
                      setGpsStatus("MANUAL_LNG");
                    }
                  }}
                  className="bg-[#0B0F14] border border-[#243244] text-white px-1.5 py-0.5 rounded w-24 text-[10px] focus:outline-none focus:border-sky-500 font-mono"
                />
              </div>
            </div>

            {/* Manual Nudge D-Pad (Moving the pin manually) */}
            <div className="flex flex-col items-center gap-1 border-b border-border/45 pb-2">
              <span className="text-[8px] text-gray-500">MANUAL NUDGE CONTROLS</span>
              <button 
                onClick={() => nudgeCoords("N")}
                className="p-1 rounded bg-[#121A22] border border-[#243244] text-sky-400 hover:text-white hover:border-sky-500 transition-all cursor-pointer"
              >
                <ArrowUp className="w-3 h-3" />
              </button>
              <div className="flex gap-4">
                <button 
                  onClick={() => nudgeCoords("W")}
                  className="p-1 rounded bg-[#121A22] border border-[#243244] text-sky-400 hover:text-white hover:border-sky-500 transition-all cursor-pointer"
                >
                  <ArrowLeft className="w-3 h-3" />
                </button>
                <button 
                  onClick={() => nudgeCoords("E")}
                  className="p-1 rounded bg-[#121A22] border border-[#243244] text-sky-400 hover:text-white hover:border-sky-500 transition-all cursor-pointer"
                >
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
              <button 
                onClick={() => nudgeCoords("S")}
                className="p-1 rounded bg-[#121A22] border border-[#243244] text-sky-400 hover:text-white hover:border-sky-500 transition-all cursor-pointer"
              >
                <ArrowDown className="w-3 h-3" />
              </button>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between gap-2">
                <span>SOURCE:</span>
                <span className="text-white truncate max-w-[80px]">{gpsStatus}</span>
              </div>
              <div className="flex justify-between gap-2 text-emerald-400">
                <span>GPS LINK:</span>
                <span className="font-bold animate-pulse">ACTIVE</span>
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* Global 3D Satellite Globe & Tracker (1/3 width) */}
      <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 flex flex-col justify-between shadow-[0_8px_32px_rgba(0,0,0,0.4)]">
        
        <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[#243244]/50">
          <Globe className="w-4 h-4 text-emerald-400" />
          <h3 className="text-sm font-bold font-mono tracking-wider text-white uppercase">
            Global Threat Globe
          </h3>
        </div>

        {/* Global WebGL-style rotating Globe using SVG */}
        <div className="flex-1 flex flex-col items-center justify-center bg-[#0B0F14]/50 rounded-xl border border-border/40 p-4 relative overflow-hidden">
          
          {/* Rotating radar grid ring */}
          <div 
            className="absolute w-44 h-44 rounded-full border border-sky-500/15 flex items-center justify-center"
            style={{ transform: `rotate(${-rotation}deg)` }}
          >
            <div className="w-full h-[1px] bg-sky-500/20" />
            <div className="w-[1px] h-full bg-sky-500/20" />
          </div>

          {/* SVG Globe */}
          <svg className="w-40 h-40 z-10" viewBox="0 0 100 100">
            {/* Globe sphere */}
            <circle cx="50" cy="50" r="45" fill="none" stroke="#243244" strokeWidth="1" />
            
            {/* Latitude lines */}
            <path d="M 6 40 Q 50 50 94 40" fill="none" stroke="#243244" strokeWidth="0.5" opacity="0.6" />
            <path d="M 5 50 Q 50 62 95 50" fill="none" stroke="#243244" strokeWidth="0.5" opacity="0.6" />
            <path d="M 6 60 Q 50 72 94 60" fill="none" stroke="#243244" strokeWidth="0.5" opacity="0.6" />
            
            {/* Longitude lines */}
            <path d="M 50 5 Q 35 50 50 95" fill="none" stroke="#243244" strokeWidth="0.5" opacity="0.6" />
            <path d="M 50 5 Q 65 50 50 95" fill="none" stroke="#243244" strokeWidth="0.5" opacity="0.6" />
            <path d="M 50 5 Q 20 50 50 95" fill="none" stroke="#243244" strokeWidth="0.5" opacity="0.3" />
            <path d="M 50 5 Q 80 50 50 95" fill="none" stroke="#243244" strokeWidth="0.3" opacity="0.3" />

            {/* Glowing threat arcs (trajectories) */}
            <path 
              d="M 20 60 Q 50 20 75 45" 
              fill="none" 
              stroke="#EF4444" 
              strokeWidth="1.5" 
              strokeDasharray="4 2"
              className="animate-pulse"
            />
            <path 
              d="M 35 30 Q 60 70 80 55" 
              fill="none" 
              stroke="#F59E0B" 
              strokeWidth="1.2" 
              strokeDasharray="3 3"
            />

            {/* Drone nodes */}
            <circle cx="20" cy="60" r="2" fill="#EF4444" className="animate-ping" />
            <circle cx="75" cy="45" r="2" fill="#EF4444" />
            <circle cx="35" cy="30" r="1.5" fill="#F59E0B" />
            <circle cx="80" cy="55" r="1.5" fill="#F59E0B" />
            
            {/* Sector center */}
            <circle cx="58" cy="52" r="2.5" fill="#10B981" />
            <circle cx="58" cy="52" r="6" fill="none" stroke="#10B981" strokeWidth="0.5" className="animate-ping" />
          </svg>

          <span className="text-[10px] font-mono text-gray-400 mt-4 z-10">ORBITAL VIEW: ACTIVE</span>
        </div>

        {/* Radar Station details */}
        <div className="mt-4 space-y-2.5 font-mono text-[10px] text-gray-400">
          <div className="flex justify-between border-b border-border/30 pb-1.5">
            <span className="flex items-center gap-1"><Radio className="w-3 h-3 text-sky-400" /> Station Alpha</span>
            <span className="text-emerald-400">ONLINE</span>
          </div>
          <div className="flex justify-between border-b border-border/30 pb-1.5">
            <span className="flex items-center gap-1"><Radio className="w-3 h-3 text-sky-400" /> Station Beta</span>
            <span className="text-emerald-400">ONLINE</span>
          </div>
          <div className="flex justify-between border-b border-border/30 pb-1.5">
            <span className="flex items-center gap-1"><ShieldAlert className="w-3 h-3 text-red-400" /> Threat Vector</span>
            <span className="text-red-400 font-bold">142° (SECTOR A)</span>
          </div>
        </div>

      </div>

    </div>
  );
}