# Widget Integration

Integrate ChatHub widget into your website to provide real-time chat support for your customers.

## Overview

The ChatHub widget is a JavaScript component that:

- Embeds into any website
- Provides real-time chat interface
- Connects customers with operators
- Requires operator authentication token
- Loads as an ES module

## Quick Start

### 1. Get Operator Token

First, obtain an operator token following the [authentication flow](authentication.md):

```javascript
// 1. Get company token
const companyToken = await getCompanyToken(login, password);

// 2. Get organization
const organizations = await getOrganizations(companyToken);
const orgId = organizations[0].id;

// 3. Get operator
const operators = await getOperators(companyToken, orgId);
const operatorId = operators[0].id;

// 4. Generate operator token
const operatorToken = await getOperatorToken(
  companyToken,
  operatorId,
  expiresAt
);

// 5. Validate token
const isValid = await validateToken(companyToken, operatorToken);
```

### 2. Embed Widget

Add the widget script to your HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Website</title>
</head>
<body>
    <!-- Your website content -->

    <!-- ChatHub Widget -->
    <script type="module" id="operator-chat-panel-script"
      src="https://widget.smsbat.com/operator-chat-panel/widget-script.js"
      token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."></script>
</body>
</html>
```

### Script Parameters

| Attribute | Value | Required | Description |
|-----------|-------|----------|-------------|
| `type` | `module` | Yes | ES module type |
| `id` | `operator-chat-panel-script` | Yes | Unique script identifier |
| `src` | Widget URL | Yes | Widget script location |
| `token` | JWT token | Yes | Operator authentication token |

## Integration Methods

### Static HTML

For static websites, embed directly in HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Website</title>
</head>
<body>
    <h1>Welcome to My Website</h1>

    <!-- ChatHub Widget -->
    <script type="module" id="operator-chat-panel-script"
      src="https://widget.smsbat.com/operator-chat-panel/widget-script.js"
      token="YOUR_OPERATOR_TOKEN"></script>
</body>
</html>
```

### Dynamic Injection (JavaScript)

For single-page applications, inject dynamically:

```javascript
function loadChatHubWidget(operatorToken) {
  // Check if widget already loaded
  const existing = document.getElementById('operator-chat-panel-script');
  if (existing) {
    existing.remove();
  }

  // Create script element
  const script = document.createElement('script');
  script.type = 'module';
  script.id = 'operator-chat-panel-script';
  script.src = 'https://widget.smsbat.com/operator-chat-panel/widget-script.js';
  script.setAttribute('token', operatorToken);

  // Append to body
  document.body.appendChild(script);
}

// Usage
const token = await getOperatorToken();
loadChatHubWidget(token);
```

### React

```jsx
import { useEffect } from 'react';

function ChatHubWidget({ operatorToken }) {
  useEffect(() => {
    if (!operatorToken) return;

    // Load widget
    const script = document.createElement('script');
    script.type = 'module';
    script.id = 'operator-chat-panel-script';
    script.src = 'https://widget.smsbat.com/operator-chat-panel/widget-script.js';
    script.setAttribute('token', operatorToken);

    document.body.appendChild(script);

    // Cleanup on unmount
    return () => {
      const existing = document.getElementById('operator-chat-panel-script');
      if (existing) {
        existing.remove();
      }
    };
  }, [operatorToken]);

  return null;
}

// Usage
function App() {
  const [token, setToken] = useState('');

  useEffect(() => {
    async function init() {
      const operatorToken = await fetchOperatorToken();
      setToken(operatorToken);
    }
    init();
  }, []);

  return (
    <div>
      <h1>My App</h1>
      <ChatHubWidget operatorToken={token} />
    </div>
  );
}
```

### Vue.js

