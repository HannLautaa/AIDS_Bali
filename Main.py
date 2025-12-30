# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# import plotly.express as px
# import math
# from esda.moran import Moran, Moran_Local
# from libpysal.weights import Queen
# from utils.LISA import lisa_map_px, lisa_map_cluster_px
# from scipy.interpolate import Rbf
# import numpy as np
# import plotly.graph_objects as go

# st.set_page_config(layout='wide')

# st.title('Dashboard Penyakit dan Analisis Kasus AIDS di Bali Tahun 2020-2024')

# def format_number(x):
#     return f'{x:,.2f}'

# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css("assets/styles.css")
    
# def calculate_morans_i(gdf_merged, col):
#     try:
#         import numpy as np
#         np.random.seed(42)

#         gdf_merged = gdf_merged.sort_index().reset_index(drop=True)

#         w = Queen.from_dataframe(gdf_merged)
#         w.transform = 'r'

#         y = gdf_merged[col].values

#         if y.sum() == 0:
#             st.warning("⚠️ Semua nilai kasus adalah 0, Moran's I tidak dapat dihitung")
#             return None, None

#         moran = Moran(y, w, permutations=999)

#         return moran, w

#     except Exception as e:
#         st.error(f"Error calculating Moran's I: {str(e)}")
#         return None, None

# def idw_interpolation(gdf_merged):
#     try:
#         # Filter hanya data yang valid (tidak NaN dan tidak 0)
#         valid_data = gdf_merged[(gdf_merged['AIDS'].notna()) & (gdf_merged['AIDS'] > 0)]
        
#         if len(valid_data) < 3:
#             st.warning("⚠️ Data tidak cukup untuk interpolasi (minimal 3 titik dengan kasus > 0)")
#             return None, None, None
        
#         # Ambil koordinat dan nilai
#         x = valid_data['lon'].values
#         y = valid_data['lat'].values
#         z = valid_data['AIDS'].values
        
#         # Buat grid
#         xi = np.linspace(x.min(), x.max(), 100)
#         yi = np.linspace(y.min(), y.max(), 100)
#         xi, yi = np.meshgrid(xi, yi)
        
#         # RBF interpolation (mirip IDW)
#         rbf = Rbf(x, y, z, function='inverse')
#         zi = rbf(xi, yi)
        
#         return xi, yi, zi
#     except Exception as e:
#         st.error(f"Error in IDW interpolation: {str(e)}")
#         return None, None, None


# data = pd.read_csv('data/Data-Bali.csv')
# data['JumlahPenduduk'] = data['JumlahPenduduk'].apply(lambda x: math.ceil(x))
# data['JumlahPenduduk'] = data['JumlahPenduduk'] * 1000
# data['Insidensi'] = (data['AIDS'] / data['JumlahPenduduk']) * 100000

# gdf = gpd.read_file('data/gadm41_IDN_2.json')
# gdf = gdf[gdf['NAME_1'] == 'Bali'].reset_index(drop=True)

# merged = gdf.merge(data, right_on='Kabupaten/Kota', left_on='NAME_2').set_index('NAME_2')

# t1, _ = st.columns([1, 5])
# with t1:
#     tahun = st.selectbox('Pilih Tahun', options=sorted(data['Tahun'].unique()), index=4)

# merged_tahun = merged[merged['Tahun'] == tahun]

# tabs1, tabs2, tabs3, tabs4 = st.tabs(['Peta Persebaran', 'Temporal', 'Analisis Epidemiologis', 'Analisis Spasial'])

# with tabs1:
#     c1, c2 = st.columns(2)

#     merged_prev = merged[merged['Tahun'] == (tahun-1)]
#     merged_prevKasus = merged_prev['AIDS'].sum()
#     merged_prevPenduduk = merged_prev['JumlahPenduduk'].sum()

#     perubahan_kasus = ((merged_tahun['AIDS'].sum() - merged_prevKasus) / merged_prevKasus) * 100
#     perubahan_penduduk = (merged_tahun['JumlahPenduduk'].sum() - merged_prevPenduduk)

#     min_aids = merged['AIDS'].min()
#     max_aids = merged['AIDS'].max()

