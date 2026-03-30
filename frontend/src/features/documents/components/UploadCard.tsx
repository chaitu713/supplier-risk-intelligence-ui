import type { ReactNode } from "react";

interface UploadCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  tintClassName: string;
  children: ReactNode;
}

export function UploadCard({
  icon,
  title,
  description,
  tintClassName,
  children,
}: UploadCardProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center gap-3">
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-2xl text-lg ${tintClassName}`}
        >
          {icon}
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-900">{title}</h3>
          <p className="text-xs text-slate-500">{description}</p>
        </div>
      </div>
      {children}
    </section>
  );
}
