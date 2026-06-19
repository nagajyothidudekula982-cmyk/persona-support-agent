API Authentication Guide

Overview:
All API requests require authentication using an API key.

Format:
Authorization: Bearer <YOUR_API_KEY>

Common Errors:

401 Unauthorized:
- Invalid API key
- Expired API key
- Missing API key

403 Forbidden:
- User does not have permission
- Role-based access denied

Best Practices:
- Never expose API keys in frontend code
- Store keys in environment variables
- Rotate keys every 30–60 days
