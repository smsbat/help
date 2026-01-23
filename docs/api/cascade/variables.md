# Message Variables

Use variables to personalize cascade messages with dynamic content like names, URLs, and custom values.

## Overview

Variables enable:

- **Personalization**: Insert recipient names, account numbers
- **Dynamic URLs**: Include unique links for each recipient
- **URL Shortening**: Automatically shorten long URLs
- **Template Reusability**: One template, many personalized messages

## Variable Types

| Type | Syntax | Purpose | Example |
|------|--------|---------|---------|
| `name` | `%name=id%` | Text variables | Names, codes, amounts |
| `url` | `%url=id%` | Full URLs | Links, tracking URLs |
| `short_url` | `%short_url=id%` | Shortened URLs | Compact links |

## Variable Syntax

Variables use the format: `%type=id%`

- **type**: Variable type (`name`, `url`, `short_url`)
- **id**: Unique identifier (integer)

### Examples

```
Hello %name=1%, your code is %name=2%
Visit our website: %url=1%
Quick link: %short_url=1%
```

## Using Variables

### Step 1: Upload Variable Values

Before sending messages, upload variable values to the API:

**Endpoint:**
```
POST https://api.counterbat.com/api/items
```

**Request:**
```json
{
  "variables": [
    {
      "id": 1,
      "type": "name",
      "value": "John"
    },
    {
      "id": 2,
      "type": "name",
      "value": "12345"
    },
    {
      "id": 3,
      "type": "url",
      "value": "https://example.com/products"
    },
    {
      "id": 4,
      "type": "short_url",
      "value": "https://example.com/very-long-url-that-needs-shortening"
    }
  ]
}
```

### Step 2: Send Message with Variables

Use uploaded variable IDs in your message:

```json
{
  "id": "msg-001",
  "fromName": "YourStore",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "transaction",
  "text": "Hello %name=1%! Your verification code is %name=2%. Visit: %short_url=4%"
}
```

**Result:**
```
Hello John! Your verification code is 12345. Visit: https://sho.rt/abc123
```

## Complete Example

### Upload Variables

```bash
curl -X POST https://api.counterbat.com/api/items \
  -H "Content-Type: application/json" \
  -H "X-Authorization-Key: your-api-key" \
  -d '{
    "variables": [
      {
        "id": 1,
        "type": "name",
        "value": "Sarah"
      },
      {
        "id": 2,
        "type": "name",
        "value": "ORD-789"
      },
      {
        "id": 3,
        "type": "url",
        "value": "https://example.com/track/ORD-789"
      }
    ]
  }'
```

### Send Message

```bash
curl -X POST https://api.counterbat.com/api/CascadeMessage/send_message/async \
  -H "Content-Type: application/json" \
  -H "X-Authorization-Key: your-api-key" \
  -d '[
    {
      "id": "order-notification",
      "fromName": "YourStore",
      "toPhone": "+380XXXXXXXXX",
      "messageType": "transaction",
      "text": "Hi %name=1%! Order %name=2% shipped. Track: %url=3%"
    }
  ]'
```

**Delivered Message:**
```
Hi Sarah! Order ORD-789 shipped. Track: https://example.com/track/ORD-789
```

## Use Cases

### Order Confirmation

```json
// Variables
{
  "variables": [
    {"id": 1, "type": "name", "value": "John"},
    {"id": 2, "type": "name", "value": "12345"},
    {"id": 3, "type": "name", "value": "$99.99"},
    {"id": 4, "type": "url", "value": "https://store.com/order/12345"}
  ]
}

// Message
{
  "text": "Hi %name=1%! Order #%name=2% for %name=3% confirmed. Details: %url=4%"
}

// Result
"Hi John! Order #12345 for $99.99 confirmed. Details: https://store.com/order/12345"
```

### Password Reset

```json
// Variables
{
  "variables": [
    {"id": 1, "type": "name", "value": "Mike"},
    {"id": 2, "type": "short_url", "value": "https://app.example.com/reset?token=abc123def456"}
  ]
}

// Message
{
  "text": "Hi %name=1%, reset your password: %short_url=2% (valid 30 min)"
}

// Result
"Hi Mike, reset your password: https://sho.rt/xyz789 (valid 30 min)"
```

### Promotional Campaign

```json
// Variables
{
  "variables": [
    {"id": 1, "type": "name", "value": "VIP20"},
    {"id": 2, "type": "short_url", "value": "https://store.com/sale?utm_source=sms&utm_campaign=summer"}
  ]
}

// Message
{
  "text": "Summer Sale! Use code %name=1% for 20% off: %short_url=2%"
}

// Result
"Summer Sale! Use code VIP20 for 20% off: https://sho.rt/abc"
```

