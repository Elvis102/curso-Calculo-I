import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import factorial

# Función original f(x) = sin(x)
def f(x):
    return np.sin(x)

# Polinomio de Taylor de orden n para sin(x) alrededor de x0 = 0
def taylor_polynomial(x, n):
    result = 0
    for k in range(n + 1):
        result += (-1)**k * (x**(2*k + 1)) / factorial(2*k + 1)
    return result

# Generar datos para el gráfico
x = np.linspace(-2*np.pi, 2*np.pi, 200)
y = f(x)

# Crear figura con deslizador
fig = go.Figure()

# Añadir la función original sin(x)
fig.add_trace(
    go.Scatter(x=x, y=y, mode='lines', name='f(x) = sin(x)', line=dict(color='blue'))
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
            {"title.text": f"Aproximación de Taylor de sin(x) con n={n}"}
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

# Configurar el layout con rango del eje y
fig.update_layout(
    title="Aproximación de Taylor de sin(x) con n=0",
    xaxis_title="x",
    yaxis_title="y",
    sliders=sliders,
    showlegend=True,
    template="plotly_white",
    yaxis=dict(range=[-1.5, 1.5])  # Configurar rango del eje y aquí
)

# Exportar como HTML
fig.write_html("taylor_series_sin_plot.html")

# Mostrar la figura
fig.show()