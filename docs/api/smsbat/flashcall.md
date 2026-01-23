# Flash Call

Flash Call is a phone verification method that uses a missed call instead of SMS to verify phone numbers. It's faster, more secure, and cost-effective.

## Overview

Flash Call verification works by:

1. User requests verification
2. System initiates a call to user's phone
3. Call is automatically terminated after 1-2 rings
4. User's app captures the caller ID
5. Caller ID is verified against expected pattern
6. User is authenticated

## Benefits

### Cost-Effective

- Up to 10x cheaper than SMS
- No message delivery fees
- Reduced costs for high-volume verification

### Faster

- Instant verification (1-3 seconds)
- No waiting for SMS delivery
- Better user experience

### More Secure

- Harder to intercept than SMS
- No OTP visible in notifications
- Resistant to SIM swap attacks

### Global Reach

- Works in countries with SMS restrictions
- No issues with SMS filtering
- Universal phone compatibility

## Basic Flash Call

### Request

```json
{
  "from": "YourApp",
  "to": "+380XXXXXXXXX",
  "type": "flashcall",
  "messageData": {
    "callerId": "+380123456789"
  }
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | string | Yes | Your sender identifier |
| `to` | string | Yes | Recipient phone number (E.164) |
| `type` | string | Yes | Set to `"flashcall"` |
| `callerId` | string | Yes | Phone number that will call user |
| `ttl` | integer | No | Time-to-live in seconds (default: 60) |

## How It Works

### 1. User Enters Phone Number

User provides their phone number in your app:

```
Phone: +380XXXXXXXXX
```

### 2. Request Flash Call

Your server requests flash call verification:

```bash
curl -X POST https://restapi.smsbat.com/bat/messagelist \
  -H "X-Authorization-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "from": "YourApp",
      "to": "+380XXXXXXXXX",
      "type": "flashcall",
      "messageData": {
        "callerId": "+380123456789"
      },
      "ttl": 60
    }]
  }'
```

### 3. API Response

API returns the expected caller ID pattern:

```json
{
  "messagelistId": 123456,
  "messages": [
    {
      "messageId": "abc123def456",
      "status": "accepted",
      "callerId": "+380123456789",
      "pattern": "***456789",
      "to": "+380XXXXXXXXX"
    }
  ]
}
```

### 4. Initiate Call

System initiates a call to user's phone and terminates after 1-2 rings.

### 5. Capture Caller ID

User's app captures the incoming call's caller ID:

```kotlin
// Android example
val cursor = contentResolver.query(
    CallLog.Calls.CONTENT_URI,
    arrayOf(CallLog.Calls.NUMBER),
    null, null,
    CallLog.Calls.DATE + " DESC"
)
```

### 6. Verify Pattern

Compare captured caller ID with expected pattern:

```javascript
// JavaScript example
function verifyFlashCall(callerId, pattern) {
  // Remove non-digits
  const callerDigits = callerId.replace(/\D/g, '');
  const patternDigits = pattern.replace(/\*/g, '.');

  // Check if matches pattern
  const regex = new RegExp(patternDigits);
  return regex.test(callerDigits);
}
```

## Implementation Examples

### Android

```kotlin
class FlashCallVerification {
    fun requestFlashCall(phoneNumber: String) {
        // 1. Request flash call from API
        val response = api.requestFlashCall(phoneNumber)
        val pattern = response.pattern

        // 2. Wait for incoming call
        val callReceiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                if (intent.action == TelephonyManager.ACTION_PHONE_STATE_CHANGED) {
                    val state = intent.getStringExtra(TelephonyManager.EXTRA_STATE)

                    if (state == TelephonyManager.EXTRA_STATE_RINGING) {
                        val callerId = intent.getStringExtra(
                            TelephonyManager.EXTRA_INCOMING_NUMBER
                        )

                        // 3. Verify caller ID against pattern
                        if (verifyPattern(callerId, pattern)) {
                            onVerificationSuccess()
                        }
                    }
                }
            }
        }

        // Register receiver
        context.registerReceiver(
            callReceiver,
            IntentFilter(TelephonyManager.ACTION_PHONE_STATE_CHANGED)
        )
    }

    private fun verifyPattern(callerId: String?, pattern: String): Boolean {
        if (callerId == null) return false

        val regex = pattern.replace("*", "\\d").toRegex()
        return regex.matches(callerId)
    }
}
```

### iOS

```swift
class FlashCallVerification {
    func requestFlashCall(phoneNumber: String) {
        // 1. Request flash call from API
        api.requestFlashCall(phoneNumber) { response in
            let pattern = response.pattern

            // 2. Use CallKit to detect incoming call
            let provider = CXProvider(configuration: providerConfiguration)
            provider.setDelegate(self, queue: nil)

            // Store pattern for verification
            self.expectedPattern = pattern
        }
    }

    // CallKit delegate
    func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
        // Capture caller ID
        let callerId = action.callUUID.uuidString

        // Verify against pattern
        if verifyPattern(callerId: callerId, pattern: expectedPattern) {
            onVerificationSuccess()
        }

