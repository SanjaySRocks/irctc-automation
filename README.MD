# IRCTC Automation

An automation tool to book irctc ticket online 

## Run

1. Install dependencies:
   `pip install -r requirements.txt`

2. Install/use Patchright's supported browser setup as required by your environment.

3. Edit:
   - `config/config.json`
   - `config/credentials.json`
   - `config/passengers.json`

4. Run:
   `python main.py`

## Structure

- `main.py` - orchestration only
- `config/` - runtime configuration and credentials
- `pages/` - page-object classes
- `utils/` - configuration loading, validation, and station helper

# Configuration  Help

config.json
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

| Field              | Description                      | Valid Values / Example       |
| ------------------ | -------------------------------- | ---------------------------- |
| `from`             | Source railway station code      | `NDLS`                       |
| `to`               | Destination railway station code | `FTP`                        |
| `quota`            | Booking quota                    | `GENERAL`, `TATKAL`          |
| `date`             | Journey date                     | Format: `DD/MM/YYYY`         |
| `train_number`     | Train number to select           | Example: `12418`             |
| `coach_type`       | Coach class code                 | `SL`, `3A`, `2A`, `1A`, `3E` |
| `auto_upgradation` | Enable auto upgradation          | `true`, `false`              |
| `payment_mode`     | Payment mode                     | `1 - Debit/Credit Card/UPI`, `2- BHIM/UPI`                     |

# Credentials

credentials.json

```json
{
    "username": "ENTER_IRCTC_USERNAME",
    "password": "ENTER_IRCTC_PASSWORD"
}
```

## Passengers Configuration

Passenger details are configured in the `passengers.json` file.

### Example

passengers.json
```json
{
    "passengers": [
        {
            "name": "SANJAY SINGH",
            "age": 25,
            "gender": "M",
            "berth": ""
        }
    ]
}
```

| Field    | Description                              | Valid Values                           |
| -------- | ---------------------------------------- | -------------------------------------- |
| `name`   | Passenger full name as per Government ID | Maximum 16 characters                  |
| `age`    | Passenger age                            | `1` to `125`                           |
| `gender` | Passenger gender                         | `M`, `F`, `T`                          |
| `berth`  | Preferred berth                          | `LB`, `MB`, `UB`, `SL`, `SU`, or empty for no preference |
