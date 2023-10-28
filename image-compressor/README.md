[![codecov](https://codecov.io/gh/k1lgor/image-compressor/branch/master/graph/badge.svg?token=OWVSAGHDPL)](https://codecov.io/gh/k1lgor/image-compressor)

# Image Compression Web Application

The Image Compression Web Application is a simple Flask-based web application that allows users to upload images for compression while maintaining image quality. The application utilizes the popular Python Imaging Library (PIL) to perform image compression.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Uploading an Image](#uploading-an-image)
- [Using Docker](#using-docker)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload images for compression while maintaining quality.
- Download the compressed image for further use.
- User-friendly web interface powered by Flask.
- Error messages for unsupported formats and compression failures.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Flask (pip install Flask)
- Python Imaging Library (PIL) (pip install Pillow)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/k1lgor/image-compressor.git
cd image-compressor
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory:

```bash
cd image-compressor
```

2. Run the Flask application:

```bash
flask run
```

3. Open your web browser and go to http://localhost:5000 to access the application.

## Usage

### Uploading an Image

1. Visit the application URL (e.g., http://localhost:5000).
2. Click the "Browse" button to select an image from your local machine.
3. Click the "Compress and Download" button to initiate the compression process.
4. The iamge will be downloaded automatically.

## Using Docker

You can also run the application using Docker and Docker Compose.

1. Make sure you have Docker and Docker Compose installed.
2. Build the Docker Image:

```bash
docker build -t image-compressor .
```

3. Start the application using Docker Compose:

```bash
docker-compose up -d
```

4. Open your web browser and go to http://localhost:5000 to access the application.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Code Coverage

For detailed code coverage information, see the [Code Coverage Report](./README_COVERAGE.md).
