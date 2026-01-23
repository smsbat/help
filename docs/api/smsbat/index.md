# SMSBAT API

SMSBAT is a RESTful API platform for sending various types of messages including Viber carousel, Viber opinion dialog, Viber promo (pictures, video), Viber business chat, OTP notifications (Viber OTP, Flash Call) and their fallback variants.

## Base URL

Requests to SMSBAT API are transmitted to an endpoint with localization. Request the address from your Manager beforehand.

Example: `https://restapi.smsbat.com` (actual URL may vary based on your region)

## Authentication

SMSBAT API supports three authentication methods:

### Method 1: HTTP Basic Auth

Use your username and password credentials:

```bash
curl -X POST https://restapi.smsbat.com/bat/messagelist \
  -u "username:password" \
  -H "Content-Type: application/json" \
  -d @request.json
```

### Method 2: API Key Header

Use the `X-Authorization-Key` header:

```bash
curl -X POST https://restapi.smsbat.com/bat/messagelist \
  -H "X-Authorization-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d @request.json
```

### Method 3: API Key as Password

Use `@` as username and your API key as password:

```bash
curl -X POST https://restapi.smsbat.com/bat/messagelist \
  -u "@:your-api-key" \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bat/messagelist` | Send messages |
| GET | `/bat/message/{messageId}` | Check message status |

## Message Types

SMSBAT API supports the following message types:

- **SMS** - Standard text messages
- **Viber Promo** - Promotional messages with rich media
- **Viber Transactional** - Transaction notifications
- **Viber Carousel** - Interactive carousel messages
- **Viber Survey** - Opinion dialog messages
- **Viber OTP** - One-time password notifications
- **RCS** - Rich Communication Services messages
- **Flash Call** - Silent call verification

## Key Features

### Fallback Messaging

When primary delivery fails, SMSBAT automatically falls back to alternative channels:

```
Viber → SMS → Email
```

### Rich Media Support

Send messages with:

- Images (JPG, PNG)
- Videos (MP4)
- PDFs
- Buttons and action links

### Message Status Tracking

Track delivery status in real-time:

- Sent
- Delivered
- Read
- Failed
- Expired

### Callbacks

Receive incoming Viber message callbacks for two-way communication.

## Quick Start

1. [Send a Message](send-message.md) - Learn how to send your first message
2. [Check Status](status.md) - Track message delivery status
3. [Message Types](viber.md) - Explore different message types

## Request Format

All requests use JSON format with the following structure:

```json
{
  "messages": [
    {
      "recipient": "+380XXXXXXXXX",
      "type": "viber",
      "text": "Your message here",
      // ... additional parameters
    }
  ]
}
```

## Response Format

Successful responses return:

```json
{
  "messages": [
    {
      "messageId": "unique-message-id",
      "recipient": "+380XXXXXXXXX",
      "status": "sent"
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

## Next Steps

- [Send Message](send-message.md) - Start sending messages
- [Viber Messages](viber.md) - Learn about Viber message types
- [SMS Messages](sms.md) - Send SMS messages
- [RCS Messages](rcs.md) - Rich Communication Services
- [Flash Call](flashcall.md) - Phone verification
- [Check Status](status.md) - Track delivery status
