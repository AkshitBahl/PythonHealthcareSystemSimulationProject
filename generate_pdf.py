#!/usr/bin/env python3
"""
Generate project report PDF using fpdf2.
Produces a clean, academic-style A4 document.
"""
from fpdf import FPDF


class ReportPDF(FPDF):
    """Custom PDF class with header/footer."""

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, "Healthcare System Simulator - Project Report", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(20, 20, 20)
        self.ln(4)
        self.cell(0, 8, title)
        self.ln(6)
        # Draw a line
        self.set_draw_color(180, 180, 180)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.ln(2)
        self.cell(0, 7, title)
        self.ln(6)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        x = self.get_x()
        self.set_x(x + indent)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(4, 5, "-")
        self.multi_cell(0, 5, text)
        self.set_x(x)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 4.5, text, fill=True)
        self.ln(3)

    def table_row(self, cols, widths, bold=False, fill=False):
        style = "B" if bold else ""
        if fill:
            self.set_fill_color(240, 240, 240)
        self.set_font("Helvetica", style, 9)
        self.set_text_color(30, 30, 30)
        h = 6
        for i, col in enumerate(cols):
            self.cell(widths[i], h, col, border=1, fill=fill)
        self.ln(h)


def build_report():
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ---- PAGE 1: Title Page ----
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "Healthcare System Simulator", align="C")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Project Report", align="C")
    pdf.ln(20)

    pdf.set_draw_color(180, 180, 180)
    pdf.line(60, pdf.get_y(), pdf.w - 60, pdf.get_y())
    pdf.ln(16)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, "Course: Advanced Programming Concepts (APC)", align="C")
    pdf.ln(10)
    pdf.cell(0, 8, "Group Members:", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Akshit Bahl  |  Divyansh Singh  |  Hiba Chehab", align="C")
    pdf.ln(14)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "May 2026", align="C")

    # ---- PAGE 2: Introduction & Project Structure ----
    pdf.add_page()

    pdf.section_title("1. Introduction")
    pdf.body_text(
        "This report documents the design and implementation of a Healthcare System Simulator "
        "developed as a group project for the Advanced Programming Concepts course. The system "
        "simulates a network of hospitals, pharmacies, doctors, and patients, and operates in "
        "two modes: Normal Operations and Pandemic Response."
    )
    pdf.body_text(
        "The project is structured as a client-server application with a Python simulation "
        "engine (backend) exposing a REST API via FastAPI, and a Next.js (React) dashboard "
        "(frontend) that visualizes the simulation state. The primary objective is to demonstrate "
        "Object-Oriented Programming principles (inheritance, encapsulation, polymorphism, "
        "composition) alongside functional programming constructs (map, filter, reduce, "
        "list comprehensions)."
    )

    pdf.section_title("2. Project Structure")
    pdf.body_text("The project is organized into three logical layers:")
    pdf.code_block(
        "PythonHealthcareSystemSimulationProject/\n"
        "  Main.py                    # Launcher (starts both servers)\n"
        "  requirements.txt           # Python dependencies\n"
        "  backend/\n"
        "    app.py                   # FastAPI app + CORS config\n"
        "    config.py                # Global constants\n"
        "    api/routes.py            # REST API endpoints\n"
        "    engine/\n"
        "      simulation.py          # Core simulation engine\n"
        "      pandemic.py            # Pandemic infection logic\n"
        "    models/\n"
        "      person.py              # Person, Patient, Doctor\n"
        "      facility.py            # Facility, Hospital, Pharmacy\n"
        "      simulation_mode.py     # SimulationMode (Strategy)\n"
        "  frontend/src/app/\n"
        "    page.js                  # Dashboard\n"
        "    hospitals/patients/pharmacy/pandemic/  # Sub-pages\n"
        "    components/              # Reusable UI components\n"
        "    hooks/useSimulation.js   # API communication hook"
    )

    # ---- OOP Design ----
    pdf.section_title("3. OOP Design and Class Hierarchy")

    pdf.sub_title("Person Hierarchy (backend/models/person.py)")
    pdf.bullet("Person - Base class with shared attributes (id, name, age, gender, contact) and a get_info() serialization method.")
    pdf.bullet("Patient(Person) - Extends Person with health_status (Healthy/Infected/Deceased), immunity, days_infected, treatments_received, admitted status. Key methods: infect(), update_health(), admit(), discharge(), treat().")
    pdf.bullet("Doctor(Person) - Extends Person with assigned_facility, assigned_patients, max_patients. Methods: assign_patient(), remove_patient(), diagnose().")

    pdf.sub_title("Facility Hierarchy (backend/models/facility.py)")
    pdf.bullet("Facility - Base class with id, name, location, facility_type, active. Provides get_status().")
    pdf.bullet("Hospital(Facility) - Bed management with total_beds, base_beds. Uses @property for computed attributes (occupied_beds, available_beds). Methods: admit_patient(), discharge_patient(), apply_surge_capacity().")
    pdf.bullet("Pharmacy(Facility) - Medication inventory (dict mapping names to stock counts). Methods: fill_prescription(), reset_daily_count().")

    pdf.sub_title("Other Classes")
    pdf.bullet("SimulationMode (backend/models/simulation_mode.py) - Implements a Strategy-like pattern with mode-specific parameters (infection_rate, surge_capacity_multiplier). Methods: set_mode(), toggle(), is_pandemic property.")
    pdf.bullet("HealthcareSimulation (backend/engine/simulation.py) - Central orchestrator composing all entities. Manages the full simulation lifecycle via daily tick() calls.")
    pdf.bullet("PandemicEngine (backend/engine/pandemic.py) - Handles pandemic-specific logic: infection seeding, daily spread, SIR counting, death tracking.")

    pdf.sub_title("OOP Principles Demonstrated")
    w = [42, 128]
    pdf.table_row(["Principle", "Where Applied"], w, bold=True, fill=True)
    pdf.table_row(["Inheritance", "Patient/Doctor extend Person; Hospital/Pharmacy extend Facility"], w)
    pdf.table_row(["Encapsulation", "Each class manages its own state (e.g., Patient.treat() handles immunity/status)"], w)
    pdf.table_row(["Polymorphism", "Patient and Doctor override to_dict() from Person.get_info()"], w)
    pdf.table_row(["Composition", "HealthcareSimulation composes Patient, Doctor, Hospital, Pharmacy lists"], w)
    pdf.table_row(["Properties", "Hospital.occupied_beds/@property for computed read-only attributes"], w)

    # ---- Functional Programming ----
    pdf.section_title("4. Functional Programming Concepts")
    pdf.bullet("map() - Used in get_state() to serialize all entities: list(map(lambda p: p.to_dict(), self.patients)). Also in tick() to apply health updates to all patients.")
    pdf.bullet("filter() - Used in tick() to find infected unadmitted patients for admission and healthy/deceased admitted patients for discharge. Also in PandemicEngine for susceptible patients.")
    pdf.bullet("reduce() - Used in get_state() to aggregate total occupied beds, capacity, and medication stock across all hospitals and pharmacies via functools.reduce.")
    pdf.bullet("List Comprehensions - Used extensively: filtering available hospitals, finding doctors at a facility, counting statuses, building inventory lists, constructing API responses.")

    # ---- Core Functionalities ----
    pdf.section_title("5. Core Functionalities")

    pdf.sub_title("5.1 Simulation Engine")
    pdf.body_text(
        "The simulation engine initializes a population of 50 patients, 12 doctors, 3 hospitals, "
        "and 2 pharmacies. Each tick() call advances the simulation by one day:"
    )
    pdf.bullet("1. Reset daily pharmacy prescription counters.")
    pdf.bullet("2. Pandemic seeding: On the first pandemic tick, 5 healthy patients are infected and hospital beds increase by 50%.")
    pdf.bullet("3. Health updates: In normal mode, 2% of healthy patients are infected. In pandemic mode, 15% infection rate via PandemicEngine.")
    pdf.bullet("4. Admissions: Infected non-admitted patients are admitted to the first hospital with available beds and doctors.")
    pdf.bullet("5. Treatment: Each admitted infected patient receives 1 medication and immunity +0.10. Recovery if immunity > 0.50, death after 2 failed treatments.")
    pdf.bullet("6. Discharges: Healthy or deceased patients are discharged.")

    pdf.sub_title("5.2 Normal vs. Pandemic Mode")
    w2 = [56, 56, 56]
    pdf.table_row(["Parameter", "Normal", "Pandemic"], w2, bold=True, fill=True)
    pdf.table_row(["Infection rate", "2%", "15%"], w2)
    pdf.table_row(["Surge capacity", "1.0x", "1.5x"], w2)

    pdf.sub_title("5.3 REST API Endpoints")
    w3 = [22, 55, 93]
    pdf.table_row(["Method", "Endpoint", "Description"], w3, bold=True, fill=True)
    pdf.table_row(["GET", "/api/status", "Full simulation state snapshot"], w3)
    pdf.table_row(["GET", "/api/hospitals", "All hospitals with occupancy data"], w3)
    pdf.table_row(["GET", "/api/hospitals/{id}", "Single hospital with patients/doctors"], w3)
    pdf.table_row(["GET", "/api/patients", "All patients with health status"], w3)
    pdf.table_row(["GET", "/api/doctors", "All doctors with assignments"], w3)
    pdf.table_row(["GET", "/api/pharmacy", "Pharmacy inventory status"], w3)
    pdf.table_row(["POST", "/api/mode", "Switch Normal/Pandemic mode"], w3)
    pdf.table_row(["POST", "/api/simulation/tick", "Advance simulation by one day"], w3)
    pdf.table_row(["POST", "/api/simulation/reset", "Reset simulation to Day 0"], w3)

    pdf.sub_title("5.4 Frontend Dashboard")
    pdf.body_text(
        "The frontend is a multi-page Next.js application with five views: Dashboard (KPI cards "
        "and bed occupancy chart), Hospitals (per-hospital detail cards with occupancy bars), "
        "Patients (sortable/filterable registry table), Pharmacy (medication inventory grid), "
        "and Pandemic (SIR compartment cards and infection statistics). A custom React hook "
        "(useSimulation) handles all API communication."
    )

    pdf.sub_title("5.5 Launcher Script (Main.py)")
    pdf.body_text(
        "Main.py provides a single-command launch: it checks/installs Python and Node dependencies, "
        "starts the FastAPI backend on port 8000, starts Next.js on port 3000, opens the browser, "
        "and gracefully terminates both servers on exit."
    )

    # ---- Contributions ----
    pdf.section_title("6. Group Member Contributions")
    pdf.body_text(
        "The work was distributed among three group members. The focus below is on backend "
        "contributions, as OOP is the core concept of this course."
    )

    pdf.sub_title("Akshit Bahl")
    pdf.bullet("OOP Model Design: Designed the class hierarchy - Person base class and its subclasses Patient and Doctor (backend/models/person.py), including health state machine logic (update_health, treat, infect), immunity system, and admission/discharge workflow.")
    pdf.bullet("Facility Classes: Implemented Facility base class and subclasses Hospital and Pharmacy (backend/models/facility.py), including bed management with @property decorators, occupancy rate calculation, and pharmacy inventory system.")
    pdf.bullet("UML Class Diagram: Created the UML class diagram documenting the OOP hierarchy.")
    pdf.bullet("Project Setup: Set up the project structure, Git repository, and Main.py launcher.")

    pdf.sub_title("Divyansh Singh")
    pdf.bullet("Simulation Engine: Implemented HealthcareSimulation (backend/engine/simulation.py) - daily tick() loop, patient population generation, doctor assignment, hospital admission logic, treatment workflow, discharge management.")
    pdf.bullet("Functional Programming: Implemented all map(), filter(), reduce(), and list comprehension usages across the simulation engine and state serialization.")
    pdf.bullet("REST API: Designed FastAPI routes (backend/api/routes.py), app setup with CORS (backend/app.py), and configuration module (backend/config.py).")
    pdf.bullet("Frontend: Built all five dashboard pages, reusable components (StatCard, BedChart, PatientTable, Sidebar), useSimulation hook, and CSS design system.")

    pdf.sub_title("Hiba Chehab")
    pdf.bullet("SimulationMode (Strategy Pattern): Designed SimulationMode class (backend/models/simulation_mode.py) with mode parameter dictionary, set_mode()/toggle() methods, and is_pandemic property.")
    pdf.bullet("Pandemic Engine: Implemented PandemicEngine class (backend/engine/pandemic.py) - infection seeding, daily spread logic, SIR compartment counting, and death tracking.")
    pdf.bullet("Mode Switching Logic: Implemented mode-switching workflow in HealthcareSimulation.set_mode(), including pandemic state reset and surge capacity activation/deactivation.")
    pdf.bullet("Testing and Documentation: Tested the simulation across different scenarios, verified edge cases, and contributed to project documentation.")

    # ---- Packages ----
    pdf.section_title("7. Required Packages and Materials")

    pdf.sub_title("Python Backend Dependencies (requirements.txt)")
    w4 = [40, 25, 105]
    pdf.table_row(["Package", "Version", "Purpose"], w4, bold=True, fill=True)
    pdf.table_row(["fastapi", "latest", "High-performance async web framework for REST API"], w4)
    pdf.table_row(["uvicorn", "latest", "ASGI server to run the FastAPI application"], w4)
    pdf.table_row(["pydantic", "latest", "Data validation and serialization (FastAPI dep)"], w4)

    pdf.body_text(
        "Python Standard Library modules used: uuid, random, functools (reduce), typing, os, sys, "
        "time, subprocess, webbrowser, pathlib."
    )

    pdf.sub_title("Frontend Dependencies (package.json)")
    pdf.table_row(["Package", "Version", "Purpose"], w4, bold=True, fill=True)
    pdf.table_row(["next", "16.2.3", "React-based framework for the web dashboard"], w4)
    pdf.table_row(["react", "19.2.4", "UI component library"], w4)
    pdf.table_row(["react-dom", "19.2.4", "React DOM rendering"], w4)
    pdf.table_row(["recharts", "^3.8.1", "Chart library for bed occupancy visualization"], w4)
    pdf.table_row(["eslint", "^9", "Code linting (dev dependency)"], w4)

    pdf.sub_title("System Requirements")
    pdf.bullet("Python 3.10 or later")
    pdf.bullet("Node.js (LTS recommended) and npm")
    pdf.bullet("A modern web browser")

    pdf.sub_title("Supplementary Materials")
    w5 = [50, 120]
    pdf.table_row(["File", "Description"], w5, bold=True, fill=True)
    pdf.table_row(["Main.py", "Unified launcher script - starts both backend and frontend"], w5)
    pdf.table_row(["UML_class.png", "UML class diagram of the OOP hierarchy"], w5)
    pdf.table_row(["README.md", "Project overview with quick-start instructions"], w5)
    pdf.table_row(["project_workflow.md", "Detailed workflow documentation"], w5)

    # ---- How to Run ----
    pdf.section_title("8. How to Run")
    pdf.code_block(
        "# Navigate to the project directory\n"
        "cd PythonHealthcareSystemSimulationProject\n\n"
        "# Run everything with a single command:\n"
        "python Main.py"
    )
    pdf.body_text(
        "The launcher will automatically install any missing dependencies and open the dashboard "
        "at http://localhost:3000. The FastAPI backend runs at http://localhost:8000 with "
        "interactive API docs at http://localhost:8000/docs."
    )

    # ---- Conclusion ----
    pdf.section_title("9. Conclusion")
    pdf.body_text(
        "This project demonstrates a comprehensive application of Object-Oriented Programming "
        "principles in Python through a healthcare simulation system. The class hierarchy models "
        "real-world entities (Person, Patient, Doctor, Facility, Hospital, Pharmacy) with proper "
        "inheritance, encapsulation, and composition. Functional programming constructs (map, filter, "
        "reduce, list comprehensions) are used throughout the simulation engine. The Strategy pattern, "
        "implemented via SimulationMode, allows dynamic switching between Normal and Pandemic modes "
        "at runtime. The REST API and web dashboard provide a clear interface for interacting with "
        "and visualizing the simulation state."
    )

    # Save
    pdf.output("report.pdf")
    print(f"Generated report.pdf ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build_report()
