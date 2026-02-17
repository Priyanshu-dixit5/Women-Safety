# 🛡️ SAFEGUARD - Women Safety Application

A comprehensive, **FREE** women safety application with real-time location tracking and emergency features.

## 🎯 Quick Start

1. Open `pg1.html` in your browser (login/signup page)
2. Create an account or login
3. Access the main dashboard at `index.html`

## ✨ Key Features

### 🚨 Emergency SOS System
- One-touch emergency alert
- Press and hold for 3 seconds
- Sends location to all saved contacts
- Activates loud alarm and voice alert
- Auto-shares via WhatsApp or SMS

### 📍 Real-Time Location Sharing (NEW!)
- **WhatsApp Sharing** - Share location via WhatsApp
- **SMS Sharing** - Share via text message  
- **Email Sharing** - Share via email
- **Continuous Auto-Tracking** - Auto-share every 2 minutes
- Copy Google Maps link for easy sharing

### 🚔 Dynamic Police Station Finder (NEW!)
- GPS-based automatic search
- Finds stations within 5km radius
- Shows distance to each station
- One-click directions via Google Maps
- Direct calling capability
- Uses free Overpass API (OpenStreetMap)

### 👥 Emergency Contacts Management
- Save unlimited emergency contacts
- Store names, phone numbers, relationships
- Quick access for alerts

### 🗺️ Live Location Tracking
- Interactive map with your real-time position
- Shows latitude, longitude, accuracy, speed
- Path tracking as you move
- Powered by Leaflet.js and OpenStreetMap

### 📸 Instant Camera
- Quick camera access for evidence
- Save photos locally
- Download captured images
- Clear all photos option

### 🛣️ Safe Routes
- Save frequently traveled routes
- Store home, work, and other locations
- Quick access to saved places

### 💡 Safety Tips
- Expert safety guidelines
- Tips for various situations
- Best practices for personal safety

## 💰 Cost: 100% FREE!

### No Costs For:
✅ Location tracking  
✅ Police station search  
✅ WhatsApp/SMS/Email sharing  
✅ Map display  
✅ All features  

### How It's Free:
- Browser-based Geolocation API
- OpenStreetMap (free map data)
- Overpass API (free OSM queries)
- No backend server required
- No API keys needed
- No monthly subscriptions

## 🚀 New Features Details

### Real-Time Location Sharing

**One-Time Sharing:**
1. Go to "Live Location" page
2. Wait for GPS lock
3. Click any sharing button (WhatsApp, SMS, Email)
4. Share with your contacts

**Continuous Tracking:**
1. Go to "Live Location" page
2. Click "Start Auto-Share"
3. Location shared every 2 minutes automatically
4. Click "Stop Auto-Share" when done

### Police Station Finder

**How It Works:**
1. Go to "Police Stations" page
2. Click "Find Nearby Stations" (or wait - auto-loads)
3. Allow location access
4. View nearby stations with distances
5. Click "Get Directions" or "Call"

**Emergency Numbers:**
- 112 - Emergency Response
- 100 - Police
- 1091 - Women Helpline
- 181 - Women Helpline (Nationwide)

## 📱 Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Maps:** Leaflet.js + OpenStreetMap
- **Location:** HTML5 Geolocation API
- **Police Data:** Overpass API (OpenStreetMap)
- **Storage:** LocalStorage (browser-based)
- **Sharing:** Native protocols (wa.me, tel:, mailto:, sms:)

## 🔒 Privacy & Security

- ✅ All data stored locally (browser localStorage)
- ✅ No external servers
- ✅ No data collection
- ✅ No tracking
- ✅ Privacy-first design
- ✅ You control your data

## 🌐 Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome/Edge | ✅ Full Support |
| Firefox | ✅ Full Support |
| Safari | ✅ Full Support |
| Mobile Browsers | ✅ Full Support |

## 📋 Requirements

- Modern web browser with JavaScript enabled
- GPS/Location services enabled
- Internet connection (for maps and police station search)
- WhatsApp Web setup (for desktop WhatsApp sharing)

## 🎯 Use Cases

### When to Use Continuous Tracking:
- 🌙 Walking home alone at night
- 🚕 Taking a taxi or ride-share
- 🗺️ Traveling to unfamiliar areas
- 👤 Meeting someone new
- 🎪 During large gatherings or events
- ⚠️ Any situation where you feel unsafe

### When to Use SOS:
- 🚨 Emergency situations
- ⚠️ Feeling threatened
- 🆘 Need immediate help
- 👮 When calling for police

### When to Find Police Stations:
- 🏙️ In a new city or area
- 📍 Planning safe routes
- 🚔 Need to file a report
- 🆘 Emergency situations

