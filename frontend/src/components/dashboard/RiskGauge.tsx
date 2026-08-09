import "./risk-gauge.css";

const LEVELS = ["LOW", "MEDIUM", "HIGH", "SEVERE"];
const COLORS: Record<string, string> = {
  LOW: "var(--risk-low)",
  MEDIUM: "var(--risk-medium)",
  HIGH: "var(--risk-high)",
  SEVERE: "var(--risk-severe)",
};

interface RiskGaugeProps {
  risk: string | null | undefined;
}

/**
 * A four-segment arc gauge — the dashboard's signature element.
 * Each arc segment represents one risk tier; the active tier is lit
 * and the needle-less pointer sits under the current reading.
 */
export function RiskGauge({ risk }: RiskGaugeProps) {
  const key = (risk || "").toUpperCase();
  const activeIndex = LEVELS.indexOf(key);

  // Four 39-degree segments across a 180-degree semicircle, with 3-degree gaps.
  const segAngle = 39;
  const gap = 3;
  const startAngle = -90;

  const polarToCartesian = (cx: number, cy: number, r: number, angleDeg: number) => {
    const angleRad = (angleDeg * Math.PI) / 180;
    return { x: cx + r * Math.cos(angleRad), y: cy + r * Math.sin(angleRad) };
  };

  const describeArc = (cx: number, cy: number, r: number, a0: number, a1: number) => {
    const start = polarToCartesian(cx, cy, r, a0);
    const end = polarToCartesian(cx, cy, r, a1);
    return `M ${start.x} ${start.y} A ${r} ${r} 0 0 1 ${end.x} ${end.y}`;
  };

  const segments = LEVELS.map((level, i) => {
    const a0 = startAngle + i * (segAngle + gap);
    const a1 = a0 + segAngle;
    return { level, path: describeArc(90, 90, 72, a0, a1) };
  });

  const pointerAngle =
    activeIndex >= 0
      ? startAngle + activeIndex * (segAngle + gap) + segAngle / 2
      : null;
  const pointerPos =
    pointerAngle !== null ? polarToCartesian(90, 90, 50, pointerAngle) : null;

  return (
    <div className="risk-gauge">
      <svg viewBox="0 0 180 108" className="risk-gauge__svg">
        {segments.map((seg) => (
          <path
            key={seg.level}
            d={seg.path}
            fill="none"
            stroke={seg.level === key ? COLORS[seg.level] : "var(--border-strong)"}
            strokeWidth={seg.level === key ? 11 : 9}
            strokeLinecap="round"
            style={{
              filter: seg.level === key ? `drop-shadow(0 0 5px ${COLORS[seg.level]})` : "none",
              transition: "all 0.3s ease",
            }}
          />
        ))}
        {pointerPos && (
          <circle
            cx={pointerPos.x}
            cy={pointerPos.y}
            r="4.5"
            fill={COLORS[key]}
            style={{ filter: `drop-shadow(0 0 4px ${COLORS[key]})` }}
          />
        )}
      </svg>
      <div className="risk-gauge__readout">
        <div className="risk-gauge__value mono" style={{ color: activeIndex >= 0 ? COLORS[key] : "var(--text-tertiary)" }}>
          {key || "N/A"}
        </div>
        <div className="risk-gauge__caption">Current Risk</div>
      </div>
    </div>
  );
}
