import VideoStream
from "../../components/video/VideoStream";

import StreamStatus
from "../../components/video/StreamStatus";

import TelemetryPanel
from "../../components/video/TelemetryPanel";

export default function VideoIntel() {

  return (

    <div
      className="
      p-5
      bg-background
      h-full
    "
    >

      <StreamStatus />

      <div
        className="
        grid
        grid-cols-4
        gap-5
        mt-5
      "
      >

        <div
          className="
          col-span-3
        "
        >
          <VideoStream />
        </div>

        <TelemetryPanel />

      </div>

    </div>
  );
}