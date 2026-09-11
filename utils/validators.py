from datetime import datetime, timedelta


def validate_journey(journey):
    target_date = datetime.strptime(journey.date, "%d/%m/%Y").date()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    if journey.quota == "TATKAL":
        if target_date != tomorrow:
            raise ValueError("Date is out of Tatkal window")

    elif journey.quota == "GENERAL":
        last_allowed_date = today + timedelta(days=60)

        if target_date < today or target_date > last_allowed_date:
            raise ValueError("Date is out of General booking window")

    else:
        raise ValueError(
            f"Invalid quota: {journey.quota}. "
            "Only TATKAL and GENERAL are supported."
        )

    return target_date