#     min_penduduk = merged['JumlahPenduduk'].min()
#     max_penduduk = merged['JumlahPenduduk'].max()

#     with c1:
#         if tahun == 2020:
#             st.metric(f'Total Kasus Baru AIDS Tahun {tahun}', merged_tahun['AIDS'].sum(), border=True)
#         else:
#             st.metric(f'Total Kasus Baru AIDS Tahun {tahun}', merged_tahun['AIDS'].sum(), border=True, delta=f'{perubahan_kasus:.2f} %',  delta_color="inverse")
#     with c2:
#         if tahun == 2020:
#             st.metric(f'Total Penduduk {tahun}', f'{merged_tahun['JumlahPenduduk'].sum():,}', border=True)
#         else:
#             st.metric(f'Total Penduduk {tahun}', f'{merged_tahun['JumlahPenduduk'].sum():,}', border=True, delta=f'{perubahan_penduduk:,}')

#     fig = px.choropleth(
#         merged_tahun,
#         geojson = merged_tahun,
#         locations = merged_tahun.index,
#         color = 'AIDS',
#         labels={
#             'AIDS': 
#             'Jumlah'
#         },
#         color_continuous_scale='Reds',
#         title=f'Peta Sebaran Kasus Baru AIDS Provinsi Bali Tahun {tahun}',
#         range_color=[min_aids, max_aids]
#     )

#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(
#         plot_bgcolor="white",
#         margin=dict(l=0, r=0, t=30, b=0)
#     )

#     fig2 = px.choropleth(
#         merged_tahun,
#         geojson = merged_tahun,
#         locations = merged_tahun.index,
#         color = 'JumlahPenduduk',
#         labels={
#             'JumlahPenduduk': 
#             'Jumlah'
#         },
#         color_continuous_scale='Reds',
#         title=f'Peta Sebaran Jumlah Penduduk Provinsi Bali Tahun {tahun}',
#         range_color=[min_penduduk, max_penduduk]
#     )

#     fig2.update_geos(fitbounds="locations", visible=False)
#     fig2.update_layout(
#         plot_bgcolor= 'rgba(0,0,0,0)',
#         margin=dict(l=0, r=0, t=30, b=0),
#     )

#     c1, c2 = st.columns(2)
#     with c1:
#         with st.container(border=True):
#             st.plotly_chart(fig, 
#                             config={
#                                 'scrollZoom': False}
#                             )
#     with c2:
#         with st.container(border=True):
#             st.plotly_chart(fig2,
#                             config={
#                                 'scrollZoom': False}
#                             )
            
# with tabs2:
#     jumlah = {}
#     jumlah_penduduk = {}

#     for i in data['Tahun'].unique():
#         jum_aids = data[data['Tahun'] == i]['AIDS']
#         jum_penduduk = data[data['Tahun'] == i]['JumlahPenduduk']
#         jum_aids = jum_aids.sum()
#         jum_penduduk = jum_penduduk.sum()
#         jumlah[f'{i}'] = jum_aids
#         jumlah_penduduk[f'{i}'] = jum_penduduk

#     jumlah_df = pd.DataFrame({'Jumlah Kasus Baru': jumlah})

#     jumlahPenduduk_df = pd.DataFrame({'Jumlah Penduduk': jumlah_penduduk})

#     fig_line = px.line(jumlah_df, x=jumlah_df.index, y='Jumlah Kasus Baru', markers=True, title='Tren Total Kasus Baru AIDS Provinsi Bali (2020-2024)')
#     fig_line.update_layout(height=350)
#     fig_line.update_xaxes(
#         dtick=1,
#         tickformat='d',
#         title_text='Tahun'
#     )

#     fig_scatter = px.scatter(data, x='Tahun', y='AIDS', color='Kabupaten/Kota', title='Tren Kasus Baru AIDS Provinsi Bali (2020-2024)')
#     fig_scatter.update_layout(height=350)
#     fig_scatter.update_traces(
#         mode='lines+markers',
#         line=dict(width=2),
#         marker=dict(
#             size=8, 
#             opacity=0.7, 
#             line=dict(width=1, color='black')
#         )
#     )
#     fig_scatter.update_xaxes(
#         dtick=1,
#         tickformat='d'
#     )
#     with st.container(border=True):
#         st.plotly_chart(fig_line)
#     with st.container(border=True):
#         st.plotly_chart(fig_scatter)

