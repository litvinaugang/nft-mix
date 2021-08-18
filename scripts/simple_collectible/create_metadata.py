
from scripts.helpful_scripts import OPENSEA_FORMAT
from brownie import ArtBot, network, config, accounts
from metadata import sample_metadata
from pathlib import Path
import os
import requests
import json


def main():
    print("Working on " + network.show_active())
    simple_collectible = ArtBot[len(ArtBot) - 1]
    number_of_tokens = simple_collectible.tokenIdCounter()
    print("number_of_tokens deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, simple_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(0,number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(token_id) +".json"
        )
        if Path(metadata_file_name).exists():
            print("trying {}".format(token_id))
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating metadata file {}".format(metadata_file_name))
            collectible_metadata['name'] = "Artbot_work_{}".format(token_id)
            collectible_metadata["description"] = "Beatuiful {}!".format(
                collectible_metadata["name"])
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/1Art_Bot_no_{}.jpg".format(token_id)
                image_to_upload = upload_to_ipfs(image_path)
                collectible_metadata["image"] = image_to_upload
                print(collectible_metadata)
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
            else: print("UPLOAD_IPFS = False")
            

#http://127.0.0.1:5001

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(uri)
    return uri

def upload_to_pinata():
    ids = []
    for i in range(0,10):
        PINATA_BASE_URL = 'https://api.pinata.cloud/'
        endpoint = 'pinning/pinFileToIPFS'
        # Change this to upload a different file
        filepath = './img/1Art_Bot_no_{}.jpg'.format(i)
        filename = filepath.split('/')[-1:][0]
        headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
                'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}


        with Path(filepath).open("rb") as fp:
            image_binary = fp.read()
            response = requests.post(PINATA_BASE_URL + endpoint,
                                    files={"file": (filename, image_binary)},
                                    headers=headers)
            ids.append(response.json()['IpfsHash'])
        return ids