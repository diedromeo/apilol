API Documentation
This document describes the public API endpoints for the Flask application.

/api Endpoint
This endpoint requires a valid authentication token to access.

URL: /api

Method: GET

Authentication: A valid token must be provided in the X-CTF-Token header.

Example Request:
GET /api HTTP/1.1
Host: [your_app_url]
X-CTF-Token: your_secret_token

Example Response (Success):
A successful request will return a JSON object with a status and a message.

{
  "status": "success",
  "message": "Token is valid. Good job! But this isn't the flag. You're on the right track, but something is missing..."
}

Example Response (Failure):
An invalid or missing token will result in a 403 Forbidden response.

{
  "status": "error",
  "message": "Forbidden"
}
s