"use client";

import { useState, useEffect, useCallback } from "react";

/**
 * Custom hook for interacting with the backend simulation via REST.
 *
 * No polling — state is only fetched on mount and after user actions
 * (tick, reset, mode toggle).
 *
 * @returns {object} { data, connected, loading, toggleMode, tickSim, resetSim }
 */

const API_BASE = "http://localhost:8000/api";

export function useSimulation() {
  const [data, setData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchState = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/status`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setData(json);
      setConnected(true);
      setLoading(false);
    } catch (err) {
      console.error("[API] Failed to fetch state:", err);
      setConnected(false);
    }
  }, []);

  // Fetch initial state on mount (once)
  useEffect(() => {
    fetchState();
  }, [fetchState]);

  const tickSim = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/simulation/tick`, { method: "POST" });
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("[API] Tick failed:", err);
    }
  }, []);

  const resetSim = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/simulation/reset`, { method: "POST" });
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("[API] Reset failed:", err);
    }
  }, []);

  const toggleMode = useCallback(async () => {
    const currentMode = data?.mode?.mode || "normal";
    const newMode = currentMode === "normal" ? "pandemic" : "normal";
    try {
      await fetch(`${API_BASE}/mode`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: newMode }),
      });
      await fetchState();
    } catch (err) {
      console.error("[API] Mode switch failed:", err);
    }
  }, [data, fetchState]);

  return { data, connected, loading, toggleMode, tickSim, resetSim, refresh: fetchState };
}
