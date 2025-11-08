import socket
import threading
import time
import json
import select
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class GloffChat:
    """
    GloffChat - Local mesh chat for devices in network range
    Simple terminal-based chat
    """
    
    def __init__(self, username: str = "Anonymous", port: int = 8888):
        self.username = username
        self.port = port
        self.socket = None
        self.running = False
        self.peers = {}
        self.message_history = []
        self.discovery_socket = None
        
    def start(self):
        """Start the chat server and discovery"""
        self.running = True
        
        # Start server
        self._start_server()
        
        # Start discovery
        self._start_discovery()
        
        # Start listening for user input
        self._start_input_listener()
        
        console.print(Panel.fit(
            f"[green]GloffChat Started![/green]\n"
            f"Username: [yellow]{self.username}[/yellow]\n"
            f"Port: [yellow]{self.port}[/yellow]\n"
            f"Looking for peers in network...\n"
            f"Type your messages and press Enter\n"
            f"Type '/quit' to exit",
            title="🚀 GloffChat"
        ))
        
    def _start_server(self):
        """Start TCP server for receiving messages"""
        def server_thread():
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(1.0)
            
            try:
                self.socket.bind(('0.0.0.0', self.port))
                self.socket.listen(5)
                
                while self.running:
                    try:
                        client_socket, addr = self.socket.accept()
                        threading.Thread(
                            target=self._handle_client,
                            args=(client_socket, addr),
                            daemon=True
                        ).start()
                    except socket.timeout:
                        continue
                    except:
                        break
            except Exception as e:
                console.print(f"[red]Server error: {e}[/red]")
        
        threading.Thread(target=server_thread, daemon=True).start()
    
    def _start_discovery(self):
        """Start peer discovery using broadcast"""
        def discovery_thread():
            self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            message = json.dumps({
                'type': 'discovery',
                'username': self.username,
                'port': self.port,
                'timestamp': time.time()
            }).encode()
            
            while self.running:
                try:
                    # Broadcast to local network
                    self.discovery_socket.sendto(message, ('255.255.255.255', 8889))
                    
                    # Listen for responses
                    self.discovery_socket.settimeout(2.0)
                    try:
                        data, addr = self.discovery_socket.recvfrom(1024)
                        message = json.loads(data.decode())
                        if message.get('type') == 'discovery_response':
                            self._add_peer(addr[0], message)
                    except socket.timeout:
                        pass
                    
                    time.sleep(5)  # Broadcast every 5 seconds
                except Exception as e:
                    if self.running:
                        console.print(f"[red]Discovery error: {e}[/red]")
                    break
        
        threading.Thread(target=discovery_thread, daemon=True).start()
    
    def _start_input_listener(self):
        """Start listening for user input in terminal"""
        def input_thread():
            while self.running:
                try:
                    message = input()
                    if not self.running:
                        break
                        
                    if message.lower() == '/quit':
                        self.stop()
                        break
                    elif message.lower() == '/peers':
                        self._list_peers()
                    elif message.lower().startswith('/'):
                        console.print(f"[yellow]Unknown command: {message}[/yellow]")
                    else:
                        self.send_message(message)
                except (EOFError, KeyboardInterrupt):
                    self.stop()
                    break
                except Exception as e:
                    console.print(f"[red]Input error: {e}[/red]")
        
        threading.Thread(target=input_thread, daemon=True).start()
    
    def _handle_client(self, client_socket, addr):
        """Handle incoming client connection"""
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                return
                
            message = json.loads(data)
            
            if message.get('type') == 'discovery':
                # Respond to discovery
                response = json.dumps({
                    'type': 'discovery_response',
                    'username': self.username,
                    'port': self.port
                }).encode()
                client_socket.send(response)
                self._add_peer(addr[0], message)
                
            elif message.get('type') == 'message':
                username = message.get('username', 'Unknown')
                text = message.get('text', '')
                timestamp = message.get('timestamp', time.time())
                
                # Display message
                self._display_message(username, text, timestamp)
                
                self.message_history.append({
                    'username': username,
                    'text': text,
                    'timestamp': timestamp,
                    'type': 'received'
                })
                
        except Exception as e:
            console.print(f"[red]Error handling client: {e}[/red]")
        finally:
            client_socket.close()
    
    def _add_peer(self, ip: str, message: dict):
        """Add a discovered peer"""
        username = message.get('username', 'Unknown')
        port = message.get('port', self.port)
        
        if ip not in self.peers:
            self.peers[ip] = {
                'username': username,
                'port': port,
                'discovered_at': time.time()
            }
            console.print(f"[green]➕ Discovered peer: {username} @ {ip}[/green]")
    
    def _display_message(self, username: str, text: str, timestamp: float):
        """Display a message in the terminal"""
        time_str = time.strftime('%H:%M:%S', time.localtime(timestamp))
        
        if username == self.username:
            panel = Panel.fit(
                Text(text, style="blue"),
                title=f"👤 {username} [{time_str}]",
                border_style="blue"
            )
        else:
            panel = Panel.fit(
                Text(text, style="green"),
                title=f"👥 {username} [{time_str}]",
                border_style="green"
            )
        
        console.print(panel)
    
    def _list_peers(self):
        """List all discovered peers"""
        if not self.peers:
            console.print("[yellow]No peers discovered yet[/yellow]")
            return
            
        console.print("\n[cyan]📡 Discovered Peers:[/cyan]")
        for ip, info in self.peers.items():
            console.print(f"  • {info['username']} @ {ip}:{info['port']}")
    
    def send_message(self, text: str):
        """Send message to all discovered peers"""
        message = {
            'type': 'message',
            'username': self.username,
            'text': text,
            'timestamp': time.time()
        }
        
        message_json = json.dumps(message).encode()
        sent_to = 0
        
        for peer_ip, peer_info in self.peers.items():
            if peer_ip == '127.0.0.1':  # Don't send to self
                continue
                
            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.settimeout(2.0)
                peer_socket.connect((peer_ip, peer_info['port']))
                peer_socket.send(message_json)
                peer_socket.close()
                sent_to += 1
            except:
                # Remove unreachable peer
                del self.peers[peer_ip]
        
        # Display own message
        self._display_message(self.username, text, time.time())
        
        self.message_history.append({
            'username': self.username,
            'text': text,
            'timestamp': time.time(),
            'type': 'sent',
            'recipients': sent_to
        })
    
    def stop(self):
        """Stop the chat"""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.discovery_socket:
            self.discovery_socket.close()
        console.print("[red]GloffChat stopped[/red]")

def main():
    """CLI entry point for gloff-chat"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GloffChat - Local mesh chat')
    parser.add_argument('--username', '-u', required=True, help='Your username')
    parser.add_argument('--port', '-p', type=int, default=8888, help='Port to use')
    
    args = parser.parse_args()
    
    chat = GloffChat(args.username, args.port)
    
    try:
        chat.start()
        # Keep main thread alive
        while chat.running:
            time.sleep(1)
    except KeyboardInterrupt:
        chat.stop()
