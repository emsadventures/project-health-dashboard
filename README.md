# project-health-dashboard
Python and Streamlit dashboard for analyzing Microsoft Planner project data.
Project Health Dashboard

A Python and Streamlit dashboard that analyzes Microsoft Planner-style project data and transforms it into actionable project insights.

📊 Project Health Dashboard

A Python and Streamlit dashboard that analyzes Microsoft Planner-style project data and transforms it into actionable project insights.

The dashboard provides project health scoring, KPI reporting, schedule visualization, phase-level reporting, and an interactive Project Advisor that answers questions about project status and progress.

Features
Project Metrics
Total task count
Completion percentage
In-progress task tracking
Not-started task tracking
Late task identification
Automated project health status using Green, Yellow, and Red indicators
Dashboard Visualizations
KPI summary cards
Completion by phase
Tasks by bucket
Status by bucket
Upcoming task tracking
Project Gantt chart
Schedule anomaly detection
Project Advisor

The dashboard includes a rule-based Project Advisor prototype that uses current project metrics to answer questions such as:

Why is the project RED?
How much progress has been made?
Are any tasks late?
What should I focus on next?

Note: The current Project Advisor is a rules-based prototype and is not connected to a large language model.

Architecture

Sample Project Data (Excel)

↓

planner_client.py

↓

dashboardV2.py

↓

ai_client.py

Project Files
File	PurposedashboardV2.py	Main Streamlit dashboard
planner_client.py	Data access layer
ai_client.py	Project Advisor logic
config.py	Configuration settings
Test Template.xlsx	Sample project data
requirements.txt	Python dependencies
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

python -m streamlit run dashboardV2.py

Current Capabilities
Automated project health scoring
Interactive project dashboard
KPI and phase-level reporting
Schedule visualization with a Gantt chart
Upcoming and late-task reporting
Invalid date-range detection
Rule-based Project Advisor
Modular data and advisor components
Data

The included Excel workbook contains fictional demonstration data.

Do not replace the sample workbook with confidential, proprietary, customer, controlled, or otherwise sensitive data in a public repository.

Future Enhancements
Microsoft Graph integration
Automated Microsoft Planner synchronization
Connection to an approved AI model
AI-generated executive summaries
Natural-language project analysis
Automated status-report generation
Additional filtering and export options
Learning Objectives

This project was created to strengthen practical skills in:

Python development
Data analysis
Data visualization
Streamlit development
Modular application architecture
Git and GitHub workflows
Project-management analytics
AI-assisted project-management concepts
Disclaimer

This project is a learning and portfolio demonstration. It is not a production Microsoft Planner integration, and the current Project Advisor uses programmed response logic rather than a connected generative AI model.

For the short repository description at the top of GitHub, use:

Python and Streamlit dashboard for project health reporting, schedule visualization, KPI tracking, and AI-assisted project insights.
