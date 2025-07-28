# Car Hire API Documentation

## API Endpoints

### Cars

#### List Cars
- **URL:** `/api/cars/`
- **Method:** GET
- **Auth Required:** No
- **Query Parameters:**
  - `search`: Search by make, model, year, transmission, fuel_type
  - `ordering`: Order by daily_rate or year
- **Success Response:** List of cars with details

#### Get Available Cars
- **URL:** `/api/cars/available/`
- **Method:** GET
- **Auth Required:** No
- **Query Parameters:**
  - `start_date`: Start date (YYYY-MM-DD)
  - `end_date`: End date (YYYY-MM-DD)
- **Success Response:** List of available cars for the date range
- **Error Response:** 400 Bad Request if dates are invalid or missing

#### Create Car
- **URL:** `/api/cars/`
- **Method:** POST
- **Auth Required:** Yes (Staff only)
- **Data:**
  ```json
  {
    "make": "string",
    "model": "string",
    "year": "integer",
    "transmission": "string (A/M)",
    "fuel_type": "string (P/D/E/H)",
    "seats": "integer",
    "daily_rate": "decimal",
    "description": "string",
    "image": "file (optional)"
  }
  ```

### Bookings

#### List User's Bookings
- **URL:** `/api/bookings/`
- **Method:** GET
- **Auth Required:** Yes
- **Success Response:** List of user's bookings

#### Create Booking
- **URL:** `/api/bookings/`
- **Method:** POST
- **Auth Required:** Yes
- **Data:**
  ```json
  {
    "car_id": "integer",
    "start_date": "date (YYYY-MM-DD)",
    "end_date": "date (YYYY-MM-DD)"
  }
  ```

#### Cancel Booking
- **URL:** `/api/bookings/{id}/cancel/`
- **Method:** POST
- **Auth Required:** Yes
- **Success Response:** Updated booking with cancelled status
- **Error Response:** 400 Bad Request if booking cannot be cancelled

### Reviews

#### List Reviews
- **URL:** `/api/reviews/`
- **Method:** GET
- **Auth Required:** No
- **Success Response:** List of all reviews

#### Create Review
- **URL:** `/api/reviews/`
- **Method:** POST
- **Auth Required:** Yes
- **Data:**
  ```json
  {
    "car_id": "integer",
    "rating": "integer",
    "comment": "string"
  }
  ```

## Authentication

### Login
- **URL:** `/api-auth/login/`
- **Method:** POST
- **Data:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Logout
- **URL:** `/api-auth/logout/`
- **Method:** POST

## Error Responses

All endpoints may return these status codes:
- 200: Success
- 201: Created successfully
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