```vue
<template>
  <div id="app">
    <h1>My App</h1>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      operatorToken: ''
    };
  },
  async mounted() {
    // Get operator token
    this.operatorToken = await this.fetchOperatorToken();

    // Load widget
    this.loadWidget();
  },
  methods: {
    async fetchOperatorToken() {
      // Your token fetching logic
      const response = await fetch('/api/chathub/token');
      return response.text();
    },
    loadWidget() {
      if (!this.operatorToken) return;

      const script = document.createElement('script');
      script.type = 'module';
      script.id = 'operator-chat-panel-script';
      script.src = 'https://widget.smsbat.com/operator-chat-panel/widget-script.js';
      script.setAttribute('token', this.operatorToken);

      document.body.appendChild(script);
    }
  },
  beforeUnmount() {
    const script = document.getElementById('operator-chat-panel-script');
    if (script) {
      script.remove();
    }
  }
};
</script>
```

### Angular

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-root',
  template: '<h1>My App</h1>'
})
export class AppComponent implements OnInit, OnDestroy {
  private operatorToken: string = '';

  async ngOnInit() {
    // Get operator token
    this.operatorToken = await this.fetchOperatorToken();

    // Load widget
    this.loadWidget();
  }

  ngOnDestroy() {
    const script = document.getElementById('operator-chat-panel-script');
    if (script) {
      script.remove();
    }
  }

  private async fetchOperatorToken(): Promise<string> {
    const response = await fetch('/api/chathub/token');
    return response.text();
  }

  private loadWidget() {
    if (!this.operatorToken) return;

    const script = document.createElement('script');
    script.type = 'module';
    script.id = 'operator-chat-panel-script';
    script.src = 'https://widget.smsbat.com/operator-chat-panel/widget-script.js';
    script.setAttribute('token', this.operatorToken);

    document.body.appendChild(script);
  }
}
```

## Token Management

### Server-Side Token Generation

**Never expose company credentials in client-side code.** Generate tokens on your server:

```javascript
// Node.js Express example
const express = require('express');
const app = express();

app.get('/api/chathub/token', async (req, res) => {
  try {
    // Authenticate your user first
    const userId = req.session.userId;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Get company token (stored securely on server)
    const companyToken = process.env.CHATHUB_COMPANY_TOKEN;

    // Get operator ID for this user
    const operatorId = await getOperatorIdForUser(userId);

    // Generate operator token
    const operatorToken = await generateOperatorToken(
      companyToken,
      operatorId
    );

    res.json({ token: operatorToken });
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

async function generateOperatorToken(companyToken, operatorId) {
  const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000); // 24 hours

  const response = await fetch(
    'https://api.chathub.smsbat.com/api/operator/get-token',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${companyToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: operatorId,
        expiresAt: expiresAt.toISOString()
      })
    }
  );

  return response.text();
}
```

### Token Refresh

Implement automatic token refresh:

```javascript
class WidgetTokenManager {
  constructor() {
    this.token = null;
    this.expiresAt = null;
    this.refreshInterval = null;
  }

  async initialize() {
    await this.refreshToken();

    // Refresh token 1 hour before expiration
    this.refreshInterval = setInterval(
      () => this.checkAndRefresh(),
      60 * 60 * 1000 // Check every hour
    );
  }

  async refreshToken() {
    const response = await fetch('/api/chathub/token');
    const data = await response.json();

    this.token = data.token;
    this.expiresAt = new Date(data.expiresAt);

    this.reloadWidget();
  }

  async checkAndRefresh() {
    const oneHour = 60 * 60 * 1000;
    const timeUntilExpiry = this.expiresAt - Date.now();

    if (timeUntilExpiry < oneHour) {
      await this.refreshToken();
    }
  }

  reloadWidget() {
    // Remove old widget
    const existing = document.getElementById('operator-chat-panel-script');
    if (existing) {
      existing.remove();
    }

    // Load new widget with fresh token
    const script = document.createElement('script');
    script.type = 'module';
    script.id = 'operator-chat-panel-script';
    script.src = 'https://widget.smsbat.com/operator-chat-panel/widget-script.js';
    script.setAttribute('token', this.token);

    document.body.appendChild(script);
  }

  destroy() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }
}

