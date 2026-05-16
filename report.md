# Healthcare System Simulator — Project Report

**Course:** Advanced Programming Concepts (APC)

**Group Members:** Akshit Bahl, Divyansh Singh, Hiba Chehab

**Date:** May 2026

---

## 1. Introduction

This report documents the design and implementation of a **Healthcare System Simulator** developed as a group project for the Advanced Programming Concepts course. The system simulates a network of hospitals, pharmacies, doctors, and patients, and operates in two modes: **Normal Operations** and **Pandemic Response**.

The project is structured as a client–server application:

- **Backend** — A Python simulation engine exposing a REST API via FastAPI.
- **Frontend** — A Next.js (React) dashboard that visualizes the simulation state in real time.

The primary objective is to demonstrate Object-Oriented Programming principles — inheritance, encapsulation, polymorphism, and composition — alongside functional programming constructs such as `map()`, `filter()`, `reduce()`, and list comprehensions.

---

## 2. Project Structure

The project is organized into three logical layers:

```
PythonHealthcareSystemSimulationProject/
├── Main.py                  # Launcher script (starts both servers)
├── requirements.txt         # Python dependencies
├── backend/
│   ├── app.py               # FastAPI app initialization and CORS
│   ├── config.py            # Global constants (ports, population size)
│   ├── api/
│   │   └── routes.py        # REST API endpoint definitions
│   ├── engine/
│   │   ├── simulation.py    # Core simulation engine (HealthcareSimulation)
│   │   └── pandemic.py      # Pandemic-specific infection logic
│   └── models/
│       ├── person.py        # Person → Patient, Doctor classes
│       ├── facility.py      # Facility → Hospital, Pharmacy classes
│       └── simulation_mode.py  # SimulationMode (Strategy pattern)
└── frontend/
    ├── package.json         # Node.js dependencies
    └── src/app/
        ├── page.js          # Dashboard page
        ├── hospitals/       # Hospitals detail page
        ├── patients/        # Patient registry page
        ├── pharmacy/        # Pharmacy inventory page
        ├── pandemic/        # Pandemic monitoring page
        ├── components/      # Reusable UI components
        └── hooks/           # Custom React hook for API communication
```

---

## 3. OOP Design and Class Hierarchy

The backbone of the project is a clean class hierarchy that models real-world healthcare entities. The following UML class diagram illustrates the relationships:

**Person Hierarchy** (`backend/models/person.py`):

- **`Person`** — Abstract base class with shared attributes (`id`, `name`, `age`, `gender`, `contact`) and a `get_info()` serialization method.
- **`Patient(Person)`** — Extends `Person` with health-specific attributes: `health_status` (Healthy/Infected/Deceased), `immunity`, `days_infected`, `treatments_received`, `admitted`, `assigned_doctor`, and `assigned_facility`. Key methods include `infect()`, `update_health()`, `admit()`, `discharge()`, and `treat()`.
- **`Doctor(Person)`** — Extends `Person` with doctor-specific attributes: `assigned_facility`, `assigned_patients`, `max_patients`, and `available`. Methods include `assign_patient()`, `remove_patient()`, and `diagnose()`.

**Facility Hierarchy** (`backend/models/facility.py`):

- **`Facility`** — Base class with shared attributes (`id`, `name`, `location`, `facility_type`, `active`) and a `get_status()` method.
- **`Hospital(Facility)`** — Extends `Facility` with bed management: `total_beds`, `base_beds`, `doctors`, `patients`. Uses Python `@property` decorators for computed attributes (`occupied_beds`, `available_beds`). Key methods include `admit_patient()`, `discharge_patient()`, `apply_surge_capacity()`, and `get_occupancy_rate()`.
- **`Pharmacy(Facility)`** — Extends `Facility` with medication inventory management. Maintains a dictionary of medication stocks and tracks prescriptions via `fill_prescription()` and `reset_daily_count()`.

**Simulation Configuration** (`backend/models/simulation_mode.py`):

- **`SimulationMode`** — Implements a Strategy-like pattern. Stores mode-specific parameters (infection rate, surge capacity multiplier) in a class-level dictionary `MODE_PARAMS`. Exposes `set_mode()`, `toggle()`, and `is_pandemic` property for dynamic runtime configuration.

**Engine Classes** (`backend/engine/`):

- **`HealthcareSimulation`** — Central orchestrator that composes `Patient`, `Doctor`, `Hospital`, `Pharmacy`, `SimulationMode`, and `PandemicEngine` objects. Manages the full simulation lifecycle through daily `tick()` calls.
- **`PandemicEngine`** — Dedicated class handling pandemic-specific logic: initial infection seeding (`seed_infection()`), daily infection spread (`spread_infection()`), and SIR (Susceptible–Infected–Recovered) compartment counting (`get_sir_counts()`).

### OOP Principles Demonstrated

