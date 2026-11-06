"""Policy Hub state and city supplements: short standalone PDFs.

These deliberately overlap with Section 7 of the nationwide policy. That overlap is
the retrieval problem the customer described: the same question is answered by more
than one document, so the right one has to win.
"""

NEW_YORK = [
    ("h1", "New York Paid Sick Leave Supplement"),
    ("p", "Policy No. HR-204-NY. Supplement to the Nationwide Paid Sick Leave Policy, HR-204. "
          "Applies to colleagues whose work location of record is in New York State."),
    ("h2", "Entitlement"),
    ("p", "New York colleagues may use up to fifty-six (56) hours of paid sick leave in a calendar "
          "year. Accrual follows the nationwide rate of one hour for every thirty hours worked. "
          "Leave is available for use as it is accrued, with no waiting period."),
    ("h2", "Documentation"),
    ("p", "Meridian does not require medical documentation for an absence of fewer than three "
          "consecutive workdays. For a longer absence, the Absence Management team may request an "
          "attestation of eligibility. A manager may not request documentation directly and may "
          "not require a colleague to disclose the nature of an illness as a condition of leave."),
    ("h2", "No Replacement Worker"),
    ("p", "A colleague may not be required to find a replacement worker as a condition of using "
          "paid sick leave. Coverage is a management responsibility."),
    ("h2", "New York City"),
    ("p", "Colleagues working in the five boroughs are additionally covered by the New York City "
          "Earned Safe and Sick Time Act. Safe time may be used for any purpose permitted by that "
          "act, including relocating for safety and attending legal proceedings. Once per calendar "
          "year a colleague may designate any individual whose close association is the equivalent "
          "of a family relationship as a covered family member."),
    ("h2", "Payout"),
    ("p", "Accrued and unused paid sick leave is not paid out at separation in New York."),
    ("h2", "Questions"),
    ("p", "Contact Absence Management through People Central. Reference policy HR-204-NY."),
]

MAINE = [
    ("h1", "Maine Earned Paid Leave Supplement"),
    ("p", "Policy No. HR-204-ME. Supplement to the Nationwide Paid Sick Leave Policy, HR-204. "
          "Applies to colleagues whose work location of record is in Maine."),
    ("h2", "Use for Any Reason"),
    ("p", "Maine is different from every other location in this policy family. Colleagues working "
          "in Maine may use the first twenty-four (24) hours of accrued leave in a calendar year "
          "for any reason at all, including vacation, a personal errand, or a family event. The "
          "reason does not have to fall within the permitted uses listed in Section 6 of HR-204."),
    ("p", "Once the first twenty-four hours have been used, the remainder of the colleague's "
          "accrued balance may be used only for the paid sick leave purposes described in "
          "Section 6 of HR-204."),
    ("table", [
        ["Hours used in the calendar year", "Permitted reasons"],
        ["First 24 hours", "Any reason, including vacation and personal time"],
        ["Hours 25 and above", "Section 6 purposes only"],
    ]),
    ("h2", "Notice"),
    ("p", "For leave that is not an emergency, give your manager four (4) weeks of notice. "
          "Meridian may deny a non-emergency request that would cause an undue hardship, but may "
          "not deny leave taken for an emergency, illness, or sudden necessity."),
    ("h2", "Accrual and Carryover"),
    ("p", "Accrual follows the nationwide rate of one hour for every thirty hours worked. The "
          "nationwide forty (40) hour carryover cap applies without change in Maine."),
    ("note", "If a Maine colleague asks whether leave can be used for vacation, the answer is yes "
             "for the first 24 hours. The nationwide policy alone would give the wrong answer."),
]

COLORADO = [
    ("h1", "Colorado Paid Sick Leave Supplement"),
    ("p", "Policy No. HR-204-CO. Supplement to the Nationwide Paid Sick Leave Policy, HR-204. "
          "Applies to colleagues whose work location of record is in Colorado."),
    ("h2", "Standard Accrual"),
    ("p", "Colorado colleagues accrue and use paid sick leave on the nationwide schedule: one hour "
          "per thirty hours worked, up to fifty-six hours of use per calendar year."),
    ("h2", "Public Health Emergency Supplement"),
    ("p", "When a federal, state, or local public health emergency is declared, Meridian provides "
          "a one-time supplemental grant of forty-eight (48) hours to each Colorado colleague. "
          "The supplemental grant:"),
    ("bullets", [
        "is in addition to the fifty-six hour annual maximum;",
        "may be used for emergency-related reasons including self-isolation, caring for a family "
        "member, and loss of child care caused by the emergency;",
        "expires four (4) weeks after the declared emergency ends; and",
        "is granted once per declared emergency, not once per calendar year.",
    ]),
    ("h2", "Documentation"),
    ("p", "Documentation may not be requested for an absence of four or fewer consecutive "
          "workdays. During a declared public health emergency, documentation may not be "
          "requested at all."),
]

