import React, { useState, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import L from 'leaflet';
import { Filter, MapPin, Loader2, ShieldCheck } from 'lucide-react';
import './MapView.css';

const MapView: React.FC = () => {
    const [samples, setSamples] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [stateFilter, setStateFilter] = useState('');
    const [districtFilter, setDistrictFilter] = useState('');
    const [riskFilter, setRiskFilter] = useState('');

    useEffect(() => {
        const fetchSamples = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/researcher/samples');
                setSamples(response.data);
            } catch (err) {
                console.error("Failed to fetch live samples", err);
            } finally {
                setLoading(false);
            }
        };
        fetchSamples();
    }, []);

    // Generate unique options for dropdowns
    const { states, districts } = useMemo(() => {
        const uniqueStates = Array.from(new Set(samples.map(s => s.state).filter(Boolean))) as string[];
        const uniqueDistricts = Array.from(new Set(samples.filter(s => stateFilter === '' || s.state === stateFilter).map(s => s.district).filter(Boolean))) as string[];
        return { 
            states: uniqueStates.sort(), 
            districts: uniqueDistricts.sort() 
        };
    }, [samples, stateFilter]);

    const filteredSamples = samples.filter(sample => {
        const matchesState = stateFilter === '' || sample.state === stateFilter;
        const matchesDistrict = districtFilter === '' || sample.district === districtFilter;
        const matchesRisk = riskFilter === '' || (sample.risk?.risk_category === riskFilter);
        return matchesState && matchesDistrict && matchesRisk;
    });

    const center: [number, number] = [23.5937, 78.9629]; // Center of India

    const getRiskColor = (risk: string) => {
        switch (risk) {
            case 'Hazardous': return '#ef4444';
            case 'Moderately Polluted': return '#f59e0b';
            case 'Safe': return '#10b981';
            default: return '#6366f1';
        }
    };

    const createCustomIcon = (risk: string) => {
        const color = getRiskColor(risk);
        return L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.4);"></div>`,
            iconSize: [14, 14],
            iconAnchor: [7, 7]
        });
    };

    if (loading) {
        return (
            <div className="map-view-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
            </div>
        );
    }

    return (
        <div className="map-view-container animate-fade-in">
            <div className="map-header glass" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="header-left">
                    <h3>Spatial Analysis Map</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Found {filteredSamples.length} locations matching criteria</p>
                </div>
                
                <div className="map-filters" style={{ display: 'flex', gap: '1rem' }}>
                    <div className="search-box glass" style={{ width: '160px', padding: '0 0.5rem' }}>
                        <Filter size={14} style={{ opacity: 0.5 }} />
                        <select 
                            value={stateFilter} 
                            onChange={(e) => { setStateFilter(e.target.value); setDistrictFilter(''); }}
                            className="filter-select"
                            style={{ fontSize: '0.75rem' }}
                        >
                            <option value="">All States</option>
                            {states.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                    </div>
                    <div className="search-box glass" style={{ width: '160px', padding: '0 0.5rem' }}>
                        <MapPin size={14} style={{ opacity: 0.5 }} />
                        <select 
                            value={districtFilter} 
                            onChange={(e) => setDistrictFilter(e.target.value)}
                            className="filter-select"
                            style={{ fontSize: '0.75rem' }}
                            disabled={!stateFilter}
                        >
                            <option value="">All Districts</option>
                            {districts.map(d => <option key={d} value={d}>{d}</option>)}
                        </select>
                    </div>
                    <div className="search-box glass" style={{ width: '160px', padding: '0 0.5rem' }}>
                        <ShieldCheck size={14} style={{ opacity: 0.5 }} />
                        <select 
                            value={riskFilter} 
                            onChange={(e) => setRiskFilter(e.target.value)}
                            className="filter-select"
                            style={{ fontSize: '0.75rem' }}
                        >
                            <option value="">All Quality</option>
                            <option value="Safe">Safe</option>
                            <option value="Moderately Polluted">Polluted</option>
                            <option value="Hazardous">Hazardous</option>
                        </select>
                    </div>
                </div>

                <div className="map-legend" style={{ marginLeft: '1rem' }}>
                    <span className="legend-item"><i style={{ background: '#ef4444' }}></i> Hazardous</span>
                    <span className="legend-item"><i style={{ background: '#f59e0b' }}></i> Polluted</span>
                    <span className="legend-item"><i style={{ background: '#10b981' }}></i> Safe</span>
                </div>
            </div>

            <div className="map-wrapper glass">
                <MapContainer center={center} zoom={5} style={{ height: '600px', width: '100%', borderRadius: '12px' }}>
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {filteredSamples.map(sample => {
                        const lat = sample.lat;
                        const lng = sample.lng;
                        if (!lat || !lng) return null;
                        
                        const riskLevel = sample.risk?.risk_category || 'Safe';
                        const hpiScore = sample.risk?.hpi || 0;
                        const locName = sample.location_name || 'Sampling Point';

                        return (
                            <Marker 
                                key={sample.id} 
                                position={[lat, lng]} 
                                icon={createCustomIcon(riskLevel)}
                            >
                                <Popup>
                                    <div className="map-popup" style={{ minWidth: '220px' }}>
                                        <h4 style={{ margin: '0 0 8px 0', borderBottom: '1px solid #eee', paddingBottom: '4px', fontSize: '1rem' }}>{locName}</h4>
                                        <div style={{ fontSize: '0.85rem' }}>
                                            <p style={{ margin: '4px 0' }}>Region: <strong>{sample.district}, {sample.state}</strong></p>
                                            <p style={{ margin: '4px 0' }}>Classification: <strong style={{ color: getRiskColor(riskLevel) }}>{riskLevel}</strong></p>
                                            <p style={{ margin: '4px 0' }}>HPI Score: <strong>{hpiScore.toFixed(2)}</strong></p>
                                            
                                            <div style={{ marginTop: '12px', background: 'rgba(255,255,255,0.05)', padding: '8px', borderRadius: '4px' }}>
                                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px' }}>
                                                    {sample.measurements.map((m: any, i: number) => (
                                                        <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0' }}>
                                                            <span style={{ fontWeight: '600' }}>{m.metal}:</span>
                                                            <span>{m.concentration.toFixed(4)}</span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </Popup>
                            </Marker>
                        );
                    })}
                </MapContainer>
            </div>
        </div>
    );
};

export default MapView;
