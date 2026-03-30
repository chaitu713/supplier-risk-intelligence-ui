interface KpiCardProps {
  label: string;
  value: string;
  subtitle: string;
  accentClassName: string;
}

export function KpiCard({
  label,
  value,
  subtitle,
  accentClassName,
}: KpiCardProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className={`h-1.5 w-14 rounded-full ${accentClassName}`} />
      <p className="mt-5 text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
        {label}
      </p>
      <p className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
        {value}
      </p>
      <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
    </div>
  );
}
