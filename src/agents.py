"""
Beaver's Choice Paper Company - Agent Definitions
Defines all AI agents and their coordination logic.
"""

import os
from smolagents import ToolCallingAgent, LiteLLMModel
from tools import (
    check_inventory_tool,
    get_all_inventory_tool,
    order_stock_tool,
    search_quote_history_tool,
    calculate_quote_tool,
    check_stock_availability_tool,
    create_sale_tool,
    get_delivery_estimate_tool
)

# Initialize the LLM model
api_key = os.getenv("UDACITY_OPENAI_API_KEY")
if not api_key:
    raise ValueError("UDACITY_OPENAI_API_KEY not found in environment variables")

model = LiteLLMModel(
    model_id="openai/gpt-4o-mini",
    api_key=api_key,
    api_base="https://openai.vocareum.com/v1"
)

# ==================== SPECIALIST AGENTS ====================

inventory_agent = ToolCallingAgent(
    tools=[check_inventory_tool, get_all_inventory_tool, order_stock_tool, get_delivery_estimate_tool],
    model=model,
    name="InventoryAgent",
    description="Specialist in inventory management, stock checking, and reordering supplies."
)

quoting_agent = ToolCallingAgent(
    tools=[search_quote_history_tool, calculate_quote_tool, check_inventory_tool],
    model=model,
    name="QuotingAgent",
    description="Specialist in generating competitive quotes based on historical data and current pricing."
)

sales_agent = ToolCallingAgent(
    tools=[check_stock_availability_tool, create_sale_tool, get_delivery_estimate_tool],
    model=model,
    name="SalesAgent",
    description="Specialist in finalizing sales transactions and order fulfillment."
)

# ==================== ORCHESTRATOR AGENT ====================

orchestrator_agent = ToolCallingAgent(
    tools=[],
    model=model,
    name="OrchestratorAgent",
    description="Main coordinator that analyzes requests and delegates to specialist agents.",
    managed_agents=[inventory_agent, quoting_agent, sales_agent]
)

# ==================== REQUEST PROCESSING ====================

def process_customer_request(request: str, request_date: str) -> str:
    """
    Process a customer request through the multi-agent system.
    
    Args:
        request: Customer's request text
        request_date: Date of the request (YYYY-MM-DD format)
    
    Returns:
        Response from the multi-agent system
    """
    # Enhanced prompt for the orchestrator
    system_prompt = f"""You are the Orchestrator Agent for Beaver's Choice Paper Company.
    
Your role is to analyze customer requests and coordinate with specialist agents:
- InventoryAgent: For checking stock, reordering supplies
- QuotingAgent: For generating price quotes
- SalesAgent: For finalizing orders and sales

Current date: {request_date}

IMPORTANT GUIDELINES:
1. For quote requests: Use QuotingAgent to search history and calculate quotes
2. For inventory questions: Use InventoryAgent to check stock levels
3. For order placement: Use SalesAgent to verify availability and create sales
4. If stock is low after a sale, use InventoryAgent to reorder
5. Always provide clear, professional responses to customers
6. Include relevant details like pricing, delivery dates, and availability

Analyze the following request and coordinate the appropriate agents to fulfill it:

{request}
"""
    
    try:
        response = orchestrator_agent.run(system_prompt)
        return str(response)
    except Exception as e:
        return f"Error processing request: {str(e)}"
