"""
Digital Readiness Self-Assessment — Content Data
All assessment questions, rubrics, maturity levels, and action plans.
"""

SCORE_LABELS = {
    1: "1 — Not in Place",
    2: "2 — Emerging",
    3: "3 — Defined",
    4: "4 — Managed",
    5: "5 — Optimised",
}

SCORE_DESCRIPTIONS = {
    1: "No formal approach. Reactive, undocumented, and inconsistent.",
    2: "Initial awareness or attempts, but informal and not consistently applied.",
    3: "Documented approach in place and generally followed, but not fully optimised.",
    4: "Consistently applied, measured, and actively improved.",
    5: "Best practice, continuously improved, and used to drive competitive advantage.",
}

TIER_KEY = {
    "Sole Trader":      "st",
    "Small Business":   "sb",
    "Medium Business":  "mb",
}

PILLARS = [
    {
        "id": 1,
        "name": "Strategy & Leadership",
        "description": "Examines whether digital thinking is embedded in your business direction, decision-making, and investment planning.",
        "icon": "🎯",
        "st": [
            "Do you have a clear vision for how digital tools can help your business operate more efficiently or grow?",
            "Have you invested time or money into digital tools or training in the past 12 months?",
            "Do you regularly review whether your digital tools are working well for your business?",
            "Do you use data from your digital tools (e.g. accounting software reports) to inform your decisions?",
        ],
        "sb": [
            "Does your business have a digital strategy or plan that links technology goals to business objectives?",
            "Is there a designated person responsible for leading digital improvement in your business?",
            "Has your business allocated a specific budget for technology investment this financial year?",
            "Does your leadership team use digital data and reports regularly to make business decisions?",
        ],
        "mb": [
            "Does your organisation have a formally documented digital strategy aligned to your corporate objectives?",
            "Is there a dedicated leadership role accountable for digital transformation (e.g. CTO, Digital Lead)?",
            "Does your organisation have a structured technology investment framework with defined ROI measurement?",
            "Does your executive team use data-driven dashboards and KPIs as part of regular strategic reviews?",
        ],
        "rubric": [
            "No digital direction — technology decisions are reactive and ad hoc.",
            "Some awareness of digital opportunities, but no formal plan or budget in place.",
            "A basic plan exists and some budget is allocated, though not consistently applied.",
            "A clear strategy guides digital investment with accountability and regular review.",
            "Digital strategy integrated with business strategy, continuously reviewed, drives measurable outcomes.",
        ],
    },
    {
        "id": 2,
        "name": "Data Management & Governance",
        "description": "Assesses how your business collects, organises, protects, and uses data — including compliance with the Australian Privacy Act 1988.",
        "icon": "🗄️",
        "st": [
            "Do you store client information in a secure, organised digital system (e.g. CRM, practice management software, or secure cloud folder)?",
            "Do you know what personal data you hold about clients and how it is protected?",
            "Are you aware of your obligations under the Australian Privacy Principles (APPs)?",
            "Do you have a process for securely disposing of client data when it is no longer needed?",
        ],
        "sb": [
            "Does your business have defined processes for collecting, storing, and managing client and operational data?",
            "Is there a current, accessible Privacy Policy in place that complies with the Privacy Act 1988?",
            "Do you periodically review what data you hold, where it is stored, and who can access it?",
            "Does your business have a documented response plan for a notifiable data breach under the NDB scheme?",
        ],
        "mb": [
            "Does your organisation have a formal Data Governance Framework with defined data ownership and stewardship roles?",
            "Is there a data classification policy that categorises data by sensitivity with appropriate access controls?",
            "Do you have automated data quality monitoring, retention schedules, and lifecycle management in place?",
            "Has your organisation implemented a comprehensive Privacy Act compliance program including a tested breach response procedure?",
        ],
        "rubric": [
            "Client data stored informally (paper, personal email); no awareness of privacy obligations.",
            "Some digital storage in place but incomplete or inconsistent; basic awareness of privacy obligations.",
            "Data stored in defined systems; a Privacy Policy exists but may not be fully current or tested.",
            "Data well-managed with access controls, regular audits, and a documented breach response plan.",
            "Comprehensive data governance framework in place, regularly reviewed, fully aligned with regulatory obligations.",
        ],
    },
    {
        "id": 3,
        "name": "Technology & Tools",
        "description": "Looks at the software and platforms your business uses, how well they are integrated, and how actively you manage your technology stack.",
        "icon": "💻",
        "st": [
            "Do you use cloud-based software for your core business operations (e.g. Xero/MYOB, Google Drive, Microsoft 365)?",
            "Do your key tools share data automatically, or do you manually re-enter information between them?",
            "Are you using software that is actively maintained and supported by its vendor?",
            "Do you have a reliable, automated backup of your critical business data stored securely?",
        ],
        "sb": [
            "Has your business adopted cloud-based platforms for key functions such as practice management, document management, and accounting?",
            "Are your core business systems integrated to reduce manual data entry and duplication?",
            "Does your business have a technology plan for upgrading or adding tools in the next 12–24 months?",
            "Do you regularly review and rationalise your software subscriptions to ensure they deliver value?",
        ],
        "mb": [
            "Does your organisation have a documented technology architecture that maps all systems, integrations, and dependencies?",
            "Are critical business systems integrated via APIs or middleware, enabling automated data flow across the organisation?",
            "Do you have a formal technology lifecycle management process including vendor assessment and contract governance?",
            "Does your organisation leverage cloud-native infrastructure (SaaS, PaaS, IaaS) to support scalability and remote working?",
        ],
        "rubric": [
            "Primarily paper-based or legacy desktop tools; no cloud adoption; no backup strategy.",
            "Some cloud tools in use but fragmented; manual processes between systems; backups inconsistent.",
            "Core cloud platforms adopted; some integration in place; basic backup and update management.",
            "Well-integrated cloud ecosystem; regular software review; robust backup and disaster recovery.",
            "Fully cloud-native architecture; automated integrations; technology roadmap actively maintained.",
        ],
    },
    {
        "id": 4,
        "name": "Processes & Automation",
        "description": "Evaluates whether business processes are documented, consistently followed, and supported by automation to reduce manual effort and error.",
        "icon": "⚙️",
        "st": [
            "Do you have documented checklists or workflows for your most common tasks (e.g. client onboarding, billing, reporting)?",
            "Do you use automation to handle repetitive tasks (e.g. automated invoicing, appointment reminders, e-signature)?",
            "Do you use a digital tool to track your time, tasks, or billable work?",
            "Can you access your work systems and files securely from any location?",
        ],
        "sb": [
            "Are your core business processes documented and accessible to all relevant team members?",
            "Does your business use automation tools to reduce manual handling (e.g. workflow triggers, automated reminders, approval routing)?",
            "Do you use digital tools to manage projects, allocate tasks, and track team progress?",
            "Have you identified and prioritised your manual or paper-based processes for digital improvement?",
        ],
        "mb": [
            "Does your organisation apply a formal process improvement methodology (e.g. BPM, Lean) to your digital transformation program?",
            "Are high-volume or repetitive processes automated using workflow automation, RPA, or AI-assisted tools?",
            "Is there a centralised project and workflow management platform used consistently across the organisation?",
            "Do you measure and report on process efficiency metrics (e.g. cycle time, error rate, throughput) to drive continuous improvement?",
        ],
        "rubric": [
            "No documented processes; tasks completed from memory; no automation; paper-dependent.",
            "Some informal processes documented; limited automation; basic task tracking in place.",
            "Core processes documented and generally followed; some automation deployed; digital project tracking in use.",
            "Processes well-documented and regularly reviewed; significant automation in place; efficiency metrics tracked.",
            "Continuous improvement culture; advanced automation; data-driven optimisation across all workflows.",
        ],
    },
    {
        "id": 5,
        "name": "People & Capability",
        "description": "Assesses the digital skills of you and your team, the training and support available, and how well your business builds digital confidence over time.",
        "icon": "👥",
        "st": [
            "Do you feel confident and competent using the digital tools your business relies on?",
            "Have you completed any relevant digital skills training or professional development in the past 12 months?",
            "Do you actively keep up to date with technology trends relevant to your profession?",
            "Do you have access to reliable IT support when you need help?",
        ],
        "sb": [
            "Have you assessed the digital skill levels of your team members and identified gaps?",
            "Does your business provide access to digital training or upskilling opportunities for team members?",
            "Is digital proficiency considered when hiring new staff or engaging contractors?",
            "Does your team have access to timely IT support with a clear escalation path for technical issues?",
        ],
        "mb": [
            "Does your organisation have a formal digital capability framework with role-specific competency standards?",
            "Is there a structured digital learning and development program aligned to your strategic digital priorities?",
            "Do you measure and track digital capability uplift across the organisation over time?",
            "Does your organisation have a dedicated IT support function with documented service levels (SLAs)?",
        ],
        "rubric": [
            "Digital skills are poor or inconsistent; no training; no access to IT support.",
            "Basic digital skills in place; occasional informal training; ad hoc IT support.",
            "Adequate digital skills for current needs; some structured training available; IT support accessible.",
            "Strong digital capability; regular training program; IT support with clear escalation paths.",
            "High-performing digital culture; formal capability framework; continuous learning; mature IT support model.",
        ],
    },
    {
        "id": 6,
        "name": "Client Experience & Digital Engagement",
        "description": "Examines how digitally accessible and engaging your services are to clients — from your online presence to how you communicate and gather feedback.",
        "icon": "🤝",
        "st": [
            "Do clients have at least one digital option to engage with you (e.g. online booking, e-signature, video meeting, client portal)?",
            "Do you have a current, professional website or online presence that accurately represents your services?",
            "Do you use digital tools to communicate with clients proactively (e.g. email updates, SMS reminders, video platforms)?",
            "Do you use any digital method to gather client feedback (e.g. online survey, Google review)?",
        ],
        "sb": [
            "Does your business offer clients self-service digital options (e.g. client portal, online bookings, electronic document signing)?",
            "Is your website current, mobile-responsive, and accessible to potential and existing clients?",
            "Does your business have a consistent digital communication approach for client engagement and retention?",
            "Do you use client data to personalise or improve your services and communications?",
        ],
        "mb": [
            "Does your organisation have a formal digital client experience (CX) strategy with defined service standards and client journey mapping?",
            "Do you use a CRM system to manage client relationships, track all interactions, and measure service delivery KPIs?",
            "Does your organisation deliver an integrated multi-channel digital client experience (portal, e-signature, video, app)?",
            "Do you use client data analytics to proactively identify service improvement opportunities and measure client satisfaction?",
        ],
        "rubric": [
            "No digital client touchpoints; communication exclusively by phone or in person; no online presence.",
            "Basic online presence (website); limited digital client interaction; no structured feedback collection.",
            "Some digital service options available (e.g. e-signature, video); website maintained; basic digital communication.",
            "Multiple digital client touchpoints integrated; CRM in use; proactive communication; client feedback collected.",
            "Exceptional digital client experience; fully integrated CX strategy; data-driven service improvement.",
        ],
    },
    {
        "id": 7,
        "name": "Security & Compliance",
        "description": "Evaluates your cybersecurity posture, incident preparedness, and awareness of regulatory obligations aligned with ACSC guidance.",
        "icon": "🔒",
        "st": [
            "Do you use strong, unique passwords and multi-factor authentication (MFA) on your key business accounts?",
            "Are your devices (laptop, phone) protected with passwords/PINs and kept up to date with operating system updates?",
            "Do you have a secure, separate backup of your important business data stored in a different location?",
            "Are you aware of common cyber threats such as phishing emails, and do you know how to respond?",
        ],
        "sb": [
            "Does your business have documented cybersecurity procedures or a basic security policy covering all team members?",
            "Is multi-factor authentication (MFA) enabled on all critical business systems and cloud accounts?",
            "Do you provide cybersecurity awareness training for your team at least annually?",
            "Does your business hold cyber liability insurance and have a basic incident response plan?",
        ],
        "mb": [
            "Does your organisation have a formally documented information security framework aligned to Australian standards (e.g. ASD Essential Eight)?",
            "Do you conduct regular vulnerability assessments, penetration testing, or third-party security audits?",
            "Is there a dedicated security function (internal or managed service) providing continuous monitoring and response capability?",
            "Does your organisation have a tested cyber incident response plan and a business continuity plan?",
        ],
        "rubric": [
            "No security measures in place; weak passwords; no backups; no awareness of cyber threats.",
            "Basic security measures (antivirus, some password hygiene); irregular backups; limited awareness.",
            "MFA enabled; regular updates applied; secure backups; basic cyber awareness in place.",
            "Security policy documented; MFA across all systems; annual training; cyber insurance held; incident plan exists.",
            "Comprehensive security framework (ASD Essential Eight aligned); regular testing; dedicated security function; tested response plan.",
        ],
    },
]

