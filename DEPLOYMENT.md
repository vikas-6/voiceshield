# 🚀 Voice Shield - Deployment Guide

Complete guide to deploy Voice Emergency Assistant to production.

## 📋 Prerequisites

Before deploying, ensure you have:

1. ✅ **GitHub Account** - Code repository (already set up)
2. ✅ **MongoDB Atlas** - Free cluster with connection string
3. ✅ **ElevenLabs API Key** - For speech-to-text and text-to-speech
4. ✅ **Google Gemini API Key** - For AI response generation
5. 🆕 **Vercel Account** - For frontend hosting (free tier)
6. 🆕 **Render Account** - For backend hosting (free tier)

---

## 🔐 Security Checklist

Before deploying, verify:

- ✅ `.env` files are gitignored
- ✅ No API keys in code or Git history
- ✅ `.env.example` files created (without real keys)
- ✅ Test files removed from repository

---

## 📦 Part 1: Deploy Backend to Render

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your `voice-shield` repository
3. Configure build settings:
   - **Name**: `voice-shield-backend`
   - **Region**: Oregon (US West) or closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

### Step 3: Add Environment Variables
In Render dashboard, add these environment variables:

```bash
MONGO_URL=mongodb+srv://<your-connection-string>
DB_NAME=voice_assistant_db
ELEVENLABS_API_KEY=sk_<your-elevenlabs-key>
GEMINI_API_KEY=AIzaSy<your-gemini-key>
CORS_ORIGINS=*
```

> [!WARNING]
> Replace `<your-connection-string>`, `<your-elevenlabs-key>`, and `<your-gemini-key>` with your actual credentials!

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Copy your backend URL (e.g., `https://voice-shield-backend.onrender.com`)

---

## 🎨 Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Authorize Vercel to access your repositories

### Step 2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Select your `voice-shield` repository
3. Configure project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `yarn build`
   - **Output Directory**: `build`
   - **Install Command**: `yarn install`

### Step 3: Add Environment Variable
In Vercel dashboard, add:

```bash
REACT_APP_BACKEND_URL=https://voice-shield-backend.onrender.com
```

> [!IMPORTANT]
> Use the exact backend URL from Render (from Step 4 above)!

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait for deployment (3-5 minutes)
3. Get your frontend URL (e.g., `https://voice-shield.vercel.app`)

---

## 🔄 Part 3: Update CORS Settings

After both are deployed, update the backend CORS settings:

1. Go to Render dashboard → Your backend service
2. Update `CORS_ORIGINS` environment variable:
   ```bash
   CORS_ORIGINS=https://voice-shield.vercel.app
   ```
3. Save changes - Render will auto-redeploy

---

## ✅ Part 4: Verify Deployment

### Test the Application

1. Open your Vercel URL: `https://voice-shield.vercel.app`
2. Click the microphone button
3. Allow microphone permissions
4. Record a test emergency: *"Help! There's a fire!"*
5. Verify:
   - ✅ Recording indicator appears
   - ✅ Transcription is displayed
   - ✅ Emergency classification shows
   - ✅ AI response is generated
   - ✅ Audio plays back
   - ✅ Event appears in the feed

### Check Backend Health

Open in browser: `https://voice-shield-backend.onrender.com/api/status`

Should return:
```json
{
  "status": "healthy",
  "mongodb": "connected",
  "timestamp": "..."
}
```

---

## 🐛 Troubleshooting

### Frontend shows "Network Error"
- **Fix**: Check `REACT_APP_BACKEND_URL` in Vercel environment variables
- Ensure it matches exactly with Render backend URL

### Backend returns "CORS Error"
- **Fix**: Update `CORS_ORIGINS` in Render to match your Vercel URL
- Verify URL includes `https://` prefix

### "MongoDB connection failed"
- **Fix**: Check `MONGO_URL` in Render environment variables
- Ensure MongoDB Atlas allows connections from anywhere (0.0.0.0/0)

### "ElevenLabs API Error"
- **Fix**: Verify `ELEVENLABS_API_KEY` is correctly set in Render
- Check ElevenLabs account is active and within quota

### Render service sleeping (free tier)
- **Note**: Free tier services sleep after 15 minutes of inactivity
- First request after sleeping may take 30-60 seconds to wake up

---

## 📝 Share with Professor

Once verified, share these links:

**Live Demo**: `https://voice-shield.vercel.app`  
**GitHub Repo**: `https://github.com/vikas-6/voice-shield`

---

## 🔄 Updating the Deployment

When you make changes to the code:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Vercel**: Auto-deploys on every push to `main`
3. **Render**: Auto-deploys on every push to `main`

---

## 💰 Cost Breakdown

- **Vercel**: Free (100GB bandwidth/month)
- **Render**: Free (750 hours/month)
- **MongoDB Atlas**: Free (512MB storage)
- **ElevenLabs**: Free tier with limits
- **Google Gemini**: Free tier

**Total Monthly Cost**: $0 🎉

---

## 📞 Support

If you encounter issues during deployment:

1. Check Render deployment logs
2. Check Vercel deployment logs
3. Use browser DevTools → Network tab to debug API calls
4. Verify all environment variables are set correctly

---

**🎓 Ready to impress your professor!** Good luck with the demo! 🚀
