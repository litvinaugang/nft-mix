from brownie import ArtBot, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed, OPENSEA_FORMAT



def main():
    print("Working on " + network.show_active())
    advanced_collectible = ArtBot[len(ArtBot) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenIdCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
        )
    set_BaseURI(advanced_collectible,
                            "https://gateway.pinata.cloud/ipfs/")
    print('setting base uri')



def set_BaseURI(nft_contract, BaseURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setBaseURI(BaseURI, {"from": dev})
    print(
        "Awesome! Base Uri set at {}".format(
            #OPENSEA_FORMAT.format(nft_contract.address, token_id)
            BaseURI
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')