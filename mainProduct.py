from utils.Common import *
import utils.Constant as C
from bean.OrgTree import *
from table.PmsDb import *
from table.UsrDb import *

import numpy as np

def processNonValid(obj):
    return None if isEmpty(obj) else obj


if __name__ == '__main__':
    resourcePath = os.getcwd().replace("\\", "/") + "/resource"
    srcPath = buildPath(resourcePath, "out-intermediate", "product-2-clear.csv")
    orgPath = buildPath(resourcePath, "out-intermediate", "organizationTrees.plk")
    outPath = buildPath(resourcePath, "out", "product.sql")


    data = read(srcPath)
    orgs : TreeBuilder = loadByPickle(orgPath)

    uuid = Uuid(header=C.H_Product)

    logger : Logger = Logger(outPath)

    ## todo guarantee_mode 好像？，最好全部都过一遍isEmpty
    with logger:
        # 逐行处理product
        for i in data.index:
            p = data.loc[i, :]
            # exchange org Id，找不到是要报错的
            ox = orgs.pool[p[C.P_org_no]].getTable()

            product : Product = Product(
                product_id=uuid.generate(),
                accept_mode=processNonValid(p[C.P_accept_mode]),
                # 0 -> rmb
                currency=0,
                customer_type=processNonValid(p[C.P_customer_type]),
                # 贷款期限，月
                loan_terms_unit="1",
                max_credit_amount=processNonValid(p[C.P_max_credit_amount]),
                min_credit_amount=processNonValid(p[C.P_min_credit_amount]),
                min_interest_rates=processNonValid(p[C.P_min_interest_rates]),
                max_interest_rates=processNonValid(p[C.P_max_interest_rates]),
                pay_mode=processNonValid(p[C.P_pay_mode]),
                # 处理期限，天
                processing_duration=processNonValid(p[C.P_processing_duration]),
                product_name=processNonValid(p[C.P_product_name]),
                product_org_id=ox.org_id,
                product_title=processNonValid(p[C.P_product_name]),
                product_type=processNonValid(p[C.P_product_type]),
                # 利率单位，年
                rates_unit="1",
                # 上架状态，默认已上架
                status="onTheShelf",
                usage_inf=processNonValid(p[C.P_usage_inf]),
                inter_org_no=ox.inter_org_no,
                max_loan_terms=processNonValid(p[C.P_max_loan_terms]),
                area=ox.area,
                is_policy_product=bool(processNonValid(p[C.P_is_policy_product])),
                guarantee_mode=processNonValid(p[C.P_guarantee_mode])
            )

            logger.writeLine(product.insert())
        pass



