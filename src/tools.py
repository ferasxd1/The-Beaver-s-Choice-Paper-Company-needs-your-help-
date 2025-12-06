"""
Beaver's Choice Paper Company - Agent Tools
Defines all tools that agents can use to interact with the system.
"""

import pandas as pd
from smolagents import tool
from utils import (
    get_stock_level,
    get_all_inventory,
    create_transaction,
    get_cash_balance,
    get_supplier_delivery_date,
    search_quote_history,
    db_engine
)

# ==================== INVENTORY TOOLS ====================

@tool
def check_inventory_tool(item_name: str, request_date: str) -> str:
    """
    Check the current stock level of a specific item.
    
    Args:
        item_name: Name of the item to check
        request_date: Date for the inventory check (YYYY-MM-DD format)
    
    Returns:
        String describing the current stock level and item details
    """
    try:
        # Get stock level
        stock_df = get_stock_level(item_name, request_date)
        current_stock = int(stock_df["current_stock"].iloc[0])
        
        # Get item details from inventory
        inventory_df = pd.read_sql("SELECT * FROM inventory WHERE item_name = :item", 
                                   db_engine, params={"item": item_name})
        
        if inventory_df.empty:
            return f"Item '{item_name}' is not in our inventory catalog."
        
        item_info = inventory_df.iloc[0]
        min_stock = int(item_info["min_stock_level"])
        unit_price = float(item_info["unit_price"])
        
        status = "ADEQUATE" if current_stock >= min_stock else "LOW - REORDER NEEDED"
        
        return (f"Item: {item_name}\n"
                f"Current Stock: {current_stock} units\n"
                f"Minimum Stock Level: {min_stock} units\n"
                f"Unit Price: ${unit_price:.2f}\n"
                f"Status: {status}")
    
    except Exception as e:
        return f"Error checking inventory for {item_name}: {str(e)}"

@tool
def get_all_inventory_tool(request_date: str) -> str:
    """
    Get a complete list of all items currently in stock.
    
    Args:
        request_date: Date for the inventory snapshot (YYYY-MM-DD format)
    
    Returns:
        String listing all items with their stock levels
    """
    try:
        inventory_dict = get_all_inventory(request_date)
        
        if not inventory_dict:
            return "No items currently in stock."
        
        result = "CURRENT INVENTORY:\n" + "="*50 + "\n"
        for item, stock in sorted(inventory_dict.items()):
            result += f"• {item}: {stock} units\n"
        
        return result
    
    except Exception as e:
        return f"Error retrieving inventory: {str(e)}"

@tool
def order_stock_tool(item_name: str, quantity: int, request_date: str) -> str:
    """
    Place an order with the supplier to restock an item.
    
    Args:
        item_name: Name of the item to order
        quantity: Quantity to order
        request_date: Date of the order (YYYY-MM-DD format)
    
    Returns:
        String confirming the order and delivery date
    """
    try:
        # Get item price
        inventory_df = pd.read_sql("SELECT * FROM inventory WHERE item_name = :item", 
                                   db_engine, params={"item": item_name})
        
        if inventory_df.empty:
            return f"Cannot order '{item_name}' - not in our catalog."
        
        unit_price = float(inventory_df.iloc[0]["unit_price"])
        total_cost = quantity * unit_price
        
        # Check if we have enough cash
        current_cash = get_cash_balance(request_date)
        if current_cash < total_cost:
            return (f"INSUFFICIENT FUNDS: Order costs ${total_cost:.2f} but only "
                   f"${current_cash:.2f} available. Cannot place order.")
        
        # Create stock order transaction
        transaction_id = create_transaction(
            item_name=item_name,
            transaction_type="stock_orders",
            quantity=quantity,
            price=total_cost,
            date=request_date
        )
        
        # Get delivery date
        delivery_date = get_supplier_delivery_date(request_date, quantity)
        
        return (f"STOCK ORDER CONFIRMED\n"
                f"Transaction ID: {transaction_id}\n"
                f"Item: {item_name}\n"
                f"Quantity: {quantity} units\n"
                f"Total Cost: ${total_cost:.2f}\n"
                f"Expected Delivery: {delivery_date}")
    
    except Exception as e:
        return f"Error placing stock order: {str(e)}"

