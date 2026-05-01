"""
REST API Routes
===============
Defines all REST endpoints for the healthcare simulation API.

Endpoints:
- GET  /api/status             — Full simulation snapshot
- GET  /api/hospitals           — All hospitals with occupancy
- GET  /api/patients            — All patients with status
- GET  /api/doctors             — All doctors
- GET  /api/pharmacy            — Pharmacy inventory status
- GET  /api/statistics          — Time-series statistics
- POST /api/mode                — Switch Normal ↔ Pandemic
- POST /api/simulation/tick     — Advance one day
- POST /api/simulation/reset    — Reset simulation to Day 0
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api")


def create_routes(simulation):
    """
    Create API routes bound to a simulation instance.

    Args:
        simulation: The HealthcareSimulation instance.

    Returns:
        APIRouter: Configured router with all endpoints.
    """

    @router.get("/status")
    async def get_status():
        """Get the full simulation state snapshot."""
        return simulation.get_state()

    @router.get("/hospitals")
    async def get_hospitals():
        """Get all hospitals with current occupancy data."""
        return {
            "hospitals": [h.to_dict() for h in simulation.hospitals],
            "day": simulation.day,
        }

    @router.get("/hospitals/{hospital_id}")
    async def get_hospital(hospital_id: str):
        """Get a single hospital's details by ID."""
        hospital = next(
            (h for h in simulation.hospitals if h.id == hospital_id), None
        )
        if hospital is None:
            return {"error": "Hospital not found"}, 404

        # List comprehension to get patients assigned to this hospital
        patients = [
            p.to_dict() for p in simulation.patients
            if p.assigned_facility == hospital_id
        ]
        # List comprehension to get doctors assigned to this hospital
        doctors = [
            d.to_dict() for d in simulation.doctors
            if d.assigned_facility == hospital_id
        ]

        result = hospital.to_dict()
        result["patients_detail"] = patients
        result["doctors_detail"] = doctors
        return result

    @router.get("/patients")
    async def get_patients():
        """Get all patients with their current status."""
        return {
            "patients": [p.to_dict() for p in simulation.patients],
            "day": simulation.day,
            "total": len(simulation.patients),
        }

    @router.get("/doctors")
    async def get_doctors():
        """Get all doctors with their assignments."""
        return {
            "doctors": [d.to_dict() for d in simulation.doctors],
            "day": simulation.day,
        }

    @router.get("/pharmacy")
    async def get_pharmacy():
        """Get pharmacy inventory status from all pharmacies."""
        return {
            "pharmacies": [p.to_dict() for p in simulation.pharmacies],
            "day": simulation.day,
        }

    @router.get("/statistics")
    async def get_statistics():
        """Get time-series statistics for all recorded days."""
        return {
            "records": simulation.stats.get_all_records(),
            "summary": simulation.stats.get_summary(),
            "day": simulation.day,
        }

    @router.post("/mode")
    async def set_mode(body: dict):
        """
        Set the simulation mode.

        Request body: { "mode": "normal" | "pandemic" }
        """
        mode = body.get("mode", "normal")
        result = simulation.set_mode(mode)
        return {"success": True, "mode": result}

    @router.post("/simulation/tick")
    async def manual_tick():
        """Advance the simulation by one day."""
        state = simulation.tick()
        return state

    @router.post("/simulation/reset")
    async def reset_simulation():
        """Reset the simulation back to Day 0 with fresh data."""
        simulation.reset()
        return simulation.get_state()

    return router
