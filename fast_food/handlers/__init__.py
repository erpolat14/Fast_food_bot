from .start import register_start_handlers
from .order import register_order_handlers

def register_handlers(dp):
    register_start_handlers(dp)
    register_order_handlers(dp)