MATURITY_LEVELS = [
    {
        "level": 1,
        "label": "Digital Beginner",
        "range": "1.0 – 1.9",
        "color": "#FCE4D6",
        "text_color": "#C55A11",
        "badge_bg": "#ED7D31",
        "description": (
            "Your business is at the start of its digital journey. Most processes are manual or paper-based, "
            "and digital tools are used informally or inconsistently. Data security and privacy obligations "
            "may not yet be fully understood."
        ),
    },
    {
        "level": 2,
        "label": "Digital Explorer",
        "range": "2.0 – 2.9",
        "color": "#FFF2CC",
        "text_color": "#7F6000",
        "badge_bg": "#BF8F00",
        "description": (
            "Your business has made initial steps into digital, but tools are fragmented and processes are "
            "inconsistent. There is growing awareness of digital opportunities, but limited strategic "
            "direction or formal planning."
        ),
    },
    {
        "level": 3,
        "label": "Digital Adopter",
        "range": "3.0 – 3.4",
        "color": "#DEEAF1",
        "text_color": "#1F3864",
        "badge_bg": "#2E75B6",
        "description": (
            "Your business uses digital tools consistently and has established core processes. You have "
            "built a solid digital foundation, but there are opportunities to better integrate systems, "
            "automate more tasks, and strengthen security."
        ),
    },
    {
        "level": 4,
        "label": "Digital Practitioner",
        "range": "3.5 – 4.4",
        "color": "#E2EFDA",
        "text_color": "#375623",
        "badge_bg": "#70AD47",
        "description": (
            "Your business has a mature digital foundation with integrated systems, clear processes, and "
            "active digital engagement with clients. The focus now is on optimising your investments and "
            "measuring the value they deliver."
        ),
    },
    {
        "level": 5,
        "label": "Digital Leader",
        "range": "4.5 – 5.0",
        "color": "#EAD1DC",
        "text_color": "#7030A0",
        "badge_bg": "#7030A0",
        "description": (
            "Your business is at the forefront of digital maturity in professional services. Digital is "
            "embedded in your strategy, culture, and client experience. The focus is on maintaining "
            "competitive advantage and driving continuous innovation."
        ),
    },
]

