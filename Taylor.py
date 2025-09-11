import numpy as np
import pandas as pd
import plotly.express as px
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

# Generar datos
x = np.linspace(-2*np.pi, 2*np.pi, 200)
data = []
for n in range(10):
    y_taylor = taylor_polynomial(x, n)
    for i in range(len(x)):
        data.append({"x": x[i], "y": y_taylor[i], "order": n, "function": "Taylor"})

# Crear DataFrame
df = pd.DataFrame(data)

# Añadir la función original sin(x) al DataFrame
y_sin = f(x)
sin_data = [{"x": x[i], "y": y_sin[i], "order": 0, "function": "sin(x)"} for i in range(len(x))]
df_sin = pd.DataFrame(sin_data)
df = pd.concat([df, df_sin], ignore_index=True)

# Crear figura con animación
fig = px.line(df, x="x", y="y", color="function", animation_frame="order", 
              line_group="function", hover_name="function", line_shape="spline")

# Añadir botones de play/pause
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                    label="Play",
                    method="animate"
                ),
                dict(
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
                    label="Pause",
                    method="animate"
                )
            ]),
            pad={"r": 10, "t": 87},
            showactive=False,
            x=0.11,
            xanchor="left",
            y=0,
            yanchor="top"
        )
    ],
    title="Aproximación de Taylor de sin(x)",
    xaxis_title="x",
    yaxis_title="y",
    yaxis=dict(range=[-1.5, 1.5]),
    showlegend=True
)

# Exportar como HTML
fig.write_html("taylor_series_sin_plot_px.html")

# Mostrar la figura
fig.show()