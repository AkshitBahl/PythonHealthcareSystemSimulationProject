"use client";

import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import InfectionChart from "../components/InfectionChart";
import { useSimulation } from "../hooks/useSimulation";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

/**
 * Pandemic Page
 * 
 * Dedicated pandemic monitoring dashboard showing:
 * - Health compartment summary cards (Healthy, Infected, Deceased)
 * - Infection curve chart
 * - Daily new cases chart
 * - Pandemic parameters
 */
export default function PandemicPage() {
  const { data, connected, toggleMode, startSim, stopSim, tickSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => {}} onStart={() => {}} onStop={() => {}} onTick={() => {}} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading pandemic data...</div></div>
        </main>
      </div>
    );
  }

  const mode = data.mode || {};
  const sir = data.sir;
  const pandemic = data.pandemic;
  const statistics = data.statistics || [];

  // Build daily new cases data
  const dailyCases = statistics
    .filter((s) => s.pandemic)
    .map((s) => ({
      day: s.day,
      "New Infections": s.pandemic.daily_new_infections || 0,
      "New Deaths": s.pandemic.daily_new_deaths || 0,
    }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload?.length) {
      return (
        <div style={{
          background: "rgba(14, 22, 40, 0.95)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          padding: "12px 16px",
          fontSize: "12px",
        }}>
          <p style={{ fontWeight: 700, marginBottom: 6 }}>Day {label}</p>
          {payload.map((p, i) => (
            <p key={i} style={{ color: p.color, marginBottom: 2 }}>
              {p.name}: <span style={{ fontWeight: 600 }}>{p.value}</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (!mode.is_pandemic) {
    return (
      <div className="app-layout">
        <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onStart={startSim} onStop={stopSim} onTick={tickSim} />
        <main className="main-content">
          <div className="page-header fade-in">
            <h2>Pandemic Response</h2>
            <p>Currently in Normal Operations mode</p>
          </div>
          <div className="empty-state">
            <div className="empty-state-icon">🦠</div>
            <h3>Pandemic Mode Not Active</h3>
            <p>Switch to Pandemic mode using the toggle in the sidebar to activate pandemic response monitoring and infection tracking.</p>
          </div>

          {/* Show historical data if available */}
          {statistics.some((s) => s.pandemic) && (
            <div style={{ marginTop: "40px" }}>
              <h3 style={{ fontSize: "16px", fontWeight: 700, color: "var(--text-primary)", marginBottom: "16px" }}>
                📜 Historical Pandemic Data
              </h3>
              <InfectionChart statistics={statistics} />
            </div>
          )}
        </main>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onStart={startSim} onStop={stopSim} onTick={tickSim} />
      <main className="main-content">
        <div className="page-header fade-in">
          <h2>🔴 Pandemic Response</h2>
          <p>Active pandemic monitoring — Day {data.day}</p>
        </div>

        {/* Health Compartment Summary Cards */}
        {sir && (
          <div className="sir-summary stagger-children">
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
          <div className="stats-grid stagger-children">
            <StatCard
              icon="📈"
              label="Total Infections"
              value={pandemic.total_infections}
              sub={`+${pandemic.daily_new_infections} today`}
              color="red"
            />
            <StatCard
              icon="💀"
              label="Total Deaths"
              value={pandemic.total_deaths}
              sub={`+${pandemic.daily_new_deaths} today`}
              color="purple"
            />
            <StatCard
              icon="📊"
              label="Infection Rate"
              value={`${(mode.infection_rate * 100).toFixed(0)}%`}
              sub="Base transmission probability"
              color="amber"
            />
            <StatCard
              icon="🏥"
              label="Surge Capacity"
              value={`${mode.surge_capacity_multiplier}x`}
              sub="Hospital bed multiplier"
              color="cyan"
            />
          </div>
        )}

        {/* Charts */}
        <div className="charts-grid">
          <InfectionChart statistics={statistics} />
          
          {/* Daily New Cases Chart */}
          <div className="chart-card" id="daily-cases-chart">
            <h3>📊 Daily New Cases</h3>
            {dailyCases.length > 0 ? (
              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={dailyCases}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                  <XAxis
                    dataKey="day"
                    tick={{ fill: "#5a6478", fontSize: 11 }}
                    axisLine={{ stroke: "rgba(255,255,255,0.06)" }}
                  />
                  <YAxis
                    tick={{ fill: "#5a6478", fontSize: 11 }}
                    axisLine={{ stroke: "rgba(255,255,255,0.06)" }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Line type="monotone" dataKey="New Infections" stroke="#ef4444" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="New Deaths" stroke="#6b7280" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state"><p>No daily data yet. Run the simulation to see daily case trends.</p></div>
            )}
          </div>
        </div>

        {/* Pandemic Parameters */}
        <div className="chart-card" style={{ marginTop: "24px" }}>
          <h3>⚙️ Active Pandemic Parameters</h3>
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "16px",
            marginTop: "16px",
          }}>
            {[
              { label: "Infection Rate", value: `${(mode.infection_rate * 100).toFixed(1)}%` },
              { label: "Surge Capacity", value: `${mode.surge_capacity_multiplier}x` },
            ].map((param) => (
              <div key={param.label} style={{
                padding: "12px 16px",
                background: "var(--bg-glass)",
                border: "1px solid var(--border-color)",
                borderRadius: "var(--radius-sm)",
              }}>
                <div style={{ fontSize: "11px", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  {param.label}
                </div>
                <div style={{ fontSize: "18px", fontWeight: 700, color: "var(--text-primary)", marginTop: "4px" }}>
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
