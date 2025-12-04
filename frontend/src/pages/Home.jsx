import React, { useState, useEffect, useRef } from 'react';
import MicRecorder from '../components/MicRecorder';
import EmergencyCard from '../components/EmergencyCard';
import EventFeed from '../components/EventFeed';
import { createWebSocket, getEvents } from '../services/api';
import { Toaster } from '../components/ui/sonner';
import { toast } from 'sonner';

const Home = () => {
  const [currentEvent, setCurrentEvent] = useState(null);
  const [events, setEvents] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);
  const wsRef = useRef(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = createWebSocket();
        
        ws.onopen = () => {
          console.log('WebSocket connected');
          setWsConnected(true);
          toast.success('Real-time connection established');
        };

        ws.onmessage = (event) => {
          try {
            const newEvent = JSON.parse(event.data);
            console.log('New event received:', newEvent);
            
            // Only process valid emergency events (skip hot-reload messages)
            if (newEvent.id && newEvent.transcript && newEvent.type) {
              // Add new event to the beginning of the list
              setEvents((prev) => [newEvent, ...prev]);
              
              // Show notification for high severity events
              if (newEvent.severity >= 7) {
                toast.error(`High Severity ${newEvent.type} Event Detected!`, {
                  description: newEvent.transcript.substring(0, 100),
                });
              }
            }
          } catch (err) {
            console.error('Error parsing WebSocket message:', err);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setWsConnected(false);
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setWsConnected(false);
          
          // Attempt to reconnect after 3 seconds
          setTimeout(() => {
            console.log('Attempting to reconnect WebSocket...');
            connectWebSocket();
          }, 3000);
        };

        wsRef.current = ws;
      } catch (error) {
        console.error('Error creating WebSocket:', error);
      }
    };

    connectWebSocket();

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Load initial events
  useEffect(() => {
    const loadEvents = async () => {
      try {
        const data = await getEvents(50);
        setEvents(data.events || []);
      } catch (error) {
        console.error('Error loading events:', error);
      }
    };

    loadEvents();
  }, []);

  const handleRecordingResult = (result) => {
    setCurrentEvent(result);
    toast.success('Voice processed successfully', {
      description: `Emergency type: ${result.type}`,
    });
  };

  const handleRecordingError = (error) => {
    toast.error('Recording Error', {
      description: error,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white" data-testid="home-page">
      <Toaster position="top-right" richColors />
      
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-slate-800">
                🎙️ Voice Emergency Assistant
              </h1>
              <p className="text-slate-600 mt-1">Real-Time Voice Emergency Detection</p>
            </div>
            <div className="flex items-center gap-2">
              <div
                className={`h-3 w-3 rounded-full ${
                  wsConnected ? 'bg-green-500' : 'bg-red-500'
                } animate-pulse`}
                data-testid="ws-status-indicator"
              />
              <span className="text-sm text-slate-600">
                {wsConnected ? 'Live' : 'Connecting...'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Recorder and Current Event */}
          <div className="lg:col-span-2 space-y-8">
            {/* Recorder Section */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12">
              <MicRecorder
                onResult={handleRecordingResult}
                onError={handleRecordingError}
              />
            </div>

            {/* Current Event Display */}
            <EmergencyCard event={currentEvent} />
          </div>

          {/* Right Column - Event Feed */}
          <div className="lg:col-span-1">
            <EventFeed events={events} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-16">
        <div className="container mx-auto px-6 py-6 text-center text-sm text-slate-600">
          <p>Voice Emergency Assistant</p>
          <p className="mt-1 text-xs">
            Using advanced voice processing for emergency detection.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;