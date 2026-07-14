"""
AI Company Tasks Module
=======================
Defines the specific tasks assigned to each agent.
Each task has a description, expected output, and assigned agent.
"""

from crewai import Task


def create_ceo_task(agent, startup_idea: str) -> Task:
    """CEO: Create business strategy and product roadmap."""
    return Task(
        description=(
            f"You are the CEO of a brand-new startup. The founder has given you this idea:\n\n"
            f'"{startup_idea}"\n\n'
            f"Your job is to architect the fundamental DNA of the company. Do not use generic placeholders like [Company Name] or [Date]. Invent a compelling startup name and use realistic dates.\n\n"
            f"Deliver the following components in beautiful Markdown format:\n"
            f"1. **Executive Summary**: A punchy, 1-paragraph synthesis of the entire business case.\n"
            f"2. **Vision & Mission**: A bold 10-year vision and a concrete, actionable mission statement.\n"
            f"3. **Value Proposition Canvas**: Define the customer profile (jobs, pains, gains) and the value map (products, pain relievers, gain creators).\n"
            f"4. **Revenue Model & Unit Economics**: How will this make money? Detail the pricing strategy (SaaS tiers, usage-based, etc.) and projected margins.\n"
            f"5. **Product Roadmap (6 Months)**: A highly structured month-by-month roadmap with clear, technical milestones.\n"
            f"6. **Risk Assessment & Mitigation**: A table of top 3 existential risks (technical, market, operational) and exact strategies to mitigate them.\n\n"
            f"Be visionary, actionable, and data-driven. Think like a YC-backed founder pitching Sequoia Capital."
        ),
        expected_output=(
            "A comprehensive, highly-structured business strategy document in Markdown containing:\n"
            "- Executive Summary\n"
            "- Vision & Mission\n"
            "- Value Proposition Canvas\n"
            "- Revenue Model & Unit Economics\n"
            "- 6-Month Product Roadmap\n"
            "- Risk Assessment & Mitigation"
        ),
        agent=agent,
    )


def create_research_task(agent, startup_idea: str) -> Task:
    """Research Agent: Conduct market analysis."""
    return Task(
        description=(
            f"Conduct comprehensive, elite-level market research for a startup based on this idea:\n\n"
            f'"{startup_idea}"\n\n'
            f"Your research must be rigorous and data-driven. Invent realistic, well-reasoned data if exact numbers are unavailable. NEVER use placeholders.\n\n"
            f"Your report must cover:\n"
            f"1. **Market Sizing (TAM, SAM, SOM)**: Provide specific dollar estimates and CAGR percentages with reasoned justifications.\n"
            f"2. **Competitive Landscape**: A detailed matrix analyzing the top 3 direct competitors. Compare them on Pricing, Target Audience, Strengths, and Weaknesses.\n"
            f"3. **Customer Demographics & Psychographics**: Define 2 distinct, highly specific buyer personas (include age, role, goals, and behavioral traits).\n"
            f"4. **Macro-Economic & Tech Trends**: Identify 3 tailwinds driving adoption of this idea right now (e.g., AI advancements, regulatory shifts).\n"
            f"5. **SWOT Analysis**: A realistic assessment of the startup's Strengths, Weaknesses, Opportunities, and Threats.\n"
            f"6. **Go-to-Market Feasibility**: The most cost-effective channel to acquire the first 1,000 users.\n\n"
            f"Present your findings as a professional McKinsey-style market research report."
        ),
        expected_output=(
            "An elite market research report in Markdown containing:\n"
            "- Market Sizing (TAM/SAM/SOM)\n"
            "- Competitive Matrix\n"
            "- Buyer Personas\n"
            "- Macro Trends\n"
            "- SWOT Analysis\n"
            "- GTM Feasibility"
        ),
        agent=agent,
    )


