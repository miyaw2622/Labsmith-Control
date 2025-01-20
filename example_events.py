class MyClass:
    def __init__(self):
        # List to store listeners
        self._listeners = []

    def add_listener(self, callback):
        """Add a listener (callback) to the event."""
        if callable(callback):
            self._listeners.append(callback)

    def trigger_event(self):
        """Trigger the event and notify all listeners."""
        print("Event triggered!")
        for callback in self._listeners:
            callback()

# Listener Example
def on_event():
    print("Listener responded to the event!")

obj = MyClass()
obj.add_listener(on_event)  # Add listener
obj.trigger_event()         # Trigger event
