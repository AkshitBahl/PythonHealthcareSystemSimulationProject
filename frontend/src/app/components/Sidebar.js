"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Sidebar Navigation Component
 * 
 * Renders the glassmorphic sidebar with:
 * - Logo/brand
 * - Navigation links with active states
 * - Mode toggle (Normal ↔ Pandemic)
 * - Simulation controls (Play/Pause/Step)
 * - Connection status indicator
 */
export default function Sidebar({ data, connected, onToggleMode, onStart, onStop, onTick }) {
  const pathname = usePathname();
  const day = data?.day || 0;
  const mode = data?.mode?.mode || "normal";
  const running = data?.running || false;

  const navLinks = [
    { href: "/", label: "Dashboard", icon: "📊" },
    { href: "/hospitals", label: "Hospitals", icon: "🏥" },
    { href: "/patients", label: "Patients", icon: "👥" },
    { href: "/pharmacy", label: "Pharmacy", icon: "💊" },
    { href: "/pandemic", label: "Pandemic", icon: "🦠" },
  ];

  return (
    <aside className="sidebar" id="main-sidebar">
      {/* Logo */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">🏥</div>
          <div className="sidebar-logo-text">
            <h1>MedSync</h1>
            <span>Healthcare Simulator</span>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="nav-section-label">Navigation</div>
        {navLinks.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`nav-link ${pathname === link.href ? "active" : ""}`}
            id={`nav-${link.label.toLowerCase()}`}
          >
            <span className="nav-icon">{link.icon}</span>
            <span>{link.label}</span>
          </Link>
        ))}

        {/* Mode Toggle */}
        <div className="nav-section-label" style={{ marginTop: "16px" }}>
          Simulation Mode
        </div>
        <div className="mode-toggle-wrapper">
          <div className="mode-toggle" onClick={onToggleMode} id="mode-toggle">
            <div className={`mode-option normal ${mode === "normal" ? "active" : ""}`}>
              🟢 Normal
            </div>
            <div className={`mode-option pandemic ${mode === "pandemic" ? "active" : ""}`}>
              🔴 Pandemic
            </div>
          </div>
        </div>
      </nav>

      {/* Simulation Controls */}
      <div className="sidebar-footer">
        <div className="sim-controls">
          <div className="day-badge">
            📅 Day: <span>{day}</span>
          </div>
          <div className="sim-buttons">
            <button
              className={`sim-btn ${running ? "active" : ""}`}
              onClick={running ? onStop : onStart}
              id="sim-play-pause"
            >
              {running ? "⏸ Pause" : "▶ Play"}
            </button>
            <button
              className="sim-btn step"
              onClick={onTick}
              disabled={running}
              id="sim-step"
              title="Advance one day"
            >
              ⏭
            </button>
          </div>
          <div className="connection-status">
            <div className={`connection-dot ${connected ? "connected" : "disconnected"}`} />
            <span style={{ color: "var(--text-muted)", fontSize: "11px" }}>
              {connected ? "Connected" : "Reconnecting..."}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
