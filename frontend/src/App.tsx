import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import MapView from './pages/MapView';
import DataLogs from './pages/DataLogs';
import RiskAlerts from './pages/RiskAlerts';
import Settings from './pages/Settings';
import AuthPage from './pages/AuthPage';
import EducationDashboard from './pages/EducationDashboard';
import './index.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/map" element={<MapView />} />
          <Route path="/data" element={<DataLogs />} />
          <Route path="/education" element={<EducationDashboard />} />
          <Route path="/alerts" element={<RiskAlerts />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
