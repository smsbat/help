# Message Types

Cascade API supports four message types, each optimized for different use cases and channels.

## Overview

| Type | Purpose | Channels | Interactive |
|------|---------|----------|-------------|
| `transaction` | Critical notifications | All | No |
| `promo` | Marketing campaigns | All | Yes (buttons) |
| `viber_survey` | Polls and feedback | Viber, SMS | Yes (options) |
| `flashcall` | Phone verification | Phone call | No |

## Transaction Messages

Critical notifications like order confirmations, account updates, and system alerts.

### Characteristics

- High priority delivery
- No promotional content
- Direct and concise
- Time-sensitive
- Routed through: Telegram → Viber → RCS → SMS

### Use Cases

- Order confirmations
- Payment notifications
- Account alerts
- Security notifications
- Delivery updates
- Password resets

### Example

```json
{
  "id": "tx-order-12345",
  "fromName": "YourStore",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "transaction",
  "text": "Order #12345 confirmed. Total: $99.99. Delivery: Jan 25. Track: https://example.com/track/12345",
  "ttl": 86400
}
```

### Best Practices

- ✅ Keep messages under 160 characters when possible
- ✅ Include relevant transaction details
- ✅ Provide tracking links
- ✅ Use clear, professional language
- ❌ Don't include marketing content
- ❌ Don't use emojis excessively

### Examples by Use Case

#### Order Confirmation

```json
{
  "messageType": "transaction",
  "text": "Order #12345 confirmed. Total: $99.99. Expected delivery: Jan 25."
}
```

#### Payment Notification

```json
{
  "messageType": "transaction",
  "text": "Payment of $150.00 to Merchant ABC successful. Transaction ID: TXN789. Balance: $850.00"
}
```

#### Security Alert

```json
{
  "messageType": "transaction",
  "text": "New login detected from iPhone at 10:30 AM. Location: New York. If this wasn't you, secure your account immediately."
}
```

#### Delivery Update

```json
{
  "messageType": "transaction",
  "text": "Your package is out for delivery! Expected arrival: 2-4 PM. Track: https://track.example.com/PKG123"
}
```

## Promo Messages

Marketing and promotional campaigns with rich media and interactive elements.

### Characteristics

- Rich media support
- Interactive buttons
- Call-to-action focused
- Longer TTL acceptable
- Routed through: Telegram → Viber → RCS → SMS

### Use Cases

- Product launches
- Sales announcements
- Event invitations
- Newsletter campaigns
- Special offers
- Brand awareness

### Example

```json
{
  "id": "promo-summer-sale",
  "fromName": "YourBrand",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "promo",
  "text": "🌟 Summer Sale! Up to 50% off on selected items. Shop now: https://example.com/sale",
  "ttl": 259200
}
```

### With Variables

```json
{
  "messageType": "promo",
  "text": "Hi %name=1%! Exclusive offer: Use code %name=2% for 20% off. Shop: %short_url=1%",
  "variables": [
    {"id": 1, "type": "name", "value": "John"},
    {"id": 2, "type": "name", "value": "VIP20"},
    {"id": 1, "type": "short_url", "value": "https://store.com/sale?utm=sms"}
  ]
}
```

### Best Practices

- ✅ Include clear call-to-action
- ✅ Use engaging language
- ✅ Add tracking parameters to URLs
- ✅ Personalize with variables
- ✅ Test on multiple channels
- ❌ Don't spam customers
- ❌ Don't use misleading content
- ❌ Don't exceed character limits

### Examples by Use Case

#### Product Launch

```json
{
  "messageType": "promo",
  "text": "🎉 NEW ARRIVAL: iPhone 15 Pro now available! Pre-order today and get free shipping. Visit: https://store.com/iphone15"
}
```

#### Flash Sale

```json
{
  "messageType": "promo",
  "text": "⚡ FLASH SALE: 2 hours only! Extra 30% off everything. Use code: FLASH30. Shop now: https://store.com/flash"
}
```

#### Event Invitation

```json
{
  "messageType": "promo",
  "text": "You're invited! VIP Shopping Event on Jan 25 at 6 PM. Exclusive deals + refreshments. RSVP: https://events.com/vip"
}
```

#### Abandoned Cart

```json
{
  "messageType": "promo",
  "text": "Hi %name=1%! You left items in your cart. Complete purchase now and get 10% off with code CART10: %short_url=1%"
}
```

## Viber Survey

Interactive polls and surveys for collecting customer feedback.

### Characteristics

- 2-5 response options
- Text limited to 85 characters
- Interactive interface on Viber
- Fallback to SMS (without interactivity)
- Single-question format

### Use Cases

- Customer satisfaction surveys
- Product feedback
- Service quality ratings
- Market research
- Event feedback
- Net Promoter Score (NPS)

### Example

