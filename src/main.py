"""
Beaver's Choice Paper Company - Main Entry Point
Runs the multi-agent system test scenarios.
"""

import pandas as pd
import time
from utils import init_database, generate_financial_report, db_engine
from agents import process_customer_request

def run_test_scenarios():
    """Execute test scenarios using the multi-agent system."""
    print("="*80)
    print("BEAVER'S CHOICE PAPER COMPANY - MULTI-AGENT SYSTEM")
    print("="*80)
    print("\nInitializing Database...")
    init_database(db_engine)
    
    try:
        quote_requests_sample = pd.read_csv("../data/quote_requests_sample.csv")
        quote_requests_sample["request_date"] = pd.to_datetime(
            quote_requests_sample["request_date"], format="%m/%d/%y", errors="coerce"
        )
        quote_requests_sample.dropna(subset=["request_date"], inplace=True)
        quote_requests_sample = quote_requests_sample.sort_values("request_date")
    except Exception as e:
        print(f"FATAL: Error loading test data: {e}")
        return
    
    # Get initial state
    initial_date = quote_requests_sample["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)
    current_cash = report["cash_balance"]
    current_inventory = report["inventory_value"]
    
    print(f"\nInitial Financial State:")
    print(f"  Cash Balance: ${current_cash:,.2f}")
    print(f"  Inventory Value: ${current_inventory:,.2f}")
    print(f"  Total Assets: ${current_cash + current_inventory:,.2f}")
    print("\n" + "="*80)
    
    results = []
    
    for idx, row in quote_requests_sample.iterrows():
        request_date = row["request_date"].strftime("%Y-%m-%d")
        
        print(f"\n{'='*80}")
        print(f"REQUEST #{idx+1}")
        print(f"{'='*80}")
        print(f"Context: {row['job']} organizing {row['event']}")
        print(f"Order Size: {row['need_size']}")
        print(f"Request Date: {request_date}")
        print(f"Current Cash: ${current_cash:,.2f}")
        print(f"Current Inventory Value: ${current_inventory:,.2f}")
        print(f"\nCustomer Request:\n{row['request']}")
        print(f"\n{'-'*80}")
        print("Processing request through multi-agent system...")
        print(f"{'-'*80}\n")
        
        # Process request with date context
        request_with_date = f"{row['request']}\n\n[Request Date: {request_date}]"
        response = process_customer_request(request_with_date, request_date)
        
        # Update financial state
        report = generate_financial_report(request_date)
        new_cash = report["cash_balance"]
        new_inventory = report["inventory_value"]
        
        cash_change = new_cash - current_cash
        inventory_change = new_inventory - current_inventory
        
        print(f"\nAGENT RESPONSE:")
        print(f"{'-'*80}")
        print(response)
        print(f"{'-'*80}")
        
        print(f"\nFINANCIAL UPDATE:")
        print(f"  Cash Balance: ${new_cash:,.2f} (Change: ${cash_change:+,.2f})")
        print(f"  Inventory Value: ${new_inventory:,.2f} (Change: ${inventory_change:+,.2f})")
        print(f"  Total Assets: ${new_cash + new_inventory:,.2f}")
        
        current_cash = new_cash
        current_inventory = new_inventory
        
        results.append({
            "request_id": idx + 1,
            "request_date": request_date,
            "job": row['job'],
            "event": row['event'],
            "need_size": row['need_size'],
            "cash_balance": current_cash,
            "inventory_value": current_inventory,
            "response": response,
        })
        
        time.sleep(2)  # Rate limiting
    
    # Final report
    print(f"\n{'='*80}")
    print("FINAL FINANCIAL REPORT")
    print(f"{'='*80}")
    final_date = quote_requests_sample["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)
    
    print(f"Report Date: {final_date}")
    print(f"Final Cash Balance: ${final_report['cash_balance']:,.2f}")
    print(f"Final Inventory Value: ${final_report['inventory_value']:,.2f}")
    print(f"Total Assets: ${final_report['total_assets']:,.2f}")
    
    print(f"\nTop Selling Products:")
    for i, product in enumerate(final_report['top_selling_products'], 1):
        print(f"  {i}. {product['item_name']}: ${product['total_revenue']:,.2f} revenue")
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv("../results/test_results.csv", index=False)
    print(f"\nResults saved to '../results/test_results.csv'")
    print(f"{'='*80}\n")
    
    return results

if __name__ == "__main__":
    results = run_test_scenarios()
