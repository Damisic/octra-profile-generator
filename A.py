from flask import Flask, send_file, jsonify
import requests
import re
import io

app = Flask(__name__)

@app.route('/avatar/<username>')
def get_avatar(username):
    username = username.lstrip('@').lower()
    profile_url = f"https://x.com/{username}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        response = requests.get(profile_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"error": "User not found or profile inaccessible"}), 404
        
        # Extract avatar URL (usually the largest one ends with =400x400 or similar)
        match = re.search(r'src="https://pbs\.twimg\.com/profile_images/[^"]*400x400[^"]*"', response.text)
        if not match:
            # Fallback pattern
            match = re.search(r'src="(https://pbs\.twimg\.com/profile_images/[^"]*)"', response.text)
        
        if not match:
            return jsonify({"error": "Avatar not found in profile"}), 404
        
        avatar_url = match.group(1) if match.lastindex else match.group(1)
        # Upgrade to original size by removing size suffix
        avatar_url = re.sub(r'_\w+\.(jpg|jpeg|png|gif)', r'.\1', avatar_url)
        
        img_response = requests.get(avatar_url, headers=headers, stream=True)
        if img_response.status_code != 200:
            return jsonify({"error": "Failed to load image"}), 500
        
        return send_file(
            io.BytesIO(img_response.content),
            mimetype=img_response.headers.get('Content-Type', 'image/jpeg'),
            download_name=f"{username}_avatar.jpg"
        )
    
    except Exception as e:
        return jsonify({"error": "Server error"}), 500

@app.route('/')
def index():
    return app.send_static_file('A.html')  # Serve your HTML/CSS/JS

if __name__ == '__main__':
    app.run(port=5000, debug=True)