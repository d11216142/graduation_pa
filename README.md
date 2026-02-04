# graduation_pa

## CPE Data Generator

This project generates 50 random CPE (Common Platform Enumeration) data entries from the NVD (National Vulnerability Database) database.

### Features

- Fetches real CPE data from the NVD API
- Extracts key information:
  - **Category**: Operating System (o), Application (a), or Hardware (h)
  - **Product Name**: Name of the software/hardware product
  - **Version**: Product version
  - **Vendor**: Product vendor/manufacturer
- Simulates additional fields:
  - **Date**: Random date within the last 2 years
  - **Location**: Simulated installation path
  - **Size (MB)**: Random size between 0.1 and 500 MB

### Installation

1. Install Python 3.7 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Run the script to generate CPE data:

```bash
# Use fallback dataset (fast, recommended)
python generate_cpe_data.py

# Use NVD API (slower but real-time data)
python generate_cpe_data.py --api
```

The script will:
1. Fetch CPE data (from fallback dataset or NVD API)
2. Process and extract required fields
3. Generate simulated fields (date, location, size)
4. Save the results to both JSON and CSV formats:
   - `cpe_data.json` - JSON format
   - `cpe_data.csv` - CSV format

#### Two Modes

1. **Fallback Mode (Default)**: Uses a pre-defined list of 75+ common CPE entries for fast generation
2. **API Mode**: Fetches real-time data from NVD API (slower due to rate limiting, ~6 seconds per request)

### Output Format

Each entry contains the following fields:

| Field    | Description                           | Example            |
|----------|---------------------------------------|--------------------|
| category | Type: o/a/h (OS/App/Hardware)         | a                  |
| product  | Product name                          | apache             |
| version  | Product version                       | 2.4.41             |
| vendor   | Vendor/manufacturer                   | apache             |
| date     | Installation/scan date (simulated)    | 2024-05-15         |
| location | Installation path (simulated)         | /usr/local/bin     |
| size_mb  | Size in megabytes (simulated)         | 125.45             |

### Example Output

```
Category: a | Product: apache | Version: 2.4.41
Vendor: apache
Date: 2024-05-15 | Location: /usr/local/bin | Size: 125.45 MB
```

### Notes

- The script respects NVD API rate limits (6 second delay between requests)
- Generation may take several minutes due to API rate limiting
- Real CPE data is fetched from official NVD sources
- Date, location, and size fields are simulated for demonstration purposes