interface Props {
  title: string;
  value: string;
  color: string;
}

export default function ThreatCard({
  title,
  value,
  color
}: Props) {
  return (
    <div
      className="
      bg-card
      border
      border-border
      rounded-xl
      p-5
    "
    >
      <p className="text-gray-400">
        {title}
      </p>

      <h2
        className="text-3xl font-bold mt-2"
        style={{ color }}
      >
        {value}
      </h2>
    </div>
  );
}