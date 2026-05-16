"use client";

import Sidebar from "../components/Sidebar";
import BedChart from "../components/BedChart";
import { useSimulation } from "../hooks/useSimulation";

/**
 * Hospitals Page
 *
 * Detailed view of each hospital showing:
 * - Per-hospital stats (beds, ICU, ventilators)
 * - Occupancy bars
 * - Assigned doctors
 */
export default function HospitalsPage() {
  const { data, connected, toggleMode, tickSim, resetSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => {}} onReset={() => {}} onTick={() => {}} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading hospitals...</div></div>
        </main>
      </div>
    );
  }

  const hospitals = data.hospitals || [];
  const doctors = data.doctors || [];

  const getOccupancyClass = (rate) => {
    if (rate >= 80) return "danger";
    if (rate >= 60) return "warning";
    return "";
  };

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onReset={resetSim} onTick={tickSim} />
      <main className="main-content">
        <div className="page-header fade-in">
          <h2>Hospitals</h2>
          <p>Hospital capacity, bed occupancy, and staff assignments — Day {data.day}</p>
        </div>

        {/* Bed Chart */}
        <div style={{ marginBottom: "28px" }}>
          <BedChart hospitals={hospitals} />
        </div>

        {/* Hospital Cards */}
        <div className="hospitals-grid">
          {hospitals.map((h) => {
            const hospitalDocs = doctors.filter((d) => d.assigned_facility === h.id);

            return (
              <div className="hospital-card" key={h.id} id={`hospital-${h.id}`}>
                <div className="hospital-card-header">
                  <div>
                    <h3>{h.name}</h3>
                    <div className="location">{h.location}</div>
                  </div>
                  <span className={`status-badge ${h.occupancy_rate >= 80 ? "critical" : h.occupancy_rate >= 50 ? "mild" : "healthy"}`}>
                    {h.occupancy_rate}%
                  </span>
                </div>

                {/* Stats Grid */}
                <div className="hospital-stats">
                  <div className="hospital-stat">
                    <div className="hospital-stat-value">{h.total_beds}</div>
                    <div className="hospital-stat-label">Beds</div>
                  </div>
                  <div className="hospital-stat">
                    <div className="hospital-stat-value">{h.icu_beds}</div>
                    <div className="hospital-stat-label">ICU</div>
                  </div>
                  <div className="hospital-stat">
                    <div className="hospital-stat-value">{h.ventilators}</div>
                    <div className="hospital-stat-label">Ventilators</div>
                  </div>
                </div>

                {/* General Bed Occupancy */}
                <div className="occupancy-bar-wrapper">
                  <div className="occupancy-bar-label">
                    <span>General Beds</span>
                    <span>{h.occupied_beds} / {h.total_beds}</span>
                  </div>
                  <div className="occupancy-bar">
                    <div
                      className={`occupancy-bar-fill ${getOccupancyClass(
                        h.total_beds > 0 ? (h.occupied_beds / h.total_beds) * 100 : 0
                      )}`}
                      style={{
                        width: `${h.total_beds > 0 ? (h.occupied_beds / h.total_beds) * 100 : 0}%`,
                      }}
                    />
                  </div>
                </div>

                {/* ICU Bed Occupancy */}
                <div className="occupancy-bar-wrapper">
                  <div className="occupancy-bar-label">
                    <span>ICU Beds</span>
                    <span>{h.occupied_icu} / {h.icu_beds}</span>
                  </div>
                  <div className="occupancy-bar">
                    <div
                      className={`occupancy-bar-fill ${getOccupancyClass(
                        h.icu_beds > 0 ? (h.occupied_icu / h.icu_beds) * 100 : 0
                      )}`}
                      style={{
                        width: `${h.icu_beds > 0 ? (h.occupied_icu / h.icu_beds) * 100 : 0}%`,
                      }}
                    />
                  </div>
                </div>

                {/* Assigned Doctors */}
                <div style={{ marginTop: "14px" }}>
                  <div style={{ fontSize: "10px", color: "var(--text-muted)", marginBottom: "6px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>
                    Assigned Doctors ({hospitalDocs.length})
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                    {hospitalDocs.map((d) => (
                      <span
                        key={d.id}
                        style={{
                          fontSize: "10px",
                          padding: "3px 7px",
                          background: "var(--bg-glass)",
                          border: "1px solid var(--border-color)",
                          borderRadius: "var(--radius-full)",
                          color: "var(--text-secondary)",
                        }}
                      >
                        {d.name}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}
