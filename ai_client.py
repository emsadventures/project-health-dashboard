def build_project_prompt(project_context):

    prompt = f"""
You are an experienced project management advisor.

Project Health:
{project_context['project_health']}

Total Tasks:
{project_context['total_tasks']}

Completed Tasks:
{project_context['completed_tasks']}

In Progress Tasks:
{project_context['in_progress_tasks']}

Not Started Tasks:
{project_context['not_started_tasks']}

Late Tasks:
{project_context['late_tasks']}

Completion Percentage:
{project_context['percent_complete']}

Write:

1. Executive Summary
2. Risks
3. Recommendations

Keep the response concise.
"""

    return prompt

def generate_advisor_response(
    question,
    project_context
):

    question = question.lower()

    if "red" in question:

        return (
            f"The project is currently "
            f"{project_context['project_health']} "
            f"because only "
            f"{project_context['percent_complete']}% "
            f"of tasks are complete. "
            f"There are "
            f"{project_context['not_started_tasks']} "
            f"tasks not started."
        )

    elif "late" in question:

        return (
            f"The project currently has "
            f"{project_context['late_tasks']} "
            f"late tasks."
        )

    elif "progress" in question:

        return (
            f"The project is "
            f"{project_context['percent_complete']}% "
            f"complete."
        )

    elif "focus" in question:

        return (
            f"Focus should be placed on the "
            f"{project_context['not_started_tasks']} "
            f"tasks that have not yet started."
        )

    return (
        "I understand the question, "
        "but I don't yet know how "
        "to answer that."
    )