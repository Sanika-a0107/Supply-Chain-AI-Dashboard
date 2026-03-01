import matplotlib.pyplot as plt
import pandas as pd

# 1. These are the exact numbers your AI model just generated
data = {
    'Factor': ['Days Scheduled', 'Total Sales', 'Product Category'],
    'Importance': [0.9575, 0.0282, 0.0142]
}

df = pd.DataFrame(data).sort_values(by='Importance', ascending=True)

# 2. Setup the visual style
plt.figure(figsize=(10, 6))
colors = ['#bdc3c7', '#34495e', '#1abc9c'] # Professional gray, dark blue, and teal

# 3. Create Horizontal Bar Chart
bars = plt.barh(df['Factor'], df['Importance'], color=colors)

# 4. Add the percentage labels on the bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
             f'{width*100:.2f}%', va='center', fontweight='bold')

# 5. Formatting
plt.title('Why are Shipments Late? (Root Cause Analysis)', fontsize=14, fontweight='bold')
plt.xlabel('Impact on Delay Prediction')
plt.xlim(0, 1.1) 
plt.tight_layout()

# 6. Save the chart as an image
plt.savefig('late_delivery_analysis.png', dpi=300)
print("✅ Success! Your insight chart has been saved as 'late_delivery_analysis.png'")
plt.show()