## 🛠️ Testing the Features

### Test Location Sharing:
1. Open "Live Location" page
2. Wait for GPS to show coordinates
3. Click "Share via WhatsApp"
4. Verify WhatsApp opens with location message
5. Try other sharing methods

### Test Police Station Finder:
1. Open "Police Stations" page
2. Allow location access
3. Wait for results to load
4. Verify stations are sorted by distance
5. Click "Get Directions" to test navigation

### Test Continuous Tracking:
1. Open "Live Location" page
2. Add at least one emergency contact
3. Click "Start Auto-Share"
4. Verify first WhatsApp tab opens
5. Wait 2 minutes for second update
6. Click "Stop Auto-Share" when done

### Test SOS System:
1. Open "SOS" page
2. Add emergency contacts first
3. Press and hold SOS button for 3 seconds
4. Verify alarm sounds
5. Check if location sharing prompt appears

## ⚠️ Important Notes

### Continuous Tracking:
- Keep browser tab open for tracking to continue
- Each update opens a new WhatsApp tab
- This is by design for free operation
- Stop tracking when journey is complete

### Police Station Search:
- Better results in urban areas
- May have limited data in remote locations
- Always keep emergency numbers memorized
- Use "Open in Maps" as backup option

### Location Accuracy:
- Works best outdoors with clear sky
- May take time to acquire GPS lock initially
- Accuracy varies by device and conditions
- Enable "High Accuracy" mode for best results

## 📖 Documentation

See `FEATURES_GUIDE.md` for comprehensive documentation including:
- Detailed feature explanations
- Step-by-step usage guides
- Troubleshooting tips
- Privacy & security information
- Technical architecture details

## 🔄 Updates & Improvements

### Version 2.0 - Real-Time Features (January 2026)
- ✅ Added WhatsApp location sharing
- ✅ Added SMS location sharing
- ✅ Added Email location sharing
- ✅ Added continuous auto-tracking (every 2 minutes)
- ✅ Added dynamic police station finder
- ✅ Integrated GPS-based search
- ✅ Added distance calculation
- ✅ Improved SOS alerts with sharing options

### Version 1.0 - Initial Release
- Emergency SOS system
- Live location tracking map
- Emergency contacts management
- Safe routes storage
- Instant camera feature
- Safety tips database
- Static police station info

## 🎓 How to Contribute

This is a client-side only application. To enhance:

1. **Add More Sharing Methods:**
   - Telegram integration
   - Other messaging apps
   - Social media sharing

2. **Improve Police Data:**
   - Add hospital finder
   - Add safe house locations
   - Emergency shelter finder

3. **Enhanced Features:**
   - Offline map caching
   - Voice commands
   - Shake to activate SOS
   - Customizable tracking intervals

## 📞 Emergency Contacts (India)

| Service | Number | Description |
|---------|--------|-------------|
| ERSS | 112 | Emergency Response Support System |
| Police | 100 | Police Emergency |
| Women Helpline | 1091 | Women in Distress |
| Women Helpline | 181 | Nationwide Women Helpline |
| Child Helpline | 1098 | Child in Distress |
| Ambulance | 102 | Medical Emergency |
| Fire | 101 | Fire Emergency |

## 🙏 Acknowledgments

- **Leaflet.js** - Open-source mapping library
- **OpenStreetMap** - Free map data
- **Overpass API** - OSM query service
- **Community Contributors** - For maintaining accurate data

## ⚖️ License

This project is created for educational and safety purposes.  
Free to use, modify, and distribute for personal safety.

## 🆘 Disclaimer

This application is a tool to enhance personal safety. It should not replace:
- Proper safety awareness
- Emergency services (always call 112/100 in emergencies)
- Professional security advice
- Personal safety precautions

**Stay safe, stay alert, and trust your instincts!** 🛡️

---

## 🎯 Quick Command Reference

```javascript
// Manually trigger functions in console if needed:

// Share location
shareViaWhatsApp();
shareViaSMS();
shareViaEmail();

// Start/Stop continuous tracking
startContinuousTracking();
stopContinuousTracking();

// Find police stations
findNearbyPoliceStations();

// Emergency SOS
triggerSOS();
```

## 📱 Progressive Web App (PWA)

You can save this app to your home screen:

**On Mobile:**
1. Open in browser
2. Tap "Share" or menu (⋮)
3. Select "Add to Home Screen"
4. Access like a native app

**On Desktop:**
1. Look for install icon in address bar
2. Click "Install"
3. Access from applications menu

---

**Created with ❤️ for Women's Safety**  
**Version 2.0 - Real-Time Features Edition**  
**Last Updated: January 2026**
#   W o m e n - S a f e t y - A p p  
 