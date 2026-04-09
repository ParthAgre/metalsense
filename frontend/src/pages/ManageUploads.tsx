import React, { useState, useEffect } from 'react';
import { Trash2, FileText, Database } from 'lucide-react';
import axios from 'axios';
import './DataLogs.css'; // Reusing table styles

interface Dataset {
    id: number;
    filename: string;
    upload_status: string;
    created_at: string;
}

const ManageUploads: React.FC = () => {
    const [datasets, setDatasets] = useState<Dataset[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchDatasets = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:8000/api/v1/researcher/uploads', {
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            setDatasets(response.data);
            setLoading(false);
        } catch (err) {
            console.error(err);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDatasets();
    }, []);

    const handleDelete = async (id: number) => {
        if (!window.confirm("Are you sure you want to delete this dataset? All associated samples and risk calculations will be permanently removed.")) return;
        
        try {
            const token = localStorage.getItem('token');
            await axios.delete(`http://localhost:8000/api/v1/researcher/uploads/${id}`, {
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            alert("Dataset deleted successfully.");
            fetchDatasets();
        } catch (err) {
            alert("Error deleting dataset.");
        }
    };

    return (
        <div className="data-logs-container animate-fade-in">
            <div className="logs-header glass">
                <div className="header-title">
                    <h3>Manage My Uploads</h3>
                    <p>View and manage the datasets you have contributed to the platform</p>
                </div>
                <div className="header-actions">
                     <div className="action-btn glass">
                        <Database size={18} />
                        <span>Total Files: {datasets.length}</span>
                    </div>
                </div>
            </div>

            <div className="table-wrapper glass">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Filename</th>
                            <th>Upload Date</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading && <tr><td colSpan={5} style={{textAlign: "center"}}>Loading datasets...</td></tr>}
                        {!loading && datasets.length === 0 && <tr><td colSpan={5} style={{textAlign: "center"}}>No datasets uploaded yet.</td></tr>}
                        {!loading && datasets.map((ds) => (
                            <tr key={ds.id}>
                                <td>#{ds.id}</td>
                                <td className="location-cell">
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <FileText size={16} color="var(--primary)" />
                                        {ds.filename}
                                    </div>
                                </td>
                                <td>{new Date(ds.created_at).toLocaleString()}</td>
                                <td>
                                    <span className={`badge ${ds.upload_status === 'completed' ? 'badge-risk-safe' : 'badge-risk-low'}`}>
                                        {ds.upload_status}
                                    </span>
                                </td>
                                <td>
                                    <button 
                                        onClick={() => handleDelete(ds.id)}
                                        className="view-btn" 
                                        style={{ color: '#f87171', display: 'flex', alignItems: 'center', gap: '4px' }}
                                    >
                                        <Trash2 size={16} />
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ManageUploads;
