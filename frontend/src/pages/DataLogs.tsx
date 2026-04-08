import React, { useState } from 'react';
import { Search, Download, Filter, Upload } from 'lucide-react';
import { mockSamples } from '../services/mockData';
import axios from 'axios';
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

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                 alert("Please login as a researcher to upload CSV files");
                 return;
            }
            await axios.post('http://127.0.0.1:8000/api/v1/researcher/upload-csv', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                }
            });
            alert('CSV Uploaded and processing started!');
        } catch(err) {
            alert('Error uploading CSV. Make sure you are logged in as a Researcher.');
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
                    <label className="action-btn glass primary" style={{ cursor: 'pointer' }}>
                        <Upload size={18} />
                        <span>Upload CSV</span>
                        <input type="file" accept=".csv" style={{ display: 'none' }} onChange={handleFileUpload} />
                    </label>
                    <button className="action-btn glass">
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
