import logging
import datetime
import threading
import queue
import os
from dotenv import load_dotenv

class ChronosQueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        timestamp = datetime.datetime.fromtimestamp(record.created).isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": record.levelname,
            "level_num": record.levelno,
            "message": record.getMessage(),
            "context": getattr(record, "context", {}),
        }
        self.log_queue.put(log_entry)

class ChronosLogger:
    def __init__(self, name="chronos", level=logging.INFO, max_queue_size=1000):
        self.name = name
        self.level = level
        self._queue = queue.Queue(maxsize=max_queue_size)
        self._thread = threading.Thread(target=self._process_queue, daemon=True)
        self._thread.start()
        self._handlers = []
        self._level_names = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.CRITICAL: "CRITICAL",
        }

    def addHandler(self, handler: logging.Handler) -> None:
        self._handlers.append(handler)

    def log(self, level: int, message: str, context: dict = None) -> None:
        try:
            timestamp = datetime.datetime.now().isoformat()
            log_entry = {
                "timestamp": timestamp,
                "level": self._level_names.get(level, str(level)),
                "level_num": level,
                "message": message,
                "context": context or {},
            }
            self._queue.put_nowait(log_entry)
        except queue.Full:
            logging.warning("ChronosLogger queue is full, log entry dropped.")

    def _process_queue(self) -> None:
        while True:
            try:
                log_entry = self._queue.get()
                if log_entry is None:
                    self._queue.task_done()
                    break
                for handler in self._handlers:
                    if log_entry["level_num"] >= handler.level:
                        handler.emit(logging.makeLogRecord(log_entry))
                self._queue.task_done()
            except Exception as e:
                logging.error(f"Error processing log queue: {e}")

    def info(self, message: str, context: dict = None) -> None:
        self.log(logging.INFO, message, context)

    def warning(self, message: str, context: dict = None) -> None:
        self.log(logging.WARNING, message, context)

    def error(self, message: str, context: dict = None) -> None:
        self.log(logging.ERROR, message, context)

    def wait(self) -> None:
        self._queue.join()

    def close(self) -> None:
        self._queue.put(None)
        self._thread.join(timeout=1.0)
        for handler in self._handlers:
            if hasattr(handler, 'close'):
                handler.close()
        self._handlers.clear()

# Example usage within your AI system:

def setup_chronos_logging():
    load_dotenv()
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    log_queue = queue.Queue()
    queue_handler = ChronosQueueHandler(log_queue)
    queue_handler.setLevel(numeric_level)

    chronos_logger = ChronosLogger()
    chronos_logger.addHandler(queue_handler)

    # Add a file handler for logging to a file
    file_handler = logging.FileHandler('ai_system.log')
    file_handler.setLevel(numeric_level)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(context)s')
    file_handler.setFormatter(file_formatter)
    chronos_logger.addHandler(file_handler)

    return chronos_logger

if __name__ == "__main__":
    chronos_logger = setup_chronos_logging()

    chronos_logger.info("AI System started", context={"system": "startup"})
    chronos_logger.warning("Potential issue detected", context={"system": "warning", "code": "W100"})
    chronos_logger.error("An error occurred", context={"system": "error", "code": "E200"})

    chronos_logger.wait()
    chronos_logger.close()