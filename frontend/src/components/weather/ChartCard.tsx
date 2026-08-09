import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { CardSkeleton, EmptyState, ErrorState } from "../common/States";
import "./chart-card.css";

interface ChartCardProps {
  title: string;
  data: Array<Record<string, unknown>> | null | undefined;
  dataKey: string;
  xKey?: string;
  color?: string;
  unit?: string;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  valueFormatter?: (value: number) => string;
}

export function ChartCard({
  title,
  data,
  dataKey,
  xKey = "label",
  color = "var(--accent)",
  unit = "",
  loading,
  error,
  onRetry,
  valueFormatter,
}: ChartCardProps) {
  const hasData = data && data.length > 0;

  return (
    <div className="panel chart-card">
      <div className="panel__header">
        <h3>{title}</h3>
      </div>
      <div className="chart-card__body">
        {loading && !hasData && <CardSkeleton lines={2} />}
        {!loading && error && !hasData && (
          <ErrorState title={`Unable to load ${title.toLowerCase()}.`} onRetry={onRetry} />
        )}
        {!loading && !error && !hasData && (
          <EmptyState title="No history yet" description="Trend data will appear once readings accumulate." />
        )}
        {hasData && (
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="var(--border)" vertical={false} />
              <XAxis
                dataKey={xKey}
                tick={{ fill: "var(--text-tertiary)", fontSize: 11 }}
                axisLine={{ stroke: "var(--border)" }}
                tickLine={false}
                minTickGap={24}
              />
              <YAxis
                tick={{ fill: "var(--text-tertiary)", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                width={40}
                unit={unit}
              />
              <Tooltip
                contentStyle={{
                  background: "var(--surface-2)",
                  border: "1px solid var(--border-strong)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
                labelStyle={{ color: "var(--text-secondary)" }}
                formatter={(value) => {
                  const num = typeof value === "number" ? value : Number(value);
                  return [valueFormatter ? valueFormatter(num) : `${num}${unit}`, title];
                }}
              />
              <Line
                type="monotone"
                dataKey={dataKey}
                stroke={color}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
