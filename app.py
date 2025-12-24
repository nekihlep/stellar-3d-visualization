import data
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Stellar 3D", page_icon="🌌", layout="wide")

st.markdown("""
<style>
div.stDownloadButton > button {
    background-color: #4A90E2 !important;
    border-color: #4A90E2 !important;
    color: white !important;
    font-weight: bold;
}
div.stDownloadButton > button:hover {
    background-color: #357ABD !important;
    border-color: #357ABD !important;
}
.stButton > button {
    background-color: #4A90E2;
    border: 1px solid #4A90E2;
    color: white;
}
.stButton > button:hover {
    background-color: #4A90E2;
    border-color: #4A90E2;
}
.stSlider > div > div > div {
    background-color: #4A90E2 !important;
}

.stRadio > div > label > div:first-child {
    background-color: white;
    border: 2px solid #4A90E2 !important;
}

.stRadio > div > label[data-baseweb="radio"] > div:first-child > div {
    background-color: #4A90E2 !important;
}

.stCheckbox > div > label > div:first-child {
    background-color: white;
    border: 2px solid #4A90E2 !important;
}

.stCheckbox > div > label > div:nth-child(2) > div > div {
    background-color: #4A90E2 !important;
    border-color: #4A90E2 !important;
}
[data-testid="stSelectbox"] > div > div {
    border-color: #4A90E2 !important;
}
[data-testid="stSelectbox"]:hover > div > div {
    border-color: #357ABD !important;
}

[data-testid="stMultiSelect"] > div > div {
    border-color: #4A90E2 !important;
}
[data-testid="stMultiSelect"]:hover > div > div {
    border-color: #357ABD !important;
}

[data-baseweb="tag"] {
    background-color: #4A90E2 !important;
    color: white !important;
}

.stTabs > div > div > div > div {
    color: #4A90E2;
}
.stTabs > div > div > div[data-baseweb="tab-list"] > div[aria-selected="true"] {
    border-bottom-color: #4A90E2 !important;
}

.stForm > div > div > button {
    background-color: #4A90E2;
    border-color: #4A90E2;
}
</style>
""", unsafe_allow_html=True)
if 'language' not in st.session_state:
    st.session_state.language = "ENG"

col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    lang_choice = st.radio(
        "🌐", ["RU", "EN"],
        horizontal=True,
        label_visibility="collapsed",
        index=0 if st.session_state.language == "ENG" else 1
    )

    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()

