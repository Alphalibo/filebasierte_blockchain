import hashlib
import time
import json
import os
import shutil  # Hinzufügen dieses Imports
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from block import Block
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], "0")

    def add_block(self, transactions):
        prev_block = self.chain[-1]
        index = prev_block.index + 1
        new_block = Block(index, transactions, prev_block.hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block, difficulty=4):
        while block.hash[:difficulty] != "0" * difficulty:
            block.nonce += 1
            block.hash = block.generate_hash()

    def download_file(self, block_index, file_name):
        if block_index < len(self.chain):
            block = self.chain[block_index]
            if file_name in block.transactions:
                try:
                    file_path = os.path.join("files", file_name)
                    destination_path = os.path.join("downloads", file_name)
                    shutil.copy(file_path, destination_path)
                    return f"File saved to {destination_path}"
                except Exception as e:
                    return f"Error saving file: {str(e)}"
            else:
                return f"File {file_name} not found in block {block_index}"
        else:
            return f"Block {block_index} not found in the blockchain."

    def get_blockchain(self):
        return self.chain

    def view_files_in_blockchain(self):
        files = []
        for block in self.chain:
            files.extend(block.transactions)
        return files
