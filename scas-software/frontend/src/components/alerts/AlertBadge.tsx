interface Props {
  severity: string;
}

export default function AlertBadge({
  severity
}: Props) {

  const color =
    severity === "CRITICAL"
      ? "#EF4444"
      : severity === "HIGH"
      ? "#F59E0B"
      : severity === "MEDIUM"
      ? "#38BDF8"
      : "#10B981";

  return (

    <span
      style={{
        background: color,
        padding:
          "4px 10px",
        borderRadius: 8
      }}
    >
      {severity}
    </span>
  );
}