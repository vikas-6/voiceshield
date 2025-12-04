import React, { useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Separator } from './ui/separator';
import StatusBadge from './StatusBadge';
import { Clock, MessageSquare, AlertCircle, Play, Pause, Volume2 } from 'lucide-react';
import { format } from 'date-fns';

const EmergencyCard = ({ event }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

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

  const playAssistantResponse = async () => {
    try {
      setIsPlaying(true);
      
      // Fetch audio from backend
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
      const audioUrl = `${backendUrl}/api/audio/${event.id}`;
      
      const response = await fetch(audioUrl);
      if (!response.ok) {
        throw new Error(`Failed to fetch audio: ${response.status}`);
      }
      
      const audioBlob = await response.blob();
      const audioUrlObject = URL.createObjectURL(audioBlob);
      
      // Play audio
      const audio = new Audio(audioUrlObject);
      audio.play();
      
      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrlObject);
      };
      
      audio.onerror = (error) => {
        console.error('Error playing audio:', error);
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrlObject);
      };
      
    } catch (error) {
      console.error('Error playing audio:', error);
      setIsPlaying(false);
    }
  };

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

        {/* Assistant Reply with Audio Playback */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-sky-600" />
            <h3 className="font-semibold text-slate-800">AI Assistant Response</h3>
          </div>
          <div 
            className="bg-sky-50 rounded-lg p-4 border border-sky-200"
            data-testid="assistant-reply"
          >
            <p className="text-slate-700 leading-relaxed mb-4">{event.assistant_reply}</p>
            
            {/* Audio Playback Controls */}
            <div className="flex items-center gap-3 mt-4 pt-3 border-t border-sky-100">
              <button
                onClick={playAssistantResponse}
                disabled={isPlaying}
                className="flex items-center gap-2 bg-sky-600 hover:bg-sky-700 disabled:bg-sky-400 text-white px-4 py-2 rounded-lg transition-colors"
              >
                {isPlaying ? (
                  <>
                    <Pause className="h-4 w-4" />
                    <span>Playing...</span>
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    <span>Listen to Response</span>
                  </>
                )}
              </button>
              <Volume2 className="h-5 w-5 text-sky-600" />
              <span className="text-sm text-slate-600">AI Generated Audio</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EmergencyCard;
