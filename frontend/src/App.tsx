import { Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "./components/layout/AppShell";
import { DataExplorerPage } from "./features/data-explorer/pages/DataExplorerPage";
import { DocumentIngestionPage } from "./features/documents/pages/DocumentIngestionPage";
import { OverviewDashboardPage } from "./features/overview-dashboard/pages/OverviewDashboardPage";
import { RiskMonitoringPage } from "./features/risk-monitoring/pages/RiskMonitoringPage";
import { SupplierAdvisorAIPage } from "./features/advisor-ai/pages/SupplierAdvisorAIPage";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<DocumentIngestionPage />} />
        <Route path="/data-explorer" element={<DataExplorerPage />} />
        <Route path="/overview-dashboard" element={<OverviewDashboardPage />} />
        <Route path="/risk-monitoring" element={<RiskMonitoringPage />} />
        <Route path="/supplier-advisor-ai" element={<SupplierAdvisorAIPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}
