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
R_create_time = "create_time"
R_enabled = "enabled"
R_address = "address"

# USER_TABLE
U_user_code = "USER_CODE"
U_org_code = "ORG_CODE"
U_user_name = "USER_NAME"

# orgtable


from table.UsrDb import Role
# Role table default value, just a dummy to keep code clean
ROLE_PRESET_APP = Role(role_id=1, role_code="@app_user", role_name="平台内置用户角色", role_type="app")
ROLE_PRESET_FI = Role(role_id=2, role_code="@fi_user", role_name="平台内置金融机构管理员", role_type="fi")
ROLE_PRESET_OP = Role(role_id=3, role_code="@op_user", role_name="平台内置运营管理员", role_type="op")