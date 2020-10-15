from table.MetaTable import MetaTable

class Product(MetaTable):
    def __init__(self,
                 product_id,
                 accept_mode,  # this is a not null value
                 currency,
                 customer_type,
                 loan_terms_unit,
                 max_credit_amount,
                 min_credit_amount,
                 min_interest_rates,
                 pay_mode,
                 processing_duration,
                 product_name,
                 product_org_id,
                 product_title,
                 product_type,
                 rates_unit,
                 usage_inf,
                 inter_org_no,    # 这个尼玛重头戏了，关联到机构去了
                 status="onTheShelf",
                 max_interest_rates=None,
                 max_loan_terms=None,
                 redirecturl=None,
                 area=None,
                 product_policy_id=None,
                 target_customer=None,
                 product_category=None,
                 is_policy_product=False,
                 guarantee_mode=None,
                 risk_model_id=None,    # 这个其实是有外键的，但是同时又允许为空
                 ext_pid=None,
                 enabled=True,
                 is_ccb_product=False,
                 create_by="admin",
                 update_by="admin",
                 create_time="now()",
                 update_time="now()",
                 status_update_time="now()"
                 ):
        super().__init__("product")
        self.status_update_time = status_update_time
        self.product_id = product_id
        self.accept_mode = accept_mode
        self.currency = currency
        self.customer_type = customer_type
        self.loan_terms_unit = loan_terms_unit
        self.max_credit_amount = max_credit_amount
        self.min_credit_amount = min_credit_amount
        self.min_interest_rates = min_interest_rates
        self.pay_mode = pay_mode
        self.processing_duration = processing_duration
        self.product_name = product_name
        self.product_org_id = product_org_id
        self.product_title = product_title
        self.product_type = product_type
        self.rates_unit = rates_unit
        self.status = status
        self.usage_inf = usage_inf
        self.inter_org_no = inter_org_no
        self.max_interest_rates = max_interest_rates
        self.max_loan_terms = max_loan_terms
        self.redirecturl = redirecturl
        self.area = area
        self.product_policy_id = product_policy_id
        self.target_customer = target_customer
        self.product_category = product_category
        self.is_policy_product = is_policy_product
        self.guarantee_mode = guarantee_mode
        self.risk_model_id = risk_model_id
        self.ext_pid = ext_pid
        self.enabled = enabled
        self.is_ccb_product = is_ccb_product
        self.create_by = create_by
        self.update_by = update_by
        self.create_time = create_time
        self.update_time = update_time