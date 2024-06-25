class TicketStrategy:
    def get_price(self):
        raise NotImplementedError

class StandardTicket(TicketStrategy):
    def get_price(self):
        return 20

class VIPTicket(TicketStrategy):
    def get_price(self):
        return 50

class PlatinumTicket(TicketStrategy):
    def get_price(self):
        return 100

class TicketContext:
    def __init__(self, strategy: TicketStrategy):
        self._strategy = strategy

    def get_price(self):
        return self._strategy.get_price()
