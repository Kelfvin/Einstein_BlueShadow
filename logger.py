class Logger(object):
    def __init__(self, log_path="default.log"):
        import sys
        self.terminal = sys.stdout
        self.log = open(log_path, "w", buffering=64, encoding="utf-8")

    def print(self, *message):
        message = ",".join([str(it) for it in message])
        self.terminal.write(str(message) + "\n")
        self.log.write(str(message) + "\n")

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        self.log.close()
