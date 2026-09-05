from app.database.leads_db import Lead, SessionLocal


def add_demo_leads():
    session = SessionLocal()

    lead_count = session.query(Lead).count()

    if lead_count == 0:
        demo_leads = [
            Lead(
                business="ABC Clothing Store",
                requirement="WhatsApp customer-support automation",
                recommended_service="AI Integration and Automation",
                timeline="Within one month",
                budget="Unknown",
                lead_status="WARM",
                summary="Customers ask about order status and delivery on WhatsApp.",
                next_action="Ask for budget and current support tools.",
            ),
            Lead(
                business="Smart School",
                requirement="School management system",
                recommended_service="Custom Software Development",
                timeline="Two months",
                budget="PKR 500,000",
                lead_status="HOT",
                summary="School needs student, fee, attendance, and teacher management.",
                next_action="Schedule a consultation.",
            ),
            Lead(
                business="New Startup",
                requirement="General inquiry about HUMAITEC services",
                recommended_service="Unknown",
                timeline="Unknown",
                budget="Unknown",
                lead_status="COLD",
                summary="Visitor asked about available HUMAITEC services.",
                next_action="Ask about their business requirement.",
            ),
        ]

        session.add_all(demo_leads)
        session.commit()

        print("Demo leads added successfully.")
    else:
        print("Leads already exist. No duplicates added.")

    session.close()


if __name__ == "__main__":
    add_demo_leads()