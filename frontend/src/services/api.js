import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API = `${BACKEND_URL}/api`;

/**
 * Send audio recording to backend for processing
 * @param {Blob} audioBlob - Audio blob from recording
 * @returns {Promise} - Promise with emergency event data
 */
export const processVoice = async (audioBlob) => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');

  try {
    const response = await axios.post(`${API}/voice`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error processing voice:', error);
    throw error;
  }
};

/**
 * Get recent emergency events
 * @param {number} limit - Maximum number of events to retrieve
 * @returns {Promise} - Promise with events list
 */
export const getEvents = async (limit = 50) => {
  try {
    const response = await axios.get(`${API}/events`, {
      params: { limit },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching events:', error);
    throw error;
  }
};

/**
 * Create WebSocket connection for real-time events
 * @returns {WebSocket} - WebSocket instance
 */
export const createWebSocket = () => {
  const wsUrl = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');
  const ws = new WebSocket(`${wsUrl}/ws`);
  return ws;
};