translations = {
    "RU": {
        "title": "🌌 Звёздное небо 3D",
        "subtitle": "Интерактивное путешествие по звёздам",
        "filters": "⚙️️ ФИЛЬТРЫ",
        "view_mode": "Режим просмотра:",
        "view_options": ["Ночное небо (глаз)", "Телескоп", "Оба"],
        "distance": "Максимальное расстояние (пк):",
        "brightness": "Диапазон звёздной величины:",
        "spectral": "Спектральные классы:",
        "table_title": "📋 Таблица данных",
        "table_select": "Показать данные для:",
        "table_options": ["Невооруженный глаз", "Телескоп", "Оба набора"],
        "columns_select": "Выберите колонки:",
        "info_title": "ℹ️ Информация о фильтрах",
        "info_content": """
        **Фильтры:**
        - **Режим просмотра**: выбирайте, как смотреть на звезды
        - **Расстояние**: максимальное расстояние от Земли в парсеках
        - **Звёздная величина**: отрицательные значения = ярче звёзды
        - **Спектральные классы**: O (самые горячие) → M (самые холодные)

        **Цвета точек:**
        - Голубые (O, B) - горячие звёзды
        - Жёлтые (G) - звёзды как Солнце
        - Красные (M) - холодные звёзды
        """,
        "legend": "<b>Спектральные классы:</b><br>" +
         "<span style='color:#9bb0ff'>O</span> - самые горячие (>30,000K)<br>" +
         "<span style='color:#aabfff'>B</span> - горячие (10,000-30,000K)<br>" +
         "<span style='color:#cad7ff'>A</span> - белые (7,500-10,000K)<br>" +
         "<span style='color:#FFFACD'>F</span> - желтовато-белые (6,000-7,500K)<br>" +
         "<span style='color:yellow'>G</span> - жёлтые (Солнце! 5,200-6,000K)<br>" +
         "<span style='color:#FFA500'>K</span> - оранжевые (3,700-5,200K)<br>" +
         "<span style='color:red'>M</span> - красные (<3,700K)",
        "info_map" : "ℹ️ Как читать карту зведного неба и работать с созвездиями",
        "info_content_map" :"""
        **📌 Основные принципы:**
        
        1. **Каждая точка** — это звезда
        2. **Цвет точки** — показывает температуру звезды (спектральный класс)
        3. **Высота точки (ось Y)** — показывает видимую яркость (чем выше, тем ярче)
        4. **Положение слева/справа (ось X)** — показывает расстояние от Земли

        
        **📝 Система обозначения звёзд:**
        
        1. **Звёзды с историческими именами:**
           - Показываются своим именем
           - Пример: *Сириус*, *Вега*, *Дубхе*, *Мицар*
        
        2. **Звёзды без собственного имени:**
           - Обозначаются как: **[Код созвездия] star [Номер]**
           - Пример: *UMa star 1*, *Ori star 3*, *Leo star 5*
        
        **Что это значит:**
        
        *UMa star 1* — первая безымянная звезда в созвездии Большой Медведицы,
        
        *Ori star 3* — третья безымянная звезда в созвездии Ориона
         
        🔭 **Код созвездия показывает, в какой области неба находится звезда**
        
        🔭 Звёзды **одного созвездия** расположены близко в 3D пространстве
        """,
        "download_bt":"📥 Список всех 88 созвездий"
    },
    "EN": {
        "title": "🌌 3D Starry Sky",
        "subtitle": "Interactive journey through the stars",
        "filters": "⚙️ FILTERS",
        "view_mode": "View mode:",
        "view_options": ["Night Sky (naked eye)", "Telescope", "Both"],
        "distance": "Maximum distance (pc):",
        "brightness": "Apparent magnitude range:",
        "spectral": "Spectral classes:",
        "table_title": "📋 Data Table",
        "table_select": "Show data for:",
        "table_options": ["Naked Eye", "Telescope", "Both sets"],
        "columns_select": "Select columns:",
        "info_title": "ℹ️ Filter Information",
        "info_content": """
        **Filters:**
        - **View mode**: choose how to view the stars
        - **Distance**: maximum distance from Earth in parsecs
        - **Apparent magnitude**: negative values = brighter stars
        - **Spectral classes**: O (hottest) → M (coolest)

        **Point colors:**
        - Blue (O, B) - hot stars
        - Yellow (G) - stars like the Sun
        - Red (M) - cool stars
        """,
            "legend": "<b>Spectral classes:</b><br>" +
                 "<span style='color:#9bb0ff'>O</span> - hottest (>30,000K)<br>" +
                 "<span style='color:#aabfff'>B</span> - hot (10,000-30,000K)<br>" +
                 "<span style='color:#cad7ff'>A</span> - white (7,500-10,000K)<br>" +
                 "<span style='color:#FFFACD'>F</span> - yellowish-white (6,000-7,500K)<br>" +
                 "<span style='color:yellow'>G</span> - yellow (Sun! 5,200-6,000K)<br>" +
                 "<span style='color:#FFA500'>K</span> - orange (3,700-5,200K)<br>" +
                 "<span style='color:red'>M</span> - red (<3,700K)",
                "info_map" : "ℹ️How to read a sky map and work with constellations",
                "info_content_map" :"""
                    **📌 Basic principles:**
                    
                    1. **Each point** is a star
                    2. **Point color** shows the star's temperature (spectral class)
                    3. **Point height (Y-axis)** shows apparent brightness (higher = brighter)
                    4. **Left/right position (X-axis)** shows distance from Earth
                    
                    
                    **📝 Star naming system:**
                    
                    1. **Stars with historical names:**
                       - Displayed with their proper names
                       - Example: *Sirius*, *Vega*, *Dubhe*, *Mizar*
                    
                    2. **Stars without proper names:**
                       - Denoted as: **[Constellation code] star [Number]**
                       - Example: *UMa star 1*, *Ori star 3*, *Leo star 5*
                    
                    **What this means:**
                    
                    *UMa star 1* — first unnamed star in the Ursa Major constellation,
                    
                    *Ori star 3* — third unnamed star in the Orion constellation
                    
                    🔭The constellation code shows in which area of the sky **the star is located**
                    
                    🔭 Stars of **the same constellation** are located close in 3D space
                    """,
            "download_bt":"📥 List of all 88 constellations"
    }
}

lang = translations[st.session_state.language]
with col3:
    with open("constellations.txt", "r", encoding="utf-8") as f:
        file_content = f.read()

    st.download_button(
        label= lang['download_bt'],
        data=file_content,
        file_name="constellations.txt"
    )
