# Cascade API

The Cascade API enables sending messages across multiple platforms with a single request, automatically routing to Telegram Bot, Viber Bot, Viber Business Messages, RCS, and SMS.

## Base URL

```
https://api.counterbat.com
```

## Authentication

Cascade API uses header-based authentication with three possible authentication headers:

### Method 1: SMSBAT API Key

```bash
curl -X POST https://api.counterbat.com/api/CascadeMessage/send_message/async \
  -H "X-Authorization-Key: your-smsbat-api-key" \
  -H "Content-Type: application/json" \
  -d @request.json
```

### Method 2: Viber Bot Token

```bash
curl -X POST https://api.counterbat.com/api/CascadeMessage/send_message/async \
  -H "X-Viber-Auth-Token: your-viber-bot-token" \
  -H "Content-Type: application/json" \
  -d @request.json
```

### Method 3: Telegram Bot Key

```bash
curl -X POST https://api.counterbat.com/api/CascadeMessage/send_message/async \
  -H "X-Tg-Bot-Key: your-telegram-bot-key" \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/CascadeMessage/send_message/async` | General cascade message sending |
| POST | `/api/CascadeMessage/send_message/tg-viber/async` | Telegram-prioritized cascade |

## How It Works

With a single API request, Cascade automatically delivers your message across multiple channels:

```
Telegram Bot → Viber Bot → Viber Business → RCS → SMS
```

The message is delivered through the first available channel, with automatic fallback to the next channel if delivery fails.

## Key Features

### Multi-Channel Delivery

Send one message, reach users on any platform:

- Telegram Bot
- Viber Bot
- Viber Business Messages
- RCS (Rich Communication Services)
- SMS

### Variable Substitution

Use dynamic content with variable placeholders:

- `%name=id%` - Text variables
- `%url=id%` - URL variables
- `%short_url=id%` - Shortened URL variables

### Message Scheduling

Schedule messages for future delivery:

```json
{
  "scheduledTime": "2025-01-24T12:00:00Z"
}
```

### Time-to-Live (TTL)

Set expiration time for messages:

```json
{
  "ttl": 3600
}
```

## Message Types

Cascade API supports:

- **Transactional** - Order confirmations, notifications
- **Promo** - Marketing and promotional messages
- **Viber Surveys** - Interactive surveys
- **Flash Calls** - Phone verification

## Response Format

Successful responses return:

```json
[
  {
    "messageId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "trackinId": "tracking-string-id"
  }
]
```

- `messageId` - GUID for message identification
- `trackinId` - String for tracking delivery status

## Quick Start

1. [Send Messages](send.md) - Start sending cascade messages
2. [Message Variables](variables.md) - Use dynamic content
3. [Message Types](message-types.md) - Explore message types

## Request Example

```json
{
  "messages": [
    {
      "recipient": "+380XXXXXXXXX",
      "text": "Hello %name=1%, your order #%url=2% is ready!",
      "variables": [
        {
          "id": 1,
          "value": "John"
        },
        {
          "id": 2,
          "value": "12345"
        }
      ]
    }
  ]
}
```

## Error Handling

HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication failed
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## Benefits

### Single Integration

One API integration for all messaging channels - no need to integrate with each platform separately.

### Automatic Routing

Smart routing ensures message delivery through the best available channel for each recipient.

### Cost Optimization

Cascade tries cheaper channels first, automatically falling back to more expensive options only when needed.

### Higher Delivery Rates

Multiple fallback channels ensure your message reaches the recipient even if the primary channel fails.

## Next Steps

- [Send Cascade Messages](send.md) - Learn how to send messages
- [Message Variables](variables.md) - Work with dynamic content
- [Message Types](message-types.md) - Explore available message types
