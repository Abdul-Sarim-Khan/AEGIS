import os
import pickle
import sqlite3
import hashlib

from flask import Flask, request, jsonify
app = Flask(__name__)
# ==================================================# AEGIS LOAD TEST FILE - MONOLITHIC VULNERABLE APP# ==================================================

# --- Endpoint Block 1 ---
@app.route('/api/v1/module_1', methods=['GET', 'POST'])
def process_module_1():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_1.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_1 = "SUPER_SECRET_KEY_1_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_1.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 1, "hash": weak_hash})

# --- Endpoint Block 2 ---
@app.route('/api/v1/module_2', methods=['GET', 'POST'])
def process_module_2():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_2.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_2 = "SUPER_SECRET_KEY_2_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_2.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 2, "hash": weak_hash})

# --- Endpoint Block 3 ---
@app.route('/api/v1/module_3', methods=['GET', 'POST'])
def process_module_3():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_3.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_3 = "SUPER_SECRET_KEY_3_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_3.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 3, "hash": weak_hash})

# --- Endpoint Block 4 ---
@app.route('/api/v1/module_4', methods=['GET', 'POST'])
def process_module_4():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_4.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_4 = "SUPER_SECRET_KEY_4_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_4.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 4, "hash": weak_hash})

# --- Endpoint Block 5 ---
@app.route('/api/v1/module_5', methods=['GET', 'POST'])
def process_module_5():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_5.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_5 = "SUPER_SECRET_KEY_5_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_5.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 5, "hash": weak_hash})

# --- Endpoint Block 6 ---
@app.route('/api/v1/module_6', methods=['GET', 'POST'])
def process_module_6():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_6.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_6 = "SUPER_SECRET_KEY_6_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_6.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 6, "hash": weak_hash})

# --- Endpoint Block 7 ---
@app.route('/api/v1/module_7', methods=['GET', 'POST'])
def process_module_7():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_7.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_7 = "SUPER_SECRET_KEY_7_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_7.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 7, "hash": weak_hash})

# --- Endpoint Block 8 ---
@app.route('/api/v1/module_8', methods=['GET', 'POST'])
def process_module_8():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_8.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_8 = "SUPER_SECRET_KEY_8_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_8.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 8, "hash": weak_hash})

# --- Endpoint Block 9 ---
@app.route('/api/v1/module_9', methods=['GET', 'POST'])
def process_module_9():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_9.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_9 = "SUPER_SECRET_KEY_9_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_9.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 9, "hash": weak_hash})

# --- Endpoint Block 10 ---
@app.route('/api/v1/module_10', methods=['GET', 'POST'])
def process_module_10():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_10.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_10 = "SUPER_SECRET_KEY_10_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_10.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 10, "hash": weak_hash})

# --- Endpoint Block 11 ---
@app.route('/api/v1/module_11', methods=['GET', 'POST'])
def process_module_11():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_11.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_11 = "SUPER_SECRET_KEY_11_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_11.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 11, "hash": weak_hash})

# --- Endpoint Block 12 ---
@app.route('/api/v1/module_12', methods=['GET', 'POST'])
def process_module_12():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_12.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_12 = "SUPER_SECRET_KEY_12_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_12.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 12, "hash": weak_hash})

# --- Endpoint Block 13 ---
@app.route('/api/v1/module_13', methods=['GET', 'POST'])
def process_module_13():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_13.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_13 = "SUPER_SECRET_KEY_13_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_13.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 13, "hash": weak_hash})

# --- Endpoint Block 14 ---
@app.route('/api/v1/module_14', methods=['GET', 'POST'])
def process_module_14():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_14.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_14 = "SUPER_SECRET_KEY_14_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_14.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 14, "hash": weak_hash})

# --- Endpoint Block 15 ---
@app.route('/api/v1/module_15', methods=['GET', 'POST'])
def process_module_15():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_15.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_15 = "SUPER_SECRET_KEY_15_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_15.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 15, "hash": weak_hash})

# --- Endpoint Block 16 ---
@app.route('/api/v1/module_16', methods=['GET', 'POST'])
def process_module_16():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_16.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_16 = "SUPER_SECRET_KEY_16_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_16.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 16, "hash": weak_hash})

# --- Endpoint Block 17 ---
@app.route('/api/v1/module_17', methods=['GET', 'POST'])
def process_module_17():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_17.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_17 = "SUPER_SECRET_KEY_17_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_17.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 17, "hash": weak_hash})

# --- Endpoint Block 18 ---
@app.route('/api/v1/module_18', methods=['GET', 'POST'])
def process_module_18():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_18.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_18 = "SUPER_SECRET_KEY_18_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_18.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 18, "hash": weak_hash})

# --- Endpoint Block 19 ---
@app.route('/api/v1/module_19', methods=['GET', 'POST'])
def process_module_19():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_19.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_19 = "SUPER_SECRET_KEY_19_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_19.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 19, "hash": weak_hash})

# --- Endpoint Block 20 ---
@app.route('/api/v1/module_20', methods=['GET', 'POST'])
def process_module_20():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_20.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_20 = "SUPER_SECRET_KEY_20_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_20.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 20, "hash": weak_hash})

