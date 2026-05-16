"use client";

import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import { useSimulation } from "../hooks/useSimulation";

/**
 * Pharmacy Page
 *
 * Shows medication inventory across all pharmacies:
 * - Summary KPI cards
 * - Medication cards grid with stock levels
 * - Low-stock alerts
 */
export default function PharmacyPage() {
  const { data, connected, toggleMode, tickSim, resetSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => {}} onReset={() => {}} onTick={() => {}} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading pharmacy...</div></div>
        </main>
      </div>
    );
  }

  const pharmacies = data.pharmacies || [];

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onReset={resetSim} onTick={tickSim} />
      <main className="main-content">
        <div className="page-header fade-in">
          <h2>Pharmacy</h2>
          <p>Medication inventory and prescription management — Day {data.day}</p>
        </div>

        {pharmacies.map((pharmacy) => {
          const meds = pharmacy.inventory || [];

          const totalStock = meds.reduce((sum, item) => sum + item.stock, 0);
          const lowStockCount = meds.filter((item) => item.stock < 20).length;

          return (
            <div key={pharmacy.id} style={{ marginBottom: "40px" }}>
              {/* Pharmacy Header */}
              <h3 style={{
                fontSize: "16px", fontWeight: 600, color: "var(--text-primary)",
                marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px",
              }}>
                {pharmacy.name}
                <span style={{
                  fontSize: "11px", color: "var(--text-muted)", fontWeight: 400,
                }}>
                  — {pharmacy.location}
                </span>
              </h3>

              {/* Summary Stats */}
              <div className="stats-grid" style={{ marginBottom: "20px" }}>
                <StatCard
                  label="Total Stock"
                  value={totalStock.toLocaleString()}
                  sub={`${meds.length} medications`}
                  color="blue"
                />
                <StatCard
                  label="Low Stock Alerts"
                  value={lowStockCount}
                  sub={lowStockCount > 0 ? "Under 20 units" : "All stocked"}
                  color={lowStockCount > 0 ? "red" : "green"}
                />
                <StatCard
                  label="Prescriptions Filled"
                  value={pharmacy.prescriptions_filled || 0}
                  sub={`${pharmacy.daily_prescriptions || 0} today`}
                  color="purple"
                />
              </div>

              {/* Medications Grid */}
              <div className="inventory-grid">
                {meds.map((med) => (
                  <div
                    className={`med-card ${med.stock < 20 ? "low-stock" : ""}`}
                    key={med.name}
                  >
                    <div className="med-card-name">{med.name}</div>
                    <div className={`med-card-stock ${med.stock < 20 ? "low" : ""}`}>
                      {med.stock}
                    </div>
                    <div className="med-card-stock-label">
                      {med.stock < 20 ? "Low Stock" : "Units in stock"}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </main>
    </div>
  );
}
