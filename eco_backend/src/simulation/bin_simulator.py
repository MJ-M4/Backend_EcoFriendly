import threading
import time
import random
from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.models.bin_model import Bin, BinStatus

def simulate_bin_status(bin: Bin):
    # capacity = 0 to 100
    bin.capacity = round(random.uniform(0, 100), 1)

    # Update status based on capacity
    if bin.capacity >= 75:
        bin.status = BinStatus.Full.value
    elif bin.capacity >= 35:
        bin.status = BinStatus.Mid.value
    else:
        bin.status = BinStatus.Empty.value

def run_bin_simulation(interval_seconds: int = 10):
    def simulation_loop():
        while True:
            session: Session = SessionLocal()
            try:
                bins = session.query(Bin).all()
                for bin in bins:
                    simulate_bin_status(bin)
                session.commit()
                print("[Simulator] Bin statuses updated.")
            except Exception as e:
                print(f"[Simulator Error] {str(e)}")
                session.rollback()
            finally:
                session.close()

            time.sleep(interval_seconds)

    # Run in background thread
    thread= threading.Thread(target=simulation_loop, daemon=True)
    thread.start()