# --- Endpoint Block 21 ---
@app.route('/api/v1/module_21', methods=['GET', 'POST'])
def process_module_21():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_21.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_21 = "SUPER_SECRET_KEY_21_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_21.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 21, "hash": weak_hash})

# --- Endpoint Block 22 ---
@app.route('/api/v1/module_22', methods=['GET', 'POST'])
def process_module_22():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_22.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_22 = "SUPER_SECRET_KEY_22_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_22.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 22, "hash": weak_hash})

# --- Endpoint Block 23 ---
@app.route('/api/v1/module_23', methods=['GET', 'POST'])
def process_module_23():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_23.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_23 = "SUPER_SECRET_KEY_23_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_23.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 23, "hash": weak_hash})

# --- Endpoint Block 24 ---
@app.route('/api/v1/module_24', methods=['GET', 'POST'])
def process_module_24():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_24.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_24 = "SUPER_SECRET_KEY_24_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_24.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 24, "hash": weak_hash})

# --- Endpoint Block 25 ---
@app.route('/api/v1/module_25', methods=['GET', 'POST'])
def process_module_25():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_25.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_25 = "SUPER_SECRET_KEY_25_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_25.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 25, "hash": weak_hash})

# --- Endpoint Block 26 ---
@app.route('/api/v1/module_26', methods=['GET', 'POST'])
def process_module_26():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_26.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_26 = "SUPER_SECRET_KEY_26_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_26.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 26, "hash": weak_hash})

# --- Endpoint Block 27 ---
@app.route('/api/v1/module_27', methods=['GET', 'POST'])
def process_module_27():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_27.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_27 = "SUPER_SECRET_KEY_27_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_27.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 27, "hash": weak_hash})

# --- Endpoint Block 28 ---
@app.route('/api/v1/module_28', methods=['GET', 'POST'])
def process_module_28():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_28.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_28 = "SUPER_SECRET_KEY_28_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_28.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 28, "hash": weak_hash})

# --- Endpoint Block 29 ---
@app.route('/api/v1/module_29', methods=['GET', 'POST'])
def process_module_29():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_29.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_29 = "SUPER_SECRET_KEY_29_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_29.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 29, "hash": weak_hash})

# --- Endpoint Block 30 ---
@app.route('/api/v1/module_30', methods=['GET', 'POST'])
def process_module_30():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_30.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_30 = "SUPER_SECRET_KEY_30_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_30.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 30, "hash": weak_hash})

# --- Endpoint Block 31 ---
@app.route('/api/v1/module_31', methods=['GET', 'POST'])
def process_module_31():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_31.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_31 = "SUPER_SECRET_KEY_31_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_31.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 31, "hash": weak_hash})

# --- Endpoint Block 32 ---
@app.route('/api/v1/module_32', methods=['GET', 'POST'])
def process_module_32():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_32.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_32 = "SUPER_SECRET_KEY_32_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_32.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 32, "hash": weak_hash})

# --- Endpoint Block 33 ---
@app.route('/api/v1/module_33', methods=['GET', 'POST'])
def process_module_33():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_33.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_33 = "SUPER_SECRET_KEY_33_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_33.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 33, "hash": weak_hash})

# --- Endpoint Block 34 ---
@app.route('/api/v1/module_34', methods=['GET', 'POST'])
def process_module_34():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_34.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_34 = "SUPER_SECRET_KEY_34_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_34.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 34, "hash": weak_hash})

# --- Endpoint Block 35 ---
@app.route('/api/v1/module_35', methods=['GET', 'POST'])
def process_module_35():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_35.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_35 = "SUPER_SECRET_KEY_35_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_35.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 35, "hash": weak_hash})

# --- Endpoint Block 36 ---
@app.route('/api/v1/module_36', methods=['GET', 'POST'])
def process_module_36():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_36.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_36 = "SUPER_SECRET_KEY_36_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_36.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 36, "hash": weak_hash})

# --- Endpoint Block 37 ---
@app.route('/api/v1/module_37', methods=['GET', 'POST'])
def process_module_37():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_37.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_37 = "SUPER_SECRET_KEY_37_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_37.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 37, "hash": weak_hash})

# --- Endpoint Block 38 ---
@app.route('/api/v1/module_38', methods=['GET', 'POST'])
def process_module_38():
    # A03: SQL Injection
    user_input = request.args.get('id', '1')
    conn = sqlite3.connect("database_38.db")
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE id = '" + user_input + "'"
    cursor.execute(query)
    
    # A03: Command Injection
    target_ip = request.args.get('ip', '127.0.0.1')
    os.system(f"ping -c 1 {target_ip}")
    
    # A02: Cryptographic Failures (Weak Hashing & Hardcoded Secrets)
    api_secret_38 = "SUPER_SECRET_KEY_38_DO_NOT_SHARE"
    weak_hash = hashlib.md5(api_secret_38.encode()).hexdigest()
    
    # A08: Insecure Deserialization
    payload = request.args.get('data', b'')
    if payload:
        try:
            parsed = pickle.loads(payload)  # Highly vulnerable
        except:
            pass
            
    return jsonify({"status": "processed", "module": 38, "hash": weak_hash})
