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
from api.fuel_calculator.calculation import router as calculation_router_fuel_calculation
from api.logs.collection import router as collection_router_logs

# Logs
from api.logs.create import router as create_router_logs

# Outstanding_money
from api.outstanding_money.collection import router as collection_router_outstanding_money
from api.outstanding_money.create import router as create_router_outstanding_money
from api.outstanding_money.delete import router as delete_router_outstanding_money
from api.outstanding_money.update import router as update_router_outstanding_money
from api.patryk_router.calculator_work.calculator import router as patryk_router_calculations

# Patryk_router
from api.patryk_router.calculator_work.one import router as patryk_router
from api.patryk_router.calculator_work.update import router as patryk_router_update
from api.patryk_router.pdfFilter.create import router as create_router_pdf_filter
from api.tasks.collection import router as collection_router_task

# Tasks
from api.tasks.create import router as create_router_task
from api.tasks.delete import router as delete_router_task
from api.tasks.statistics import router as statistics_router_task
from api.tasks.update import router as update_router_task

api_router = APIRouter()

# Login
api_router.include_router(login_router, tags=["Auth"])

# Patryk
api_router.include_router(patryk_router, tags=["Patryk/Calculator"])
api_router.include_router(patryk_router_update, tags=["Patryk/Calculator"])
api_router.include_router(patryk_router_calculations, tags=["Patryk/Calculator"])

# Pdf_filter_patryk
api_router.include_router(create_router_pdf_filter, tags=["Patryk/PdfFilter"])

# Outstanding_money
api_router.include_router(collection_router_outstanding_money, tags=["OutstandingMoney"])
api_router.include_router(create_router_outstanding_money, tags=["OutstandingMoney"])
api_router.include_router(update_router_outstanding_money, tags=["OutstandingMoney"])
api_router.include_router(delete_router_outstanding_money, tags=["OutstandingMoney"])

# Logs
api_router.include_router(collection_router_logs, tags=["Logs"])
api_router.include_router(create_router_logs, tags=["Logs"])

# Fuel_calculator
api_router.include_router(calculation_router_fuel_calculation, tags=["FuelCalculator"])

# Tasks
api_router.include_router(create_router_task, tags=["Tasks"])
api_router.include_router(collection_router_task, tags=["Tasks"])
api_router.include_router(update_router_task, tags=["Tasks"])
api_router.include_router(delete_router_task, tags=["Tasks"])
api_router.include_router(statistics_router_task, tags=["Tasks"])

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
