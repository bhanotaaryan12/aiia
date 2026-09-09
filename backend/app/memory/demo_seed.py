import logging
from app.memory.middleware.lifecycle import AgentMemoryLifecycle
from app.memory.graph.storage import TenantGraphStorage

logger = logging.getLogger(__name__)

def seed_demo_data():
    """Populate seed memory graphs for demo users."""
    lifecycle = AgentMemoryLifecycle()
    
    demo_users = {
        "admin@aiia.gov.in": [
            ("My name is Dr. Rajesh Kumar and I am the Super Administrator and Lead Investigator for AIIA CTMS.", "Welcome Dr. Kumar! System administration privileges confirmed."),
            ("I prefer executive summary outputs formatted in markdown tables with CDISC SDTM compliance codes.", "Noted your dashboard format and CDISC preference."),
            ("I am monitoring trial AYU-OA-2024 for Ashwagandha Osteoarthritis and trial AYU-DM-2024 for Diabetes Mellitus.", "Recorded active monitoring of AYU-OA-2024 and AYU-DM-2024."),
            ("Trial AYU-OA-2024 has enrolled 85 participants out of 120 target across AIIA New Delhi and BHU Varanasi sites.", "Updated enrollment statistics for AYU-OA-2024."),
            ("Central Ethics Committee approved protocol amendment v2.1 under NDCT Rules 2019.", "Recorded ethics clearance for protocol v2.1."),
            ("Priority safety rule: Any Serious Adverse Event must be escalated to CDSCO and Ethics Committee within 24 hours.", "Recorded critical 24-hour safety escalation protocol.")
        ],
        "dr_sharma": [
            ("My name is Dr. Rajesh Sharma and I am Principal Investigator at AIIA New Delhi.", "Welcome Dr. Sharma!"),
            ("I prefer summary outputs formatted in markdown bullet points with CDISC compliance codes.", "Noted your summary format preference."),
            ("I am currently working on clinical trial AIIA-2024-ASHWA for Ashwagandha in Type 2 Diabetes Mellitus.", "Recorded project AIIA-2024-ASHWA."),
            ("We enrolled 150 participants and filed ethics approval with central ethics committee under NDCT Rules 2019.", "Recorded ethics and enrollment details.")
        ]
    }

    for user_id, turns in demo_users.items():
        for user_msg, asst_msg in turns:
            lifecycle.after_agent_turn(user_id=user_id, message=user_msg, response_text=asst_msg, session_id="demo_session")
        print(f"Successfully seeded demo memory graph for user: {user_id}")

if __name__ == "__main__":
    seed_demo_data()
