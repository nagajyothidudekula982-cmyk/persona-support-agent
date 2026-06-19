# Authentication Guide

## API Key Authentication

To access the API, every request must include a valid API key.

Example:

Authorization: Bearer YOUR_API_KEY

## Common Errors

401 Unauthorized
- Invalid API key
- Expired API key
- Missing Authorization header

403 Forbidden
- Your account does not have permission to access this resource.

## Best Practices

- Never share your API key.
- Store API keys securely using environment variables.
- Rotate API keys regularly for security.
