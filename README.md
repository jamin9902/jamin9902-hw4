# County Health Data API

A Flask-based API that provides county health data based on ZIP codes. The application allows users to query various health measures for counties across the United States.

## Available Health Measures

The API provides access to the following health measures:

- Violent crime rate
- Unemployment
- Children in poverty
- Diabetic screening
- Mammography screening
- Preventable hospital stays
- Uninsured
- Sexually transmitted infections
- Physical inactivity
- Adult obesity
- Premature Death
- Daily fine particulate matter

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure the database file `data.db` is present in the root directory. The database is created from the CSV files:

   - `county_health_rankings.csv`: Contains health measures data
   - `zip_county.csv`: Maps ZIP codes to counties

3. Run the application:

```bash
python api/app.py
```

4. The server will start on `http://localhost:5000`

## API Usage

The API accepts POST requests to the `/county_data` endpoint with the following JSON format:

```json
{
  "zip": "12345",
  "measure_name": "Adult obesity"
}
```

### Parameters:

- `zip`: A 5-digit ZIP code (required)
- `measure_name`: One of the valid health measures listed above (required)

### Response Format:

```json
{
  "county": "Example County",
  "state": "Example State",
  "value": 25.5
}
```

### Error Responses:

- 400: Bad Request (Invalid ZIP code format or missing required fields)
- 404: Not Found (ZIP code or measure not found in database)
- 418: I'm a teapot (Easter egg response when {"coffee": "teapot"} is sent)
