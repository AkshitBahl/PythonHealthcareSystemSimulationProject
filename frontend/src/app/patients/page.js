"use client";

import Sidebar from "../components/Sidebar";
import PatientTable from "../components/PatientTable";
import StatCard from "../components/StatCard";
import { useSimulation } from "../hooks/useSimulation";

/**
 * Patients Page
 * 
 * Full patient registry with filtering, sorting, and status overview stats.
 */
export default function PatientsPage() {
  const { data, connected, toggleMode, startSim, stopSim, tickSim } = useSimulation();

  if (!data) {
    return (
      <div className="app-layout">
        <Sidebar data={null} connected={connected} onToggleMode={() => {}} onStart={() => {}} onStop={() => {}} onTick={() => {}} />
        <main className="main-content">
          <div className="loading-container"><div className="loading-spinner" /><div className="loading-text">Loading patients...</div></div>
        </main>
      </div>
    );
  }

  const patients = data.patients || [];
  const hospitals = data.hospitals || [];

  // Count per-status
  const counts = {};
  patients.forEach((p) => {
    counts[p.health_status] = (counts[p.health_status] || 0) + 1;
  });
  const infectedCount = patients.filter((p) => p.infected).length;
  const admittedCount = patients.filter((p) => p.admitted).length;
  const avgImmunity = patients.length
    ? Math.round((patients.reduce((s, p) => s + p.immunity, 0) / patients.length) * 100)
    : 0;

  return (
    <div className="app-layout">
      <Sidebar data={data} connected={connected} onToggleMode={toggleMode} onStart={startSim} onStop={stopSim} onTick={tickSim} />
      <main className="main-content">
        <div className="page-header fade-in">
          <h2>Patients</h2>
          <p>Complete patient registry with health status tracking — Day {data.day}</p>
        </div>

        {/* Summary Stats */}
        <div className="stats-grid stagger-children">
          <StatCard icon="💚" label="Healthy" value={counts.Healthy || 0} sub="No conditions" color="green" />
          <StatCard icon="🤒" label="Mild" value={counts.Mild || 0} sub="Outpatient care" color="amber" />
          <StatCard icon="🏥" label="Severe" value={counts.Severe || 0} sub="Hospitalized" color="red" />
          <StatCard icon="🚨" label="Critical" value={counts.Critical || 0} sub="ICU required" color="red" />
          <StatCard icon="💙" label="Recovered" value={counts.Recovered || 0} sub="Post-illness" color="blue" />
          <StatCard icon="🛡️" label="Avg Immunity" value={`${avgImmunity}%`} sub={`${infectedCount} infected · ${admittedCount} admitted`} color="purple" />
        </div>

        {/* Patient Table */}
        <PatientTable patients={patients} hospitals={hospitals} />
      </main>
    </div>
  );
}
