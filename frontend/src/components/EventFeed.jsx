import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Badge } from './ui/badge';
import { Clock, Flame, Heart, Shield, Car, CheckCircle } from 'lucide-react';
import { format } from 'date-fns';

const EventFeed = ({ events }) => {
  const getEventIcon = (type) => {
    switch (type) {
      case 'FIRE':
        return <Flame className="h-4 w-4 text-orange-600" />;
      case 'MEDICAL':
        return <Heart className="h-4 w-4 text-red-600" />;
      case 'VIOLENCE':
        return <Shield className="h-4 w-4 text-purple-600" />;
      case 'ACCIDENT':
        return <Car className="h-4 w-4 text-yellow-600" />;
      case 'NORMAL':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      default:
        return <CheckCircle className="h-4 w-4 text-gray-600" />;
    }
  };

  const getEventColor = (type) => {
    switch (type) {
      case 'FIRE':
        return 'border-l-orange-500';
      case 'MEDICAL':
        return 'border-l-red-500';
      case 'VIOLENCE':
        return 'border-l-purple-500';
      case 'ACCIDENT':
        return 'border-l-yellow-500';
      case 'NORMAL':
        return 'border-l-green-500';
      default:
        return 'border-l-gray-500';
    }
  };

  return (
    <Card className="w-full h-full shadow-md" data-testid="event-feed">
      <CardHeader className="bg-slate-50 pb-4">
        <CardTitle className="text-xl font-bold text-slate-800">
          Real-Time Event Feed
        </CardTitle>
        <p className="text-sm text-slate-600 mt-1">
          {events.length} {events.length === 1 ? 'event' : 'events'} logged
        </p>
      </CardHeader>
      
      <CardContent className="p-0">
        <ScrollArea className="h-[600px]" data-testid="event-feed-scroll">
          {events.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 px-4">
              <div className="text-slate-400 text-center">
                <Clock className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p className="text-sm">No events yet</p>
                <p className="text-xs mt-1">Events will appear here in real-time</p>
              </div>
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {events.map((event, index) => (
                <div
                  key={event.id || index}
                  className={`p-4 border-l-4 ${getEventColor(event.type)} hover:bg-slate-50 transition-colors`}
                  data-testid={`event-item-${index}`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start gap-3 flex-1 min-w-0">
                      <div className="mt-1">
                        {getEventIcon(event.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant="secondary" className="text-xs">
                            {event.type}
                          </Badge>
                          <span className="text-xs text-slate-500">
                            Severity: {event.severity}/10
                          </span>
                        </div>
                        <p className="text-sm text-slate-700 line-clamp-2 mb-1">
                          {event.transcript}
                        </p>
                        <div className="flex items-center gap-1 text-xs text-slate-500">
                          <Clock className="h-3 w-3" />
                          {event.timestamp ? format(new Date(event.timestamp), 'HH:mm:ss') : 'N/A'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default EventFeed;
