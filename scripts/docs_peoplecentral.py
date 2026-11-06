"""People Central (ServiceNow) knowledge articles.

Rendered with the article properties block on page one, the way a ServiceNow
article looks when it is printed or exported to PDF.
"""

PERF_EMPLOYEE = [
    ("h1", "Performance Management: What to Expect as a Colleague"),
    ("p", "This article walks you through the annual performance cycle from your side of the "
          "process. Managers follow a separate article for the calibration step."),
    ("h2", "The cycle at a glance"),
    ("table", [
        ["Window", "What happens", "Your action"],
        ["January", "Goals open in Workday", "Draft three to five goals"],
        ["February 15", "Goal approval closes", "Confirm goals with your manager"],
        ["July", "Mid-year check-in", "Write a short progress note"],
        ["November 1 - 20", "Self-review window", "Submit your self-review"],
        ["December", "Manager reviews and calibration", "No action"],
        ["Late January", "Review conversations", "Attend your review meeting"],
    ]),
    ("h2", "Writing your self-review"),
    ("p", "The self-review is capped at 400 words per goal. Managers consistently say the most "
          "useful reviews are specific rather than long. Name the work, say what changed because "
          "of it, and name the people you worked with."),
    ("numbers", [
        "Open Workday, then Performance, then My Reviews.",
        "For each goal, describe what you delivered and the measurable result.",
        "Add up to three examples of how you worked, not just what you delivered.",
        "Flag anything that blocked you, including dependencies outside your control.",
        "Submit by 11:59 p.m. local time on November 20. Late submissions still count but may "
        "not reach your manager before calibration.",
    ]),
    ("h2", "What your manager sees"),
    ("p", "Your manager sees your goals, your self-review, and any feedback you requested through "
          "Workday. Your manager does not see draft text you have not submitted, and does not see "
          "feedback that another colleague marked private to HR."),
    ("h2", "Ratings"),
    ("p", "Meridian uses a four-level scale. The definitions below are the same ones your manager "
          "uses, so there is no hidden rubric."),
    ("table", [
        ["Rating", "Meaning"],
        ["Exceptional", "Delivered beyond the scope of the role and raised the bar for others"],
        ["Strong", "Delivered the full scope of the role well"],
        ["Developing", "Delivered part of the scope; specific gaps are named in the review"],
        ["Below", "Did not deliver the scope; a formal plan follows"],
    ]),
    ("h2", "If you disagree with your review"),
    ("p", "Tell your manager during the conversation and ask for the specific examples behind the "
          "rating. If you still disagree after that conversation, you have ten (10) business days "
          "to add a written comment to the review in Workday. The comment becomes part of the "
          "record. You may also contact an Employee Relations Partner."),
    ("h2", "Time away during the cycle"),
    ("p", "Approved leave does not lower a rating. If you were out for a significant part of the "
          "year, your manager is expected to evaluate the work you did during the time you were "
          "present, not to prorate you downward for being away."),
    ("h2", "Related articles"),
    ("bullets", [
        "KB0011330 - Workday navigation: finding your time off balance",
        "HR-171 Performance Management Policy in Policy Hub",
    ]),
]

