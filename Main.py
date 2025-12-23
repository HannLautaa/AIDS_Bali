import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import math

st.set_page_config(layout='wide')

st.title('Dashboard Penyakit dan Analisis Kasus AIDS di Bali Tahun 2020-2024')

def format_number(x):
    return f'{x:,.2f}'

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")

data = pd.read_csv('data/Data-Bali.csv')
data['JumlahPenduduk'] = data['JumlahPenduduk'].apply(lambda x: math.ceil(x))
data['JumlahPenduduk'] = data['JumlahPenduduk'] * 1000
data['Insidensi'] = (data['AIDS'] / data['JumlahPenduduk']) * 100000

gdf = gpd.read_file('data/gadm41_IDN_2.json')
gdf = gdf[gdf['NAME_1'] == 'Bali'].reset_index(drop=True)

merged = gdf.merge(data, right_on='Kabupaten/Kota', left_on='NAME_2').set_index('NAME_2')
# merged_2024 = merged[merged['Tahun'] == 2024]

# with st.sidebar:
t1, _ = st.columns([1, 5])
with t1:
    tahun = st.selectbox('Pilih Tahun', options=sorted(data['Tahun'].unique()), index=4)

merged_tahun = merged[merged['Tahun'] == tahun]

tabs1, tabs2, tabs3, tabs4 = st.tabs(['Peta Persebaran', 'Temporal', 'Analisis Epidemiologis', 'Analisis Spasial'])

with tabs1:
    c1, c2 = st.columns(2)

    merged_prev = merged[merged['Tahun'] == (tahun-1)]
    merged_prevKasus = merged_prev['AIDS'].sum()
    merged_prevPenduduk = merged_prev['JumlahPenduduk'].sum()

    perubahan_kasus = ((merged_tahun['AIDS'].sum() - merged_prevKasus) / merged_prevKasus) * 100
    perubahan_penduduk = (merged_tahun['JumlahPenduduk'].sum() - merged_prevPenduduk)

    min_aids = merged['AIDS'].min()
    max_aids = merged['AIDS'].max()

    min_penduduk = merged['JumlahPenduduk'].min()
    max_penduduk = merged['JumlahPenduduk'].max()

    with c1:
        if tahun == 2020:
            st.metric(f'Total Kasus Baru AIDS Tahun {tahun}', merged_tahun['AIDS'].sum(), border=True)
        else:
            st.metric(f'Total Kasus Baru AIDS Tahun {tahun}', merged_tahun['AIDS'].sum(), border=True, delta=f'{perubahan_kasus:.2f} %',  delta_color="inverse")
    with c2:
        if tahun == 2020:
            st.metric(f'Total Penduduk {tahun}', f'{merged_tahun['JumlahPenduduk'].sum():,}', border=True)
        else:
            st.metric(f'Total Penduduk {tahun}', f'{merged_tahun['JumlahPenduduk'].sum():,}', border=True, delta=f'{perubahan_penduduk:,}')

    fig = px.choropleth(
        merged_tahun,
        geojson = merged_tahun,
        locations = merged_tahun.index,
        color = 'AIDS',
        labels={
            'AIDS': 
            'Jumlah'
        },
        color_continuous_scale='Reds',
        title=f'Peta Sebaran Kasus Baru AIDS Provinsi Bali Tahun {tahun}',
        range_color=[min_aids, max_aids]
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        # paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=30, b=0)
    )

    fig2 = px.choropleth(
        merged_tahun,
        geojson = merged_tahun,
        locations = merged_tahun.index,
        color = 'JumlahPenduduk',
        labels={
            'JumlahPenduduk': 
            'Jumlah'
        },
        color_continuous_scale='Reds',
        title=f'Peta Sebaran Jumlah Penduduk Provinsi Bali Tahun {tahun}',
        range_color=[min_penduduk, max_penduduk]
    )

    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(
        # paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor= 'rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
    )

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.plotly_chart(fig, 
                            config={
                                # 'displayModeBar': True,
                                'scrollZoom': False}
                            )
    with c2:
        with st.container(border=True):
            st.plotly_chart(fig2,
                            config={
                                # 'displayModeBar': True,
                                'scrollZoom': False}
                            )
            
