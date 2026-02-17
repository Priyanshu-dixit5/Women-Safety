# Quick Start Guide - Flask Backend Integration

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Flask Server
**Windows:**
```bash
run_server.bat
```

**Linux/Mac:**
```bash
chmod +x run_server.sh
./run_server.sh
```

**Or manually:**
```bash
python app.py
```

You should see:
```
Database initialized successfully!
Starting Flask server on http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

### Step 3: Open the Application
Open `pg1.html` in your web browser. The frontend will automatically connect to the Flask backend.

## ✅ What's Changed

### Backend (New)
- **Flask Server** (`app.py`) - Handles all API requests
- **SQLite Database** (`safeguard.db`) - Stores user data, contacts, routes, and location history
- **RESTful API** - Clean endpoints for all operations

### Frontend (Updated)
- **pg1.html** - Now syncs with Flask backend instead of localStorage only
- **API Integration** - All registration, login, and password reset operations use the backend
- **Error Handling** - Better error messages and connection checking

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register` | POST | Register new user |
| `/api/login` | POST | User login |
| `/api/verify-email` | POST | Verify email for password reset |
| `/api/reset-password` | POST | Reset password |
| `/api/contacts` | GET/POST | Manage emergency contacts |
| `/api/routes` | GET/POST | Manage safe routes |
| `/api/location` | POST | Save location history |

## 🐛 Troubleshooting

### "Cannot connect to server" Error
- Make sure Flask server is running (`python app.py`)
- Check that server is on `http://127.0.0.1:5000`
- Verify no firewall is blocking the connection

### 404 Errors
- All endpoints are prefixed with `/api/`
- Check browser console for detailed error messages
- Verify Flask server logs for request details

### Database Errors
- Delete `safeguard.db` and restart server (database will be recreated)
- Check file permissions in the project directory

## 📝 Notes

- The database is automatically created on first run
- All passwords are hashed using SHA256
- CORS is enabled for local development
- The server runs in debug mode by default

## 🔄 Migration from localStorage

If you have existing data in localStorage:
1. The app will still work, but new registrations will go to the database
2. You can manually migrate data by registering again through the new system
3. Old localStorage data will remain but won't sync with the backend
