import React from 'react';
import { AlertCircle, ShieldAlert, CheckCircle, Info } from 'lucide-react';
import { mockSamples } from '../services/mockData';
import './RiskAlerts.css';

const RiskAlerts: React.FC = () => {
    const highRiskSamples = mockSamples.filter(s => s.risk_level === 'High');
    const lowRiskSamples = mockSamples.filter(s => s.risk_level === 'Low');

    return (
        <div className="risk-alerts-container animate-fade-in">
            <div className="alerts-header">
                <h3>Safety Advisories & Alerts</h3>
                <p>Real-time updates on water quality hazards</p>
            </div>

            <div className="alerts-content">
                <section className="alert-section">
                    <div className="section-title critical">
                        <ShieldAlert size={20} />
                        <h4>Critical Alerts (High Risk)</h4>
                    </div>
                    <div className="alert-cards">
                        {highRiskSamples.map(sample => (
                            <div key={sample.id} className="alert-card glass high">
                                <div className="alert-badge">CRITICAL</div>
                                <h4>{sample.location_name}</h4>
                                <p className="alert-desc">
                                    Significant concentrations of <strong>Arsenic</strong> and <strong>Iron</strong> detected.
                                    Immediate caution advised for local residents.
                                </p>
                                <div className="alert-actions">
                                    <div className="risk-val">HPI: {sample.hpi_score}</div>
                                    <button className="safety-btn">View Health Advisory</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="alert-section">
                    <div className="section-title warning">
                        <AlertCircle size={20} />
                        <h4>Warning Alerts (Low Risk)</h4>
                    </div>
                    <div className="alert-cards">
                        {lowRiskSamples.map(sample => (
                            <div key={sample.id} className="alert-card glass low">
                                <div className="alert-badge">WARNING</div>
                                <h4>{sample.location_name}</h4>
                                <p className="alert-desc">
                                    Elevated levels of industrial discharge detected. Monitoring local filtration systems is recommended.
                                </p>
                                <div className="alert-actions">
                                    <div className="risk-val">HPI: {sample.hpi_score}</div>
                                    <button className="safety-btn">Guidelines</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                <div className="safety-tips glass">
                    <div className="tips-header">
                        <Info size={24} />
                        <h4>General Safety Recommendations</h4>
                    </div>
                    <ul className="tips-list">
                        <li>
                            <CheckCircle size={18} className="success-icon" />
                            <span>Use activated carbon filters for private wells in high-risk zones.</span>
                        </li>
                        <li>
                            <CheckCircle size={18} className="success-icon" />
                            <span>Avoid direct contact with water bodies showing visible industrial runoff.</span>
                        </li>
                        <li>
                            <CheckCircle size={18} className="success-icon" />
                            <span>Boiling water does not remove heavy metals like Lead or Arsenic.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default RiskAlerts;
