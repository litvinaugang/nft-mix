from brownie import ArtBot, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import OPENSEA_FORMAT


def main():
    print("Working on " + network.show_active())
    simple_collectible = ArtBot[len(ArtBot) - 1]
    number_of_tokens = simple_collectible.tokenIdCounter()
    print("number_of_tokens deployed is {}".format(number_of_tokens))
    for token_id in range(1,number_of_tokens):
        print("token uri: {}".format(simple_collectible.tokenURI(token_id)))