// Usage
const widgetManager = new WidgetTokenManager();
await widgetManager.initialize();
```

## Multiple Organizations

Load different widgets for different organizations:

```javascript
function loadWidgetForOrganization(organizationId) {
  return new Promise((resolve, reject) => {
    // Get operator for this organization
    fetch(`/api/chathub/token?org=${organizationId}`)
      .then(response => response.json())
      .then(data => {
        const script = document.createElement('script');
        script.type = 'module';
        script.id = `operator-chat-panel-script-${organizationId}`;
        script.src = 'https://widget.smsbat.com/operator-chat-panel/widget-script.js';
        script.setAttribute('token', data.token);

        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load widget'));

        document.body.appendChild(script);
      })
      .catch(reject);
  });
}

// Usage
await loadWidgetForOrganization('sales');
await loadWidgetForOrganization('support');
```

## Best Practices

### Security

- ✅ Generate tokens server-side
- ✅ Never expose company credentials in client code
- ✅ Use HTTPS for all API requests
- ✅ Implement token expiration
- ✅ Validate tokens before use
- ❌ Don't store tokens in localStorage without encryption
- ❌ Don't commit tokens to version control

### Performance

- ✅ Load widget asynchronously
- ✅ Use ES modules (modern browsers)
- ✅ Implement token caching
- ✅ Handle errors gracefully
- ❌ Don't block page load

### User Experience

- ✅ Show loading state while widget initializes
- ✅ Handle network errors
- ✅ Provide fallback contact method
- ✅ Test on different browsers and devices

### Error Handling

```javascript
async function loadWidgetSafely(operatorToken) {
  try {
    // Validate token first
    const isValid = await validateToken(operatorToken);

    if (!isValid) {
      console.error('Invalid operator token');
      showFallbackContact();
      return;
    }

    // Load widget
    await loadWidget(operatorToken);

  } catch (error) {
    console.error('Failed to load chat widget:', error);
    showFallbackContact();
  }
}

function showFallbackContact() {
  // Show alternative contact method
  const fallback = document.createElement('div');
  fallback.innerHTML = `
    <div class="chat-fallback">
      <p>Chat is temporarily unavailable.</p>
      <p>Contact us: <a href="mailto:support@example.com">support@example.com</a></p>
    </div>
  `;
  document.body.appendChild(fallback);
}
```

## Troubleshooting

### Widget Not Loading

1. Check operator token is valid
2. Verify token hasn't expired
3. Ensure script URL is correct
4. Check browser console for errors
5. Verify network connectivity

### Token Expired

```javascript
// Detect expired token and refresh
window.addEventListener('error', async (event) => {
  if (event.message.includes('token expired')) {
    console.log('Token expired, refreshing...');
    await refreshWidgetToken();
  }
});
```

### Multiple Widget Instances

Ensure only one widget loads at a time:

```javascript
function loadWidgetOnce(token) {
  // Remove any existing widgets
  const existingScripts = document.querySelectorAll(
    'script[id^="operator-chat-panel-script"]'
  );

  existingScripts.forEach(script => script.remove());

  // Load new widget
  loadWidget(token);
}
```

### Cross-Origin Issues

Ensure your domain is whitelisted. Contact support if you encounter CORS errors.

## Testing

### Local Development

```javascript
// Use test token for development
const isDevelopment = process.env.NODE_ENV === 'development';
const token = isDevelopment
  ? 'test-token-for-development'
  : await getProductionToken();

loadWidget(token);
```

### Integration Testing

```javascript
describe('ChatHub Widget', () => {
  it('should load widget with valid token', async () => {
    const token = await getTestToken();
    loadWidget(token);

    await waitFor(() => {
      const widget = document.getElementById('operator-chat-panel-script');
      expect(widget).toBeTruthy();
    });
  });

  it('should handle invalid token', async () => {
    const invalidToken = 'invalid-token';

    try {
      await loadWidget(invalidToken);
    } catch (error) {
      expect(error.message).toContain('Invalid token');
    }
  });
});
```

## Next Steps

- [Authentication](authentication.md) - Manage tokens
- [Operators](operators.md) - Set up operators
- [Organizations](organizations.md) - Configure organizations
