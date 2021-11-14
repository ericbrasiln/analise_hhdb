# import pandas and plotly modules
import pandas as pd
import plotly.express as px
# import module for dealing with your OS
import os

# input CSV path
csv_path = input("Enter CSV path: ")
# input name of output file
output_file = input("Enter output file name: ")
# upper case the output file name
output_file = output_file.upper()

# Create dataframe using pandas `pd.read_csv(<path to csv>)`
df = pd.read_csv(f'{csv_path}', sep=',', index_col=0)

# use regex to find the pattern of date and remove it
df['Acervo'] = df['Acervo'].str.replace('- \d{4} a \d{4}', '', regex=True)
df['Acervo'] = df['Acervo'].str.replace('- \d{4}', '', regex=True)
# find rows in column 'Ano' that contains the string '-' and delete them
#df = df[df['Ano'].str.contains('-') == False]
# find NA in 'Ano' and delete them
df = df[df['Ano'].isna() == False]
df['Ano'] = df['Ano'].astype('int64')
# iterate over 'Acervo' column and if the value is longer than 40 characters,
# replace the last 50 characters with '...'
for index, row in df.iterrows():
    if len(row['Acervo']) > 40:
        df.at[index, 'Acervo'] = row['Acervo'][:40] + '...'
# df_ano_acervo = df filtered by 'Ano' and 'Acervo'
df_ano_acervo = df.filter(items=['Ano', 'Acervo'])\
    .groupby(['Ano', 'Acervo'])\
    .size()
# use reset_index() to reset the index 
df_ano_acervo = df_ano_acervo.reset_index(name='quant_oco_ano').sort_values(by=['Ano'])
# use query() to filter the dataframe by 'Ano'
df_ano_acervo = df_ano_acervo[(df_ano_acervo['Ano'] >= 1900)] #& (df_ano_acervo['Ano'] <= 1919)]

# df_acervos = df grouped by 'Acervo'
df_acervos = df.groupby('Acervo').size().reset_index(name='Total de Ocorrências').sort_values(by=['Total de Ocorrências'], ascending=False)
df_acervos = df_acervos.head(20)

# df_ano_page = df filtered by 'Ano' and 'Página'
df_ano_pg = df.filter(items=['Ano', 'Página'])\
    .groupby(['Ano', 'Página'])\
    .size()
df_ano_pg = df_ano_pg.reset_index(name='quant_oco_ano').sort_values(by=['Ano'])
df_ano_pg_filter = df_ano_pg.query('Página <=20')
df_ano_pg_filter = df_ano_pg_filter.query('Ano >=1900')

# df_years = df filtered by 'Ano' and count number of occurrences
df_filter = df[(df['Ano'] >= 1900) & (df['Ano'] <= 2000)]
df_years = df_filter['Ano'].value_counts()
df_years = df_years.reset_index().rename(columns={'index': 'Ano', 'Ano': 'Quantidade'}).sort_values(by=['Ano'])

###############################################################################
# Graph 1: Difusão de Ocorrências por Página
###############################################################################
# scatter plot with plotly express using the count of the number of times the 'Acervo' was repeated
fig = px.scatter(df_ano_pg_filter, x= 'Ano' , y='Página', color='quant_oco_ano', height=1000, width=1200,
                 hover_data=[df_ano_pg_filter['Ano'], df_ano_pg_filter['Página'], df_ano_pg_filter['quant_oco_ano']],
                 title=f"{output_file} - Ano X Página",
                 size='quant_oco_ano',
                 )
# config the layout
fig.update_layout(
    autosize=True,
    hovermode="closest",
    legend=dict(orientation="v"),
    showlegend=False,
    xaxis=dict(title="Difusão das ocorrências nas páginas ao longo do tempo"),
    yaxis=dict(title="Páginas"),
    title_font_size=20,
    title_pad=dict(l=300, r=0, t=0, b=0),
)
# update xaxes
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
fig.show()
#save the figure as a html file
fig.write_html(f'{output_file}_scatter_pages.html')
fig.write_image(f'{output_file}_scatter_pages.png')

###############################################################################
# Graph 2: Gráfico de Barras de Ocorrências em cada Acervo
###############################################################################
# create a bar chart with the df_acervos dataframe
fig = px.bar(df_acervos, x='Acervo', y='Total de Ocorrências', color= 'Acervo', height=800, width=1000,
                 hover_data=[df_acervos['Acervo'], df_acervos['Total de Ocorrências']],
                 title=f'{output_file} - Jornal X Total de ocorrências (20+)',
                 )
fig.update_layout(
    autosize=True,
    hovermode="closest",
    legend=dict(orientation="v"),
    showlegend=False,
    xaxis=dict(title="Acervos"),
    yaxis=dict(title="Total de Ocorrências"),
    title_font_size=16,
    title_pad=dict(l=150, r=0, t=0, b=0),
)
# show values on the bars
fig.update_traces(textposition='outside', texttemplate='%{y:.1s}')
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
fig.show()
#save the figure as a html and png file
fig.write_html(f'{output_file}_bar_acervos.html')
fig.write_image(f'{output_file}_bar_acervos.png')