TOP_ACTIONS = {
    1: [
        "Adopt a cloud accounting platform — Xero or MYOB are recommended for Australian professional services.",
        "Set up Microsoft 365 or Google Workspace for secure file storage, email, and collaboration.",
        "Visit cyber.gov.au and download the ACSC Small Business Cyber Security Guide (free).",
        "Review your Privacy Act obligations at oaic.gov.au/privacy — particularly whether you need a Privacy Policy.",
        "Pick ONE manual process and find a digital tool to replace it within the next 30 days.",
        "Attend a free digital skills workshop via business.gov.au or your industry association.",
    ],
    2: [
        "Enable MFA on ALL business accounts today — it is free, takes 10 minutes, and is one of the highest-impact security actions you can take.",
        "Document your five most common business processes — this creates the foundation for future automation.",
        "Create or update your Privacy Policy to comply with the Privacy Act 1988.",
        "Consolidate fragmented tools into an integrated cloud ecosystem (e.g. Microsoft 365 + practice management platform).",
        "Allocate a modest annual digital budget — even $1,000–$3,000 per year creates real momentum.",
        "Explore free resources at digitalskillsorg.com.au for training options.",
    ],
    3: [
        "Identify your top three integration opportunities between your core tools to eliminate duplication.",
        "Introduce at least one new automation this quarter (e.g. automated invoicing, e-signature workflows, or appointment reminders).",
        "Develop a basic cybersecurity plan aligned to the ACSC top four mitigation strategies.",
        "Build a one-page 12-month digital roadmap with three to five measurable goals.",
        "Set up a simple client feedback process (e.g. a post-engagement survey using Google Forms or SurveyMonkey).",
        "Review your team's digital training needs and identify one course or certification to pursue this year.",
    ],
    4: [
        "Develop a two-year digital roadmap with measurable outcomes and a structured investment plan.",
        "Implement a structured client feedback loop — target Net Promoter Score (NPS) or equivalent.",
        "Explore AI-assisted tools relevant to your profession (e.g. document drafting, analytics, intelligent scheduling).",
        "Conduct an annual cybersecurity audit or engage a managed security provider for ongoing monitoring.",
        "Invest in structured digital capability development — consider industry certifications or vendor training programs.",
        "Benchmark your digital maturity against industry peers using the Digital Solutions Program (business.gov.au).",
    ],
    5: [
        "Formalise a digital innovation program with dedicated time and budget for exploring emerging technologies.",
        "Explore advanced capabilities: AI-driven analytics, robotic process automation (RPA), or intelligent client portals.",
        "Review your security posture against the ASD Essential Eight Maturity Model — target Maturity Level 2 or above.",
        "Develop knowledge management plans to ensure digital capability is embedded across the organisation.",
        "Position digital leadership as a market differentiator — communicate your capabilities to clients and prospects.",
        "Share insights with industry peers — contribute to association working groups or publish case studies.",
    ],
}

