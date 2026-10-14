# project-health-dashboard
Python and Streamlit dashboard for analyzing Microsoft Planner project data.

# Project Health Dashboard

This project started as a way to learn Python while building something related to my day-to-day work in project management.

The dashboard uses sample Microsoft Planner-style task data to calculate project health metrics, visualize schedules, identify risks, and provide a simple Project Advisor that can answer basic questions using project data.

## What It Does

- Calculates project completion metrics
- Tracks completed, in-progress, and not-started tasks
- Flags late tasks
- Displays project health status
- Visualizes schedules with a Gantt chart
- Summarizes task status by phase
- Provides a basic Project Advisor interface

## Why I Built It

I wanted a project that combined project management concepts with Python, data analysis, visualization, and application development.

This was also an opportunity to learn:

- Python
- Pandas
- Streamlit
- Git and GitHub
- Basic application architecture

## Project Structure

```text
dashboardV2.py      Main dashboard application
planner_client.py   Data loading and preparation
ai_client.py        Project Advisor logic
config.py           Configuration settings
requirements.txt    Project dependencies
