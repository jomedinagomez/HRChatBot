"""Generate the demo corpus.

Run from the repo root:  python scripts/generate_samples.py

Layout mirrors the customer's S3 Hive partitioning, so audience comes from the
folder rather than from anything printed on the page:

    domain=hr_chatbot/src=<system>/persona=<manager|non-manager>/<file>

Persona follows their rule: 'Manager' means manager-only and 'Non-Manager' means
every employee can read it, managers included. That is the only access rule the
customer applies today.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import docs_peoplecentral as pc
import docs_policyhub as ph
import docs_sharepoint as sp
import docs_states as st
from render import COMPANY, write_pdf

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "samples" / "documents"
BUCKET = "s3://edp-km-hrchatbot-demo-us-west-2"

MANAGER = "Manager"
EVERYONE = "Non-Manager"

# Security filter principals. In production these are Entra group object IDs.
ALL_EMPLOYEES = "all-employees"
MANAGERS = "managers"

CORPUS = [
    # ------------------------------------------------------------- Policy Hub
    dict(id="HR-204", src="policy_hub", file="Meridian_Nationwide Paid Sick Leave Policy Final.pdf",
         title="Nationwide Paid Sick Leave Policy", body=ph.NATIONWIDE_PSL,
         persona=EVERYONE, family="paid-sick-leave", revision="Rev. 4"),
    dict(id="HR-210", src="policy_hub", file="Flexible PTO Program.pdf",
         title="Flexible Paid Time Off Program", body=ph.FLEXIBLE_PTO,
         persona=EVERYONE, family="paid-time-off", revision="Rev. 3"),
    dict(id="HR-118", src="policy_hub", file="Colleague Privacy Notice.pdf",
         title="Colleague Privacy Notice", body=ph.PRIVACY_NOTICE,
         persona=EVERYONE, family="privacy", revision="Rev. 2"),
    dict(id="HR-101", src="policy_hub", file="Code of Conduct.pdf",
         title="Code of Conduct", body=ph.CODE_OF_CONDUCT,
         persona=EVERYONE, family="conduct", revision="Rev. 6"),
    dict(id="HR-162", src="policy_hub", file="Hybrid and Remote Work Policy.pdf",
         title="Hybrid and Remote Work Policy", body=ph.REMOTE_WORK,
         persona=EVERYONE, family="workplace", revision="Rev. 2"),
    dict(id="FIN-402", src="policy_hub", file="Travel and Expense Policy.pdf",
         title="Travel and Expense Policy", body=ph.TRAVEL_EXPENSE,
         persona=EVERYONE, family="finance", revision="Rev. 9"),
    dict(id="PH-INDEX", src="policy_hub", file="HR Policy _Table of Contents.pdf",
         title="HR Policy Table of Contents", body=st.POLICY_INDEX,
         persona=EVERYONE, family="reference", revision="Current"),
    # State supplements repeat answers that are also in HR-204. That overlap is
    # the retrieval problem the customer asked to see reproduced.
    dict(id="HR-204-NY", src="policy_hub", file="New York.pdf",
         title="New York Paid Sick Leave Supplement", body=st.NEW_YORK,
         persona=EVERYONE, family="paid-sick-leave", revision="Rev. 3", parent="HR-204"),
    dict(id="HR-204-ME", src="policy_hub", file="Maine.pdf",
         title="Maine Earned Paid Leave Supplement", body=st.MAINE,
         persona=EVERYONE, family="paid-sick-leave", revision="Rev. 2", parent="HR-204"),
    dict(id="HR-204-CO", src="policy_hub", file="Colorado.pdf",
         title="Colorado Healthy Families and Workplaces Supplement", body=st.COLORADO,
         persona=EVERYONE, family="paid-sick-leave", revision="Rev. 3", parent="HR-204"),
    dict(id="HR-204-SEA", src="policy_hub", file="Seattle.pdf",
         title="Seattle Paid Sick and Safe Time Supplement", body=st.SEATTLE,
         persona=EVERYONE, family="paid-sick-leave", revision="Rev. 2", parent="HR-204"),
    dict(id="HR-204-PHL", src="policy_hub", file="Philadelphia.pdf",
         title="Philadelphia Promoting Healthy Families and Workplaces Supplement",
         body=st.PHILADELPHIA, persona=EVERYONE, family="paid-sick-leave",
         revision="Rev. 1", parent="HR-204"),
    # ------------------------------------------ People Central (ServiceNow)
    dict(id="KB0010514", src="people_central",
         file="Performance_Management_Global_KB0010514.pdf",
         title="Performance Management: What to Expect as a Colleague", body=pc.PERF_EMPLOYEE,
         persona=EVERYONE, family="performance", revision="v4"),
    dict(id="KB0010537", src="people_central",
         file="Performance_Management_Global_MGR_KB0010537.pdf",
         title="Performance Calibration: Manager Preparation Guide", body=pc.PERF_MANAGER,
         persona=MANAGER, family="performance", revision="v7"),
    dict(id="KB0010779", src="people_central",
         file="Employee_Relations_Managers_Toolkit_US_MGR_KB0010779.pdf",
         title="Employee Relations Toolkit for Managers (U.S.)", body=pc.MANAGER_TOOLKIT,
         persona=MANAGER, family="employee-relations", revision="v3"),
    dict(id="KB0011204", src="people_central",
         file="How_To_Request_Leave_Of_Absence_KB0011204.pdf",
         title="How to request a leave of absence", body=pc.LEAVE_REQUEST_HOWTO,
         persona=EVERYONE, family="leave-of-absence", revision="v6"),
    dict(id="KB0011330", src="people_central",
         file="Workday_Time_Off_Balances_KB0011330.pdf",
         title="Workday navigation: finding your time off balance", body=pc.WORKDAY_BALANCES,
         persona=EVERYONE, family="systems", revision="v2"),
    dict(id="KB0011402", src="people_central",
         file="New_Hire_Onboarding_Checklist_KB0011402.pdf",
         title="New colleague onboarding checklist: first 30 days", body=pc.ONBOARDING,
         persona=EVERYONE, family="onboarding", revision="v5"),
    # ------------------------------------------------------------ SharePoint
    # Scripted Q&A pairs, standing in for the answers Lex serves today.
    dict(id="SP-QA", src="sharepoint", area="HR Help", file="HR Quick Answers.pdf",
         title="HR quick answers", body=sp.SCRIPTED_ANSWERS,
         persona=EVERYONE, family="scripted-answers", revision="v18"),
    dict(id="SP-BEN-FAQ", src="sharepoint", area="Benefits", file="Benefits FAQ.pdf",
         title="Benefits questions we get every week", body=sp.BENEFITS_FAQ,
         persona=EVERYONE, family="benefits", revision="v12"),
    dict(id="SP-MGR-CARD", src="sharepoint", area="Manager hub",
         file="Manager Quick Card - Approving Time Away.pdf",
         title="Manager quick card: approving time away", body=sp.MANAGER_QUICK_CARD,
         persona=MANAGER, family="paid-sick-leave", revision="v3"),
    dict(id="SP-PERF-MEMO", src="sharepoint", area="Talent",
         file="Performance Cycle Dates Memo.pdf",
         title="Memo: performance cycle dates", body=sp.PERF_TIMELINE_MEMO,
         persona=EVERYONE, family="performance", revision="v1"),
    dict(id="SP-ELIG", src="sharepoint", area="Benefits",
         file="Time Away Eligibility Matrix.pdf",
         title="Time away eligibility at a glance", body=sp.ELIGIBILITY_MATRIX,
         persona=EVERYONE, family="paid-sick-leave", revision="v6"),
]

CONTENT_SOURCE = {
    "policy_hub": "Policy_Hub",
    "people_central": "PeopleCentral",
    "sharepoint": "SharePoint",
}


def chrome(entry):
    """Page header and footer. Never mentions audience."""
    src = entry["src"]
    if src == "policy_hub":
        return "policyhub", f"{entry['id']} | {entry['revision']}", f"Policy Hub | {entry['id']}"
    if src == "people_central":
        return "peoplecentral", f"{entry['id']} | {entry['revision']}", "People Central knowledge article"
    return "sharepoint", f"HR Connect | {entry['area']}", f"SharePoint | {entry['area']}"


def source_url(entry):
    """Deep link into the system of record, shaped like the customer's real URLs."""
    src = entry["src"]
    if src == "policy_hub":
        number = int(hashlib.sha1(entry["id"].encode()).hexdigest()[:4], 16) % 9000 + 100
        return (f"https://meridian.policyhub.com/PolicyHub/DocumentViewer.aspx"
                f"?Document={number}&ResolveRevision=1&Redirect=1&PolicyViewType=Hyperlink")
    if src == "people_central":
        guid = hashlib.sha1(entry["id"].encode()).hexdigest()[:32]
        return f"https://meridianexternal.service-now.com/hrportal?id=kb_article_view&sys_kb_id={guid}"
    area = entry["area"].replace(" ", "%20")
    return f"https://meridianfg.sharepoint.com/sites/HRConnect/{area}/{entry['file'].replace(' ', '%20')}"


