import {
  useThreatStore
} from "../../store/threatStore";

export default function ThreatIntel() {

  const threats =
    useThreatStore(
      state => state.threats
    );

  return (

    <div
      className="
      p-5
      bg-background
      h-full
    "
    >

      <h1
        className="
        text-2xl
        font-bold
        mb-5
      "
      >

        Threat Intelligence

      </h1>

      <div
        className="
        grid
        grid-cols-2
        gap-4
      "
      >

        {threats.map(
          threat => (

          <div

            key={threat.id}

            className="
            bg-card
            border
            border-border
            rounded-xl
            p-5
          "
          >

            <h3>

              {threat.cluster}

            </h3>

            <p>

              Threat:
              {" "}
              {threat.score}

            </p>

            <p>

              ETA:
              {" "}
              {threat.eta}s

            </p>

            <p>

              Class:
              {" "}
              {threat.classification}

            </p>

          </div>

        ))}

      </div>

    </div>
  );
}