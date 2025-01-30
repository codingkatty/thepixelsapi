import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from supabase import create_client, Client
from PIL import Image, ImageColor
from io import BytesIO

app = Flask(__name__)
CORS(app)

supabase_url = "https://msfutgjgflgkckxreksp.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1zZnV0Z2pnZmxna2NreHJla3NwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMwMTk1NDEsImV4cCI6MjA0ODU5NTU0MX0.pIQlsN43fHNmB1MCjONz6jomwz3x3vdgfGyfSlmWw_U"
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/image', methods=['GET'])
def get_image():
    # create image from pixels
    img = Image.new('RGB', (32, 16), color = 'white')
    pixels = supabase.from_('pixels').select('*').execute()

    for pixel in pixels.data:
        x = int(pixel['x'])
        y = int(pixel['y'])
        color = pixel['color']
        img.putpixel((x, y), ImageColor.getrgb(color))
    
    scaled_img = img.resize((1600, 800), Image.NEAREST)

    img_io = BytesIO()
    scaled_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/trending', methods=['GET'])
def get_trending_color():
    query = supabase.from_('pixels').select('color').execute()
    colors = [pixel['color'] for pixel in query.data]

    trending_color = max(set(colors), key = colors.count)
    count = colors.count(trending_color)
    
    return jsonify({"trending": trending_color, "count": count}), 200

@app.route('/pixels', methods=['GET'])
def get_pixels():
    query = supabase.from_('pixels').select('*')
    
    x = request.args.getlist('x')
    y = request.args.getlist('y')
    color = request.args.getlist('color')

    color = ['#' + c.lstrip('#') for c in color] 
    
    if x:
        query = query.in_('x', x)
    if y:
        query = query.in_('y', y)
    if color:
        query = query.in_('color', color)
    
    pixels = query.execute()
    return jsonify({"pixels": pixels.data}), 200

@app.route('/setpixel', methods=['POST', 'OPTIONS'])
def set_pixel():
    x = request.json['x']
    y = request.json['y']
    color = request.json['color']

    if x < 0 or x > 31 or y < 0 or y > 15:
        return jsonify({"message": "Invalid coordinates"}), 400

    supabase.from_('pixels').update({'color': color}).eq('x', x).eq('y', y).execute()
    supabase.from_('pixels').update({'timeCreated': 'now()'}).eq('x', x).eq('y', y).execute()
    
    return jsonify({"message": "The pixel is set!"}), 200

@app.route('/', methods=['GET'])
def documentation():
    return send_file('docsserver.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)