#     fig_line2 = px.line(jumlahPenduduk_df, x=jumlahPenduduk_df.index, y='Jumlah Penduduk', markers=True, title='Tren Total Penduduk Provinsi Bali (2020-2024)')
#     fig_line2.update_layout(height=350)
#     fig_line2.update_xaxes(
#         dtick=1,
#         tickformat='d',
#         title_text='Tahun'
#     )

#     fig_scatter2 = px.scatter(data, x='Tahun', y='JumlahPenduduk', color='Kabupaten/Kota', title='Tren Penduduk Provinsi Bali (2020-2024)')
#     fig_scatter2.update_layout(height=350)
#     fig_scatter2.update_traces(
#         mode='lines+markers',
#         line=dict(width=2),
#         marker=dict(
#             size=8, 
#             opacity=0.7, 
#             line=dict(width=1, color='black')
#         )
#     )
#     fig_scatter2.update_xaxes(
#         dtick=1,
#         tickformat='d'
#     )
#     with st.container(border=True):
#         st.plotly_chart(fig_line2)
#     with st.container(border=True):
#         st.plotly_chart(fig_scatter2)

# with tabs3:
#     with st.container(border=True):
#         c1, _, c2, _ = st.columns([2, 0.1, 1, 0.1])

#     with c1:
#         st.markdown('### Insidensi')
#         st.markdown(
#             """
#             <div style="text-align: justify; padding-bottom:1rem;">
#             Insidensi rate (incidence rate) adalah ukuran epidemiologi yang menunjukkan jumlah kasus baru suatu penyakit atau kejadian tertentu 
#             dalam suatu populasi pada periode waktu tertentu, dibandingkan dengan jumlah penduduk yang berisiko mengalami kejadian tersebut pada waktu yang sama. 
#             Digunakan untuk menggambarkan seberapa cepat penyakit atau kejadian baru muncul dalam populasi, biasanya dinyatakan per 1.000 atau per 100.000 penduduk per tahun.

#             </div>
#             """,
#             unsafe_allow_html=True
#             )
#     with c2:
#         with st.container(border=False, vertical_alignment='center', height='stretch'):
#             with st.container(border=True):
#                 st.markdown('### Rumus')
#                 st.markdown(r'$\text {Incidence Rate} = \frac{\text{Jumlah kasus baru}}{\text{Total populasi}} \times 100.000$')

#     min_ins = data['Insidensi'].min()
#     max_ins = data['Insidensi'].max()

#     fig3 = px.choropleth(
#         merged_tahun,
#         geojson = merged_tahun,
#         locations = merged_tahun.index,
#         color = 'Insidensi',
#         color_continuous_scale='Reds',
#         title=f'Peta Insidensi Kasus AIDS Provinsi Bali Tahun {tahun} per 100.000 Penduduk',
#         range_color=[min_ins, max_ins]
#     )

#     fig3.update_geos(fitbounds="locations", visible=False)
#     fig3.update_layout(
#         plot_bgcolor= 'rgba(0,0,0,0)',
#         margin=dict(l=0, r=0, t=30, b=0),
#     )

#     fig_scatter2 = px.scatter(data, x='Tahun', y='Insidensi', color='Kabupaten/Kota', title='Tren Insidensi Kasus AIDS Provinsi Bali (2020-2024)')
#     fig_scatter2.update_layout(height=350)
#     fig_scatter2.update_traces(
#         mode='lines+markers',
#         line=dict(width=2),
#         marker=dict(
#             size=8, 
#             opacity=0.7, 
#             line=dict(width=1, color='black')
#         )
#     )
#     fig_scatter2.update_xaxes(
#         dtick=1,
#         tickformat='d'
#     )

#     with st.container(border=True):
#         st.plotly_chart(fig3)
#         with st.expander('Interpretasi'):
#             st.write('Misal akan dilihat insidensi kasus baru AIDS di Denpasar pada tahun 2024. Maka interpretasinya adalah,')
#             st.write(r'**Pada tahun 2024 di Denpasar, terdapat sekitar 42 kasus baru AIDS pada setiap 100.000 penduduknya.**')
#     with st.container(border=True):
#         st.plotly_chart(fig_scatter2)


