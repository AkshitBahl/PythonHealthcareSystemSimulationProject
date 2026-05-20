"use client";

import Sidebar from "./components/Sidebar";
import StatCard from "./components/StatCard";
import PatientTable from "./components/PatientTable";
import { useSimulation } from "./hooks/useSimulation";

/*
 Dashboard Home Page
 KPI stat cards (patients, beds, infections, pharmacy)
 Bed occupancy chart
 Quick patient overview table
*/
export default function DashboardPage() {
  const { data, connected, toggleMode, tickSim, resetSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar
          data={null}
          connected={connected}
          onToggleMode={() => { }}
          onReset={() => { }}
          onTick={() => { }}
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
  const infectedCount = statusCounts.Infected || 0;
  const admittedCount = patients.filter((p) => p.admitted).length;

  return (
    <div className="app-layout">
      <Sidebar
        data={data}
        connected={connected}
        onToggleMode={toggleMode}
        onReset={resetSim}
        onTick={tickSim}
      />
      <main className="main-content">
        {/* Page Header */}
        <div className="page-header fade-in">
          <h2>Dashboard Overview</h2>
          <p>
            Healthcare network status — Day {data.day} ·{" "}
            <span style={{ color: mode.is_pandemic ? "var(--red)" : "var(--green)" }}>
              {mode.is_pandemic ? "Pandemic Mode" : "Normal Operations"}
            </span>
          </p>
        </div>

        {/* KPI Stats */}
        <div className="stats-grid">
          <StatCard
            label="Total Patients"
            value={overview.total_patients}
            sub={`${admittedCount} admitted · ${statusCounts.Healthy || 0} healthy · ${statusCounts.Deceased || 0} deceased`}
            color="blue"
          />
          <StatCard
            label="Bed Occupancy"
            value={`${overview.overall_occupancy || 0}%`}
            sub={`${overview.total_occupied_beds || 0} / ${overview.total_beds || 0} beds`}
            color={overview.overall_occupancy >= 80 ? "red" : overview.overall_occupancy >= 50 ? "amber" : "green"}
          />
          <StatCard
            label="Active Infections"
            value={infectedCount}
            sub={mode.is_pandemic ? `${statusCounts.Healthy || 0} healthy · ${statusCounts.Deceased || 0} deceased` : "Normal operations"}
            color={infectedCount > 0 ? "red" : "green"}
          />
          <StatCard
            label="Pharmacy Stock"
            value={totalStock.toLocaleString()}
            sub={lowStockCount > 0 ? `${lowStockCount} low stock alerts` : "All medications stocked"}
            color={lowStockCount > 0 ? "amber" : "cyan"}
          />
          <StatCard
            label="Hospitals"
            value={overview.total_hospitals}
            sub={`${overview.total_doctors || 0} doctors`}
            color="purple"
          />
          <StatCard
            label="Day"
            value={data.day}
            sub="Current simulation day"
            color="cyan"
          />
        </div>

        {/* Patient Table */}
        <PatientTable patients={patients} hospitals={hospitals} />
      </main>
    </div>
  );
}
