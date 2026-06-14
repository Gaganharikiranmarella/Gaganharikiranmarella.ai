const messages = [

"TRACKING HOSTILE UAV SWARM",

"PREDICTIVE TRAJECTORY MODEL ACTIVE",

"THREAT CLASSIFIER OPERATIONAL",

"MULTI-TARGET TRACKING ACTIVE",

"COMMAND NETWORK SECURE"
];

export default function IntelTicker() {

  return (

    <div
      className="
      overflow-hidden
      border
      border-border
      rounded-xl
      bg-card
      p-3
    "
    >

      <div
        className="
        animate-pulse
        whitespace-nowrap
      "
      >

        {messages.join(" • ")}

      </div>

    </div>
  );
}