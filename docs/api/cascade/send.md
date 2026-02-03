# Send Cascade Messages

Send messages across multiple channels with a single API request. Cascade automatically routes your message through Telegram Bot, Viber Bot, Viber Business Messages, RCS, and SMS.

## Endpoints

### Standard Cascade

```
POST /api/CascadeMessage/send_message/async
```

Routes messages through all available channels in sequence.

### Telegram-Viber Priority

```
POST /api/CascadeMessage/send_message/tg-viber/async
```

Prioritizes Telegram and Viber channels for faster delivery.

## Authentication

Cascade API supports three authentication headers. Include at least one:

| Header | Description |
|--------|-------------|
| `X-Authorization-Key` | SMSBAT API key (recommended) |
| `X-Viber-Auth-Token` | Viber bot credentials |
| `X-Tg-Bot-Key` | Telegram bot key |

## Request Structure

### Headers

```bash
Content-Type: application/json
X-Authorization-Key: your-smsbat-api-key
X-Viber-Auth-Token: your-viber-token
X-Tg-Bot-Key: your-telegram-key
```

### Request Body

Send an array of message objects:

```json
[
  {
    "id": "unique-tracking-id",
    "fromName": "YourBrand",
    "toPhone": "+380XXXXXXXXX",
    "messageType": "transaction",
    "text": "Your order #12345 has been confirmed",
    "ttl": 3600,
    "scheduledSent": "2025-01-25T10:00:00Z"
  }
]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Your tracking identifier |
| `fromName` | string | Yes | Sender display name |
| `toPhone` | string | Yes | Recipient phone number (E.164 format) |
| `messageType` | string | Yes | Message type: `transaction`, `promo`, `viber_survey`, `flashcall` |
| `text` | string | Yes* | Message content (* required for most types) |
| `ttl` | integer | No | Time-to-live in seconds |
| `scheduledSent` | string | No | ISO 8601 datetime for scheduled delivery |

## Message Types

### Transaction Messages

Critical notifications like order confirmations and account updates:

```json
{
  "id": "order-12345",
  "fromName": "YourStore",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "transaction",
  "text": "Your order #12345 has been confirmed and will arrive tomorrow.",
  "ttl": 86400
}
```

### Promo Messages

Marketing campaigns with rich media:

```json
{
  "id": "promo-summer-sale",
  "fromName": "YourBrand",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "promo",
  "text": "Summer Sale! Up to 50% off. Shop now: https://example.com/sale",
  "ttl": 259200
}
```

### Viber Survey

Interactive polls with 2-5 response options:

```json
{
  "id": "survey-satisfaction",
  "fromName": "YourBrand",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "viber_survey",
  "text": "How satisfied are you with our service?",
  "surveyOptions": [
    "Very Satisfied",
    "Satisfied",
    "Neutral",
    "Dissatisfied",
    "Very Dissatisfied"
  ],
  "ttl": 604800
}
```

Survey text maximum: 85 characters

### Flash Call

Phone verification via automated call:

```json
{
  "id": "verify-user-123",
  "fromName": "YourApp",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "flashcall",
  "ttl": 300
}
```

## Examples

### Basic Transaction

```bash
curl -X POST https://restapi.smsbat.com/api/CascadeMessage/send_message/async \
  -H "Content-Type: application/json" \
  -H "X-Authorization-Key: your-api-key" \
  -d '[
    {
      "id": "tx-001",
      "fromName": "YourBank",
      "toPhone": "+380XXXXXXXXX",
      "messageType": "transaction",
      "text": "Payment of $100 was successful. Transaction ID: ABC123"
    }
  ]'
```

### Scheduled Promo

```bash
curl -X POST https://restapi.smsbat.com/api/CascadeMessage/send_message/async \
  -H "Content-Type: application/json" \
  -H "X-Authorization-Key: your-api-key" \
  -d '[
    {
      "id": "promo-001",
      "fromName": "YourStore",
      "toPhone": "+380XXXXXXXXX",
      "messageType": "promo",
      "text": "Flash Sale starts in 1 hour! Visit: https://example.com",
      "scheduledSent": "2025-01-25T09:00:00Z",
      "ttl": 3600
    }
  ]'
