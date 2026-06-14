export default function StreamStatus() {

  return (

    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-4
      flex
      justify-between
      items-center
    "
    >

      <div>

        <h2
          className="
          text-xl
          font-semibold
        "
        >
          Video Intelligence
        </h2>

        <p className="text-gray-400">

          Live ISR Feed

        </p>

      </div>

      <div
        className="
        flex
        gap-3
        items-center
      "
      >

        <div
          className="
          w-3
          h-3
          rounded-full
          bg-green-500
        "
        />

        <span>

          STREAM CONNECTED

        </span>

      </div>

    </div>
  );
}