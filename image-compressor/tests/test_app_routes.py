import os

from app import app

app.secret_key = os.getenv("secret_key")


def test_home_page():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Photo Compressor" in response.data
    assert b"Choose an image to compress" in response.data


def test_upload_image():
    client = app.test_client()

    # Open the test image file and create a file object
    with open("tests/test_data/test_image.jpg", "rb") as image_file:
        data = {"file": (image_file, "test_image.jpg")}
        response = client.post("/", data=data, content_type="multipart/form-data")

    assert response.status_code == 302  # Redirect after successful upload


def test_upload_invalid_file():
    client = app.test_client()

    # Open the invalid image file and create a file object
    with open("tests/test_data/invalid_image.txt", "rb") as invalid_file:
        data = {"file": (invalid_file, "invalid_image.txt")}
        response = client.post(
            "/", data=data, content_type="multipart/form-data", follow_redirects=True
        )

    assert response.status_code == 400  # Expecting a Bad Request status code
    assert b"Invalid file format. Please upload a valid image." in response.data
    assert response.status_code == 400  # Expecting a Bad Request status code
    assert b"Invalid file format. Please upload a valid image." in response.data
