"""
Beaver's Choice Paper Company - Multi-Agent System
A comprehensive solution for intelligent inventory and sales management.
"""

__version__ = "1.0.0"
__author__ = "Feras Khairallah"

from .agents import (
    inventory_agent,
    quoting_agent,
    sales_agent,
    orchestrator_agent,
    process_customer_request
)

from .tools import (
    check_inventory_tool,
    get_all_inventory_tool,
    order_stock_tool,
    search_quote_history_tool,
    calculate_quote_tool,
    check_stock_availability_tool,
    create_sale_tool,
    get_delivery_estimate_tool
)

__all__ = [
    # Agents
    "inventory_agent",
    "quoting_agent",
    "sales_agent",
    "orchestrator_agent",
    "process_customer_request",
    # Tools
    "check_inventory_tool",
    "get_all_inventory_tool",
    "order_stock_tool",
    "search_quote_history_tool",
    "calculate_quote_tool",
    "check_stock_availability_tool",
    "create_sale_tool",
    "get_delivery_estimate_tool",
]
