class HashMap:
    # Citation: paraphrased and repurposed from C950 Supplemental Resources C950 - Webinar-1 - Let’s Go Hashing -
    # Recording (Figure 7.8.2: Hash table using chaining. Zybooks)

    # Constructor used to create a HashMap object of size 27 if no integer value is passed as an argument. This data
    # structure has a space complexity of O(n) because each element requires memory.
    def __init__(self, capacity=27):
        self.list = []
        for i in range(capacity):
            self.list.append([])

    def insert(self, key, item):
        # Hashes the integer key passed as an argument then modulo divides it by the length of the list storing the
        # remainder in the  bucket variable. This function runs in O(n) time when preforming inserts.
        bucket = hash(key) % len(self.list)
        bucketList = self.list[bucket]

        # Updates key if its already in the bucket.
        for kv in bucketList:

            if kv[0] == key:
                kv[1] = item
                return True

        # If key is not in the bucket already. The item is added to the end of the bucket list.
        key_value = [key, item]
        bucketList.append(key_value)
        return True

    # Returns the value attached to the key integer passed as an argument. This function runs in O(1) time accessing
    # elements in  the hash table by their key.
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucketList = self.list[bucket]

        for pair in bucketList:
            if key == pair[0]:
                return pair[1]
        return None
