from hashlib import sha256
import json
from time import time

class Block:

    def __init__(self, timestamp=None, data=None):
        self.timestamp = timestamp or time()
        self.data = [] if data is None else data
        self.prevHash = None
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):

        hash = sha256()
        hash.update(str(self.prevHash).encode('utf-8'))
        hash.update(str(self.timestamp).encode('utf-8'))
        hash.update(str(self.data).encode('utf-8'))
        hash.update(str(self.nonce).encode('utf-8'))
        return hash.hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()

class Blockchain:

    def __init__(self):
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.blockTime = 30000

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)

        self.difficulty += (-1, 1)[int(time()) - int(self.getLastBlock().timestamp) < self.blockTime]

    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash):
                return False

        return True

    def __str__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp, 'nonce': item.nonce, 'hash': item.hash, 'prevHash': item.prevHash} for item in self.chain], indent=4)

from blockchain import Block
from blockchain import Blockchain
from time import time

JeChain = Blockchain()

# Add a new block
JeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 100})))
# (This is just a fun example, real cryptocurrencies often have some more steps to implement).

# Prints out the updated chain
print(JeChain)