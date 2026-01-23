# SMSBAT Documentation

Official documentation for the SMSBAT messaging platform.

## About

This repository contains the source code for [help.smsbat.com](https://help.smsbat.com) - the official documentation site for SMSBAT API, ChatHub API, and Cascade API.

## Technologies

- **MkDocs** - Static site generator
- **Material for MkDocs** - Modern documentation theme
- **mkdocs-static-i18n** - Multi-language support
- **GitHub Pages** - Hosting

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/smsbat/help.git
cd help
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run local development server:
```bash
mkdocs serve
```

4. Open your browser at `http://127.0.0.1:8000`

## Building

To build the static site:

```bash
mkdocs build
```

The generated site will be in the `site/` directory.

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch using GitHub Actions.

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── using-smsbat/              # Using SMSBAT section
│   ├── index.md
│   ├── quickstart.md
│   ├── authentication.md
│   ├── message-types.md
│   ├── delivery-status.md
│   └── fallback.md
├── api/                       # API documentation
│   ├── index.md
│   ├── smsbat/               # SMSBAT API
│   ├── chathub/              # ChatHub API
│   └── cascade/              # Cascade API
└── integrations/             # Integration guides
    ├── index.md
    ├── php.md
    ├── python.md
    ├── nodejs.md
    ├── java.md
    └── csharp.md
```

## Multi-language Support

The documentation supports multiple languages:

- **English** (default) - `/en/`
- **Ukrainian** - `/uk/`

To add a new language, update the `mkdocs.yml` file and create corresponding translation files.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Copyright © 2025 SMSBAT

## Support

- Email: support@smsbat.com
- Website: [smsbat.com](https://smsbat.com)
- Documentation: [help.smsbat.com](https://help.smsbat.com)
