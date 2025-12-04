import React from 'react';
import { AlertTriangle, Flame, Heart, Shield, Car, CheckCircle } from 'lucide-react';
import { Badge } from './ui/badge';

const StatusBadge = ({ type, severity }) => {
  const getTypeConfig = () => {
    switch (type) {
      case 'FIRE':
        return {
          icon: Flame,
          label: 'Fire Emergency',
          color: 'bg-orange-100 text-orange-800 border-orange-300',
        };
      case 'MEDICAL':
        return {
          icon: Heart,
          label: 'Medical Emergency',
          color: 'bg-red-100 text-red-800 border-red-300',
        };
      case 'VIOLENCE':
        return {
          icon: Shield,
          label: 'Violence Threat',
          color: 'bg-purple-100 text-purple-800 border-purple-300',
        };
      case 'ACCIDENT':
        return {
          icon: Car,
          label: 'Accident',
          color: 'bg-yellow-100 text-yellow-800 border-yellow-300',
        };
      case 'NORMAL':
        return {
          icon: CheckCircle,
          label: 'Normal',
          color: 'bg-green-100 text-green-800 border-green-300',
        };
      default:
        return {
          icon: AlertTriangle,
          label: 'Unknown',
          color: 'bg-gray-100 text-gray-800 border-gray-300',
        };
    }
  };

  const config = getTypeConfig();
  const Icon = config.icon;

  return (
    <div className="flex flex-col gap-2" data-testid="status-badge">
      <Badge
        variant="outline"
        className={`${config.color} px-4 py-2 text-sm font-semibold inline-flex items-center gap-2 w-fit`}
        data-testid={`badge-${type.toLowerCase()}`}
      >
        <Icon className="h-4 w-4" />
        {config.label}
      </Badge>
      
      {/* Severity indicator */}
      <div className="flex items-center gap-2" data-testid="severity-indicator">
        <span className="text-sm font-medium text-slate-600">Severity:</span>
        <div className="flex gap-1">
          {[...Array(10)].map((_, i) => (
            <div
              key={i}
              className={`h-2 w-6 rounded-full ${
                i < severity
                  ? severity <= 3
                    ? 'bg-green-500'
                    : severity <= 6
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                  : 'bg-slate-200'
              }`}
            />
          ))}
        </div>
        <span className="text-sm font-bold text-slate-700" data-testid="severity-value">
          {severity}/10
        </span>
      </div>
    </div>
  );
};

export default StatusBadge;
