import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

interface AppShellProps {
  children: ReactNode;
}

const navItems = [
  { to: "/", label: "Document Ingestion" },
  { to: "/data-explorer", label: "Data Explorer" },
  { to: "/overview-dashboard", label: "Overview Dashboard" },
  { to: "/risk-monitoring", label: "Risk Monitoring" },
  { to: "/supplier-advisor-ai", label: "Supplier Advisor AI" },
];

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur lg:hidden">
        <div className="mx-auto flex max-w-7xl gap-2 overflow-x-auto px-4 py-3">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium transition ${
                  isActive
                    ? "bg-blue-700 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </div>

      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-200 bg-white px-5 py-6 lg:block">
        <div className="rounded-3xl bg-gradient-to-br from-blue-700 to-indigo-700 px-5 py-6 text-white shadow-lg">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-100">
            Supplier Intelligence
          </p>
          <h1 className="mt-3 text-xl font-semibold leading-tight">
            React Migration Workspace
          </h1>
          <p className="mt-2 text-sm text-blue-100">
            Streamlit features being migrated one page at a time into a production-ready UI.
          </p>
        </div>

        <nav className="mt-8 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-blue-50 text-blue-700"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="lg:pl-72">{children}</main>
    </div>
  );
}
