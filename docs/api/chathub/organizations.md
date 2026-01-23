# Organizations

Manage organizations within your ChatHub account. Organizations serve as containers for operators and chat operations.

## Overview

Organizations in ChatHub:

- Group operators by department, team, or function
- Isolate chat operations between different business units
- Manage permissions at organizational level
- Track metrics per organization

## List Organizations

Retrieve all organizations accessible with your company token.

### Endpoint

```
GET /api/company/organization
```

### Request

```bash
curl -X GET https://chatapi.smsbat.com/api/company/organization \
  -H "Authorization: Bearer {company-token}" \
  -H "Accept: text/plain"
```

### Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | Bearer {token} | Yes | Company token |
| `Accept` | text/plain | Yes | Response format |

### Response

```json
[
  {
    "id": 6,
    "name": "Customer Support"
  },
  {
    "id": 24,
    "name": "Sales Team"
  },
  {
    "id": 42,
    "name": "Technical Support"
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique organization identifier |
| `name` | string | Organization display name |

## Organization Structure

Each organization contains:

- **Operators**: Chat agents assigned to organization
- **Chat Sessions**: Active and historical chat conversations
- **Widgets**: Embedded chat widgets for this organization
- **Settings**: Organization-specific configuration

## Use Cases

### Multi-Department Company

```
Company: ACME Corp
├── Organization: Sales (id: 10)
│   ├── Operator: John (Sales Rep)
│   └── Operator: Sarah (Sales Manager)
├── Organization: Support (id: 20)
│   ├── Operator: Mike (Support Agent)
│   └── Operator: Lisa (Support Lead)
└── Organization: Technical (id: 30)
    └── Operator: Alex (Tech Expert)
```

### Multi-Brand Business

```
Company: Retail Group
├── Organization: Brand A (id: 101)
│   └── Widget: branda.com
├── Organization: Brand B (id: 102)
│   └── Widget: brandb.com
└── Organization: Brand C (id: 103)
    └── Widget: brandc.com
```

## Implementation Examples

### Python

```python
import requests

def get_organizations(company_token):
    """Get list of all organizations"""
    response = requests.get(
        'https://chatapi.smsbat.com/api/company/organization',
        headers={
            'Authorization': f'Bearer {company_token}',
            'Accept': 'text/plain'
        }
    )
    response.raise_for_status()
    return response.json()

def find_organization_by_name(company_token, name):
    """Find organization by name"""
    organizations = get_organizations(company_token)

    for org in organizations:
        if org['name'].lower() == name.lower():
            return org

    return None

def get_organization_by_id(company_token, org_id):
    """Get specific organization by ID"""
    organizations = get_organizations(company_token)

    for org in organizations:
        if org['id'] == org_id:
            return org

    return None

# Usage
token = "your-company-token"

# Get all organizations
orgs = get_organizations(token)
print(f"Found {len(orgs)} organizations")

# Find specific organization
support_org = find_organization_by_name(token, "Support")
if support_org:
    print(f"Support organization ID: {support_org['id']}")

