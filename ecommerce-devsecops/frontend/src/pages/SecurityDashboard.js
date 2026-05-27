import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

const SecurityDashboard = () => {
  const [selectedTab, setSelectedTab] = useState('overview');
  const [vulnerabilityData, setVulnerabilityData] = useState([]);
  const [threatData, setThreatData] = useState([]);
  const [complianceData, setComplianceData] = useState([]);

  useEffect(() => {
    // Fetch security data from backend
    fetchSecurityData();
    const interval = setInterval(fetchSecurityData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchSecurityData = async () => {
    try {
      const response = await fetch('/api/security/overview');
      if (response.ok) {
        const data = await response.json();
        setVulnerabilityData(data.vulnerabilities || []);
        setThreatData(data.threats || []);
        setComplianceData(data.compliance || []);
      }
    } catch (error) {
      console.error('Error fetching security data:', error);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const SecurityKPI = ({ title, value, status, trend }) => (
    <motion.div
      variants={itemVariants}
      className="relative bg-gradient-to-br from-gray-900 via-gray-800 to-black border border-cyan-500/30 rounded-lg p-6 backdrop-blur-xl shadow-2xl hover:border-cyan-500/60 transition-all hover:shadow-cyan-500/20"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 rounded-lg pointer-events-none" />
      <div className="relative z-10">
        <p className="text-cyan-400/70 text-sm font-medium uppercase tracking-wider">{title}</p>
        <div className="mt-3 flex items-baseline justify-between">
          <h3 className="text-4xl font-bold text-white drop-shadow-lg">{value}</h3>
          <span className={`text-sm font-bold ${trend > 0 ? 'text-red-400' : 'text-green-400'}`}>
            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        </div>
        <div className="mt-4 h-1 bg-gradient-to-r from-cyan-500/50 to-purple-500/50 rounded-full overflow-hidden">
          <div
            className={`h-full bg-gradient-to-r ${
              status === 'critical'
                ? 'from-red-500 to-red-600'
                : status === 'warning'
                ? 'from-yellow-500 to-yellow-600'
                : 'from-green-500 to-green-600'
            }`}
            style={{ width: `${Math.random() * 100}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-gray-400">Status: <span className="text-white font-semibold capitalize">{status}</span></p>
      </div>
    </motion.div>
  );

  const ThreatHeatmap = () => (
    <motion.div
      variants={itemVariants}
      className="bg-gradient-to-br from-gray-900 via-gray-800 to-black border border-purple-500/30 rounded-lg p-6 backdrop-blur-xl shadow-2xl hover:border-purple-500/60 transition-all"
    >
      <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" />
        Threat Severity Heatmap
      </h3>
      <div className="grid grid-cols-7 gap-1">
        {Array.from({ length: 28 }).map((_, i) => (
          <div
            key={i}
            className={`h-6 rounded-sm cursor-pointer transition-all hover:scale-110 border border-gray-700/50 ${
              i % 5 === 0
                ? 'bg-red-600/70'
                : i % 5 === 1
                ? 'bg-red-500/50'
                : i % 5 === 2
                ? 'bg-yellow-500/60'
                : i % 5 === 3
                ? 'bg-blue-500/40'
                : 'bg-green-500/30'
            }`}
            title={`Day ${i + 1}`}
          />
        ))}
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black p-8">
      {/* Animated background */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-600/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-600/20 rounded-full blur-3xl animate-pulse" />
      </div>

      <motion.div
        className="max-w-7xl mx-auto"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-8">
          <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 mb-2">
            Security Operations Center
          </h1>
          <p className="text-gray-400 text-lg">Enterprise Threat Intelligence & Posture Management</p>
        </motion.div>

        {/* Tabs */}
        <motion.div variants={itemVariants} className="flex gap-2 mb-8 flex-wrap">
          {['overview', 'vulnerabilities', 'threats', 'compliance', 'recommendations'].map((tab) => (
            <button
              key={tab}
              onClick={() => setSelectedTab(tab)}
              className={`px-6 py-2 rounded-lg font-medium transition-all transform hover:scale-105 ${
                selectedTab === tab
                  ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white shadow-lg shadow-cyan-500/50'
                  : 'bg-gray-800/50 text-gray-300 border border-gray-700/50 hover:border-cyan-500/50'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </motion.div>

        {/* KPI Cards */}
        <motion.div variants={containerVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <SecurityKPI title="Security Score" value="8.7/10" status="warning" trend={-2.5} />
          <SecurityKPI title="Critical CVEs" value="12" status="critical" trend={3.2} />
          <SecurityKPI title="Open Incidents" value="47" status="warning" trend={5.1} />
          <SecurityKPI title="Compliant Assets" value="94%" status="success" trend={1.8} />
        </motion.div>

        {/* Main Content */}
        {selectedTab === 'overview' && (
          <motion.div
            variants={containerVariants}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            {/* CVE Trend Analytics */}
            <motion.div
              variants={itemVariants}
              className="bg-gradient-to-br from-gray-900 via-gray-800 to-black border border-cyan-500/30 rounded-lg p-6 backdrop-blur-xl shadow-2xl hover:border-cyan-500/60 transition-all"
            >
              <h3 className="text-xl font-bold text-white mb-4">CVE Trend Analytics</h3>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={vulnerabilityData || cveTrendData}>
                  <defs>
                    <linearGradient id="cveGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00d9ff" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#00d9ff" stopOpacity={0.1} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis stroke="#666" />
                  <YAxis stroke="#666" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1a1a2e',
                      border: '1px solid #00d9ff',
                      borderRadius: '8px',
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke="#00d9ff"
                    fillOpacity={1}
                    fill="url(#cveGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </motion.div>

            {/* Threat Distribution */}
            <motion.div
              variants={itemVariants}
              className="bg-gradient-to-br from-gray-900 via-gray-800 to-black border border-purple-500/30 rounded-lg p-6 backdrop-blur-xl shadow-2xl hover:border-purple-500/60 transition-all"
            >
              <h3 className="text-xl font-bold text-white mb-4">Threat Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={threatDistributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {threatDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={threatColors[index]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1a1a2e',
                      border: '1px solid #a855f7',
                      borderRadius: '8px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </motion.div>

            {/* Threat Heatmap */}
            <motion.div variants={itemVariants} className="lg:col-span-2">
              <ThreatHeatmap />
            </motion.div>
          </motion.div>
        )}

        {selectedTab === 'vulnerabilities' && (
          <motion.div variants={containerVariants} className="grid grid-cols-1 gap-6">
            <motion.div
              variants={itemVariants}
              className="bg-gradient-to-br from-gray-900 via-gray-800 to-black border border-red-500/30 rounded-lg p-6 backdrop-blur-xl"
            >
              <h3 className="text-xl font-bold text-white mb-4">Vulnerability Priority List</h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {vulnerabilityList.map((vuln, idx) => (
                  <div
                    key={idx}
                    className={`border-l-4 px-4 py-3 bg-gray-800/50 rounded-r ${
                      vuln.severity === 'critical'
                        ? 'border-l-red-500'
                        : vuln.severity === 'high'
                        ? 'border-l-orange-500'
                        : 'border-l-yellow-500'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-white">{vuln.cve}</p>
                        <p className="text-sm text-gray-300">{vuln.description}</p>
                      </div>
                      <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                        vuln.severity === 'critical'
                          ? 'bg-red-900/50 text-red-200'
                          : vuln.severity === 'high'
                          ? 'bg-orange-900/50 text-orange-200'
                          : 'bg-yellow-900/50 text-yellow-200'
                      }`}>
                        {vuln.severity.toUpperCase()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}

        {selectedTab === 'compliance' && (
          <motion.div variants={containerVariants} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {complianceFrameworks.map((framework) => (
              <motion.div
                key={framework.name}
                variants={itemVariants}
                className="bg-gradient-to-br from-gray-900 via-gray-800 to-black border border-blue-500/30 rounded-lg p-6 backdrop-blur-xl"
              >
                <div className="flex justify-between items-start mb-4">
                  <h4 className="font-bold text-white">{framework.name}</h4>
                  <span className="text-lg font-bold text-cyan-400">{framework.score}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full transition-all"
                    style={{ width: `${framework.score}%` }}
                  />
                </div>
                <p className="text-xs text-gray-400 mt-3">{framework.controls} controls verified</p>
              </motion.div>
            ))}
          </motion.div>
        )}

        {selectedTab === 'recommendations' && (
          <motion.div variants={containerVariants} className="space-y-4">
            {aiRecommendations.map((rec, idx) => (
              <motion.div
                key={idx}
                variants={itemVariants}
                className="bg-gradient-to-br from-gray-900 via-gray-800 to-black border-l-4 border-l-green-500 border border-green-500/30 rounded-lg p-6 backdrop-blur-xl"
              >
                <div className="flex gap-4">
                  <div className="text-3xl">🤖</div>
                  <div className="flex-1">
                    <h4 className="font-bold text-white mb-2">{rec.title}</h4>
                    <p className="text-gray-300 text-sm mb-3">{rec.description}</p>
                    <div className="flex gap-2 flex-wrap">
                      <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-all">
                        Apply Fix
                      </button>
                      <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium rounded-lg transition-all">
                        Learn More
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

// Mock Data
const cveTrendData = [
  { name: 'Day 1', value: 23 },
  { name: 'Day 2', value: 29 },
  { name: 'Day 3', value: 20 },
  { name: 'Day 4', value: 35 },
  { name: 'Day 5', value: 31 },
  { name: 'Day 6', value: 40 },
  { name: 'Day 7', value: 38 },
];

const threatDistributionData = [
  { name: 'Malware', value: 28 },
  { name: 'Phishing', value: 35 },
  { name: 'Exploits', value: 22 },
  { name: 'Unauthorized Access', value: 15 },
];

const threatColors = ['#ef4444', '#f97316', '#eab308', '#3b82f6'];

const vulnerabilityList = [
  {
    cve: 'CVE-2024-1234',
    description: 'Remote Code Execution in auth module',
    severity: 'critical',
  },
  {
    cve: 'CVE-2024-5678',
    description: 'SQL Injection in product search',
    severity: 'high',
  },
  {
    cve: 'CVE-2024-9012',
    description: 'XSS vulnerability in user profile',
    severity: 'high',
  },
  {
    cve: 'CVE-2024-3456',
    description: 'Weak password requirements',
    severity: 'medium',
  },
];

const complianceFrameworks = [
  { name: 'PCI-DSS', score: 85, controls: 12 },
  { name: 'OWASP Top 10', score: 92, controls: 10 },
  { name: 'CIS Benchmarks', score: 88, controls: 20 },
  { name: 'NIST Cybersecurity Framework', score: 79, controls: 5 },
  { name: 'SOC 2', score: 91, controls: 15 },
  { name: 'ISO 27001', score: 84, controls: 18 },
];

const aiRecommendations = [
  {
    title: 'Patch Critical RCE Vulnerability',
    description: 'CVE-2024-1234 detected in authentication module. Update framework to v2.5.1. Estimated fix time: 30 minutes. Risk if not patched: Immediate system compromise possible.',
  },
  {
    title: 'Implement WAF Rules for Injection Attacks',
    description: 'SQL injection patterns detected in product search API. Implement parameterized queries and input validation. Priority: HIGH',
  },
  {
    title: 'Enable Multi-Factor Authentication',
    description: 'Current login system lacks MFA. Enable TOTP-based MFA to reduce credential compromise risk by 94%. Users: 2,547',
  },
  {
    title: 'Upgrade Container Base Images',
    description: 'Frontend container using outdated Alpine 3.14. Upgrade to 3.19 for security patches. 0 breaking changes detected.',
  },
];

export default SecurityDashboard;