with tabs2:
    jumlah = {}
    for i in data['Tahun'].unique():
        jum = data[data['Tahun'] == i]['AIDS']
        jum = jum.sum()
        jumlah[f'{i}'] = jum

    jumlah_df = pd.DataFrame({'Jumlah Kasus Baru': jumlah})

    fig_line = px.line(jumlah_df, x=jumlah_df.index, y='Jumlah Kasus Baru', markers=True, title='Tren Total Kasus Baru AIDS Provinsi Bali (2020-2024)')
    fig_line.update_layout(height=350)
    fig_line.update_xaxes(
        dtick=1,
        tickformat='d',
        title_text='Tahun'
    )

    fig_scatter = px.scatter(data, x='Tahun', y='AIDS', color='Kabupaten/Kota', title='Tren Kasus Baru AIDS Provinsi Bali (2020-2024)')
    fig_scatter.update_layout(height=350)
    fig_scatter.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(
            size=8, 
            opacity=0.7, 
            line=dict(width=1, color='black')
        )
    )
    fig_scatter.update_xaxes(
        dtick=1,
        tickformat='d'   # pastikan tanpa desimal
    )
    with st.container(border=True):
        st.plotly_chart(fig_line)
    with st.container(border=True):
        st.plotly_chart(fig_scatter)

with tabs3:
    with st.container(border=True):
        c1, _, c2, _ = st.columns([2, 0.1, 1, 0.1])

    with c1:
        st.markdown('### Insidensi')
        st.markdown(
            """
            <div style="text-align: justify; padding-bottom:1rem;">
            Insidensi rate (incidence rate) adalah ukuran epidemiologi yang menunjukkan jumlah kasus baru suatu penyakit atau kejadian tertentu 
            dalam suatu populasi pada periode waktu tertentu, dibandingkan dengan jumlah penduduk yang berisiko mengalami kejadian tersebut pada waktu yang sama. 
            Digunakan untuk menggambarkan seberapa cepat penyakit atau kejadian baru muncul dalam populasi, biasanya dinyatakan per 1.000 atau per 100.000 penduduk per tahun.

            </div>
            """,
            unsafe_allow_html=True
            )
    with c2:
        with st.container(border=False, vertical_alignment='center', height='stretch'):
            with st.container(border=True):
                st.markdown('### Rumus')
                st.markdown(r'$\text {Incidence Rate} = \frac{\text{Jumlah kasus baru}}{\text{Total populasi}} \times 100.000$')

    min_ins = data['Insidensi'].min()
    max_ins = data['Insidensi'].max()

    fig3 = px.choropleth(
        merged_tahun,
        geojson = merged_tahun,
        locations = merged_tahun.index,
        color = 'Insidensi',
        color_continuous_scale='Reds',
        title=f'Peta Insidensi Kasus AIDS Provinsi Bali Tahun {tahun} per 100.000 Penduduk',
        range_color=[min_ins, max_ins]
    )

    fig3.update_geos(fitbounds="locations", visible=False)
    fig3.update_layout(
        # paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor= 'rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
    )

    fig_scatter2 = px.scatter(data, x='Tahun', y='Insidensi', color='Kabupaten/Kota', title='Tren Insidensi Kasus AIDS Provinsi Bali (2020-2024)')
    fig_scatter2.update_layout(height=350)
    fig_scatter2.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(
            size=8, 
            opacity=0.7, 
            line=dict(width=1, color='black')
        )
    )
    fig_scatter2.update_xaxes(
        dtick=1,
        tickformat='d'   # pastikan tanpa desimal
    )

    with st.container(border=True):
        st.plotly_chart(fig3)
        with st.expander('Interpretasi'):
            st.write('Misal akan dilihat insidensi kasus baru AIDS di Denpasar pada tahun 2024. Maka interpretasinya adalah,')
            st.write(r'**Pada tahun 2024 di Denpasar, terdapat sekitar 42 kasus baru AIDS pada setiap 100.000 penduduknya.**')
    with st.container(border=True):
        st.plotly_chart(fig_scatter2)

