import os

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from PIL import Image

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_valid_image(file):
    return file and allowed_file(file.filename)


def compress_image(input_path, output_path, quality=85):
    try:
        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=quality)
        return True
    except Exception as e:
        return str(e)


@app.route("/", methods=["GET", "POST"])
def photo_compressor():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            if not is_valid_image(uploaded_file):
                return (
                    "Invalid file format. Please upload a valid image.",
                    400,
                )  # Return a 400 status code

            input_path = os.path.join("uploads", uploaded_file.filename)
            output_path = os.path.join("compressed", uploaded_file.filename)
            uploaded_file.save(input_path)

            compression_result = compress_image(input_path, output_path)
            if compression_result is True:
                return redirect(url_for("download_compressed", filename=uploaded_file.filename))
            else:
                flash(f"Compression Error: {compression_result}", "error")

    return render_template("index.html")


@app.route("/download/<filename>")
def download_compressed(filename):
    compressed_path = os.path.join("compressed", filename)
    return send_file(compressed_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
