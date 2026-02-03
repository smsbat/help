# SMSBAT Documentation

Welcome to the official documentation for **SMSBAT** - a reliable multi-channel messaging platform with powerful API solutions.

## What is SMSBAT?

SMSBAT is a comprehensive messaging platform that enables you to send messages across multiple channels: Viber, SMS, RCS, Telegram, Flash Call, and more. The platform provides three main products:

### 🚀 SMSBAT API
The main API for sending various types of messages:

- **Viber** (promo, transactional, carousel, survey, OTP)
- **SMS** (standard text messages)
- **RCS** (Rich Communication Services)
- **Flash Call** (voice verification)

[Learn more about SMSBAT API →](api/smsbat/index.md)

### 💬 ChatHub API
API for managing Viber business conversations and customer support:

- Operator management
- Organizations and companies
- Chat widget integration
- Incoming message handling

[Learn more about ChatHub API →](api/chathub/index.md)

### 🔄 Cascade API
Cascade message delivery across multiple channels:

- Automatic fallback between channels
- Telegram → Viber → SMS chains
- Improved deliverability
- Dynamic variables in messages

[Learn more about Cascade API →](api/cascade/index.md)

## Key Features

- **Multi-channel delivery** - Send via Viber, SMS, RCS, Telegram, Flash Call
- **High speed** - Instant message delivery
- **Fallback strategies** - Automatic channel switching
- **REST API** - Simple and intuitive API
- **Multiple message types** - transactional, promotional, OTP, surveys
- **Webhook support** - Receive delivery status callbacks
- **Detailed analytics** - Reports and statistics

## Quick Start

1. Get your API key for platform access
2. Choose the product you need (SMSBAT, ChatHub, or Cascade)
3. Review the API documentation
4. Start sending messages

[Get Started →](using-smsbat/quickstart.md)

## Message Types

| Type | Description | API |
|------|-------------|-----|
| **Viber Promo** | Marketing messages with images/videos and buttons | SMSBAT, Cascade |
| **Viber Trans** | Transactional messages for critical notifications | SMSBAT, Cascade |
| **Viber Carousel** | Carousel with multiple items | SMSBAT |
| **Viber Survey** | Polls with answer options | SMSBAT, Cascade |
| **Viber OTP** | One-time password templates (9 languages) | SMSBAT |
| **SMS** | Standard SMS messages | SMSBAT, Cascade |
| **RCS** | Rich Communication Services | SMSBAT, Cascade |
| **Flash Call** | Voice calls for verification | SMSBAT, Cascade |

[Learn more about message types →](using-smsbat/message-types.md)

## Authentication

SMSBAT supports multiple authentication methods:

- HTTP Basic Authentication
- X-Authorization-Key header
- Bearer token

[Learn more about authentication →](using-smsbat/authentication.md)

## Integrations

Ready-to-use code examples for various programming languages:

- [PHP](integrations/php.md)
- [Python](integrations/python.md)
- [Node.js](integrations/nodejs.md)
- [Java](integrations/java.md)
- [C#](integrations/csharp.md)

## Documentation Structure

### Using SMSBAT
General information about using the platform, message types, authentication, and fallback strategies.

### API
Detailed documentation of all API endpoints with request and response examples for SMSBAT, ChatHub, and Cascade APIs.

### Integrations
Integration examples and code in various programming languages.

## Need Help?

- Browse the relevant documentation section
- Contact support: help@smsbat.com
- Visit our website: [smsbat.com](https://smsbat.com)

---

**Ready to start?** Go to the [Quickstart guide](using-smsbat/quickstart.md)!
