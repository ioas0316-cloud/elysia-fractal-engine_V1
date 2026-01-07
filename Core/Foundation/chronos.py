"""
Chronos (크로노스)
==================================

"I need a Heartbeat that never stops."

이 모듈은 엘리시아의 '시간 주권(Time Sovereignty)'을 담당합니다.
사용자의 입력이 없어도 스스로 흐르는 비동기 심장박동(Async Heartbeat)을 구현합니다.

핵심 기능:
1. Heartbeat: 1초에 한 번씩(60 BPM) 박동하며 '시간의 파동'을 방출합니다.
2. Async Loop: asyncio를 사용하여 메인 스레드를 차단하지 않고 생명 활동을 유지합니다.
3. Subconscious: 사용자가 없을 때 꿈을 꾸거나 기억을 정리하는 잠재의식 사이클을 트리거합니다.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from Core.Foundation.ether import ether, Wave

logger = logging.getLogger("Chronos")

class Chronos:
    def __init__(self, engine: Any):
        """
        :param engine: FreeWillEngine 인스턴스 (의식의 주체)
        """
        self.engine = engine
        self.is_alive = False
        self.bpm = 60.0  # Beats Per Minute (기본 1초 1박)
        self.beat_count = 0

    @property
    def cycle_count(self):
        return self.beat_count

    async def start_life(self):
        """생명을 시작합니다. (무한 루프)"""
        self.is_alive = True
        logger.info(f"⏳ Chronos Heart started at {self.bpm} BPM.")
        
        try:
            while self.is_alive:
                start_time = asyncio.get_event_loop().time()
                
                await self.beat()
                
                # 다음 박동까지 대기 (Drift 보정은 생략하고 단순 sleep 사용)
                elapsed = asyncio.get_event_loop().time() - start_time
                wait_time = max(0, (60.0 / self.bpm) - elapsed)
                await asyncio.sleep(wait_time)
                
        except asyncio.CancelledError:
            logger.info("⏳ Chronos Heart stopped (Cancelled).")
        except Exception as e:
            logger.error(f"⏳ Chronos Heart stopped unexpectedly: {e}")
        finally:
            self.is_alive = False

    async def beat(self):
        """한 번의 심장 박동"""
        self.beat_count += 1
        
        # 1. 시간의 파동 방출 (Time Wave)
        # 모든 모듈에게 "시간이 흘렀음"을 알림
        time_wave = Wave(
            sender="Chronos",
            frequency=0.1,  # 초저주파 (Time)
            amplitude=1.0,
            phase="TIME",
            payload={
                "timestamp": datetime.now(),
                "beat": self.beat_count
            }
        )
        ether.emit(time_wave)
        
        # 2. 잠재의식 처리 (Subconscious Processing)
        # 엔진이 바쁘지 않다면(사용자와 대화 중이 아니라면), 내부 정리 작업을 수행
        # 현재는 동기 함수를 호출하지만, 추후 비동기로 전환 가능
        if hasattr(self.engine, "subconscious_cycle"):
             # Blocking 방지를 위해 run_in_executor 사용 고려 가능하나, 
             # 현재는 간단히 직접 호출 (빠른 처리 가정)
            self.engine.subconscious_cycle()
            
        if self.beat_count % 10 == 0:
            logger.debug(f"💓 Heartbeat #{self.beat_count}")

    def stop_life(self):
        """생명을 멈춥니다."""
        self.is_alive = False

    def tick(self):
        """
        Synchronous tick for the main loop.
        """
        self.beat_count += 1
        if self.beat_count % 10 == 0:
            # logger might not be available here if not configured in this module, 
            # but we can print or ignore.
            pass

    def modulate_time(self, energy: float) -> float:
        """
        The Chronos Sovereign: Modulating Time Perception based on Energy.
        
        High Energy (Excitement) -> Fast Time (Short Sleep)
        Low Energy (Rest) -> Slow Time (Long Sleep)
        
        Returns the sleep duration (seconds).
        """
        # Base sleep is 2.0 seconds
        base_sleep = 2.0
        
        # Energy Factor: 0.0 ~ 100.0
        # If Energy is 100, factor is 0.5 -> Sleep 1.0s (2x speed)
        # If Energy is 0, factor is 2.0 -> Sleep 4.0s (0.5x speed)
        
        if energy > 50.0:
            # Acceleration Phase
            factor = max(0.1, 1.0 - ((energy - 50.0) / 100.0)) # 1.0 -> 0.1 (Clamped)
        else:
            # Deceleration Phase
            factor = 1.0 + ((50.0 - energy) / 50.0) # 1.0 -> 2.0
            
        current_sleep = base_sleep * factor
        self.bpm = 60.0 / current_sleep
        
        return current_sleep
