from table.MetaTable import MetaTable


'''
定义涉及到的表

初始化密码
是否强制修改密码
交易密码？

用户初始密码：
{bcrypt}$2a$10$m1SPz.Uq2AhwYeuvy49SeOmNvXw.hGDAO6qm/0ox2j8c6KUZ2Gddq

'''

class User(MetaTable):

    # def __init__(self, table_name,
    def __init__(self,
                 user_id,
                 user_name,
                 mobile,
                 display_name,
                 area = None,
                 force_chg_psw = True,
                 password = "{bcrypt}$2a$10$m1SPz.Uq2AhwYeuvy49SeOmNvXw.hGDAO6qm/0ox2j8c6KUZ2Gddq",
                 regist_channel = "system",
                 bind_enterprise = True,
                 enabled = True,
                 account_non_expired = True,
                 credentials_non_expired = True,
                 create_by = "system",
                 regist_time = "now()",
                 create_time = "now()",
                 update_time = "now()"
                 ):
        super().__init__("user")
        self.regist_time = regist_time
        self.create_by = create_by
        self.credentials_non_expired = credentials_non_expired
        self.account_non_expired = account_non_expired
        self.enabled = enabled
        self.bind_enterprise = bind_enterprise
        self.regist_channel = regist_channel
        self.password = password
        self.force_chg_psw = force_chg_psw
        self.area = area
        self.update_time = update_time
        self.create_time = create_time
        self.display_name = display_name
        self.mobile = mobile
        self.user_name = user_name
        self.user_id = user_id


class IdVerifyInfo(MetaTable):

    # def __init__(self, table_name,
    def __init__(self,
                 rec_id,
                 id_num, # 身份证号
                 id_name,
                 user_id,
                 mobile,
                 id_type = "1010", # 默认身份证
                 auth_level=None,
                 verify_channel = None,
                 verified = True,
                 expired = False,
                 verify_time = "now()",
                 create_time = "now()",
                 update_time = "now()"
                 ):
        super().__init__("id_verify_info")
        self.verify_channel = verify_channel
        self.auth_level = auth_level
        self.rec_id = rec_id
        self.id_type = id_type
        self.id_num = id_num
        self.id_name = id_name
        self.user_id = user_id
        self.mobile = mobile
        self.verified = verified
        self.expired = expired
        self.verify_time = verify_time
        self.create_time = create_time
        self.update_time = update_time


class BusinessInfo(MetaTable):

    # def __init__(self, table_name,
    def __init__(self,
                 rec_id,
                 cp_cell_phone,
                 cp_cert_no,
                 cp_name,
                 cust_cer_no, # 统一社会信用代码
                 cust_name,
                 user_id,
                 industry_type,
                 area,
                 auth_level = None,
                 auth_channel = None,
                 verified = True,
                 create_time = "now()",
                 update_time = "now()",
                 refresh_time = "now()"
                 ):
        super().__init__("business_info")
        self.rec_id = rec_id
        self.cp_cell_phone = cp_cell_phone
        self.cp_cert_no = cp_cert_no
        self.cp_name = cp_name
        self.cust_cer_no = cust_cer_no
        self.cust_name = cust_name
        self.user_id = user_id
        self.industry_type = industry_type
        self.area = area
        self.auth_level = auth_level
        self.auth_channel = auth_channel
        self.verified = verified
        self.create_time = create_time
        self.update_time = update_time
        self.refresh_time = refresh_time


class EntScaleInfo(MetaTable):
    # def __init__(self, table_name,
    def __init__(self,
                 rec_id,
                 business_id,
                 user_id,
                 business_income = None,
                 commun_add = None,
                 employee_num = None,
                 ent_email = None,
                 ent_highlights = None,
                 ent_size_type = None,
                 enterprise_nature = None, # code
                 established_time = None,
                 finacial_status = None,
                 industry = None, # code
                 main_business = None,
                 owner_structure = None,
                 register_add = None,
                 register_capital = None,
                 total_assets = None,
                 create_time = "now()",
                 update_time = "now()"
                 ):
        super().__init__("ent_scale_info")
        # 构造函数中不作类型检查，但是需要注意数据库中的数字类型
        self.rec_id = rec_id
        self.business_id = business_id
        self.user_id = user_id
        self.business_income = business_income          # decimal
        self.commun_add = commun_add
        self.employee_num = employee_num                # int
        self.ent_email = ent_email
        self.ent_highlights = ent_highlights
        self.ent_size_type = ent_size_type
        self.enterprise_nature = enterprise_nature
        self.established_time = established_time
        self.finacial_status = finacial_status
        self.industry = industry
        self.main_business = main_business
        self.owner_structure = owner_structure
        self.register_add = register_add
        self.register_capital = register_capital        # decimal
        self.total_assets = total_assets                # decimal
        self.create_time = create_time
        self.update_time = update_time

# more
class Organization(MetaTable):
    def __init__(self,
                 org_id = None,
                 inter_org_no = None,
                 parent_org_id = None,
                 area = None,
                 fi_org_type = None,
                 org_name = None,
                 org_level = None,
                 top_org_id = None,
                 enabled = True,       # true
                 org_type = "fi",   # ?
                 set_fi_store = False,  # false
                 set_top = False        # false
                 ):
        super().__init__("organization")
        self.org_id = org_id
        self.inter_org_no = inter_org_no
        self.parent_org_id = parent_org_id
        self.area = area
        self.fi_org_type = fi_org_type
        self.org_name = org_name
        self.org_level = org_level
        self.top_org_id = top_org_id
        self.enabled = enabled
        self.org_type = org_type
        self.set_fi_store = set_fi_store
        self.set_top = set_top

class UserLinkOrganization(MetaTable):
    def __init__(self,
                 id,     # not very important
                 user_id,
                 user_org_id,
                 create_by = "system",
                 create_time = "now()",
                 update_time = "now()",
                 enabled = True,
                 update_by = "system",
                 display_name = None,
                 employee_number = None,
                 mail = None
                 ):
        super().__init__("user_organization")
        self.id = id
        self.user_id = user_id
        self.user_org_id = user_org_id
        self.create_by = create_by
        self.create_time = create_time
        self.update_time = update_time
        self.enabled = enabled
        self.update_by = update_by
        self.display_name = display_name
        self.employee_number = employee_number
        self.mail = mail

'''
Role可以使用flyway里已经有的app, fi, op
已经写在Constant里作为伪Role用
'''
class Role(MetaTable):
    def __init__(self,
                 role_id,
                 role_code,
                 role_name,
                 role_org_id = None,
                 role_type = None,
                 create_by = "system",
                 update_by = "system",
                 create_time = "now()",
                 update_time = "now()",
                 description = None,
                 enabled = True,
                 build_in = True
                 ):
        super().__init__("role")
        self.role_id = role_id
        self.role_code = role_code
        self.role_org_id = role_org_id
        self.role_type = role_type
        self.create_by = create_by
        self.update_by = update_by
        self.create_time = create_time
        self.update_time = update_time
        self.description = description
        self.enabled = enabled
        self.role_name = role_name
        self.build_in = build_in

class UserLinkRole(MetaTable):
    def __init__(self,
                 user_id,
                 role_id
                 ):
        super().__init__("user_role")
        self.role_id = role_id
        self.user_id = user_id