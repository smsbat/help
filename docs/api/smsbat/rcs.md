# RCS Messages

RCS (Rich Communication Services) is the next generation of messaging for Android devices, offering rich media, interactivity, and advanced features beyond traditional SMS.

## Overview

RCS provides enhanced messaging capabilities:

- Rich media (images, videos, GIFs)
- Interactive buttons and carousels
- Read receipts and typing indicators
- Higher character limits (up to 3072 characters)
- Better delivery tracking
- Branded sender identification

## Availability

- **Platform**: Android devices only
- **Network**: Requires carrier RCS support
- **Fallback**: Automatically falls back to SMS if RCS unavailable

## Basic RCS Message

### Request

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Your RCS message text with rich formatting"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | string | Yes | Alphanumeric sender ID |
| `to` | string | Yes | Recipient phone number (E.164) |
| `type` | string | Yes | Set to `"rcs"` |
| `text` | string | Yes | Message content (up to 3072 chars) |
| `messageData` | object | No | Rich media and buttons |

## Message Types

### Text Only

Simple text message with extended character limit:

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Welcome to our service! RCS allows us to send much longer messages with rich formatting and interactive elements."
}
```

### Text + Image

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Check out our new product!",
  "messageData": {
    "media": {
      "url": "https://example.com/product.jpg",
      "type": "image/jpeg",
      "height": 600,
      "width": 800
    }
  }
}
```

### Text + Image + Button

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Summer Sale - Up to 50% off!",
  "messageData": {
    "media": {
      "url": "https://example.com/sale-banner.jpg",
      "type": "image/jpeg"
    },
    "buttons": [
      {
        "text": "Shop Now",
        "action": {
          "type": "openUrl",
          "url": "https://example.com/sale"
        }
      }
    ]
  }
}
```

### Text + Video

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Watch our product demo",
  "messageData": {
    "media": {
      "url": "https://example.com/demo.mp4",
      "type": "video/mp4",
      "thumbnail": "https://example.com/thumbnail.jpg"
    }
  }
}
```

### Text + Multiple Buttons

```json
{
  "from": "YourService",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Your order #12345 is ready for pickup",
  "messageData": {
    "buttons": [
      {
        "text": "Track Order",
        "action": {
          "type": "openUrl",
          "url": "https://example.com/track/12345"
        }
      },
      {
        "text": "Contact Support",
        "action": {
          "type": "dial",
          "phoneNumber": "+380XXXXXXXXX"
        }
      },
      {
        "text": "Cancel Order",
        "action": {
          "type": "openUrl",
          "url": "https://example.com/cancel/12345"
        }
      }
    ]
  }
}
```

## RCS Carousel

