#!/bin/bash

# Voice Emergency Assistant - Production Deployment Script

echo "🚀 Starting Voice Emergency Assistant Production Deployment..."

# Create log directory
mkdir -p logs

# Deploy Backend
echo "🔧 Deploying Backend..."
cd backend

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start backend server in background with logging
echo "🏃 Starting backend server..."
nohup uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started with PID: $BACKEND_PID"

cd ..

# Deploy Frontend
echo "🎨 Deploying Frontend..."
cd frontend

# Install Node dependencies
echo "📦 Installing Node dependencies..."
yarn install

# Build production frontend
echo "🔨 Building production frontend..."
yarn build

# Serve frontend
echo "🏃 Serving frontend..."
nohup yarn global add serve && nohup serve -s build -l 3000 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started with PID: $FRONTEND_PID"

cd ..

echo "🎉 Deployment complete!"
echo "📊 Backend running on http://localhost:8000"
echo "📊 Frontend running on http://localhost:3000"
echo "📝 Logs available in the logs/ directory"
echo "🛑 To stop services, run: pkill -f 'uvicorn|serve'"