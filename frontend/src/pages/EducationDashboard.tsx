import { useEffect, useState } from 'react';
import axios from 'axios';
import { BookOpen } from 'lucide-react';
import './DataLogs.css';
import './AuthPage.css'; // For .card class which is now glassmorphic

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export default function EducationDashboard() {
  const [metals, setMetals] = useState<any[]>([]);
  const [materials, setMaterials] = useState<any[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const metRes = await axios.get(`${API_BASE_URL}/education/metals`);
        const matRes = await axios.get(`${API_BASE_URL}/education/materials`);
        setMetals(metRes.data);
        setMaterials(matRes.data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="page-container page-enter">
      <header className="page-header">
        <div>
          <h1 className="page-title">Education & Insights</h1>
          <p className="page-subtitle">Understand Heavy Metals and Health Factors</p>
        </div>
      </header>
      
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3><BookOpen size={20} style={{marginRight: '8px', verticalAlign: 'middle'}}/> Heavy Metal Directory</h3>
        <table className="data-table" style={{ marginTop: '15px' }}>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Standard Limit (mg/L)</th>
              <th>Health Impact</th>
            </tr>
          </thead>
          <tbody>
            {metals.map((m) => (
              <tr key={m.id}>
                <td style={{ fontWeight: 'bold' }}>{m.symbol}</td>
                <td>{m.name}</td>
                <td>{m.standard_limit}</td>
                <td>{m.health_effects}</td>
              </tr>
            ))}
            {metals.length === 0 && <tr><td colSpan={4}>Loading metals...</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Learning Materials</h3>
        <ul style={{ listStyleType: 'none', padding: 0, marginTop: '15px' }}>
         {materials.map(mat => (
             <li key={mat.id} style={{ padding: '10px', borderBottom: '1px solid #1e293b' }}>
                <h4 style={{ color: '#38bdf8' }}>{mat.title}</h4>
                <p style={{ marginTop: '5px', color: '#94a3b8' }}>{mat.content_markdown}</p>
             </li>
         ))}
        </ul>
      </div>
    </div>
  );
}
