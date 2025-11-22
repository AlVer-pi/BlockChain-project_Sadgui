from hashlib import sha256
import time
import json

class Block:
    def __init__(self, i, ts, data, prev):
        self.index = i
        self.timestamp = ts
        self.data = data
        self.prev = prev
        self.nonce = 0
        self.hash = self.calc()

    def calc(self):
        s = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.prev}{self.nonce}"
        return sha256(s.encode()).hexdigest()

    def mine(self, diff):
        while not self.hash.startswith(diff):
            self.nonce += 1
            self.hash = self.calc()

class Chain:
    def __init__(self, diff="00"):
        self.diff = diff
        self.blocks = [self.genesis()]

    def genesis(self):
        b = Block(0, time.time(), {"genesis": True}, "0")
        b.mine(self.diff)
        return b

    def add(self, data):
        p = self.blocks[-1]
        b = Block(len(self.blocks), time.time(), data, p.hash)
        b.mine(self.diff)
        self.blocks.append(b)

    def check(self):
        for i in range(1, len(self.blocks)):
            cur = self.blocks[i]
            prev = self.blocks[i - 1]
            if cur.prev != prev.hash:
                return False
            if cur.calc() != cur.hash:
                return False
            if not cur.hash.startswith(self.diff):
                return False
        return True

    def show(self):
        print("\nCurrent blockchain:")
        for b in self.blocks:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(b.timestamp))
            print(f"Block {b.index} | time={time_str} | data={b.data} | hash={b.hash[:12]} | prev={b.prev[:12]} | nonce={b.nonce}")

if __name__ == "__main__":
    chain = Chain("0000")

    while True:
        print("\nOptions:")
        print("1. Add a new block")
        print("2. Tamper with a block")
        print("3. Show blockchain")
        print("4. Check blockchain validity")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            user_data = input("Enter data for the new block: ")
            chain.add({"user_input": user_data})
            print("Block added!")

        elif choice == "2":
            chain.show()
            block_index = int(input("Enter the index of the block you want to tamper with: "))
            if 0 < block_index < len(chain.blocks):  # cannot tamper genesis
                new_value = input("Enter new (fake) data: ")
                chain.blocks[block_index].data = {"tampered_data": new_value}
                chain.blocks[block_index].hash = chain.blocks[block_index].calc()
                print(f"Block {block_index} has been tampered with!")
            else:
                print("Invalid block index or cannot tamper with genesis block.")

        elif choice == "3":
            chain.show()

        elif choice == "4":
            print("Blockchain valid:", chain.check())

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")