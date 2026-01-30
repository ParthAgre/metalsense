import React from 'react';
import { User, Bell, Shield, Laptop, LogOut } from 'lucide-react';
import './Settings.css';

const Settings: React.FC = () => {
    return (
        <div className="settings-container animate-fade-in">
            <div className="settings-header">
                <h3>Platform Settings</h3>
                <p>Manage your account and notification preferences</p>
            </div>

            <div className="settings-grid">
                <div className="settings-nav glass">
                    <div className="s-nav-item active"><User size={20} /> Profile</div>
                    <div className="s-nav-item"><Bell size={20} /> Notifications</div>
                    <div className="s-nav-item"><Shield size={20} /> Security</div>
                    <div className="s-nav-item"><Laptop size={20} /> Appearance</div>
                    <div className="s-nav-item logout"><LogOut size={20} /> Sign Out</div>
                </div>

                <div className="settings-content glass">
                    <div className="profile-section">
                        <div className="profile-header">
                            <div className="profile-avatar large"></div>
                            <div className="profile-info">
                                <h4>Shashwat Singh</h4>
                                <p>Environmental Researcher</p>
                            </div>
                            <button className="edit-btn glass">Edit Profile</button>
                        </div>

                        <div className="settings-form">
                            <div className="form-group">
                                <label>Email Address</label>
                                <input type="email" value="shashwat@example.com" readOnly className="glass" />
                            </div>
                            <div className="form-group">
                                <label>Default Region</label>
                                <select className="glass">
                                    <option>North India (Gangetic Plain)</option>
                                    <option>Western Ghats</option>
                                    <option>Northeast India</option>
                                </select>
                            </div>
                            <div className="form-group toggle-group">
                                <div>
                                    <label>Push Notifications</label>
                                    <p className="form-desc">Get alerted on critical risk level changes in your region.</p>
                                </div>
                                <div className="toggle active"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
