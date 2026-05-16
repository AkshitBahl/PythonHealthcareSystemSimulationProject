"use client";

import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import { useSimulation } from "../hooks/useSimulation";

/**
 * Pandemic Page
 *
 * Dedicated pandemic monitoring dashboard showing:
 * - Health compartment summary cards (Healthy, Infected, Deceased)
 * - Pandemic stat cards
 * - Pandemic parameters
 */
export default function PandemicPage() {
  const { data, connected, toggleMode, tickSim, resetSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => {}} onReset={() => {}} onTick={() => {}} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading pandemic data...</div></div>
        </main>
      </div>
    );
  }

  const mode = data.mode || {};
  const sir = data.sir;
  const pandemic = data.pandemic;

  if (!mode.is_pandemic) {
    return (
      <div className="app-layout">
        <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onReset={resetSim} onTick={tickSim} />
        <main className="main-content">
          <div className="page-header fade-in">
            <h2>Pandemic Response</h2>
            <p>Currently in Normal Operations mode</p>
          </div>
          <div className="empty-state">
            <h3>Pandemic Mode Not Active</h3>
            <p>Switch to Pandemic mode using the toggle in the sidebar to activate pandemic response monitoring and infection tracking.</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onReset={resetSim} onTick={tickSim} />
      <main className="main-content">
        <div className="page-header fade-in">
          <h2>Pandemic Response</h2>
          <p>Active pandemic monitoring — Day {data.day}</p>
        </div>

        {/* Health Compartment Summary Cards */}
        {sir && (
          <div className="sir-summary">
            <div className="sir-card susceptible">
              <div className="sir-card-value">{sir.healthy}</div>
              <div className="sir-card-label">Healthy</div>
            </div>
            <div className="sir-card infected">
              <div className="sir-card-value">{sir.infected}</div>
              <div className="sir-card-label">Infected</div>
            </div>
            <div className="sir-card deceased">
              <div className="sir-card-value">{sir.deceased}</div>
              <div className="sir-card-label">Deceased</div>
            </div>
          </div>
        )}

        {/* Pandemic Stat Cards */}
        {pandemic && (
          <div className="stats-grid">
            <StatCard
              label="Total Infections"
              value={pandemic.total_infections}
              sub={`+${pandemic.daily_new_infections} today`}
              color="red"
            />
            <StatCard
              label="Total Deaths"
              value={pandemic.total_deaths}
              sub={`+${pandemic.daily_new_deaths} today`}
              color="purple"
            />
            <StatCard
              label="Infection Rate"
              value={`${(mode.infection_rate * 100).toFixed(0)}%`}
              sub="Base transmission probability"
              color="amber"
            />
            <StatCard
              label="Surge Capacity"
              value={`${mode.surge_capacity_multiplier}x`}
              sub="Hospital bed multiplier"
              color="cyan"
            />
          </div>
        )}

        {/* Pandemic Parameters */}
        <div className="chart-card" style={{ marginTop: "20px" }}>
          <h3>Active Pandemic Parameters</h3>
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            gap: "14px",
            marginTop: "14px",
          }}>
            {[
              { label: "Infection Rate", value: `${(mode.infection_rate * 100).toFixed(1)}%` },
              { label: "Surge Capacity", value: `${mode.surge_capacity_multiplier}x` },
            ].map((param) => (
              <div key={param.label} style={{
                padding: "10px 14px",
                background: "var(--bg-glass)",
                border: "1px solid var(--border-color)",
                borderRadius: "var(--radius-sm)",
              }}>
                <div style={{ fontSize: "10px", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.04em" }}>
                  {param.label}
                </div>
                <div style={{ fontSize: "16px", fontWeight: 700, color: "var(--text-primary)", marginTop: "4px" }}>
                  {param.value}
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
