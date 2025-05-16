#! usr/local/bin/python3.14

"""
TCP Chat Client implementation

This module provides a chat client that can:
- Connect to a chat server
- Send messages to other clients
- Receive messages from the server
- Get delivery confirmations
"""

import socket
import threading
import sys
import logging

class ChatClient:
    """
    TCP Chat Client class that connects to a server and handles messaging.
    """
    
    def __init__(self, server_host='localhost', server_port=5555):
        """
        Initialize the chat client.
        
        Args:
            server_host (str): Server host address. Defaults to 'localhost'.
            server_port (int): Server port number. Defaults to 5555.
        """
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.name = None
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the client."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='chat_client.log',
            filemode='a'
        )
        logging.info("Client logging initialized")
        
    def connect(self, name):
        """
        Connect to the chat server with the specified name.
        
        Args:
            name (str): Name to identify the client in the chat.
        """
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            self.client_socket.sendall(name.encode('utf-8'))
            self.name = name
            self.running = True
            
            # Start thread for receiving messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            logging.info(f"Connected to server as {name}")
            
            print(f"Connected to chat server as {name}")
            print("Type your messages. Use @recipient for private messages.")
            print("Type 'exit' to quit.")
            
            self.send_messages()
            
        except Exception as e:
            logging.error(f"Connection error: {e}")
            print(f"Connection error: {e}")
        finally:
            self.disconnect()
            
    def receive_messages(self):
        """Receive messages from the server and display them."""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}\nYou: ", end='', flush=True)
                logging.info(f"Received message: {message}")
            except Exception as e:
                logging.error(f"Receive error: {e}")
                break
                
    def send_messages(self):
        """Handle user input and send messages to the server."""
        while self.running:
            try:
                message = input("You: ")
                if message.lower() == 'exit':
                    self.running = False
                    break
                    
                if message:
                    self.client_socket.sendall(message.encode('utf-8'))
                    logging.info(f"Sent message: {message}")
                    
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                logging.error(f"Send error: {e}")
                print(f"Error sending message: {e}")
                
    def disconnect(self):
        """Cleanly disconnect from the server."""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        logging.info("Disconnected from server")
        print("Disconnected from server")
        
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python console_chat_client.py <server_host> <server_port> <name>")
        sys.exit(1)
        
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]
    
    client = ChatClient(host, port)
    client.connect(name)
