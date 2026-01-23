# API Documentation

SMSBAT provides three powerful APIs for different messaging and communication needs:

## SMSBAT API

The core messaging API for sending various types of messages including SMS, Viber, RCS, and Flash Call with fallback strategies.

[Explore SMSBAT API →](smsbat/index.md)

**Key Features:**

- Multiple message types (SMS, Viber, RCS, Flash Call)
- Fallback messaging when primary delivery fails
- Rich media support (images, videos, PDFs)
- Message status tracking
- OTP notifications

## ChatHub API

REST API for managing Viber business chats, client conversations, and customer support automation.

[Explore ChatHub API →](chathub/index.md)

**Key Features:**

- Company and operator token management
- Organization management
- Operator synchronization
- Widget integration for web applications
- Real-time chat support

## Cascade API

Multi-channel messaging API that automatically routes messages across Telegram Bot, Viber Bot, Viber Business Messages, RCS, and SMS with a single request.

[Explore Cascade API →](cascade/index.md)

**Key Features:**

- One API request for multi-channel delivery
- Automatic platform routing
- Variable substitution for dynamic content
- Message scheduling
- Time-to-live (TTL) support

## Getting Started

1. **Choose Your API** - Select the API that best fits your use case
2. **Get Credentials** - Contact your SMSBAT manager to obtain API credentials
3. **Review Authentication** - Each API uses different authentication methods
4. **Test Endpoints** - Use the provided examples to test integration
5. **Go Live** - Deploy your integration to production

## Authentication

Each API uses different authentication methods:

- **SMSBAT API**: HTTP Basic Auth, API Key Header, or API Key as Password
- **ChatHub API**: Bearer token (JWT) or `X-Authorization-Key` header
- **Cascade API**: `X-Authorization-Key`, `X-Viber-Auth-Token`, or `X-Tg-Bot-Key` headers

## Support

Need help? Contact our support team:

- Email: [support@smsbat.com](mailto:support@smsbat.com)
- Documentation: [developers.smsbat.com](https://developers.smsbat.com)

## Rate Limits

Please contact your account manager for information about rate limits and quotas for your account.
