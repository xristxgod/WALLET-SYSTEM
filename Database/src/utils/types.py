CRYPTOAddress = str

class EndpointType(object):
    CREATE_WALLET = ("POST", "<domain>/api/<network>/create/wallet")
    BALANCE = ("GET", "<domain>/api/<network>/balance/<address>")

    OPTIMAL_FEE = ("GET", "<domain>/api/<network>/fee/<inputs>&<outputs>")

    CREATE_TRANSACTION = ("POST", "<domain>/api/<network>/create/transaction")
    SEND_TRANSACTION = ("POST", "<domain>/api/<network>/create/transaction")