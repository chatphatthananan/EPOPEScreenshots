import datetime
import os
from datetime import date

email = {
        'sender' : 'xxx',
        'to' : 'xxx',
        'subject' : '',
        'body' : '',
        'is_html' : False,
        'filename': []
    }

SGTAM_log_config = {
                    'logTaskID' : 117,
                    'statusFlag' : 2,
                    'logMsg' : 'EPO PE Screenshots started.',
                    'logID' : None
                }

SGP_EXPORTFINAL_URL = ['http://10.86.137.60/public/#/data-production/production-system', 'SgpExportFinal']
DNX_WORKFLOW_URL = ['http://10.86.137.60/public/#/administration/dnx-workflow', 'DnxWorkflow']
CONNECTED_DEVICES_URL = ['http://10.86.137.60/public/#/monitoring/connected-devices', 'ConnectedDevices']
CONNECTED_DEVICES_PROVIDERS_URL = ['http://10.86.137.60/public/#/monitoring/connected-devices-by-provider', 'ConnectedDevicesByProvider']
CORRELATION_INFORMATION_URL = ['http://10.86.137.60/public/#/monitoring/correlation-information', 'CorrelationInformation']
BLL_SERVER_URL = ['http://10.86.137.60/public/#/jobs-events/bll-server-status', 'BllServer']

GENERAL_CHECK_URL_LIST = [SGP_EXPORTFINAL_URL, DNX_WORKFLOW_URL, CONNECTED_DEVICES_URL, CONNECTED_DEVICES_PROVIDERS_URL, CORRELATION_INFORMATION_URL, BLL_SERVER_URL]

CPS_URL = [['http://10.86.137.60/public/#/administration/cps/defaultSystem', 'CpsTree'],
           ['http://10.86.137.60/public/#/administration/cps/defaultSystem/SgpMasterInGermany', 'SgpMasterInGermany'],
           ['http://10.86.137.60/public/#/administration/cps/defaultSystem/SgpMasterInSgp', 'SgpMasterInSgp'],
           ['http://10.86.137.60/public/#/administration/cps/defaultSystem/SgpMasterForCustomers', 'SgpMasterForCustomers'],
           ['http://10.86.137.60/public/#/administration/cps/defaultSystem/SgpMasterFedAuth', 'SgpMasterFedAuth'],
           ['http://10.86.137.60/public/#/administration/cps/defaultSystem/SgpMasterInAws', 'SgpMasterInAws']
           ]
