# Django Profile Endpoint

A dynamic profile API endpoint built with Django that returns user information along with random cat facts from an external API.

## Features

- GET `/me` endpoint with required JSON structure
- Dynamic UTC timestamp in ISO 8601 format
- Integration with Cat Facts API
- Graceful error handling and fallbacks
- Environment-based configuration
- CORS support
- Health check endpoint

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Deglobeal/dynamic_Profile
cd dynamic_Profile