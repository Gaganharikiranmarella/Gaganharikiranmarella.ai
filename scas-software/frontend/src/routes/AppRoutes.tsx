import { Routes, Route }
from "react-router-dom";

import Dashboard
from "../pages/Dashboard/Dashboard";

import Airspace
from "../pages/Airspace/Airspace";

import VideoIntel
from "../pages/VideoIntel/VideoIntel";

export default function AppRoutes() {

  return (

    <Routes>

      <Route
        path="/"
        element={<Dashboard />}
      />

      <Route
        path="/airspace"
        element={<Airspace />}
      />

      <Route
        path="/video-intel"
        element={<VideoIntel />}
      />

    </Routes>
  );
}