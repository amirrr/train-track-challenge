# Train Track Flask API

This file contains the Flask API for the Train Track project. The API allows users to check for conflicts in train routes and visualize them. It checks for conflicts under the assumption that trains can travel in both directions on a track at the same time. This means that in the figure below, if a train is traveling from A to B, another train can travel from B to A at the same time on the longer path.

```text
A - B
|   |
C - D
```

## Prerequisites

- Python 3.9
- Flask
- NetworkX

## Project Structure

- `traintrack.py`: Contains the logic for checking train route conflicts and generating visualizations.
- `app.py`: The Flask application that serves as the API.
- `templates`: Directory containing HTML templates for the web interface.

## API Endpoints

- `/`: Main page with options to upload JSON data or paste JSON data for processing.
- `/upload_json`: Handles file uploads and processes the JSON data from an uploaded file.
- `/process_json`: Processes JSON data received via a POST request and returns a rendered template with the result.
- `/test_plot`: A test route for generating and displaying a sample train track visualization.

## Usage

1. Start the Flask application by running `app.py`.
2. Access the main page at [http://localhost:5000/](http://localhost:5000/).
3. Choose to upload a JSON file or paste JSON data for processing.
4. Check for conflicts and visualize train routes.
5. The result will be displayed, indicating if the route is available or unavailable.
6. Additionally, a visualization will be shown with color-coded tracks.

## Sample JSON Data

The API expects JSON data in the following format:

```json
{
    "station_graph": [ ... ],
    "routes": [ ... ],
    "check_route": { ... }
}
```

## Testing

You can test the application using `unittest` by running the following command:

```shell
python -m unittest discover .
```

Make sure to install the required dependencies and libraries before running the application.

