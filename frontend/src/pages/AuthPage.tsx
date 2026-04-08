import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './AuthPage.css'; // Minimal inline styles below or similar to existing css

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export default function AuthPage() {
  const [view, setView] = useState<'login' | 'register-citizen' | 'register-researcher'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (view === 'login') {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, { email, password });
        localStorage.setItem('token', response.data.access_token);
        const userRes = await axios.get(`${API_BASE_URL}/users/me`, {
          headers: { Authorization: `Bearer ${response.data.access_token}` }
        });
        localStorage.setItem('role', userRes.data.role);
        navigate('/');
      } else {
        const role = view === 'register-researcher' ? 'researcher' : 'citizen';
        await axios.post(`${API_BASE_URL}/users/register`, {
          email, password, full_name: role, role, is_active: true
        });
        alert('Registered successfully! Please login.');
        setView('login');
      }
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Authentication error. Please check your credentials.';
      alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
  };

  return (
    <div className="auth-container animate-fade-in" style={{ padding: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <div className="card glass" style={{ maxWidth: '450px', width: '100%' }}>
        
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid var(--border)', paddingBottom: '10px' }}>
             <button 
                onClick={() => setView('login')} 
                style={{ background: 'none', color: view === 'login' ? 'var(--primary)' : 'var(--text-muted)', fontWeight: view === 'login' ? 'bold' : 'normal', flex: 1 }}
             >
                Login
             </button>
             <button 
                onClick={() => setView('register-citizen')} 
                style={{ background: 'none', color: view === 'register-citizen' ? 'var(--primary)' : 'var(--text-muted)', fontWeight: view === 'register-citizen' ? 'bold' : 'normal', flex: 1 }}
             >
                Citizen Sign-Up
             </button>
             <button 
                onClick={() => setView('register-researcher')} 
                style={{ background: 'none', color: view === 'register-researcher' ? 'var(--primary)' : 'var(--text-muted)', fontWeight: view === 'register-researcher' ? 'bold' : 'normal', flex: 1 }}
             >
                Researcher Sign-Up
             </button>
        </div>

        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center', color: 'var(--text-main)' }}>
            {view === 'login' ? 'Welcome Back' : view === 'register-citizen' ? 'Join as Citizen' : 'Join as Researcher'}
        </h2>
        
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
          <div>
              <label style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '5px', display: 'block' }}>Email Address</label>
              <input type="email" placeholder="e.g. citizen1@example.com" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%' }} />
          </div>
          <div>
              <label style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '5px', display: 'block' }}>Password</label>
              <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%' }} />
          </div>
          
          <button type="submit" className="action-btn primary glass" style={{ width: '100%', justifyContent: 'center', marginTop: '10px' }}>
            {view === 'login' ? 'Secure Login' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  );
}
