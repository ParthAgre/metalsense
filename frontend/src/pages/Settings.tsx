import React, { useState, useEffect } from 'react';
import { User, LogOut, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Settings.css';

interface UserData {
    full_name: string;
    email: string;
    role: string;
}

const Settings: React.FC = () => {
    const [user, setUser] = useState<UserData | null>(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/auth');
                    return;
                }
                const response = await axios.get('http://localhost:8000/api/v1/users/me', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setUser(response.data);
            } catch (err) {
                console.error("Failed to fetch user data", err);
            } finally {
                setLoading(false);
            }
        };
        fetchUser();
    }, [navigate]);

    const handleSignOut = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        navigate('/auth');
    };

    if (loading) {
        return (
            <div className="settings-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
            </div>
        );
    }

    return (
        <div className="settings-container animate-fade-in">
            <div className="settings-header">
                <h3>Platform Settings</h3>
                <p>Manage your account preferences</p>
            </div>

            <div className="settings-grid">
                <div className="settings-nav glass">
                    <div className="s-nav-item active">
                        <User size={20} /> Profile
                    </div>
                    <button onClick={handleSignOut} className="s-nav-item logout" style={{ background: 'transparent', border: 'none', width: '100%', textAlign: 'left', cursor: 'pointer', padding: '0.75rem 1rem' }}>
                        <LogOut size={20} /> Sign Out
                    </button>
                </div>

                <div className="settings-content glass">
                    <div className="profile-section">
                        <div className="profile-header">
                            <div className="profile-avatar large" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem', color: 'white', fontWeight: 'bold', background: 'var(--primary)' }}>
                                {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
                            </div>
                            <div className="profile-info">
                                <h4>{user?.full_name}</h4>
                                <p style={{ textTransform: 'capitalize' }}>{user?.role}</p>
                            </div>
                        </div>

                        <div className="settings-form">
                            <div className="form-group">
                                <label>Full Name</label>
                                <input type="text" value={user?.full_name || ''} readOnly className="glass" />
                            </div>
                            <div className="form-group">
                                <label>Email Address</label>
                                <input type="email" value={user?.email || ''} readOnly className="glass" />
                            </div>
                            <div className="form-group">
                                <label>Account Role</label>
                                <input type="text" value={user?.role || ''} readOnly className="glass" style={{ textTransform: 'capitalize' }} />
                                <p className="form-desc">Primary account permission level.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
