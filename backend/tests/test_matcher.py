import os
import sys
import json
import logging

# Adjust path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.matcher import JobMatcher

# Disable noisy logging for the test output
logging.getLogger("app.services.matcher").setLevel(logging.CRITICAL)

def run_tests():
    print("Initializing JobMatcher...")
    matcher = JobMatcher()
    
    target_jd = """
    Senior Frontend Engineer (React)
    We are looking for a Senior Frontend Engineer with 5+ years of experience.
    Core skills required: React, TypeScript, Tailwind CSS, State Management (Redux/Zustand).
    Must have experience with performance optimization and building scalable web applications.
    """

    resumes = {
        "Technical (Strong Match)": """
        John Doe - Senior Frontend Developer
        Experience: 6 years building web apps.
        Skills: React, TypeScript, JavaScript, HTML, CSS, Tailwind CSS, Redux, Next.js.
        Achievements: Optimized React app performance reducing load time by 40%. Led a team of 3 developers.
        """,
        "Managerial (Poor Match)": """
        Jane Smith - Product Manager
        Experience: 8 years in product management.
        Skills: Agile, Scrum, Jira, Roadmapping, Stakeholder Management, Team Leadership.
        Achievements: Delivered 5 major product launches. Managed cross-functional teams.
        """,
        "Entry-Level (Partial Match)": """
        Alice Johnson - Junior Web Developer
        Experience: 1 year.
        Skills: HTML, CSS, JavaScript, basic React.
        Achievements: Built a personal portfolio using React and simple CSS. Eager to learn.
        """
    }

    results = {}
    for name, text in resumes.items():
        print(f"Evaluating: {name}...")
        res = matcher.evaluate(sanitized_resume_text=text, job_description=target_jd)
        results[name] = res

    # Save results to a file
    output_file = os.path.join(os.path.dirname(__file__), "test_results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Testing complete. Results saved to {output_file}")

if __name__ == "__main__":
    run_tests()