# with tabs4:
#     def show_morans(t):
#         with st.container(border=True):
#             st.subheader(f'Tahun {str(t)}')
#             mt = merged[merged['Tahun'] == t]
#             moran, w = calculate_morans_i(mt, 'AIDS')
#             if moran:
#                 c1, c2, c3 = st.columns(3)

#                 is_significant = moran.p_sim < 0.05

#                 with c1:                
#                     st.metric("Moran's I", f'{moran.I:.4f}', border=True)
#                 with c2:
#                     st.metric('P-Value', f'{moran.p_sim:.4f}', border=True)
#                 with c3:
#                     st.metric('Z-score', f'{moran.z_sim:.4f}', border=True)
                
#                 if is_significant:
#                     st.success("✅ Autokorelasi spasial signifikan")
#                 else:
#                     st.info("ℹ️ Tidak ada autokorelasi signifikan")

#     st.markdown(r"## $\cdot$ Moran's I")

#     m1, m2 = st.columns(2)
#     m3, m4 = st.columns(2)

#     with m1:
#         show_morans(2020)
#     with m2:
#         show_morans(2021)
#     with m3:
#         show_morans(2022)
#     with m4:
#         show_morans(2023)
#     show_morans(2024)

#     st.markdown(r"## $\cdot$ LISA")
#     l1, l2 = st.columns(2)
#     with l1:
#         with st.container(border=True):
#             lisa_map_px(merged_tahun, 'AIDS')
#     with l2:
#         with st.container(border=True):
#             lisa_map_cluster_px(merged_tahun, 'AIDS')
    
    
#     st.markdown(r"## $\cdot$ Interpolasi Spasial (IDW)")

#     idw_data = merged[merged['Tahun'] == 2024].copy().reset_index(drop=True)
#     idw_data = idw_data.to_crs(epsg=32749)

#     idw_data['lon'] = idw_data.geometry.centroid.x
#     idw_data['lat'] = idw_data.geometry.centroid.y

#     xi, yi, zi = idw_interpolation(idw_data)
                
#     if xi is not None:
#         fig = go.Figure(data=go.Contour(
#             x=xi[0],
#             y=yi[:, 0],
#             z=zi,
#             colorscale='YlOrRd',
#             contours=dict(
#                 coloring='heatmap',
#                 showlabels=True
#             ),
#             colorbar=dict(title="Kasus Prediksi")
#         ))
        
#         # Tambahkan titik observasi
#         fig.add_trace(go.Scatter(
#             x=idw_data['lon'],
#             y=idw_data['lat'],
#             mode='markers+text',
#             marker=dict(size=10, color='blue', symbol='circle'),
#             text=idw_data['Kabupaten/Kota'],
#             textposition="top center",
#             name='Kabupaten'
#         ))
        
#         fig.update_layout(
#             title=f'Interpolasi Spasial Kasus Baru AIDS ({tahun})',
#             xaxis_title='Longitude',
#             yaxis_title='Latitude',
#             height=600
#         )
        
#         with st.container(border=True):
#             st.plotly_chart(fig, use_container_width=True)
        
#         st.info("📍 Peta menunjukkan estimasi risiko kasus baru AIDS di area yang tidak teramati berdasarkan interpolasi dari kabupaten sekitarnya.")
            

import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
from esda.moran import Moran, Moran_Local
from libpysal.weights import Queen
from utils.LISA import lisa_map_px, lisa_map_cluster_px
from scipy.interpolate import Rbf

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    layout='wide',
    page_title='Dashboard AIDS Bali',
    page_icon='📊'
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_data
def load_data():
    """Load and preprocess the main dataset"""
    try:
        data = pd.read_csv('data/Data-Bali.csv')
        data['JumlahPenduduk'] = data['JumlahPenduduk'].apply(lambda x: math.ceil(x) * 1000)
        data['Insidensi'] = (data['AIDS'] / data['JumlahPenduduk']) * 100000
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def load_geodata():
    """Load geographic data for Bali"""
    try:
        gdf = gpd.read_file('data/gadm41_IDN_2.json')
        gdf = gdf[gdf['NAME_1'] == 'Bali'].reset_index(drop=True)
        return gdf
    except Exception as e:
        st.error(f"Error loading geodata: {str(e)}")
        return None

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def merge_data(gdf, data):
    return gdf.merge(data, right_on='Kabupaten/Kota', left_on='NAME_2').set_index('NAME_2')

