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
  const { data, connected, toggleMode, startSim, stopSim, tickSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => {}} onStart={() => {}} onStop={() => {}} onTick={() => {}} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading pharmacy...</div></div>
        </main>
      </div>
    );
  }

  const pharmacies = data.pharmacies || [];

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onStart={startSim} onStop={stopSim} onTick={tickSim} />
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
            <div key={pharmacy.id} style={{ marginBottom: "48px" }}>
              {/* Pharmacy Header */}
              <h3 style={{
                fontSize: "18px", fontWeight: 700, color: "var(--text-primary)",
                marginBottom: "20px", display: "flex", alignItems: "center", gap: "10px",
              }}>
                💊 {pharmacy.name}
                <span style={{
                  fontSize: "12px", color: "var(--text-muted)", fontWeight: 400,
                }}>
                  📍 {pharmacy.location}
                </span>
              </h3>

              {/* Summary Stats */}
              <div className="stats-grid stagger-children" style={{ marginBottom: "24px" }}>
                <StatCard
                  icon="📦"
                  label="Total Stock"
                  value={totalStock.toLocaleString()}
                  sub={`${meds.length} medications`}
                  color="blue"
                />
                <StatCard
                  icon="⚠️"
                  label="Low Stock Alerts"
                  value={lowStockCount}
                  sub={lowStockCount > 0 ? "Under 20 units" : "All stocked"}
                  color={lowStockCount > 0 ? "red" : "green"}
                />
                <StatCard
                  icon="📋"
                  label="Prescriptions Filled"
                  value={pharmacy.prescriptions_filled || 0}
                  sub={`${pharmacy.daily_prescriptions || 0} today`}
                  color="purple"
                />
              </div>

              {/* Medications Grid */}
              <div className="inventory-grid stagger-children">
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
                      {med.stock < 20 ? "⚠️ Low Stock" : "Units in stock"}
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
