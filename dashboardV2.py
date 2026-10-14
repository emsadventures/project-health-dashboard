import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
from datetime import datetime
from matplotlib.patches import Patch
from planner_client import get_tasks, get_buckets

from ai_client import (
    build_project_prompt,
    generate_advisor_response
)

st.set_page_config(
page_title="Project Health Dashboard",
page_icon="📊",
layout="wide"
)

# --------------------------------------------------
# LOAD PLANNER DATA
# --------------------------------------------------

tasks = get_tasks()
buckets = get_buckets()

# --------------------------------------------------
# CLEAN AND PREPARE DATA
# --------------------------------------------------

# Remove rows without a task name
tasks = tasks.dropna(subset=["Task Name"]).copy()

# Match Planner bucket IDs with readable bucket names
bucket_map = dict(
    zip(
        buckets["Bucket ID"],
        buckets["Bucket Name"]
    )
)

tasks["Bucket Name"] = tasks["Bucket"].map(bucket_map)

tasks["Bucket Name"] = tasks["Bucket Name"].fillna(
    "Unknown Bucket"
)

# Convert Planner dates into datetime values
tasks["Start date"] = pd.to_datetime(
    tasks["Start date"],
    errors="coerce"
)

tasks["Due date"] = pd.to_datetime(
    tasks["Due date"],
    errors="coerce"
)


# --------------------------------------------------
# CALCULATE PROJECT METRICS
# --------------------------------------------------

total_tasks = len(tasks)

completed_tasks = len(
    tasks[tasks["Status"] == "Completed"]
)

in_progress_tasks = len(
    tasks[tasks["Status"] == "In progress"]
)

not_started_tasks = len(
    tasks[tasks["Status"] == "Not started"]
)

if total_tasks > 0:
    percent_complete = (
        completed_tasks / total_tasks
    ) * 100
else:
    percent_complete = 0


# --------------------------------------------------
# DETERMINE PROJECT HEALTH
# --------------------------------------------------

if percent_complete >= 75:
    project_health = "GREEN"
elif percent_complete >= 40:
    project_health = "YELLOW"
else:
    project_health = "RED"


# --------------------------------------------------
# IDENTIFY LATE TASKS
# --------------------------------------------------

late_tasks = tasks[
    tasks["Late"].astype(str).str.lower() == "true"
]


# --------------------------------------------------
# CREATE BUCKET METRICS
# --------------------------------------------------

bucket_counts = tasks["Bucket Name"].value_counts()

bucket_status = pd.crosstab(
    tasks["Bucket Name"],
    tasks["Status"]
)


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("Project Health Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Tasks",
    total_tasks
)

col2.metric(
    "Completion %",
    f"{percent_complete:.1f}%"
)

col3.metric(
    "Late Tasks",
    len(late_tasks)
)
col4, col5, col6 = st.columns(3)
col4.metric("Completed",completed_tasks)
col5.metric("In Progress",in_progress_tasks)
col6.metric("Not Started",not_started_tasks)

if project_health == "GREEN":
    st.success("Project Health: GREEN")

elif project_health == "YELLOW":
    st.warning("Project Health: YELLOW")

else:
    st.error("Project Health: RED")

# --------------------------------------------------
# PROJECT CONTEXT FOR AI
# --------------------------------------------------
from ai_client import build_project_prompt

project_context = {
    "project_health": project_health,
    "total_tasks": total_tasks,
    "completed_tasks": completed_tasks,
    "in_progress_tasks": in_progress_tasks,
    "not_started_tasks": not_started_tasks,
    "late_tasks": len(late_tasks),
    "percent_complete": round(percent_complete, 1)
}

ai_prompt = build_project_prompt(
    project_context
)
with st.expander("AI Prompt Preview"):

    st.code(ai_prompt)

st.subheader("Project Advisor")

advisor_question = st.text_input(
    "Ask a project question:",
    placeholder="Why is this project RED?"
)

if advisor_question:

    response = generate_advisor_response(
        advisor_question,
        project_context
    )

    st.info(response)
# --------------------------------------------------
# COMPLETION BY BUCKET
# --------------------------------------------------

completion_data = []

preferred_bucket_order = [
    "Planning",
    "Design",
    "Execution",
    "Testing",
    "Deployment",
    "Closeout"
]

for bucket in preferred_bucket_order:

    bucket_tasks = tasks[
        tasks["Bucket Name"] == bucket
    ]

    if bucket_tasks.empty:
        continue

    completed_in_bucket = len(
        bucket_tasks[
            bucket_tasks["Status"] == "Completed"
        ]
    )

    total_in_bucket = len(bucket_tasks)

    bucket_percent = (
        completed_in_bucket /
        total_in_bucket
    ) * 100

    completion_data.append({
        "Phase": bucket,
        "Completion %": round(bucket_percent, 1)
    })

completion_df = pd.DataFrame(
    completion_data
)

left_col, right_col = st.columns(2)
with left_col:
    st.subheader("Completion by Phase")
    st.dataframe(completion_df,hide_index=True,width="stretch")
with right_col:
    st.subheader("Status by Bucket")
    st.dataframe(bucket_status,hide_index=True,width='stretch')
st.subheader("Tasks by Bucket")
bucket_df = bucket_counts.reset_index()
bucket_df.columns = ["Bucket Name","Count"]
st.dataframe(bucket_df,hide_index=True,width="stretch")

# --------------------------------------------------
# LATE TASKS
# --------------------------------------------------

st.subheader("Late Tasks")

if late_tasks.empty:
    st.success("No late tasks")

