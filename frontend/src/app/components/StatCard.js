"use client";

/**
 * StatCard Component
 * 
 * Displays a KPI metric card with icon, label, value, and subtitle.
 * Includes a colored top accent bar and hover animations.
 * 
 * @param {string} icon - Emoji icon
 * @param {string} label - Metric label
 * @param {string|number} value - Main metric value
 * @param {string} sub - Subtitle text
 * @param {string} color - Color theme (blue, green, red, amber, purple, cyan)
 */
export default function StatCard({ icon, label, value, sub, color = "blue" }) {
  return (
    <div className={`stat-card ${color}`} id={`stat-${label?.toLowerCase().replace(/\s+/g, "-")}`}>
      <div className="stat-card-header">
        <div className={`stat-card-icon ${color}`}>{icon}</div>
        <span className="stat-card-label">{label}</span>
      </div>
      <div className="stat-card-value">{value ?? "—"}</div>
      <div className="stat-card-sub">{sub}</div>
    </div>
  );
}