SEATTLE = [
    ("h1", "Seattle Paid Sick and Safe Time Supplement"),
    ("p", "Policy No. HR-204-SEA. Supplement to the Nationwide Paid Sick Leave Policy, HR-204. "
          "Applies to colleagues whose work location of record is in the City of Seattle."),
    ("h2", "Employer Tier"),
    ("p", "Meridian Financial Group is a Tier 3 employer for purposes of the Seattle Paid Sick and "
          "Safe Time Ordinance. Tier 3 status affects the carryover amount described below."),
    ("h2", "Accrual and Carryover"),
    ("table", [
        ["Item", "Seattle", "Nationwide"],
        ["Accrual rate", "1 hour per 30 hours worked", "1 hour per 30 hours worked"],
        ["Year-end carryover cap", "108 hours", "40 hours"],
        ["Annual use maximum", "No separate cap", "56 hours"],
    ]),
    ("p", "The higher Seattle carryover cap replaces the nationwide cap. A Seattle colleague who "
          "ends the year with ninety accrued hours carries all ninety forward."),
    ("h2", "Household Member"),
    ("p", "For safe-time absences, household member includes a spouse, a domestic partner, a "
          "former spouse, a parent of a shared child, and any individual with whom the colleague "
          "shares a residence. This definition is broader than the family member definition in "
          "Section 6 of HR-204 and applies only to safe-time absences in Seattle."),
    ("h2", "Separation and Rehire"),
    ("p", "If a Seattle colleague is rehired within twelve (12) months, previously accrued and "
          "unused hours are reinstated."),
]

PHILADELPHIA = [
    ("h1", "Philadelphia Paid Sick Leave Supplement"),
    ("p", "Policy No. HR-204-PHL. Supplement to the Nationwide Paid Sick Leave Policy, HR-204. "
          "Applies to colleagues whose work location of record is in the City of Philadelphia. "
          "It does not apply elsewhere in Pennsylvania."),
    ("h2", "Coverage"),
    ("p", "Philadelphia colleagues accrue and use paid sick leave on the nationwide schedule. This "
          "supplement adds the complaint and anti-retaliation rights described below."),
    ("h2", "Right to File a Complaint"),
    ("p", "A colleague who works in Philadelphia and believes that paid sick leave was denied, or "
          "that they were retaliated against for requesting or taking leave, may file a complaint "
          "with the city agency administering the ordinance within one hundred eighty (180) days "
          "of the alleged violation. A colleague may also bring a civil action. These rights are "
          "in addition to, and not a replacement for, Meridian's internal reporting channels."),
    ("h2", "Posting and Notice"),
    ("p", "The required city notice is posted in each Philadelphia office and is available in "
          "People Central. Colleagues who work remotely in Philadelphia receive the notice "
          "electronically at hire and annually thereafter."),
    ("note", "A colleague working in Pittsburgh or elsewhere in Pennsylvania is not covered by "
             "this supplement and should follow the nationwide policy."),
]

POLICY_INDEX = [
    ("h1", "U.S. Human Resources Policy Index"),
    ("p", "Maintained by HR Policy Governance. Revised quarterly. Use this index to find the "
          "controlling document before contacting the service desk."),
    ("h2", "Time Away From Work"),
    ("table", [
        ["Policy No.", "Title", "Applies to"],
        ["HR-204", "Nationwide Paid Sick Leave Policy", "PTO-ineligible colleagues"],
        ["HR-204-NY", "New York Paid Sick Leave Supplement", "New York State"],
        ["HR-204-ME", "Maine Earned Paid Leave Supplement", "Maine"],
        ["HR-204-CO", "Colorado Paid Sick Leave Supplement", "Colorado"],
        ["HR-204-SEA", "Seattle Paid Sick and Safe Time Supplement", "City of Seattle"],
        ["HR-204-PHL", "Philadelphia Paid Sick Leave Supplement", "City of Philadelphia"],
        ["HR-210", "Flexible Paid Time Off Policy", "PTO-eligible colleagues"],
        ["HR-301", "Leave of Absence Policy", "All U.S. colleagues"],
    ]),
    ("h2", "Conduct and Privacy"),
    ("table", [
        ["Policy No.", "Title", "Applies to"],
        ["HR-101", "Code of Conduct", "All colleagues"],
        ["HR-118", "Colleague Privacy Notice", "All colleagues"],
        ["FIN-402", "Travel and Expense Policy", "All colleagues"],
    ]),
    ("h2", "Workplace"),
    ("table", [
        ["Policy No.", "Title", "Applies to"],
        ["HR-162", "Hybrid and Remote Work Policy", "U.S. colleagues"],
        ["HR-171", "Performance Management Policy", "All colleagues"],
    ]),
    ("h2", "How to Read a Supplement"),
    ("p", "A supplement changes only what it says it changes. Everything else in the parent policy "
          "still applies. If a supplement and the parent policy appear to conflict on the same "
          "point, the supplement controls for colleagues in that location."),
]
