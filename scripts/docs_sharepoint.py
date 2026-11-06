"""SharePoint pages: FAQs, quick cards, memos, and scripted answers."""

SCRIPTED_ANSWERS = [
    ("h1", "HR quick answers"),
    ("p", "Short answers to the questions HR hears most often. Most of these are not covered by "
          "a policy document, so the answer lives here."),
    ("h2", "Systems and access"),
    ("qa", [
        ("How do I reset my Workday password?",
         "Use the Forgot Password link on the Workday sign-in page. If you are locked out after "
         "three attempts, contact the Technology Service Desk, not HR."),
        ("Who do I contact about a payslip error?",
         "Open a Payroll case in People Central and attach the payslip period. Payroll responds "
         "within two business days."),
        ("How do I update my home address?",
         "Workday, Personal Information, Contact. If you are moving to another state, also tell "
         "HR before the move so benefits and tax withholding stay correct."),
    ]),
    ("h2", "Time away"),
    ("qa", [
        ("How many sick days do I have left?",
         "HR cannot look up an individual balance from here. Check Workday, Absence, "
         "Absence Balance. The Available column is the number to use."),
        ("Can I take paid sick leave for a dentist appointment?",
         "Yes. Routine preventive care is a permitted use under the Nationwide Paid Sick Leave "
         "Policy."),
        ("Do I need a doctor's note for one sick day?",
         "No. Documentation may be requested only after more than three consecutive scheduled "
         "workdays, and in some states only after four."),
    ]),
    ("h2", "Employment verification"),
    ("qa", [
        ("I need proof of employment for a mortgage.",
         "Use the automated verification service linked in People Central. HR does not issue "
         "letters for routine verifications."),
        ("A former employer is asking for a reference.",
         "Meridian confirms dates of employment and job title only. Direct the request to the "
         "verification service."),
    ]),
    ("note", "These answers are general. For your own balance, entitlement, or case status, "
             "check Workday or open a case in People Central."),
]

BENEFITS_FAQ = [
    ("h1", "Benefits questions we get every week"),
    ("p", "Written by the Benefits team for the colleague portal. Last reviewed in October."),
    ("h2", "Enrolment"),
    ("qa", [
        ("When can I change my elections?",
         "During open enrolment each November, or within 31 days of a qualifying life event such "
         "as marriage, birth, adoption, or a spouse's loss of coverage."),
        ("I missed open enrolment. What happens?",
         "Your current elections roll over at the new year's rates, except for the health savings "
         "account contribution, which resets to zero and must be re-elected."),
    ]),
    ("h2", "Comparing the medical plans"),
    ("table", [
        ["Feature", "Core PPO", "Value HDHP", "Select HMO"],
        ["Annual deductible, individual", "$1,200", "$2,800", "$0"],
        ["Coinsurance after deductible", "20%", "10%", "Copay only"],
        ["Out-of-pocket maximum", "$5,000", "$6,500", "$4,000"],
        ["Health savings account eligible", "No", "Yes", "No"],
        ["Out-of-network coverage", "Yes", "Yes", "Emergency only"],
    ]),
    ("h2", "Which plan should I pick?"),
    ("p", "Benefits cannot recommend a plan. The decision tool in the enrolment portal models "
          "your expected costs under each option using last year's claims. Colleagues who expect "
          "low usage and want to build a health savings account often choose the Value HDHP; "
          "colleagues who prefer predictable copays often choose the Select HMO."),
    ("h2", "Dependents"),
    ("qa", [
        ("Can I cover my domestic partner?",
         "Yes. Complete the domestic partner affidavit during enrolment. Imputed income may "
         "apply depending on your state."),
        ("Until what age can I cover a child?",
         "Through the end of the month in which the child turns 26, regardless of student or "
         "marital status."),
    ]),
]

