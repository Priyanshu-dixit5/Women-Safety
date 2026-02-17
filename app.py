from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import hashlib
import os
import json
from datetime import datetime
import webbrowser
import threading
import time

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for local development

# Database file
DB_FILE = 'safeguard.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Emergency contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emergency_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            relationship TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Safe routes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS safe_routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Location history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            latitude REAL,
            longitude REAL,
            accuracy REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Sync status table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sync_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            operation TEXT NOT NULL,
            table_name TEXT NOT NULL,
            record_id INTEGER,
            source TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_FILE}")

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def log_sync(user_id, operation, table_name, record_id, source='web'):
    """Log synchronization activity"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sync_status (user_id, operation, table_name, record_id, source)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, operation, table_name, record_id, source))
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'pg1.html')

@app.route('/pg1.html')
def login_page():
    return send_from_directory('.', 'pg1.html')

@app.route('/index.html')
def main_app():
    return send_from_directory('.', 'index.html')

@app.route('/test_connection.html')
def test_connection():
    return send_from_directory('.', 'test_connection.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Flask backend is running'})

# Authentication endpoints
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        security_question = data.get('securityQuestion', '')
        security_answer = data.get('securityAnswer', '').strip().lower()
        
        # Validation
        if not all([username, name, email, password, security_question, security_answer]):
            return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
        
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'status': 'error', 'message': 'Email already exists'}), 400
        
        # Create user
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, name, email, password, security_question, security_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, name, email, hashed_password, security_question, security_answer))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_sync(user_id, 'CREATE', 'users', user_id, 'web')
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except sqlite3.IntegrityError as e:
        return jsonify({'status': 'error', 'message': 'Username or email already exists'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        hashed_password = hash_password(password)
        cursor.execute('''
            SELECT id, username, name, email FROM users
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            log_sync(user['id'], 'LOGIN', 'users', user['id'], 'web')
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'name': user['name'],
                    'email': user['email']
                }
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/verify-email', methods=['POST'])
def verify_email():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({'status': 'error', 'message': 'Email is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, security_question FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'status': 'success',
                'securityQuestion': user['security_question']
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Email not found'}), 404
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        security_answer = data.get('securityAnswer', '').strip().lower()
        new_password = data.get('newPassword', '')
        
        if not all([email, security_answer, new_password]):
            return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM users
            WHERE email = ? AND security_answer = ?
        ''', (email, security_answer))
        
        user = cursor.fetchone()
        
        if user:
            hashed_password = hash_password(new_password)
            cursor.execute('''
                UPDATE users SET password = ? WHERE id = ?
            ''', (hashed_password, user['id']))
            conn.commit()
            conn.close()
            
            log_sync(user['id'], 'UPDATE', 'users', user['id'], 'web')
            
            return jsonify({
                'status': 'success',
                'message': 'Password reset successfully'
            }), 200
        else:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Invalid email or security answer'}), 401
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Contacts endpoints
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'status': 'error', 'message': 'user_id is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, phone, relationship FROM emergency_contacts
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        contacts = []
        for row in cursor.fetchall():
            contacts.append({
                'id': row['id'],
                'name': row['name'],
                'phone': row['phone'],
                'relation': row['relationship'] or ''
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'contacts': contacts
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        relationship = data.get('relationship', '').strip()
        
        if not all([user_id, name, phone]):
            return jsonify({'status': 'error', 'message': 'user_id, name, and phone are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO emergency_contacts (user_id, name, phone, relationship)
            VALUES (?, ?, ?, ?)
        ''', (user_id, name, phone, relationship))
        
        contact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_sync(user_id, 'CREATE', 'emergency_contacts', contact_id, 'web')
        
        return jsonify({
            'status': 'success',
            'message': 'Contact added successfully',
            'contact_id': contact_id
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user_id before deleting
        cursor.execute('SELECT user_id FROM emergency_contacts WHERE id = ?', (contact_id,))
        contact = cursor.fetchone()
        
        if not contact:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Contact not found'}), 404
        
        user_id = contact['user_id']
        
        cursor.execute('DELETE FROM emergency_contacts WHERE id = ?', (contact_id,))
        conn.commit()
        conn.close()
        
        log_sync(user_id, 'DELETE', 'emergency_contacts', contact_id, 'web')
        
        return jsonify({
            'status': 'success',
            'message': 'Contact deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Routes endpoints
@app.route('/api/routes', methods=['GET'])
def get_routes():
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'status': 'error', 'message': 'user_id is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, address FROM safe_routes
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        routes = []
        for row in cursor.fetchall():
            routes.append({
                'id': row['id'],
                'name': row['name'],
                'address': row['address']
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'routes': routes
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/routes', methods=['POST'])
def add_route():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name', '').strip()
        address = data.get('address', '').strip()
        
        if not all([user_id, name, address]):
            return jsonify({'status': 'error', 'message': 'user_id, name, and address are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO safe_routes (user_id, name, address)
            VALUES (?, ?, ?)
        ''', (user_id, name, address))
        
        route_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_sync(user_id, 'CREATE', 'safe_routes', route_id, 'web')
        
        return jsonify({
            'status': 'success',
            'message': 'Route added successfully',
            'route_id': route_id
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/routes/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user_id before deleting
        cursor.execute('SELECT user_id FROM safe_routes WHERE id = ?', (route_id,))
        route = cursor.fetchone()
        
        if not route:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Route not found'}), 404
        
        user_id = route['user_id']
        
        cursor.execute('DELETE FROM safe_routes WHERE id = ?', (route_id,))
        conn.commit()
        conn.close()
        
        log_sync(user_id, 'DELETE', 'safe_routes', route_id, 'web')
        
        return jsonify({
            'status': 'success',
            'message': 'Route deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Location endpoint
@app.route('/api/location', methods=['POST'])
def save_location():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        
        if not user_id or latitude is None or longitude is None:
            return jsonify({'status': 'error', 'message': 'user_id, latitude, and longitude are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO location_history (user_id, latitude, longitude, accuracy)
            VALUES (?, ?, ?, ?)
        ''', (user_id, latitude, longitude, accuracy))
        
        location_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_sync(user_id, 'CREATE', 'location_history', location_id, 'web')
        
        return jsonify({
            'status': 'success',
            'message': 'Location saved successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Sync status endpoint
@app.route('/api/sync-status', methods=['GET'])
def get_sync_status():
    try:
        user_id = request.args.get('user_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT * FROM sync_status
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT * FROM sync_status
                ORDER BY timestamp DESC
                LIMIT 50
            ''')
        
        statuses = []
        for row in cursor.fetchall():
            statuses.append({
                'id': row['id'],
                'user_id': row['user_id'],
                'operation': row['operation'],
                'table_name': row['table_name'],
                'record_id': row['record_id'],
                'source': row['source'],
                'timestamp': row['timestamp']
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'sync_status': statuses
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Safeguard Flask Backend...")
    print(f"📁 Database: {DB_FILE}")
    print("🌐 Server will start on http://127.0.0.1:5000")
    print("📝 API endpoints available at http://127.0.0.1:5000/api/")
    print("\n✅ Backend ready!")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://127.0.0.1:5000')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