PERF_MANAGER = [
    ("h1", "Performance Calibration: Manager Preparation Guide"),
    ("p", "This article covers how to prepare for and run a calibration session, from entering "
          "provisional ratings through to recording the outcome. Treat what is discussed in the "
          "session as confidential."),
    ("h2", "What calibration is for"),
    ("p", "Calibration is a consistency check across managers, not a ranking exercise and not a "
          "forced distribution. The question in the room is whether two colleagues doing "
          "comparable work in comparable conditions would receive comparable ratings from "
          "different managers. If the answer is no, the group works out why."),
    ("h2", "Before the session"),
    ("numbers", [
        "Enter a provisional rating for every direct report in Workday by December 1.",
        "For each provisional rating, prepare three concrete examples drawn from the work. An "
        "example names the deliverable, the difficulty, and the outcome.",
        "Review the self-review before you finalise the provisional rating, not after.",
        "Identify anyone whose scope changed mid-year, who was on leave, or who carried a "
        "significant unplanned workload, and note it.",
        "Submit your preparation packet to your HR Business Partner at least seven (7) business "
        "days before the session.",
    ]),
    ("note", "Seven business days is a hard cut-off. Packets that arrive late are scheduled into "
             "the overflow session in mid-January, which delays the colleague's review "
             "conversation."),
    ("h2", "Running the session"),
    ("table", [
        ["Minutes", "Agenda item", "Led by"],
        ["0 - 5", "Ground rules and confidentiality reminder", "HR facilitator"],
        ["5 - 20", "Walk the provisional ratings", "Each manager"],
        ["20 - 35", "Discuss outliers and scope differences", "Group"],
        ["35 - 42", "Bias check against the rating definitions", "HR facilitator"],
        ["42 - 45", "Confirm decisions and name open items", "HR facilitator"],
    ]),
    ("p", "The session is scheduled for forty-five (45) minutes. If the group cannot reach a "
          "decision on a colleague within the session, the item is recorded as open and the HR "
          "facilitator responds within two (2) business days."),
    ("h2", "What stays in the room"),
    ("bullets", [
        "Comparisons between named colleagues stay in the room and are never shared.",
        "The colleague receives the agreed rating and the examples that support it.",
        "Notes about another manager's team are not retained after the session.",
        "Never record a health reason, leave usage, or accommodation in a performance note.",
    ]),
    ("h2", "Disagreement"),
    ("p", "If you disagree with the group's conclusion, say so in the session and ask the "
          "facilitator to record it. You then have three (3) business days after the session to "
          "escalate in writing to your HR Business Partner. Silence in the session is treated as "
          "agreement."),
    ("h2", "Things that are never a basis for a rating"),
    ("bullets", [
        "Approved leave of any kind, including paid sick leave and parental leave",
        "A pending or granted accommodation",
        "Participation in an investigation",
        "Working a hybrid schedule that meets the policy minimum",
    ]),
]

MANAGER_TOOLKIT = [
    ("h1", "Employee Relations Toolkit for Managers (U.S.)"),
    ("p", "Use this toolkit for the first conversation. Anything in the escalate column goes to "
          "Employee Relations before you act."),
    ("h2", "Decide where it belongs"),
    ("table", [
        ["Situation", "Handle yourself", "Escalate first"],
        ["Repeated lateness", "Yes, coaching conversation", "If a disability or leave may be involved"],
        ["Missed deliverable", "Yes, document in a note", "If it follows a formal plan"],
        ["Peer conflict", "Yes, facilitate once", "If either party alleges harassment"],
        ["Allegation of discrimination", "No", "Always, same day"],
        ["Request for an accommodation", "No", "Always, route to Absence Management"],
        ["Possible policy violation involving money", "No", "Always, Compliance"],
    ]),
    ("h2", "A coaching conversation that works"),
    ("numbers", [
        "Open with the observation, not the conclusion. 'The last three status reports came in "
        "after the deadline' rather than 'you are unreliable'.",
        "Ask what is getting in the way and listen to the whole answer before responding.",
        "Agree on one specific change and a date to review it.",
        "Write a short note the same day: date, what was discussed, what was agreed.",
        "Follow up on the date you agreed, even if things improved.",
    ]),
    ("h2", "Sample language"),
    ("p", "When a colleague mentions a health issue during a performance conversation: 'Thank you "
          "for telling me. I am not going to ask for details. I am going to connect you with "
          "Absence Management, who can talk through what support is available. Let us pause the "
          "performance discussion until you have had that conversation.'"),
    ("p", "When a colleague asks you to keep an allegation confidential: 'I want to support you, "
          "and I also have to be honest that I cannot promise confidentiality for something like "
          "this. I am required to involve Employee Relations. I will tell you what I pass on.'"),
    ("h2", "What not to do"),
    ("bullets", [
        "Do not investigate an allegation of harassment or discrimination yourself.",
        "Do not ask about a diagnosis, a treatment plan, or a clinician's name.",
        "Do not keep a private file of performance notes outside Workday.",
        "Do not discuss one colleague's performance or pay with another colleague.",
        "Do not promise an outcome you do not control, including a rating or a transfer.",
    ]),
    ("h2", "Contacts"),
    ("table", [
        ["Need", "Contact", "Response target"],
        ["Employee Relations consult", "ER Partner for your business area", "1 business day"],
        ["Accommodation or leave", "Absence Management via People Central", "2 business days"],
        ["Ethics or compliance", "Ethics Helpline", "Immediate intake"],
    ]),
]

