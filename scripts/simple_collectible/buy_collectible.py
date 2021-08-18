#!/usr/bin/python3
from brownie import ArtBot, accounts, network, config
from scripts.helpful_scripts import OPENSEA_FORMAT


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    simple_collectible = ArtBot[len(ArtBot) - 1]
    token_id = simple_collectible.tokenIdCounter()
    transaction = simple_collectible.buyArt(1,{"from":dev})
    transaction.wait(1)
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(simple_collectible.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
    print(simple_collectible.tokenURI(token_id))
    print(token_id)
