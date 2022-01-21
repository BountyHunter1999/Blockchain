# Module 1 - Create a Blockchain
from datetime import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part I - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {"index": len(self.chain) + 1,
                 "timestamp": str(datetime.now()),
                 "proof": proof,  # also known as nonce
                 "previous_hash": previous_hash
                 }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        # Return the last block that was added
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        # take the previous_proof(i.e. nonce) and create a new valid proof
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        """
        Parameters
        ----------
        block : block which is a dictionary with keys
            DESCRIPTION.

        Returns hex value after sha256 encryption
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):

        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # previous hash of each block is equal to hash of the previous block
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            # check the proof of each block according to proof of work
            previous_proof = previous_block["proof"]
            proof = block["proof"]

            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            # this block will become previous block for the next iteation
            previous_block = block
            block_index += 1

        return True


# Part II - Mining our Blockchain

# Creating the Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()


# mining a new block
@app.route("/mine_block", methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations on mining a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return response, 200  # no need to jsonify a dict(flask does it for us)
    # return jsonify(response), 200 


# Getting the full Blockchain
@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {"chain": blockchain.chain,
                'length': len(blockchain.chain)
                }

    return response, 200


# Checking to see if the chain is valid

@app.route("/is_valid", methods=['GET'])
def is_valid():
    if blockchain.is_chain_valid(blockchain.chain):
        return {"message": "Chain is valid, bruh"}, 200
    else:
        return {"message": "Chain isn't valid, bruh"}, 300


# Running the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