LEAVE_REQUEST_HOWTO = [
    ("h1", "How to request a leave of absence"),
    ("p", "Use this article when you will be away for more than five consecutive scheduled "
          "workdays. For a shorter absence, request paid sick leave or PTO in Workday instead."),
    ("h2", "Before you start"),
    ("bullets", [
        "Have your expected start date and estimated return date ready.",
        "Know whether the leave is for you or for a family member.",
        "You do not need a doctor's note to open the request.",
    ]),
    ("h2", "Steps"),
    ("numbers", [
        "In Workday, select Absence, then Request Absence.",
        "Choose Leave of Absence as the type.",
        "Select the reason category. If you are unsure, choose Medical - Self and the Absence "
        "Management team will reclassify it if needed.",
        "Enter the expected dates. Estimated dates are fine; you can revise them later.",
        "Submit. You will receive a case number within one business day.",
        "Watch for a secure message from Absence Management with any forms you need.",
    ]),
    ("h2", "What your manager sees"),
    ("p", "Your manager sees the dates and the approval status. Your manager does not see the "
          "reason category, any forms you submit, or any medical information. If your manager "
          "asks for a diagnosis, you are not required to provide it; contact Employee Relations."),
    ("h2", "Pay during leave"),
    ("p", "Pay depends on the leave type and your location. Absence Management confirms your pay "
          "arrangement in writing after the case is opened. Do not assume a leave is unpaid based "
          "on what a colleague told you; the answer differs by state and by leave type."),
    ("h2", "Returning to work"),
    ("p", "Contact Absence Management at least five (5) business days before your planned return "
          "so that systems access and payroll are restored on time. If your return date changes, "
          "update the case rather than telling your manager only."),
]

WORKDAY_BALANCES = [
    ("h1", "Workday navigation: finding your time off balance"),
    ("p", "Short how-to for colleagues. One to two minutes."),
    ("h2", "Steps"),
    ("numbers", [
        "Open Workday from the colleague portal.",
        "Select the Absence application on your home page.",
        "Under View, select Absence Balance.",
        "Set the As Of date. The default is today; set it to a future date to see what you will "
        "have accrued by then.",
        "Select Run.",
    ]),
    ("h2", "Reading the result"),
    ("table", [
        ["Column", "What it means"],
        ["Beginning balance", "Hours you carried into the current year"],
        ["Accrued", "Hours earned so far this year"],
        ["Taken", "Hours already used"],
        ["Scheduled", "Approved future absences not yet taken"],
        ["Available", "Beginning plus accrued, less taken and scheduled"],
    ]),
    ("note", "Available is the number to rely on. It already subtracts absences you have booked "
             "for later in the year."),
    ("h2", "Common questions"),
    ("qa", [
        ("My balance looks lower than I expected.",
         "Check the Scheduled column. Approved future time off is already deducted."),
        ("I do not see an Absence Balance option.",
         "Colleagues enrolled in Flexible PTO see PTO Balance instead. Both show the same "
         "columns."),
        ("The balance has not updated after my last pay period.",
         "Accrual posts two business days after payroll closes. Wait a full cycle before "
         "raising a case."),
    ]),
]

ONBOARDING = [
    ("h1", "New colleague onboarding checklist: first 30 days"),
    ("p", "Your first month, step by step. There is a separate checklist covering the hiring "
          "side of onboarding."),
    ("h2", "Day one"),
    ("bullets", [
        "Complete identity verification with the onboarding specialist",
        "Collect your laptop and badge",
        "Set up multi-factor authentication",
        "Complete the Code of Conduct acknowledgement",
    ]),
    ("h2", "Week one"),
    ("bullets", [
        "Enrol in benefits; you have 31 days from your start date",
        "Add your emergency contact in Workday",
        "Confirm your work location of record is correct",
        "Meet your onboarding buddy",
    ]),
    ("h2", "Weeks two and three"),
    ("bullets", [
        "Finish required compliance training",
        "Draft your first set of goals with your manager",
        "Review the policies that apply to your role in Policy Hub",
    ]),
    ("h2", "Day 30"),
    ("bullets", [
        "Thirty-day check-in with your manager",
        "Confirm your goals are approved in Workday",
        "Complete the new colleague experience survey",
    ]),
    ("note", "Benefits enrolment is the one deadline that cannot be extended. If you miss the "
             "31-day window you wait until the next open enrolment or a qualifying life event."),
]
