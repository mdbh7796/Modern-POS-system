import os
from datetime import datetime

class ReceiptService:
    def __init__(self, output_dir="receipts"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_receipt(self, order, items):
        """
        Generates a text receipt for the given order.
        order: Order object
        items: List of dict {'product': ProductObj, 'qty': int}
        """
        timestamp_str = order.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"receipt_{order.id}_{timestamp_str}.txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
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
                f.write(f"{product.name:<15} x{qty}  ${line_total:.2f}\n")
            
            f.write("-" * 30 + "\n")
            f.write(f"TOTAL:              ${order.total_amount:.2f}\n")
            f.write("="*30 + "\n")
            f.write("    Thank you for visiting!    \n")
            f.write("="*30 + "\n")
            
        return filepath
