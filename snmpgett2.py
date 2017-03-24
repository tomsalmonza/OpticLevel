from pysnmp.hlapi import *
from private import SNMP

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           UsmUserData(SNMP['user'],
                       authKey=SNMP['auth'],
                       privKey=SNMP['priv'],
                       authProtocol=usmHMACSHAAuthProtocol,
                       privProtocol=usmAesCfb128Protocol),
           UdpTransportTarget(('svrt1-isd.wolcomm.net', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
)

if errorIndication:
    print('errorIndication: %s' % errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))