def main():
    if DOCS.exists():
        shutil.rmtree(DOCS)

    metadata = []
    for entry in CORPUS:
        manager_only = entry["persona"] == MANAGER
        partition = Path(
            "domain=hr_chatbot", f"src={entry['src']}",
            f"persona={'manager' if manager_only else 'non-manager'}",
        )
        (DOCS / partition).mkdir(parents=True, exist_ok=True)

        theme, header, footer = chrome(entry)
        write_pdf(DOCS / partition / entry["file"], entry["body"], theme,
                  COMPANY, header, footer)

        relative = (partition / entry["file"]).as_posix()
        record = {
            "document_id": entry["id"],
            "file": f"documents/{relative}",
            "file_name": entry["file"],
            "title": entry["title"],
            "url": source_url(entry),
            "s3_uri": f"{BUCKET}/{relative}",
            "content_source": CONTENT_SOURCE[entry["src"]],
            "persona": entry["persona"],
            "group_ids": [MANAGERS] if manager_only else [ALL_EMPLOYEES],
            "policy_family": entry["family"],
            "revision": entry["revision"],
        }
        if entry.get("parent"):
            record["parent_document_id"] = entry["parent"]
        metadata.append(record)

    (ROOT / "samples" / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    managers = sum(1 for d in metadata if d["persona"] == MANAGER)
    print(f"Wrote {len(metadata)} documents to {DOCS}")
    print(f"  Manager: {managers}   Non-Manager: {len(metadata) - managers}")


if __name__ == "__main__":
    main()
