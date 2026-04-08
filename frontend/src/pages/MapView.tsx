import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import { mockSamples } from '../services/mockData';
import L from 'leaflet';
import './MapView.css';

// Fix for default marker icons in Leaflet with React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapView: React.FC = () => {
    const [samples, setSamples] = useState<any[]>(mockSamples);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/researcher/samples')
            .then(res => {
                if (res.data && res.data.length > 0) {
                     setSamples(res.data);
                }
            })
            .catch(err => console.error("Failed to fetch live samples, using mock.", err));
    }, []);

    const center: [number, number] = [23.5937, 78.9629]; // Center of India

    const getRiskColor = (risk: string) => {
        switch (risk) {
            case 'High': return '#ef4444';
            case 'Low': return '#f59e0b';
            case 'Safe': return '#10b981';
            default: return '#6366f1';
        }
    };

    return (
        <div className="map-view-container animate-fade-in">
            <div className="map-header glass">
                <h3>Pollution Heatmap</h3>
                <div className="map-legend">
                    <span className="legend-item"><i style={{ background: '#ef4444' }}></i> High Risk</span>
                    <span className="legend-item"><i style={{ background: '#f59e0b' }}></i> Low Risk</span>
                    <span className="legend-item"><i style={{ background: '#10b981' }}></i> Safe</span>
                </div>
            </div>

            <div className="map-wrapper glass">
                <MapContainer center={center} zoom={5} style={{ height: '600px', width: '100%', borderRadius: '12px' }}>
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {samples.map(sample => {
                        const lat = sample.lat || sample.latitude;
                        const lng = sample.lng || sample.longitude;
                        if (!lat || !lng) return null;
                        
                        const riskLevel = sample.risk?.risk_category || sample.risk_level || 'Safe';
                        const hpiScore = sample.risk?.hpi || sample.hpi_score || 0;
                        const locName = sample.source_type || sample.location_name || 'Sampling Point';

                        return (
                        <React.Fragment key={sample.id}>
                            <Marker position={[lat, lng]}>
                                <Popup>
                                    <div className="map-popup">
                                        <h4>{locName}</h4>
                                        <p>Risk: <strong style={{ color: getRiskColor(riskLevel) }}>{riskLevel}</strong></p>
                                        <p>HPI Score: {hpiScore}</p>
                                    </div>
                                </Popup>
                            </Marker>
                            <Circle
                                center={[lat, lng]}
                                radius={20000}
                                pathOptions={{
                                    fillColor: getRiskColor(riskLevel),
                                    color: getRiskColor(riskLevel),
                                    fillOpacity: 0.3
                                }}
                            />
                        </React.Fragment>
                        );
                    })}
                </MapContainer>
            </div>
        </div>
    );
};

export default MapView;
