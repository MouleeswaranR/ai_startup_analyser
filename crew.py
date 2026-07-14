"""
AI Company Crew Module
======================
Assembles all agents and tasks into a CrewAI Crew instance.
Provides a single `run_company(startup_idea)` function that
orchestrates the entire AI company workflow.
"""

import json
import os
import time
from datetime import datetime
import concurrent.futures
import litellm

from crewai import Crew, Process

from agents import (
    create_ceo_agent,
    create_research_agent,
    create_developer_agent,
    create_marketing_agent,
    create_customer_support_agent,
)
from tasks import (
    create_ceo_task,
    create_research_task,
    create_developer_task,
    create_marketing_task,
    create_support_task,
)
from config import OUTPUT_DIR, AGENT_DELAY_SECONDS, validate_config


def run_company(startup_idea: str, model_name: str = None) -> dict:
    """
    Run the entire AI company pipeline for a given startup idea.

    Args:
        startup_idea: The user's startup concept description.
        model_name: Optional LLM model name to override the default.

    Returns:
        A dictionary with the output from each department.
    """
    validate_config(model_name)

    # ── Run agents one-by-one with delays (Groq rate limits) ─
    agent_configs = [
        ("ceo_strategy",        create_ceo_agent,              create_ceo_task),
        ("market_research",     create_research_agent,         create_research_task),
        ("product_development", create_developer_agent,        create_developer_task),
        ("marketing_plan",      create_marketing_agent,        create_marketing_task),
        ("customer_support",    create_customer_support_agent, create_support_task),
    ]

    outputs = {}
    crews_to_run = []
    
    for dept_name, agent_factory, task_factory in agent_configs:
        agent = agent_factory(model_name)
        task = task_factory(agent, startup_idea)
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
        crews_to_run.append((dept_name, crew))
    
    def run_crew(dept_name, crew):
        for attempt in range(3):
            try:
                result = crew.kickoff()
                return dept_name, str(result)
            except Exception as e:
                err_str = str(e).lower()
                if "rate_limit" in err_str or "ratelimit" in err_str or "connection error" in err_str or "internalservererror" in err_str:
                    wait = (AGENT_DELAY_SECONDS or 5) * (attempt + 1)
                    print(f"⚠️ API Error ({e})! Retrying {dept_name} in {wait}s... (attempt {attempt+1}/3)")
                    time.sleep(wait)
                else:
                    return dept_name, f"Error: {e}"
        return dept_name, "Failed after 3 retries due to API errors."

    print("\n🚀 Running all 5 agents in parallel...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_crew, dept_name, crew) for dept_name, crew in crews_to_run]
        for future in concurrent.futures.as_completed(futures):
            dept_name, result = future.result()
            outputs[dept_name] = result

    # Build full report from all outputs
    outputs["full_report"] = "\n\n---\n\n".join(
        f"## {k.replace('_', ' ').title()}\n\n{v}" for k, v in outputs.items()
    )


    # ── Save to Files ────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(OUTPUT_DIR, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    for name, content in outputs.items():
        filepath = os.path.join(run_dir, f"{name}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {name.replace('_', ' ').title()}\n\n")
            f.write(f"**Startup Idea:** {startup_idea}\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")
            f.write(content)

    # Save metadata
    metadata = {
        "startup_idea": startup_idea,
        "timestamp": timestamp,
        "output_dir": run_dir,
        "departments": [k for k in outputs.keys() if k != "full_report"],
    }
    with open(os.path.join(run_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    outputs["_metadata"] = metadata
    return outputs


# ── CLI Entry Point ──────────────────────────────────────
if __name__ == "__main__":
    idea = input("🚀 Enter your startup idea: ").strip()
    if not idea:
        print("Please provide a startup idea!")
    else:
        print(f"\n🏢 Starting AI Company for: {idea}\n")
        print("=" * 60)
        results = run_company(idea)
        print("\n" + "=" * 60)
        print("✅ All departments have completed their work!")
        print(f"📁 Results saved to: {results['_metadata']['output_dir']}")