# ==================== QUOTING TOOLS ====================

@tool
def search_quote_history_tool(search_terms: str, limit: int = 5) -> str:
    """
    Search historical quotes for similar requests.
    
    Args:
        search_terms: Comma-separated search terms (e.g., "glossy,ceremony,cardstock")
        limit: Maximum number of results to return
    
    Returns:
        String with historical quote information
    """
    try:
        terms_list = [term.strip() for term in search_terms.split(",")]
        quotes = search_quote_history(terms_list, limit)
        
        if not quotes:
            return "No matching historical quotes found."
        
        result = f"FOUND {len(quotes)} SIMILAR HISTORICAL QUOTES:\n" + "="*60 + "\n"
        
        for i, quote in enumerate(quotes, 1):
            result += f"\nQuote #{i}:\n"
            result += f"  Event Type: {quote.get('event_type', 'N/A')}\n"
            result += f"  Order Size: {quote.get('order_size', 'N/A')}\n"
            result += f"  Total Amount: ${quote.get('total_amount', 0):.2f}\n"
            result += f"  Explanation: {quote.get('quote_explanation', 'N/A')[:100]}...\n"
        
        return result
    
    except Exception as e:
        return f"Error searching quote history: {str(e)}"

@tool
def calculate_quote_tool(items_and_quantities: str, request_date: str) -> str:
    """
    Calculate a quote for requested items with bulk discounts.
    
    Args:
        items_and_quantities: Format "item1:qty1,item2:qty2" (e.g., "A4 paper:500,Cardstock:200")
        request_date: Date of the quote request (YYYY-MM-DD format)
    
    Returns:
        Detailed quote with pricing breakdown and discounts
    """
    try:
        # Parse items and quantities
        items_list = []
        for item_qty in items_and_quantities.split(","):
            parts = item_qty.split(":")
            if len(parts) == 2:
                items_list.append((parts[0].strip(), int(parts[1].strip())))
        
        if not items_list:
            return "Invalid format. Use: 'item1:qty1,item2:qty2'"
        
        quote_details = []
        subtotal = 0.0
        unavailable_items = []
        
        for item_name, quantity in items_list:
            # Check if item exists in inventory
            inventory_df = pd.read_sql("SELECT * FROM inventory WHERE item_name = :item", 
                                       db_engine, params={"item": item_name})
            
            if inventory_df.empty:
                unavailable_items.append(item_name)
                continue
            
            unit_price = float(inventory_df.iloc[0]["unit_price"])
            item_total = quantity * unit_price
            subtotal += item_total
            
            quote_details.append({
                "item": item_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "item_total": item_total
            })
        
        # Apply bulk discounts
        if subtotal >= 5000:
            discount_rate = 0.15  # 15% for orders over $5000
        elif subtotal >= 2000:
            discount_rate = 0.10  # 10% for orders over $2000
        elif subtotal >= 1000:
            discount_rate = 0.05  # 5% for orders over $1000
        else:
            discount_rate = 0.0
        
        discount_amount = subtotal * discount_rate
        total = subtotal - discount_amount
        
        # Format quote
        result = "QUOTE DETAILS:\n" + "="*60 + "\n"
        
        for detail in quote_details:
            result += (f"{detail['item']}: {detail['quantity']} units × "
                      f"${detail['unit_price']:.2f} = ${detail['item_total']:.2f}\n")
        
        result += "\n" + "-"*60 + "\n"
        result += f"Subtotal: ${subtotal:.2f}\n"
        
        if discount_rate > 0:
            result += f"Bulk Discount ({discount_rate*100:.0f}%): -${discount_amount:.2f}\n"
        
        result += f"TOTAL: ${total:.2f}\n"
        
        if unavailable_items:
            result += f"\nNOTE: The following items are not available: {', '.join(unavailable_items)}\n"
        
        return result
    
    except Exception as e:
        return f"Error calculating quote: {str(e)}"

# ==================== SALES TOOLS ====================