# Get by ID
org = get_organization_by_id(token, 24)
print(f"Organization: {org['name']}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

class OrganizationManager {
  constructor(companyToken) {
    this.companyToken = companyToken;
    this.baseUrl = 'https://chatapi.smsbat.com';
  }

  async getOrganizations() {
    const response = await axios.get(
      `${this.baseUrl}/api/company/organization`,
      {
        headers: {
          'Authorization': `Bearer ${this.companyToken}`,
          'Accept': 'text/plain'
        }
      }
    );

    return response.data;
  }

  async findByName(name) {
    const organizations = await this.getOrganizations();

    return organizations.find(org =>
      org.name.toLowerCase() === name.toLowerCase()
    );
  }

  async findById(id) {
    const organizations = await this.getOrganizations();
    return organizations.find(org => org.id === id);
  }

  async listByIds(ids) {
    const organizations = await this.getOrganizations();
    return organizations.filter(org => ids.includes(org.id));
  }
}

// Usage
const manager = new OrganizationManager('your-company-token');

async function manageOrganizations() {
  // Get all organizations
  const orgs = await manager.getOrganizations();
  console.log(`Found ${orgs.length} organizations`);

  // Find by name
  const support = await manager.findByName('Support');
  console.log('Support org:', support);

  // Find by ID
  const org = await manager.findById(24);
  console.log('Organization:', org);

  // Get multiple organizations
  const selectedOrgs = await manager.listByIds([10, 20, 30]);
  console.log('Selected organizations:', selectedOrgs);
}

manageOrganizations();
```

### PHP

```php
<?php

class OrganizationManager {
    private $companyToken;
    private $baseUrl = 'https://chatapi.smsbat.com';

    public function __construct($companyToken) {
        $this->companyToken = $companyToken;
    }

    public function getOrganizations() {
        $ch = curl_init($this->baseUrl . '/api/company/organization');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->companyToken,
            'Accept: text/plain'
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }

    public function findByName($name) {
        $organizations = $this->getOrganizations();

        foreach ($organizations as $org) {
            if (strcasecmp($org['name'], $name) === 0) {
                return $org;
            }
        }

        return null;
    }

    public function findById($id) {
        $organizations = $this->getOrganizations();

        foreach ($organizations as $org) {
            if ($org['id'] === $id) {
                return $org;
            }
        }

        return null;
    }
}

// Usage
$manager = new OrganizationManager('your-company-token');

// Get all organizations
$orgs = $manager->getOrganizations();
echo "Found " . count($orgs) . " organizations\n";

// Find by name
$support = $manager->findByName('Support');
if ($support) {
    echo "Support organization ID: " . $support['id'] . "\n";
}

// Find by ID
$org = $manager->findById(24);
if ($org) {
    echo "Organization: " . $org['name'] . "\n";
}
```

## Working with Organizations

### List All Organizations

```javascript
const organizations = await getOrganizations(companyToken);

organizations.forEach(org => {
  console.log(`${org.id}: ${org.name}`);
});
```

Output:
```
6: Customer Support
24: Sales Team
42: Technical Support
```

### Filter Organizations

```javascript
// Get organizations matching criteria
const supportOrgs = organizations.filter(org =>
  org.name.toLowerCase().includes('support')
);

// Get organizations by IDs
const specificOrgs = organizations.filter(org =>
  [10, 20, 30].includes(org.id)
);
```

### Map Organizations

```javascript
// Create ID to name mapping
const orgMap = organizations.reduce((map, org) => {
  map[org.id] = org.name;
  return map;
}, {});

console.log(orgMap[24]); // "Sales Team"
```

## Integration Patterns

### Organization Selection UI

```javascript
async function renderOrganizationSelect(companyToken) {
  const organizations = await getOrganizations(companyToken);

  const select = document.createElement('select');
  select.id = 'organization-select';

  organizations.forEach(org => {
    const option = document.createElement('option');
    option.value = org.id;
    option.textContent = org.name;
    select.appendChild(option);
  });

  return select;
}
```

### Route Chats by Organization

```javascript
async function routeChatToOrganization(chatRequest) {
  const organizations = await getOrganizations(companyToken);

  // Route based on business logic
  let targetOrg;

  if (chatRequest.department === 'sales') {
    targetOrg = organizations.find(org =>
      org.name.toLowerCase().includes('sales')
    );
  } else if (chatRequest.department === 'support') {
    targetOrg = organizations.find(org =>
      org.name.toLowerCase().includes('support')
    );
  }

  return targetOrg?.id;
}
```

### Organization Metrics

```javascript
class OrganizationMetrics {
  async getMetrics(companyToken, orgId) {
    // Get operators for organization
    const operators = await getOperators(companyToken, orgId);

    // Get chat statistics (example)
    return {
      organizationId: orgId,
      operatorCount: operators.length,
      activeOperators: operators.filter(op => op.isActive).length,
      // Add more metrics as needed
    };
  }

  async getAllMetrics(companyToken) {
    const organizations = await getOrganizations(companyToken);

    const metrics = await Promise.all(
      organizations.map(org =>
        this.getMetrics(companyToken, org.id)
      )
    );

    return metrics;
  }
}
```

## Best Practices

### Caching

Cache organization list to reduce API calls:

```javascript
class CachedOrganizationManager {
  constructor(companyToken, cacheTTL = 300000) { // 5 minutes
    this.companyToken = companyToken;
    this.cacheTTL = cacheTTL;
    this.cache = null;
    this.cacheTime = 0;
  }

  async getOrganizations(forceRefresh = false) {
    const now = Date.now();

    if (!forceRefresh &&
        this.cache &&
        now - this.cacheTime < this.cacheTTL) {
      return this.cache;
    }

    this.cache = await fetchOrganizations(this.companyToken);
    this.cacheTime = now;

    return this.cache;
  }

  clearCache() {
    this.cache = null;
    this.cacheTime = 0;
  }
}
```

### Error Handling

```javascript
async function getOrganizationsWithRetry(companyToken, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await getOrganizations(companyToken);
    } catch (error) {
      if (error.response?.status === 401) {
        throw new Error('Invalid or expired company token');
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

### Validation

```javascript
function validateOrganizationId(organizations, orgId) {
  const org = organizations.find(o => o.id === orgId);

  if (!org) {
    throw new Error(`Organization ${orgId} not found`);
  }

  return org;
}

// Usage
const organizations = await getOrganizations(companyToken);
const org = validateOrganizationId(organizations, requestedOrgId);
```

## Troubleshooting

### Empty Organization List

- Verify company token is valid
- Check token has organization access
- Ensure organizations exist in account

### Organization Not Found

- Verify organization ID is correct
- Check organization wasn't deleted
- Refresh organization list

### 401 Unauthorized

- Verify company token is valid and not expired
- Request new company token if needed
- Check token format is correct

## Next Steps

- [Authentication](authentication.md) - Get company token
- [Operators](operators.md) - Manage operators in organizations
- [Widget Integration](widget.md) - Integrate chat for organizations
