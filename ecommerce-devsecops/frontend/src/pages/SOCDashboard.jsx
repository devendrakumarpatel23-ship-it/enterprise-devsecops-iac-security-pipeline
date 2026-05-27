import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './SOCDashboard.css';

const SOCDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [threatScore, setThreatScore] = useState(0);
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [threatIntel, setThreatIntel] = useState(null);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [liveFeed, setLiveFeed] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [mitreCoverage, setMitreCoverage] = useState(null);

  // Fetch SOC dashboard data
  const fetchDashboardData = useCallback(async () => {
    try {
      const [dashRes, threatRes, alertsRes, incidentsRes, intelRes, mitreRes] = await Promise.all([
        axios.get('/api/soc/dashboard'),
        axios.get('/api/soc/threat-score'),
        axios.get('/api/soc/alerts?limit=20'),
        axios.get('/api/soc/incidents?limit=50'),
        axios.get('/api/soc/threat-intelligence'),
        axios.get('/api/soc/mitre-coverage'),
      ]);

      setDashboardData(dashRes.data.data);
      setThreatScore(threatRes.data);
      setAlerts(alertsRes.data.alerts || []);
      setIncidents(incidentsRes.data.incidents || []);
      setThreatIntel(intelRes.data.intelligence);
      setMitreCoverage(mitreRes.data.coverage);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching SOC data:', error);
      setLoading(false);
    }
  }, []);

  // Fetch live feed updates
  const fetchLiveFeed = useCallback(async () => {
    try {
      const res = await axios.get('/api/soc/live-feed');
      setLiveFeed(res.data.feed.recent_activity);
    } catch (error) {
      console.error('Error fetching live feed:', error);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchDashboardData();
    fetchLiveFeed();

    // Set up auto-refresh intervals
    const dashboardInterval = setInterval(fetchDashboardData, 5000); // Every 5 seconds
    const feedInterval = setInterval(fetchLiveFeed, 3000); // Every 3 seconds

    return () => {
      clearInterval(dashboardInterval);
      clearInterval(feedInterval);
    };
  }, [fetchDashboardData, fetchLiveFeed]);

  if (loading) {
    return (
      <div className="soc-loading">
        <div className="soc-spinner"></div>
        <p>Loading SOC War Room...</p>
      </div>
    );
  }

  return (
    <div className="soc-dashboard">
      {/* Header */}
      <div className="soc-header">
        <div className="soc-title">
          <h1>🛡️ SECURITY OPERATIONS CENTER (SOC) WAR ROOM</h1>
          <p className="soc-subtitle">Enterprise Cyber Defense & Incident Response Platform</p>
        </div>
        <div className="soc-header-stats">
          <div className="header-stat critical">
            <span className="stat-value">{alerts.filter(a => a.severity === 'CRITICAL').length}</span>
            <span className="stat-label">CRITICAL ALERTS</span>
          </div>
          <div className="header-stat">
            <span className="stat-value">{incidents.filter(i => i.status !== 'resolved').length}</span>
            <span className="stat-label">OPEN INCIDENTS</span>
          </div>
          <div className="header-stat">
            <span className="stat-value">{dashboardData?.active_alerts || 0}</span>
            <span className="stat-label">TOTAL ALERTS</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="soc-tabs">
        <button
          className={`soc-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 OVERVIEW
        </button>
        <button
          className={`soc-tab ${activeTab === 'incidents' ? 'active' : ''}`}
          onClick={() => setActiveTab('incidents')}
        >
          🚨 INCIDENT QUEUE
        </button>
        <button
          className={`soc-tab ${activeTab === 'alerts' ? 'active' : ''}`}
          onClick={() => setActiveTab('alerts')}
        >
          ⚠️ ALERTS
        </button>
        <button
          className={`soc-tab ${activeTab === 'intelligence' ? 'active' : ''}`}
          onClick={() => setActiveTab('intelligence')}
        >
          🤖 THREAT INTELLIGENCE
        </button>
      </div>

      {/* Main Content */}
      <div className="soc-content">
        {activeTab === 'overview' && (
          <div className="soc-overview">
            {/* Threat Scorecard */}
            <div className="soc-grid-2">
              <div className="soc-card threat-scorecard">
                <h3>🔴 THREAT SCORE</h3>
                <div className="threat-gauge">
                  <div
                    className="threat-meter"
                    style={{
                      width: `${threatScore.threat_score}%`,
                      backgroundColor: getThreatColor(threatScore.threat_score),
                    }}
                  >
                    <span className="threat-percentage">{Math.round(threatScore.threat_score)}%</span>
                  </div>
                </div>
                <p className="threat-level">{threatScore.risk_level}</p>
                <p className="threat-trend">Trend: {threatScore.trend.toUpperCase()}</p>
              </div>

              <div className="soc-card security-posture">
                <h3>🛡️ SECURITY POSTURE</h3>
                <div className="posture-gauge">
                  <svg viewBox="0 0 200 200" className="gauge-svg">
                    <circle cx="100" cy="100" r="90" className="gauge-background" />
                    <circle
                      cx="100"
                      cy="100"
                      r="90"
                      className="gauge-foreground"
                      style={{
                        strokeDasharray: `${(threatScore.security_posture / 100) * 565} 565`,
                      }}
                    />
                    <text x="100" y="110" className="gauge-text">
                      {Math.round(threatScore.security_posture)}%
                    </text>
                  </svg>
                </div>
              </div>
            </div>

            {/* Key Metrics */}
            <div className="soc-metrics-grid">
              <div className="soc-metric-card">
                <div className="metric-icon">🎯</div>
                <div className="metric-info">
                  <h4>Critical Incidents</h4>
                  <p className="metric-value">{incidents.filter(i => i.severity === 'CRITICAL').length}</p>
                </div>
              </div>
              <div className="soc-metric-card">
                <div className="metric-icon">📡</div>
                <div className="metric-info">
                  <h4>Active Threats</h4>
                  <p className="metric-value">{dashboardData?.active_threats?.length || 0}</p>
                </div>
              </div>
              <div className="soc-metric-card">
                <div className="metric-icon">🔍</div>
                <div className="metric-info">
                  <h4>Security Events</h4>
                  <p className="metric-value">{dashboardData?.recent_events?.length || 0}</p>
                </div>
              </div>
              <div className="soc-metric-card">
                <div className="metric-icon">🗺️</div>
                <div className="metric-info">
                  <h4>MITRE ATT&CK</h4>
                  <p className="metric-value">{mitreCoverage?.covered_tactics || 0} Tactics</p>
                </div>
              </div>
            </div>

            {/* Live Feed */}
            <div className="soc-live-section">
              <h3>📡 LIVE SECURITY FEED</h3>
              <div className="live-feed-container">
                {liveFeed && liveFeed.length > 0 ? (
                  liveFeed.map((event, idx) => (
                    <div key={idx} className={`live-event severity-${event.severity.toLowerCase()}`}>
                      <span className="event-type-badge">{event.type}</span>
                      <span className="event-message">{event.message}</span>
                      <span className="event-time">{new Date(event.timestamp).toLocaleTimeString()}</span>
                    </div>
                  ))
                ) : (
                  <p className="no-data">No recent activity</p>
                )}
              </div>
            </div>

            {/* MITRE ATT&CK Coverage */}
            {mitreCoverage && (
              <div className="soc-card mitre-card">
                <h3>🎯 MITRE ATT&CK COVERAGE</h3>
                <div className="mitre-coverage-bar">
                  <div
                    className="mitre-coverage-fill"
                    style={{ width: `${mitreCoverage.coverage_percentage}%` }}
                  >
                    <span>{Math.round(mitreCoverage.coverage_percentage)}%</span>
                  </div>
                </div>
                <p className="mitre-info">
                  {mitreCoverage.covered_tactics} of {mitreCoverage.total_tactics} tactics covered
                </p>
                {mitreCoverage.tactics && (
                  <div className="mitre-tactics">
                    {mitreCoverage.tactics.slice(0, 6).map((tactic, idx) => (
                      <span key={idx} className="mitre-tactic-badge">
                        {tactic}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'incidents' && (
          <div className="soc-incidents-panel">
            <h3>🚨 INCIDENT RESPONSE QUEUE</h3>
            {incidents.length > 0 ? (
              <div className="incidents-list">
                {incidents.map((incident) => (
                  <div
                    key={incident.incident_id}
                    className={`incident-card severity-${incident.severity.toLowerCase()}`}
                    onClick={() => setSelectedIncident(incident)}
                  >
                    <div className="incident-header">
                      <span className="incident-id">{incident.incident_id.substring(0, 8)}</span>
                      <span className={`incident-status status-${incident.status.toLowerCase()}`}>
                        {incident.status}
                      </span>
                    </div>
                    <h4>{incident.title}</h4>
                    <p className="incident-description">{incident.description}</p>
                    <div className="incident-details">
                      <span className="detail">Attack: {incident.attack_type}</span>
                      <span className="detail">Analyst: {incident.assigned_analyst}</span>
                      <span className="detail">Systems: {incident.affected_systems.length}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No incidents currently</p>
            )}

            {selectedIncident && (
              <div className="incident-detail-panel">
                <h4>Incident Details</h4>
                <div className="detail-content">
                  <p><strong>ID:</strong> {selectedIncident.incident_id}</p>
                  <p><strong>Status:</strong> {selectedIncident.status}</p>
                  <p><strong>Severity:</strong> {selectedIncident.severity}</p>
                  <p><strong>Attack Type:</strong> {selectedIncident.attack_type}</p>
                  <p><strong>Affected Systems:</strong> {selectedIncident.affected_systems.join(', ')}</p>
                  <p><strong>Affected Users:</strong> {selectedIncident.affected_users.join(', ')}</p>
                  {selectedIncident.impact_assessment && (
                    <>
                      <h5>Impact Assessment:</h5>
                      <p><strong>Estimated Impact:</strong> {selectedIncident.impact_assessment.estimated_impact}</p>
                      <p><strong>Systems Affected:</strong> {selectedIncident.impact_assessment.systems_affected}</p>
                    </>
                  )}
                  <h5>Remediation Actions:</h5>
                  {selectedIncident.remediation_actions.length > 0 ? (
                    <ul>
                      {selectedIncident.remediation_actions.map((action, idx) => (
                        <li key={idx}>{action}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>No remediation actions yet</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'alerts' && (
          <div className="soc-alerts-panel">
            <h3>⚠️ SECURITY ALERTS</h3>
            {alerts.length > 0 ? (
              <div className="alerts-list">
                {alerts.map((alert) => (
                  <div
                    key={alert.alert_id}
                    className={`alert-card severity-${alert.severity.toLowerCase()}`}
                  >
                    <div className="alert-header">
                      <h4>{alert.title}</h4>
                      <span className="alert-severity-badge">{alert.severity}</span>
                    </div>
                    <p>{alert.description}</p>
                    <div className="alert-details">
                      <span>🎯 {alert.attack_type}</span>
                      <span>📍 {alert.source_ips[0]}</span>
                      <span>🎪 {alert.event_count} events</span>
                      <span>📊 {(alert.confidence_score * 100).toFixed(1)}% confidence</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No alerts currently</p>
            )}
          </div>
        )}

        {activeTab === 'intelligence' && threatIntel && (
          <div className="soc-intelligence-panel">
            <h3>🤖 THREAT INTELLIGENCE & PREDICTIONS</h3>
            
            <div className="intelligence-grid">
              <div className="intelligence-card">
                <h4>📈 Threat Landscape</h4>
                <div className="intelligence-stat">
                  <span className="label">Known Threats:</span>
                  <span className="value">{threatIntel.threat_landscape.known_threats}</span>
                </div>
                <div className="intelligence-stat">
                  <span className="label">Active Campaigns:</span>
                  <span className="value">{threatIntel.threat_landscape.active_campaigns}</span>
                </div>
                <div className="intelligence-stat">
                  <span className="label">New This Month:</span>
                  <span className="value">{threatIntel.threat_landscape.new_threats_this_month}</span>
                </div>
              </div>

              <div className="intelligence-card">
                <h4>🔝 Top TTPs</h4>
                {threatIntel.top_ttps && threatIntel.top_ttps.map((ttp, idx) => (
                  <div key={idx} className="ttp-item">
                    <span className="ttp-code">{ttp.ttp}</span>
                    <span className="ttp-name">{ttp.name}</span>
                    <span className="ttp-freq">{ttp.frequency}%</span>
                  </div>
                ))}
              </div>

              <div className="intelligence-card">
                <h4>💡 AI Insights</h4>
                {threatIntel.executive_summary && (
                  <p className="insight-text">{threatIntel.executive_summary}</p>
                )}
              </div>
            </div>

            <div className="recommendations-section">
              <h4>🎯 Recommended Actions</h4>
              <ul className="recommendations-list">
                {threatIntel.recommendations && threatIntel.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Helper function to get threat color
function getThreatColor(score) {
  if (score >= 80) return '#ff0000';
  if (score >= 60) return '#ff9800';
  if (score >= 40) return '#ffeb3b';
  return '#4caf50';
}

export default SOCDashboard;
