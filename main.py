import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from supabase import create_client, Client
from PIL import Image, ImageColor
from io import BytesIO

app = Flask(__name__)
CORS(app)

supabase_url = "https://msfutgjgflgkckxreksp.supabase.co"
supabase_key = os.environ.get('SUPABASE_KEY')
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

# pixels: take in x y and returns color and last modified of pixel
@app.route('/pixeldata', methods=['GET'])
def get_pixel():
    x = request.args.get('x')
    y = request.args.get('y')

    if not x or not y:
        return jsonify({"message": "Invalid parameters"}), 400

    color_response = supabase.from_('pixels').select('color').eq('x', x).eq('y', y).single().execute()
    time_created_response = supabase.from_('pixels').select('timeCreated').eq('x', x).eq('y', y).single().execute()

    if color_response.data and time_created_response.data:
        color = color_response.data['color']
        time_created = time_created_response.data['timeCreated']
        return jsonify({"color": color, "timeCreated": time_created}), 200
    else:
        return jsonify({"message": "Pixel not found"}), 404

@app.route('/pixels', methods=['GET'])
def get_pixels():
    query = supabase.from_('pixels').select('*')
    
    x = request.args.get('x')
    y = request.args.get('y')
    color = request.args.get('color')
    
    if x:
        query = query.eq('x', x)

    if y:
        query = query.eq('y', y)

    if color:
        query = query.eq('color', color)

    
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
def home():
    return jsonify({"message": "Service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)