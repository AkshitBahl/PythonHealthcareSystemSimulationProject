"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Sidebar Navigation Component
 *
 * Renders the sidebar with:
 * - Logo/brand
 * - Navigation links with active states
 * - Mode toggle (Normal / Pandemic)
 * - Simulation controls (Step / Reset)
 * - Connection status indicator
 */
export default function Sidebar({ data, connected, onToggleMode, onReset, onTick }) {
  const pathname = usePathname();
  const day = data?.day || 0;
  const mode = data?.mode?.mode || "normal";

  const navLinks = [
    { href: "/", label: "Dashboard", icon: "D" },
    { href: "/hospitals", label: "Hospitals", icon: "H" },
    { href: "/patients", label: "Patients", icon: "P" },
    { href: "/pharmacy", label: "Pharmacy", icon: "Rx" },
    { href: "/pandemic", label: "Pandemic", icon: "V" },
  ];

  return (
    <aside className="sidebar" id="main-sidebar">
      {/* Logo */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">MS</div>
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
        <div className="nav-section-label" style={{ marginTop: "14px" }}>
          Simulation Mode
        </div>
        <div className="mode-toggle-wrapper">
          <div className="mode-toggle" onClick={onToggleMode} id="mode-toggle">
            <div className={`mode-option normal ${mode === "normal" ? "active" : ""}`}>
              Normal
            </div>
            <div className={`mode-option pandemic ${mode === "pandemic" ? "active" : ""}`}>
              Pandemic
            </div>
          </div>
        </div>
      </nav>

      {/* Simulation Controls */}
      <div className="sidebar-footer">
        <div className="sim-controls">
          <div className="day-badge">
            Day: <span>{day}</span>
          </div>
          <div className="sim-buttons">
            <button
              className="sim-btn reset"
              onClick={onReset}
              id="sim-reset"
              title="Reset simulation to Day 0"
            >
              Reset
            </button>
            <button
              className="sim-btn step"
              onClick={onTick}
              id="sim-step"
              title="Advance one day"
            >
              +1
            </button>
          </div>
          <div className="connection-status">
            <div className={`connection-dot ${connected ? "connected" : "disconnected"}`} />
            <span style={{ color: "var(--text-muted)", fontSize: "10px" }}>
              {connected ? "Connected" : "Reconnecting..."}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
