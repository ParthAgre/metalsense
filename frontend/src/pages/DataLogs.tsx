import React, { useState, useEffect } from 'react';
import { Search, Download, Filter, Upload } from 'lucide-react';
import axios from 'axios';
import './DataLogs.css';

interface ApiSample {
    id: number;
    lat: number;
    lng: number;
    timestamp: string;
    source_type: string;
    measurements: { metal: string; concentration: number }[];
    risk: { hpi: number; risk_category: string };
}

const DataLogs: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [samples, setSamples] = useState<ApiSample[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchSamples = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:8000/api/v1/researcher/samples', {
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            setSamples(response.data);
            setLoading(false);
        } catch (err) {
            console.error(err);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSamples();
    }, []);

    const filteredSamples = samples.filter(sample =>
        sample.source_type.toLowerCase().includes(searchTerm.toLowerCase()) || 
        sample.id.toString().includes(searchTerm)
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
            await axios.post('http://localhost:8000/api/v1/researcher/upload-csv', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${token}`
                }
            });
            alert('CSV Uploaded and processing successfully in the background!');
            fetchSamples(); // reload dynamic table stats
        } catch(err) {
            alert('Error uploading CSV. Make sure you are logged in as a Researcher.');
        }
    };

    const getMetalConc = (sample: ApiSample, metalName: string) => {
        const m = sample.measurements.find(m => m.metal.toLowerCase() === metalName.toLowerCase());
        return m ? m.concentration : 0;
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
                            <th>Source</th>
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
                        {loading && <tr><td colSpan={9} style={{textAlign: "center"}}>Loading samples...</td></tr>}
                        {!loading && filteredSamples.map((sample, idx) => (
                            <tr key={sample.id || idx}>
                                <td>#{sample.id}</td>
                                <td className="location-cell">{sample.source_type}</td>
                                <td>{new Date(sample.timestamp).toLocaleDateString()}</td>
                                <td>{getMetalConc(sample, 'Arsenic').toFixed(3)}</td>
                                <td>{getMetalConc(sample, 'Lead').toFixed(3)}</td>
                                <td>{getMetalConc(sample, 'Mercury').toFixed(4)}</td>
                                <td className="weight-bold">{sample.risk?.hpi ? sample.risk.hpi.toFixed(1) : 'Processing'}</td>
                                <td>
                                    <span className={`badge ${getRiskBadgeClass(sample.risk?.risk_category || 'Safe')}`}>
                                        {sample.risk?.risk_category || 'Safe'}
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