```json
{
  "id": "survey-satisfaction-001",
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

### Constraints

- **Text**: Maximum 85 characters
- **Options**: 2-5 choices
- **Option Length**: Keep under 30 characters each
- **TTL**: Recommended 7-30 days

### Best Practices

- ✅ Ask one clear question
- ✅ Provide balanced options
- ✅ Use simple language
- ✅ Keep options concise
- ✅ Set appropriate TTL (7+ days)
- ❌ Don't ask multiple questions
- ❌ Don't use technical jargon
- ❌ Don't bias responses

### Examples by Use Case

#### Customer Satisfaction (NPS)

```json
{
  "messageType": "viber_survey",
  "text": "How likely are you to recommend us to a friend?",
  "surveyOptions": [
    "0 - Not at all",
    "1-6 - Unlikely",
    "7-8 - Likely",
    "9-10 - Very Likely"
  ]
}
```

#### Product Feedback

```json
{
  "messageType": "viber_survey",
  "text": "How do you rate our new product?",
  "surveyOptions": [
    "⭐️ Excellent",
    "⭐️ Good",
    "⭐️ Average",
    "⭐️ Poor",
    "⭐️ Very Poor"
  ]
}
```

#### Service Quality

```json
{
  "messageType": "viber_survey",
  "text": "Was your support experience helpful?",
  "surveyOptions": [
    "Yes, very helpful",
    "Somewhat helpful",
    "Not helpful"
  ]
}
```

#### Event Feedback

```json
{
  "messageType": "viber_survey",
  "text": "Would you attend our events again?",
  "surveyOptions": [
    "Definitely yes",
    "Probably yes",
    "Not sure",
    "Probably not",
    "Definitely not"
  ]
}
```

## Flash Call

Phone verification using automated calls instead of SMS codes.

### Characteristics

- Cost-effective verification
- Faster than SMS (1-3 seconds)
- No visible code in notifications
- Resistant to SIM swap attacks
- Phone call only (no Telegram/Viber)

### Use Cases

- User registration
- Login verification
- Phone number validation
- Two-factor authentication
- Account recovery
- Transaction confirmation

### Example

```json
{
  "id": "verify-user-12345",
  "fromName": "YourApp",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "flashcall",
  "ttl": 300
}
```

### How It Works

1. User enters phone number
2. API initiates flash call
3. Call terminates after 1-2 rings
4. App captures caller ID
5. Caller ID verified against pattern
6. User authenticated

### Best Practices

- ✅ Set short TTL (60-300 seconds)
- ✅ Implement caller ID detection
- ✅ Provide SMS fallback
- ✅ Handle permission requests
- ✅ Show clear instructions
- ❌ Don't use for promotional purposes
- ❌ Don't set long TTL

### Example with Fallback

```json
{
  "id": "verify-001",
  "fromName": "YourApp",
  "toPhone": "+380XXXXXXXXX",
  "messageType": "flashcall",
  "ttl": 300,
  "fallback": {
    "messageType": "transaction",
    "text": "Your verification code: 123456"
  }
}
```

## Choosing the Right Type

### Decision Tree

```
Is it time-critical or transactional?
├─ Yes → transaction
└─ No
   └─ Is it promotional?
      ├─ Yes → promo
      └─ No
         └─ Is it a survey?
            ├─ Yes → viber_survey
            └─ No → Is it for verification?
               ├─ Yes → flashcall
               └─ No → transaction (default)
```

### Comparison Matrix

| Feature | Transaction | Promo | Survey | Flash Call |
|---------|-------------|-------|--------|------------|
| Rich Media | ❌ | ✅ | ❌ | ❌ |
| Interactive | ❌ | ✅ | ✅ | ❌ |
| Personalization | ✅ | ✅ | ✅ | ❌ |
| Typical TTL | Hours | Days | Week | Minutes |
| Cost | Medium | Medium | Medium | Low |
| Delivery Speed | Fast | Fast | Fast | Fastest |

## Implementation Example

```javascript
class CascadeMessageBuilder {
  constructor(apiKey) {
    this.apiKey = apiKey;
  }

  buildTransaction(id, fromName, toPhone, text, ttl = 86400) {
    return {
      id,
      fromName,
      toPhone,
      messageType: 'transaction',
      text,
      ttl
    };
  }

  buildPromo(id, fromName, toPhone, text, ttl = 259200) {
    return {
      id,
      fromName,
      toPhone,
      messageType: 'promo',
      text,
      ttl
    };
  }

  buildSurvey(id, fromName, toPhone, text, options, ttl = 604800) {
    if (text.length > 85) {
      throw new Error('Survey text must be under 85 characters');
    }

    if (options.length < 2 || options.length > 5) {
      throw new Error('Survey must have 2-5 options');
    }

    return {
      id,
      fromName,
      toPhone,
      messageType: 'viber_survey',
      text,
      surveyOptions: options,
      ttl
    };
  }

  buildFlashCall(id, fromName, toPhone, ttl = 300) {
    return {
      id,
      fromName,
      toPhone,
      messageType: 'flashcall',
      ttl
    };
  }

  async send(message) {
    // Implementation to send message
  }
}

// Usage
const builder = new CascadeMessageBuilder('your-api-key');

// Transaction
const transaction = builder.buildTransaction(
  'order-123',
  'Store',
  '+380XXXXXXXXX',
  'Order confirmed'
);

// Promo
const promo = builder.buildPromo(
  'promo-001',
  'Brand',
  '+380XXXXXXXXX',
  'Sale now on!'
);

// Survey
const survey = builder.buildSurvey(
  'survey-001',
  'Brand',
  '+380XXXXXXXXX',
  'Rate our service?',
  ['Excellent', 'Good', 'Average', 'Poor']
);

// Flash Call
const flashCall = builder.buildFlashCall(
  'verify-001',
  'App',
  '+380XXXXXXXXX'
);
```

## Next Steps

- [Send Messages](send.md) - Start sending cascade messages
- [Message Variables](variables.md) - Personalize messages
- [SMSBAT API](../smsbat/index.md) - Explore SMSBAT features
