# Auth
LOGIN = "/authentication/login"
AUTOMATICALLY_LOGIN = "/authentication/automatically_login/{user_id}"

# Patryk_Calculator_Work
CALCULATOR_KEYS = "/calculator_work/calculator_keys"
CALCULATOR_KEYS_UPDATE = "/calculator_work/calculator_keys/update"
CALCULATOR = "/calculator_work/calculator_keys/calculations"

# Patryk_Pdf_Filter
CREATE_PDF = "/pdf_filter/create"

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
CREATE_LOG = "/logs/create/{description}"

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

# Calendar Condition
COLLECTION_CALENDAR_CONDITION = "/calendar/condition/collection"
CREATE_CALENDAR_CONDITION = "/calendar/condition/create"
UPDATE_CALENDAR_CONDITION = "/calendar/condition/update/{condition_id}"
DELETE_CALENDAR_CONDITION = "/calendar/condition/delete/{condition_id}"

