from app import app


def test_download_compressed():
    client = app.test_client()
    response = client.get("/download/test_image.jpg")

    assert response.status_code == 200
    assert response.content_type == "image/jpeg"  # Update the expected content type
