# project-health-dashboard
Python and Streamlit dashboard for analyzing Microsoft Planner project data.
Project Health Dashboard

A Python and Streamlit dashboard that analyzes Microsoft Planner-style project data and transforms it into actionable project insights.

The dashboard provides project health scoring, KPI reporting, schedule visualization, phase-level reporting, and an interactive Project Advisor that answers questions about project status and progress.

Features

Project Metrics

Total task count
Completion percentage
In-progress task tracking
Not-started task tracking
Late task identification
Automated project health status (Green / Yellow / Red)

Dashboard Visualizations

KPI summary cards
Completion by phase
Tasks by bucket
Status by bucket
Upcoming task tracking
Project Gantt chart
Schedule anomaly detection

Project Advisor The advisor can answer questions such as:

Why is the project RED?
How much progress has been made?
Are any tasks late?
What should I focus on next?
Architecture

Sample Project Data (Excel) | V planner_client.py | V dashboardV2.py | V ai_client.py

Project Files

dashboardV2.py

Main Streamlit dashboard

planner_client.py

Data access layer

ai_client.py

Project Advisor logic

config.py

Configuration settings

Test Template.xlsx

Sample project data

requirements.txt

Python dependencies
Technology Stack
Python
Streamlit
Pandas
Matplotlib
OpenPyXL
Git
GitHub
Installation

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run dashboardV2.py

Example Capabilities
Automated project health scoring
Interactive project dashboard
Schedule visualization with Gantt charts
Phase and bucket analysis
Risk identification
Project Advisor responses
Modular application design
Future Enhancements
Microsoft Graph integration
Automated Planner synchronization
AI-generated executive summaries
Automated status report generation
Natural language project analysis
Learning Objectives

This project was built to strengthen skills in:

Python development
Data visualization
Data analysis
Application architecture
Streamlit development
Git and GitHub workflows
AI-assisted project management concepts
Screenshots

Screenshots will be added in future updates.

For the short GitHub repository description, use:

Python and Streamlit dashboard for project health reporting, schedule visualization, KPI tracking, and AI-assisted project insights.
