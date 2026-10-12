import { useCallback, useEffect, useMemo, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

async function getJson(path) {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  return response.json();
}

function formatTime(value) {
  if (!value) return "—";
  return new Intl.DateTimeFormat(undefined, { hour: "2-digit", minute: "2-digit" }).format(new Date(value));
}

function severityClass(severity = "low") {
  return `badge badge-${severity.toLowerCase()}`;
}

function App() {
  const [incidents, setIncidents] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [demoRunning, setDemoRunning] = useState(false);

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [incidentData, metricData] = await Promise.all([
        getJson("/incidents"),
        getJson("/telemetry/metrics"),
      ]);
      setIncidents(incidentData.incidents || []);
      setMetrics(metricData.metrics || []);
    } catch (requestError) {
      setError(`${requestError.message}. Is the backend running on port 8000?`);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
    const refreshTimer = window.setInterval(loadDashboard, 5000);
    return () => window.clearInterval(refreshTimer);
  }, [loadDashboard]);

  async function runFailureDemo() {
    setDemoRunning(true);
    setError("");
    try {
      for (const metric of [
        { name: "error_rate", service: "demo-payment-service", value: 31 },
        { name: "db_connections", service: "demo-payment-service", value: 100 },
      ]) {
        const response = await fetch(`${API_URL}/telemetry/metrics`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(metric),
        });
        if (!response.ok) throw new Error(`Demo request failed (${response.status})`);
      }
      await loadDashboard();
    } catch (requestError) {
      setError(`${requestError.message}. Is the backend running on port 8000?`);
    } finally {
      setDemoRunning(false);
    }
  }

  const openIncidents = useMemo(() => incidents.filter((incident) => incident.status !== "resolved").length, [incidents]);
  const criticalCount = useMemo(() => incidents.filter((incident) => ["critical", "high"].includes(incident.severity)).length, [incidents]);
  const latestMetrics = metrics.slice(-4).reverse();

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark">⌁</span><span>LiveOps <em>Agent</em></span></div>
        <div className="topbar-actions"><span className="live-dot" /> API connected to <code>localhost:8000</code><button className="icon-button" onClick={loadDashboard} aria-label="Refresh dashboard">↻</button></div>
      </header>

      <section className="hero">
        <div><p className="eyebrow">Operations command center</p><h1>Good morning, operator.</h1><p className="subhead">A focused view of your production health and active incidents.</p></div>
        <div className="hero-actions"><div className="hero-status"><span className="pulse" /> {openIncidents ? "Incidents detected" : "Systems nominal"}</div><button className="demo-button" onClick={runFailureDemo} disabled={demoRunning}>{demoRunning ? "Running demo…" : "Run failure demo"}</button></div>
      </section>

      {error && <div className="error-banner"><strong>Backend unavailable</strong><span>{error}</span></div>}

      <section className="stat-grid">
        <article className="stat-card"><span className="stat-label">Open incidents</span><strong>{loading ? "—" : openIncidents}</strong><span className="stat-note">Requires attention</span></article>
        <article className="stat-card accent"><span className="stat-label">High priority</span><strong>{loading ? "—" : criticalCount}</strong><span className="stat-note">High or critical severity</span></article>
        <article className="stat-card"><span className="stat-label">Telemetry points</span><strong>{loading ? "—" : metrics.length}</strong><span className="stat-note">Collected by the agent</span></article>
      </section>

      <section className="content-grid">
        <article className="panel incidents-panel">
          <div className="panel-heading"><div><p className="eyebrow">Live feed</p><h2>Active incidents</h2></div><span className="count-pill">{incidents.length}</span></div>
          {loading ? <div className="empty-state">Loading incident feed…</div> : incidents.length === 0 ? <div className="empty-state"><span className="empty-icon">✓</span><strong>No active incidents</strong><span>Your services are looking healthy.</span></div> : <div className="incident-list">{incidents.slice(0, 6).map((incident) => <div className="incident-row" key={incident.id}><div className={`severity-bar ${incident.severity}`} /><div className="incident-main"><div className="incident-title"><strong>{incident.service}</strong><span className={severityClass(incident.severity)}>{incident.severity}</span></div><p>{incident.message}</p><span className="incident-meta">{incident.type} · detected {formatTime(incident.detected_at)}</span></div><span className={`status status-${incident.status}`}>{incident.status}</span></div>)}</div>}
        </article>

        <article className="panel metrics-panel"><div className="panel-heading"><div><p className="eyebrow">Signals</p><h2>Recent telemetry</h2></div><span className="live-label">● LIVE</span></div>{latestMetrics.length === 0 ? <div className="empty-state compact">No metrics collected yet.</div> : <div className="metric-list">{latestMetrics.map((metric, index) => <div className="metric-row" key={metric.id || `${metric.name}-${index}`}><div className="metric-info"><strong>{metric.name.replaceAll("_", " ")}</strong><span>{metric.service}</span></div><strong className="metric-value">{metric.value}</strong><div className="metric-track"><i style={{ width: `${Math.min(Number(metric.value) || 0, 100)}%` }} /></div></div>)}</div>}</article>
      </section>

      <footer><span>LiveOps Agent <span className="muted">v0.1.0</span></span><span>Auto-refreshes every 5s · <button className="text-button" onClick={loadDashboard}>Refresh now</button></span></footer>
    </main>
  );
}

export default App;
