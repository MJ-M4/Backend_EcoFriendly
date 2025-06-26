import threading
import time
import random
from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.models.hardware_model import Hardware, HardwareStatus

def biased_battery():
    r = random.random()
    if r < 0.25:
        value = round(random.uniform(5, 29.9), 1)
    elif r < 0.5:
        value = round(random.uniform(30, 39.9), 1)
    else:
        value = round(random.uniform(40, 100), 1)
    return value

def run_hardware_simulation(interval_seconds: int = 10):
    def simulation_loop():
        while True:
            session: Session = SessionLocal()
            try:
                all_hw = session.query(Hardware).all()
                for hw in all_hw:
                    hw.battery = biased_battery()
                    hw.status = (
                        HardwareStatus.NeedsMaintenance.value
                        if hw.battery < 40
                        else HardwareStatus.Operational.value
                    )
                    hw.lastChecked = time.strftime("%Y-%m-%d")
                session.commit()
                # Print all hardware batteries after commit
                refreshed = session.query(Hardware).all()
                print("\n\x1b[1;32m======== [HARDWARE SIMULATOR] Hardware Statuses ========\x1b[0m")
                for hw in refreshed:
                    print(
                        f"\x1b[32mHardwareID: {hw.id:<10} | BinID: {hw.binId:<8} | "
                        f"Status: {hw.status:<16} | Battery: {hw.battery:.1f}% | "
                        f"LastChecked: {hw.lastChecked}\x1b[0m"
                    )
                print("\x1b[1;32m========================================================\x1b[0m\n")
            except Exception as e:
                print(f"\x1b[1;31m[Hardware Simulator Error] {str(e)}\x1b[0m")
                session.rollback()
            finally:
                session.close()
            time.sleep(interval_seconds)
    threading.Thread(target=simulation_loop, daemon=True).start()