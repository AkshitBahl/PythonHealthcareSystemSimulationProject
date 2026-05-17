"use client";

import Sidebar from "../components/Sidebar";
import { useSimulation } from "../hooks/useSimulation";

/**
 * Hospitals Page
 *
 * Simple per-hospital cards showing total beds, available beds,
 * and the percentage of beds currently free.
 */
export default function HospitalsPage() {
  const { data, connected, toggleMode, tickSim, resetSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => { }} onReset={() => { }} onTick={() => { }} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading hospitals...</div></div>
        </main>
      </div>
    );
  }

  const hospitals = data.hospitals || [];

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onReset={resetSim} onTick={tickSim} />
      <main className="main-content">
        <div className="page-header fade-in">
          <h2>Hospitals</h2>
          <p>Hospital bed capacity and availability — Day {data.day}</p>
        </div>

        {/* Hospital Cards */}
        <div className="hospitals-grid">
          {hospitals.map((h) => {
            const availablePct = h.total_beds > 0
              ? Math.round((h.available_beds / h.total_beds) * 100)
              : 0;
            const availClass =
              availablePct >= 50 ? "healthy" : availablePct >= 20 ? "mild" : "critical";

            return (
              <div className="hospital-card" key={h.id} id={`hospital-${h.id}`}>
                <div className="hospital-card-header">
                  <div>
                    <h3>{h.name}</h3>
                    <div className="location">{h.location}</div>
                  </div>
                  <span className={`status-badge ${availClass}`}>
                    {availablePct}% free
                  </span>
                </div>

                {/* Stats */}
                <div
                  className="hospital-stats"
                  style={{ gridTemplateColumns: "1fr 1fr", marginBottom: 0 }}
                >
                  <div className="hospital-stat">
                    <div className="hospital-stat-value">{h.total_beds}</div>
                    <div className="hospital-stat-label">Total Beds</div>
                  </div>
                  <div className="hospital-stat">
                    <div className="hospital-stat-value">{h.available_beds}</div>
                    <div className="hospital-stat-label">Available Beds</div>
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
