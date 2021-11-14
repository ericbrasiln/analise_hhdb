# import pandas and plotly modules
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# input path to csv file and output name
csv_path = input("Enter the path of the csv file: ")
output = input("Enter the name of the output file: ")

# read csv file
df = pd.read_csv(f'{csv_path}', sep=',')

# sort the dataframe by the column 'Frequência de ocorrências X páginas'
df_freq_cl = df.sort_values(by=['Frequência de ocorrências X páginas'], ascending=True)
# reset the index of the dataframe
df_freq_cl = df_freq_cl.reset_index(drop=True)
# add a column with sequence of numbers from 1 to the number of rows in the df_freq_cl
df_freq_cl['Frequências'] = df_freq_cl.index + 1
#print(df_freq_cl.head())

# sort the dataframe by the column 'Total de Ocorrências'
df_occur_cl = df.sort_values(by=['Total de Ocorrências'], ascending=False)
# reset the index of the dataframe
df_occur_cl = df_occur_cl.reset_index(drop=True)
# add a column with sequence of numbers from 1 to the number of rows in the df_occur_cl
df_occur_cl['Ocorrências'] = df_occur_cl.index + 1

# merge the two dataframes by the column 'Acervo' 
df_merge = pd.merge(df_occur_cl, df_freq_cl, on='Acervo')
# and drop the columns 'Total de Páginas', 'Frequência de ocorrências X páginas' and 'Total de Ocorrências'
df_merge = df_merge.drop(columns=['Total de Páginas_x', 'Frequência de ocorrências X páginas_x', 'Total de Ocorrências_x'])
df_merge = df_merge.drop(columns=['Total de Páginas_y', 'Frequência de ocorrências X páginas_y', 'Total de Ocorrências_y'])

# if value in row 'Ocorrências' is greater than value in row 'Frequência'
# add the difference to new column 'Variação'
df_merge['Variação'] = df_merge['Ocorrências'] - df_merge['Frequências']
# df_merge = only the first 10 rows
df_merge = df_merge.head(10)

###############################################################################
# Graph 1: Frequency of occurrences per page
###############################################################################
# plot the dataframe
fig = px.bar(df_freq_cl, x='Frequência de ocorrências X páginas', y='Acervo', orientation='h',
                color='Acervo', hover_data=['Acervo','Total de Páginas','Total de Ocorrências'], height=800)
fig.update_layout(title_text=f'{output}')
fig.update_xaxes(title_text='Frequência de ocorrências X páginas')
fig.update_yaxes(title_text='Nome do acervo')
fig.update_xaxes(
        tickangle = 60,
        title_standoff = 25,
        nticks=20, tickfont_size=10,
        ticks="outside", tickwidth=1,
        ticklen=5,
        )
fig.update_yaxes(
        tickfont_size=10,
        ticks="outside", tickwidth=1,
        ticklen=5,
        )
# remove legend
fig.update_layout(showlegend=False)
fig.show()
# save the figure as html and png
fig.write_html(f'{output}_freq.html')
fig.write_image(f'{output}_freq.png')

###############################################################################
# Graph 2: Total of occurrences per page
###############################################################################
# plot the dataframe
fig = px.bar(df_occur_cl, x='Total de Ocorrências', y='Acervo', orientation='h',
                color='Acervo', hover_data=['Acervo','Total de Páginas','Frequência de ocorrências X páginas'], height=800)
fig.update_layout(title_text=f'{output}')
fig.update_xaxes(title_text='Total de Ocorrências')
fig.update_yaxes(title_text='Nome do acervo')
fig.update_xaxes(
        tickangle = 60,
        title_standoff = 25,
        nticks=20, tickfont_size=10,
        ticks="outside", tickwidth=1,
        ticklen=5,
        )
fig.update_yaxes(
        tickfont_size=10,
        ticks="outside", tickwidth=1,
        ticklen=5,
        )
# remove legend
fig.update_layout(showlegend=False)
fig.show()
# save the figure as html and png
fig.write_html(f'{output}_occur.html')
fig.write_image(f'{output}_occur.png')

###############################################################################
# Graph 3: Difference between frequency and occurrences
###############################################################################
# create a table using plotly go
fig = go.Figure(data=[go.Table(
    header=dict(values=['Acervo', 'Ocorrências', 'Frequências', 'Variação']),
    cells=dict(values=[df_merge['Acervo'], df_merge['Ocorrências'], df_merge['Frequências'], df_merge['Variação']],
                fill_color='#F5F8FF',
                align='center',
                font=dict(
                    size=12,
                    # if value in row 'Variação' is greater than 0 then color the cell red
                    # if value in row 'Variação' is less than 0 then color the cell green
                    color = ['darkslategray','darkslategray','darkslategray',['green' if i > 0 else 'red' for i in df_merge['Variação']]]
                    )
                )
    )
])
fig.update_layout(
    width=800,
    height=1200,
)
# update the layout of the table 
fig.update_layout(
    title_text=f'Classificação de Acervos - {output}',
    title_x=0.5,
    title_font_size=20,
    title_font_family='Arial',
    title_xanchor='center',
    title_yanchor='top',
    title_xref='paper',
    title_yref='paper',)
fig.show()
# save the figure as html and png
fig.write_html(f'{output}_table.html')
fig.write_image(f'{output}_table.png')
