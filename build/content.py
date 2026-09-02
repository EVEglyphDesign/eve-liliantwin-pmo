"""Content for the Universal DI Framework PMO Model brief.

Named audience: Elaine's management consulting team, delivered to Lilian.
Register: Andy's brief — one idea per sentence, buyer nouns, active verbs.
"""

TITLE = "Universal DI Framework PMO Model"
TAGLINE = "The PMO that runs inside your systems."
LEAD = ("Lilian Corvington — Practice Lead, Universal DI Framework PMO · "
        "EVEglyphDesign")
VERSION = "v1.0 — 2026"

LEDE = (
    "A management consulting PMO team that runs your SAP transformation "
    "inside your own systems. Every document, every decision, every "
    "reasoning step lands in your private repository as your trade secret "
    "from day one — and stays there when we go."
)

# Four surfaces. Each has a plain buyer-language paragraph and a named
# reference project. IKEA and Vodafone are the two reference points the
# operator authorised for public use.
SURFACES = [
    {
        "name": "Documents",
        "ref_kicker": "Reference:",
        "ref": ("a global retailer's country-by-country SAP programme "
                "(IKEA), where every proposal, blueprint, and specification "
                "was drafted in the client's own environment and versioned "
                "on the client's own systems."),
        "body": ("Proposals, blueprints, functional and technical specs, "
                 "meeting minutes. Drafted from your workshop notes, "
                 "priced from your scope, versioned every time you change "
                 "them. Every document says who wrote it, what it was "
                 "built from, and when."),
    },
    {
        "name": "Risks",
        "ref_kicker": "Reference:",
        "ref": ("a European telecoms transformation (Vodafone), where "
                "scope and change signals were tracked continuously "
                "against workshop context and surfaced to the steering "
                "committee before they became invoices."),
        "body": ("Scope movement, decision drift, and early warnings — "
                 "tracked against the workshop record you already have. "
                 "You see a change coming while there is still time to "
                 "price it, not after it lands in the invoice."),
    },
    {
        "name": "Changes",
        "ref_kicker": "Reference:",
        "ref": ("configuration work driven by plain-language questions "
                "against the project's own ALM record, with every change "
                "reviewed and approved by a human on the client team "
                "before it reached S/4HANA."),
        "body": ("Ask the system a plain-English question about your SAP "
                 "project. It drafts the change, shows you exactly what "
                 "it will do, and only pushes to S/4HANA after your team "
                 "approves it. No push without a signature."),
    },
    {
        "name": "Tests",
        "ref_kicker": "Reference:",
        "ref": ("test scenarios and evidence generated straight from the "
                "same requirements record the specs were drafted from, "
                "aligned to SAP Activate, kept alongside the deliverables "
                "in the client repository."),
        "body": ("Test scenarios written from the same requirements the "
                 "specs were drafted from. Scripts generated, runs "
                 "scheduled, evidence kept next to the deliverables. "
                 "When audit asks what you tested, the answer is in one "
                 "place."),
    },
]

TEAM_HEADING = "How the team is built"
TEAM_PARAS = [
    ("Every consultant on the team runs their own twin. The twin does "
     "the drafting, the tracking, the querying, and the test-writing on "
     "the client's side of the wall — using the client's own tools and "
     "the client's own data. Nothing crosses back to us."),
    ("The twins coordinate through protocol standards, not through a "
     "shared platform we own. Lilian sits at the top of the triangles "
     "and keeps the client's programme moving as one thing, not four."),
    ("When we finish, the twins go home with the client. The reasoning "
     "stays where the work was done."),
]

CALLOUT_KICKER = "The point."
CALLOUT = ("Your project's context reasoning is a trade secret. It is "
           "your workshops, your decisions, your language, your people. "
           "It should never live on a vendor's platform. With this "
           "model, it does not.")

COMPARE_HEADING = "Compared to a packaged AI assistant"
COMPARE_INTRO = (
    "We compare to Luzid because a management consulting group we work "
    "with brought it to us, and it is the cleanest example of the "
    "packaged category. The comparison is not about who has more "
    "features. It is about where the reasoning ends up."
)

COMPARE_LEFT_HEADER = "Universal DI Framework PMO Model"
COMPARE_RIGHT_HEADER = "Luzid — packaged AI assistant"

COMPARE_ROWS = [
    ("Where the work lives",
     "In your own private repository, on your own systems, from day one.",
     "On Luzid's platform, behind a Luzid login."),
    ("Who owns the reasoning when the engagement ends",
     "You do. Every context artifact is a trade secret you already own.",
     "Luzid."),
    ("How the team is organised",
     ("Every consultant runs their own twin. Twins produce reasoning on "
      "your surface, coordinated through protocol standards. A team "
      "lead keeps the programme moving as one thing."),
     ("One central agent (David) on a shared vendor platform, operated "
      "by their implementation team.")),
    ("Deliverables — documents, risks, changes, tests",
     ("Drafted in your environment, versioned on your systems, reviewed "
      "by your team, kept in your repository."),
     "Drafted on Luzid's platform, exported to your tools, retained by Luzid."),
    ("Protection of your trade secrets",
     ("Your data never leaves your boundary. Reasoning happens on your "
      "side of the wall."),
     "Your data crosses into Luzid to be reasoned on."),
    ("What is behind the outputs",
     ("A public decision-intelligence framework with a 96-source "
      "evidence register. Your team can read it before you sign."),
     "A vendor marketing site."),
]

CLOSING_LINE = ("Same four things on the page. Different thing in your "
                "building six months later.")

FRAMEWORK_HEADING = "The framework behind the model"
FRAMEWORK_PARA = (
    "The PMO model is one delivery pattern of a broader decision-"
    "intelligence framework we publish openly, with primary sources "
    "cited throughout. If your team wants to read the argument before "
    "we talk, start there."
)
FRAMEWORK_LINKS = [
    ("Decision Intelligence Framework — peer-review draft (v1.2)",
     "https://eveglyphdesign.github.io/decision-intelligence-framework/"),
    ("EVEglyph Executive Boot Contract — operating canon",
     "https://eveglyphdesign.github.io/eve-glyph-boot-contract/"),
    ("Source repository for this brief",
     "https://github.com/EVEglyphDesign/eve-liliantwin-pmo"),
]

CTA_HEADING = "Talk to us"
CTA_PARA = ("Direct line to Lilian on WhatsApp. One message, one "
            "conversation, no gatekeeper.")
CTA_LABEL = "Message on WhatsApp"
CTA_URL = "https://wa.me/15062921452"
