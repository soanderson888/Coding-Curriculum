import tkinter as tk
from cryptography.fernet import Fernet
import threading
import socket
import traceback



class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.key = None

    def generate_key(self):
        self.key = Fernet.generate_key()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Server started. Listening for connections...")
        self.client_socket, _ = self.server_socket.accept()
        print("Connected to client.")

    def send_key(self):
        self.client_socket.sendall(self.key)

    def send_message(self, message):
        encrypted_message = self.encrypt_message(message)
        self.client_socket.sendall(encrypted_message)

    def receive_message(self):
        encrypted_message = self.client_socket.recv(4096)
        decrypted_message = self.decrypt_message(encrypted_message)
        return decrypted_message

    def encrypt_message(self, message):
        cipher_suite = Fernet(self.key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        cipher_suite = Fernet(self.key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

    def close(self):
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()


class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.key = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Connected to server.")

    def receive_key(self):
        self.key = self.client_socket.recv(4096)

    def send_message(self, message):
        encrypted_message = self.encrypt_message(message)
        self.client_socket.sendall(encrypted_message)

    def receive_message(self):
        encrypted_message = self.client_socket.recv(4096)
        decrypted_message = self.decrypt_message(encrypted_message)
        return decrypted_message

    def encrypt_message(self, message):
        cipher_suite = Fernet(self.key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        cipher_suite = Fernet(self.key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

    def close(self):
        if self.client_socket:
            self.client_socket.close()


def validate_input(message):
   
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"]
    special_characters = ["'", "\"", ";"]

    for keyword in sql_keywords:
        if keyword in message.upper():
            return False

    for char in special_characters:
        if char in message:
            return False

    return True

class ChatApplication(tk.Tk):
    def __init__(self, title, host, port):
        super().__init__()
        self.title(title)
        self.host = host
        self.port = port
        self.chat_server = None
        self.chat_client = None
        self.chat_text = tk.Text(self)
        self.chat_text.pack()
        self.message_entry = tk.Entry(self)
        self.message_entry.pack()
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack()

    def start_server(self):
        self.chat_server = ChatServer(self.host, self.port)
        self.chat_server.generate_key()
        self.chat_server.start()
        self.chat_server.send_key()
        self.receive_messages()

    def start_client(self):
        self.chat_client = ChatClient(self.host, self.port)
        self.chat_client.connect()
        self.chat_client.receive_key()
        self.receive_messages()

    def send_message(self):
        message = self.message_entry.get()
        if not validate_input(message):
            self.display_error("Invalid input: Potential SQL injection or XSS attack.")
            return

        if self.chat_server:
            self.chat_server.send_message(message)
        elif self.chat_client:
            self.chat_client.send_message(message)

        self.display_message("You: " + message)
        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        threading.Thread(target=self.receive_loop).start()

    def receive_loop(self):
        while True:
            try:
                if self.chat_server:
                    message = self.chat_server.receive_message()
                elif self.chat_client:
                    message = self.chat_client.receive_message()

                self.display_message("Other user: " + message)
            except Exception as e:
                self.display_error("Exception occurred during decryption:")
                traceback.print_exc()
                break

    def display_error(self, error_message):
        self.chat_text.insert(tk.END, "Error: " + error_message + "\n")

    def display_message(self, message):
        self.chat_text.insert(tk.END, message + "\n")

    def close(self):
        if self.chat_server:
            self.chat_server.close()
        if self.chat_client:
            self.chat_client.close()
        self.destroy()

def main():
    host = 'localhost'
    port = 12345

    choice = input("Enter 's' to start as server or 'c' to start as client: ")

    if choice.lower() == 's':
        chat_app = ChatApplication("Secure Chat Server", host, port)
        chat_app.start_server()
        chat_app.mainloop()
        chat_app.close()
    elif choice.lower() == 'c':
        chat_app = ChatApplication("Secure Chat Client", host, port)
        chat_app.start_client()
        chat_app.mainloop()
        chat_app.close()
    else:
        print("Invalid choice. Exiting...")

if __name__ == '__main__':
    main()
