#!/usr/bin/local/python3.14

"""
TCP Chat Server implementation

This module provides a multi-client chat server that:
- Listens on a specified TCP port for client connections
- Supports multiple concurrent clients (at least 2)
- Routes messages between clients
- Provides delivery confirmation
- Logs all communication events
"""

import socket
import threading
import logging
from datetime import datetime

class ChatServer:
    """
    TCP Chat Server class that handles multiple client connections and message routing.
    """
    
    def __init__(self, host='0.0.0.0', port=5555):
        """
        Initialize the chat server.
        
        Args:
            host (str): Host address to bind to. Defaults to '0.0.0.0'.
            port (int): Port number to listen on. Defaults to 5555.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Format: {client_socket: {'name': str, 'address': tuple}}
        self.lock = threading.Lock()
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the server."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='chat_server.log',
            filemode='a'
        )
        logging.info("Server logging initialized")
        
    def start(self):
        """Start the chat server and begin accepting connections."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            logging.info(f"Server started on {self.host}:{self.port}")
            print(f"Chat server is running on {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                ).start()
                
        except Exception as e:
            logging.error(f"Server error: {e}")
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()
            logging.info("Server socket closed")
            
    def handle_client(self, client_socket, client_address):
        """
        Handle communication with a connected client.
        
        Args:
            client_socket (socket.socket): Socket object for the client connection.
            client_address (tuple): Client's address (ip, port).
        """
        try:
            # Get client name (first message should be the name)
            name = client_socket.recv(1024).decode('utf-8').strip()
            if not name:
                raise ValueError("No name provided")
                
            with self.lock:
                self.clients[client_socket] = {'name': name, 'address': client_address}
                
            logging.info(f"New connection: {name} from {client_address}")
            self.broadcast(f"{name} has joined the chat!", exclude=client_socket)
            client_socket.sendall("Connected to the chat server!".encode('utf-8'))
            
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                logging.info(f"Message from {name}: {message}")
                
                # Check if it's a private message (format: @recipient message)
                if message.startswith('@'):
                    recipient, *msg_parts = message[1:].split(' ', 1)
                    if not msg_parts:
                        client_socket.sendall("Invalid private message format".encode('utf-8'))
                        continue
                        
                    private_msg = msg_parts[0]
                    self.send_private(name, recipient, private_msg, client_socket)
                else:
                    self.broadcast(f"{name}: {message}", exclude=client_socket)
                    
        except Exception as e:
            logging.error(f"Error with client {client_address}: {e}")
        finally:
            with self.lock:
                if client_socket in self.clients:
                    disconnected_name = self.clients[client_socket]['name']
                    del self.clients[client_socket]
                    self.broadcast(f"{disconnected_name} has left the chat.")
                    logging.info(f"{disconnected_name} disconnected")
            client_socket.close()
            
    def send_private(self, sender, recipient_name, message, sender_socket):
        """
        Send a private message to a specific recipient.
        
        Args:
            sender (str): Name of the message sender.
            recipient_name (str): Name of the recipient.
            message (str): The message content.
            sender_socket (socket.socket): Socket of the sender.
        """
        recipient_socket = None
        with self.lock:
            for sock, client_info in self.clients.items():
                if client_info['name'] == recipient_name:
                    recipient_socket = sock
                    break
                    
        if recipient_socket:
            try:
                timestamp = datetime.now().strftime('%H:%M:%S')
                full_msg = f"[{timestamp}] PM from {sender}: {message}"
                recipient_socket.sendall(full_msg.encode('utf-8'))
                sender_socket.sendall(f"Message delivered to {recipient_name}".encode('utf-8'))
                logging.info(f"Private message from {sender} to {recipient_name}")
            except Exception as e:
                sender_socket.sendall(f"Failed to deliver message to {recipient_name}".encode('utf-8'))
                logging.error(f"Private message delivery failed: {e}")
        else:
            sender_socket.sendall(f"Recipient {recipient_name} not found".encode('utf-8'))
            logging.warning(f"Recipient {recipient_name} not found")
            
    def broadcast(self, message, exclude=None):
        """
        Broadcast a message to all connected clients except the excluded one.
        
        Args:
            message (str): Message to broadcast.
            exclude (socket.socket, optional): Socket to exclude from broadcast. Defaults to None.
        """
        with self.lock:
            for client_socket in self.clients:
                if client_socket != exclude:
                    try:
                        client_socket.sendall(message.encode('utf-8'))
                    except Exception as e:
                        logging.error(f"Broadcast failed to {self.clients[client_socket]['name']}: {e}")

if __name__ == "__main__":
    server = ChatServer()
    server.start()
