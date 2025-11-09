# KAIZEN: CSR & Sustainability Impact Tracker

**Team:** KAIZEN
<br>
**Authors:** Meriem Aoudia & Maha Junaid Ranrawaya

---

## About The Project

**KAIZEN** is a comprehensive Odoo 19 application built for the Odoo Hackathon 2025. Its mission is to transform how organizations manage Corporate Social Responsibility (CSR) by focusing on employee engagement and providing powerful, data-driven analytics for managers.

The module gamifies CSR participation for employees while giving the organization a strategic dashboard to track its impact against the UN Sustainable Development Goals (SDGs) and manage its carbon footprint.

## Core Features

### 1. The Employee Hub
* **My Impact Dashboard:** A personal dashboard where employees can view their "Impact Points," volunteering hours, rank, and progress.
* **Log Activities:** A simple form to submit new volunteering or donation activities for approval.
* **Opportunities Map (Simulated):** A kanban view showing available volunteering events, featuring a simulated OpenStreetMap embed to show nearby opportunities.
* **Rewards & Redemption:** A catalog where employees can spend their earned Impact Points on company perks (e.g., "Extra Impact Day").
* **Share on LinkedIn (Simulated):** A "Share" button on the dashboard that simulates sharing achievements to LinkedIn, amplifying engagement.

### 2. The Strategic CSR Dashboard (Manager)
* **Organization Dashboard:** A high-level kanban view showing total approved activities, total CO₂ offset, and overall carbon budget usage.
* **SDG Impact Grid:** A visual grid of all 17 UN SDGs, color-coded to show which goals the company is contributing to and which are lagging.
* **AI-Powered Recommendations:** A section that identifies the top 3 lagging SDGs and provides strategic recommendations.
* **Strategic Opportunities (Simulated):** Automatically pulls in *simulated* opportunities from "GlobalGiving" that match the company's lagging SDGs.
* **Departmental Carbon Budgets:** A list view to set and track carbon budgets for each department.
* **Activity Validation:** A kanban view for managers to approve or reject employee-submitted activities.

## Technical Stack & Features
* **Framework:** Odoo 19 (Python)
* **Frontend:** Odoo Views (XML), including Kanban Dashboards, Forms, Lists, and embedded HTML/iframes.
* **Key Logic:**
    * **Gamification Engine:** Custom Python logic for calculating points, bonuses, and leaderboard ranks.
    * **Workflow:** Odoo's built-in workflow for activity submission and approval.
* **Simulated API Integrations:**
    * All API simulations are centralized in `models/csr_utils.py` for a stable, reliable demo.
    * **AI (Gemini):** Simulated function to auto-classify activities into UN SDGs.
    * **Carbon Interface:** Simulated function to calculate CO₂ offset for environmental activities.
    * **GlobalGiving:** Simulated function to fetch strategic volunteering opportunities.
    * **LinkedIn:** Simulated function to "share" employee achievements from the dashboard.
    * **OpenStreetMap:** A static iframe embed (no API key needed) simulates a live map of events.

## Installation

1.  Clone this repository into your Odoo `addons` directory.
2.  Ensure all dependencies in `__manifest__.py` are met (e.g., `hr`, `mail`).
3.  Restart your Odoo server.
4.  Navigate to **Apps** in your Odoo instance.
5.  Click **Update Apps List**.
6.  Find "KAIZEN: CSR & Sustainability Tracker" and click **Install**.
