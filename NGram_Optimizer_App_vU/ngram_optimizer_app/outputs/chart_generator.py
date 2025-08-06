# Chart generator placeholder
import plotly.express as px
import os, tempfile

def generate_charts(df, break_even):
    outputs = []
    context_filters = [
        (1, 'Branded', 'chart_branded.html'),
        (1, 'Competitor', 'chart_competitor.html'),
        (1, 'Generic', 'chart_generic.html'),
        (2, None, 'chart_2gram.html'),
        (3, None, 'chart_3gram.html')
    ]

    for n, context, filename in context_filters:
        if context:
            subset = df[(df['n'] == n) & (df['n-gram Context'] == context)]
            title = f"1-Gram Bubble Chart: {context}"
        else:
            subset = df[df['n'] == n].nlargest(100, 'Spend')
            title = f"Top 100 {n}-Gram Bubble Chart"

        fig = px.scatter(
            subset,
            x='CPC', y='CE',
            size='Spend',
            color='Efficiency Zone',
            hover_name='ngram',
            title=title,
            size_max=30,
            template="plotly_white"
        )
        fig.add_shape(
            type="line",
            x0=0, x1=subset['CPC'].max(),
            y0=break_even, y1=break_even,
            line=dict(dash='dash', color='black'),
            name="Break-even CE"
        )
        filepath = os.path.join(tempfile.gettempdir(), filename)
        fig.write_html(filepath)
        outputs.append(filepath)

    return outputs
