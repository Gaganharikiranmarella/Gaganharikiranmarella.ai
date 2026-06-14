export default function Topbar() {
  return (
    <div
      className="
      h-16
      border-b
      border-border
      bg-card
      flex
      items-center
      justify-between
      px-6
    "
    >
      <h2
        className="
        text-lg
        font-semibold
      "
      >
        Command Center
      </h2>

      <div
        className="
        flex
        items-center
        gap-3
      "
      >
        <div
          className="
          w-3
          h-3
          rounded-full
          bg-success
        "
        />

        <span>SYSTEM OPERATIONAL</span>
      </div>
    </div>
  );
}