### Account Verification

```json
// Variables
{
  "variables": [
    {"id": 1, "type": "name", "value": "789456"},
    {"id": 2, "type": "name", "value": "10"}
  ]
}

// Message
{
  "text": "Your verification code: %name=1%. Valid for %name=2% minutes."
}

// Result
"Your verification code: 789456. Valid for 10 minutes."
```

## Implementation Examples

### Python

```python
import requests

class CascadeVariables:
    def __init__(self, api_key):
        self.base_url = 'https://api.counterbat.com'
        self.headers = {
            'Content-Type': 'application/json',
            'X-Authorization-Key': api_key
        }

    def upload_variables(self, variables):
        """Upload variable values"""
        response = requests.post(
            f'{self.base_url}/api/items',
            headers=self.headers,
            json={'variables': variables}
        )
        response.raise_for_status()
        return response.json()

    def send_with_variables(self, tracking_id, from_name, to_phone,
                           message_type, text, variables):
        """Upload variables and send message"""
        # Upload variables first
        self.upload_variables(variables)

        # Send message
        message = {
            'id': tracking_id,
            'fromName': from_name,
            'toPhone': to_phone,
            'messageType': message_type,
            'text': text
        }

        response = requests.post(
            f'{self.base_url}/api/CascadeMessage/send_message/async',
            headers=self.headers,
            json=[message]
        )

        response.raise_for_status()
        return response.json()[0]

# Usage
cascade = CascadeVariables('your-api-key')

# Define variables
variables = [
    {'id': 1, 'type': 'name', 'value': 'John'},
    {'id': 2, 'type': 'name', 'value': 'ORD-12345'},
    {'id': 3, 'type': 'url', 'value': 'https://example.com/track/ORD-12345'}
]

# Send message with variables
result = cascade.send_with_variables(
    tracking_id='order-notification',
    from_name='YourStore',
    to_phone='+380XXXXXXXXX',
    message_type='transaction',
    text='Hi %name=1%! Order %name=2% shipped. Track: %url=3%',
    variables=variables
)

print(f"Message sent: {result['messageId']}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

class CascadeVariables {
  constructor(apiKey) {
    this.baseUrl = 'https://api.counterbat.com';
    this.headers = {
      'Content-Type': 'application/json',
      'X-Authorization-Key': apiKey
    };
  }

  async uploadVariables(variables) {
    const response = await axios.post(
      `${this.baseUrl}/api/items`,
      { variables },
      { headers: this.headers }
    );

    return response.data;
  }

  async sendWithVariables({ id, fromName, toPhone, messageType, text, variables }) {
    // Upload variables first
    await this.uploadVariables(variables);

    // Send message
    const response = await axios.post(
      `${this.baseUrl}/api/CascadeMessage/send_message/async`,
      [{
        id,
        fromName,
        toPhone,
        messageType,
        text
      }],
      { headers: this.headers }
    );

    return response.data[0];
  }
}

// Usage
const cascade = new CascadeVariables('your-api-key');

const result = await cascade.sendWithVariables({
  id: 'order-notification',
  fromName: 'YourStore',
  toPhone: '+380XXXXXXXXX',
  messageType: 'transaction',
  text: 'Hi %name=1%! Order %name=2% shipped. Track: %url=3%',
  variables: [
    { id: 1, type: 'name', value: 'John' },
    { id: 2, type: 'name', value: 'ORD-12345' },
    { id: 3, type: 'url', value: 'https://example.com/track/ORD-12345' }
  ]
});

console.log('Message sent:', result.messageId);
```

### PHP

