import React, { useState, useRef } from 'react';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { processVoice } from '../services/api';

const MicRecorder = ({ onResult, onError }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
        
        // Process the recording
        await processRecording(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      onError('Failed to access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processRecording = async (audioBlob) => {
    setIsProcessing(true);
    try {
      const result = await processVoice(audioBlob);
      onResult(result);
    } catch (error) {
      console.error('Error processing recording:', error);
      onError('Failed to process recording. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-6" data-testid="mic-recorder">
      <div className="relative">
        {/* Pulse animation when recording */}
        {isRecording && (
          <div className="absolute inset-0 -m-4">
            <div className="absolute inset-0 rounded-full bg-red-500 opacity-20 animate-ping" />
            <div className="absolute inset-0 rounded-full bg-red-500 opacity-20 animate-pulse" />
          </div>
        )}
        
        {/* Main recording button */}
        <Button
          data-testid="record-button"
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
          size="lg"
          className={`relative h-32 w-32 rounded-full text-white shadow-lg transition-all duration-300 ${
            isRecording
              ? 'bg-red-600 hover:bg-red-700 scale-110'
              : 'bg-sky-600 hover:bg-sky-700'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          {isProcessing ? (
            <Loader2 className="h-12 w-12 animate-spin" />
          ) : isRecording ? (
            <MicOff className="h-12 w-12" />
          ) : (
            <Mic className="h-12 w-12" />
          )}
        </Button>
      </div>

      {/* Status text */}
      <div className="text-center">
        {isProcessing ? (
          <p className="text-lg font-medium text-slate-700" data-testid="status-processing">
            Processing your recording...
          </p>
        ) : isRecording ? (
          <p className="text-lg font-medium text-red-600 animate-pulse" data-testid="status-recording">
            Recording... Click to stop
          </p>
        ) : (
          <p className="text-lg font-medium text-slate-600" data-testid="status-ready">
            Click to start recording
          </p>
        )}
      </div>
    </div>
  );
};

export default MicRecorder;
