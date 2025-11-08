import socket
import threading
import time
import json
from rich.console import Console
from rich.panel import Panel

console = Console()

class GloffChat:
    def __init__(self, username: str = "User", port: int = 8888):
        self.username = username
        self.port = port
        self.running = False
        self.peers = {}
        self.message_history = []
    
    def start(self):
        """Запуск чата"""
        self.running = True
        
        # Запускаем сервер и discovery в отдельных потоках
        threading.Thread(target=self._start_server, daemon=True).start()
        threading.Thread(target=self._start_discovery, daemon=True).start()
        threading.Thread(target=self._start_input, daemon=True).start()
        
        console.print(Panel.fit(
            f"[green]GloffChat Started![/green]\n"
            f"Username: [yellow]{self.username}[/yellow]\n"
            f"Port: [yellow]{self.port}[/yellow]\n"
            f"🌐 Local network only\n"
            f"📡 Range: WiFi coverage (50-100m)\n"
            f"Type messages and press Enter\n"
            f"Type '/quit' to exit",
            title="💬 GloffChat"
        ))
    
    def _start_server(self):
        """TCP сервер для приёма сообщений"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(1.0)
        
        try:
            sock.bind(('0.0.0.0', self.port))
            sock.listen(5)
            
            while self.running:
                try:
                    client, addr = sock.accept()
                    threading.Thread(
                        target=self._handle_client, 
                        args=(client, addr), 
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
        except Exception as e:
            console.print(f"[red]Server error: {e}[/red]")
        finally:
            sock.close()
    
    def _start_discovery(self):
        """Поиск других пользователей в сети"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        discovery_msg = json.dumps({
            'type': 'discovery',
            'username': self.username,
            'port': self.port
        }).encode()
        
        while self.running:
            try:
                # Рассылаем broadcast
                sock.sendto(discovery_msg, ('255.255.255.255', 8889))
                time.sleep(5)
            except:
                break
    
    def _start_input(self):
        """Обработка ввода пользователя"""
        while self.running:
            try:
                message = input()
                if not self.running:
                    break
                    
                if message.lower() == '/quit':
                    self.stop()
                    break
                elif message.lower() == '/peers':
                    self._show_peers()
                elif message.lower() == '/help':
                    self._show_help()
                else:
                    self.send_message(message)
            except (EOFError, KeyboardInterrupt):
                self.stop()
                break
            except Exception as e:
                console.print(f"[red]Input error: {e}[/red]")
    
    def _handle_client(self, client, addr):
        """Обработка входящих соединений"""
        try:
            data = client.recv(1024).decode()
            if not data:
                return
                
            message = json.loads(data)
            
            if message.get('type') == 'discovery':
                # Отвечаем на discovery
                response = json.dumps({
                    'type': 'discovery_response', 
                    'username': self.username,
                    'port': self.port
                }).encode()
                client.send(response)
                self._add_peer(addr[0], message)
                
            elif message.get('type') == 'message':
                username = message.get('username', 'Unknown')
                text = message.get('text', '')
                
                # Показываем сообщение
                self._display_message(username, text, is_own=False)
                
                self.message_history.append({
                    'username': username,
                    'text': text,
                    'timestamp': time.time(),
                    'type': 'received'
                })
                
        except Exception as e:
            console.print(f"[red]Client error: {e}[/red]")
        finally:
            client.close()
    
    def _add_peer(self, ip: str, message: dict):
        """Добавляем найденного пользователя"""
        if ip not in self.peers:
            self.peers[ip] = {
                'username': message.get('username', 'Unknown'),
                'port': message.get('port', self.port)
            }
            console.print(f"[green]➕ Found: {message.get('username')} @ {ip}[/green]")
    
    def _display_message(self, username: str, text: str, is_own: bool = False):
        """Красивый вывод сообщения"""
        time_str = time.strftime('%H:%M:%S')
        
        if is_own:
            panel = Panel.fit(
                f"{text}",
                title=f"👤 {username} [{time_str}]",
                border_style="blue"
            )
        else:
            panel = Panel.fit(
                f"{text}", 
                title=f"👥 {username} [{time_str}]",
                border_style="green"
            )
        
        console.print(panel)
    
    def _show_peers(self):
        """Показать список подключенных"""
        if not self.peers:
            console.print("[yellow]No peers found yet[/yellow]")
            return
            
        console.print("\n[cyan]📡 Connected peers:[/cyan]")
        for ip, info in self.peers.items():
            console.print(f"  • {info['username']} @ {ip}")
    
    def _show_help(self):
        """Показать справку"""
        console.print(Panel.fit(
            "[green]GloffChat Commands:[/green]\n"
            "/help - Show this help\n" 
            "/peers - Show connected users\n"
            "/quit - Exit chat\n"
            "Any other text - Send message",
            title="❓ Help"
        ))
    
    def send_message(self, text: str):
        """Отправить сообщение всем"""
        message = json.dumps({
            'type': 'message',
            'username': self.username,
            'text': text,
            'timestamp': time.time()
        }).encode()
        
        sent_to = 0
        
        for peer_ip, peer_info in self.peers.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2.0)
                sock.connect((peer_ip, peer_info['port']))
                sock.send(message)
                sock.close()
                sent_to += 1
            except:
                # Удаляем недоступного
                del self.peers[peer_ip]
        
        # Показываем своё сообщение
        self._display_message(self.username, text, is_own=True)
        
        self.message_history.append({
            'username': self.username, 
            'text': text,
            'timestamp': time.time(),
            'type': 'sent',
            'recipients': sent_to
        })
    
    def stop(self):
        """Остановка чата"""
        self.running = False
        console.print("[red]Chat stopped[/red]")

def main():
    """CLI команда для запуска чата"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GloffChat - Local network chat')
    parser.add_argument('--username', '-u', required=True, help='Your username')
    parser.add_argument('--port', '-p', type=int, default=8888, help='Port to use')
    
    args = parser.parse_args()
    
    chat = GloffChat(args.username, args.port)
    
    try:
        chat.start()
        # Держим основной поток alive
        while chat.running:
            time.sleep(1)
    except KeyboardInterrupt:
        chat.stop()
