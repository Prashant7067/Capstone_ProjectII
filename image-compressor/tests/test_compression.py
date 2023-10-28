import os
import tempfile

from app import compress_image


def test_compress_image():
    input_path = os.path.join("tests", "test_data", "test_image.jpg")
    output_path = os.path.join(tempfile.gettempdir(), "compressed_test_image.jpg")
    result = compress_image(input_path, output_path, quality=70)  # noqa: F821

    assert result is True

    # Clean up
    os.remove(output_path)


def test_compress_invalid_image():
    input_path = os.path.join("tests", "test_data", "invalid_image.txt")
    output_path = os.path.join(tempfile.gettempdir(), "compressed_invalid_image.jpg")
    result = compress_image(input_path, output_path)

    assert "cannot identify image file" in result


def test_compress_image_exception():
    input_path = "nonexistent_image.jpg"
    output_path = os.path.join(tempfile.gettempdir(), "compressed_nonexistent_image.jpg")
    result = compress_image(input_path, output_path, quality=70)

    assert isinstance(result, str)
    assert "No such file or directory" in result


def test_compress_image_quality_max():
    input_path = os.path.join("tests", "test_data", "valid_image.jpg")
    output_path = os.path.join(tempfile.gettempdir(), "compressed_valid_image.jpg")

    # Compress with maximum quality (100)
    result = compress_image(input_path, output_path, quality=100)

    assert result is True


def test_compress_image_quality_min():
    input_path = os.path.join("tests", "test_data", "valid_image.jpg")
    output_path = os.path.join(tempfile.gettempdir(), "compressed_valid_image.jpg")

    # Compress with minimum quality (0)
    result = compress_image(input_path, output_path, quality=0)

    assert result is True


def test_compress_image_valid():
    input_path = os.path.join("tests", "test_data", "valid_image.jpg")
    output_path = os.path.join(tempfile.gettempdir(), "compressed_valid_image.jpg")
    result = compress_image(input_path, output_path, quality=70)

    assert result is True
