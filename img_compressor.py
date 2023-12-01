from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance
from flask import send_file

import os

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
#app.config['COMPRESSED_FOLDER'] = './static/compressed'
#app.config['ENHANCED_FOLDER'] = './static/enhanced'
app.config['COMPRESSED_FOLDER'] = os.path.join('static', 'compressed')
app.config['ENHANCED_FOLDER'] = os.path.join('static', 'enhanced')
app.config['FUSED_FOLDER'] = os.path.join('static', 'fused')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

if not os.path.exists(app.config['COMPRESSED_FOLDER']):
    os.makedirs(app.config['COMPRESSED_FOLDER'])

if not os.path.exists(app.config['ENHANCED_FOLDER']):
    os.makedirs(app.config['ENHANCED_FOLDER'])

if not os.path.exists(app.config['FUSED_FOLDER']):
    os.makedirs(app.config['FUSED_FOLDER'])
    
def allowed_file(filename):
    # Check if the file extension is allowed
    return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
         

def enhance_image(input_path, output_path, sharpness_factor, contrast_factor, color_factor):
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness_factor)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast_factor)

        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(color_factor)

        img.save(output_path)

def compress_image(input_path, output_path, desired_size, desired_byte_format):
    # Open the input image
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # Calculate the initial size of the image
        size = os.path.getsize(input_path)
        # Convert the desired size to bytes
        if desired_byte_format == 'KB':
            desired_size = int(desired_size.replace("KB", "")) * 1024
        elif desired_byte_format == 'MB':
            desired_size = int(desired_size.replace("MB", "")) * 1024 * 1024
        elif desired_byte_format == 'GB':
            desired_size = int(desired_size.replace("GB", "")) * 1024 * 1024 * 1024
        else:
            raise ValueError("Invalid size format! Use KB, MB or GB.")
        
        # If the image size is already smaller than the desired size, return the input image
        if size < desired_size:
            return img
        
        # Initialize the quality parameter
        quality = 100
        
        # Compress the image until the desired size is reached
        while size > desired_size:
            if quality <= 0:
                break
            img.save(output_path, "JPEG", quality=quality)
            size = os.path.getsize(output_path)
            quality -= 5
        
        # Return the compressed image
        return img
    
def fusion_logic(input_path1, input_path2):
    # Open the images
    image1 = Image.open(input_path1)
    image2 = Image.open(input_path2)

    # Check and adjust image sizes if necessary
    if image1.size != image2.size:
        # Resize or crop one of the images to match the size of the other
        image1 = image1.resize(image2.size)

    # Check and adjust image modes if necessary
    if image1.mode != image2.mode:
        # Convert one of the images to the mode of the other
        image1 = image1.convert(image2.mode)

    # Blend the images
    fused_image = Image.blend(image1, image2, alpha=0.5)

    return fused_image


@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        print("1 clear")
        file = request.files['file']
        
        # If the user does not select a file, submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Save the uploaded file to the uploads folder
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            print("2")
            # Compress the image and save it to the uploads folder with a "_compressed" suffix
            output_path = os.path.join(app.config['COMPRESSED_FOLDER'], os.path.splitext(filename)[0] + "_compressed.jpg")
            desired_size = request.form['size']
            desired_byte_format = request.form['option']
            compress_image(input_path, output_path, desired_size, desired_byte_format)
            
            # Return the download link for the compressed image
            return render_template('./result.html', filename=os.path.basename(output_path))
            
    return render_template('./index.html')

@app.route('/enhance', methods=['POST'])
def enhance():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            sharpness_factor = float(request.form['sharpness'])
            contrast_factor = float(request.form['contrast'])
            color_factor = float(request.form['color'])

            output_path = os.path.join(app.config['ENHANCED_FOLDER'], os.path.splitext(filename)[0] + "_enhanced.jpg")
            enhance_image(input_path, output_path, sharpness_factor, contrast_factor, color_factor)

            return send_file(output_path, as_attachment=True)

    return render_template('./index.html')


@app.route('/fusion', methods=['GET', 'POST'])
def fusion():
    if request.method == 'POST':
        if 'file1' not in request.files or 'file2' not in request.files:
            flash('Two files are required for fusion')
            return redirect(request.url)

        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            flash('Both files are required for fusion')
            return redirect(request.url)

        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            filename1 = secure_filename(file1.filename)
            input_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            file1.save(input_path1)

            filename2 = secure_filename(file2.filename)
            input_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            file2.save(input_path2)

            fused_image = fusion_logic(input_path1, input_path2)
            

            fused_filename = os.path.splitext(filename1)[0] + "_" + os.path.splitext(filename2)[0] + "_fused.jpg"
            fused_path = os.path.join(app.config['FUSED_FOLDER'], fused_filename)
            fused_image.save(fused_path)

            return send_file(fused_path, as_attachment=True)

    return render_template('./fusion.html')

'''
@app.route('/static/compressed/<filename>')
def download(filename):
    # Get the path to the compressed image file
    compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if the compressed image file exists
    if not os.path.exists(compressed_path):
        return "Error: File not found"
    
    # Return the compressed image file for download
    return send_file(compressed_path, as_attachment=True)
'''
@app.route('/static/compressed/<filename>')
def download(filename):
    # Return the download link for the compressed image
    #path = output_path
    #return send_file(path, as_attachment=True)
    compressed_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
    if not os.path.exists(compressed_path):
        return "Error: File not found"
    return send_file(compressed_path, as_attachment=True)
    #path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
    # Return the file for download
    #return send_file(path, as_attachment=True)
    #return redirect(url_for('static', filename=os.path.join('compressed/', filename)), code=301)

@app.route('/static/enhanced/<filename>')
def download_enhanced(filename):
    enhanced_path = os.path.join(app.config['ENHANCED_FOLDER'], filename)
    if not os.path.exists(enhanced_path):
        return "Error: File not found"
    return send_file(enhanced_path, as_attachment=True)

@app.route('/static/fused/<filename>')
def download_fused(filename):
    fused_path = os.path.join(app.config['FUSED_FOLDER'], filename)
    if not os.path.exists(fused_path):
        return "Error: File not found"
    return send_file(fused_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
