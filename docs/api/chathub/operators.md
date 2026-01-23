# Operators

Manage chat operators within your ChatHub organizations. Operators are agents who handle customer conversations.

## Overview

Operators in ChatHub:

- Handle customer chat conversations
- Belong to specific organizations
- Have active, inactive, or deleted status
- Can have individual authentication tokens
- Receive and respond to messages

## List Operators

Retrieve all operators for a specific organization.

### Endpoint

```
GET /api/operator?organizationId={id}
```

### Request

```bash
curl -X GET "https://api.chathub.smsbat.com/api/operator?organizationId=24" \
  -H "Authorization: Bearer {company-token}" \
  -H "Accept: text/plain"
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `organizationId` | integer | Query | Yes | Organization ID |

### Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | Bearer {token} | Yes |
| `Accept` | text/plain | Yes |

### Response

```json
[
  {
    "id": 101,
    "name": "John Smith",
    "status": 0,
    "organization": {
      "id": 24,
      "name": "Customer Support"
    }
  },
  {
    "id": 102,
    "name": "Sarah Johnson",
    "status": 0,
    "organization": {
      "id": 24,
      "name": "Customer Support"
    }
  },
  {
    "id": 103,
    "name": "Mike Wilson",
    "status": 1,
    "organization": {
      "id": 24,
      "name": "Customer Support"
    }
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique operator identifier |
| `name` | string | Operator display name |
| `status` | integer | Operator status (0=Active, 1=Inactive, 2=Deleted) |
| `organization` | object | Parent organization details |
| `organization.id` | integer | Organization ID |
| `organization.name` | string | Organization name |

## Operator Status

| Status | Value | Description |
|--------|-------|-------------|
| Active | 0 | Operator is currently working and can receive chats |
| Inactive | 1 | Operator is temporarily disabled |
| Deleted | 2 | Operator has been removed from system |

## Add Operators

Add new operators to organizations using the synchronize endpoint.

### Endpoint

```
POST /api/operator/synchronize
```

### Request

```bash
curl -X POST https://api.chathub.smsbat.com/api/operator/synchronize \
  -H "Authorization: Bearer {company-token}" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "organizationId": 24,
      "name": "Alex Brown"
    },
    {
      "organizationId": 24,
      "name": "Emma Davis"
    }
  ]'
```

### Request Body

Array of operator objects:

```json
[
  {
    "organizationId": 24,
    "name": "Alex Brown"
  },
  {
    "organizationId": 24,
    "name": "Emma Davis"
  }
]
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organizationId` | integer | Yes | Target organization ID |
| `name` | string | Yes | Operator display name |

### Response

```json
[
  {
    "id": 104,
    "name": "Alex Brown",
    "status": 0
  },
  {
    "id": 105,
    "name": "Emma Davis",
    "status": 0
  }
]
```

## Implementation Examples

### Python

```python
import requests

class OperatorManager:
    def __init__(self, company_token, base_url='https://api.chathub.smsbat.com'):
        self.company_token = company_token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {company_token}',
            'Accept': 'text/plain'
        }

    def list_operators(self, organization_id):
        """Get all operators for an organization"""
        response = requests.get(
            f'{self.base_url}/api/operator',
            headers=self.headers,
            params={'organizationId': organization_id}
        )
        response.raise_for_status()
        return response.json()

    def add_operators(self, operators):
        """Add new operators
        Args:
            operators: List of dicts with organizationId and name
        """
        response = requests.post(
            f'{self.base_url}/api/operator/synchronize',
            headers={**self.headers, 'Content-Type': 'application/json'},
            json=operators
        )
        response.raise_for_status()
        return response.json()

    def get_active_operators(self, organization_id):
        """Get only active operators"""
        operators = self.list_operators(organization_id)
        return [op for op in operators if op['status'] == 0]

    def find_operator_by_name(self, organization_id, name):
        """Find operator by name"""
        operators = self.list_operators(organization_id)
        for operator in operators:
            if operator['name'].lower() == name.lower():
                return operator
        return None

# Usage
manager = OperatorManager('your-company-token')

# List operators
operators = manager.list_operators(organization_id=24)
print(f"Found {len(operators)} operators")

# Get only active operators
active = manager.get_active_operators(24)
print(f"{len(active)} active operators")

# Add new operators
new_operators = manager.add_operators([
    {'organizationId': 24, 'name': 'John Doe'},
    {'organizationId': 24, 'name': 'Jane Smith'}
])
print(f"Added {len(new_operators)} operators")

# Find operator by name
operator = manager.find_operator_by_name(24, 'John Doe')
if operator:
    print(f"Found operator: {operator['name']} (ID: {operator['id']})")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

class OperatorManager {
  constructor(companyToken, baseUrl = 'https://api.chathub.smsbat.com') {
    this.companyToken = companyToken;
    this.baseUrl = baseUrl;
    this.headers = {
      'Authorization': `Bearer ${companyToken}`,
      'Accept': 'text/plain'
    };
  }

  async listOperators(organizationId) {
    const response = await axios.get(
      `${this.baseUrl}/api/operator`,
      {
        headers: this.headers,
        params: { organizationId }
      }
    );

    return response.data;
  }

  async addOperators(operators) {
    const response = await axios.post(
      `${this.baseUrl}/api/operator/synchronize`,
      operators,
      {
        headers: {
          ...this.headers,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;
  }

  async getActiveOperators(organizationId) {
    const operators = await this.listOperators(organizationId);
    return operators.filter(op => op.status === 0);
  }

  async findOperatorByName(organizationId, name) {
    const operators = await this.listOperators(organizationId);
    return operators.find(op =>
      op.name.toLowerCase() === name.toLowerCase()
    );
  }

  async getOperatorById(organizationId, operatorId) {
    const operators = await this.listOperators(organizationId);
    return operators.find(op => op.id === operatorId);
  }
}

// Usage
const manager = new OperatorManager('your-company-token');

async function manageOperators() {
  // List operators
  const operators = await manager.listOperators(24);
  console.log(`Found ${operators.length} operators`);

  // Get active operators
  const active = await manager.getActiveOperators(24);
  console.log(`${active.length} active operators`);

  // Add new operators
  const newOperators = await manager.addOperators([
    { organizationId: 24, name: 'John Doe' },
    { organizationId: 24, name: 'Jane Smith' }
  ]);
  console.log(`Added ${newOperators.length} operators`);

  // Find operator by name
  const operator = await manager.findOperatorByName(24, 'John Doe');
  if (operator) {
    console.log(`Found: ${operator.name} (ID: ${operator.id})`);
  }
}

manageOperators();
```

### PHP

```php
<?php

class OperatorManager {
    private $companyToken;
    private $baseUrl;

    public function __construct($companyToken, $baseUrl = 'https://api.chathub.smsbat.com') {
        $this->companyToken = $companyToken;
        $this->baseUrl = $baseUrl;
    }

    public function listOperators($organizationId) {
        $url = $this->baseUrl . '/api/operator?organizationId=' . $organizationId;

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->companyToken,
            'Accept: text/plain'
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }

    public function addOperators($operators) {
        $ch = curl_init($this->baseUrl . '/api/operator/synchronize');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->companyToken,
            'Content-Type: application/json',
            'Accept: text/plain'
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($operators));

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }

    public function getActiveOperators($organizationId) {
        $operators = $this->listOperators($organizationId);
        return array_filter($operators, function($op) {
            return $op['status'] === 0;
        });
    }

    public function findOperatorByName($organizationId, $name) {
        $operators = $this->listOperators($organizationId);

        foreach ($operators as $operator) {
            if (strcasecmp($operator['name'], $name) === 0) {
                return $operator;
            }
        }

        return null;
    }
}

// Usage
$manager = new OperatorManager('your-company-token');

// List operators
$operators = $manager->listOperators(24);
echo "Found " . count($operators) . " operators\n";

// Get active operators
$active = $manager->getActiveOperators(24);
echo count($active) . " active operators\n";

// Add new operators
$newOperators = $manager->addOperators([
    ['organizationId' => 24, 'name' => 'John Doe'],
    ['organizationId' => 24, 'name' => 'Jane Smith']
]);
echo "Added " . count($newOperators) . " operators\n";

// Find operator
$operator = $manager->findOperatorByName(24, 'John Doe');
if ($operator) {
    echo "Found: " . $operator['name'] . " (ID: " . $operator['id'] . ")\n";
}
```

## Common Use Cases

### Onboard New Team Members

```javascript
async function onboardOperators(teamMembers, organizationId) {
  const operators = teamMembers.map(member => ({
    organizationId,
    name: member.fullName
  }));

  const created = await addOperators(operators);

  // Generate tokens for each operator
  for (const operator of created) {
    const token = await getOperatorToken(operator.id);
    await sendWelcomeEmail(operator, token);
  }

  return created;
}
```

### Monitor Operator Status

```javascript
async function getOperatorStatistics(organizationId) {
  const operators = await listOperators(organizationId);

  return {
    total: operators.length,
    active: operators.filter(op => op.status === 0).length,
    inactive: operators.filter(op => op.status === 1).length,
    deleted: operators.filter(op => op.status === 2).length
  };
}
```

### Load Balancing

```javascript
async function assignChatToOperator(organizationId, chatId) {
  const activeOperators = await getActiveOperators(organizationId);

  if (activeOperators.length === 0) {
    throw new Error('No active operators available');
  }

  // Simple round-robin assignment
  const operatorIndex = chatId % activeOperators.length;
  return activeOperators[operatorIndex];
}
```

### Bulk Import

```javascript
async function importOperatorsFromCSV(csvData, organizationId) {
  const lines = csvData.split('\n').slice(1); // Skip header

  const operators = lines
    .filter(line => line.trim())
    .map(line => {
      const [name] = line.split(',');
      return { organizationId, name: name.trim() };
    });

  // Batch import in chunks of 100
  const chunkSize = 100;
  const results = [];

  for (let i = 0; i < operators.length; i += chunkSize) {
    const chunk = operators.slice(i, i + chunkSize);
    const imported = await addOperators(chunk);
    results.push(...imported);

    console.log(`Imported ${results.length}/${operators.length}`);
  }

  return results;
}
```

## Best Practices

### Error Handling

```javascript
async function addOperatorsSafely(operators) {
  try {
    return await addOperators(operators);
  } catch (error) {
    if (error.response?.status === 400) {
      console.error('Invalid operator data:', error.response.data);
      // Handle validation errors
    } else if (error.response?.status === 401) {
      console.error('Authentication failed');
      // Refresh token
    } else {
      console.error('Unexpected error:', error);
    }

    throw error;
  }
}
```

### Caching

```javascript
class CachedOperatorManager extends OperatorManager {
  constructor(companyToken) {
    super(companyToken);
    this.cache = new Map();
    this.cacheTTL = 60000; // 1 minute
  }

  async listOperators(organizationId, useCache = true) {
    const cacheKey = `org_${organizationId}`;
    const cached = this.cache.get(cacheKey);

    if (useCache && cached && Date.now() - cached.time < this.cacheTTL) {
      return cached.data;
    }

    const data = await super.listOperators(organizationId);

    this.cache.set(cacheKey, {
      data,
      time: Date.now()
    });

    return data;
  }

  clearCache(organizationId = null) {
    if (organizationId) {
      this.cache.delete(`org_${organizationId}`);
    } else {
      this.cache.clear();
    }
  }
}
```

### Validation

```javascript
function validateOperatorData(operators) {
  const errors = [];

  operators.forEach((op, index) => {
    if (!op.organizationId) {
      errors.push(`Operator ${index}: Missing organizationId`);
    }

    if (!op.name || op.name.trim().length === 0) {
      errors.push(`Operator ${index}: Name is required`);
    }

    if (op.name && op.name.length > 100) {
      errors.push(`Operator ${index}: Name too long (max 100 chars)`);
    }
  });

  if (errors.length > 0) {
    throw new Error('Validation failed:\n' + errors.join('\n'));
  }
}

// Usage
try {
  validateOperatorData(operatorData);
  await addOperators(operatorData);
} catch (error) {
  console.error(error.message);
}
```

### Rate Limiting

```javascript
class RateLimitedOperatorManager extends OperatorManager {
  constructor(companyToken, requestsPerSecond = 5) {
    super(companyToken);
    this.minInterval = 1000 / requestsPerSecond;
    this.lastRequest = 0;
  }

  async throttle() {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequest;

    if (timeSinceLastRequest < this.minInterval) {
      await new Promise(resolve =>
        setTimeout(resolve, this.minInterval - timeSinceLastRequest)
      );
    }

    this.lastRequest = Date.now();
  }

  async listOperators(organizationId) {
    await this.throttle();
    return super.listOperators(organizationId);
  }

  async addOperators(operators) {
    await this.throttle();
    return super.addOperators(operators);
  }
}
```

## Troubleshooting

### No Operators Returned

- Verify organizationId is correct
- Check organization exists and has operators
- Ensure company token has access to organization

### Failed to Add Operators

- Verify organizationId exists
- Check operator name format
- Ensure company token is valid
- Verify JSON format is correct

### 401 Unauthorized

- Verify company token is valid
- Check token hasn't expired
- Request new token if needed

### Duplicate Operators

The synchronize endpoint may allow duplicate names. Implement deduplication:

```javascript
async function addUniqueOperators(newOperators, organizationId) {
  const existing = await listOperators(organizationId);
  const existingNames = new Set(
    existing.map(op => op.name.toLowerCase())
  );

  const unique = newOperators.filter(op =>
    !existingNames.has(op.name.toLowerCase())
  );

  if (unique.length === 0) {
    return [];
  }

  return await addOperators(unique);
}
```

## Next Steps

- [Authentication](authentication.md) - Get operator tokens
- [Organizations](organizations.md) - Manage organizations
- [Widget Integration](widget.md) - Integrate chat widget