@tool
def check_stock_availability_tool(items_and_quantities: str, request_date: str) -> str:
    """
    Check if requested items are available in sufficient quantities.
    
    Args:
        items_and_quantities: Format "item1:qty1,item2:qty2"
        request_date: Date to check availability (YYYY-MM-DD format)
    
    Returns:
        Availability status for each item
    """
    try:
        items_list = []
        for item_qty in items_and_quantities.split(","):
            parts = item_qty.split(":")
            if len(parts) == 2:
                items_list.append((parts[0].strip(), int(parts[1].strip())))
        
        result = "STOCK AVAILABILITY CHECK:\n" + "="*60 + "\n"
        all_available = True
        
        for item_name, quantity in items_list:
            stock_df = get_stock_level(item_name, request_date)
            current_stock = int(stock_df["current_stock"].iloc[0])
            
            if current_stock >= quantity:
                status = "✓ AVAILABLE"
            else:
                status = f"✗ INSUFFICIENT (only {current_stock} available)"
                all_available = False
            
            result += f"{item_name}: Requested {quantity}, {status}\n"
        
        result += "\n" + "-"*60 + "\n"
        result += "Overall Status: " + ("ORDER CAN BE FULFILLED" if all_available else "CANNOT FULFILL - INSUFFICIENT STOCK")
        
        return result
    
    except Exception as e:
        return f"Error checking availability: {str(e)}"

@tool
def create_sale_tool(items_and_quantities: str, total_price: float, request_date: str) -> str:
    """
    Finalize a sale by creating sales transactions and updating inventory.
    
    Args:
        items_and_quantities: Format "item1:qty1,item2:qty2"
        total_price: Total sale amount
        request_date: Date of the sale (YYYY-MM-DD format)
    
    Returns:
        Confirmation of the sale with transaction details
    """
    try:
        items_list = []
        for item_qty in items_and_quantities.split(","):
            parts = item_qty.split(":")
            if len(parts) == 2:
                items_list.append((parts[0].strip(), int(parts[1].strip())))
        
        # First check if all items are available
        for item_name, quantity in items_list:
            stock_df = get_stock_level(item_name, request_date)
            current_stock = int(stock_df["current_stock"].iloc[0])
            
            if current_stock < quantity:
                return (f"SALE FAILED: Insufficient stock for {item_name}. "
                       f"Requested: {quantity}, Available: {current_stock}")
        
        # Create sales transactions
        transaction_ids = []
        for item_name, quantity in items_list:
            # Get unit price
            inventory_df = pd.read_sql("SELECT * FROM inventory WHERE item_name = :item", 
                                       db_engine, params={"item": item_name})
            unit_price = float(inventory_df.iloc[0]["unit_price"])
            item_price = quantity * unit_price
            
            trans_id = create_transaction(
                item_name=item_name,
                transaction_type="sales",
                quantity=quantity,
                price=item_price,
                date=request_date
            )
            transaction_ids.append(trans_id)
        
        # Get delivery estimate
        total_quantity = sum(qty for _, qty in items_list)
        delivery_date = get_supplier_delivery_date(request_date, total_quantity)
        
        result = "SALE COMPLETED SUCCESSFULLY!\n" + "="*60 + "\n"
        result += f"Transaction IDs: {', '.join(map(str, transaction_ids))}\n"
        result += f"Total Amount: ${total_price:.2f}\n"
        result += f"Estimated Delivery: {delivery_date}\n"
        result += "\nItems Sold:\n"
        
        for item_name, quantity in items_list:
            result += f"  • {item_name}: {quantity} units\n"
        
        return result
    
    except Exception as e:
        return f"Error creating sale: {str(e)}"

@tool
def get_delivery_estimate_tool(quantity: int, request_date: str) -> str:
    """
    Get estimated delivery date based on order quantity.
    
    Args:
        quantity: Total quantity of items in the order
        request_date: Order date (YYYY-MM-DD format)
    
    Returns:
        Estimated delivery date
    """
    try:
        delivery_date = get_supplier_delivery_date(request_date, quantity)
        
        if quantity <= 10:
            timeframe = "same day"
        elif quantity <= 100:
            timeframe = "1 business day"
        elif quantity <= 1000:
            timeframe = "4 business days"
        else:
            timeframe = "7 business days"
        
        return f"Estimated Delivery: {delivery_date} ({timeframe})"
    
    except Exception as e:
        return f"Error estimating delivery: {str(e)}"
