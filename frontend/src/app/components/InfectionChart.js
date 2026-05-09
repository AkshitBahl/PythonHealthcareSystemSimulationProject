"use client";

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";

/**
 * InfectionChart Component
 * 
 * Renders an area chart showing Healthy-Infected-Deceased curves
 * over time during pandemic mode.
 * 
 * Simplified model: no Susceptible/Recovered — only 3 compartments.
 * 
 * @param {Array} statistics - Array of daily statistic records
 */
export default function InfectionChart({ statistics = [] }) {
  // Extract pandemic data from statistics
  const chartData = statistics
    .filter((s) => s.pandemic?.sir)
    .map((s) => ({
      day: s.day,
      Healthy: s.pandemic.sir.healthy,
      Infected: s.pandemic.sir.infected,
      Deceased: s.pandemic.sir.deceased,
    }));

  if (chartData.length === 0) {
    return (
      <div className="chart-card" id="infection-chart">
        <h3>🦠 Infection Curves</h3>
        <div className="empty-state">
          <div className="empty-state-icon">📈</div>
          <h3>No pandemic data</h3>
          <p>Switch to Pandemic mode and run the simulation to see infection curves.</p>
        </div>
      </div>
    );
  }

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

  return (
    <div className="chart-card" id="infection-chart">
      <h3>🦠 Infection Curves</h3>
      <ResponsiveContainer width="100%" height={320}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorHealthy" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorInfected" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorDeceased" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6b7280" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6b7280" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
          <XAxis
            dataKey="day"
            tick={{ fill: "#5a6478", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.06)" }}
            label={{ value: "Day", position: "insideBottomRight", offset: -5, fill: "#5a6478" }}
          />
          <YAxis
            tick={{ fill: "#5a6478", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.06)" }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: "12px", paddingTop: "8px" }}
          />
          <Area
            type="monotone" dataKey="Healthy" stroke="#10b981"
            fillOpacity={1} fill="url(#colorHealthy)" strokeWidth={2}
          />
          <Area
            type="monotone" dataKey="Infected" stroke="#ef4444"
            fillOpacity={1} fill="url(#colorInfected)" strokeWidth={2}
          />
          <Area
            type="monotone" dataKey="Deceased" stroke="#6b7280"
            fillOpacity={1} fill="url(#colorDeceased)" strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
