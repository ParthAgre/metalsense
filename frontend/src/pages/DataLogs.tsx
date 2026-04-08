import React, { useState } from 'react';
import { Search, Download, Filter } from 'lucide-react';
import { mockSamples } from '../services/mockData';
import './DataLogs.css';

const DataLogs: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');

    const filteredSamples = mockSamples.filter(sample =>
        sample.location_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const getRiskBadgeClass = (risk: string) => {
        switch (risk) {
            case 'High': return 'badge-risk-high';
            case 'Low': return 'badge-risk-low';
            case 'Safe': return 'badge-risk-safe';
            default: return '';
        }
    };

    return (
        <div className="data-logs-container animate-fade-in">
            <div className="logs-header glass">
                <div className="header-title">
                    <h3>Water Quality Logs</h3>
                    <p>Comprehensive record of all heavy metal sampling data</p>
                </div>
                <div className="header-actions">
                    <div className="search-box glass">
                        <Search size={18} />
                        <input
                            type="text"
                            placeholder="Filter by location..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <button className="action-btn glass">
                        <Filter size={18} />
                        <span>Filter</span>
                    </button>
                    <button className="action-btn glass primary">
                        <Download size={18} />
                        <span>Export CSV</span>
                    </button>
                </div>
            </div>

            <div className="table-wrapper glass">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Location</th>
                            <th>Date</th>
                            <th>Arsenic (As)</th>
                            <th>Lead (Pb)</th>
                            <th>Mercury (Hg)</th>
                            <th>HPI</th>
                            <th>Risk Level</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredSamples.map(sample => (
                            <tr key={sample.id}>
                                <td>#{sample.id}</td>
                                <td className="location-cell">{sample.location_name}</td>
                                <td>{new Date(sample.sampling_date).toLocaleDateString()}</td>
                                <td>{sample.conc_arsenic.toFixed(3)}</td>
                                <td>{sample.conc_lead.toFixed(3)}</td>
                                <td>{sample.conc_mercury.toFixed(4)}</td>
                                <td className="weight-bold">{sample.hpi_score.toFixed(1)}</td>
                                <td>
                                    <span className={`badge ${getRiskBadgeClass(sample.risk_level)}`}>
                                        {sample.risk_level}
                                    </span>
                                </td>
                                <td>
                                    <button className="view-btn">View Full</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DataLogs;