def format_number(x):
    """Format numbers with thousand separators"""
    return f'{x:,.2f}'

def calculate_morans_i(gdf_merged, col):
    """Calculate Moran's I statistic for spatial autocorrelation"""
    try:
        np.random.seed(42)
        gdf_merged = gdf_merged.sort_index().reset_index(drop=True)
        
        # Create spatial weights matrix
        w = Queen.from_dataframe(gdf_merged)
        w.transform = 'r'
        
        y = gdf_merged[col].values
        
        # Check if all values are zero
        if y.sum() == 0:
            return None, None, "All case values are zero"
        
        # Calculate Moran's I with permutation test
        moran = Moran(y, w, permutations=999)
        return moran, w, None
        
    except Exception as e:
        return None, None, str(e)

def idw_interpolation(gdf_merged):
    """Perform IDW interpolation for spatial prediction"""
    try:
        # Filter valid data (not NaN and > 0)
        valid_data = gdf_merged[(gdf_merged['AIDS'].notna()) & (gdf_merged['AIDS'] > 0)]
        
        if len(valid_data) < 3:
            return None, None, None, "Insufficient data for interpolation (minimum 3 points required)"
        
        # Extract coordinates and values
        x = valid_data['lon'].values
        y = valid_data['lat'].values
        z = valid_data['AIDS'].values
        
        # Create interpolation grid
        xi = np.linspace(x.min(), x.max(), 100)
        yi = np.linspace(y.min(), y.max(), 100)
        xi, yi = np.meshgrid(xi, yi)
        
        # RBF interpolation (similar to IDW)
        rbf = Rbf(x, y, z, function='inverse')
        zi = rbf(xi, yi)
        
        return xi, yi, zi, None
        
    except Exception as e:
        return None, None, None, str(e)

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_choropleth(merged_data, column, title, color_range=None, colorscale='Reds'):
    """Create a choropleth map"""
    fig = px.choropleth(
        merged_data,
        geojson=merged_data,
        locations=merged_data.index,
        color=column,
        labels={column: 'Jumlah'},
        color_continuous_scale=colorscale,
        title=title,
        range_color=color_range
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=40, b=0),
        title_font_size=14
    )
    
    return fig

def create_line_chart(df, x, y, title, height=350):
    """Create a line chart with markers"""
    fig = px.line(df, x=x, y=y, markers=True, title=title)
    fig.update_layout(height=height)
    fig.update_xaxes(dtick=1, tickformat='d', title_text='Tahun')
    fig.update_traces(line=dict(width=3))
    return fig

def create_scatter_plot(data, x, y, color, title, height=350):
    """Create a scatter plot with lines"""
    fig = px.scatter(data, x=x, y=y, color=color, title=title)
    fig.update_layout(height=height)
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=8, opacity=0.7, line=dict(width=1, color='black'))
    )
    fig.update_xaxes(dtick=1, tickformat='d')
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load CSS
    # load_css("assets/styles.css")
    
    # Title
    st.title('📊 Dashboard Analisis Kasus AIDS di Bali (2020-2024)')
    st.markdown('---')
    
    # Load data
    with st.spinner('Loading data...'):
        data = load_data()
        gdf = load_geodata()
        
        if data is None or gdf is None:
            st.error("Failed to load data. Please check your data files.")
            return
        merged = merge_data(gdf, data)
    
    # Year selector
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        tahun = st.selectbox(
            '📅 Pilih Tahun',
            options=sorted(data['Tahun'].unique()),
            index=len(data['Tahun'].unique()) - 1
        )
    
    merged_tahun = merged[merged['Tahun'] == tahun]
    
    # Create tabs
    tabs = st.tabs([
        '🗺️ Peta Persebaran',
        '📈 Analisis Temporal',
        '🔬 Analisis Epidemiologis',
        '🌍 Analisis Spasial'
    ])
    
    # ========================================================================
    # TAB 1: SPATIAL DISTRIBUTION MAP
    # ========================================================================
    with tabs[0]:
        render_spatial_tab(merged, merged_tahun, tahun, data)
    
    # ========================================================================
    # TAB 2: TEMPORAL ANALYSIS
    # ========================================================================
    with tabs[1]:
        render_temporal_tab(data)
    
    # ========================================================================
    # TAB 3: EPIDEMIOLOGICAL ANALYSIS
    # ========================================================================
    with tabs[2]:
        render_epidemiological_tab(data, merged, merged_tahun, tahun)
    
    # ========================================================================
    # TAB 4: SPATIAL ANALYSIS
    # ========================================================================
    with tabs[3]:
        render_spatial_analysis_tab(merged, merged_tahun, tahun)

