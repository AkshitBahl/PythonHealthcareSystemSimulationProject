"use client";

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from "recharts";

/**
 * BedChart Component
 * 
 * Renders a bar chart showing bed occupancy per hospital.
 * Bars are colored based on occupancy level (green/amber/red).
 * 
 * @param {Array} hospitals - Array of hospital data objects
 */
export default function BedChart({ hospitals = [] }) {
  if (!hospitals.length) {
    return (
      <div className="chart-card">
        <h3>🛏️ Bed Occupancy</h3>
        <div className="empty-state">
          <p>No hospital data available</p>
        </div>
      </div>
    );
  }

  const chartData = hospitals.map((h) => ({
    name: h.name?.split(" ").slice(0, 2).join(" ") || "Hospital",
    occupied: h.occupied_beds + (h.occupied_icu || 0),
    total: h.total_beds + (h.icu_beds || 0),
    rate: h.occupancy_rate || 0,
  }));

  const getBarColor = (rate) => {
    if (rate >= 80) return "#ef4444";
    if (rate >= 60) return "#f59e0b";
    return "#10b981";
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload?.length) {
      const d = payload[0].payload;
      return (
        <div style={{
          background: "rgba(14, 22, 40, 0.95)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          padding: "12px 16px",
          fontSize: "12px",
        }}>
          <p style={{ fontWeight: 700, marginBottom: 4 }}>{d.name}</p>
          <p style={{ color: "#8892a8" }}>
            Occupied: <span style={{ color: "#e8ecf4" }}>{d.occupied} / {d.total}</span>
          </p>
          <p style={{ color: "#8892a8" }}>
            Rate: <span style={{ color: getBarColor(d.rate) }}>{d.rate}%</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-card" id="bed-occupancy-chart">
      <h3>🛏️ Bed Occupancy by Hospital</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} barCategoryGap="20%">
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
          <XAxis
            dataKey="name"
            tick={{ fill: "#5a6478", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.06)" }}
          />
          <YAxis
            tick={{ fill: "#5a6478", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.06)" }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="occupied" radius={[6, 6, 0, 0]} maxBarSize={50}>
            {chartData.map((entry, i) => (
              <Cell key={i} fill={getBarColor(entry.rate)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
