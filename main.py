from algoikit_utils.beta.algorand_client import(
    AlgorandClient,
    AssetCreateParams,
    AssestOptionParams,
    AssetTransferParams,
    PayParamas,

)

#client to connect to localnet
algorand = AlgorandClient.default_local_net()

#import dispenser from KMD
dispenser = algorand.account.dispenser()
print ("Dispenser Address:", dispenser.address)



creator = algorand.account.random()
#print(algorand.account.get_information(creator.address))

#fund creator account

algorand.send.payment(
    PayParamas(

        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000 # 10 algos
    )
)

print(algorand.account.get_information(creator.address))
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Edu4Teen",
        unit_name="E4T",
    )
)

asset_id=sent_txn["confirmation"] ["asset"]
print("Asset ID", "Asset_ID")

receiver_acct = algorand.account.random()

algorand.send.payment(
   PayParamas(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000 # 10 algos
    )
)


#create a new txn group
group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
      AssetOptionParams(
          sender=receiver_acct.address,
          asset_id=asset_id
      )
)

group_txn.add_payment(
    PayParamas(
        sender=receiver_acct.address,
        receiver=creator.address,
        amount=1_000_000 # 1 algos
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver= receiver_acct.address,
        asset_id=asset_id,
        amount=10,
    )
)

group_txn.execution()

print(algorand.account.get_information(receiver_acct.address))

print("Receiver account Asset Balance", algorand.account.get_information(receiver_acct.address)['assets'][0]['amount'])
print("Creator account Asset Balance", algorand.account.get_information(creator.address)['assets'][0]['amount'])