MANAGER_QUICK_CARD = [
    ("h1", "Manager quick card: approving time away"),
    ("p", "One page. Keep it open during approval week."),
    ("h2", "Approve or escalate"),
    ("table", [
        ["Request", "Your call", "Route instead"],
        ["PTO for vacation", "Approve or decline on coverage", "-"],
        ["Paid sick leave", "Approve", "Never decline for coverage"],
        ["More than 5 consecutive days", "-", "Absence Management"],
        ["Request tied to an accommodation", "-", "Absence Management"],
        ["Pattern you find concerning", "-", "Employee Relations before acting"],
    ]),
    ("h2", "Three things to remember"),
    ("numbers", [
        "You may decline PTO for coverage. You may not decline paid sick leave for coverage.",
        "You never need to know why a colleague is sick, and you should not ask.",
        "Record only the dates and the approval. Nothing about the reason.",
    ]),
    ("h2", "Where to look things up"),
    ("bullets", [
        "Entitlement amounts: HR-204 for PTO-ineligible colleagues, HR-210 for Flexible PTO",
        "State differences: the supplement for that state in Policy Hub",
        "Balances: Workday, Absence, Absence Balance",
    ]),
]

PERF_TIMELINE_MEMO = [
    ("h1", "Memo: performance cycle dates"),
    ("p", "To: All U.S. colleagues and managers. From: Talent Management. Subject: Key dates for "
          "the annual performance cycle."),
    ("p", "The dates below are firm. Business areas may add earlier internal deadlines but may "
          "not extend the ones listed here."),
    ("table", [
        ["Date", "Milestone", "Who acts"],
        ["January 8", "Goal setting opens", "Colleagues"],
        ["February 15", "Goal approval closes", "Managers"],
        ["July 10 - 31", "Mid-year check-in window", "Both"],
        ["November 1 - 20", "Self-review window", "Colleagues"],
        ["December 1", "Provisional ratings due", "Managers"],
        ["December 8", "Calibration packets due to HR", "Managers"],
        ["December 9 - 19", "Calibration sessions", "Managers and HR"],
        ["January 12 - 30", "Review conversations", "Managers"],
        ["February 6", "Written comment window closes", "Colleagues"],
    ]),
    ("h2", "Two notes"),
    ("bullets", [
        "A colleague on approved leave during the self-review window receives an extension "
        "automatically; no request is needed.",
        "Managers who join Meridian after October 1 partner with their HR Business Partner for "
        "their first cycle.",
    ]),
]

ELIGIBILITY_MATRIX = [
    ("h1", "Time away eligibility at a glance"),
    ("p", "Reference table maintained by Benefits. Use it to find which policy governs a "
          "colleague, then read that policy for the detail."),
    ("table", [
        ["Colleague group", "Governing policy", "Sick time source", "Annual amount"],
        ["U.S. hourly, PTO-ineligible", "HR-204", "Paid Sick Leave accrual", "Up to 56 hours"],
        ["U.S. salaried grade 54+", "HR-210", "Flexible PTO", "18 to 28 days"],
        ["U.S. salaried below grade 54", "HR-204", "Paid Sick Leave accrual", "Up to 56 hours"],
        ["Mexico", "Mexico leave schedule", "Statutory plus company", "By category"],
        ["Contingent worker", "Supplier program", "Supplier program", "Not applicable"],
        ["Intern", "Internship addendum", "Pro-rated grant", "24 hours"],
    ]),
    ("h2", "State overlays for PTO-ineligible colleagues"),
    ("table", [
        ["Location", "What changes", "Where it is written"],
        ["Maine", "First 24 hours usable for any reason", "HR-204-ME"],
        ["New York State", "No documentation under 3 days", "HR-204-NY"],
        ["New York City", "Safe time and designated person", "HR-204-NY"],
        ["Colorado", "48-hour public health emergency grant", "HR-204-CO"],
        ["Seattle", "108-hour carryover cap", "HR-204-SEA"],
        ["Philadelphia", "City complaint right", "HR-204-PHL"],
    ]),
    ("note", "A colleague in Pittsburgh is not covered by the Philadelphia supplement. City "
             "overlays apply only within the named city."),
]
