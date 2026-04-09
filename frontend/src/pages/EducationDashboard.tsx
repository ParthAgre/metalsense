import { useEffect, useState } from 'react';
import axios from 'axios';
import { BookOpen, ShieldCheck, Microscope, Zap, Info, Loader2, ExternalLink } from 'lucide-react';
import './EducationDashboard.css';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export default function EducationDashboard() {
  const [metals, setMetals] = useState<any[]>([]);
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const metRes = await axios.get(`${API_BASE_URL}/education/metals`);
        const matRes = await axios.get(`${API_BASE_URL}/education/materials`);
        setMetals(metRes.data);
        setMaterials(matRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const handleLearnMore = (metalName: string) => {
    const url = `https://en.wikipedia.org/wiki/${metalName}`;
    window.open(url, '_blank');
  };

  if (loading) {
    return (
        <div className="education-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
            <Loader2 className="animate-spin" size={48} color="var(--primary)" />
        </div>
    );
  }

  return (
    <div className="education-container animate-fade-in">
      <section className="education-hero glass">
        <Microscope size={48} color="var(--primary)" style={{ marginBottom: '1rem' }} />
        <h2>Education & Health Insights</h2>
        <p>Understanding the impact of heavy metal contaminants on environmental and human health.</p>
      </section>
      
      <div className="section-header" style={{ marginTop: '2rem' }}>
        <h3><Zap size={20} style={{marginRight: '8px', verticalAlign: 'middle', color: '#fbbf24'}}/> Heavy Metal Directory</h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Permissible limits and physiological impacts</p>
      </div>

      <div className="education-grid">
        {metals.map((m) => (
          <div key={m.id} className="metal-card glass">
            <div className="metal-symbol">{m.symbol}</div>
            <h4 style={{ fontSize: '1.2rem', margin: '0.5rem 0' }}>{m.name}</h4>
            <div className="metal-limit">
              <ShieldCheck size={14} />
              Standard Limit: <span className="limit-tag">{m.standard_limit} mg/L</span>
            </div>
            <div className="impact-list">
              <p><strong>Health Impact:</strong></p>
              <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>{m.health_effects}</p>
            </div>
            <button className="view-btn" onClick={() => handleLearnMore(m.name)}>
                Understand More <ExternalLink size={12} style={{ marginLeft: '4px' }} />
            </button>
          </div>
        ))}
      </div>

      <div className="learning-section">
        <div className="section-header" style={{ marginBottom: '1.5rem' }}>
            <h3><BookOpen size={20} style={{marginRight: '8px', verticalAlign: 'middle', color: 'var(--primary)'}}/> Knowledge Base</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Articles and research snippets</p>
        </div>
        
        <div className="materials-list">
          {materials.map(mat => (
              <div key={mat.id} className="material-card glass animate-fade-in">
                <div className="material-icon">
                    <Info size={24} />
                </div>
                <div className="material-info">
                    <h4>{mat.title}</h4>
                    <p>{mat.content_markdown}</p>
                </div>
              </div>
          ))}
        </div>
      </div>
    </div>
  );
}
