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
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 1 — Strategy & Leadership
    # ─────────────────────────────────────────────────────────────────────────
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
        "st_labels": [
            [
                "No vision — digital tools are used as they come up, with no overall direction",
                "Vague ideas about digital potential but nothing written down or acted on",
                "A basic direction is in place and some tools have been chosen deliberately",
                "Clear vision guides which tools I use, with regular check-ins on whether they're working",
                "A purposeful digital strategy drives my business decisions and measurable growth",
            ],
            [
                "No investment — using the same tools I've always had, with no new learning",
                "Minor ad-hoc spend on one tool or one course, not planned in advance",
                "Deliberately invested in at least one new tool or training with a specific goal",
                "Regular, planned investment in tools and skills — budgeted and reviewed",
                "Strategic investment with tracked outcomes, feeding into a continuous improvement cycle",
            ],
            [
                "Never reviewed — tools are used because they were set up, not because they're optimal",
                "Occasionally check in informally, usually when something isn't working",
                "Review tools at least once a year and make changes based on what I find",
                "Scheduled reviews with clear criteria — tools are updated, dropped, or added based on evidence",
                "Continuous evaluation with performance metrics guiding every tool decision",
            ],
            [
                "No — decisions are made from memory or gut feel",
                "Occasionally look at reports but don't act on them systematically",
                "Regularly consult reports for key decisions like pricing, time allocation, or cash flow",
                "Data from multiple tools is actively used to drive decisions week-to-week",
                "Data-driven decision-making is embedded — dashboards and metrics guide strategy",
            ],
        ],
        "sb": [
            "Does your business have a digital strategy or plan that links technology goals to business objectives?",
            "Is there a designated person responsible for leading digital improvement in your business?",
            "Has your business allocated a specific budget for technology investment this financial year?",
            "Does your leadership team use digital data and reports regularly to make business decisions?",
        ],
        "sb_labels": [
            [
                "No digital strategy — technology is purchased reactively as problems arise",
                "Informal ideas about digital direction, but nothing documented or shared with the team",
                "A basic plan exists linking some technology goals to business needs, though not fully formalised",
                "A documented digital strategy is in place, reviewed annually, and guides investment decisions",
                "Digital strategy fully integrated with business planning, with defined KPIs and regular review",
            ],
            [
                "No one is responsible — digital decisions are made ad hoc by whoever is available",
                "Someone informally handles tech issues, but it's not a defined part of their role",
                "One person is nominally responsible for digital, though without a formal mandate or time allocation",
                "A designated role with clear accountability for digital improvement is in place",
                "Digital leadership is embedded in the organisational structure with defined outcomes and reporting",
            ],
            [
                "No budget — technology is purchased from general funds when urgent",
                "A rough estimate exists but no formal budget line",
                "A specific technology budget is allocated, though not always fully spent or tracked",
                "A defined technology budget with clear categories is set, tracked, and reported on",
                "Technology investment is strategically planned with ROI measurement and rolling multi-year forecasting",
            ],
            [
                "No — decisions are based on experience and instinct, not data",
                "Reports are generated but rarely reviewed or acted on",
                "Key reports (e.g. financials, utilisation) are reviewed in leadership meetings",
                "Data from multiple systems informs regular leadership decisions across all business areas",
                "A live dashboard provides real-time business intelligence used to drive strategy and performance",
            ],
        ],
        "mb": [
            "Does your organisation have a formally documented digital strategy aligned to your corporate objectives?",
            "Is there a dedicated leadership role accountable for digital transformation (e.g. CTO, Digital Lead)?",
            "Does your organisation have a structured technology investment framework with defined ROI measurement?",
            "Does your executive team use data-driven dashboards and KPIs as part of regular strategic reviews?",
        ],
        "mb_labels": [
            [
                "No documented digital strategy — digital initiatives are project-based and disconnected",
                "A draft or informal strategy exists but is not approved, communicated, or linked to corporate goals",
                "A documented digital strategy exists and is referenced in planning, though not consistently applied",
                "An approved digital strategy is actively implemented, reviewed annually, and linked to corporate KPIs",
                "Digital strategy is integrated into enterprise planning, board-reviewed, and drives measurable outcomes",
            ],
            [
                "No dedicated role — digital is managed alongside other responsibilities without accountability",
                "Digital responsibility is assigned informally to a senior leader without a formal mandate",
                "A defined digital leadership role exists but is under-resourced or lacks executive authority",
                "A dedicated leader (CTO/Digital Lead) has a clear mandate, budget, and executive sponsorship",
                "Digital leadership is embedded at C-suite level with a formal charter, team, and board reporting",
            ],
            [
                "No framework — technology investments are approved informally case-by-case",
                "Basic investment approval process exists but ROI is not defined or tracked",
                "A structured approval process is in place for major investments, with some ROI tracking",
                "A formal investment framework with defined criteria, governance, and post-implementation review",
                "Technology investment is governed by a portfolio framework with continuous ROI measurement and optimisation",
            ],
            [
                "No dashboards — strategic reviews rely on ad hoc reports or verbal updates",
                "Some data presented at reviews but inconsistently and without defined KPIs",
                "Key KPIs are tracked and presented at regular reviews using standard reports",
                "Dashboards provide real-time business intelligence used consistently in strategic decision-making",
                "Integrated enterprise analytics platform supports all strategic reviews with predictive capability",
            ],
        ],
        "rubric": [
            "No digital direction — technology decisions are reactive and ad hoc.",
            "Some awareness of digital opportunities, but no formal plan or budget in place.",
            "A basic plan exists and some budget is allocated, though not consistently applied.",
            "A clear strategy guides digital investment with accountability and regular review.",
            "Digital strategy integrated with business strategy, continuously reviewed, drives measurable outcomes.",
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 2 — Data Management & Governance
    # ─────────────────────────────────────────────────────────────────────────
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
        "st_labels": [
            [
                "Client info stored in paper files, personal email, or a disorganised mix of locations",
                "Some digital storage in use but inconsistent — information is spread across multiple places",
                "Most client information is in one digital system, though not fully organised or consistently maintained",
                "All client information is stored in a secure, organised digital system with regular upkeep",
                "A purpose-built CRM or practice management system is fully utilised with complete, accurate client records",
            ],
            [
                "No clear picture of what data I hold or where it is",
                "Broadly aware of what data exists, but not where it's stored or how it's protected",
                "Can identify the main categories of client data held and the systems they're in",
                "Clear inventory of client data with documented protections and access controls in place",
                "Comprehensive data register maintained, regularly reviewed, with robust protection for all personal data",
            ],
            [
                "Not aware of the APPs or any privacy obligations",
                "Heard of the Privacy Act but unfamiliar with specific obligations that apply to my business",
                "Broadly aware of my key APP obligations (e.g. collection, storage, disclosure)",
                "Well-informed about all relevant APPs and have taken steps to comply",
                "Fully compliant with all applicable APPs, with documented policies and regular reviews to stay current",
            ],
            [
                "No process — data is deleted (or not) informally with no policy",
                "Ad hoc deletion when I think of it, but no defined retention timeframe",
                "A basic approach to data disposal exists (e.g. delete after X years) but not consistently followed",
                "A documented retention and disposal process is in place and followed for all client data",
                "Automated retention scheduling with secure disposal protocols aligned to legal obligations",
            ],
        ],
        "sb": [
            "Does your business have defined processes for collecting, storing, and managing client and operational data?",
            "Is there a current, accessible Privacy Policy in place that complies with the Privacy Act 1988?",
            "Do you periodically review what data you hold, where it is stored, and who can access it?",
            "Does your business have a documented response plan for a notifiable data breach under the NDB scheme?",
        ],
        "sb_labels": [
            [
                "No defined processes — data handling is ad hoc and varies by staff member",
                "Informal practices exist but are not documented or consistently followed",
                "Basic data management processes are documented and generally followed for key data types",
                "Defined, documented processes for all major data types are consistently applied and periodically reviewed",
                "Mature data management practices across the full data lifecycle, regularly audited and improved",
            ],
            [
                "No Privacy Policy exists",
                "A Privacy Policy exists but is outdated, incomplete, or not publicly accessible",
                "A Privacy Policy is in place and accessible to clients, though may not reflect all current obligations",
                "A current, legally reviewed Privacy Policy is in place, accessible on the website, and reviewed annually",
                "Comprehensive Privacy Policy aligned to all APPs, proactively communicated to clients, updated whenever obligations change",
            ],
            [
                "No review ever conducted — no visibility over data holdings",
                "Occasional informal check-ins but no structured review process",
                "An annual data review takes place covering most systems and data types",
                "Regular structured reviews cover all data categories, storage locations, and access rights",
                "Continuous data governance with automated monitoring, regular access audits, and real-time visibility",
            ],
            [
                "No plan exists — a breach would be handled reactively with no defined process",
                "Aware of the NDB scheme but no formal plan in place",
                "A basic breach response process exists but is not formally documented or tested",
                "A documented NDB-compliant breach response plan is in place and staff are aware of it",
                "A tested, regularly reviewed breach response plan with clear roles, timelines, and OAIC notification procedures",
            ],
        ],
        "mb": [
            "Does your organisation have a formal Data Governance Framework with defined data ownership and stewardship roles?",
            "Is there a data classification policy that categorises data by sensitivity with appropriate access controls?",
            "Do you have automated data quality monitoring, retention schedules, and lifecycle management in place?",
            "Has your organisation implemented a comprehensive Privacy Act compliance program including a tested breach response procedure?",
        ],
        "mb_labels": [
            [
                "No data governance framework — data ownership is undefined and inconsistent",
                "Data ownership informally assigned but no formal framework or stewardship roles",
                "A basic data governance framework is documented with some assigned ownership roles",
                "A formal framework with defined data owners, stewards, and governance processes is in place",
                "Enterprise data governance programme with active oversight, regular reporting, and continuous maturity improvement",
            ],
            [
                "No classification policy — all data is treated the same regardless of sensitivity",
                "Informal awareness of data sensitivity but no formal classification system",
                "A basic classification scheme exists (e.g. Public/Internal/Confidential) with some access controls",
                "A defined classification policy with consistent labelling and role-based access controls across systems",
                "Automated data classification with dynamic access management and policy enforcement across all platforms",
            ],
            [
                "No data quality monitoring or lifecycle management — data accumulates without review",
                "Manual data quality checks performed occasionally; retention is informal",
                "Some data quality processes exist; a basic retention schedule is in place for key data types",
                "Automated data quality monitoring with alerts; retention schedules enforced across major systems",
                "End-to-end data lifecycle management with automated quality, retention, and archival across all systems",
            ],
            [
                "No compliance program — privacy obligations are not formally managed",
                "Basic awareness of Privacy Act obligations but no structured compliance program",
                "Key Privacy Act obligations are addressed; a breach procedure exists but has not been tested",
                "A comprehensive compliance program is in place with documented procedures and annual training",
                "Mature privacy compliance programme with regular independent audits, tested breach response, and proactive regulatory engagement",
            ],
        ],
        "rubric": [
            "Client data stored informally (paper, personal email); no awareness of privacy obligations.",
            "Some digital storage in place but incomplete or inconsistent; basic awareness of privacy obligations.",
            "Data stored in defined systems; a Privacy Policy exists but may not be fully current or tested.",
            "Data well-managed with access controls, regular audits, and a documented breach response plan.",
            "Comprehensive data governance framework in place, regularly reviewed, fully aligned with regulatory obligations.",
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 3 — Technology & Tools
    # ─────────────────────────────────────────────────────────────────────────
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
        "st_labels": [
            [
                "No cloud tools — working from desktop software, paper, or personal email",
                "Using one or two cloud tools informally, but core operations still largely offline",
                "Core business functions (e.g. accounting, file storage) are handled in cloud-based tools",
                "All key operations run on cloud platforms that are well set up and regularly updated",
                "Fully cloud-based operation with best-fit tools for every function, regularly reviewed for value",
            ],
            [
                "Everything is re-entered manually — no tools talk to each other",
                "Mostly manual, with one or two basic integrations (e.g. bank feed in accounting software)",
                "A few key tools are integrated, reducing some re-entry, though manual steps remain",
                "Core tools are integrated with automated data flow — minimal manual re-entry required",
                "Fully integrated ecosystem with seamless automated data flow across all tools",
            ],
            [
                "Using outdated or unsupported software with no clear update path",
                "Most software is current but some tools are outdated or on legacy plans",
                "Core tools are maintained and updated, though a few may be past their best-fit period",
                "All software is current, vendor-supported, and updated promptly when new versions are released",
                "Proactive software lifecycle management — tools are reviewed, updated, and replaced on a planned schedule",
            ],
            [
                "No backup — data exists only on one device or location",
                "Occasional manual backups, but irregular and not stored securely offsite",
                "Regular backups are in place for most data, stored separately from the primary location",
                "Automated, scheduled backups of all critical data to a secure offsite or cloud location",
                "Comprehensive backup strategy with automated testing, offsite storage, and documented recovery procedures",
            ],
        ],
        "sb": [
            "Has your business adopted cloud-based platforms for key functions such as practice management, document management, and accounting?",
            "Are your core business systems integrated to reduce manual data entry and duplication?",
            "Does your business have a technology plan for upgrading or adding tools in the next 12–24 months?",
            "Do you regularly review and rationalise your software subscriptions to ensure they deliver value?",
        ],
        "sb_labels": [
            [
                "No cloud adoption — operating on desktop software, shared drives, or paper-based processes",
                "One or two cloud tools in use, but most functions still rely on non-cloud solutions",
                "Cloud tools adopted for core functions, though coverage is incomplete across some areas",
                "Cloud platforms used across all key business functions with consistent staff adoption",
                "Fully cloud-native operation with best-fit platforms across all functions, actively maintained and governed",
            ],
            [
                "No integration — all data is manually transferred between systems",
                "One or two basic integrations in place (e.g. bank feeds); most data transfer is still manual",
                "Key systems share data through integrations or automation, reducing the most common manual tasks",
                "Core systems are well-integrated with automated data flows and minimal duplication",
                "Seamless system integration across all platforms with real-time data synchronisation and zero duplication",
            ],
            [
                "No technology plan — tools are added only when an urgent problem arises",
                "Informal ideas about future tools but nothing documented or prioritised",
                "A basic technology plan exists with a few planned upgrades or additions",
                "A documented technology roadmap covering 12–24 months, reviewed regularly with budget allocated",
                "A strategic technology roadmap tied to business objectives, with vendor assessments and approved investment",
            ],
            [
                "No review — subscriptions continue regardless of whether they're being used",
                "Occasional informal check on costs but no structured review process",
                "Annual review of subscriptions with some cancellations or changes made",
                "Regular structured subscription review with clear value criteria — unused tools are removed promptly",
                "Continuous subscription management with defined ROI criteria, usage tracking, and procurement governance",
            ],
        ],
        "mb": [
            "Does your organisation have a documented technology architecture that maps all systems, integrations, and dependencies?",
            "Are critical business systems integrated via APIs or middleware, enabling automated data flow across the organisation?",
            "Do you have a formal technology lifecycle management process including vendor assessment and contract governance?",
            "Does your organisation leverage cloud-native infrastructure (SaaS, PaaS, IaaS) to support scalability and remote working?",
        ],
        "mb_labels": [
            [
                "No architecture documentation — systems and integrations are undocumented and ad hoc",
                "Some informal diagrams or documentation exist but are incomplete and out of date",
                "A basic architecture document exists covering major systems, though not all integrations are mapped",
                "A maintained architecture map covers all systems, integrations, and dependencies, reviewed regularly",
                "Enterprise architecture is formally governed, regularly updated, and used to guide all technology decisions",
            ],
            [
                "No API or middleware integration — all data exchange is manual",
                "A few point-to-point integrations in place; most data exchange remains manual",
                "Key systems are integrated via APIs or middleware, with automated flow for priority processes",
                "Comprehensive integration across critical systems with automated, reliable data flows and monitoring",
                "Enterprise integration platform enables real-time automated data flow across all systems with centralised governance",
            ],
            [
                "No lifecycle management — tools are purchased and forgotten until they break or expire",
                "Vendor relationships and contracts managed informally with no formal review cycle",
                "A basic review process for major vendors and contracts is in place",
                "A formal lifecycle management process covers all major systems with scheduled reviews and renegotiation",
                "Comprehensive technology lifecycle programme with vendor scorecards, contract governance, and strategic roadmapping",
            ],
            [
                "No cloud infrastructure — operating on on-premises servers or legacy systems",
                "Limited cloud adoption — some SaaS tools in use but infrastructure remains largely on-premises",
                "Key business functions run on cloud platforms with moderate support for remote working",
                "Cloud-first strategy with SaaS/PaaS adoption across all major functions and full remote working capability",
                "Fully cloud-native infrastructure with elastic scalability, active cost optimisation, and enterprise-grade resilience",
            ],
        ],
        "rubric": [
            "Primarily paper-based or legacy desktop tools; no cloud adoption; no backup strategy.",
            "Some cloud tools in use but fragmented; manual processes between systems; backups inconsistent.",
            "Core cloud platforms adopted; some integration in place; basic backup and update management.",
            "Well-integrated cloud ecosystem; regular software review; robust backup and disaster recovery.",
            "Fully cloud-native architecture; automated integrations; technology roadmap actively maintained.",
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 4 — Processes & Automation
    # ─────────────────────────────────────────────────────────────────────────
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
        "st_labels": [
            [
                "No documentation — all tasks are done from memory with no consistent process",
                "Mental checklists or informal notes exist but nothing formally written down",
                "Written checklists or process guides exist for one or two key tasks",
                "Documented workflows cover most common tasks and are regularly followed and updated",
                "Comprehensive process documentation for all regular tasks, reviewed and refined continuously",
            ],
            [
                "No automation — all tasks including invoicing and reminders are done manually",
                "One or two automated features in use (e.g. bank feed or calendar reminders) but nothing systematic",
                "A few deliberate automation tools in place (e.g. auto-invoicing, e-signature) saving meaningful time",
                "Automation handles most routine tasks, significantly reducing manual effort",
                "Comprehensive automation across all repetitive tasks with continuous optimisation for time and accuracy",
            ],
            [
                "No tracking — time and tasks managed from memory or paper notes",
                "Occasional tracking using basic tools (e.g. spreadsheet or notes app) but not consistently",
                "A digital tool is used regularly to track time or tasks for billing and productivity",
                "All billable time and tasks tracked consistently in a digital tool with regular review and reporting",
                "Integrated time and task tracking feeding directly into billing, reporting, and business performance analysis",
            ],
            [
                "No — work requires being in a specific location or using a specific device",
                "Can access some files remotely but systems are largely location-dependent",
                "Most key systems and files are accessible remotely with basic security measures",
                "All work systems accessible securely from any location via cloud tools and MFA",
                "Fully location-independent working environment with enterprise-grade security and seamless remote access",
            ],
        ],
        "sb": [
            "Are your core business processes documented and accessible to all relevant team members?",
            "Does your business use automation tools to reduce manual handling (e.g. workflow triggers, automated reminders, approval routing)?",
            "Do you use digital tools to manage projects, allocate tasks, and track team progress?",
            "Have you identified and prioritised your manual or paper-based processes for digital improvement?",
        ],
        "sb_labels": [
            [
                "No documentation — processes exist only in people's heads",
                "Some processes written down informally; not consistently accessible to all staff",
                "Core processes documented and stored centrally, though not always kept up to date",
                "Comprehensive process documentation maintained in a shared system and regularly reviewed",
                "A living process library accessible to all staff, version-controlled, and continuously improved",
            ],
            [
                "No automation — all workflows rely on manual action and follow-up",
                "One or two basic automations in place (e.g. email reminders) but ad hoc",
                "Several deliberate automations reduce manual work across key workflows",
                "Automation is systematically applied across most workflows with measurable efficiency gains",
                "Advanced workflow automation with triggers, routing, and approvals across all major processes",
            ],
            [
                "No digital project management — tasks assigned verbally or via email with no tracking",
                "Basic tracking via spreadsheets or shared docs, but inconsistent",
                "A project management tool is used for some projects, though not consistently across the team",
                "All projects and tasks managed in a shared digital tool with consistent visibility for the whole team",
                "Integrated project management platform used consistently across all work with real-time progress reporting",
            ],
            [
                "No mapping done — no visibility of which processes are manual or how to improve them",
                "Aware of a few inefficient processes but no formal review or prioritisation",
                "Key manual processes have been identified and some improvements are planned or underway",
                "A formal process review has been completed with a prioritised roadmap for digital improvement",
                "Continuous process improvement programme with regular reviews, quantified benefits, and tracked outcomes",
            ],
        ],
        "mb": [
            "Does your organisation apply a formal process improvement methodology (e.g. BPM, Lean) to your digital transformation program?",
            # ✏️ Sandra: explain RPA in question
            "Are high-volume or repetitive processes automated using workflow automation, RPA (Robotic Process Automation), or AI-assisted tools?",
            "Is there a centralised project and workflow management platform used consistently across the organisation?",
            "Do you measure and report on process efficiency metrics (e.g. cycle time, error rate, throughput) to drive continuous improvement?",
        ],
        "mb_labels": [
            [
                "No methodology — digital improvements are reactive and unstructured",
                "Some process improvement awareness but no formal methodology applied",
                "A recognised methodology (e.g. BPM, Lean) is selectively applied to key improvement projects",
                "A formal methodology is consistently applied to digital transformation with trained practitioners",
                "Enterprise-wide process improvement culture with certified practitioners and continuous optimisation across all functions",
            ],
            [
                "No automation of high-volume processes — handled entirely by manual effort",
                "Basic automation in isolated areas (e.g. scheduled reports) but RPA or AI not in use",
                "Workflow automation deployed for some high-volume processes with measurable efficiency gains",
                "RPA or AI-assisted automation applied across most high-volume processes with tracked ROI",
                "Advanced automation (RPA + AI) enterprise-wide with a continuous pipeline of automation opportunities",
            ],
            [
                "No centralised platform — project management is fragmented across teams and tools",
                "A tool exists but adoption is inconsistent and data quality is poor",
                "A centralised platform is in use across most teams with reasonable consistency",
                "One platform used consistently across the organisation with real-time visibility and governance",
                "Integrated enterprise work management platform driving visibility, accountability, and performance at all levels",
            ],
            [
                "No process metrics tracked — improvement is based on opinion, not data",
                "Some informal tracking but no regular reporting or action taken on findings",
                "Key process metrics tracked and reported periodically with some improvement actions",
                "Defined process KPIs tracked regularly with formal reporting and improvement targets",
                "Real-time process intelligence with automated dashboards driving continuous, data-led optimisation",
            ],
        ],
        "rubric": [
            "No documented processes; tasks completed from memory; no automation; paper-dependent.",
            "Some informal processes documented; limited automation; basic task tracking in place.",
            "Core processes documented and generally followed; some automation deployed; digital project tracking in use.",
            "Processes well-documented and regularly reviewed; significant automation in place; efficiency metrics tracked.",
            "Continuous improvement culture; advanced automation; data-driven optimisation across all workflows.",
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 5 — People & Capability
    # ─────────────────────────────────────────────────────────────────────────
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
        "st_labels": [
            [
                "Not confident — regularly struggle with the tools I need to use for my work",
                "Manage the basics but often uncertain; rely on help or workarounds frequently",
                "Comfortable with day-to-day use of my core tools; occasionally need guidance for new features",
                "Confident and proficient across all tools I use; quick to learn new functionality",
                "Expert-level competence; able to maximise the value of every tool and help others do the same",
            ],
            [
                "No training in the past 12 months",
                "Picked up skills informally (YouTube, trial and error) but no structured learning",
                "Completed at least one structured course, webinar, or training relevant to my business tools",
                "Regular training (multiple courses or events) completed and applied to my work",
                "Ongoing professional development programme including certifications, peer learning, and skill application",
            ],
            [
                "No effort to stay current — not sure what's changing in my field",
                "Occasionally read about new tools or trends when something comes up in conversation",
                "Regularly read industry publications or follow relevant technology sources",
                "Actively monitor technology trends and evaluate new tools against my business needs",
                "Proactive approach to technology awareness — attend events, participate in communities, and experiment with new tools",
            ],
            [
                "No IT support — problems are either solved by searching online or left unresolved",
                "Occasional help from a friend, family member, or online forums — unreliable and slow",
                "Access to a trusted IT contact (e.g. freelancer or vendor support) for most issues",
                "Reliable IT support available within a reasonable timeframe with clear escalation for urgent issues",
                "Proactive IT support relationship with preventative maintenance, fast response, and trusted advice on new technology",
            ],
        ],
        "sb": [
            "Have you assessed the digital skill levels of your team members and identified gaps?",
            "Does your business provide access to digital training or upskilling opportunities for team members?",
            "Is digital proficiency considered when hiring new staff or engaging contractors?",
            "Does your team have access to timely IT support with a clear escalation path for technical issues?",
        ],
        "sb_labels": [
            [
                "No assessment done — no visibility of team digital capabilities or gaps",
                "Informally aware of some gaps but no structured assessment conducted",
                "An informal skills review has been done and key gaps have been identified",
                "A structured digital skills assessment has been completed for all team members with documented gaps",
                "Regular digital capability assessment with benchmarking against role requirements and industry standards",
            ],
            [
                "No training provided — staff learn on their own if they want to",
                "Training available if requested, but not proactively offered or funded",
                "Some training is provided (e.g. tool-specific onboarding, one-off courses) for key team members",
                "A structured training programme is in place with regular opportunities for all team members",
                "A comprehensive digital learning programme with individual development plans and tracked outcomes",
            ],
            [
                "Not considered — digital skills are not part of hiring criteria",
                "Occasionally mentioned during hiring but not formally assessed",
                "Digital proficiency is listed as a requirement in role descriptions and discussed at interview",
                "Digital capability is formally assessed during hiring for all roles with defined minimum standards",
                "Digital competency frameworks guide all recruitment and onboarding with role-specific assessments and plans",
            ],
            [
                "No IT support — staff resolve issues themselves or wait for problems to fix themselves",
                "Ad hoc IT help available but no defined process or expected response time",
                "IT support accessible via a known contact with most issues resolved within a reasonable timeframe",
                "A defined IT support process with clear escalation paths and tracked response times",
                "Dedicated IT support function with SLAs, proactive monitoring, and regular team satisfaction reviews",
            ],
        ],
        "mb": [
            "Does your organisation have a formal digital capability framework with role-specific competency standards?",
            # ✏️ Sandra: add "(L&D)" after "learning and development"
            "Is there a structured digital learning and development (L&D) program aligned to your strategic digital priorities?",
            "Do you measure and track digital capability uplift across the organisation over time?",
            "Does your organisation have a dedicated IT support function with documented service levels (SLAs)?",
        ],
        "mb_labels": [
            [
                "No capability framework — digital skills are undefined and unmanaged",
                "General awareness of digital skills importance but no defined framework or standards",
                "A basic capability framework exists with some role-specific digital requirements defined",
                "A formal digital capability framework with role-level competency standards is in use across the organisation",
                "A mature digital capability framework linked to performance management, career pathways, and strategic workforce planning",
            ],
            [
                "No structured programme — digital learning is ad hoc and individually driven",
                "Some digital training available but not aligned to strategic priorities or consistently delivered",
                "A structured digital L&D programme exists but is not fully aligned to strategic digital goals",
                "A strategic digital L&D programme is in place, aligned to priorities, and available to all staff",
                "An integrated digital learning ecosystem with personalised pathways, certification tracks, and measurable uplift outcomes",
            ],
            [
                "No measurement — no visibility of whether digital skills are improving",
                "Informal feedback collected but no systematic tracking or reporting",
                "Periodic capability assessments conducted with basic before/after comparison",
                "Regular capability measurement with defined metrics reported to leadership",
                "Continuous digital capability measurement with real-time dashboards, trend analysis, and integrated workforce planning",
            ],
            [
                "No dedicated IT function — support is ad hoc with no defined service levels",
                "IT support exists but SLAs are informal and rarely enforced",
                "An IT support function is in place with some documented response standards",
                "A dedicated IT support function with formal SLAs is in place and performance is monitored",
                "Mature IT support function with tiered SLAs, proactive monitoring, self-service capabilities, and regular performance reporting",
            ],
        ],
        "rubric": [
            "Digital skills are poor or inconsistent; no training; no access to IT support.",
            "Basic digital skills in place; occasional informal training; ad hoc IT support.",
            "Adequate digital skills for current needs; some structured training available; IT support accessible.",
            "Strong digital capability; regular training program; IT support with clear escalation paths.",
            "High-performing digital culture; formal capability framework; continuous learning; mature IT support model.",
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 6 — Client Experience & Digital Engagement
    # ─────────────────────────────────────────────────────────────────────────
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
        "st_labels": [
            [
                "No digital options — all client engagement is face-to-face or by phone",
                "Clients can email me but no purpose-built digital engagement tools are available",
                "At least one digital option is available (e.g. video calls or e-signature) though not consistently offered",
                "Multiple digital touchpoints are in place and actively offered to all clients",
                "A seamless digital engagement experience with multiple options that clients can access independently",
            ],
            [
                "No website or online presence",
                "A basic website or social media presence exists but is outdated or incomplete",
                "A professional website exists and is mostly current with accurate service information",
                "A well-maintained, mobile-friendly website accurately reflects services and is regularly updated",
                "A professional, SEO-optimised website integrated with booking, contact forms, and client portal — actively maintained",
            ],
            [
                "No proactive digital communication — clients hear from me only when they contact me",
                "Occasional emails or messages sent manually when I remember",
                "Regular use of at least one digital channel (e.g. email newsletter, SMS reminders) for client communication",
                "Proactive digital communication across multiple channels, scheduled and tracked",
                "Automated, personalised multi-channel client communications with engagement tracking and optimisation",
            ],
            [
                "No client feedback collected — no system or process in place",
                "Occasionally ask for feedback verbally but nothing recorded digitally",
                "A basic digital feedback method is used periodically (e.g. email survey or Google review request)",
                "Regular digital feedback collection with results reviewed and used to improve services",
                "Systematic client feedback programme with NPS or satisfaction tracking, trend analysis, and published improvements",
            ],
        ],
        "sb": [
            "Does your business offer clients self-service digital options (e.g. client portal, online bookings, electronic document signing)?",
            "Is your website current, mobile-responsive, and accessible to potential and existing clients?",
            "Does your business have a consistent digital communication approach for client engagement and retention?",
            "Do you use client data to personalise or improve your services and communications?",
        ],
        "sb_labels": [
            [
                "No self-service options — all client interactions require direct staff involvement",
                "One basic self-service feature available (e.g. online enquiry form) but not a true client portal",
                "One or more self-service options in place (e.g. e-signature or online booking) used by most clients",
                "A client portal or suite of self-service tools actively used by the majority of clients",
                "Comprehensive self-service digital experience with portal, e-signature, payments, and real-time service tracking",
            ],
            [
                "No website or a severely outdated one that does not represent the business accurately",
                "A website exists but is not mobile-responsive or regularly updated",
                "Website is reasonably current and mobile-friendly but not fully optimised for client access",
                "A well-maintained, mobile-responsive website with clear service information and easy contact options",
                "A high-performing website with SEO, accessibility compliance, live chat, client portal integration, and regular content updates",
            ],
            [
                "No consistent approach — client communication is reactive and ad hoc",
                "Some digital communication happens but without a defined strategy or schedule",
                "A basic digital communication approach is in place (e.g. monthly newsletter, follow-up emails)",
                "A documented digital communication plan covers all client lifecycle stages with consistent delivery",
                "An integrated multi-channel communication strategy personalised by client type, tracked and continuously optimised",
            ],
            [
                "Client data not used — services and communications are generic for all clients",
                "Occasionally reference client history informally but no systematic use of data",
                "Client data used to personalise some communications or tailor services for key clients",
                "Client data systematically used to improve service delivery and personalise communications for all clients",
                "Advanced use of client data and analytics to proactively identify needs, personalise engagement, and drive service innovation",
            ],
        ],
        "mb": [
            "Does your organisation have a formal digital client experience (CX) strategy with defined service standards and client journey mapping?",
            "Do you use a CRM system to manage client relationships, track all interactions, and measure service delivery KPIs?",
            "Does your organisation deliver an integrated multi-channel digital client experience (portal, e-signature, video, app)?",
            "Do you use client data analytics to proactively identify service improvement opportunities and measure client satisfaction?",
        ],
        "mb_labels": [
            [
                "No CX strategy — client experience is managed informally and inconsistently",
                "Some awareness of client experience goals but no formal strategy or journey mapping",
                "A documented CX approach exists with some journey mapping for key client segments",
                "A formal CX strategy with defined service standards and client journey maps is in use across the organisation",
                "An enterprise CX programme with advanced journey mapping, real-time feedback loops, and continuous experience optimisation",
            ],
            [
                "No CRM — client relationships managed via email, spreadsheets, or informally",
                "A CRM is in place but adoption is poor and data quality is inconsistent",
                "CRM is used by most staff to track client interactions, though KPI reporting is limited",
                "CRM fully adopted with consistent data entry, used to track KPIs and manage client relationships",
                "CRM integrated with all client-facing systems, providing a single source of truth for all client data and service KPIs",
            ],
            [
                "Single-channel only — clients can only engage through one digital method",
                "Two or three isolated digital channels available but not integrated",
                "Multiple digital channels in place with some integration across the client experience",
                "An integrated multi-channel experience delivers a consistent journey across all digital touchpoints",
                "A fully orchestrated omni-channel client experience with real-time personalisation and seamless channel switching",
            ],
            [
                "No client analytics — satisfaction is assessed informally or not at all",
                "Basic satisfaction data collected (e.g. ad hoc surveys) but not analysed systematically",
                "Regular client satisfaction measurement with results reviewed and shared with leadership",
                # ✏️ Sandra: explain NPS
                "Client data analytics used to identify trends, measure NPS (Net Promoter Score), and drive targeted service improvements",
                "Advanced client analytics with predictive modelling, real-time satisfaction tracking, and proactive service intervention",
            ],
        ],
        "rubric": [
            "No digital client touchpoints; communication exclusively by phone or in person; no online presence.",
            "Basic online presence (website); limited digital client interaction; no structured feedback collection.",
            "Some digital service options available (e.g. e-signature, video); website maintained; basic digital communication.",
            "Multiple digital client touchpoints integrated; CRM in use; proactive communication; client feedback collected.",
            "Exceptional digital client experience; fully integrated CX strategy; data-driven service improvement.",
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    # PILLAR 7 — Security & Compliance
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": 7,
        "name": "Security & Compliance",
        "description": "Evaluates your cybersecurity posture, incident preparedness, and awareness of regulatory obligations aligned with ACSC guidance.",
        "icon": "🔒",
        "st": [
            "Do you use strong, unique passwords and multi-factor authentication (MFA) on your key business accounts?",
            "Are your devices (laptop, phone) protected with passwords/PINs and kept up to date with operating system updates?",
            "Do you have a secure, separate backup of your important business data stored in a different location?",
            # ✏️ Sandra: explain what ACSC is — moved to label opt 5
            "Are you aware of common cyber threats such as phishing emails, and do you know how to respond?",
        ],
        "st_labels": [
            [
                "Reusing simple passwords across accounts — no MFA in use",
                "Mostly unique passwords but some reuse; MFA enabled on only one or two accounts",
                "Strong unique passwords for key accounts; MFA enabled on email and financial accounts",
                "Strong unique passwords and MFA enabled across all business accounts",
                "Password manager in use with strong unique passwords and MFA enforced on every business account",
            ],
            [
                "Devices unprotected and rarely updated",
                "Devices have basic protection but updates are often delayed or ignored",
                "Devices are password-protected and updates are installed within a reasonable timeframe",
                "All devices protected with strong PINs/passwords and kept consistently up to date",
                "All devices fully patched and protected — updates applied promptly, device encryption enabled, remote wipe configured",
            ],
            [
                "No backup — data exists only on one device or service",
                "Occasional manual backups but stored in the same location as the primary data",
                "Regular backups in place stored separately (e.g. cloud + local), though not automated",
                "Automated backups stored in a separate secure location, with occasional testing",
                "Automated, encrypted backups to multiple locations with regular restoration testing and documented recovery procedure",
            ],
            [
                "Not aware of common threats — would not recognise a phishing attempt",
                "Broadly aware that cyber threats exist but uncertain how to identify or respond to them",
                "Can recognise common threats (e.g. phishing, scam calls) and know the basic steps to take",
                "Confident in identifying and responding to common threats; know who to contact and what to report",
                # ✏️ Sandra: explain what ACSC is
                "Cyber-aware at an expert level — actively practise threat recognition, follow ACSC (Australian Cyber Security Centre) guidance, and keep knowledge current",
            ],
        ],
        "sb": [
            # ✏️ Sandra: explain what ACSC is — handled in label opt 5
            "Does your business have documented cybersecurity procedures or a basic security policy covering all team members?",
            "Is multi-factor authentication (MFA) enabled on all critical business systems and cloud accounts?",
            "Do you provide cybersecurity awareness training for your team at least annually?",
            "Does your business hold cyber liability insurance and have a basic incident response plan?",
        ],
        "sb_labels": [
            [
                "No security policy or procedures — cybersecurity is managed ad hoc",
                "Informal cybersecurity practices exist but nothing is documented or communicated to staff",
                "A basic security policy exists covering key areas (passwords, devices, email), accessible to staff",
                "A documented security policy covering all major risk areas is in place, communicated to all staff, and reviewed annually",
                # ✏️ Sandra: explain what ACSC is
                "A comprehensive, regularly reviewed security policy aligned to ACSC (Australian Cyber Security Centre) guidance, with staff attestation and clear enforcement",
            ],
            [
                "MFA not enabled on any business systems",
                "MFA enabled on one or two systems (e.g. email) but not consistently across the business",
                "MFA enabled on most critical systems, with a few exceptions",
                "MFA enabled across all critical business systems and cloud accounts",
                "MFA enforced organisation-wide with centralised management, monitoring, and regular access reviews",
            ],
            [
                "No cybersecurity training provided",
                "Occasional informal guidance given (e.g. email warning) but no structured training",
                "At least one structured cybersecurity training session or module delivered in the past 12 months",
                "Annual cybersecurity awareness training completed by all staff with documented records",
                "Regular, structured cybersecurity training programme with phishing simulations, updated annually, and tracked completion",
            ],
            [
                "No cyber insurance and no incident response plan",
                "Aware of the need but neither insurance nor a plan is in place",
                "Either cyber insurance or a basic incident response plan is in place (but not both)",
                "Both cyber liability insurance and a documented incident response plan are in place",
                "Current cyber insurance policy reviewed annually; tested incident response plan with defined roles, escalation paths, and communication templates",
            ],
        ],
        "mb": [
            # ✏️ Sandra: explain what ASD is — handled in labels
            "Does your organisation have a formally documented information security framework aligned to Australian standards (e.g. ASD Essential Eight)?",
            "Do you conduct regular vulnerability assessments, penetration testing, or third-party security audits?",
            # ✏️ Sandra: explain MSP and SOC — handled in labels
            "Is there a dedicated security function (internal or managed service) providing continuous monitoring and response capability?",
            "Does your organisation have a tested cyber incident response plan and a business continuity plan?",
        ],
        "mb_labels": [
            [
                "No formal security framework — security measures are ad hoc and undocumented",
                "Informal security practices exist but no recognised framework has been adopted",
                # ✏️ Sandra: explain what ASD is
                "A security framework has been documented but is not fully implemented or aligned to ASD (Australian Signals Directorate) Essential Eight",
                "A formal security framework aligned to ASD (Australian Signals Directorate) Essential Eight is implemented and reviewed annually",
                "A mature, regularly audited information security framework fully aligned to ASD (Australian Signals Directorate) Essential Eight with continuous improvement processes",
            ],
            [
                "No assessments ever conducted",
                "Occasional ad hoc checks but no scheduled or formal assessment programme",
                "Some form of security assessment conducted at least annually (internal or external)",
                "Regular scheduled vulnerability assessments and periodic penetration testing with documented findings and remediation",
                "Continuous vulnerability management programme with scheduled pen testing, third-party audits, and real-time threat monitoring",
            ],
            [
                "No dedicated security function — security managed as part of general IT responsibilities",
                "Security awareness exists within IT but no dedicated function or monitoring capability",
                "A part-time or shared security resource provides some oversight; basic monitoring tools in place",
                # ✏️ Sandra: explain MSP
                "A dedicated security function (internal team or Managed Service Provider (MSP)) provides regular monitoring and incident response",
                # ✏️ Sandra: explain SOC
                "A mature Security Operations Centre (SOC) with 24/7 monitoring, threat intelligence, and rapid response capability",
            ],
            [
                "No incident response or business continuity plan exists",
                "Plans are under development or exist only informally",
                "Both plans are documented but have not been tested or exercised",
                "Both plans are documented, communicated to relevant staff, and tested at least annually",
                "Regularly exercised, board-endorsed plans with defined RTO/RPO targets, post-exercise improvements, and integration with insurance and regulatory obligations",
            ],
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
