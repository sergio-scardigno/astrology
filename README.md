# Astrology API

This is a web-based astrology application that provides various astrological calculations and data.

## Features

*   Calculates planetary positions and house cusps.
*   Provides data for different celestial bodies.
*   Geocoding functionality to convert city names into coordinates.
*   Docker support for easy deployment.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/astrology-api.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application locally, use the following command:

```bash
python main.py
```

The application will be available at `http://localhost:5000`.

## Docker

To build the Docker image, run the following command:

```bash
docker build -t astrology-api .
```

To run the application in a Docker container:

```bash
docker run -p 5000:5000 astrology-api
```

## Dependencies

The required Python packages are listed in the `requirements.txt` file:

*   Flask
*   pyswisseph
*   geopy

## API Endpoints

The following API endpoints are available:

*   `/`: Returns the positions of the planets and house cusps for a given date, time, and location.
*   `/api/planets`: Returns the positions of the planets for a given date and time.
*   `/api/houses`: Returns the house cusps for a given date, time, and location.
*   `/api/geocode`: Converts a city name into coordinates.