###############################################################################
# Graph 3: Scatter plot de Ocorrências por Ano em cada Acervo
###############################################################################
# scatter plot with plotly express using the count of the number of times the 'Acervo' was repeated
fig = px.scatter(df_ano_acervo, x= 'Ano' , y='Acervo', color='Acervo', height=1000, width=1200,
                 hover_data=[df_ano_acervo['Ano'], df_ano_acervo['Acervo'], df_ano_acervo['quant_oco_ano']],
                 title=f"{output_file} - Ano X Acervo",
                 size='quant_oco_ano',
                 )
# config the layout
fig.update_layout(
    autosize=True,
    hovermode="closest",
    legend=dict(orientation="v"),
    showlegend=False,
    xaxis=dict(title="Anos em que há ao menos uma ocorrência"),
    yaxis=dict(title="Jornais"),
    title_font_size=20,
    title_pad=dict(l=300, r=0, t=0, b=0),
)
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
fig.show()
#save the figure as a html and png file
fig.write_html(f'{output_file}_scatter_anos.html')
fig.write_image(f'{output_file}_scatter_anos.png')

###############################################################################
# Graph 4: Gráfico de linha de Ocorrências por Ano em cada Acervo
###############################################################################
#line plot with plotly express using the count of the number of times the 'Acervo' was repeated between 1901 and 1940
fig = px.line(df_ano_acervo, x='Ano', y='quant_oco_ano', color='Acervo', height=1000, width=1200,
                 hover_data=[df_ano_acervo['Ano'], df_ano_acervo['Acervo'], df_ano_acervo['quant_oco_ano']],
                 title=f'{output_file} - Ano X Acervo',
                 markers=True,
                 )
# config the layout
fig.update_layout(
    autosize=True,
    hovermode="closest",
    legend=dict(orientation="v"),
    showlegend=True,
    xaxis=dict(title="Anos"),
    yaxis=dict(title="Total de Ocorrências"),
    title_font_size=20,
    title_pad=dict(l=300, r=0, t=0, b=0),
)
fig.show()
#save the figure as a html and png file
fig.write_html(f'{output_file}_line_anos.html')
fig.write_image(f'{output_file}_line_anos.png')

###############################################################################
# Graph 5: Gráfico de barra de Ocorrências por Ano
###############################################################################
# create a bar plot with plotly express using the count of the number of time each year was repeted as in df_years
fig = px.bar(df_years, x='Ano', y='Quantidade', color='Ano', height=1000, width=1200,
                    hover_data=[df_years['Ano'], df_years['Quantidade']],
                    title=f'{output_file} - Ano X Quantidade',
                    )
fig.update_traces(textposition='outside', texttemplate='%{y:.1s}')
# config the layout
fig.update_layout(
    autosize=True,
    hovermode="closest",
    legend=dict(orientation="v"),
    showlegend=False,
    xaxis=dict(title="Anos"),
    yaxis=dict(title="Quantidade de Ocorrências"),
    title_font_size=20,
    title_pad=dict(l=300, r=0, t=0, b=0),
)
fig.update_xaxes(
        tickangle = 60,
        title_standoff = 25,
        nticks=20, tickfont_size=10, 
        ticks="outside", tickwidth=1,
        ticklen=10,
        )
fig.update_yaxes(
        tickfont_size=10,
        ticks="outside", tickwidth=1,
        ticklen=5,
        )
fig.show()
#save the figure as a html and png file
fig.write_html(f'{output_file}_bar_anos.html')
fig.write_image(f'{output_file}_bar_anos.png')

###############################################################################

# function to get the sum of 'quant_oco_ano' in each decade
def get_sum_decade(df, ano_inicial, ano_final):
    return df.query(f'Ano >= {ano_inicial} and Ano <= {ano_final}')['quant_oco_ano'].sum()
# Creates a dictionary with beggining and end of each decade
# decades_dic = {'decade_beggining': 'decade_end'} 1850: 1859, 1860:1869, 1870:1879, 1880:1889, 1890:1899, 
decades_dic = {1900:1909, 1910:1919, 1920:1929, 1930:1939, 1940:1949, 1950:1959, 1960:1969, 1970:1979, 1980:1989, 1990:1999, 2000:2009}
# iterate over decades_dic passing in the key and value to function get_sum_decade
decades = {key: get_sum_decade(df_ano_acervo, key, value) for key, value in decades_dic.items()}
# create a dataframe from decades dict
df6 = pd.DataFrame.from_dict(decades, orient='index')
df6.reset_index(inplace=True)
df6.columns = ['Década', 'quant_oco_ano']

# create a bar chart with the df6 dataframe
fig = px.bar(df6, x='Década', y='quant_oco_ano', color= 'Década', height=500, width=500,
                 hover_data=[df6['Década'], df6['quant_oco_ano']],
                 title=f'{output_file} - Década X Ocorrências',
                 )

fig.update_layout(
    autosize=True,
    hovermode="closest",
    legend=dict(orientation="v"),
    showlegend=False,
    xaxis=dict(title="Quantidade de ocorrências"),
    yaxis=dict(title="Décadas"),
    title_font_size=16,
    title_pad=dict(l=50, r=0, t=0, b=0),
)
# update xaxes
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
fig.show()
#save the figure as a html and png file
fig.write_html(f'{output_file}_decades_bar.html')
fig.write_image(f'{output_file}_decades_bar.png')
