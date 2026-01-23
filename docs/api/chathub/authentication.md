# Authentication

SMSBAT ChatHub API uses a two-level JWT token-based authentication system with company tokens and operator tokens.

## Authentication Flow

```mermaid
graph TD
    A[Login Credentials] --> B[Get Company Token]
    B --> C[Use Company Token]
    C --> D[Get Operator Token]
    D --> E[Use Operator Token]
    E --> F[Validate Token]
```

## Company Token

Company tokens provide organization-level access to ChatHub API.

### Get Company Token

**Endpoint:** `POST /api/company/get-token`

**Request:**

```bash
curl -X POST https://chatapi.smsbat.com/api/company/get-token \
  -H "Content-Type: application/json" \
  -d '{
    "login": "your-company-login",
    "password": "your-company-password"
  }'
```

**Request Body:**

```json
{
  "login": "string",
  "password": "string"
}
```

**Response:**

```json
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

The response is a JWT token string.

### Use Company Token

Include the company token in API requests using one of two methods:

#### Method 1: Authorization Header (Recommended)

```bash
curl -X GET https://chatapi.smsbat.com/api/company/organization \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Method 2: X-Authorization-Key Header

```bash
curl -X GET https://chatapi.smsbat.com/api/company/organization \
  -H "X-Authorization-Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Operator Token

Operator tokens provide user-specific access for individual operators within an organization.

### Get Operator Token

**Endpoint:** `POST /api/operator/get-token`

**Request:**

```bash
curl -X POST https://chatapi.smsbat.com/api/operator/get-token \
  -H "Authorization: Bearer {company-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "expiresAt": "2025-12-31T23:59:59Z"
  }'
```

**Request Body:**

```json
{
  "id": 0,
  "expiresAt": "2025-01-20T14:33:34.147Z"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Operator ID |
| `expiresAt` | string (ISO 8601) | Yes | Token expiration date and time |

**Response:**

```json
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVyYXRvcl9pZCI6MTIzLCJleHAiOjE3Mzc0MTI3OTl9.example_signature"
```

### Use Operator Token

Include the operator token in API requests:

```bash
curl -X GET https://chatapi.smsbat.com/api/operator \
  -H "Authorization: Bearer {operator-token}"
```

## Token Validation

Verify that a token is still valid before using it.

**Endpoint:** `POST /api/operator/validate-token`

**Request:**

```bash
curl -X POST https://chatapi.smsbat.com/api/operator/validate-token \
  -H "Authorization: Bearer {company-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Request Body:**

```json
{
  "token": "string"
}
```

**Response (Valid Token):**

```json
{
  "valid": true,
  "operatorId": 123,
  "expiresAt": "2025-12-31T23:59:59Z"
}
```

**Response (Invalid Token):**

```json
{
  "valid": false,
  "error": "Token expired"
}
```

## Token Expiration

### Company Tokens

- No explicit expiration in the API
- Contact your account manager for token lifecycle policies
- Rotate tokens periodically for security

### Operator Tokens

- Expiration set when requesting token (`expiresAt` parameter)
- Validate tokens before use
- Request new tokens before expiration

## Implementation Examples

### Python

```python
import requests
from datetime import datetime, timedelta

class ChatHubAuth:
    def __init__(self, base_url):
        self.base_url = base_url
        self.company_token = None
        self.operator_tokens = {}

    def get_company_token(self, login, password):
        """Get company authentication token"""
        response = requests.post(
            f"{self.base_url}/api/company/get-token",
            json={"login": login, "password": password}
        )
        response.raise_for_status()
        self.company_token = response.json()
        return self.company_token

    def get_operator_token(self, operator_id, expires_days=30):
        """Get operator token with expiration"""
        expires_at = (
            datetime.utcnow() + timedelta(days=expires_days)
        ).isoformat() + "Z"

        response = requests.post(
            f"{self.base_url}/api/operator/get-token",
            headers={"Authorization": f"Bearer {self.company_token}"},
            json={"id": operator_id, "expiresAt": expires_at}
        )
        response.raise_for_status()

        token = response.json()
        self.operator_tokens[operator_id] = token
        return token

    def validate_token(self, token):
        """Validate if token is still valid"""
        response = requests.post(
            f"{self.base_url}/api/operator/validate-token",
            headers={"Authorization": f"Bearer {self.company_token}"},
            json={"token": token}
        )
        response.raise_for_status()
        return response.json()

# Usage
auth = ChatHubAuth("https://chatapi.smsbat.com")

# Get company token
company_token = auth.get_company_token("login", "password")

# Get operator token
operator_token = auth.get_operator_token(operator_id=123, expires_days=30)

# Validate token
is_valid = auth.validate_token(operator_token)
print(f"Token valid: {is_valid['valid']}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

class ChatHubAuth {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.companyToken = null;
    this.operatorTokens = {};
  }

  async getCompanyToken(login, password) {
    const response = await axios.post(
      `${this.baseUrl}/api/company/get-token`,
      { login, password }
    );

    this.companyToken = response.data;
    return this.companyToken;
  }

  async getOperatorToken(operatorId, expiresDays = 30) {
    const expiresAt = new Date(
      Date.now() + expiresDays * 24 * 60 * 60 * 1000
    ).toISOString();

    const response = await axios.post(
      `${this.baseUrl}/api/operator/get-token`,
      { id: operatorId, expiresAt },
      {
        headers: {
          Authorization: `Bearer ${this.companyToken}`
        }
      }
    );

    const token = response.data;
    this.operatorTokens[operatorId] = token;
    return token;
  }

  async validateToken(token) {
    const response = await axios.post(
      `${this.baseUrl}/api/operator/validate-token`,
      { token },
      {
        headers: {
          Authorization: `Bearer ${this.companyToken}`
        }
      }
    );

    return response.data;
  }
}

// Usage
const auth = new ChatHubAuth('https://chatapi.smsbat.com');

async function authenticate() {
  // Get company token
  const companyToken = await auth.getCompanyToken('login', 'password');

  // Get operator token
  const operatorToken = await auth.getOperatorToken(123, 30);

  // Validate token
  const validation = await auth.validateToken(operatorToken);
  console.log('Token valid:', validation.valid);
}

authenticate();
```

### PHP

```php
<?php

class ChatHubAuth {
    private $baseUrl;
    private $companyToken;
    private $operatorTokens = [];

    public function __construct($baseUrl) {
        $this->baseUrl = $baseUrl;
    }

    public function getCompanyToken($login, $password) {
        $ch = curl_init($this->baseUrl . '/api/company/get-token');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json'
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
            'login' => $login,
            'password' => $password
        ]));

        $response = curl_exec($ch);
        curl_close($ch);

        $this->companyToken = json_decode($response);
        return $this->companyToken;
    }

    public function getOperatorToken($operatorId, $expiresDays = 30) {
        $expiresAt = date(
            'Y-m-d\TH:i:s\Z',
            time() + ($expiresDays * 24 * 60 * 60)
        );

        $ch = curl_init($this->baseUrl . '/api/operator/get-token');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->companyToken
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
            'id' => $operatorId,
            'expiresAt' => $expiresAt
        ]));

        $response = curl_exec($ch);
        curl_close($ch);

        $token = json_decode($response);
        $this->operatorTokens[$operatorId] = $token;
        return $token;
    }

    public function validateToken($token) {
        $ch = curl_init($this->baseUrl . '/api/operator/validate-token');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->companyToken
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
            'token' => $token
        ]));

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }
}

