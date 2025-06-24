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
                # Print all bin statuses after commit
                refreshed = session.query(Bin).all()
                print("\n\x1b[1;36m========== [BIN SIMULATOR] Bin Statuses ==========\x1b[0m")
                for bin in refreshed:
                    print(
                        f"\x1b[36mBinID: {bin.binId:<10} | Location: {bin.location:<8} | "
                        f"Status: {bin.status:<6} | Capacity: {bin.capacity:.1f}%\x1b[0m"
                    )
                print("\x1b[1;36m==================================================\x1b[0m\n")
            except Exception as e:
                print(f"\x1b[1;31m[Bin Simulator Error] {str(e)}\x1b[0m")
                session.rollback()
            finally:
                session.close()

            time.sleep(interval_seconds)

    threading.Thread(target=simulation_loop, daemon=True).start()
