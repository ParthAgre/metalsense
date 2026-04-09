import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Link } from 'react-router-dom';
import { Droplets, ShieldCheck, Activity, MapPin, Database, Loader2 } from 'lucide-react';
import axios from 'axios';
import './Dashboard.css';

interface DashboardStats {
    total_samples: number;
    avg_hpi: number;
    avg_mi: number;
    risk_distribution: Record<string, number>;
    metal_averages: { name: string; value: number }[];
    latest_site: string;
}

const Dashboard: React.FC = () => {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://localhost:8000/api/v1/researcher/dashboard-stats', {
                    headers: token ? { Authorization: `Bearer ${token}` } : {}
                });
                setStats(response.data);
            } catch (err) {
                console.error("Failed to fetch dashboard stats", err);
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="dashboard-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
            </div>
        );
    }

    if (!stats || stats.total_samples === 0) {
        return (
            <div className="dashboard-container animate-fade-in">
                <div className="dashboard-header-actions" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1rem' }}>
                    <Link to="/manage-uploads" className="action-btn glass primary" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Database size={18} />
                        <span>Manage My Data</span>
                    </Link>
                </div>
                <div className="card glass" style={{ padding: '4rem', textAlign: 'center' }}>
                    <h3>No Data Available</h3>
                    <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>Please upload a CSV file to see your personalized dashboard stats.</p>
                    <Link to="/data" className="action-btn glass primary" style={{ display: 'inline-flex', marginTop: '2rem', textDecoration: 'none' }}>Go to Uploads</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard-container animate-fade-in">
            <div className="dashboard-header-actions" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1rem' }}>
                <Link to="/manage-uploads" className="action-btn glass primary" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Database size={18} />
                    <span>Manage My Data</span>
                </Link>
            </div>

            <div className="stats-grid">
                <div className="stat-card glass">
                    <div className="stat-icon blue">
                        <Droplets size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Avg. HPI Score</p>
                        <h3 className="stat-value">{stats.avg_hpi}</h3>
                        <span className="stat-trend">Based on {stats.total_samples} samples</span>
                    </div>
                </div>

                <div className="stat-card glass">
                    <div className="stat-icon green">
                        <ShieldCheck size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Safety Status</p>
                        <h3 className={`stat-value risk-${stats.avg_hpi > 100 ? 'high' : stats.avg_hpi > 50 ? 'moderately' : 'safe'}`}>
                            {stats.avg_hpi > 100 ? 'Hazardous' : stats.avg_hpi > 50 ? 'Polluted' : 'Safe'}
                        </h3>
                        <span className="stat-trend">Regional Average</span>
                    </div>
                </div>

                <div className="stat-card glass">
                    <div className="stat-icon orange">
                        <Activity size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Avg. Metal Index</p>
                        <h3 className="stat-value">{stats.avg_mi}</h3>
                        <span className="stat-trend">Multi-metal aggregate</span>
                    </div>
                </div>

                <div className="stat-card glass">
                    <div className="stat-icon purple">
                        <MapPin size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Latest Sampling Site</p>
                        <h3 className="stat-value">{stats.latest_site}</h3>
                        <span className="stat-trend">Recent acquisition</span>
                    </div>
                </div>
            </div>

            <div className="charts-grid">
                <div className="chart-card glass">
                    <div className="chart-header">
                        <h4>Average Pollutant Concentrations</h4>
                    </div>
                    <div className="chart-wrapper">
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={stats.metal_averages}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis dataKey="name" stroke="#94a3b8" />
                                <YAxis stroke="#94a3b8" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                    itemStyle={{ color: '#f8fafc' }}
                                />
                                <Bar dataKey="value" fill="#6366f1" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="chart-card glass">
                    <div className="chart-header">
                        <h4>Risk Category Distribution</h4>
                    </div>
                    <div className="chart-wrapper">
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={Object.entries(stats.risk_distribution).map(([name, value]) => ({ name, value }))}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis dataKey="name" stroke="#94a3b8" />
                                <YAxis stroke="#94a3b8" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                    itemStyle={{ color: '#f8fafc' }}
                                />
                                <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
