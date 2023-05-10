class WrongEventType(Exception):
    def __init__(self, event_type, message='event.type must be only KEYDOWN'):
        self.message = message
        self.event_type = event_type
        super().__init__(self.message)