| Principle | Where Applied |
|---|---|
| **Inheritance** | `Patient` and `Doctor` extend `Person`; `Hospital` and `Pharmacy` extend `Facility` |
| **Encapsulation** | Each class manages its own state. `Patient.treat()` internally handles immunity changes and status transitions |
| **Polymorphism** | Both `Patient` and `Doctor` override `to_dict()` from the base `Person.get_info()`. Similarly for facilities |
| **Composition** | `HealthcareSimulation` composes lists of `Patient`, `Doctor`, `Hospital`, `Pharmacy`, plus a `SimulationMode` and `PandemicEngine` |
| **Properties** | `Hospital.occupied_beds` and `Hospital.available_beds` use `@property` decorators for computed read-only attributes |

---

## 4. Functional Programming Concepts

The project uses Python functional programming constructs as required by the course:

- **`map()`** — Used in `HealthcareSimulation.get_state()` to serialize all entity lists to dictionaries (e.g., `list(map(lambda p: p.to_dict(), self.patients))`), and in `tick()` to apply health updates to all patients.
- **`filter()`** — Used in `tick()` to identify patients needing admission (`health_status == "Infected" and not admitted`) and patients eligible for discharge (`admitted and health_status in ("Healthy", "Deceased")`). Also used in `PandemicEngine.spread_infection()` to isolate susceptible patients.
- **`reduce()`** — Used in `get_state()` to aggregate total occupied beds, total capacity, and total medication stock across all hospitals and pharmacies via `functools.reduce`.
- **List Comprehensions** — Used extensively throughout the codebase: filtering available hospitals by bed capacity, finding doctors at a specific facility, counting patient statuses, building inventory lists, and constructing API response dictionaries.

---

## 5. Core Functionalities

### 5.1 Simulation Engine

The simulation engine (`HealthcareSimulation`) initializes a population of 50 patients, 12 doctors, 3 hospitals, and 2 pharmacies. Each call to `tick()` advances the simulation by one day and performs the following operations in order:

1. **Reset daily counters** — Pharmacy daily prescription counts are reset.
2. **Pandemic seeding** — On the first pandemic-mode tick, 5 random healthy patients are infected and hospital surge capacity is activated (+50% beds).
3. **Health updates** — In normal mode, `map()` applies `update_health()` to all patients, and 2% of healthy patients are randomly infected. In pandemic mode, the `PandemicEngine` handles infection spread at a 15% rate.
4. **Hospital admissions** — `filter()` identifies infected, non-admitted patients. Each is admitted to the first available hospital with an available doctor.
5. **Treatment** — Admitted infected patients receive one medication from a pharmacy and one treatment session. Each treatment boosts immunity by 0.10. If immunity exceeds 0.50, the patient recovers. If 2 treatments are reached without recovery, the patient is marked deceased.
6. **Discharges** — Patients who are now healthy or deceased are discharged from their hospital and doctor.

### 5.2 Normal vs. Pandemic Mode

The `SimulationMode` class defines parameters for each mode:

| Parameter | Normal | Pandemic |
|---|---|---|
| Infection rate | 2% | 15% |
| Surge capacity multiplier | 1.0x | 1.5x |

Mode switching is handled at runtime through the REST API. When switching to pandemic mode, initial infections are seeded and hospitals gain additional bed capacity. When switching back to normal, pandemic state is reset and hospital beds revert to base capacity.

### 5.3 REST API

