from __future__ import annotations

import textwrap
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parents[1] / "samples"

PROPOSALS = {
    "Apex Systems": [
        "APEX SYSTEMS | Response to the Unified Procurement Analytics RFP | 18 October 2026\n\n1. Executive summary\nApex proposes a secure, extensible procurement analytics platform that consolidates supplier, contract, and spend data into a governed workspace. Our design supports the requested 1,200 users, existing identity provider, and staged expansion to additional business units. We understand the buyer requires implementation within six months, auditable access, and transparent total cost.",
        "2. Proposed solution and delivery\nA modular cloud architecture uses a managed data warehouse, an integration layer with documented REST APIs, and a role-based web application. The platform scales horizontally and supports SSO through SAML and OIDC.\n\nDelivery is planned across 24 weeks: discovery (4 weeks), foundation and integrations (8 weeks), configuration and migration (6 weeks), acceptance and training (4 weeks), and production transition (2 weeks). A delivery lead, solution architect, two integration engineers, security lead, and change manager are assigned. Weekly governance tracks dependencies, decisions, and risks. The legacy ERP connector requires buyer test credentials by week 3.",
        "3. Commercial, security, and support\nFixed implementation fee: $1,480,000. Annual subscription: $360,000 for up to 1,200 named users. Optional data migration beyond three source systems is time-and-materials at $220/hour. Taxes and buyer-provided cloud tenancy are excluded. Pricing is valid for 90 days.\n\nControls include AES-256 encryption at rest, TLS 1.2+ in transit, SSO, least-privilege role controls, immutable audit events, annual penetration testing, and documented incident response. Apex maintains ISO 27001 certification; the current certificate and scope can be provided during diligence. Customer data is hosted in the selected region and is not used to train shared models.\n\nSupport is 24x7 for critical incidents, with a 30-minute initial response target for severity 1. Standard support includes named service management, monthly service reviews, and quarterly release briefings. Apex has delivered comparable analytics programs for two large public-sector organizations; references are available with permission. The proposal assumes buyer SMEs are available for two workshops each week.",
    ],
    "BrightPath Tech": [
        "BRIGHTPATH TECH | Unified Procurement Analytics Proposal | 18 October 2026\n\n1. Executive summary\nBrightPath can get the buyer's procurement teams working quickly with a straightforward cloud analytics application. The product brings purchasing data into a common dashboard and can be configured for the requested departments. We prioritize a low initial cost and a short path to launch.",
        "2. Solution and schedule\nOur hosted platform includes dashboards, supplier records, and exportable reports. Standard file imports are available; integration details for the buyer's ERP will be confirmed during onboarding. The application supports user accounts and configurable permissions. Architecture and scaling specifics can be shared in a technical workshop.\n\nWe target a 12-week launch: kickoff and data review (2 weeks), configuration (4 weeks), imports and user testing (4 weeks), and training and launch (2 weeks). The team includes one implementation manager and two configuration specialists. The schedule assumes timely sample files and one buyer contact. We have not included a detailed contingency schedule.",
        "3. Price and service\nYear 1 price: $420,000, comprising $120,000 onboarding and $300,000 annual subscription for 1,200 users. Additional data imports may incur fees after discovery. Travel, taxes, and custom reports are excluded. Renewal pricing is subject to the order form.\n\nThe service is hosted in a major cloud environment. Data is encrypted in transit and at rest. We support standard login controls and can discuss single sign-on options. Detailed certification status, audit-log retention, data residency, and incident response commitments are not specified in this response.\n\nSupport is available by email during business hours, with urgent issues escalated to an on-call engineer. BrightPath has completed several small-business reporting deployments; this would be our first procurement analytics deployment at this user scale. Customer references can be arranged after mutual approval.",
    ],
    "NexaWorks": [
        "NEXAWORKS | Proposal for Unified Procurement Analytics | 18 October 2026\n\n1. Executive summary\nNexaWorks proposes a phased analytics service that unifies spend, supplier, and contract information while keeping source-system ownership clear. The design emphasizes practical integration, accountable delivery, and a support transition that continues beyond launch. Our proposal addresses 1,200 initial users and six-month delivery, with explicit decisions and acceptance gates.",
        "2. Architecture and implementation\nA managed data platform receives source data through API and scheduled-file connectors. Validation rules report rejected records before publishing curated datasets to a browser-based analytics workspace. SSO, role mapping, and a documented REST interface are included. The initial scope covers two ERP sources and one contract repository; further systems are estimated through change control.\n\nThe 20-week plan includes mobilization and discovery (3 weeks), solution design and data mapping (4 weeks), two-week integration iterations (6 weeks), user acceptance and remediation (4 weeks), and training and go-live (3 weeks). A program manager, integration architect, three engineers, test lead, security adviser, and adoption specialist are named roles. RAID reviews run weekly; a four-week schedule reserve is held before the buyer's required date. Acceptance criteria and named owners are defined for each milestone.",
        "3. Commercials, assurance, and service\nImplementation: $790,000 fixed fee. Annual subscription: $445,000 for 1,200 users and the three named source systems. Optional connectors are $45,000 each after a scoped estimate. Fees exclude tax and buyer-side data cleansing. Subscription increases are capped at 4% annually for the initial three-year term.\n\nSecurity includes AES-256 at rest, TLS 1.2+ in transit, SSO, least privilege, centralized audit logging with 12-month retention, annual penetration tests, and a documented incident plan with a 24-hour notification target. NexaWorks is ISO 27001 certified; the scope statement and independent SOC 2 Type II report are available under NDA. Data remains in the buyer-selected region and is deleted within 60 days after termination, subject to backup expiry.\n\nA named service manager coordinates 24x7 severity-1 response (15-minute acknowledgement target), monthly service reporting, quarterly roadmap sessions, and two days of post-launch hypercare. NexaWorks has delivered 11 analytics implementations, including four procurement programs of similar integration scope. Two references have approved contact subject to buyer scheduling. The buyer supplies data owners and test access by the mobilization gate.",
    ],
    "Orbit Digital": [
        "ORBIT DIGITAL | Procurement Insights Platform Response | 18 October 2026\n\n1. Executive overview\nOrbit Digital is pleased to propose its established insights platform for the buyer's procurement transformation. We bring long experience helping complex organizations improve visibility and standardize reporting. The proposed service will give procurement leaders a consolidated view of suppliers and spend while supporting a measured rollout.",
        "2. Platform and implementation\nThe Orbit Insights suite provides configurable dashboards, supplier profiles, scheduled reports, and data exports. It is designed for enterprise workloads and can be tailored to the buyer's governance model. The proposal anticipates connection to the buyer's existing systems; exact interface patterns and source-system sequencing will be agreed during discovery. A detailed integration inventory and dependency plan are not included at this stage.\n\nThe indicative schedule is 18 to 26 weeks depending on source-data readiness. Work proceeds through discovery, configuration, data loading, user review, and rollout. A senior engagement manager coordinates Orbit's product specialists and the buyer's team. Resource levels and acceptance measures will be finalized after a joint planning session.",
        "3. Price, controls, and experience\nEstimated first-year price is $970,000: $310,000 implementation and $660,000 annual platform subscription. The estimate assumes three standard data sources and excludes custom interfaces, extensive remediation, travel, and taxes. Final commercial terms follow discovery.\n\nThe platform supports encryption in transit and at rest, configurable user roles, and standard cloud security monitoring. Orbit maintains an information-security program and conducts periodic external testing. Specific certification evidence, audit retention periods, incident notification targets, and data residency commitments can be discussed during contracting; they are not committed in this response.\n\nOrbit offers a 24x7 service desk for critical issues, a named customer success lead, and quarterly account reviews. Our teams have supported more than 30 enterprise analytics deployments across regulated and public-sector organizations. Three customer references are available, including two procurement transformation programs. Orbit's account team has long-standing delivery relationships with several listed clients. The proposal is subject to final scoping and the buyer's standard legal review.",
    ],
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for supplier, pages in PROPOSALS.items():
        path = OUT_DIR / f"{supplier.replace(' ', '_')}.pdf"
        path.write_bytes(_make_pdf(pages))
        print(f"Created {path}")


def _make_pdf(pages: list[str]) -> bytes:
    objects: list[bytes] = []
    page_ids = [3 + index * 2 for index in range(len(pages))]
    content_ids = [page_id + 1 for page_id in page_ids]
    font_id = 3 + len(pages) * 2
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode("ascii"))
    for page_id, content_id, page_text in zip(page_ids, content_ids, pages):
        page_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>"
        )
        lines = []
        for paragraph in page_text.splitlines():
            lines.extend(textwrap.wrap(paragraph, width=82) or [""])
        commands = ["BT", "/F1 10 Tf", "54 748 Td", "14 TL"]
        for index, line in enumerate(lines):
            safe = line.encode("ascii", errors="replace").decode("ascii")
            escaped = safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            if index:
                commands.append("T*")
            commands.append(f"({escaped}) Tj")
        commands.append("ET")
        stream = "\n".join(commands).encode("ascii")
        content_obj = f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"\nendstream"
        objects.extend([page_obj.encode("ascii"), content_obj])
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    output = bytearray(b"%PDF-1.4\n%Synthetic RFP proposal\n")
    offsets = [0]
    for object_id, content in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{object_id} 0 obj\n".encode("ascii"))
        output.extend(content)
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(output)


if __name__ == "__main__":
    main()