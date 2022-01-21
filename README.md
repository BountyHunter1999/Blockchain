# First-Block-Chain

- Here we created our first blockchain(simple)
- it has a basic proof of work i.e diff of square and 4 leading 0's
- created a flask app to create the endpoints
  - `/mine_block`: to mine a new block
  - `/get_chain`: to get the chain in the block chain
  - `/is_valid`: to check if the chain in the blockchain is valid
    - follows the proof of work
    - and the previous_hash property is same as the hash of the previous block
