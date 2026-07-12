from fastapi import APIRouter

# login
from api.endpoints.auth.login import router as login_router

# Calendar
from api.endpoints.calendar.collection import router as collection_router_calendary

# Calendar Condition
from api.endpoints.calendar.condition.collection import router as collection_router_calendar_condition
from api.endpoints.calendar.condition.create import router as create_router_condition
from api.endpoints.calendar.condition.delete import router as delete_router_condition
from api.endpoints.calendar.condition.update import router as update_router_condition
from api.endpoints.calendar.create import router as create_router_calendary

# Calendar Day
from api.endpoints.calendar.days.update import router as update_router_days
from api.endpoints.calendar.statistics import router as statistics_router_statistics

# Contact (publiczny create + obsluga zgloszen)
from api.endpoints.contact.collection import router as collection_router_contact
from api.endpoints.contact.create import router as create_router_contact
from api.endpoints.contact.delete import router as delete_router_contact
from api.endpoints.contact.one import router as one_router_contact
from api.endpoints.contact.update import router as update_router_contact

# Calculator
from api.endpoints.fuel_calculator.calculation import router as calculation_router_fuel_calculation

# Logs
from api.endpoints.logs.collection import router as collection_router_logs

# Outstanding_money
from api.endpoints.outstanding_money.collection import router as collection_router_outstanding_money
from api.endpoints.outstanding_money.create import router as create_router_outstanding_money
from api.endpoints.outstanding_money.delete import router as delete_router_outstanding_money
from api.endpoints.outstanding_money.update import router as update_router_outstanding_money

# Patryk_router
from api.endpoints.patryk_router.calculator_work.calculator import router as patryk_router_calculations
from api.endpoints.patryk_router.calculator_work.one import router as patryk_router
from api.endpoints.patryk_router.calculator_work.update import router as patryk_router_update

# Rental - billing (okresy, odczyty, preview/close, snapshoty)
from api.endpoints.rental.billing.close import router as close_router_rental_billing
from api.endpoints.rental.billing.collection import router as collection_router_rental_billing
from api.endpoints.rental.billing.create import router as create_router_rental_billing
from api.endpoints.rental.billing.delete import router as delete_router_rental_billing
from api.endpoints.rental.billing.one import router as one_router_rental_billing
from api.endpoints.rental.billing.preview import router as preview_router_rental_billing
from api.endpoints.rental.billing.update import router as update_router_rental_billing

# Rental - słowniki
from api.endpoints.rental.dictionaries.collection import router as collection_router_rental_dictionaries
from api.endpoints.rental.dictionaries.create import router as create_router_rental_dictionaries
from api.endpoints.rental.dictionaries.delete import router as delete_router_rental_dictionaries
from api.endpoints.rental.dictionaries.one import router as one_router_rental_dictionaries
from api.endpoints.rental.dictionaries.update import router as update_router_rental_dictionaries

# Rental - podział rodzinny
from api.endpoints.rental.family.collection import router as collection_router_rental_family
from api.endpoints.rental.family.create import router as create_router_rental_family
from api.endpoints.rental.family.delete import router as delete_router_rental_family
from api.endpoints.rental.family.one import router as one_router_rental_family
from api.endpoints.rental.family.update import router as update_router_rental_family
from api.endpoints.tasks.collection import router as collection_router_task

# Tasks
from api.endpoints.tasks.create import router as create_router_task
from api.endpoints.tasks.delete import router as delete_router_task
from api.endpoints.tasks.statistics import router as statistics_router_task
from api.endpoints.tasks.update import router as update_router_task

api_router = APIRouter()

# Login (tag deklaruje endpoint)
api_router.include_router(login_router)

# Patryk (tag deklaruje endpoint)
api_router.include_router(patryk_router)
api_router.include_router(patryk_router_update)
api_router.include_router(patryk_router_calculations)

# Outstanding_money (tagi deklarują endpointy)
api_router.include_router(collection_router_outstanding_money)
api_router.include_router(create_router_outstanding_money)
api_router.include_router(update_router_outstanding_money)
api_router.include_router(delete_router_outstanding_money)

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

# Calendar Condition (tagi deklarują endpointy)
api_router.include_router(collection_router_calendar_condition)
api_router.include_router(create_router_condition)
api_router.include_router(update_router_condition)
api_router.include_router(delete_router_condition)

# Calendar (tagi deklarują endpointy)
api_router.include_router(create_router_calendary)
api_router.include_router(collection_router_calendary)
api_router.include_router(statistics_router_statistics)

# Calendar Day (tag deklaruje endpoint)
api_router.include_router(update_router_days)

# Rentals - słowniki (tagi deklarują endpointy)
api_router.include_router(create_router_rental_dictionaries)
api_router.include_router(collection_router_rental_dictionaries)
api_router.include_router(one_router_rental_dictionaries)
api_router.include_router(update_router_rental_dictionaries)
api_router.include_router(delete_router_rental_dictionaries)

# Rentals - billing: okresy, odczyty, preview/close, snapshoty (tagi deklarują endpointy)
api_router.include_router(create_router_rental_billing)
api_router.include_router(collection_router_rental_billing)
api_router.include_router(one_router_rental_billing)
api_router.include_router(update_router_rental_billing)
api_router.include_router(preview_router_rental_billing)
api_router.include_router(close_router_rental_billing)
api_router.include_router(delete_router_rental_billing)

# Rentals - podział rodzinny (tagi deklarują endpointy)
api_router.include_router(create_router_rental_family)
api_router.include_router(collection_router_rental_family)
api_router.include_router(one_router_rental_family)
api_router.include_router(update_router_rental_family)
api_router.include_router(delete_router_rental_family)

# Contact (tagi deklarują endpointy; create publiczny z X-Contact-Token)
api_router.include_router(create_router_contact)
api_router.include_router(collection_router_contact)
api_router.include_router(one_router_contact)
api_router.include_router(update_router_contact)
api_router.include_router(delete_router_contact)
