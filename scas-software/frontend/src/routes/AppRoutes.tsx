import { Routes, Route } from "react-router-dom";
import Dashboard from "../pages/Dashboard/Dashboard";
import Airspace from "../pages/Airspace/Airspace";
import VideoIntel from "../pages/VideoIntel/VideoIntel";
import ThreatIntel from "../pages/ThreatIntel/ThreatIntel";
import Analytics from "../pages/Analytics/Analytics";
import Settings from "../pages/Settings/Settings";
import Overview from "../pages/Overview/Overview";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/airspace" element={<Airspace />} />
      <Route path="/video-intel" element={<VideoIntel />} />
      <Route path="/threat-intel" element={<ThreatIntel />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/overview" element={<Overview />} />
    </Routes>
  );
}