import streamlit as st
import youtube
import many_chat
import airtable
import instagram
import web_analytics


# @st.cache_data
def youtube_data():
    youtube.main()
    # st.dataframe(df)






def instagram_data():
    instagram.main()
    # if st.button("Recargar datos"):
    #     st.cache_data.clear()  # Esto limpiará el caché de datos en todas las funciones con `@st.cache_data`
    #     st.write("Datos recargados desde la fuente original.")

def many_chat_data():
    many_chat.main()

def web_analytics_data():
    web_analytics.main()

# @st.cache_data
def airtable_data():
    airtable.main()

def inicio():
    

    data = {
        "Redes sociales" : 
        [st.Page(youtube_data,title="Youtube",icon=":material/slideshow:"), st.Page(instagram_data,title="Instagram",icon=":material/photo_camera:")],
        "Many chat" : [st.Page(many_chat_data,title="Many Chat")],
        "Web Analytics" : [st.Page(web_analytics_data,title="Google Analytics")],
        "Airtable" : [st.Page(airtable_data,title="CRM Agendaciones VProject")]
        }
    pg = st.navigation(data)
    pg.run()
    
st.set_page_config(layout="wide")
def main():
    
    inicio()
    
































if __name__=="__main__":
    main()