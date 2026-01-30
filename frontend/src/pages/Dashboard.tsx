import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Droplets, ShieldCheck, Activity, MapPin } from 'lucide-react';
import { mockSamples } from '../services/mockData';
import './Dashboard.css';

const Dashboard: React.FC = () => {
    const latestSample = mockSamples[1]; // Using Yamuna for demo

    const pollutionData = [
        { name: 'As', value: latestSample.conc_arsenic * 100 },
        { name: 'Cr', value: latestSample.conc_chromium * 10 },
        { name: 'Cu', value: latestSample.conc_copper },
        { name: 'Fe', value: latestSample.conc_iron },
        { name: 'Pb', value: latestSample.conc_lead * 100 },
        { name: 'Zn', value: latestSample.conc_zinc / 2 },
    ];

    return (
        <div className="dashboard-container animate-fade-in">
            <div className="stats-grid">
                <div className="stat-card glass">
                    <div className="stat-icon blue">
                        <Droplets size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">HPI Score</p>
                        <h3 className="stat-value">{latestSample.hpi_score}</h3>
                        <span className="stat-trend high">↑ 12% from last wk</span>
                    </div>
                </div>

                <div className="stat-card glass">
                    <div className="stat-icon green">
                        <ShieldCheck size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Risk Level</p>
                        <h3 className={`stat-value risk-${latestSample.risk_level.toLowerCase()}`}>
                            {latestSample.risk_level}
                        </h3>
                        <span className="stat-trend">Stable</span>
                    </div>
                </div>

                <div className="stat-card glass">
                    <div className="stat-icon orange">
                        <Activity size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Metal Index (MI)</p>
                        <h3 className="stat-value">{latestSample.mi_score}</h3>
                        <span className="stat-trend low">↓ 2% from last wk</span>
                    </div>
                </div>

                <div className="stat-card glass">
                    <div className="stat-icon purple">
                        <MapPin size={24} />
                    </div>
                    <div className="stat-info">
                        <p className="stat-label">Active Site</p>
                        <h3 className="stat-value">{latestSample.location_name.split('-')[1]}</h3>
                        <span className="stat-trend">Monitoring active</span>
                    </div>
                </div>
            </div>

            <div className="charts-grid">
                <div className="chart-card glass">
                    <div className="chart-header">
                        <h4>Heavy Metal Concentration (Historical)</h4>
                    </div>
                    <div className="chart-wrapper">
                        <ResponsiveContainer width="100%" height={300}>
                            <AreaChart data={pollutionData}>
                                <defs>
                                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis dataKey="name" stroke="#94a3b8" />
                                <YAxis stroke="#94a3b8" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                    itemStyle={{ color: '#f8fafc' }}
                                />
                                <Area type="monotone" dataKey="value" stroke="#6366f1" fillOpacity={1} fill="url(#colorValue)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="chart-card glass">
                    <div className="chart-header">
                        <h4>Pollutant Comparison</h4>
                    </div>
                    <div className="chart-wrapper">
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={pollutionData}>
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
