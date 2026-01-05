from PyQt6.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from data.database import SessionLocal
from data.models import Order
from sqlalchemy import func

class ReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)
        
        # Dark theme for plot
        self.figure.patch.set_facecolor('#1e1e1e')
        
    def refresh_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Style
        ax.set_facecolor('#2d2d2d')
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff') 
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')
        ax.tick_params(axis='x', colors='#ffffff')
        ax.tick_params(axis='y', colors='#ffffff')
        ax.yaxis.label.set_color('#ffffff')
        ax.xaxis.label.set_color('#ffffff')
        ax.title.set_color('#ffffff')

        # Data: Sales by Day (Simplified)
        # Ideally, we aggregation by Date(timestamp)
        # SQLite: strftime('%Y-%m-%d', timestamp)
        
        db = SessionLocal()
        # Group by date for the last 7 entries (demo)
        results = db.query(
            func.strftime('%Y-%m-%d', Order.timestamp).label('date'),
            func.sum(Order.total_amount).label('total')
        ).group_by('date').all()
        db.close()
        
        if not results:
            ax.text(0.5, 0.5, "No Data", color="white", ha="center")
            self.canvas.draw()
            return
            
        dates = [r.date[5:] for r in results] # MM-DD
        amounts = [r.total for r in results]
        
        bars = ax.bar(dates, amounts, color='#FF9F1C')
        ax.set_title("Recent Sales Revenue")
        ax.set_ylabel("Revenue ($)")
        
        self.canvas.draw()