# ============================================================================
# TAB RENDERING FUNCTIONS
# ============================================================================

def render_spatial_tab(merged, merged_tahun, tahun, data):
    """Render the spatial distribution tab"""
    # Calculate metrics
    if tahun > data['Tahun'].min():
        merged_prev = merged[merged['Tahun'] == (tahun - 1)]
        merged_prevKasus = merged_prev['AIDS'].sum()
        merged_prevPenduduk = merged_prev['JumlahPenduduk'].sum()
        
        perubahan_kasus = ((merged_tahun['AIDS'].sum() - merged_prevKasus) / merged_prevKasus) * 100 if merged_prevKasus > 0 else 0
        perubahan_penduduk = merged_tahun['JumlahPenduduk'].sum() - merged_prevPenduduk
        show_delta = True
    else:
        perubahan_kasus = 0
        perubahan_penduduk = 0
        show_delta = False
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if show_delta:
            st.metric(
                f'Total Kasus Baru AIDS',
                merged_tahun['AIDS'].sum(),
                delta=f'{perubahan_kasus:.2f}%',
                delta_color="inverse"
            )
        else:
            st.metric(f'Total Kasus Baru AIDS', merged_tahun['AIDS'].sum())
    
    with col2:
        if show_delta:
            st.metric(
                f'Total Penduduk',
                f"{merged_tahun['JumlahPenduduk'].sum():,}",
                delta=f'{perubahan_penduduk:,}'
            )
        else:
            st.metric(f'Total Penduduk', f"{merged_tahun['JumlahPenduduk'].sum():,}")
    
    with col3:
        avg_incidence = (merged_tahun['AIDS'].sum() / merged_tahun['JumlahPenduduk'].sum()) * 100000
        st.metric('Insidensi Rata-rata', f'{avg_incidence:.2f}/100k')
    
    with col4:
        highest = merged_tahun.loc[merged_tahun['AIDS'].idxmax(), 'Kabupaten/Kota']
        st.metric('Kabupaten Tertinggi', highest)
    
    st.markdown('---')
    
    # Get color ranges
    min_aids = merged['AIDS'].min()
    max_aids = merged['AIDS'].max()
    min_penduduk = merged['JumlahPenduduk'].min()
    max_penduduk = merged['JumlahPenduduk'].max()
    
    # Create maps
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            fig1 = create_choropleth(
                merged_tahun,
                'AIDS',
                f'Peta Sebaran Kasus Baru AIDS Provinsi Bali Tahun {tahun}',
                color_range=[min_aids, max_aids]
            )
            st.plotly_chart(fig1, use_container_width=True, config={'scrollZoom': False})
    
    with col2:
        with st.container(border=True):
            fig2 = create_choropleth(
                merged_tahun,
                'JumlahPenduduk',
                f'Peta Sebaran Jumlah Penduduk Provinsi Bali Tahun {tahun}',
                color_range=[min_penduduk, max_penduduk]
            )
            st.plotly_chart(fig2, use_container_width=True, config={'scrollZoom': False})
    
    # Data table
    with st.expander('📋 Lihat Data Tabel'):
        display_cols = ['Kabupaten/Kota', 'AIDS', 'JumlahPenduduk', 'Insidensi']
        st.dataframe(
            merged_tahun[display_cols].sort_values('AIDS', ascending=False),
            use_container_width=True
        )

