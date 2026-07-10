# Auth
LOGIN = "/authentication/login"
AUTOMATICALLY_LOGIN = "/authentication/automatically_login/{user_id}"

# Patryk_Calculator_Work
CALCULATOR_KEYS = "/calculator_work/calculator_keys"
CALCULATOR_KEYS_UPDATE = "/calculator_work/calculator_keys/update"
CALCULATOR = "/calculator_work/calculator_keys/calculations"

# Outstanding_money
COLLECTION_OUTSTANDING_MONEY = "/outstanding_money/collection"
CREATE_LIST_OUTSTANDING_MONEY = "/outstanding_money/create_list"
ADD_ITEM_OUTSTANDING_MONEY = "/outstanding_money/add_item"
EDIT_NAME_LIST_OUTSTANDING_MONEY = "/outstanding_money/edit_name_list"
EDIT_ITEM_OUTSTANDING_MONEY = "/outstanding_money/edit_item"
DELETE_LIST_OUTSTANDING_MONEY = "/outstanding_money/delete_list/{id}"
DELETE_ITEM_OUTSTANDING_MONEY = "/outstanding_money/delete_item/{id}"

# Logs
COLLECTION_LOGS = "/logs/collection/{number}"

# Fuel_calculator
FUEL_CALCULATION = "/fuel/fuel_calculations"

# Tasks
CREATE_TASK = "/tasks/create"
COLLECTION_TASKS = "/tasks/collection"
UPDATE_TASKS = "/tasks/update/{task_id}"
UPDATE_ACTIVE_TASKS = "/tasks/update/active/{task_id}"
DELETE_TASK = "/tasks/delete/{task_id}"
STATISTICS_TASK = "/tasks/statistics"

# Calendar Days
CREATE_CALENDAR = "/calendar/generate"
COLLECTION_CALENDAR = "/calendar/collection"
STATISTICS_CALENDAR = "/calendar/statistics"

# Calendar Condition
COLLECTION_CALENDAR_CONDITION = "/calendar/condition/collection"
CREATE_CALENDAR_CONDITION = "/calendar/condition/create"
UPDATE_CALENDAR_CONDITION = "/calendar/condition/update/{condition_id}"
DELETE_CALENDAR_CONDITION = "/calendar/condition/delete/{condition_id}"

# Calendar Day Work
UPDATE_CALENDAR_DAY_WORK_BY_ID = "/calendar/day/work/update/{day_id}"
UPDATE_CALENDAR_DAYS = "/calendar/days/work/update"
UPDATE_CALENDAR_DAYS_SALARY = "/calendar/days/work/update/salary"

# Rentals - słowniki: mieszkania
CREATE_RENTAL_APARTMENT = "/rentals/apartments/create"
COLLECTION_RENTAL_APARTMENTS = "/rentals/apartments/collection"
ONE_RENTAL_APARTMENT = "/rentals/apartments/one/{apartment_id}"
UPDATE_RENTAL_APARTMENT = "/rentals/apartments/update/{apartment_id}"
DELETE_RENTAL_APARTMENT = "/rentals/apartments/delete/{apartment_id}"

# Rentals - słowniki: najemcy
CREATE_RENTAL_TENANT = "/rentals/tenants/create"
COLLECTION_RENTAL_TENANTS = "/rentals/tenants/collection"
ONE_RENTAL_TENANT = "/rentals/tenants/one/{tenant_id}"
UPDATE_RENTAL_TENANT = "/rentals/tenants/update/{tenant_id}"
DELETE_RENTAL_TENANT = "/rentals/tenants/delete/{tenant_id}"

# Rentals - słowniki: najmy (najemca + mieszkanie + czynsz)
CREATE_RENTAL_TENANCY = "/rentals/tenancies/create"
COLLECTION_RENTAL_TENANCIES = "/rentals/tenancies/collection"
ONE_RENTAL_TENANCY = "/rentals/tenancies/one/{tenancy_id}"
UPDATE_RENTAL_TENANCY = "/rentals/tenancies/update/{tenancy_id}"
DELETE_RENTAL_TENANCY = "/rentals/tenancies/delete/{tenancy_id}"

