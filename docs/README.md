# SmartFit Documentation

This directory contains documentation for the SmartFit application.

## Contents

- [API Documentation](api_documentation.md): Comprehensive documentation for all API endpoints
- [Project Structure](project_structure.md): Overview of the project's directory structure and architecture
- [Development Guide](development_guide.md): Guide for developers working on the project

## API Documentation

The [API Documentation](api_documentation.md) provides detailed information about all available API endpoints, including:

- Authentication
- User Management
- Diet Plans
- Workout Plans
- Video Tutorials
- Video Library
- Body Measurements
- Recipe Library
- Shopping
- Contact Forms
- Error Handling
- Pagination

Each endpoint is documented with:

- URL
- HTTP Method
- Authentication requirements
- Request parameters and body
- Response format
- Example requests and responses

## Getting Started

To get started with the SmartFit API, follow these steps:

1. Register a user account using the `/api/register/` endpoint
2. Obtain an authentication token using the `/api/token/` endpoint
3. Include the token in the Authorization header for all authenticated requests:
   ```
   Authorization: Bearer your_access_token
   ```

## Testing the API

You can test the API using tools like:

- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [curl](https://curl.se/)

Example curl request:

```bash
curl -X POST \
  http://localhost:8000/api/token/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
}'
```

## Contributing to Documentation

When adding new API endpoints or modifying existing ones, please update the API documentation accordingly. Follow these guidelines:

1. Use the existing format for consistency
2. Include all required parameters and their descriptions
3. Provide example requests and responses
4. Document error cases and their responses

## Contact

For questions or issues related to the API, please contact the development team or submit an issue in the project repository.