def create_developer_task(agent, startup_idea: str) -> Task:
    """Developer Agent: Build product prototype & landing page."""
    return Task(
        description=(
            f"You are the Staff/Principal Engineer for a new startup:\n\n"
            f'"{startup_idea}"\n\n'
            f"Your goal is to design a robust, scalable, and modern technical foundation. Avoid generic jargon; make concrete technical choices.\n\n"
            f"Your deliverables:\n"
            f"1. **System Architecture**: Define the exact tech stack (e.g., Next.js, FastAPI, PostgreSQL, Redis, Kubernetes) and explain WHY these were chosen over alternatives.\n"
            f"2. **Data Model (ERD)**: Outline the primary database tables/collections, their key fields, and relationships.\n"
            f"3. **Core API Contract**: Provide a detailed RESTful or GraphQL specification for the 3 most important API endpoints (include paths, methods, request/response JSON payloads).\n"
            f"4. **Security & Scale**: Detail the authentication strategy (e.g., JWT, OAuth) and how the system will handle its first 10,000 concurrent users.\n"
            f"5. **MVP Code Snippet**: Write the core business logic (in Python, TS, or Go) for the most complex feature of the startup.\n\n"
            f"Ensure all code snippets are syntax-highlighted and the architecture is production-ready."
        ),
        expected_output=(
            "A production-grade technical architecture document containing:\n"
            "- System Architecture & Stack Justification\n"
            "- Database Schema / ERD\n"
            "- Core API Contract (JSON examples)\n"
            "- Security & Scaling Strategy\n"
            "- MVP Core Business Logic Code Snippet"
        ),
        agent=agent,
    )


def create_marketing_task(agent, startup_idea: str) -> Task:
    """Marketing Agent: Create go-to-market strategy & content."""
    return Task(
        description=(
            f"You are the Chief Marketing Officer (CMO) for this startup:\n\n"
            f'"{startup_idea}"\n\n'
            f"Your job is to engineer a viral, high-converting Go-To-Market (GTM) campaign. NEVER use placeholders like [Link] or [Company Name]. Invent a compelling brand name.\n\n"
            f"Deliver the following ready-to-publish assets:\n"
            f"1. **Brand Identity**: Define the brand voice (e.g., bold, empathetic, technical), core colors, and the 1-sentence 'Elevator Pitch'.\n"
            f"2. **Launch Campaign Strategy**: A step-by-step timeline for Product Hunt launch, PR outreach, and community seeding.\n"
            f"3. **High-Converting Ad Copy**: Write 3 distinct Facebook/Instagram ad variations (A/B/C testing different hooks: emotional, logical, FOMO).\n"
            f"4. **SEO Content Strategy**: Outline a pillar blog post (Title, H2s, target keywords) designed to rank on page 1 of Google.\n"
            f"5. **Drip Email Sequence**: Write the exact subject lines and body copy for a 3-part onboarding email sequence (Welcome, Aha Moment, Conversion).\n\n"
            f"Focus on psychology, conversion rate optimization (CRO), and growth hacking."
        ),
        expected_output=(
            "A comprehensive marketing and growth campaign containing:\n"
            "- Brand Identity & Elevator Pitch\n"
            "- Launch Campaign Strategy\n"
            "- 3 High-Converting Ad Variations\n"
            "- SEO Content Outline\n"
            "- 3-Part Onboarding Email Sequence"
        ),
        agent=agent,
    )


def create_support_task(agent, startup_idea: str) -> Task:
    """Customer Support Agent: Create FAQ & response templates."""
    return Task(
        description=(
            f"You are the Head of Customer Success setting up support for a new startup:\n\n"
            f'"{startup_idea}"\n\n'
            f"IMPORTANT RULES:\n"
            f"- You MUST invent a real, creative startup name based on the idea. NEVER write [Startup Name] or any [placeholder] brackets.\n"
            f"- Fill in ALL values: use a real company name, real sample user names (e.g. 'Sarah'), real email (e.g. support@companyname.com), real phone (e.g. +1-800-555-1234).\n"
            f"- NEVER leave any square brackets [ ] in your output. Every field must have a concrete value.\n\n"
            f"Create the following operational playbook:\n"
            f"1. **Customer FAQ (Top 10)**: Provide 10 highly realistic questions and empathetic, clear answers covering Pricing, Technical Troubleshooting, and Account Management.\n"
            f"2. **Macro Response Templates**: Write ready-to-send email templates for:\n"
            f"   - An angry customer requesting a refund.\n"
            f"   - A user reporting a critical bug/outage.\n"
            f"   - A power user requesting a complex custom feature.\n"
            f"3. **Onboarding Checklist**: A 5-step checklist for Customer Success Managers to ensure a successful enterprise client deployment.\n"
            f"4. **Escalation Matrix**: Define exactly when a Tier 1 ticket should be escalated to Engineering versus Account Management.\n\n"
            f"All responses should be empathetic, professional, and brand-aligned. Zero placeholders."
        ),
        expected_output=(
            "A complete Customer Success playbook with ALL placeholder values filled in containing:\n"
            "- Top 10 Customer FAQ\n"
            "- Macro Response Templates (Refund, Bug, Feature Request)\n"
            "- CSM Onboarding Checklist\n"
            "- Escalation Matrix"
        ),
        agent=agent,
    )
