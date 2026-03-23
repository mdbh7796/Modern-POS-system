import os
from datetime import datetime

class ReceiptService:
    def __init__(self, output_dir="receipts"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_receipt(self, order, items, currency_service=None):
        """
        Generates a text receipt for the given order.
        order: Order object
        items: List of dict {'product': ProductObj, 'qty': int}
        currency_service: Optional CurrencyService instance for formatting
        """
        timestamp_str = order.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"receipt_{order.id}_{timestamp_str}.txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("="*30 + "\n")
            f.write("      COFFEE SHOP POS      \n")
            f.write("="*30 + "\n")
            f.write(f"Order ID: {order.id}\n")
            f.write(f"Date: {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 30 + "\n")
            
            for item in items:
                product = item['product']
                qty = item['qty']
                line_total = product.price * qty
                
                # Format price using currency_service if available
                if currency_service:
                    fmt_total = currency_service.format(line_total)
                else:
                    fmt_total = f"${line_total:.2f}"
                
                f.write(f"{product.name:<15} x{qty}  {fmt_total}\n")
            
            f.write("-" * 30 + "\n")
            
            if currency_service:
                fmt_order_total = currency_service.format(order.total_amount)
            else:
                fmt_order_total = f"${order.total_amount:.2f}"
                
            f.write(f"TOTAL:              {fmt_order_total}\n")
            f.write("="*30 + "\n")
            f.write("    Thank you for visiting!    \n")
            f.write("="*30 + "\n")
            
        return filepath