st.markdown(f"<h1 style='text-align: center;'>{lang['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{lang['subtitle']}</p>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.header(lang['filters'])

# 1. Выбор режима
mode = st.sidebar.radio(
    lang['view_mode'],
    options=lang['view_options'],
    index=2
)

# 2. Фильтр по расстоянию
distance_range = st.sidebar.slider(
    lang['distance'],
    min_value=10,
    max_value=300,
    value=300,
    step=10
)

# 3. Фильтр по яркости (mag)
mag_range = st.sidebar.slider(
    lang['brightness'],
    min_value=-1.5,
    max_value=7.9,
    value=(-1.5, 7.9),
    step=0.5
)

# 4. Фильтр по спектральному классу
spectral_classes = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
selected_spectral = st.sidebar.multiselect(
    lang['spectral'],
    options=spectral_classes,
    default=spectral_classes
)

spectral_colors = {
    'O': '#9bb0ff', 'B': '#aabfff', 'A': '#cad7ff', 'F': '#FFFACD', 'G': 'yellow', 'K': '#FFA500', 'M': 'red',
    'L': '#ff8c00',
    'T': '#ff4500',
    'Y': '#8b0000',
    '': '#cccccc'
}


@st.cache_data
def load_data():
    df_eye = data.df_naked_eye_final.copy()
    df_tel = data.df_telescope_final.copy()
    for df in [df_eye, df_tel]:
        df['spect_class'] = df['spect'].str[0].fillna('')
        df['color'] = df['spect_class'].map(spectral_colors)

    return df_eye, df_tel


df_eye, df_tel = load_data()


def filter_data(df, distance_max, mag_min, mag_max, selected_spectral):
    # Фильтр по расстоянию
    df_filtered = df[df['dist'] <= distance_max].copy()

    # Фильтр по яркости
    df_filtered = df_filtered[(df_filtered['mag'] >= mag_min) &
                              (df_filtered['mag'] <= mag_max)]

    # Фильтр по спектральному классу
    if selected_spectral:
        df_filtered = df_filtered[df_filtered['spect_class'].isin(selected_spectral)]

    return df_filtered

df_eye_filtered = filter_data(df_eye, distance_range, mag_range[0], mag_range[1], selected_spectral)
df_tel_filtered = filter_data(df_tel, distance_range, mag_range[0], mag_range[1], selected_spectral)

with st.expander(lang['info_title']):
    st.markdown(lang['info_content'])
with st.expander(lang['info_map']):
    st.markdown(lang['info_content_map'])

fig = go.Figure()

show_eye = mode in [lang['view_options'][0], lang['view_options'][2]]  # Первый или третий вариант
show_tel = mode in [lang['view_options'][1], lang['view_options'][2]]  # Второй или третий вариант

if show_eye and len(df_eye_filtered) > 0:
    fig.add_trace(go.Scatter3d(
        x=df_eye_filtered['x'],
        y=df_eye_filtered['y'],
        z=df_eye_filtered['z'],
        mode='markers',
        marker=dict(
            size=6,
            color=df_eye_filtered['color'],
            opacity=0.9,
            line=dict(width=0)
        ),
        text=df_eye_filtered['proper'] + '<br>' +
             'Constellation: ' + df_eye_filtered['con'] + '<br>' +
             'Spectrum: ' + df_eye_filtered['spect'] + '<br>' +
             'Mag: ' + df_eye_filtered['mag'].round(2).astype(str) + '<br>' +
             'Distance: ' + df_eye_filtered['dist'].round(1).astype(str) + ' пк',
        hoverinfo='text',
        name=''
    ))

if show_tel and len(df_tel_filtered) > 0:
    fig.add_trace(go.Scatter3d(
        x=df_tel_filtered['x'],
        y=df_tel_filtered['y'],
        z=df_tel_filtered['z'],
        mode='markers',
        marker=dict(
            size=3,
            color=df_tel_filtered['color'],
            opacity=0.6,
            line=dict(width=0)
        ),
        text=df_tel_filtered['proper'] + '<br>' +
             'Constellation: ' + df_tel_filtered['con'] + '<br>' +
             'Spectrum: ' + df_tel_filtered['spect'] + '<br>' +
             'Mag: ' + df_tel_filtered['mag'].round(2).astype(str) + '<br>' +
             'Distance: ' + df_tel_filtered['dist'].round(1).astype(str) + ' пк',
        hoverinfo='text',
        name=''
    ))
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='black',

        camera=dict(
            eye=dict(x=0, y=2, z=0),
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0)
        ),
        aspectmode='auto'
    ),

    paper_bgcolor='black',
    margin=dict(l=20, r=200,t=80,b=20),
    showlegend=False,
    height=700
)
# Легенда спектральных классов
fig.add_annotation(
    x=1.2,
    y=0.5,
    xref="paper",
    yref="paper",
    text=lang['legend'],
    showarrow=False,
    align="left",
    bordercolor="black",
    borderwidth=1,
    borderpad=8,
    bgcolor="rgba(255, 255, 255, 0.9)",
    font=dict(size=16, color='black'),
    width=230
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"### {lang['table_title']}")

table_data_option = st.selectbox(
    lang['table_select'],
    options=lang['table_options'],
    key='table_selector'
)

if table_data_option == lang['table_options'][0]:  # Первый вариант
    table_df = df_eye_filtered
elif table_data_option == lang['table_options'][1]:  # Второй вариант
    table_df = df_tel_filtered
else:
    table_df = pd.concat([df_eye_filtered, df_tel_filtered])

columns_to_show = st.multiselect(
    lang['columns_select'],
    options=['proper', 'con', 'spect', 'mag', 'absmag', 'dist', 'lum'],
    default=['proper', 'con', 'mag', 'dist'],
    key='column_selector'
)

if len(table_df) > 0 and columns_to_show:
    display_df = table_df[columns_to_show].copy()
    if 'mag' in display_df.columns:
        display_df['mag'] = display_df['mag'].round(2)
    if 'absmag' in display_df.columns:
        display_df['absmag'] = display_df['absmag'].round(2)
    if 'dist' in display_df.columns:
        display_df['dist'] = display_df['dist'].round(1)
    if 'lum' in display_df.columns:
        display_df['lum'] = display_df['lum'].round(3)

    st.dataframe(display_df, use_container_width=True)
