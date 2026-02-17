# Quick Setup Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask Server
```bash
# Windows
start.bat

# Linux/Mac
python app.py
```

The server will:
- ✅ Automatically create the SQLite database (`safeguard.db`)
- ✅ Start on `http://127.0.0.1:5000`
- ✅ Open your browser automatically

## 🔄 UI Flow

1. **Login/Register Page** (`pg1.html`)
   - Register a new account or login
   - After successful login → redirects to main app

2. **Main App** (`index.html`)
   - Dashboard with all features
   - Contacts, Routes, SOS, etc.
   - Logout button → redirects back to login page

3. **Logout**
   - Clears session
   - Redirects to login/register page

## 📊 Database Synchronization

- **Single Database**: Both web and desktop use the same `safeguard.db` file
- **Real-time Sync**: Changes are immediately available across all interfaces
- **Sync Logging**: All operations are logged in the `sync_status` table

## 🔑 Default Access

- **URL**: `http://127.0.0.1:5000`
- **Database**: `safeguard.db` (created automatically)

## ✅ Features

- ✅ User Registration & Login
- ✅ Password Reset (via security questions)
- ✅ Emergency Contacts Management
- ✅ Safe Routes Management
- ✅ Location History
- ✅ Sync Status Tracking
- ✅ CORS enabled for local development

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill
```

### Database Issues
- Delete `safeguard.db` to reset (will be recreated automatically)
- Make sure no other process is using the database

### Cannot Connect
- Verify Flask server is running
- Check `http://127.0.0.1:5000/health` in browser
- Check firewall settings
