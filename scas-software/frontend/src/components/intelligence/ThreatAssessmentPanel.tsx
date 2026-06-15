export default function ThreatAssessmentPanel(){

  return(

    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-5
    "
    >

      <h3 className="mb-4">

        Threat Assessment

      </h3>

      <div>

        Threat Score

        <div
          className="
          text-red-500
          text-4xl
          font-bold
        "
        >
          0.91
        </div>

      </div>

      <div className="mt-4">

        Classification:

        CRITICAL

      </div>

    </div>
  );
}