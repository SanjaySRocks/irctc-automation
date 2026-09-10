# IRCTC Automation

An automation tool built with Python and Playwright to automate the IRCTC ticket booking process.

The tool supports regular and **Tatkal ticket booking** and is designed to make the booking workflow faster by automating repetitive steps such as journey details, train selection, coach selection, passenger details, review, and payment selection.

## Features

- Automated IRCTC ticket booking workflow
- Supports **General and Tatkal booking**
- Journey source and destination configuration
- Journey date configuration
- Train number selection
- Coach/class selection
- Automatic coach availability checking
- Passenger details automation
- Preferred berth selection
- Auto-upgradation support
- Payment mode selection
- Payment vendor selection where supported by the configuration
- Configurable booking details through JSON files

## Project Structure

```text
irctc_playwright_structured/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   ├── config.json
│   ├── credentials.json
│   └── passengers.json
│
├── pages/
│   ├── base_page.py
│   ├── journey_page.py
│   ├── login_page.py
│   ├── train_page.py
│   ├── passenger_page.py
│   ├── review_page.py
│   └── payment_page.py
│
└── utils/
    ├── config_loader.py
    ├── validators.py
    └── station_utils.py
```

### Directory Description

| Path | Purpose |
|---|---|
| `main.py` | Main booking workflow and orchestration |
| `config/` | Runtime configuration, credentials, and passenger information |
| `pages/` | Page-object classes containing IRCTC UI interactions |
| `utils/` | Configuration loading, validation, and helper functions |
| `requirements.txt` | Python dependencies |

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install/use Patchright's supported browser setup

Set up the browser required by Patchright according to your environment.

### 3. Configure the application

Update the following files:

```text
config/config.json
config/credentials.json
config/passengers.json
```

### 4. Run the automation

```bash
python main.py
```

## Configuration

The main booking configuration is stored in:

```text
config/config.json
```

### Example

```json
{
    "from": "NDLS",
    "to": "FTP",
    "quota": "GENERAL",
    "date": "24/10/2026",
    "train_number": "12418",
    "coach_type": "SL",
    "auto_upgradation": true,
    "payment_mode": 2
}
```

### Configuration Fields

| Field | Description | Valid Values / Example |
|---|---|---|
| `from` | Source railway station code | `NDLS` |
| `to` | Destination railway station code | `FTP` |
| `quota` | Booking quota | `GENERAL`, `TATKAL` |
| `date` | Journey date | `DD/MM/YYYY` |
| `train_number` | Train number to select | `12418` |
| `coach_type` | Preferred coach/class | `SL`, `3A`, `2A`, `1A`, `3E` |
| `auto_upgradation` | Enable automatic class upgradation | `true`, `false` |
| `payment_mode` | Payment mode | `1`, `2` |

### Payment Modes

```text
1 - Pay through Credit & Debit Cards / Net Banking / Wallets / EMI / UPI_CC / UPI_CL / Rewards and Others
2 - Pay through BHIM/UPI
```

## Tatkal Booking

The automation supports **Tatkal ticket booking**.

To use Tatkal booking, set the quota in `config.json`:

```json
{
    "from": "NDLS",
    "to": "FTP",
    "quota": "TATKAL",
    "date": "24/10/2026",
    "train_number": "12418",
    "coach_type": "SL",
    "auto_upgradation": true,
    "payment_mode": 2
}
```

Tatkal tickets have limited availability and can sell out very quickly. The automation is intended to reduce the time spent on repetitive manual steps so the booking process can be performed faster.

**Important:** The automation cannot guarantee ticket availability or successful booking. Booking depends on IRCTC availability, server response, network conditions, payment processing, and other factors.

## Credentials

IRCTC login credentials are stored separately in:

```text
config/credentials.json
```

### Example

```json
{
    "username": "ENTER_IRCTC_USERNAME",
    "password": "ENTER_IRCTC_PASSWORD"
}
```

### Security

Do not commit your actual credentials to Git or publish them publicly.

It is recommended to add `credentials.json` to `.gitignore` if it is not already excluded.

## Passenger Configuration

Passenger information is stored in:

```text
config/passengers.json
```

### Example

```json
{
    "passengers": [
        {
            "name": "JOHN DOE",
            "age": 30,
            "gender": "M",
            "berth": ""
        }
    ]
}
```

### Passenger Fields

| Field | Description | Valid Values |
|---|---|---|
| `name` | Passenger full name as per Government ID | Maximum 16 characters |
| `age` | Passenger age | `1` to `125` |
| `gender` | Passenger gender | `M`, `F`, `T` |
| `berth` | Preferred berth | `LB`, `MB`, `UB`, `SL`, `SU`, or empty |

An empty `berth` value means no specific berth preference is selected.

## Disclaimer

This automation is provided for **educational and personal automation purposes**.

You are responsible for ensuring that your use of this automation complies with **IRCTC's terms, policies, booking rules, applicable laws, and any other relevant restrictions**.

The automation does not guarantee ticket availability, successful booking, payment completion, or any particular booking outcome.

**Use this automation at your own risk. The author/developer is not responsible for account restrictions, booking failures, payment issues, financial loss, service interruptions, or any other consequences resulting from the use of this automation.**

Always verify the booking details, passenger information, fare, and final booking status before relying on the result.
