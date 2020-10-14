# primary id formatter
H_Organization = "11"
H_User = "22"
H_Role = "33" # never used
H_UserRole = "44"
H_UserOrganization = "55"

# raw table

R_id = "id"
R_org_name = "org_name"
R_branch = "branch"
R_level_1_code = "level_1_code"
R_level_1_value = "level_1_value"
R_level_2_code = "level_2_code"
R_level_2_value = "level_2_value"
R_level_3_code = "level_3_code"
R_level_3_value = "level_3_value"
R_parent_org_id = "parent_org_id"
R_parent_org_name = "parent_org_name"
R_top_org_id = "top_org_id"
R_top_org_name = "top_org_name"
R_province_code = "province_code"
R_city_code = "city_code"
R_district_code = "district_code"

R_province_value = "province_name"
R_city_value = "city_name"
R_district_value = "district_name"

R_create_time = "create_time"
R_enabled = "enabled"
R_address = "address"

# USER_TABLE
U_user_code = "USER_CODE"
U_org_code = "ORG_CODE"
U_user_name = "USER_NAME"

# product table
P_valid = "valid"
P_org_no = "org_no"
P_product_name = "product_name"
P_accept_mode = "accept_mode"
P_guarantee_mode = "guarantee_mode"
P_usage_inf = "usage_inf"
P_pay_mode = "pay_mode"
P_credit_amount = "credit_amount"
P_min_credit_amount = "min_credit_amount"
P_max_credit_amount = "max_credit_amount"
P_max_loan_terms = "max_loan_terms"

P_interest_rates = "interest_rates"
P_min_interest_rates = "min_interest_rates"
P_max_interest_rates = "max_interest_rates"


P_processing_duration = "processing_duration"
P_customer_type = "customer_type"
P_product_type = "product_type"
P_is_policy_product = "is_policy_product"








from table.UsrDb import Role
# Role table default value, just a dummy to keep code clean
ROLE_PRESET_APP = Role(role_id=1, role_code="@app_user", role_name="平台内置用户角色", role_type="app")
ROLE_PRESET_FI = Role(role_id=2, role_code="@fi_user", role_name="平台内置金融机构管理员", role_type="fi")
ROLE_PRESET_OP = Role(role_id=3, role_code="@op_user", role_name="平台内置运营管理员", role_type="op")