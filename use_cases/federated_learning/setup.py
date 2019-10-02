#!/usr/bin/env python3
import sys
import use_cases.federated_learning.iroha_config as iroha_config
import json
from utils.administrator import Domain, Admin
from layers.identification.user import User
from layers.incentive.asset import Asset

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

# Set the ip of one iroha node
ip_iroha_node = '123.456.789'
admin = Admin(ip_iroha_node)
domain = Domain('public', 'default_role')
admin.create_domain(domain)
asset = Asset('coin', domain, 3)
admin.create_asset(asset)


#################################
# workers nodes setup
################################
# create accounts in the network
# for the sake of the example all nodes have the same information
x = {"age": 30, "city": "New York"}
public = Domain('public', 'default_role')
account_information = json.dumps(x)

worker1 = User(iroha_config.worker1_private_key, iroha_config.worker1_name, domain, ip_iroha_node, account_information)
worker2 = User(iroha_config.worker2_private_key, iroha_config.worker2_name, domain, ip_iroha_node, account_information)
worker3 = User(iroha_config.worker3_private_key, iroha_config.worker3_name, domain, ip_iroha_node, account_information)
worker4 = User(iroha_config.worker4_private_key, iroha_config.worker4_name, domain, ip_iroha_node, account_information)
worker5 = User(iroha_config.worker5_private_key, iroha_config.worker5_name, domain, ip_iroha_node, account_information)
worker6 = User(iroha_config.worker6_private_key, iroha_config.worker6_name, domain, ip_iroha_node, account_information)
worker7 = User(iroha_config.worker7_private_key, iroha_config.worker7_name, domain, ip_iroha_node, account_information)
worker8 = User(iroha_config.worker8_private_key, iroha_config.worker8_name, domain, ip_iroha_node, account_information)
worker9 = User(iroha_config.worker9_private_key, iroha_config.worker9_name, domain, ip_iroha_node, account_information)
##################################
# chief node setup
# ################################
# create an account in the network
chief = User(iroha_config.chief_private_key, iroha_config.chief_name, domain, ip_iroha_node, account_information)

##################################
# grant access
# ################################
# grant access so chief node can share us his information
worker1.grants_access_set_details_to(chief, iroha_config.worker1_private_key)
worker2.grants_access_set_details_to(chief, iroha_config.worker2_private_key)
worker3.grants_access_set_details_to(chief, iroha_config.worker3_private_key)
worker4.grants_access_set_details_to(chief, iroha_config.worker4_private_key)
worker5.grants_access_set_details_to(chief, iroha_config.worker5_private_key)
worker6.grants_access_set_details_to(chief, iroha_config.worker6_private_key)
worker7.grants_access_set_details_to(chief, iroha_config.worker7_private_key)
worker8.grants_access_set_details_to(chief, iroha_config.worker8_private_key)
worker9.grants_access_set_details_to(chief, iroha_config.worker9_private_key)

# grant access so worker node can share us his information
chief.grants_access_set_details_to(worker1, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker2, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker3, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker4, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker5, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker6, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker7, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker8, iroha_config.chief_private_key)
chief.grants_access_set_details_to(worker9, iroha_config.chief_private_key)


print('**********************************')
print('**********************************')
print('The BSMD is created and iroha configured')
print('**********************************')
print('**********************************')
