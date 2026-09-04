def is_available(value):
    return value and value.strip().lower() != "unknown"


def calculate_lead_score(requirement, timeline, budget):
    if (
        is_available(requirement)
        and is_available(timeline)
        and is_available(budget)
    ):
        return {
            "status": "HOT",
            "reason": "The client has a clear requirement, timeline, and budget."
        }

    if is_available(requirement):
        return {
            "status": "WARM",
            "reason": "The client has a clear requirement but important information is missing."
        }

    return {
        "status": "COLD",
        "reason": "The client is making a general inquiry without a clear project requirement."
    }


if __name__ == "__main__":
    result = calculate_lead_score(
        requirement="WhatsApp customer support automation",
        timeline="Within one month",
        budget="Unknown",
    )

    print(result)