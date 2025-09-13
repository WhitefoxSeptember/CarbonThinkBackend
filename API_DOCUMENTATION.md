# CarbonThink Backend API Documentation

## Overview

The CarbonThink Backend API provides endpoints for managing carbon footprint tracking, user accounts, and carbon consumption activities. This RESTful API is built with Django and integrates with Supabase for data storage.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API uses basic authentication mechanisms. User authentication is handled through the accounts endpoints.

---

## Accounts Module

### 1. List All Users

**GET** `/api/accounts/`

**Description:** Retrieve a list of all users in the system.

**Response:**
```json
{
  "users": [
    {
      "id": "uuid",
      "username": "string",
      "email": "string",
      "created_at": "datetime"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Database error

### 2. Get User Details

**GET** `/api/accounts/<user_id>/`

**Description:** Retrieve details for a specific user.

**Parameters:**
- `user_id` (path) - UUID of the user

**Response:**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "datetime"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - User not found
- `500 Internal Server Error` - Database error

### 3. Update User

**PUT** `/api/accounts/<user_id>/`

**Description:** Update user information.

**Parameters:**
- `user_id` (path) - UUID of the user

**Request Body:**
```json
{
  "username": "string",
  "email": "string"
}
```

**Response:**
```json
{
  "message": "User updated successfully",
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string"
  }
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Invalid data
- `404 Not Found` - User not found
- `500 Internal Server Error` - Database error

### 4. Delete User

**DELETE** `/api/accounts/<user_id>/`

**Description:** Delete a user account.

**Parameters:**
- `user_id` (path) - UUID of the user

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - User not found
- `500 Internal Server Error` - Database error

### 5. Register User

**POST** `/api/accounts/register/`

**Description:** Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": "uuid"
}
```

**Status Codes:**
- `201 Created` - Success
- `400 Bad Request` - Missing required fields or invalid data
- `500 Internal Server Error` - Database error

### 6. Login

**POST** `/api/accounts/login/`

**Description:** Authenticate user login.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": "uuid",
  "token": "string"
}
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing credentials

### 7. Logout

**POST** `/api/accounts/logout/`

**Description:** Log out the current user.

**Response:**
```json
{
  "message": "Logout successful"
}
```

**Status Codes:**
- `200 OK` - Success

---

## Sources Module

### 1. List Carbon Sources

**GET** `/api/sources/`

**Description:** Retrieve all available carbon sources.

**Response:**
```json
{
  "sources": [
    {
      "id": "uuid",
      "name": "string",
      "category": "string",
      "emission_factor": "number",
      "unit": "string"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Database error

### 2. Get Source Details

**GET** `/api/sources/<source_id>/`

**Description:** Retrieve details for a specific carbon source.

**Parameters:**
- `source_id` (path) - UUID of the carbon source

**Response:**
```json
{
  "id": "uuid",
  "name": "string",
  "category": "string",
  "emission_factor": "number",
  "unit": "string",
  "description": "string"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Source not found
- `500 Internal Server Error` - Database error

### 3. Get Source Categories

**GET** `/api/sources/categories/`

**Description:** Retrieve all available carbon source categories.

**Response:**
```json
{
  "categories": [
    {
      "name": "string",
      "count": "number"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Database error

### 4. Calculate Carbon Footprint

**POST** `/api/sources/calculate/`

**Description:** Calculate carbon footprint for given sources and quantities.

**Request Body:**
```json
{
  "sources": [
    {
      "source_id": "uuid",
      "quantity": "number"
    }
  ]
}
```

**Response:**
```json
{
  "total_emissions": "number",
  "unit": "kg CO2e",
  "breakdown": [
    {
      "source_name": "string",
      "quantity": "number",
      "emissions": "number"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Invalid request data
- `500 Internal Server Error` - Database error

### 5. Add Source to User

**POST** `/api/sources/user/add/`

**Description:** Add a carbon source to a user's tracking list.

**Request Body:**
```json
{
  "user_id": "uuid",
  "source_id": "uuid",
  "quantity": "number",
  "date": "YYYY-MM-DD"
}
```

**Response:**
```json
{
  "message": "Source added successfully",
  "record_id": "uuid"
}
```

**Status Codes:**
- `201 Created` - Success
- `400 Bad Request` - Missing required fields or invalid data
- `404 Not Found` - User or source not found
- `500 Internal Server Error` - Database error

### 6. Get User Records by Timeframe

**GET** `/api/sources/user/records/`

**Description:** Retrieve user's carbon source records within a timeframe.

**Query Parameters:**
- `user_id` (required) - UUID of the user
- `start_date` (required) - Start date (YYYY-MM-DD)
- `end_date` (required) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "records": [
    {
      "id": "uuid",
      "source_name": "string",
      "quantity": "number",
      "emissions": "number",
      "date": "YYYY-MM-DD"
    }
  ],
  "total_emissions": "number",
  "period": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Missing or invalid parameters
- `404 Not Found` - User not found
- `500 Internal Server Error` - Database error

### 7. Remove Source from User

**DELETE** `/api/sources/user/remove/`

**Description:** Remove a carbon source record from user's tracking.

**Query Parameters:**
- `user_id` (required) - UUID of the user
- `record_id` (required) - UUID of the record to remove

**Response:**
```json
{
  "message": "Source removed successfully"
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Missing required parameters
- `404 Not Found` - User or record not found
- `500 Internal Server Error` - Database error

### 8. Get User Sources

**GET** `/api/sources/user/sources/`

**Description:** Retrieve all carbon sources associated with a user.

**Query Parameters:**
- `user_id` (required) - UUID of the user

**Response:**
```json
{
  "user_sources": [
    {
      "source_id": "uuid",
      "source_name": "string",
      "category": "string",
      "total_quantity": "number",
      "total_emissions": "number",
      "last_used": "YYYY-MM-DD"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Missing user_id parameter
- `404 Not Found` - User not found
- `500 Internal Server Error` - Database error

---

## Activities Module

### 1. Track Carbon Consumption

**POST** `/api/activities/consumption/`

**Description:** Track and calculate carbon consumption for a user within a specified timeframe.

**Request Body:**
```json
{
  "user_id": "uuid",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "period": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  },
  "total_consumption": "number",
  "unit": "kg CO2e",
  "activities": [
    {
      "date": "YYYY-MM-DD",
      "source_name": "string",
      "quantity": "number",
      "emissions": "number"
    }
  ],
  "daily_average": "number"
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Missing required fields or invalid date format
- `404 Not Found` - User not found
- `500 Internal Server Error` - Database error

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Detailed error message"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

---

## Notes

- All datetime fields are in ISO 8601 format
- All UUIDs are in standard UUID4 format
- Emission calculations are returned in kg CO2e (kilograms of CO2 equivalent)
- Date parameters should be in YYYY-MM-DD format
- The API uses JSON for both request and response bodies
- Content-Type should be set to `application/json` for POST and PUT requests

---

## Development Status

This API is currently in development. Some endpoints may have additional features or modifications in future versions. Please refer to this documentation for the most up-to-date information on available endpoints and their usage.