Display multiple items in a scrollable carousel:

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Featured Products",
  "messageData": {
    "carousel": {
      "cards": [
        {
          "title": "Product A",
          "description": "Premium quality product",
          "media": {
            "url": "https://example.com/product-a.jpg",
            "type": "image/jpeg"
          },
          "buttons": [
            {
              "text": "Buy Now",
              "action": {
                "type": "openUrl",
                "url": "https://example.com/product-a"
              }
            },
            {
              "text": "Details",
              "action": {
                "type": "openUrl",
                "url": "https://example.com/product-a/details"
              }
            }
          ]
        },
        {
          "title": "Product B",
          "description": "Best seller",
          "media": {
            "url": "https://example.com/product-b.jpg",
            "type": "image/jpeg"
          },
          "buttons": [
            {
              "text": "Buy Now",
              "action": {
                "type": "openUrl",
                "url": "https://example.com/product-b"
              }
            }
          ]
        }
      ]
    }
  }
}
```

## Button Actions

### Open URL

```json
{
  "text": "Visit Website",
  "action": {
    "type": "openUrl",
    "url": "https://example.com"
  }
}
```

### Dial Phone Number

```json
{
  "text": "Call Us",
  "action": {
    "type": "dial",
    "phoneNumber": "+380XXXXXXXXX"
  }
}
```

### Send Location

```json
{
  "text": "Share Location",
  "action": {
    "type": "shareLocation"
  }
}
```

### Calendar Event

```json
{
  "text": "Add to Calendar",
  "action": {
    "type": "createCalendarEvent",
    "title": "Appointment",
    "startTime": "2025-01-25T14:00:00Z",
    "endTime": "2025-01-25T15:00:00Z"
  }
}
```

## Media Specifications

### Images

- **Formats**: JPEG, PNG, GIF
- **Max size**: 2MB
- **Recommended resolution**: 800x600 or 1200x800
- **Aspect ratio**: 16:9 or 4:3

### Videos

- **Formats**: MP4, 3GP
- **Max size**: 10MB
- **Max duration**: 2 minutes
- **Recommended resolution**: 1280x720

### Audio

- **Formats**: MP3, AAC
- **Max size**: 5MB
- **Max duration**: 5 minutes

## Fallback to SMS

RCS automatically falls back to SMS when:

- Recipient doesn't have RCS
- RCS is disabled on recipient device
- Network doesn't support RCS

```json
{
  "from": "YourBrand",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Check out our new product!",
  "messageData": {
    "media": {
      "url": "https://example.com/product.jpg",
      "type": "image/jpeg"
    },
    "buttons": [
      {
        "text": "Shop Now",
        "action": {
          "type": "openUrl",
          "url": "https://example.com/shop"
        }
      }
    ]
  },
  "fallback": {
    "type": "sms",
    "text": "Check out our new product! Visit: https://example.com/shop"
  }
}
```

## Use Cases

### E-commerce

```json
{
  "from": "YourStore",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Your order has been shipped!",
  "messageData": {
    "media": {
      "url": "https://example.com/package.jpg",
      "type": "image/jpeg"
    },
    "buttons": [
      {
        "text": "Track Package",
        "action": {
          "type": "openUrl",
          "url": "https://example.com/track/ABC123"
        }
      },
      {
        "text": "Contact Support",
        "action": {
          "type": "dial",
          "phoneNumber": "+380XXXXXXXXX"
        }
      }
    ]
  }
}
```

### Banking

```json
{
  "from": "YourBank",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Low balance alert: Your account balance is $50",
  "messageData": {
    "buttons": [
      {
        "text": "View Balance",
        "action": {
          "type": "openUrl",
          "url": "https://bank.example.com/balance"
        }
      },
      {
        "text": "Transfer Money",
        "action": {
          "type": "openUrl",
          "url": "https://bank.example.com/transfer"
        }
      }
    ]
  }
}
```

### Travel

```json
{
  "from": "YourAirline",
  "to": "+380XXXXXXXXX",
  "type": "rcs",
  "text": "Your flight is departing in 3 hours",
  "messageData": {
    "media": {
      "url": "https://example.com/boarding-pass.jpg",
      "type": "image/jpeg"
    },
    "buttons": [
      {
        "text": "Check-in",
        "action": {
          "type": "openUrl",
          "url": "https://airline.example.com/checkin"
        }
      },
      {
        "text": "Add to Calendar",
        "action": {
          "type": "createCalendarEvent",
          "title": "Flight Departure",
          "startTime": "2025-01-25T10:00:00Z"
        }
      }
    ]
  }
}
```

## Best Practices

### Content

- ✅ Use high-quality images (800x600 minimum)
- ✅ Keep button text short (2-3 words)
- ✅ Provide SMS fallback for rich content
- ✅ Test on different Android devices
- ❌ Don't exceed 4-5 buttons per message
- ❌ Avoid large video files (>5MB)

### Media

- Use HTTPS URLs for all media
- Optimize images for mobile
- Include alt text for accessibility
- Test media URLs before sending

### Buttons

- Maximum 4 buttons per message
- Clear call-to-action text
- Test all button actions
- Consider fallback for unavailable actions

### Branding

- Use consistent sender ID
- Include brand logo where appropriate
- Maintain brand voice and tone
- Ensure visual consistency

## Delivery Status

RCS provides enhanced delivery tracking:

- **Sent**: Message sent to carrier
- **Delivered**: Message delivered to device
- **Read**: Message opened by recipient
- **Failed**: Delivery failed, fallback triggered

Check status using the [status endpoint](status.md).

## Next Steps

- [Viber Messages](viber.md) - Alternative rich messaging
- [SMS Messages](sms.md) - Fallback messaging
- [Check Status](status.md) - Track delivery
- [Fallback Strategies](../../using-smsbat/fallback.md) - Configure fallbacks