else:
    st.dataframe(
        late_tasks[
            [
                "Task Name",
                "Bucket Name",
                "Status",
                "Priority",
                "Due date"
            ]
        ]
    )


# --------------------------------------------------
# UPCOMING INCOMPLETE TASKS
# --------------------------------------------------

today = pd.Timestamp.today().normalize()

upcoming_tasks = tasks[
    tasks["Due date"].notna()
    & (tasks["Due date"] >= today)
    & (tasks["Status"] != "Completed")
].sort_values("Due date")
upcoming_display = upcoming_tasks.copy()

upcoming_display["Due date"] = (
    upcoming_display["Due date"]
    .dt.strftime("%b %d, %Y")
)

st.subheader("Upcoming Tasks")
st.dataframe(upcoming_display[["Task Name","Bucket Name","Status","Priority","Due date"]].head(10),
hide_index=True,width="stretch")
# --------------------------------------------------
# PREPARE GANTT CHART DATA
# --------------------------------------------------
gantt_tasks = tasks.dropna(
    subset=["Start date", "Due date"]
).copy()

# Identify tasks whose dates are reversed
invalid_dates = gantt_tasks[
    gantt_tasks["Due date"] < gantt_tasks["Start date"]
]

if not invalid_dates.empty:

    invalid_dates_display = invalid_dates.copy()

    invalid_dates_display["Start date"] = (
        invalid_dates_display["Start date"]
        .dt.strftime("%b %d, %Y")
    )

    invalid_dates_display["Due date"] = (
        invalid_dates_display["Due date"]
        .dt.strftime("%b %d, %Y") )

    st.warning("Some tasks have due dates before start dates.")

    st.dataframe(
        invalid_dates_display[
            [
                "Task Name",
                "Start date",
                "Due date"
            ]
        ],
        hide_index=True,
        width="stretch"
    )
# Exclude reversed date ranges from the chart
gantt_tasks = gantt_tasks[
    gantt_tasks["Due date"] >= gantt_tasks["Start date"]
].copy()

gantt_tasks = gantt_tasks.sort_values(
    ["Start date", "Due date"]
)


# --------------------------------------------------
# GANTT CHART COLORS
# --------------------------------------------------

bucket_colors = {
    "Planning": "#FFB4A2",       # peach
    "Design": "#64DFDF",         # aqua
    "Execution": "#FFE08A",      # soft yellow
    "Testing": "#9381FF",        # periwinkle
    "Deployment": "#FF6B6B",     # coral
    "Closeout": "#80ED99"        # mint
}


# --------------------------------------------------
# CREATE GANTT CHART
# --------------------------------------------------

plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(
    figsize=(15, 9)
)

for chart_position, (_, row) in enumerate(
    gantt_tasks.iterrows()
):

    start_date = row["Start date"]
    due_date = row["Due date"]

    duration = (
        due_date - start_date
    ).days

    color = bucket_colors.get(
        row["Bucket Name"],
        "#B0B0B0"
    )

    # Same-day tasks appear as milestone diamonds
    if duration == 0:
        ax.scatter(
            start_date,
            chart_position,
            marker="D",
            s=75,
            color=color,
            edgecolor="#555555",
            linewidth=0.6,
            zorder=3
        )

    # Multi-day tasks appear as horizontal bars
    else:
        ax.barh(
            chart_position,
            duration,
            left=start_date,
            height=0.7,
            color=color,
            edgecolor="#666666",
            linewidth=0.5
        )


# --------------------------------------------------
# FORMAT GANTT CHART
# --------------------------------------------------

ax.set_yticks(
    range(len(gantt_tasks))
)

ax.set_yticklabels(
    gantt_tasks["Task Name"]
)

# Earliest tasks appear at the top
ax.invert_yaxis()

# Add today's vertical line
ax.axvline(
    datetime.today(),
    color="#333333",
    linestyle="--",
    linewidth=1.5,
    label="Today",
    zorder=2
)

# Format timeline labels
ax.xaxis.set_major_locator(
    mdates.WeekdayLocator(
        byweekday=mdates.MO,
        interval=1
    )
)

ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%b %d")
)

plt.setp(
    ax.get_xticklabels(),
    rotation=45,
    ha="right"
)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.25
)

ax.grid(
    axis="y",
    linestyle="-",
    alpha=0.15
)

ax.set_title(
    "Project Schedule",
    fontsize=16,
    fontweight="bold",
    pad=15
)

ax.set_xlabel("Date")
ax.set_ylabel("Task")


# --------------------------------------------------
# ADD LEGEND
# --------------------------------------------------

legend_items = [
    Patch(
        facecolor=color,
        edgecolor="#666666",
        label=bucket
    )
    for bucket, color in bucket_colors.items()
]

today_legend = plt.Line2D(
    [0],
    [0],
    color="#333333",
    linestyle="--",
    linewidth=1.5,
    label="Today"
)

milestone_legend = plt.Line2D(
    [0],
    [0],
    marker="D",
    color="none",
    markerfacecolor="#9381FF",
    markeredgecolor="#555555",
    markersize=7,
    label="Same-day milestone"
)

legend_items.extend(
    [
        today_legend,
        milestone_legend
    ]
)

ax.legend(
    handles=legend_items,
    title="Schedule Key",
    bbox_to_anchor=(1.01, 1),
    loc="upper left",
    frameon=True
)


# --------------------------------------------------
# DISPLAY CHART
# --------------------------------------------------

plt.tight_layout()
st.pyplot(fig)