// Usage
$auth = new ChatHubAuth('https://chatapi.smsbat.com');

// Get company token
$companyToken = $auth->getCompanyToken('login', 'password');

// Get operator token
$operatorToken = $auth->getOperatorToken(123, 30);

// Validate token
$validation = $auth->validateToken($operatorToken);
echo "Token valid: " . ($validation['valid'] ? 'Yes' : 'No');
```

## Best Practices

### Token Storage

- ✅ Store tokens securely (encrypted database, secrets manager)
- ✅ Never commit tokens to version control
- ✅ Use environment variables for credentials
- ❌ Don't store tokens in plain text
- ❌ Don't expose tokens in client-side code

### Token Rotation

- Rotate company tokens periodically (every 3-6 months)
- Set reasonable expiration for operator tokens (7-30 days)
- Implement automatic token refresh before expiration
- Revoke tokens when operators leave

### Error Handling

```javascript
async function authenticateWithRetry(login, password, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await getCompanyToken(login, password);
    } catch (error) {
      if (error.response?.status === 401) {
        throw new Error('Invalid credentials');
      }

      if (i === retries - 1) throw error;

      // Wait before retry
      await new Promise(resolve =>
        setTimeout(resolve, Math.pow(2, i) * 1000)
      );
    }
  }
}
```

### Token Validation

Always validate tokens before critical operations:

```javascript
async function performSecureOperation(token, operation) {
  // Validate token first
  const validation = await validateToken(token);

  if (!validation.valid) {
    throw new Error('Token expired or invalid');
  }

  // Proceed with operation
  return await operation();
}
```

## Security Considerations

### HTTPS Only

Always use HTTPS when sending authentication requests:

```javascript
// ✅ Correct
const baseUrl = 'https://chatapi.smsbat.com';

// ❌ Wrong - never use HTTP for authentication
const baseUrl = 'http://api.chathub.smsbat.com';
```

### Token Scope

Use the appropriate token for each operation:

- **Company Token**: Organization management, operator creation
- **Operator Token**: Chat operations, message handling

### Rate Limiting

Implement rate limiting for authentication requests:

```javascript
class RateLimitedAuth {
  constructor() {
    this.lastRequest = 0;
    this.minInterval = 1000; // 1 second between requests
  }

  async getToken(login, password) {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequest;

    if (timeSinceLastRequest < this.minInterval) {
      await new Promise(resolve =>
        setTimeout(resolve, this.minInterval - timeSinceLastRequest)
      );
    }

    this.lastRequest = Date.now();
    return await makeAuthRequest(login, password);
  }
}
```

## Troubleshooting

### 401 Unauthorized

- Verify credentials are correct
- Check token hasn't expired
- Ensure token is included in request headers
- Validate token format

### 403 Forbidden

- Verify token has required permissions
- Check if using correct token type (company vs operator)
- Ensure token hasn't been revoked

### Token Expired

- Request new token
- Implement automatic token refresh
- Set appropriate expiration times

## Next Steps

- [Organizations](organizations.md) - Manage organizations
- [Operators](operators.md) - Work with operators
- [Widget Integration](widget.md) - Integrate chat widget
