from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection helper function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    return conn

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

# Endpoint to get a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Endpoint to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    name = new_user.get('name')
    email = new_user.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User added successfully!"}), 201

# Endpoint to update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.get_json()
    name = updated_user.get('name')
    email = updated_user.get('email')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cur.execute('UPDATE users SET name = %s, email = %s WHERE id = %s',
                (name, email, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User updated successfully!"})

# Endpoint to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cur.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)