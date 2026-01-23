# SMSBAT ChatHub API

ChatHub REST API manages Viber business chats, client conversations, and customer support automation workflows.

## Base URL

```
https://chatapi.smsbat.com
```

## Swagger Documentation

Interactive API documentation is available at:

```
https://chatapi.smsbat.com/index.html
```

## Authentication

ChatHub uses a Bearer token-based authentication system with JWT tokens. Tokens can be passed in two ways:

### Method 1: Authorization Header

```bash
curl -X GET https://chatapi.smsbat.com/api/company/organization \
  -H "Authorization: Bearer your-jwt-token"
```

### Method 2: X-Authorization-Key Header

```bash
curl -X GET https://chatapi.smsbat.com/api/company/organization \
  -H "X-Authorization-Key: your-jwt-token"
```

## Authentication Flow

ChatHub uses a two-level token system:

1. **Company Token** - Organization-level access token
2. **Operator Token** - Individual operator access token

### Workflow

```mermaid
graph LR
    A[Get Company Token] --> B[List Organizations]
    B --> C[List/Add Operators]
    C --> D[Get Operator Token]
    D --> E[Integrate Widget]
```

## Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/company/get-token` | Obtain company authorization token |
| GET | `/api/company/organization` | Retrieve organization list |
| GET | `/api/operator` | List operators by organization |
| POST | `/api/operator/synchronize` | Add new operators |
| POST | `/api/operator/status` | Change operator status |
| POST | `/api/operator/get-token` | Generate operator tokens (max 24h expiration) |
| POST | `/api/operator/validate-token` | Verify token validity |

## Key Features

### Company Token Management

Obtain and manage organization-level tokens for API access.

### Organization Management

- List all organizations
- Retrieve organization details
- Manage organization settings

### Operator Management

- List operators by organization
- Add new operators
- Change operator status (Active/Inactive/Deleted)
- Generate operator-specific tokens (max 24 hours)
- Validate operator tokens

### Widget Integration

Integrate ChatHub widget into web applications for real-time customer support.

## Quick Start

1. [Authentication](authentication.md) - Get your company and operator tokens
2. [Organizations](organizations.md) - Manage organizations
3. [Operators](operators.md) - Add and manage operators
4. [Widget Integration](widget.md) - Integrate chat widget

## Request Format

All requests use JSON format:

```json
{
  "login": "your-login",
  "password": "your-password"
}
```

## Response Format

Successful responses return:

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiration": "2025-01-24T12:00:00Z"
}
```

## Error Handling

HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Token Expiration

Tokens have an expiration time. When a token expires:

1. The API will return `401 Unauthorized`
2. Request a new token using the authentication endpoint
3. Update your application with the new token

## Next Steps

- [Authentication](authentication.md) - Learn how to authenticate
- [Organizations](organizations.md) - Manage organizations
- [Operators](operators.md) - Work with operators
- [Widget Integration](widget.md) - Integrate the chat widget
