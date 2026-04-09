import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import MapView from './pages/MapView';
import DataLogs from './pages/DataLogs';
import RiskAlerts from './pages/RiskAlerts';
import Settings from './pages/Settings';
import AuthPage from './pages/AuthPage';
import ManageUploads from './pages/ManageUploads';
import EducationDashboard from './pages/EducationDashboard';
import './index.css';

const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode, allowedRoles?: string[] }) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role') || 'citizen';

  if (!token) {
    return <Navigate to="/auth" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to="/map" replace />;
  }

  return <>{children}</>;
};

const HomeRoute = () => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role') || 'citizen';
  
  if (!token) return <Navigate to="/auth" replace />;
  return role === 'researcher' ? <Dashboard /> : <Navigate to="/map" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/*" element={
          <ProtectedRoute>
            <Layout>
              <Routes>
                <Route path="/" element={<HomeRoute />} />
                <Route path="/map" element={<MapView />} />
                <Route path="/education" element={<EducationDashboard />} />
                <Route path="/alerts" element={<RiskAlerts />} />
                <Route path="/data" element={
                  <ProtectedRoute allowedRoles={['researcher']}>
                    <DataLogs />
                  </ProtectedRoute>
                } />
                <Route path="/manage-uploads" element={
                  <ProtectedRoute allowedRoles={['researcher']}>
                    <ManageUploads />
                  </ProtectedRoute>
                } />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </Layout>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
