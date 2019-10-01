from enum import Enum


class OrderState(Enum):
    INITIATED = 'In the shopping cart'
    CONFIRMED = 'Sizzling in the kitchen'
    COMPLETED = 'On its way'
    DELIVERED = "Delivered to you"