        action.fulfill()
    }

    private func verifyPattern(callerId: String, pattern: String) -> Bool {
        let regex = try! NSRegularExpression(
            pattern: pattern.replacingOccurrences(of: "*", with: "\\d")
        )
        let range = NSRange(location: 0, length: callerId.count)
        return regex.firstMatch(in: callerId, range: range) != nil
    }
}
```

### Web (Server-Side)

```javascript
// Node.js example
const express = require('express');
const app = express();

app.post('/request-verification', async (req, res) => {
  const { phoneNumber } = req.body;

  // 1. Request flash call
  const response = await fetch('https://restapi.smsbat.com/bat/messagelist', {
    method: 'POST',
    headers: {
      'X-Authorization-Key': process.env.SMSBAT_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [{
        from: 'YourApp',
        to: phoneNumber,
        type: 'flashcall',
        messageData: {
          callerId: process.env.FLASH_CALL_NUMBER
        },
        ttl: 60
      }]
    })
  });

  const data = await response.json();
  const { messageId, pattern } = data.messages[0];

  // 2. Store pattern for verification
  await redis.setex(`flashcall:${messageId}`, 60, pattern);

  // 3. Return pattern to client
  res.json({ messageId, pattern });
});

app.post('/verify-flashcall', async (req, res) => {
  const { messageId, callerId } = req.body;

  // 1. Get expected pattern
  const pattern = await redis.get(`flashcall:${messageId}`);

  if (!pattern) {
    return res.status(400).json({ error: 'Verification expired' });
  }

  // 2. Verify caller ID
  const regex = new RegExp(pattern.replace(/\*/g, '\\d'));
  const isValid = regex.test(callerId);

  if (isValid) {
    // Mark phone as verified
    await markPhoneVerified(callerId);
    res.json({ verified: true });
  } else {
    res.status(400).json({ error: 'Invalid caller ID' });
  }
});
```

## Response Format

### Success Response

```json
{
  "messagelistId": 123456,
  "messages": [
    {
      "messageId": "abc123def456",
      "status": "accepted",
      "callerId": "+380123456789",
      "pattern": "***456789",
      "to": "+380XXXXXXXXX",
      "ttl": 60
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `messageId` | string | Unique verification ID |
| `status` | string | Status: `accepted`, `rejected` |
| `callerId` | string | Full caller ID number |
| `pattern` | string | Pattern to match (digits + asterisks) |
| `to` | string | Recipient phone number |
| `ttl` | integer | Validity period in seconds |

## Pattern Matching

The API returns a pattern with asterisks masking some digits:

```
Full number: +380123456789
Pattern:     ***456789
```

Your app should:

1. Capture incoming caller ID
2. Extract digits from caller ID
3. Match against pattern (asterisks = any digit)
4. Verify match within TTL period

## Fallback to SMS

If Flash Call fails, automatically fall back to SMS:

```json
{
  "from": "YourApp",
  "to": "+380XXXXXXXXX",
  "type": "flashcall",
  "messageData": {
    "callerId": "+380123456789"
  },
  "fallback": {
    "type": "sms",
    "text": "Your verification code is: 123456"
  },
  "ttl": 60
}
```

## Use Cases

### Account Registration

Verify phone numbers during signup without SMS costs.

### Login Verification

Two-factor authentication using flash call.

### Phone Number Update

Verify new phone number when user updates profile.

### Transaction Confirmation

Confirm high-value transactions with flash call.

## Best Practices

### TTL

- ✅ Set TTL to 60-90 seconds
- ✅ Allow user to retry after expiration
- ❌ Don't use TTL longer than 120 seconds

### User Experience

- Show "Waiting for call..." message
- Display countdown timer (60 seconds)
- Provide option to "Use SMS instead"
- Auto-detect and verify caller ID

### Error Handling

- Handle missing phone permissions
- Timeout after TTL expires
- Provide SMS fallback option
- Show clear error messages

### Permissions

Request phone permissions before flash call:

**Android:**
```xml
<uses-permission android:name="android.permission.READ_PHONE_STATE" />
<uses-permission android:name="android.permission.READ_CALL_LOG" />
```

**iOS:**
```xml
<key>NSPhoneCallUsageDescription</key>
<string>We need phone access to verify your number</string>
```

### Testing

- Test on different devices
- Test with different carriers
- Test permission denial scenarios
- Test network timeout scenarios

## Limitations

### Platform Support

- Works on all mobile devices
- Requires phone call capability
- Needs READ_PHONE_STATE permission
- May not work on tablets without phone

### Network

- Requires active phone connection
- May fail in poor network conditions
- Carrier restrictions may apply
- International rates may vary

### Privacy

- Users may block unknown numbers
- Some devices have call blocking
- Requires explicit permissions
- Consider user privacy concerns

## Troubleshooting

### Call Not Received

- Check phone has signal
- Verify number format (E.164)
- Check carrier restrictions
- Try SMS fallback

### Pattern Not Matching

- Ensure capturing correct caller ID
- Strip non-digit characters
- Check pattern format
- Verify within TTL period

### Permission Denied

- Request permissions properly
- Explain why permissions needed
- Provide alternative (SMS)
- Handle gracefully

## Next Steps

- [Viber OTP](viber.md#viber-otp) - Alternative OTP delivery
- [SMS Messages](sms.md) - SMS fallback
- [Check Status](status.md) - Track flash call status
