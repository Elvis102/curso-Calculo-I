import numpy as np
import plotly.graph_objects as go

# Define the function f(x) = -x^2 + 2x (a simple parabola)
def f(x):
    return -x**2 + 2*x

# Define the derivative (slope of tangent) at x0
def derivative(x):
    return -2*x + 2

# Points and parameters
x0 = 0.5  # Point of tangency
h_values = [1.0, 0.5, 0.2, 0.1]  # Different h values for secant lines
x = np.linspace(-1, 3, 400)

# Function curve
y = f(x)

# Tangent line at x0
tangent_y = f(x0) + derivative(x0) * (x - x0)

# Create the plot
fig = go.Figure()

# Add function curve
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x) = -x² + 2x', line=dict(color='black')))

# Add tangent line
fig.add_trace(go.Scatter(x=x, y=tangent_y, mode='lines', name='Tangent at x0', line=dict(color='red')))

# Add secant lines for different h values
for h in h_values:
    x_sec = [x0, x0 + h]
    y_sec = [f(x0), f(x0 + h)]
    slope = (f(x0 + h) - f(x0)) / h
    secant_y = f(x0) + slope * (x - x0)
    fig.add_trace(go.Scatter(x=x, y=secant_y, mode='lines', name=f'Secant (h={h})', line=dict(color='blue', dash='dash')))

# Update layout
fig.update_layout(
    title='Tangent and Secant Lines Approaching the Derivative',
    xaxis_title='x',
    yaxis_title='f(x)',
    legend_title='Lines',
    showlegend=True
)

# Highlight the point of tangency
fig.add_trace(go.Scatter(x=[x0], y=[f(x0)], mode='markers', name='Point (x0, f(x0))', marker=dict(size=10, color='blue')))

fig.show()