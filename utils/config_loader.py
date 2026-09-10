import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class JourneyConfig:
    from_station: str
    to_station: str
    quota: str
    date: str


@dataclass(frozen=True)
class BookingConfig:
    train_number: str
    coach_type: str
    auto_upgradation: bool


@dataclass(frozen=True)
class PaymentConfig:
    mode: int
    vendor: str


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


@dataclass(frozen=True)
class AppConfig:
    journey: JourneyConfig
    booking: BookingConfig
    payment: PaymentConfig
    credentials: Credentials
    passengers: list


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_config(config_dir="config") -> AppConfig:
    base = Path(config_dir)

    config = _load_json(base / "config.json")
    credentials = _load_json(base / "credentials.json")
    passengers = _load_json(base / "passengers.json").get("passengers", [])

    return AppConfig(
        journey=JourneyConfig(
            from_station=config["from"],
            to_station=config["to"],
            quota=config["quota"].upper(),
            date=config["date"],
        ),
        booking=BookingConfig(
            train_number=config.get("train_number", ""),
            coach_type=config.get("coach_type", ""),
            auto_upgradation=config.get("auto_upgradation", False),
        ),
        payment=PaymentConfig(
            mode=config.get("payment_mode", 1),
            vendor=config.get("payment_vendor", "Paytm UPI"),
        ),
        credentials=Credentials(
            username=credentials.get("username", ""),
            password=credentials.get("password", ""),
        ),
        passengers=passengers,
    )
