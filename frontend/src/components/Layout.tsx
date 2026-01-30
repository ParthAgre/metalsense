import React from 'react';
import { LayoutDashboard, Map as MapIcon, Database, AlertTriangle, Settings, Menu } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import './Layout.css';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const location = useLocation();

    return (
        <div className="layout-container">
            <aside className="sidebar glass">
                <div className="logo">
                    <div className="logo-icon">M</div>
                    <span>MetalSense</span>
                </div>
                <nav>
                    <Link to="/" className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>
                        <LayoutDashboard size={20} />
                        <span>Dashboard</span>
                    </Link>
                    <Link to="/map" className={`nav-item ${location.pathname === '/map' ? 'active' : ''}`}>
                        <MapIcon size={20} />
                        <span>Map View</span>
                    </Link>
                    <Link to="/data" className={`nav-item ${location.pathname === '/data' ? 'active' : ''}`}>
                        <Database size={20} />
                        <span>Data Logs</span>
                    </Link>
                    <Link to="/alerts" className={`nav-item ${location.pathname === '/alerts' ? 'active' : ''}`}>
                        <AlertTriangle size={20} />
                        <span>Risk Alerts</span>
                    </Link>
                </nav>
                <div className="sidebar-footer">
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
                        <input type="text" placeholder="Search locations..." className="glass" />
                    </div>
                    <div className="header-profile">
                        <div className="profile-img"></div>
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
