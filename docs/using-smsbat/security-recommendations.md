# Security Rules and Recommendations

The security guidelines included below are meant to help you securely perform most common user actions, like authentication, API interactions, and user management within the SMSBAT platform and through the SMSBAT APIs.

## Account Security

Once you create an SMSBAT account, you will use your email and password to sign in to the SMSBAT web interface. 

### Password Management

SMSBAT password strength is important for your account's security. Follow these critical password tips to help protect your account:

- Do not use the same password for different users.
- Do not use passwords that you use elsewhere, especially for other online channels/services.
- Change passwords periodically.
- Never share your passwords or API keys with 3rd parties, including SMSBAT staff. Instead, use the SMSBAT web interface password reset form or manage API keys over the appropriate interface.

### Account Users

Here's how to manage account user credentials for maximum security:

1. Within the SMSBAT web interface, navigate to your team and user settings.
2. Limit the Account Manager or Administrator roles strictly to personnel who require full access. 
3. For daily operations and API integrations, assign roles with the principle of least privilege.
4. Verify all users' email addresses and phone numbers.

## API-Related Security Controls

This section provides information on how to increase security for API connectivity.

To mitigate the risk of network data transfer interception:

- Always use SSL/TLS encrypted connections (`HTTPS`) when interacting with our APIs.
- Increase security for API connectivity by using dedicated API keys instead of user credentials for API integrations. This mitigates the risk of network data transfer interception.
- Restrict API keys to specific IP addresses (IP Safelisting) if your integration allows for static IPs.

### Password/Token Abuse

To mitigate the risk of token or API key abuse:

- Treat your API keys and tokens like passwords and keep them secret. 
- Avoid hard coding user credentials or API keys on a public code repository.
- When working with the API, use tokens as environment variables instead of hard coding them into your programs.
- Rotate your API keys periodically.

## Verify the Authenticity of the Login Page to Prevent Phishing Attacks

Pay close attention to the URL and site content to ensure you are logging into the legitimate SMSBAT portal:

1. **Check the domain name:** The domain name can help confirm that you are landing on a legitimate SMSBAT site. It should always end in `smsbat.com`. Watch out for domains that imitate actual businesses (e.g., "smsbät.com", "sms-bat.com" if not officially communicated).
2. **Check the site's security status:** Look for the padlock icon in your browser's address bar to verify the connection is secured with HTTPS.
3. **Evaluate the URL:** A website's URL consists of the connection type ("HTTPS"), application, domain name ("smsbat"), extension (".com"), and the file path. Verify that the URL is exact.
4. **Review Certificate details:** Most browsers allow you to view the security certificate by clicking the padlock icon in the address bar. Ensure the certificate is issued to the correct entity.

If you suspect a phishing attempt or any security-related issues, please contact `help@smsbat.com` immediately.