# Rentals - słowniki: rodzaje kosztów
CREATE_RENTAL_COST_TYPE = "/rentals/cost_types/create"
COLLECTION_RENTAL_COST_TYPES = "/rentals/cost_types/collection"
ONE_RENTAL_COST_TYPE = "/rentals/cost_types/one/{cost_type_id}"
UPDATE_RENTAL_COST_TYPE = "/rentals/cost_types/update/{cost_type_id}"
DELETE_RENTAL_COST_TYPE = "/rentals/cost_types/delete/{cost_type_id}"

# Rentals - słowniki: koszty mieszkań
CREATE_RENTAL_APARTMENT_COST = "/rentals/apartment_costs/create"
COLLECTION_RENTAL_APARTMENT_COSTS = "/rentals/apartment_costs/collection"
ONE_RENTAL_APARTMENT_COST = "/rentals/apartment_costs/one/{apartment_cost_id}"
UPDATE_RENTAL_APARTMENT_COST = "/rentals/apartment_costs/update/{apartment_cost_id}"
DELETE_RENTAL_APARTMENT_COST = "/rentals/apartment_costs/delete/{apartment_cost_id}"

# Rentals - słowniki: liczniki
CREATE_RENTAL_METER = "/rentals/meters/create"
COLLECTION_RENTAL_METERS = "/rentals/meters/collection"
ONE_RENTAL_METER = "/rentals/meters/one/{meter_id}"
UPDATE_RENTAL_METER = "/rentals/meters/update/{meter_id}"
DELETE_RENTAL_METER = "/rentals/meters/delete/{meter_id}"

# Rentals - okresy rozliczeniowe
CREATE_RENTAL_PERIOD = "/rentals/periods/create"
COLLECTION_RENTAL_PERIODS = "/rentals/periods/collection"
ONE_RENTAL_PERIOD = "/rentals/periods/one/{period_id}"
UPDATE_RENTAL_PERIOD = "/rentals/periods/update/{period_id}"
PREVIEW_RENTAL_PERIOD = "/rentals/periods/preview/{period_id}"
CLOSE_RENTAL_PERIOD = "/rentals/periods/close/{period_id}"
REOPEN_RENTAL_PERIOD = "/rentals/periods/reopen/{period_id}"
DELETE_RENTAL_PERIOD = "/rentals/periods/delete/{period_id}"

# Rentals - odczyty liczników w okresie
CREATE_RENTAL_METER_READING = "/rentals/readings/create"
COLLECTION_RENTAL_METER_READINGS = "/rentals/readings/collection/{period_id}"
UPDATE_RENTAL_METER_READING = "/rentals/readings/update/{reading_id}"
DELETE_RENTAL_METER_READING = "/rentals/readings/delete/{reading_id}"

# Rentals - snapshoty rozliczeń mieszkań
COLLECTION_RENTAL_SETTLEMENTS = "/rentals/settlements/collection"
ONE_RENTAL_SETTLEMENT = "/rentals/settlements/one/{settlement_id}"

# Rentals - podział rodzinny: beneficjenci
CREATE_RENTAL_BENEFICIARY = "/rentals/beneficiaries/create"
COLLECTION_RENTAL_BENEFICIARIES = "/rentals/beneficiaries/collection"
ONE_RENTAL_BENEFICIARY = "/rentals/beneficiaries/one/{beneficiary_id}"
UPDATE_RENTAL_BENEFICIARY = "/rentals/beneficiaries/update/{beneficiary_id}"
DELETE_RENTAL_BENEFICIARY = "/rentals/beneficiaries/delete/{beneficiary_id}"

# Rentals - podział rodzinny: reguły podziału
CREATE_RENTAL_ALLOCATION_RULE = "/rentals/allocation_rules/create"
COLLECTION_RENTAL_ALLOCATION_RULES = "/rentals/allocation_rules/collection"
ONE_RENTAL_ALLOCATION_RULE = "/rentals/allocation_rules/one/{rule_id}"
UPDATE_RENTAL_ALLOCATION_RULE = "/rentals/allocation_rules/update/{rule_id}"
DELETE_RENTAL_ALLOCATION_RULE = "/rentals/allocation_rules/delete/{rule_id}"

# Rentals - podział rodzinny: snapshoty podziału per okres
COLLECTION_RENTAL_BENEFICIARY_SETTLEMENTS = "/rentals/beneficiary_settlements/collection"
