# Send Message

Send messages through SMSBAT API using the `/bat/messagelist` endpoint.

## Endpoint

```
POST /bat/messagelist
```

## Request Structure

The request body is a JSON array of message objects:

```json
{
  "messages": [
    {
      "from": "YourSender",
      "to": "+380XXXXXXXXX",
      "type": "sms",
      "text": "Your message text",
      "customerMessageId": "your-internal-id",
      "ttl": 3600
    }
  ]
}
```

## Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `from` | string | Alphanumeric sender ID |
| `to` | string | Recipient phone number in E.164 format (e.g., +380XXXXXXXXX) |
| `type` | string | Message type: `sms`, `viber_promo`, `viber_trans`, `viber_carousel`, `viber_survey`, `viber_otp`, `rcs`, `flashcall` |
| `text` | string | Message content (required for most types, optional for some) |

### Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `customerMessageId` | string | Your internal identifier for tracking |
| `ttl` | integer | Time-to-live in seconds |
| `messageData` | object | Type-specific configuration (varies by message type) |

## Authentication

Choose one of three authentication methods:

=== "API Key Header"

    ```bash
    curl -X POST https://api.smsbat.com/bat/messagelist \
      -H "X-Authorization-Key: your-api-key" \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [{
          "from": "YourSender",
          "to": "+380XXXXXXXXX",
          "type": "sms",
          "text": "Hello from SMSBAT!"
        }]
      }'
    ```

=== "HTTP Basic Auth"

    ```bash
    curl -X POST https://api.smsbat.com/bat/messagelist \
      -u "username:password" \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [{
          "from": "YourSender",
          "to": "+380XXXXXXXXX",
          "type": "sms",
          "text": "Hello from SMSBAT!"
        }]
      }'
    ```

=== "API Key as Password"

    ```bash
    curl -X POST https://api.smsbat.com/bat/messagelist \
      -u "@:your-api-key" \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [{
          "from": "YourSender",
          "to": "+380XXXXXXXXX",
          "type": "sms",
          "text": "Hello from SMSBAT!"
        }]
      }'
    ```

## Response

### Success Response

```json
{
  "messagelistId": 123456,
  "messages": [
    {
      "messageId": "abc123def456",
      "status": "accepted",
      "parts": 1,
      "customerMessageId": "your-internal-id",
      "to": "+380XXXXXXXXX"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `messagelistId` | integer | Unique identifier for the message list |
| `messageId` | string | Unique identifier for each message |
| `status` | string | Message status: `accepted`, `rejected`, `failed` |
| `parts` | integer | Number of message parts (for SMS) |
| `customerMessageId` | string | Your internal identifier (if provided) |
| `to` | string | Recipient phone number |

## Message Types

### SMS

Simple text messages:

```json
{
  "from": "YourSender",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Your SMS message text"
}
```

### Viber Promo

Promotional messages with rich media:

```json
{
  "from": "YourSender",
  "to": "+380XXXXXXXXX",
  "type": "viber_promo",
  "text": "Check out our new product!",
  "messageData": {
    "image": "https://example.com/image.jpg",
    "button": {
      "text": "View Product",
      "url": "https://example.com/product"
    }
  }
}
```

### Viber Transactional

Transaction notifications:

```json
{
  "from": "YourSender",
  "to": "+380XXXXXXXXX",
  "type": "viber_trans",
  "text": "Your order #12345 has been confirmed"
}
```

### Viber OTP

One-time password notifications:

```json
{
  "from": "YourSender",
  "to": "+380XXXXXXXXX",
  "type": "viber_otp",
  "messageData": {
    "code": "123456",
    "validity": 300
  }
}
```

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Request successful |
| 400 | Bad request - invalid parameters |
| 401 | Unauthorized - authentication failed |
| 429 | Too many requests - rate limit exceeded |
| 500 | Internal server error |

### Error Response

```json
{
  "error": {
    "code": "INVALID_RECIPIENT",
    "message": "Invalid phone number format"
  }
}
```

## Best Practices

### Phone Number Format

Always use E.164 format for phone numbers:

- ✅ Correct: `+380XXXXXXXXX`
- ❌ Incorrect: `380XXXXXXXXX`, `0XXXXXXXXX`

### Message Text

- Keep SMS under 160 characters to avoid multiple parts
- Use UTF-8 encoding for international characters
- Test special characters before bulk sending

### TTL (Time-to-Live)

- Set appropriate TTL for time-sensitive messages
- OTP messages: 300-600 seconds (5-10 minutes)
- Promotional messages: 3600-86400 seconds (1-24 hours)

### Customer Message ID

- Use unique identifiers for each message
- Helps with tracking and debugging
- Useful for correlating with your system's records

## Rate Limits

Contact your account manager for information about:

- Messages per second
- Messages per day
- Concurrent connections

## Next Steps

- [Viber Messages](viber.md) - Explore Viber message types
- [SMS Messages](sms.md) - Learn more about SMS
- [Check Status](status.md) - Track message delivery
