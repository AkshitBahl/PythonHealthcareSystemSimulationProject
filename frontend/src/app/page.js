"use client";

import Sidebar from "./components/Sidebar";
import StatCard from "./components/StatCard";
import BedChart from "./components/BedChart";
import InfectionChart from "./components/InfectionChart";
import PatientTable from "./components/PatientTable";
import { useSimulation } from "./hooks/useSimulation";

/**
 * Dashboard Home Page
 * 
 * Main overview page showing:
 * - KPI stat cards (patients, beds, infections, pharmacy)
 * - Bed occupancy chart
 * - Infection curve chart (pandemic mode)
 * - Quick patient overview table
 */
export default function DashboardPage() {
  const { data, connected, toggleMode, startSim, stopSim, tickSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar
          data={null}
          connected={connected}
          onToggleMode={() => {}}
          onStart={() => {}}
          onStop={() => {}}
          onTick={() => {}}
        />
        <main className="main-content">
          <div className="loading-container">
            <div className="loading-spinner" />
            <div className="loading-text">Connecting to simulation backend...</div>
          </div>
        </main>
      </div>
    );
  }

  const overview = data.overview || {};
  const mode = data.mode || {};
  const hospitals = data.hospitals || [];
  const patients = data.patients || [];
  const pharmacies = data.pharmacies || [];
  const statistics = data.statistics || [];
  const sir = data.sir;

  // Calculate pharmacy stock
  const totalStock = pharmacies.reduce((acc, p) => {
    return acc + p.inventory.reduce((sum, item) => sum + item.stock, 0);
  }, 0);
  const lowStockCount = pharmacies.reduce((acc, p) => {
    return acc + p.inventory.filter((item) => item.stock < 20).length;
  }, 0);

  // Patient status counts
  const statusCounts = {};
  patients.forEach((p) => {
    statusCounts[p.health_status] = (statusCounts[p.health_status] || 0) + 1;
  });
  const infectedCount = patients.filter((p) => p.infected).length;
  const admittedCount = patients.filter((p) => p.admitted).length;

  return (
    <div className="app-layout">
      <Sidebar
        data={data}
        connected={connected}
        onToggleMode={toggleMode}
        onStart={startSim}
        onStop={stopSim}
        onTick={tickSim}
      />
      <main className="main-content">
        {/* Page Header */}
        <div className="page-header fade-in">
          <h2>Dashboard Overview</h2>
          <p>
            Real-time healthcare network status — Day {data.day} •{" "}
            <span style={{ color: mode.is_pandemic ? "var(--red)" : "var(--green)" }}>
              {mode.is_pandemic ? "🔴 Pandemic Mode" : "🟢 Normal Operations"}
            </span>
          </p>
        </div>

        {/* KPI Stats */}
        <div className="stats-grid stagger-children">
          <StatCard
            icon="👥"
            label="Total Patients"
            value={overview.total_patients}
            sub={`${admittedCount} admitted · ${statusCounts.Healthy || 0} healthy`}
            color="blue"
          />
          <StatCard
            icon="🛏️"
            label="Bed Occupancy"
            value={`${overview.overall_occupancy || 0}%`}
            sub={`${overview.total_occupied_beds || 0} / ${overview.total_capacity || 0} beds`}
            color={overview.overall_occupancy >= 80 ? "red" : overview.overall_occupancy >= 50 ? "amber" : "green"}
          />
          <StatCard
            icon="🦠"
            label="Active Infections"
            value={infectedCount}
            sub={mode.is_pandemic ? `${sir?.recovered || 0} recovered · ${sir?.deceased || 0} deceased` : "Normal operations"}
            color={infectedCount > 0 ? "red" : "green"}
          />
          <StatCard
            icon="💊"
            label="Pharmacy Stock"
            value={totalStock.toLocaleString()}
            sub={lowStockCount > 0 ? `⚠️ ${lowStockCount} low stock alerts` : "All medications stocked"}
            color={lowStockCount > 0 ? "amber" : "cyan"}
          />
          <StatCard
            icon="🏥"
            label="Hospitals"
            value={overview.total_hospitals}
            sub={`${overview.total_doctors || 0} doctors`}
            color="purple"
          />
          <StatCard
            icon="📊"
            label="Day"
            value={data.day}
            sub={data.running ? "▶ Simulation running" : "⏸ Paused"}
            color="cyan"
          />
        </div>

        {/* Charts */}
        <div className="charts-grid">
          <BedChart hospitals={hospitals} />
          <InfectionChart statistics={statistics} />
        </div>

        {/* Patient Table */}
        <PatientTable patients={patients} hospitals={hospitals} />
      </main>
    </div>
  );
}
