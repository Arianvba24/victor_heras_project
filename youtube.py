import streamlit as st
import pandas as pd
import json
from requests_html import HTMLSession
import locale
import plotly.graph_objects as go
import time
from datetime import datetime

# locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  

# st.set_page_config(layout="wide")


# def change_value():
#     try:

#         # if initial_date:
#         if "value_date_calendar" not in st.session_state:
#             st.session_state["value_date_calendar"] = initial_date

#         else:
#             st.session_state["initial_date"] = initial_date

#     except:
#         pass

@st.dialog("Elija su respuesta")
def actualizar_youtube():
    st.write("¿Desea actualizar los valores de youtube?")
    col1,col2 = st.columns([1,1])

    with col1:

        if st.button("Si"):
            st.rerun()

    with col2:
        if st.button("No"):
            st.rerun()


def formatear_por_miles(valor):
    
    return f"{locale.format_string('%.0f', valor, grouping=True)}"

def main():

    with open(r"data_youtube.json") as j:
        value_json = json.load(j)


    titles = []
    likes_list = []
    views_list = []
    comment_count_list = []
    data_list = []

    for data in value_json:
        final_value = data
        if 'items' in final_value and len(final_value['items']) > 0:
            video_info = final_value['items'][0]
            title = video_info['snippet']['title']
            likes = video_info['statistics'].get('likeCount', 0)
            views = video_info['statistics'].get('viewCount', 0)
            comment_count = video_info['statistics'].get('commentCount', 0)
            date_data = video_info['snippet']["publishedAt"]
            # ------------
            titles.append(title)
            likes_list.append(likes)
            views_list.append(views)
            comment_count_list.append(comment_count)
            data_list.append(date_data)


    dataframe_values = {
        "Titulos" : titles,
        "Likes" : likes_list,
        "Visitas" : views_list,
        "Comentarios" : comment_count_list,
        "Fecha" : data_list

    }

    df = pd.DataFrame(dataframe_values)
        
    df = df[1:]

    

    df["Fecha"] = df["Fecha"].apply(lambda x: x[:10])
    df["Fecha"] = pd.to_datetime(df["Fecha"],format="%Y-%m-%d")

    st.title("Análisis de Youtube")
    df["Likes"] = df["Likes"].astype(int)
    df["Visitas"] = df["Visitas"].astype(int)
    df["Comentarios"] = df["Comentarios"].astype(int)

    df_value = df.copy()
    
    # def change_value():

    # Modificaciones--------------------------------------------------------------------------------------------
    # if "filtro" in st.session_state and st.session_state["filtro"] == True and "value_date_calendar" in st.session_state:
    #     df = df.loc[
    #         df["Fecha"] >= pd.to_datetime(st.session_state["value_date_calendar"])
    #         ]

    # if "value_date_calendar" in st.session_state and "final_value_date_calendar" not in st.session_state:
    #     df = df.loc[
    #         df["Fecha"] >= pd.to_datetime(st.session_state["value_date_calendar"])
    #         ]

    # elif "value_date_calendar" in st.session_state and "final_value_date_calendar" in st.session_state:
    #     df = df.loc[
    #         (df["Fecha"] >= pd.to_datetime(st.session_state["value_date_calendar"])) & 
    #         (df["Fecha"] <= pd.to_datetime(st.session_state["final_value_date_calendar"]))

            
    #         ]
    # -----------------------------------------------------------------------------------------------------------
    if "value_date_calendar" in st.session_state or "value_date_calendar" in st.session_state:

        if st.session_state["value_date_calendar"] and st.session_state["final_value_date_calendar"]:
            df = df.loc[
                (df["Fecha"] >= pd.to_datetime(st.session_state["value_date_calendar"])) & 
                (df["Fecha"] <= pd.to_datetime(st.session_state["final_value_date_calendar"]))


                ]

        elif st.session_state["value_date_calendar"]:
            df = df.loc[
                df["Fecha"] >= pd.to_datetime(st.session_state["value_date_calendar"])
                ]

        elif st.session_state["final_value_date_calendar"]:
            df = df.loc[
                # (df["Fecha"] >= pd.to_datetime(st.session_state["value_date_calendar"])) & 
                df["Fecha"] <= pd.to_datetime(st.session_state["final_value_date_calendar"])

                
                ]


    







    # Analysing date------------------------------------------
    cantidad = df["Titulos"].count()
    suma_likes = df["Likes"].sum()
    suma_visitas = df["Visitas"].sum()
    suma_comentarios = df["Comentarios"].sum()

    col1,col2,col3,col4,col5 = st.columns([1,1,1,1,2])

    valor_total_likes = df

    # Chart values-----------------------------
   
    visitas = df.groupby("Titulos")["Visitas"].sum().reset_index().sort_values(by="Visitas",ascending=False)
    likes = df.groupby("Titulos")["Likes"].sum().reset_index().sort_values(by="Likes",ascending=False)
    comentarios = df.groupby("Titulos")["Comentarios"].sum().reset_index().sort_values(by="Comentarios",ascending=False)
     

    st.header("Pulse aquí para actualizar youtube")
    if st.button("Actualizar youtube"):
        actualizar_youtube()



    with col1:
        st.metric(label="Total de videos",value = formatear_por_miles(cantidad))

    with col2:
        st.metric(label="Total de visualizaciones",value = formatear_por_miles(suma_visitas))

    with col3:
        st.metric(label="Total de likes",value = formatear_por_miles(suma_likes))

    with col4:
        st.metric(label="Total de comentarios",value = formatear_por_miles(suma_comentarios))

    with col5:
        initial_date = st.date_input("Fecha inicio",key="value_date_calendar",value=df["Fecha"].min())
    
        final_date = st.date_input("Fecha final",key="final_value_date_calendar",value=df["Fecha"].max())
        # filtros = st.button("Borrar filtros",key="filtro")
        # # try:

        # if filtros:
        #     try:

        #         del st.session_state["value_date_calendar"]
        #         del st.session_state["final_value_date_calendar"]


        #         # if st.session_state["filtro"] == True:

        #         #     st.success("Filtro quitado")

        #     except:
        #         pass

        # except:
        #     pass

        # elif filtros

        # print(initial_date)
        # initial_date = datetime.strftime(initial_date,"%Y-%m-%d")
        # final_value = st.date_input("Fecha inicio",format="DD/MM/YYYY",key="002")
        # final_value = datetime.strftime(final_value,"%Y-%m-%d")

        # if initial_date:
        #     if "initial_date" not in st.session_state:
        #         st.session_state["initial_date"] = initial_date

        #     else:
        #         st.session_state["initial_date"] = initial_date
        # if final_value:
            # if "final_value" not in st.session_state:
            #     st.session_state["final_value"] = [final_value]

            # else:
            #     st.session_state["final_value"] = [final_value]

   
    # st.empty()
    # st.title("")
    st.write("")
    st.write("")
    # st.empty()
    
    cola1,col2 = st.columns([3,1])
    with cola1:

        st.dataframe(df,use_container_width=True)




    tab1,tab2,tab3 = st.tabs(["Visualizaciones","Likes","Comentarios"])

    with tab1:
        
                
        fig = go.Figure(layout=go.Layout(
            width=1500,  # Ancho del gráfico
            height=1200))

        fig.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=visitas["Titulos"].values[0:20][::-1],x=visitas["Visitas"].values[0:20][::-1],name="Visualizaciones",orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),text=list(map(formatear_por_miles,visitas["Visitas"].values[0:20][::-1])),textposition="inside",textangle=0))
        fig.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de visualizaciones"},yaxis=dict(
                title_font=dict(size=20),  # Tamaño de la fuente del título del eje Y
                tickfont=dict(size=16)      # Tamaño de la fuente de las etiquetas del eje Y
            ))
        st.plotly_chart(fig)

    with tab2:
        fig2 = go.Figure(layout=go.Layout(
            width=1500,  # Ancho del gráfico
            height=1200))

        fig2.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=likes["Titulos"].values[0:20][::-1],x=likes["Likes"].values[0:20][::-1],name="Visualizaciones",orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),text=list(map(formatear_por_miles,likes["Likes"].values[0:20][::-1])),textposition="inside",textangle=0))
        fig2.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de likes"},yaxis=dict(
                title_font=dict(size=20),  # Tamaño de la fuente del título del eje Y
                tickfont=dict(size=16)      # Tamaño de la fuente de las etiquetas del eje Y
            ))
        st.plotly_chart(fig2)

    
    with tab3:
        fig3 = go.Figure(layout=go.Layout(
            width=1500,  # Ancho del gráfico
            height=1200))

        fig3.add_trace(go.Bar(hoverlabel={"font" : {"size" : 15}},y=comentarios["Titulos"].values[0:20][::-1],x=comentarios["Comentarios"].values[0:20][::-1],name="Visualizaciones",orientation="h",textfont={"size": 15},marker=dict(cornerradius=15,color="#DFD7F1"),text=list(map(formatear_por_miles,comentarios["Comentarios"].values[0:20][::-1])),textposition="inside",textangle=0))
        fig3.update_layout(title_font={"color":"black","family":"Arial","size":30},title={"text":"Número de comentarios"},yaxis=dict(
                title_font=dict(size=20),  # Tamaño de la fuente del título del eje Y
                tickfont=dict(size=16)      # Tamaño de la fuente de las etiquetas del eje Y
            ))
        st.plotly_chart(fig3)





    
