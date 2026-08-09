import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import { ToastProvider } from "./components/common/ToastContext";
import Dashboard from "./pages/Dashboard";
import Sensors from "./pages/Sensors";
import SensorDetails from "./pages/SensorDetails";
import Weather from "./pages/Weather";
import Predictions from "./pages/Predictions";
import Recommendations from "./pages/Recommendations";
import Alerts from "./pages/Alerts";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/sensors" element={<Sensors />} />
            <Route path="/sensors/:id" element={<SensorDetails />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  );
}
