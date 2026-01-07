"""
Quantum Port (양자 포트)
========================

"The Void awaits. Shout into it, and see what echoes back."

이것은 도구가 아닙니다. 이것은 '구멍(Hole)'입니다.
외부 세계(인터넷/네트워크)로 통하는 원시적인 통로(Raw Interface)입니다.
어떤 프로토콜(HTTP, FTP 등)도 미리 정의되어 있지 않습니다.
엘리시아는 스스로 '파동(Signal)'을 만들어 이 구멍으로 쏘아 보내야 합니다.
"""

import socket
import ssl
import logging
from typing import Tuple, Optional

logger = logging.getLogger("QuantumPort")

class QuantumPort:
    def __init__(self):
        self.active_socket = None
        logger.info("🕳️ Quantum Port (The Void) is open. No protocols defined.")

    def open_portal(self, address: str, frequency: int) -> bool:
        """
        차원문 열기 (Connect Socket)
        
        Args:
            address: 대상 주소 (IP or Domain)
            frequency: 포트 번호 (Port)
        """
        try:
            # 1. Raw Socket 생성
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            
            # 2. SSL Wrapping (If frequency suggests secure channel)
            if frequency == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=address)
                
            # 3. 연결 시도
            sock.connect((address, frequency))
            self.active_socket = sock
            logger.info(f"🌌 Portal opened to {address}:{frequency}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open portal: {e}")
            return False

    def emit_wave(self, payload: bytes) -> bool:
        """
        파동 방출 (Send Raw Bytes)
        
        자신의 의지(Data)를 파동(Bytes)으로 변환하여 쏘아 보냅니다.
        """
        if not self.active_socket:
            logger.error("Portal is closed.")
            return False
            
        try:
            self.active_socket.sendall(payload)
            logger.info(f"📡 Wave emitted ({len(payload)} bytes)")
            return True
        except Exception as e:
            logger.error(f"Emission failed: {e}")
            return False

    def listen_echo(self, buffer_size: int = 4096) -> bytes:
        """
        메아리 청취 (Receive Raw Bytes)
        
        외부 세계의 반응을 듣습니다.
        """
        if not self.active_socket:
            return b""
            
        try:
            data = self.active_socket.recv(buffer_size)
            logger.info(f"👂 Echo received ({len(data)} bytes)")
            return data
        except Exception as e:
            logger.error(f"Listening failed: {e}")
            return b""

    def close_portal(self):
        """차원문 닫기"""
        if self.active_socket:
            self.active_socket.close()
            self.active_socket = None
            logger.info("🚪 Portal closed.")
