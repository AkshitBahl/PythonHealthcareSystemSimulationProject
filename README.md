# Python Healthcare System Simulator

An ultimate healthcare-based medical system simulation. It mimics the functionality of a network of hospitals, pharmacies, and patients using an Object-Oriented approach. It operates in two scenarios: **Normal Operations** and **Pandemic Response**.

Features a **Python FastAPI** backend simulation engine and a **Next.js** real-time data dashboard. They communicate over WebSockets to provide dynamic, live updates of bed occupancies, infection curves, and resource management.

## 🚀 Quick Start
Run the whole application with a single command. The script will automatically check and install any missing required packages (pip/npm) and launch both servers.

```bash
python Main.py
```
*Wait ~5 seconds, and a browser window will open tracking the live simulation at `http://localhost:3000`.*

---

## 🏗️ Technical Architecture

*   **Backend:** Python 3, FastAPI, Uvicorn (ASGI server), WebSockets.
*   **Frontend:** Next.js (React), Recharts (data visualization), standard CSS (no external CSS frameworks like Tailwind used to strictly follow guidelines).
*   **Paradigm:** Object-Oriented Programming (OOP) in Python.

### Class Hierarchy and OOP Details

The codebase is heavily constructed around inheritance and distinct entity encapsulation.

*   `Person(Base)`
    *   `Patient`: Tracks health, infections, immunity, and handles medical histories.
    *   `Doctor`: Assigns patients, triggers diagnosis, generates prescriptions.
    *   `Nurse`: Cares for patients to slightly boost recovery variables.
*   `Facility(Base)`
    *   `Hospital`: Handles physical capacity (beds, ICU), and patient admissions/discharges.
    *   `Pharmacy`: Managed independent inventories of `Medication` via `InventoryManager`. Uses logic to fill prescriptions.
    *   `Clinic`: Used for assigning outpatient cases.
*   `SimulationMode`: Dynamically modifies global infection parameters, multiplier capacities, and operational rules dynamically.

**Notable Functional Python Concepts utilized:**
*   **Multiple Instantiation**: Specifically tracked via the `HealthcareSimulation` class (`backend.engine.simulation`). Automatically breeds 50+ `Patient` entities, 10 `Doctor` objects, multiple facilities.
*   **List Comprehension**: Extensively used formatting dictionaries, extracting objects via identifiers, and building fast logic trees (e.g., getting specific IDs in `backend/api/routes.py` and tracking data in `backend/engine/statistics.py`).
*   **`map()`**: Converting complex class structures to serialized dictionary data across lists (`backend.engine.simulation.get_state()`), batch updating day progress for all patients.
*   **`filter()`**: Fast subset extractions (e.g., only getting low-stock data `backend.models.inventory`, isolating infected patients inside the pandemic logic).
*   **`reduce()`**: Cross-calculating summation aggregates (e.g., adding available beds across the network via `functools.reduce` in `backend.engine.statistics.py`).

---

## 🦠 Scenarios and Logic

### Normal Operations
*   Small population chance of minor illnesses.
*   Patients visit facilities, doctors prescribe care, pharmacies decrement usage.
*   System resets and operates cleanly inside expected bounds.

### Pandemic Response
Activation triggers the `PandemicEngine` applying a core **SIR Model** (Susceptible-Infected-Recovered).
*   Infection rates spike based on calculated immunity values inside the `Patient` instances.
*   Surge capacity logic triggers across `Hospital` objects (+50% capacity buffers).
*   Dynamic real-time visualizations display Infection Curves vs ICU Bed availability curves.

## Package List
*   `fastapi` - High-performance web framework.
*   `uvicorn[standard]` - High-performance ASGI server for FastAPI.
*   `websockets` - Enables two-way communication between the engine and UI.
*   `pydantic` - Data serialization inside FastAPI.
*   `next` / `react` / `recharts` - Display interface libraries.
