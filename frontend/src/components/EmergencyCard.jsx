import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Separator } from './ui/separator';
import StatusBadge from './StatusBadge';
import { Clock, MessageSquare, AlertCircle } from 'lucide-react';
import { format } from 'date-fns';

const EmergencyCard = ({ event }) => {
  if (!event) {
    return (
      <Card className="w-full" data-testid="emergency-card-empty">
        <CardContent className="flex flex-col items-center justify-center py-12">
          <AlertCircle className="h-16 w-16 text-slate-300 mb-4" />
          <p className="text-slate-500 text-center">
            Record a voice message to see results here
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full shadow-md" data-testid="emergency-card">
      <CardHeader className="bg-slate-50">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold text-slate-800">Emergency Analysis</CardTitle>
          <div className="flex items-center gap-2 text-sm text-slate-600" data-testid="event-timestamp">
            <Clock className="h-4 w-4" />
            {event.timestamp ? format(new Date(event.timestamp), 'MMM dd, yyyy HH:mm:ss') : 'N/A'}
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="pt-6 space-y-6">
        {/* Emergency Type and Severity */}
        <div>
          <StatusBadge type={event.type} severity={event.severity} />
        </div>

        <Separator />

        {/* Transcript */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-sky-600" />
            <h3 className="font-semibold text-slate-800">Transcript</h3>
          </div>
          <div 
            className="bg-slate-50 rounded-lg p-4 border border-slate-200"
            data-testid="event-transcript"
          >
            <p className="text-slate-700 leading-relaxed">{event.transcript}</p>
          </div>
        </div>

        <Separator />

        {/* Assistant Reply */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-sky-600" />
            <h3 className="font-semibold text-slate-800">AI Assistant Response</h3>
          </div>
          <div 
            className="bg-sky-50 rounded-lg p-4 border border-sky-200"
            data-testid="assistant-reply"
          >
            <p className="text-slate-700 leading-relaxed">{event.assistant_reply}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EmergencyCard;