The backend exposes a RESTful API via FastAPI with the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/status` | Full simulation state snapshot |
| GET | `/api/hospitals` | All hospitals with occupancy data |
| GET | `/api/hospitals/{id}` | Single hospital detail with patients and doctors |
| GET | `/api/patients` | All patients with health status |
| GET | `/api/doctors` | All doctors with assignments |
| GET | `/api/pharmacy` | Pharmacy inventory status |
| POST | `/api/mode` | Switch between Normal and Pandemic mode |
| POST | `/api/simulation/tick` | Advance simulation by one day |
| POST | `/api/simulation/reset` | Reset simulation to Day 0 |

CORS middleware is configured to allow cross-origin requests from the Next.js frontend running on port 3000.

### 5.4 Frontend Dashboard

The frontend is a multi-page Next.js application with five views:

- **Dashboard** — Overview with KPI cards (patients, beds, infections, pharmacy stock, hospitals, current day) and a bed occupancy bar chart.
- **Hospitals** — Per-hospital detail cards showing bed/ICU/ventilator counts, occupancy progress bars, and assigned doctors.
- **Patients** — Sortable and filterable patient registry table with status badges and immunity levels.
- **Pharmacy** — Medication inventory grid for each pharmacy with stock levels and low-stock indicators.
- **Pandemic** — Pandemic-specific monitoring with SIR compartment cards, infection/death statistics, and active pandemic parameters.

A custom React hook (`useSimulation`) handles all API communication, fetching state on mount and after user actions (tick, reset, mode toggle).

### 5.5 Launcher Script

`Main.py` provides a single-command launch experience:

1. Checks and installs Python dependencies from `requirements.txt`.
2. Checks and installs Node.js dependencies via `npm install`.
3. Starts the FastAPI backend on port 8000 using Uvicorn.
4. Starts the Next.js frontend on port 3000.
5. Opens the browser automatically after a 5-second delay.
6. Gracefully terminates both processes on exit.

---

## 6. Group Member Contributions

The work was distributed among three group members. The focus below is on backend contributions, as OOP is the core concept of this course.

### Akshit Bahl

- **OOP Model Design**: Designed and implemented the class hierarchy — the `Person` base class and its subclasses `Patient` and `Doctor` (`backend/models/person.py`), including the health state machine logic (`update_health()`, `treat()`, `infect()`), immunity system, and the admission/discharge workflow.
- **Facility Classes**: Implemented the `Facility` base class and its subclasses `Hospital` and `Pharmacy` (`backend/models/facility.py`), including bed management with `@property` decorators, occupancy rate calculation, and the pharmacy inventory system.
- **UML Class Diagram**: Created the UML class diagram documenting the class hierarchy and relationships.
- **Project Setup**: Set up the project structure, Git repository, and `Main.py` launcher script.

### Divyansh Singh

- **Simulation Engine**: Implemented the core `HealthcareSimulation` class (`backend/engine/simulation.py`) — the daily `tick()` loop, patient population generation, doctor assignment, hospital admission logic, treatment workflow, and discharge management.
- **Functional Programming**: Implemented all `map()`, `filter()`, `reduce()`, and list comprehension usages across the simulation engine and state serialization (`get_state()`).
- **REST API**: Designed and implemented the FastAPI routes (`backend/api/routes.py`), the application setup with CORS middleware (`backend/app.py`), and the configuration module (`backend/config.py`).
- **Frontend**: Built the Next.js dashboard including all five pages (Dashboard, Hospitals, Patients, Pharmacy, Pandemic), reusable components (StatCard, BedChart, PatientTable, Sidebar), and the `useSimulation` hook for API communication. Implemented the CSS design system.

### Hiba Chehab

- **SimulationMode (Strategy Pattern)**: Designed and implemented the `SimulationMode` class (`backend/models/simulation_mode.py`), including the mode parameter dictionary (`MODE_PARAMS`), the `set_mode()` / `toggle()` methods, and the `is_pandemic` property.
- **Pandemic Engine**: Implemented the `PandemicEngine` class (`backend/engine/pandemic.py`) — the infection seeding mechanism (`seed_infection()`), daily infection spread logic (`spread_infection()`), SIR compartment counting (`get_sir_counts()`), and death tracking.
- **Mode Switching Logic**: Implemented the mode-switching workflow in `HealthcareSimulation.set_mode()`, including pandemic state reset and hospital surge capacity activation/deactivation.
- **Testing and Documentation**: Tested the simulation across different scenarios (normal and pandemic), verified edge cases, and contributed to project documentation.

---

## 7. Required Packages and Materials

### Python Backend Dependencies (`requirements.txt`)

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | latest | High-performance async web framework for the REST API |
| `uvicorn` | latest | ASGI server to run the FastAPI application |
| `pydantic` | latest | Data validation and serialization (FastAPI dependency) |

**Python Standard Library modules used:** `uuid`, `random`, `functools` (for `reduce`), `typing`, `os`, `sys`, `time`, `subprocess`, `webbrowser`, `pathlib`.

### Frontend Dependencies (`package.json`)

| Package | Version | Purpose |
|---|---|---|
| `next` | 16.2.3 | React-based framework for the web dashboard |
| `react` | 19.2.4 | UI component library |
| `react-dom` | 19.2.4 | React DOM rendering |
| `recharts` | ^3.8.1 | Chart library for bed occupancy visualization |
| `eslint` | ^9 | Code linting (dev dependency) |
| `eslint-config-next` | 16.2.3 | Next.js ESLint configuration (dev dependency) |

### System Requirements

- Python 3.10 or later
- Node.js (LTS recommended) and npm
- A modern web browser

### Supplementary Materials

| File | Description |
|---|---|
| `Main.py` | Unified launcher script — starts both backend and frontend |
| `UML_class.png` | UML class diagram of the OOP hierarchy |
| `README.md` | Project overview with quick-start instructions |
| `project_workflow.md` | Detailed workflow documentation |
| `.gitignore` | Git ignore rules for Python/Node artifacts |

---

## 8. How to Run

```bash
# Clone the repository and navigate to the project directory
cd PythonHealthcareSystemSimulationProject

# Run everything with a single command:
python Main.py
```

The launcher will automatically install any missing dependencies and open the dashboard at `http://localhost:3000`. The FastAPI backend runs at `http://localhost:8000` with interactive API docs at `http://localhost:8000/docs`.

---

## 9. Conclusion

This project demonstrates a comprehensive application of Object-Oriented Programming principles in Python through a healthcare simulation system. The class hierarchy models real-world entities (Person, Patient, Doctor, Facility, Hospital, Pharmacy) with proper inheritance, encapsulation, and composition. Functional programming constructs (`map`, `filter`, `reduce`, list comprehensions) are used throughout the simulation engine. The Strategy pattern, implemented via `SimulationMode`, allows dynamic switching between Normal and Pandemic operation modes at runtime. The REST API and web dashboard provide a clear interface for interacting with and visualizing the simulation state.