def render_temporal_tab(data):
    """Render the temporal analysis tab"""
    st.subheader('📈 Tren Kasus AIDS dari Waktu ke Waktu')
    
    # Aggregate data
    yearly_aids = data.groupby('Tahun')['AIDS'].sum().reset_index()
    yearly_pop = data.groupby('Tahun')['JumlahPenduduk'].sum().reset_index()
    
    # AIDS cases trend
    with st.container(border=True):
        fig1 = create_line_chart(
            yearly_aids,
            'Tahun',
            'AIDS',
            'Tren Total Kasus Baru AIDS Provinsi Bali (2020-2024)'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    # AIDS cases by region
    with st.container(border=True):
        fig2 = create_scatter_plot(
            data,
            'Tahun',
            'AIDS',
            'Kabupaten/Kota',
            'Tren Kasus Baru AIDS per Kabupaten/Kota (2020-2024)'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('---')
    st.subheader('👥 Tren Populasi')
    
    # Population trend
    with st.container(border=True):
        fig3 = create_line_chart(
            yearly_pop,
            'Tahun',
            'JumlahPenduduk',
            'Tren Total Penduduk Provinsi Bali (2020-2024)'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # Population by region
    with st.container(border=True):
        fig4 = create_scatter_plot(
            data,
            'Tahun',
            'JumlahPenduduk',
            'Kabupaten/Kota',
            'Tren Penduduk per Kabupaten/Kota (2020-2024)'
        )
        st.plotly_chart(fig4, use_container_width=True)

def render_epidemiological_tab(data, merged, merged_tahun, tahun):
    """Render the epidemiological analysis tab"""
    st.subheader('🔬 Analisis Insidensi')
    
    # Explanation section
    with st.container(border=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown('#### 📖 Definisi Insidensi')
            st.markdown("""
            <div style="text-align: justify;">
            Insidensi rate (incidence rate) adalah ukuran epidemiologi yang menunjukkan jumlah 
            kasus baru suatu penyakit atau kejadian tertentu dalam suatu populasi pada periode 
            waktu tertentu, dibandingkan dengan jumlah penduduk yang berisiko mengalami kejadian 
            tersebut pada waktu yang sama. Digunakan untuk menggambarkan seberapa cepat penyakit 
            atau kejadian baru muncul dalam populasi, biasanya dinyatakan per 100.000 penduduk per tahun.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('#### 📐 Rumus Perhitungan')
            st.markdown(r'$$\text{Incidence Rate} = \frac{\text{Jumlah kasus baru}}{\text{Total populasi}} \times 100{,}000$$')
    
    st.markdown('---')
    
    # Incidence map and trend
    min_ins = data['Insidensi'].min()
    max_ins = data['Insidensi'].max()
    
    with st.container(border=True):
        fig1 = create_choropleth(
            merged_tahun,
            'Insidensi',
            f'Peta Insidensi Kasus AIDS Provinsi Bali Tahun {tahun} per 100.000 Penduduk',
            color_range=[min_ins, max_ins],
            colorscale='RdYlGn_r'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.expander('💡 Interpretasi'):
            highest_inc = merged_tahun.loc[merged_tahun['Insidensi'].idxmax()]
            st.markdown(f"""
            **Contoh Interpretasi untuk {highest_inc['Kabupaten/Kota']}:**
            
            Pada tahun {tahun} di {highest_inc['Kabupaten/Kota']}, terdapat sekitar 
            **{highest_inc['Insidensi']:.2f} kasus baru AIDS** pada setiap 100.000 penduduknya.
            
            Ini berarti tingkat kejadian kasus baru AIDS di {highest_inc['Kabupaten/Kota']} 
            adalah {highest_inc['Insidensi']:.2f} per 100.000 populasi.
            """)
    
    with st.container(border=True):
        fig2 = create_scatter_plot(
            data,
            'Tahun',
            'Insidensi',
            'Kabupaten/Kota',
            'Tren Insidensi Kasus AIDS per Kabupaten/Kota (2020-2024)'
        )
        st.plotly_chart(fig2, use_container_width=True)

def render_spatial_analysis_tab(merged, merged_tahun, tahun):
    """Render the spatial analysis tab"""
    
    # Moran's I Analysis
    st.subheader("📊 Moran's I - Autokorelasi Spasial")
    st.markdown("""
    Moran's I mengukur sejauh mana kasus AIDS di suatu wilayah berkorelasi dengan wilayah tetangganya.
    Nilai berkisar dari -1 (dispersi sempurna) hingga +1 (klasterisasi sempurna).
    """)
    
    years = sorted(merged['Tahun'].unique())
    cols = st.columns(min(3, len(years)))
    
    for idx, year in enumerate(years):
        with cols[idx % 3]:
            render_morans_section(merged, year)
    
    st.markdown('---')
    
    # LISA Analysis
    st.subheader("🗺️ LISA - Local Indicators of Spatial Association")
    st.markdown("""
    LISA mengidentifikasi klaster spasial lokal dan outlier dalam distribusi kasus AIDS.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown(f'**LISA Map - {tahun}**')
            lisa_map_px(merged_tahun, 'AIDS')
    
    with col2:
        with st.container(border=True):
            st.markdown(f'**LISA Cluster Map - {tahun}**')
            lisa_map_cluster_px(merged_tahun, 'AIDS')
    
    st.markdown('---')
    
    # IDW Interpolation
    st.subheader("🌐 Interpolasi Spasial (Inverse Distance Weighting)")
    st.markdown("""
    IDW memprediksi nilai kasus AIDS di lokasi yang tidak teramati berdasarkan 
    data dari lokasi terdekat.
    """)
    
    render_idw_section(merged, tahun)

def render_morans_section(merged, year):
    """Render Moran's I analysis for a specific year"""
    with st.container(border=True):
        st.markdown(f'**Tahun {year}**')
        
        mt = merged[merged['Tahun'] == year]
        moran, w, error = calculate_morans_i(mt, 'AIDS')
        
        if error:
            st.warning(f"⚠️ {error}")
            return
        
        if moran:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Moran's I", f'{moran.I:.4f}')
                st.metric('P-Value', f'{moran.p_sim:.4f}')
            
            with col2:
                st.metric('Z-score', f'{moran.z_sim:.4f}')
                
                # Interpretation
                if moran.p_sim < 0.05:
                    if moran.I > 0:
                        st.success("✅ Klasterisasi signifikan")
                    else:
                        st.info("ℹ️ Dispersi signifikan")
                else:
                    st.info("ℹ️ Tidak ada pola spasial signifikan")

def render_idw_section(merged, tahun):
    """Render IDW interpolation section"""
    idw_data = merged[merged['Tahun'] == tahun].copy().reset_index(drop=True)
    idw_data = idw_data.to_crs(epsg=32749)
    
    idw_data['lon'] = idw_data.geometry.centroid.x
    idw_data['lat'] = idw_data.geometry.centroid.y
    
    xi, yi, zi, error = idw_interpolation(idw_data)
    
    if error:
        st.warning(f"⚠️ {error}")
        return
    
    if xi is not None:
        fig = go.Figure(data=go.Contour(
            x=xi[0],
            y=yi[:, 0],
            z=zi,
            colorscale='YlOrRd',
            contours=dict(
                coloring='heatmap',
                showlabels=True
            ),
            colorbar=dict(title="Kasus Prediksi")
        ))
        
        # Add observation points
        fig.add_trace(go.Scatter(
            x=idw_data['lon'],
            y=idw_data['lat'],
            mode='markers+text',
            marker=dict(size=10, color='blue', symbol='circle', line=dict(width=2, color='white')),
            text=idw_data['Kabupaten/Kota'],
            textposition="top center",
            textfont=dict(size=10),
            name='Kabupaten'
        ))
        
        fig.update_layout(
            title=f'Interpolasi Spasial Kasus Baru AIDS Tahun {tahun}',
            xaxis_title='Longitude (UTM)',
            yaxis_title='Latitude (UTM)',
            height=600,
            showlegend=True
        )
        
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
        
        st.info("📍 Peta menunjukkan estimasi risiko kasus baru AIDS di area yang tidak teramati berdasarkan interpolasi dari kabupaten sekitarnya menggunakan metode Inverse Distance Weighting.")

# ============================================================================
# RUN APPLICATION
# ============================================================================

main()