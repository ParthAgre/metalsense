import React, { useState, useEffect, useMemo } from 'react';
import { Download, Filter, Upload, FileText, MapPin, Loader2, ShieldCheck } from 'lucide-react';
import axios from 'axios';
import './DataLogs.css';

interface ApiSample {
    id: number;
    lat: number;
    lng: number;
    location_name?: string;
    state?: string;
    district?: string;
    timestamp: string;
    source_type: string;
    measurements: { metal: string; concentration: number }[];
    risk: { hpi: number; mi: number; risk_category: string };
}

const DataLogs: React.FC = () => {
    const [stateFilter, setStateFilter] = useState('');
    const [districtFilter, setDistrictFilter] = useState('');
    const [riskFilter, setRiskFilter] = useState('');
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

    // Generate unique options for dropdowns
    const { states, districts } = useMemo(() => {
        const uniqueStates = Array.from(new Set(samples.map(s => s.state).filter(Boolean))) as string[];
        const uniqueDistricts = Array.from(new Set(samples.filter(s => stateFilter === '' || s.state === stateFilter).map(s => s.district).filter(Boolean))) as string[];
        return { 
            states: uniqueStates.sort(), 
            districts: uniqueDistricts.sort() 
        };
    }, [samples, stateFilter]);

    const filteredSamples = samples.filter(sample => {
        const matchesState = stateFilter === '' || sample.state === stateFilter;
        const matchesDistrict = districtFilter === '' || sample.district === districtFilter;
        const matchesRisk = riskFilter === '' || (sample.risk?.risk_category === riskFilter);
        return matchesState && matchesDistrict && matchesRisk;
    });

    const getRiskBadgeClass = (risk: string) => {
        switch (risk) {
            case 'Hazardous': return 'badge-risk-high';
            case 'Moderately Polluted': return 'badge-risk-low';
            case 'Safe': return 'badge-risk-safe';
            default: return 'badge-risk-safe';
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
            alert('CSV Uploaded! Processing will complete in the background.');
            setTimeout(fetchSamples, 3000); 
        } catch(err) {
            alert('Error uploading CSV. Make sure you are logged in as a Researcher.');
        }
    };

    const getMetalConc = (sample: ApiSample, metalName: string) => {
        const m = sample.measurements.find(m => m.metal.toLowerCase() === metalName.toLowerCase());
        return m ? m.concentration : 0;
    };

    if (loading && samples.length === 0) {
        return (
            <div className="data-logs-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
            </div>
        );
    }

    return (
        <div className="data-logs-container animate-fade-in">
            <div className="logs-header glass">
                <div className="header-title">
                    <h3>Water Quality Logs</h3>
                    <p>Comprehensive record of all spatial heavy metal sampling data</p>
                </div>
                <div className="header-actions">
                    <div className="search-box glass" style={{ width: '180px' }}>
                        <Filter size={18} style={{ opacity: 0.5 }} />
                        <select 
                            value={stateFilter} 
                            onChange={(e) => { setStateFilter(e.target.value); setDistrictFilter(''); }}
                            className="filter-select"
                        >
                            <option value="">All States</option>
                            {states.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                    </div>
                    <div className="search-box glass" style={{ width: '180px' }}>
                        <MapPin size={18} style={{ opacity: 0.5 }} />
                        <select 
                            value={districtFilter} 
                            onChange={(e) => setDistrictFilter(e.target.value)}
                            className="filter-select"
                            disabled={!stateFilter}
                        >
                            <option value="">All Districts</option>
                            {districts.map(d => <option key={d} value={d}>{d}</option>)}
                        </select>
                    </div>
                    <div className="search-box glass" style={{ width: '180px' }}>
                        <ShieldCheck size={18} style={{ opacity: 0.5 }} />
                        <select 
                            value={riskFilter} 
                            onChange={(e) => setRiskFilter(e.target.value)}
                            className="filter-select"
                        >
                            <option value="">All Quality</option>
                            <option value="Safe">Safe</option>
                            <option value="Moderately Polluted">Polluted</option>
                            <option value="Hazardous">Hazardous</option>
                        </select>
                    </div>
                    <label className="action-btn glass primary" style={{ cursor: 'pointer' }}>
                        <Upload size={18} />
                        <span>Upload CSV</span>
                        <input type="file" accept=".csv" style={{ display: 'none' }} onChange={handleFileUpload} />
                    </label>
                </div>
            </div>

            <div className="table-wrapper glass">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Location</th>
                            <th>District</th>
                            <th>State</th>
                            <th>Date</th>
                            <th>Arsenic (As)</th>
                            <th>Iron (Fe)</th>
                            <th>Uranium (U)</th>
                            <th>HPI</th>
                            <th>Risk Level</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredSamples.length === 0 && <tr><td colSpan={10} style={{textAlign: "center", padding: '2rem'}}>No samples match the selected filters.</td></tr>}
                        {filteredSamples.map((sample) => (
                            <tr key={sample.id}>
                                <td>#{sample.id}</td>
                                <td className="location-cell">
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <FileText size={14} color="var(--primary)" />
                                        {sample.location_name}
                                    </div>
                                </td>
                                <td>{sample.district}</td>
                                <td>{sample.state}</td>
                                <td>{new Date(sample.timestamp).toLocaleDateString()}</td>
                                <td style={{ color: getMetalConc(sample, 'As') > 0.01 ? '#ef4444' : 'inherit', fontWeight: getMetalConc(sample, 'As') > 0.01 ? 'bold' : 'normal' }}>
                                    {getMetalConc(sample, 'As').toFixed(4)}
                                </td>
                                <td>{getMetalConc(sample, 'Fe').toFixed(3)}</td>
                                <td>{getMetalConc(sample, 'U').toFixed(4)}</td>
                                <td className="weight-bold">{sample.risk?.hpi ? sample.risk.hpi.toFixed(1) : '...'}</td>
                                <td>
                                    <span className={`badge ${getRiskBadgeClass(sample.risk?.risk_category || 'Safe')}`}>
                                        {sample.risk?.risk_category || 'Safe'}
                                    </span>
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