```

### Bulk Messages

```bash
curl -X POST https://restapi.smsbat.com/api/CascadeMessage/send_message/async \
  -H "Content-Type: application/json" \
  -H "X-Authorization-Key: your-api-key" \
  -d '[
    {
      "id": "bulk-001",
      "fromName": "YourBrand",
      "toPhone": "+380111111111",
      "messageType": "transaction",
      "text": "Message 1"
    },
    {
      "id": "bulk-002",
      "fromName": "YourBrand",
      "toPhone": "+380222222222",
      "messageType": "transaction",
      "text": "Message 2"
    },
    {
      "id": "bulk-003",
      "fromName": "YourBrand",
      "toPhone": "+380333333333",
      "messageType": "transaction",
      "text": "Message 3"
    }
  ]'
```

## Response

### Success Response

```json
[
  {
    "messageId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "trackinId": "tx-001"
  },
  {
    "messageId": "8b2f1e9a-4c6d-4e2a-9f8b-1a3d5c7e9f0b",
    "trackinId": "tx-002"
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `messageId` | string (UUID) | System message identifier |
| `trackinId` | string | Your tracking identifier (from request) |

Use `messageId` for status tracking and `trackinId` for correlating with your system.

## Implementation Examples

### Python

```python
import requests
from datetime import datetime, timedelta

class CascadeMessenger:
    def __init__(self, api_key):
        self.base_url = 'https://restapi.smsbat.com'
        self.headers = {
            'Content-Type': 'application/json',
            'X-Authorization-Key': api_key
        }

    def send_message(self, tracking_id, from_name, to_phone,
                     message_type, text, ttl=None, scheduled=None):
        """Send single cascade message"""
        message = {
            'id': tracking_id,
            'fromName': from_name,
            'toPhone': to_phone,
            'messageType': message_type,
            'text': text
        }

        if ttl:
            message['ttl'] = ttl

        if scheduled:
            message['scheduledSent'] = scheduled.isoformat()

        response = requests.post(
            f'{self.base_url}/api/CascadeMessage/send_message/async',
            headers=self.headers,
            json=[message]
        )

        response.raise_for_status()
        return response.json()[0]

    def send_bulk(self, messages):
        """Send multiple messages"""
        response = requests.post(
            f'{self.base_url}/api/CascadeMessage/send_message/async',
            headers=self.headers,
            json=messages
        )

        response.raise_for_status()
        return response.json()

# Usage
messenger = CascadeMessenger('your-api-key')

# Send single message
result = messenger.send_message(
    tracking_id='order-12345',
    from_name='YourStore',
    to_phone='+380XXXXXXXXX',
    message_type='transaction',
    text='Your order has been confirmed',
    ttl=86400
)

print(f"Message ID: {result['messageId']}")

# Send scheduled message
scheduled_time = datetime.now() + timedelta(hours=2)
result = messenger.send_message(
    tracking_id='promo-001',
    from_name='YourBrand',
    to_phone='+380XXXXXXXXX',
    message_type='promo',
    text='Sale starts now!',
    scheduled=scheduled_time
)

# Bulk send
messages = [
    {
        'id': f'bulk-{i}',
        'fromName': 'YourBrand',
        'toPhone': f'+38011111111{i}',
        'messageType': 'transaction',
        'text': f'Message {i}'
    }
    for i in range(100)
]

results = messenger.send_bulk(messages)
print(f"Sent {len(results)} messages")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

class CascadeMessenger {
  constructor(apiKey) {
    this.baseUrl = 'https://restapi.smsbat.com';
    this.headers = {
      'Content-Type': 'application/json',
      'X-Authorization-Key': apiKey
    };
  }

  async sendMessage({ id, fromName, toPhone, messageType, text, ttl, scheduledSent }) {
    const message = {
      id,
      fromName,
      toPhone,
      messageType,
      text
    };

    if (ttl) message.ttl = ttl;
    if (scheduledSent) message.scheduledSent = scheduledSent;

    const response = await axios.post(
      `${this.baseUrl}/api/CascadeMessage/send_message/async`,
      [message],
      { headers: this.headers }
    );

    return response.data[0];
  }

  async sendBulk(messages) {
    const response = await axios.post(
      `${this.baseUrl}/api/CascadeMessage/send_message/async`,
      messages,
      { headers: this.headers }
    );

    return response.data;
  }

  async sendTelegramViber({ id, fromName, toPhone, messageType, text }) {
    const response = await axios.post(
      `${this.baseUrl}/api/CascadeMessage/send_message/tg-viber/async`,
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
const messenger = new CascadeMessenger('your-api-key');

// Send single message
const result = await messenger.sendMessage({
  id: 'order-12345',
  fromName: 'YourStore',
  toPhone: '+380XXXXXXXXX',
  messageType: 'transaction',
  text: 'Your order has been confirmed',
  ttl: 86400
});

console.log('Message ID:', result.messageId);

// Send scheduled message
const scheduledTime = new Date(Date.now() + 2 * 60 * 60 * 1000);
await messenger.sendMessage({
  id: 'promo-001',
  fromName: 'YourBrand',
  toPhone: '+380XXXXXXXXX',
  messageType: 'promo',
  text: 'Sale starts now!',
  scheduledSent: scheduledTime.toISOString()
});

// Bulk send
const messages = Array.from({ length: 100 }, (_, i) => ({
  id: `bulk-${i}`,
  fromName: 'YourBrand',
  toPhone: `+38011111111${i}`,
  messageType: 'transaction',
  text: `Message ${i}`
}));

const results = await messenger.sendBulk(messages);
console.log(`Sent ${results.length} messages`);
```

### PHP

```php
<?php

class CascadeMessenger {
    private $baseUrl = 'https://restapi.smsbat.com';
    private $apiKey;

    public function __construct($apiKey) {
        $this->apiKey = $apiKey;
    }

    public function sendMessage($id, $fromName, $toPhone, $messageType,
                                $text, $ttl = null, $scheduledSent = null) {
        $message = [
            'id' => $id,
            'fromName' => $fromName,
            'toPhone' => $toPhone,
            'messageType' => $messageType,
            'text' => $text
        ];

        if ($ttl !== null) {
            $message['ttl'] = $ttl;
        }

        if ($scheduledSent !== null) {
            $message['scheduledSent'] = $scheduledSent;
        }

        $ch = curl_init($this->baseUrl . '/api/CascadeMessage/send_message/async');

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

    public function sendBulk($messages) {
        $ch = curl_init($this->baseUrl . '/api/CascadeMessage/send_message/async');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'X-Authorization-Key: ' . $this->apiKey
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($messages));

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }
}

// Usage
$messenger = new CascadeMessenger('your-api-key');

// Send single message
$result = $messenger->sendMessage(
    'order-12345',
    'YourStore',
    '+380XXXXXXXXX',
    'transaction',
    'Your order has been confirmed',
    86400
);

echo "Message ID: " . $result['messageId'] . "\n";

// Bulk send
$messages = [];
for ($i = 0; $i < 100; $i++) {
    $messages[] = [
        'id' => "bulk-$i",
        'fromName' => 'YourBrand',
        'toPhone' => "+38011111111$i",
        'messageType' => 'transaction',
        'text' => "Message $i"
    ];
}

$results = $messenger->sendBulk($messages);
echo "Sent " . count($results) . " messages\n";
```

## Best Practices

### Phone Numbers

Always use E.164 format:
- ✅ `+380XXXXXXXXX`
- ❌ `380XXXXXXXXX`
- ❌ `0XXXXXXXXX`

### Tracking IDs

- Use unique IDs for each message
- Include context in ID (e.g., `order-12345`, `promo-summer-2025`)
- Keep IDs under 255 characters
- Avoid special characters

### TTL (Time-to-Live)

Recommended TTL values:

- **OTP/Verification**: 300-600 seconds (5-10 minutes)
- **Transactional**: 3600-86400 seconds (1-24 hours)
- **Promotional**: 86400-259200 seconds (1-3 days)
- **Surveys**: 604800 seconds (7 days)

### Scheduled Messages

- Use UTC timezone for `scheduledSent`
- Don't schedule more than 30 days in advance
- Account for timezone differences
- Test with near-future schedules first

### Bulk Sending

- Send in batches of 100-1000 messages
- Implement rate limiting
- Handle errors gracefully
- Retry failed messages

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request - invalid parameters |
| 401 | Unauthorized - invalid API key |
| 429 | Too many requests |
| 500 | Server error |

### Error Response

```json
{
  "error": {
    "code": "INVALID_PHONE",
    "message": "Invalid phone number format",
    "field": "toPhone"
  }
}
```

### Retry Logic

```javascript
async function sendWithRetry(message, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await messenger.sendMessage(message);
    } catch (error) {
      if (error.response?.status === 400) {
        // Don't retry validation errors
        throw error;
      }

      if (i === maxRetries - 1) throw error;

      // Exponential backoff
      await new Promise(resolve =>
        setTimeout(resolve, Math.pow(2, i) * 1000)
      );
    }
  }
}
```

## Next Steps

- [Message Variables](variables.md) - Use dynamic content
- [Message Types](message-types.md) - Explore message types
- [Delivery Status](../../using-smsbat/delivery-status.md) - Track delivery
