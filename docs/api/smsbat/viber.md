# Viber Messages

SMSBAT API supports multiple types of Viber messages for different use cases, from promotional campaigns to transaction notifications.

## Message Types Overview

| Type | Purpose | Rich Media | Interactive |
|------|---------|------------|-------------|
| `viber_promo` | Marketing campaigns | ✅ Images, Videos | ✅ Buttons |
| `viber_trans` | Transactional notifications | ✅ PDFs | ❌ |
| `viber_carousel` | Product showcases | ✅ Images | ✅ Multiple buttons |
| `viber_survey` | Polls and feedback | ❌ | ✅ Multiple options |
| `viber_otp` | One-time passwords | ❌ | ❌ |

## Viber Promo

Promotional messages with rich media support for marketing campaigns.

### Supported Content

- Image only
- Text only
- Text + button
- Image + text + button
- Video + text
- Video + text + button
- Video only

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `img` | string | No | Image URL |
| `video` | string | No | Video file URL |
| `thumbnail` | string | No | Video preview image |
| `buttonText` | string | No | Call-to-action button label |
| `buttonAction` | string | No | Button click URL destination |
| `fileSize` | integer | No | Video file size in bytes |
| `duration` | integer | No | Video length in seconds |

### Examples

#### Text + Image + Button

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "viber_promo",
  "text": "Summer Sale! Up to 50% off on selected items.",
  "messageData": {
    "img": "https://example.com/summer-sale.jpg",
    "buttonText": "Shop Now",
    "buttonAction": "https://example.com/sale"
  }
}
```

#### Video + Text + Button

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "viber_promo",
  "text": "Watch our new product demo!",
  "messageData": {
    "video": "https://example.com/demo.mp4",
    "thumbnail": "https://example.com/thumbnail.jpg",
    "fileSize": 5242880,
    "duration": 30,
    "buttonText": "Learn More",
    "buttonAction": "https://example.com/product"
  }
}
```

#### Image Only

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "viber_promo",
  "messageData": {
    "img": "https://example.com/banner.jpg"
  }
}
```

## Viber Transactional

Transaction notifications for time-sensitive information like order confirmations and receipts.

### Supported Content

- Text only
- PDF file + text
- PDF file only

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fileUrl` | string | No | PDF document URL |
| `fileName` | string | No | Display name for attachment |
| `fileType` | string | No | File type (use "pdf") |

### Examples

#### Text Only

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "viber_trans",
  "text": "Your order #12345 has been confirmed and will be delivered tomorrow.",
  "ttl": 86400
}
```

#### Text + PDF

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "viber_trans",
  "text": "Thank you for your purchase! Please find your invoice attached.",
  "messageData": {
    "fileUrl": "https://example.com/invoice-12345.pdf",
    "fileName": "Invoice_12345.pdf",
    "fileType": "pdf"
  },
  "ttl": 86400
}
```

## Viber Carousel

Multi-item browsable showcase for products or content.

### Structure

Array of carousel items, each containing:

- Title
- Image
- Primary button (main action)
- Secondary button (alternative action)

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `carousel` | array | Yes | Array of carousel items |
| `items` | array | Yes | Individual card objects |

### Example

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "viber_carousel",
  "text": "Check out our featured products",
  "messageData": {
    "carousel": {
      "items": [
        {
          "title": "Product A",
          "imageUrl": "https://example.com/product-a.jpg",
          "primaryButton": {
            "text": "Buy Now",
            "url": "https://example.com/product-a"
          },
          "secondaryButton": {
            "text": "Details",
            "url": "https://example.com/product-a/details"
          }
        },
        {
          "title": "Product B",
          "imageUrl": "https://example.com/product-b.jpg",
          "primaryButton": {
            "text": "Buy Now",
            "url": "https://example.com/product-b"
          },
          "secondaryButton": {
            "text": "Details",
            "url": "https://example.com/product-b/details"
          }
        }
      ]
    }
  }
}
```

## Viber Survey

Interactive polls and feedback collection with multiple choice options.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `survey` | object | Yes | Survey container |
| `options` | array | Yes | Array of 1-5 answer choices |

### Constraints

- Maximum 5 response options supported
- Each option should be concise (recommended: under 30 characters)

### Example

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "viber_survey",
  "text": "How satisfied are you with our service?",
  "messageData": {
    "survey": {
      "options": [
        "Very Satisfied",
        "Satisfied",
        "Neutral",
        "Dissatisfied",
        "Very Dissatisfied"
      ]
    }
  }
}
```

## Viber OTP

One-time password delivery with pre-defined templates.

### Key Features

- 9 pre-defined templates
- Parameter validation (TEXT, NUMBER types)
- Multi-language support (19 languages)
- Case-sensitive variable names

### Supported Languages

Ukrainian, English, Russian, Polish, Romanian, Spanish, German, French, Italian, Portuguese, Dutch, Turkish, Arabic, Hebrew, Hindi, Chinese, Japanese, Korean, Vietnamese

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `templateId` | string (UUID) | Yes | Template identifier |
| `templateLang` | string | Yes | ISO language code |
| `templateParams` | object | Yes | Variables matching template |

### Example

```json
{
  "from": "YourApp",
  "to": "+380XXXXXXXXX",
  "type": "viber_otp",
  "messageData": {
    "templateId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "templateLang": "en",
    "templateParams": {
      "PIN": "123456",
      "TIME": "10"
    }
  },
  "ttl": 600
}
```

Template example: "Your code: 123456. Valid for 10 minutes. Never share this code."

## General Requirements

All Viber message types require:

- `from`: Alphanumeric sender ID
- `to`: Phone number in E.164 format
- `type`: Message type identifier
- `ttl`: Message expiration time in seconds (recommended)

## Fallback to SMS

All Viber message types support SMS fallback. If Viber delivery fails, the message automatically falls back to SMS:

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "viber_promo",
  "text": "Your Viber message",
  "messageData": {
    "img": "https://example.com/image.jpg"
  },
  "fallback": {
    "type": "sms",
    "text": "Your SMS fallback message (image not included)"
  }
}
```

## Best Practices

### Images

- Use JPG or PNG format
- Recommended size: 800x600 pixels
- Keep file size under 1MB
- Use HTTPS URLs

### Videos

- Use MP4 format
- Keep file size under 10MB
- Include thumbnail image
- Specify duration and fileSize

### Buttons

- Keep button text short (2-3 words)
- Use clear call-to-action phrases
- Always use HTTPS URLs
- Test URLs before sending

### TTL (Time-to-Live)

- Promotional messages: 24-72 hours
- Transactional messages: 24 hours
- OTP messages: 5-10 minutes
- Surveys: 7-30 days

## Next Steps

- [SMS Messages](sms.md) - Learn about SMS fallback
- [RCS Messages](rcs.md) - Rich Communication Services
- [Check Status](status.md) - Track delivery status
