import socket
import os
import time
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog


class GUI:
    def __init__(self, blockchain, root):
        self.blockchain = blockchain
        self.root = root
        self.root.title("Blockchain GUI")
        self.create_gui()

    def clean_file_name(self, file_name):
        valid_characters = '-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
        cleaned_name = ''.join(c for c in file_name if c in valid_characters)
        return cleaned_name

    def get_user_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def mine_and_upload(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*")]
        )

        if file_path:
            if os.path.exists(file_path):
                folder_path = filedialog.askdirectory()
                file_name = os.path.basename(file_path)
                timestamp = time.ctime(time.time())
                user_ip = self.get_user_ip()

                destination_folder = "files"
                os.makedirs(destination_folder, exist_ok=True)

                destination_path = os.path.join(destination_folder, file_name)

                shutil.copy(file_path, destination_path)

                file_info = f"File: {file_name}, Uploaded by: {user_ip}, Timestamp: {timestamp}"
                self.blockchain.add_block([file_info])
                self.update_output(f"File {file_name} uploaded to blockchain by {user_ip} at {timestamp}.")
            else:
                self.update_output(f"File not found at path: {file_path}")
        else:
            self.update_output("Upload canceled.")

    def download_with_location(self):
        block_index = simpledialog.askinteger("Block Selection", "Enter Block Index:")
        if block_index is not None:
            files_in_block = self.blockchain.view_files_in_blockchain()
            if len(files_in_block) > 0:
                file_name = simpledialog.askstring("File Selection", "Enter File Name:", initialvalue=files_in_block[0])
                if file_name:
                    cleaned_file_name = self.clean_file_name(file_name)
                    result = self.blockchain.download_file(block_index, cleaned_file_name)
                    if result:
                        self.update_output(result)
                    else:
                        self.update_output(f"Error downloading file {cleaned_file_name} from block {block_index}")

    def update_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def view_blockchain(self):
        blockchain = self.blockchain.get_blockchain()
        output = ""
        for block in blockchain:
            output += f"Block {block.index}:\n"
            output += f"Transactions: {block.transactions}\n"
            output += f"Previous Hash: {block.prev_hash}\n"
            output += f"Hash: {block.hash}\n\n"

        self.update_output(output)

    def view_files(self):
        files = self.blockchain.view_files_in_blockchain()
        if files:
            output = "Files in Blockchain:\n"
            for file in files:
                output += file + "\n"
        else:
            output = "No files found in Blockchain."

        self.update_output(output)

    def create_gui(self):
        self.output_text = tk.Text(self.root, height=20, width=60)
        self.output_text.pack()

        upload_button = tk.Button(self.root, text="Upload File to Blockchain", command=self.mine_and_upload)
        upload_button.pack()

        download_with_location_button = tk.Button(self.root, text="Download with Location",
                                                  command=self.download_with_location)
        download_with_location_button.pack()

        blockchain_frame = tk.Frame(self.root)
        blockchain_frame.pack()

        blockchain = self.blockchain.get_blockchain()
        for row, block in enumerate(blockchain, start=1):
            if block.transactions:
                tk.Label(blockchain_frame, text=block.index, padx=10, pady=5, borderwidth=1, relief="solid").grid(
                    row=row, column=0)
                tk.Label(blockchain_frame, text=", ".join(block.transactions), padx=10, pady=5, borderwidth=1,
                         relief="solid").grid(row=row, column=1)

        view_buttons_frame = tk.Frame(self.root)
        view_buttons_frame.pack()

        view_blockchain_button = tk.Button(view_buttons_frame, text="View Blockchain", command=self.view_blockchain)
        view_blockchain_button.grid(row=0, column=0)
