import hashlib
import time
import json
import os
import shutil
import socket
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.generate_hash()

    def generate_hash(self):
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()

    def get_file_content(self, file_name):
        for transaction in self.transactions:
            if transaction.startswith("File: ") and transaction.endswith(file_name):
                file_path = os.path.join("files", file_name)
                try:
                    with open(file_path, 'rb') as f:
                        return f.read()
                except FileNotFoundError:
                    pass
        return None