```php
<?php

class CascadeVariables {
    private $baseUrl = 'https://api.counterbat.com';
    private $apiKey;

    public function __construct($apiKey) {
        $this->apiKey = $apiKey;
    }

    public function uploadVariables($variables) {
        $ch = curl_init($this->baseUrl . '/api/items');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'X-Authorization-Key: ' . $this->apiKey
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS,
                   json_encode(['variables' => $variables]));

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }

    public function sendWithVariables($id, $fromName, $toPhone,
                                     $messageType, $text, $variables) {
        // Upload variables
        $this->uploadVariables($variables);

        // Send message
        $message = [
            'id' => $id,
            'fromName' => $fromName,
            'toPhone' => $toPhone,
            'messageType' => $messageType,
            'text' => $text
        ];

        $ch = curl_init(
            $this->baseUrl . '/api/CascadeMessage/send_message/async'
        );

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'X-Authorization-Key: ' . $this->apiKey
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([$message]));

        $response = curl_exec($ch);
        curl_close($ch);

        $result = json_decode($response, true);
        return $result[0];
    }
}

// Usage
$cascade = new CascadeVariables('your-api-key');

$variables = [
    ['id' => 1, 'type' => 'name', 'value' => 'John'],
    ['id' => 2, 'type' => 'name', 'value' => 'ORD-12345'],
    ['id' => 3, 'type' => 'url', 'value' => 'https://example.com/track/ORD-12345']
];

$result = $cascade->sendWithVariables(
    'order-notification',
    'YourStore',
    '+380XXXXXXXXX',
    'transaction',
    'Hi %name=1%! Order %name=2% shipped. Track: %url=3%',
    $variables
);

echo "Message sent: " . $result['messageId'] . "\n";
```

## Best Practices

### Variable IDs

- ✅ Use sequential IDs (1, 2, 3, ...)
- ✅ Reuse IDs for bulk messages with same variables
- ✅ Document variable ID mapping
- ❌ Don't use random IDs
- ❌ Don't skip ID numbers

### Variable Values

- ✅ Validate values before uploading
- ✅ Handle special characters properly
- ✅ Test with edge cases
- ❌ Don't include HTML in name variables
- ❌ Don't exceed reasonable length limits

### URL Variables

- ✅ Use `short_url` for long URLs
- ✅ Include tracking parameters
- ✅ Use HTTPS
- ❌ Don't use suspicious-looking URLs
- ❌ Don't include sensitive data in URLs

### Performance

- Upload variables once, send multiple messages
- Batch variable uploads
- Cache commonly used variables
- Clean up old variables periodically

## Advanced Patterns

### Bulk Personalization

```javascript
async function sendBulkPersonalized(recipients) {
  const messages = [];
  const variables = [];
  let varId = 1;

  recipients.forEach((recipient, index) => {
    // Variables for this recipient
    const nameVarId = varId++;
    const orderVarId = varId++;
    const urlVarId = varId++;

    variables.push(
      { id: nameVarId, type: 'name', value: recipient.name },
      { id: orderVarId, type: 'name', value: recipient.orderId },
      { id: urlVarId, type: 'url', value: recipient.trackingUrl }
    );

    messages.push({
      id: `order-${recipient.orderId}`,
      fromName: 'YourStore',
      toPhone: recipient.phone,
      messageType: 'transaction',
      text: `Hi %name=${nameVarId}%! Order %name=${orderVarId}% shipped. Track: %url=${urlVarId}%`
    });
  });

  // Upload all variables
  await uploadVariables(variables);

  // Send all messages
  return await sendBulk(messages);
}
```

### Template System

```javascript
class MessageTemplate {
  constructor(template) {
    this.template = template;
    this.varIdCounter = 1;
  }

  create(data) {
    const variables = [];
    let text = this.template;

    // Replace placeholders with variable syntax
    Object.entries(data).forEach(([key, value]) => {
      const varId = this.varIdCounter++;
      variables.push({
        id: varId,
        type: this.getVarType(value),
        value: value
      });

      text = text.replace(`{{${key}}}`, `%${this.getVarType(value)}=${varId}%`);
    });

    return { text, variables };
  }

  getVarType(value) {
    if (value.startsWith('http')) return 'url';
    return 'name';
  }
}

// Usage
const template = new MessageTemplate(
  'Hi {{name}}! Order {{orderId}} shipped. Track: {{trackUrl}}'
);

const { text, variables } = template.create({
  name: 'John',
  orderId: 'ORD-123',
  trackUrl: 'https://example.com/track/ORD-123'
});

await sendWithVariables({ text, variables });
```

## Troubleshooting

### Variables Not Replaced

- Verify variables were uploaded before sending
- Check variable ID matches in text and upload
- Ensure correct syntax: `%type=id%`
- Validate variable type matches value

### URL Shortening Failed

- Check URL is valid and accessible
- Verify URL starts with http:// or https://
- Ensure URL isn't already shortened
- Try using `url` instead of `short_url`

### Variable Limit Exceeded

- Contact support for variable limits
- Reuse variable IDs when possible
- Clean up old variables
- Optimize variable usage

## Next Steps

- [Send Messages](send.md) - Send cascade messages
- [Message Types](message-types.md) - Explore message types
- [SMSBAT API](../smsbat/index.md) - Learn about SMSBAT API
