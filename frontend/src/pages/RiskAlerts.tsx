import React, { useState, useEffect } from 'react';
import { AlertCircle, ShieldAlert, CheckCircle, Info, MapPin, Loader2, ExternalLink } from 'lucide-react';
import axios from 'axios';
import './RiskAlerts.css';

interface ApiSample {
    id: number;
    location_name: string;
    state: string;
    district: string;
    risk: { hpi: number; risk_category: string };
    measurements: { metal: string; concentration: number }[];
}

const RiskAlerts: React.FC = () => {
    const [samples, setSamples] = useState<ApiSample[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSamples = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/researcher/samples');
                setSamples(response.data);
            } catch (err) {
                console.error("Failed to fetch alerts", err);
            } finally {
                setLoading(false);
            }
        };
        fetchSamples();
    }, []);

    const highRiskSamples = samples.filter(s => s.risk.risk_category === 'Hazardous');
    const lowRiskSamples = samples.filter(s => s.risk.risk_category === 'Moderately Polluted');

    const getImpactMetals = (sample: ApiSample) => {
        return sample.measurements
            .filter(m => m.concentration > 0)
            .map(m => m.metal)
            .join(', ');
    };

    const handleActionClick = (type: string) => {
        const url = type === 'health' 
            ? 'https://www.who.int/teams/environment-climate-change-and-health/water-sanitation-and-health/water-safety-and-quality/drinking-water-quality-guidelines'
            : 'https://cgwb.gov.in/water-quality-standards.html';
        window.open(url, '_blank');
    };

    if (loading) {
        return (
            <div className="risk-alerts-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
            </div>
        );
    }

    return (
        <div className="risk-alerts-container animate-fade-in">
            <div className="alerts-header">
                <h3>Safety Advisories & Alerts</h3>
                <p>Real-time updates on water quality hazards detected in your datasets</p>
            </div>

            <div className="alerts-content">
                {highRiskSamples.length === 0 && lowRiskSamples.length === 0 && (
                    <div className="card glass" style={{ padding: '3rem', textAlign: 'center', margin: '2rem 0' }}>
                        <CheckCircle size={48} color="#10b981" style={{ marginBottom: '1rem' }} />
                        <h4>All Clear</h4>
                        <p style={{ color: 'var(--text-muted)' }}>No critical water quality hazards detected at this time.</p>
                    </div>
                )}

                {highRiskSamples.length > 0 && (
                    <section className="alert-section">
                        <div className="section-title critical">
                            <ShieldAlert size={20} />
                            <h4>Critical Alerts (Hazardous)</h4>
                        </div>
                        <div className="alert-cards">
                            {highRiskSamples.map(sample => (
                                <div key={sample.id} className="alert-card glass high">
                                    <div className="alert-badge">HAZARDOUS</div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                                        <MapPin size={16} color="var(--primary)" />
                                        <h4>{sample.location_name}</h4>
                                    </div>
                                    <p className="alert-region">{sample.district}, {sample.state}</p>
                                    <p className="alert-desc" style={{ marginTop: '10px' }}>
                                        Immediate danger: Elevated concentrations of <strong>{getImpactMetals(sample)}</strong> detected. 
                                        Potability index exceeds safe limits significantly.
                                    </p>
                                    <div className="alert-actions" style={{ marginTop: '1.5rem' }}>
                                        <div className="risk-val">HPI: {sample.risk.hpi.toFixed(1)}</div>
                                        <button className="safety-btn" onClick={() => handleActionClick('health')}>
                                            Health Advisory <ExternalLink size={14} style={{ marginLeft: '4px' }} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {lowRiskSamples.length > 0 && (
                    <section className="alert-section" style={{ marginTop: '2rem' }}>
                        <div className="section-title warning">
                            <AlertCircle size={20} />
                            <h4>Warning Alerts (Polluted)</h4>
                        </div>
                        <div className="alert-cards">
                            {lowRiskSamples.map(sample => (
                                <div key={sample.id} className="alert-card glass low">
                                    <div className="alert-badge">WARNING</div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                                        <MapPin size={16} color="var(--primary)" />
                                        <h4>{sample.location_name}</h4>
                                    </div>
                                    <p className="alert-region">{sample.district}, {sample.state}</p>
                                    <p className="alert-desc" style={{ marginTop: '10px' }}>
                                        Moderate contamination levels for <strong>{getImpactMetals(sample)}</strong>. 
                                        Continuous monitoring and localized filtration recommended.
                                    </p>
                                    <div className="alert-actions" style={{ marginTop: '1.5rem' }}>
                                        <div className="risk-val">HPI: {sample.risk.hpi.toFixed(1)}</div>
                                        <button className="safety-btn" onClick={() => handleActionClick('guidelines')}>
                                             Guidelines <ExternalLink size={14} style={{ marginLeft: '4px' }} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                <div className="safety-tips glass" style={{ marginTop: '3rem' }}>
                    <div className="tips-header">
                        <Info size={24} />
                        <h4>General Safety Recommendations</h4>
                    </div>
                    <ul className="tips-list">
                        <li>
                            <CheckCircle size={18} className="success-icon" />
                            <span>Use activated carbon or reverse osmosis (RO) systems in high-risk zones.</span>
                        </li>
                        <li>
                            <CheckCircle size={18} className="success-icon" />
                            <span>Check for visible discoloration or metallic odor in domestic water supplies.</span>
                        </li>
                        <li>
                            <CheckCircle size={18} className="success-icon" />
                            <span>Note: Standard boiling does NOT eliminate heavy metals like Lead or Arsenic.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default RiskAlerts;
