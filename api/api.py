from fastapi import APIRouter

# login
from api.auth.login import router as login_router
from api.calendar.collection import router as collection_router_calendary

# Calendar Condition
from api.calendar.condition.collection import router as collection_router_calendar_condition
from api.calendar.condition.create import router as create_router_condition
from api.calendar.condition.delete import router as delete_router_condition
from api.calendar.condition.update import router as update_router_condition

# Calendar
from api.calendar.create import router as create_router_calendary

# Calendar Day
from api.calendar.days.update import router as update_router_days
from api.calendar.statistics import router as statistics_router_statistics

# Calculator
from api.endpoints.fuel_calculator.calculation import router as calculation_router_fuel_calculation

# Logs
from api.endpoints.logs.collection import router as collection_router_logs

# Patryk_router
from api.endpoints.patryk_router.calculator_work.calculator import router as patryk_router_calculations
from api.endpoints.patryk_router.calculator_work.one import router as patryk_router
from api.endpoints.patryk_router.calculator_work.update import router as patryk_router_update
from api.endpoints.tasks.collection import router as collection_router_task

# Tasks
from api.endpoints.tasks.create import router as create_router_task
from api.endpoints.tasks.delete import router as delete_router_task
from api.endpoints.tasks.statistics import router as statistics_router_task
from api.endpoints.tasks.update import router as update_router_task

# Outstanding_money
from api.outstanding_money.collection import router as collection_router_outstanding_money
from api.outstanding_money.create import router as create_router_outstanding_money
from api.outstanding_money.delete import router as delete_router_outstanding_money
from api.outstanding_money.update import router as update_router_outstanding_money

api_router = APIRouter()

# Login
api_router.include_router(login_router, tags=["Auth"])

# Patryk (tag deklaruje endpoint)
api_router.include_router(patryk_router)
api_router.include_router(patryk_router_update)
api_router.include_router(patryk_router_calculations)

# Outstanding_money
api_router.include_router(collection_router_outstanding_money, tags=["OutstandingMoney"])
api_router.include_router(create_router_outstanding_money, tags=["OutstandingMoney"])
api_router.include_router(update_router_outstanding_money, tags=["OutstandingMoney"])
api_router.include_router(delete_router_outstanding_money, tags=["OutstandingMoney"])

# Logs (tag deklaruje endpoint)
api_router.include_router(collection_router_logs)

# Fuel_calculator (tag deklaruje endpoint)
api_router.include_router(calculation_router_fuel_calculation)

# Tasks (tagi deklarują endpointy — wzorzec ARCHITEKTURA.md)
api_router.include_router(create_router_task)
api_router.include_router(collection_router_task)
api_router.include_router(update_router_task)
api_router.include_router(delete_router_task)
api_router.include_router(statistics_router_task)

# Calendar Condition
api_router.include_router(collection_router_calendar_condition, tags=["Calendar/Conditions"])
api_router.include_router(create_router_condition, tags=["Calendar/Conditions"])
api_router.include_router(update_router_condition, tags=["Calendar/Conditions"])
api_router.include_router(delete_router_condition, tags=["Calendar/Conditions"])

# Calendar
api_router.include_router(create_router_calendary, tags=["Calendar"])
api_router.include_router(collection_router_calendary, tags=["Calendar"])
api_router.include_router(statistics_router_statistics, tags=["Calendar"])

# Calendar Day
api_router.include_router(update_router_days, tags=["Calendar/Days"])
