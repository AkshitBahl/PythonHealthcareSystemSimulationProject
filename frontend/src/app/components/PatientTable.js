"use client";

import { useState, useMemo } from "react";

/**
 * PatientTable Component
 * 
 * Renders a sortable, filterable table of all patients.
 * Shows name, age, gender, health status, immunity, treatments, and facility.
 * 
 * Health statuses: Healthy, Infected, Deceased (simplified 3-status model)
 * 
 * @param {Array} patients - Array of patient data objects
 * @param {Array} hospitals - Array of hospital data (for name lookup)
 */
export default function PatientTable({ patients = [], hospitals = [] }) {
  const [sortKey, setSortKey] = useState("name");
  const [sortDir, setSortDir] = useState("asc");
  const [filter, setFilter] = useState("All");

  // Hospital ID → name lookup
  const hospitalMap = useMemo(() => {
    const map = {};
    hospitals.forEach((h) => (map[h.id] = h.name));
    return map;
  }, [hospitals]);

  // Filter patients by status
  const filtered = useMemo(() => {
    if (filter === "All") return patients;
    if (filter === "Admitted") return patients.filter((p) => p.admitted);
    if (filter === "Infected & Unadmitted")
      return patients.filter(
        (p) => p.health_status === "Infected" && !p.admitted
      );
    return patients.filter((p) => p.health_status === filter);
  }, [patients, filter]);

  // Sort patients
  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      let av = a[sortKey];
      let bv = b[sortKey];
      if (typeof av === "string") av = av.toLowerCase();
      if (typeof bv === "string") bv = bv.toLowerCase();
      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
  }, [filtered, sortKey, sortDir]);

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const statuses = ["All", "Healthy", "Infected", "Infected & Unadmitted", "Deceased"];

  const getStatusClass = (status) => status?.toLowerCase() || "";

  return (
    <div className="data-table-wrapper" id="patient-table">
      <div className="data-table-header">
        <h3>Patient Registry</h3>
        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
          {/* Status filter */}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            style={{
              background: "var(--bg-glass)",
              border: "1px solid var(--border-color)",
              borderRadius: "var(--radius-sm)",
              color: "var(--text-secondary)",
              padding: "6px 10px",
              fontSize: "12px",
              cursor: "pointer",
              outline: "none",
            }}
            id="patient-filter"
          >
            {statuses.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
          <span className="count">{sorted.length} patients</span>
        </div>
      </div>
      <div style={{ maxHeight: "520px", overflowY: "auto" }}>
        <table className="data-table">
          <thead>
            <tr>
              {[
                { key: "name", label: "Name" },
                { key: "age", label: "Age" },
                { key: "gender", label: "Gender" },
                { key: "health_status", label: "Status" },
                { key: "immunity", label: "Immunity" },
                { key: "treatments_received", label: "Treatments" },
                { key: "admitted", label: "Facility" },
              ].map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  style={{ cursor: "pointer", userSelect: "none" }}
                >
                  {col.label} {sortKey === col.key ? (sortDir === "asc" ? "↑" : "↓") : ""}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((p) => (
              <tr key={p.id}>
                <td style={{ color: "var(--text-primary)", fontWeight: 500 }}>{p.name}</td>
                <td>{p.age}</td>
                <td>{p.gender}</td>
                <td>
                  <span className={`status-badge ${getStatusClass(p.health_status)}`}>
                    {p.health_status}
                  </span>
                </td>
                <td>
                  <span style={{
                    color: p.immunity >= 0.5 ? "var(--green)" :
                      p.immunity >= 0.3 ? "var(--amber)" : "var(--red)",
                    fontWeight: 600,
                  }}>
                    {Math.round(p.immunity * 100)}%
                  </span>
                </td>
                <td>
                  {p.health_status === "Infected" && p.treatments_received > 0 ? (
                    <span className="status-badge infected">
                      {p.treatments_received} / 4
                    </span>
                  ) : p.health_status === "Infected" ? (
                    <span style={{ color: "var(--text-muted)" }}>Awaiting</span>
                  ) : (
                    <span style={{ color: "var(--text-muted)" }}>—</span>
                  )}
                </td>
                <td>
                  {p.admitted ? (
                    <span className="status-badge admitted">
                      {hospitalMap[p.assigned_facility]?.split(" ").slice(0, 2).join(" ") || "Hospital"}
                    </span>
                  ) : (
                    <span style={{ color: "var(--text-muted)" }}>—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
