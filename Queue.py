class Queue:
    def __init__(self):
        # Using an empty list as the base of our queue.
        self.queue = []

    # Returns the first item in the queue. Runs in O(1) time because you are accessing the first element by index.
    def peek(self):
        if len(self.queue) <= 0:
            return None
        else:
            return self.queue[0]

    # Takes an item as an object and appends it to the back of the queue.
    def enqueue(self, item):
        self.queue.append(item)

    # Removes the first item form the queue.
    def dequeue(self):
        self.queue.pop(0)

    # Checks if queue is empty and return true or false.
    def is_empty(self):
        if len(self.queue) <= 0:
            return True
        else:
            return False
