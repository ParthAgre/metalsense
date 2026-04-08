import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
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
                    {mockSamples.map(sample => (
                        <React.Fragment key={sample.id}>
                            <Marker position={[sample.latitude, sample.longitude]}>
                                <Popup>
                                    <div className="map-popup">
                                        <h4>{sample.location_name}</h4>
                                        <p>Risk: <strong style={{ color: getRiskColor(sample.risk_level) }}>{sample.risk_level}</strong></p>
                                        <p>HPI Score: {sample.hpi_score}</p>
                                    </div>
                                </Popup>
                            </Marker>
                            <Circle
                                center={[sample.latitude, sample.longitude]}
                                radius={20000}
                                pathOptions={{
                                    fillColor: getRiskColor(sample.risk_level),
                                    color: getRiskColor(sample.risk_level),
                                    fillOpacity: 0.3
                                }}
                            />
                        </React.Fragment>
                    ))}
                </MapContainer>
            </div>
        </div>
    );
};

export default MapView;
