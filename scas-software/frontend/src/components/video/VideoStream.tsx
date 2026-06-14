import DetectionOverlay
from "./DetectionOverlay";

export default function VideoStream() {

  const detections = [

    {
      x:120,
      y:100,
      width:120,
      height:80,
      label:"UAV-001",
      confidence:0.94
    }
  ];

  return (

    <div
      className="
      relative
      bg-black
      rounded-xl
      overflow-hidden
      border
      border-border
      h-[700px]
    "
    >

      <img

        src="
http://192.168.1.10:8080/video
"

        className="
        w-full
        h-full
        object-cover
      "

      />

      <DetectionOverlay

        detections={detections}

      />

    </div>
  );
}