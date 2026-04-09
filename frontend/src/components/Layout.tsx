import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Map as MapIcon, Database, AlertTriangle, Settings, Menu, LogOut, BookOpen, User as UserIcon } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Layout.css';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const location = useLocation();
    const navigate = useNavigate();
    const role = localStorage.getItem('role') || 'citizen';
    const [userName, setUserName] = useState('');

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const response = await axios.get('http://localhost:8000/api/v1/users/me', {
                        headers: { Authorization: `Bearer ${token}` }
                    });
                    setUserName(response.data.full_name);
                }
            } catch (err) {
                console.error("Failed to fetch user", err);
            }
        };
        fetchUser();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        navigate('/auth');
    };

    const getInitials = (name: string) => {
        return name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
    };

    return (
        <div className="layout-container">
            <aside className="sidebar glass">
                <div className="logo">
                    <div className="logo-icon">M</div>
                    <span>MetalSense</span>
                </div>
                <nav>
                    {role === 'researcher' && (
                        <Link to="/" className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>
                            <LayoutDashboard size={20} />
                            <span>Dashboard</span>
                        </Link>
                    )}
                    <Link to="/map" className={`nav-item ${location.pathname === '/map' ? 'active' : ''}`}>
                        <MapIcon size={20} />
                        <span>Map View</span>
                    </Link>
                    {role === 'researcher' && (
                        <Link to="/data" className={`nav-item ${location.pathname === '/data' ? 'active' : ''}`}>
                            <Database size={20} />
                            <span>Data Logs</span>
                        </Link>
                    )}
                    <Link to="/alerts" className={`nav-item ${location.pathname === '/alerts' ? 'active' : ''}`}>
                        <AlertTriangle size={20} />
                        <span>Risk Alerts</span>
                    </Link>
                    <Link to="/education" className={`nav-item ${location.pathname === '/education' ? 'active' : ''}`}>
                        <BookOpen size={20} />
                        <span>Education</span>
                    </Link>
                </nav>
                <div className="sidebar-footer">
                    <button onClick={handleLogout} className="nav-item logout-btn" style={{ background: 'transparent', border: 'none', width: '100%', textAlign: 'left', cursor: 'pointer', outline: 'none' }}>
                        <LogOut size={20} />
                        <span>Sign Out</span>
                    </button>
                    <Link to="/settings" className={`nav-item ${location.pathname === '/settings' ? 'active' : ''}`}>
                        <Settings size={20} />
                        <span>Settings</span>
                    </Link>
                </div>
            </aside>

            <main className="main-content">
                <header className="header glass">
                    <button className="mobile-menu-btn">
                        <Menu size={24} />
                    </button>
                    <div className="header-search">
                        {/* Search removed as requested */}
                    </div>
                    <div className="header-profile">
                        <div className="profile-img-circle">
                            {userName ? getInitials(userName) : <UserIcon size={20} />}
                        </div>
                    </div>
                </header>
                <div className="page-content">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
