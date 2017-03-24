from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

#
# SNMPv3/USM setup
#

# user: usr-sha-aes, auth: SHA, priv AES
config.addV3User(
    snmpEngine, 'nmsUser',
    config.usmHMACSHAAuthProtocol, 'none',
    config.usmAesCfb128Protocol, 'none'
)
config.addTargetParams(snmpEngine, 'my-creds', 'nmsUser', 'none')

#
# Setup transport endpoint and bind it with security settings yielding
# a target name (choose one entry depending of the transport needed).
#

# UDP/IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
)
config.addTargetAddr(
    snmpEngine, 'svrt1-isd.wolcomm.net',
    udp.domainName, ('svrt1-isd.wolcomm.net', 161),
    'my-creds'
)

# Error/response reciever
def cbFun(sendRequestHandle,
          errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for oid, val in varBindTable:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

# Prepare and send a request message
cmdgen.GetCommandGenerator().sendReq(
    snmpEngine,
    'svrt1-isd.wolcomm.net',
    ( ((1,3,6,1,2,1,1,1,0), None), ),
    cbFun
)

# Run I/O dispatcher which would send pending queries and process responses
snmpEngine.transportDispatcher.runDispatcher()

