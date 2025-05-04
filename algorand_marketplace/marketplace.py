from pyteal import *

def marketplace_contract():
    seller = Addr("SELLER_ALGORAND_ADDRESS")

    item_price_key = Bytes("Price")     # uint64
    item_asset_id_key = Bytes("Asset")  # uint64
    buyer_key = Bytes("Buyer")          # addr

    on_create = Seq([
        App.globalPut(item_price_key, Btoi(Txn.application_args[0])),
        App.globalPut(item_asset_id_key, Btoi(Txn.application_args[1])),
        Approve()
    ])

    on_buy = Seq([
        Assert(
            And(
                Txn.application_args.length() == Int(1),
                Txn.sender() != seller,
                Gtxn[0].type_enum() == TxnType.Payment,
                Gtxn[0].receiver() == seller,
                Gtxn[0].amount() >= App.globalGet(item_price_key),
                Gtxn[0].sender() == Txn.sender()
            )
        ),
        App.globalPut(buyer_key, Txn.sender()),
        Approve()
    ])

    on_claim_asset = Seq([
        Assert(
            And(
                Txn.sender() == seller,
                App.globalGet(buyer_key) != Global.zero_address()
            )
        ),
        Approve()
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, 
         Cond(
             [Txn.application_args[0] == Bytes("buy"), on_buy],
             [Txn.application_args[0] == Bytes("claim"), on_claim_asset]
         )
        ]
    )

    return program

if __name__ == "__main__":
    from pyteal import compileTeal, Mode
    print(compileTeal(marketplace_contract(), mode=Mode.Application))