RESOURCES = [
    ("ACSC Small Business Cyber Security Guide", "https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/small-business-cyber-security-guide"),
    ("ASD Essential Eight Framework", "https://www.asd.gov.au/resources/essential-eight"),
    ("Office of the Australian Information Commissioner (OAIC)", "https://www.oaic.gov.au/privacy"),
    ("Notifiable Data Breaches Scheme", "https://www.oaic.gov.au/privacy/notifiable-data-breaches"),
    ("Digital Solutions Program — Business.gov.au", "https://business.gov.au/grants-and-programs/digital-solutions-australian-small-business-advisory-service"),
    ("Digital Skills Organisation", "https://www.digitalskillsorg.com.au"),
]


def get_maturity_level(avg_score: float) -> dict:
    """Return the maturity level dict for a given average score."""
    if avg_score < 2.0:
        return MATURITY_LEVELS[0]
    elif avg_score < 3.0:
        return MATURITY_LEVELS[1]
    elif avg_score < 3.5:
        return MATURITY_LEVELS[2]
    elif avg_score < 4.5:
        return MATURITY_LEVELS[3]
    else:
        return MATURITY_LEVELS[4]


def compute_results(scores: dict) -> dict:
    """
    scores: {pillar_id (1–7): [s1, s2, s3, s4]}
    Returns dict with per-pillar scores, total, average, maturity level.
    """
    pillar_totals = {}
    pillar_avgs = {}
    all_scores = []

    for p in PILLARS:
        pid = p["id"]
        vals = [v for v in scores.get(pid, []) if v is not None]
        if vals:
            total = sum(vals)
            avg = total / len(vals)
        else:
            total = 0
            avg = 0.0
        pillar_totals[pid] = total
        pillar_avgs[pid] = round(avg, 2)
        all_scores.extend(vals)

    total_score = sum(all_scores)
    avg_score = round(total_score / len(all_scores), 2) if all_scores else 0.0
    maturity = get_maturity_level(avg_score)

    return {
        "pillar_totals": pillar_totals,
        "pillar_avgs": pillar_avgs,
        "total_score": total_score,
        "avg_score": avg_score,
        "maturity": maturity,
        "answered": len(all_scores),
    }
