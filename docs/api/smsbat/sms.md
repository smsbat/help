# SMS Messages

Send standard text messages using SMSBAT API. SMS is the most universal messaging channel with the highest delivery rates across all mobile devices.

## Overview

SMS (Short Message Service) is ideal for:

- Time-critical notifications
- Fallback for Viber/RCS messages
- Reaching users without smartphones
- Universal compatibility across all mobile networks
- High delivery rates (95%+)

## Basic SMS Message

### Request

```json
{
  "from": "YourSender",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Your SMS message text"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | string | Yes | Alphanumeric sender ID (up to 11 characters) |
| `to` | string | Yes | Recipient phone number in E.164 format |
| `type` | string | Yes | Set to `"sms"` |
| `text` | string | Yes | Message content |
| `customerMessageId` | string | No | Your internal tracking ID |
| `ttl` | integer | No | Time-to-live in seconds |

## Examples

### Simple SMS

```bash
curl -X POST https://api.smsbat.com/bat/messagelist \
  -H "X-Authorization-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "from": "YourBrand",
      "to": "+380XXXXXXXXX",
      "type": "sms",
      "text": "Hello! This is a test SMS message."
    }]
  }'
```

### SMS with Customer ID

```json
{
  "messages": [{
    "from": "YourStore",
    "to": "+380XXXXXXXXX",
    "type": "sms",
    "text": "Your order #12345 has been shipped.",
    "customerMessageId": "order-12345-notification"
  }]
}
```

### SMS with TTL

```json
{
  "messages": [{
    "from": "YourApp",
    "to": "+380XXXXXXXXX",
    "type": "sms",
    "text": "Your verification code is: 123456",
    "ttl": 300
  }]
}
```

## Character Encoding

### GSM 7-bit Encoding

Standard GSM alphabet (160 characters per SMS):

```
A-Z a-z 0-9
@ £ $ ¥ è é ù ì ò Ç Ø ø Å å
Δ _ Φ Γ Λ Ω Π Ψ Σ Θ Ξ
! " # % & ' ( ) * + , - . / : ; < = > ?
```

### Extended GSM Characters

These characters count as 2 characters:

```
| ^ € { } [ ] ~ \
```

### Unicode (UCS-2) Encoding

Messages with special characters use Unicode encoding (70 characters per SMS):

- Emoji: 😀 🎉 ❤️
- Cyrillic: А Б В Г Д Е Ж
- Special symbols: ✓ ✗ ★ ♥

## Message Length

### Single SMS

- **GSM 7-bit**: 160 characters
- **Unicode**: 70 characters

### Multi-part SMS

When your message exceeds the limit, it's split into multiple parts:

- **GSM 7-bit**: 153 characters per part
- **Unicode**: 67 characters per part

#### Example

```json
{
  "messages": [{
    "from": "YourBrand",
    "to": "+380XXXXXXXXX",
    "type": "sms",
    "text": "This is a very long message that will be split into multiple parts. Each part will be delivered separately but will appear as a single message on the recipient's phone. The system automatically handles the splitting and reassembly."
  }]
}
```

This message (201 characters) will be split into 2 parts.

## Response

### Success Response

```json
{
  "messagelistId": 123456,
  "messages": [
    {
      "messageId": "abc123def456",
      "status": "accepted",
      "parts": 2,
      "customerMessageId": "order-12345-notification",
      "to": "+380XXXXXXXXX"
    }
  ]
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `messageId` | Unique identifier for tracking |
| `status` | Message status (`accepted`, `rejected`) |
| `parts` | Number of SMS parts |
| `to` | Recipient phone number |

## Sender ID

### Alphanumeric Sender

Use your brand name as sender (up to 11 characters):

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Hello from YourBrand!"
}
```

Restrictions:

- Maximum 11 characters
- Letters and numbers only
- No spaces or special characters
- Recipient cannot reply to alphanumeric senders

### Numeric Sender

Use a phone number as sender (for two-way SMS):

```json
{
  "from": "+380123456789",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Hello! You can reply to this message."
}
```

## Use Cases

### OTP Verification

```json
{
  "from": "YourApp",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Your verification code is: 123456. Valid for 5 minutes.",
  "ttl": 300
}
```

### Order Notifications

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Your order #12345 has been delivered. Thank you for shopping with us!"
}
```

### Appointment Reminders

```json
{
  "from": "YourClinic",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Reminder: Your appointment is scheduled for tomorrow at 2:00 PM."
}
```

### Payment Confirmations

```json
{
  "from": "YourBank",
  "to": "+380XXXXXXXXX",
  "type": "sms",
  "text": "Payment of 100 USD to Merchant ABC was successful. Transaction ID: 789xyz"
}
```

## Best Practices

### Message Content

- ✅ Keep messages concise and clear
- ✅ Include sender identification
- ✅ Add call-to-action if needed
- ✅ Use proper grammar and spelling
- ❌ Avoid excessive punctuation!!!
- ❌ Don't use all CAPS
- ❌ Avoid URL shorteners that look suspicious

### Character Usage

- Check character count before sending
- Be aware of extended GSM characters (count as 2)
- Test with special characters before bulk sending
- Consider using GSM encoding for longer messages

### Phone Numbers

- Always use E.164 format: `+380XXXXXXXXX`
- Validate phone numbers before sending
- Remove invalid numbers from your list
- Keep your contact list updated

### Timing

- Respect local time zones
- Avoid sending at night (10 PM - 8 AM)
- Consider business hours for commercial messages
- Set appropriate TTL for time-sensitive messages

### Compliance

- Obtain consent before sending marketing messages
- Include opt-out instructions for promotional SMS
- Follow local regulations (GDPR, etc.)
- Respect "Do Not Disturb" lists

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_RECIPIENT` | Wrong phone format | Use E.164 format |
| `INVALID_SENDER` | Invalid sender ID | Check sender ID rules |
| `MESSAGE_TOO_LONG` | Exceeds max length | Split or shorten message |
| `INVALID_ENCODING` | Unsupported characters | Use GSM or Unicode |

## Cost Optimization

### Reduce Message Parts

- Keep messages under 160 characters (GSM) or 70 (Unicode)
- Avoid special characters that trigger Unicode
- Use abbreviations when appropriate
- Remove unnecessary spaces

### Example Optimization

❌ **Before** (171 characters, 2 SMS):
```
Hello John! Your order #12345 has been successfully delivered to your address at 123 Main Street. Thank you for shopping with us! We hope to see you again soon.
```

✅ **After** (156 characters, 1 SMS):
```
Hi John! Order #12345 delivered to 123 Main St. Thanks for shopping with us! Visit example.com/order/12345 for details.
```

## Bulk Sending

Send multiple messages in one request:

```json
{
  "messages": [
    {
      "from": "YourBrand",
      "to": "+380111111111",
      "type": "sms",
      "text": "Message 1"
    },
    {
      "from": "YourBrand",
      "to": "+380222222222",
      "type": "sms",
      "text": "Message 2"
    },
    {
      "from": "YourBrand",
      "to": "+380333333333",
      "type": "sms",
      "text": "Message 3"
    }
  ]
}
```

## Next Steps

- [Viber Messages](viber.md) - Rich media messaging
- [RCS Messages](rcs.md) - Rich Communication Services
- [Check Status](status.md) - Track delivery status
- [Fallback Strategies](../../using-smsbat/fallback.md) - Configure fallbacks
