import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import factorial

# Función original f(x) = e^x
def f(x):
    return np.exp(x)

# Polinomio de Taylor de orden n para e^x alrededor de x0 = 0
def taylor_polynomial(x, n):
    return sum((x**k) / factorial(k) for k in range(n + 1))

# Generar datos para el gráfico
x = np.linspace(-2, 2, 100)
y = f(x)

# Crear figura con deslizador
fig = go.Figure()

# Añadir la función original e^x
fig.add_trace(
    go.Scatter(x=x, y=y, mode='lines', name='f(x) = e^x', line=dict(color='blue'))
)

# Añadir el polinomio de Taylor inicial (n=0)
y_taylor = taylor_polynomial(x, 0)
fig.add_trace(
    go.Scatter(x=x, y=y_taylor, mode='lines', name='P_0(x)', line=dict(color='red'))
)

# Configurar los pasos del deslizador
steps = []
for n in range(0, 10):
    y_taylor = taylor_polynomial(x, n)
    step = dict(
        method="update",
        args=[
            {"y": [y, y_taylor], "visible": [True, True]},
            {"title.text": f"Aproximación de Taylor de e^x con n={n}"}
        ],
        label=str(n)
    )
    steps.append(step)

# Añadir deslizador
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Grado n: "},
    pad={"t": 50},
    steps=steps
)]

# Configurar el layout
fig.update_layout(
    title="Aproximación de Taylor de e^x con n=0",
    xaxis_title="x",
    yaxis_title="y",
    sliders=sliders,
    showlegend=True,
    template="plotly_white"
)

# Mostrar la figura
# Exportar como HTML
fig.write_html("taylor_series_plot.html")
fig.show()