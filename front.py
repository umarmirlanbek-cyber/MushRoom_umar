import streamlit as st
import requests

api_url = 'http://127.0.0.1:9000/predict'

st.title('Mushrooms Poison Test')

cap_shape = st.selectbox('форма колпачка', ['c', 'f', 'k', 's', 'x'])
cap_surface = st.selectbox('поверхность крышки', ['g', 's', 'y'])
cap_color = st.selectbox('Цвет колпачка',['c', 'e', 'g', 'n', 'p', 'r', 'u', 'w', 'y'])
bruises = st.selectbox('синяки', ['t', 'f'])
odor = st.selectbox('Запах', ['c', 'f', 'l', 'm', 'n', 'p', 's', 'y', 'a'])
gill_attachment = st.selectbox('жаберное прикрепление', ['f', 'a', 'd', 'n'])
gill_spacing = st.selectbox('Интервалы между жабрами', ['c', 'w'])
gill_size = st.selectbox('Размер жабер', ['b', 'n'])
gill_color = st.selectbox('Жаберный цвет',['e', 'g', 'h', 'k', 'n', 'o', 'p', 'r', 'u', 'w', 'y'])
stalk_shape = st.selectbox('форма стебля', ['e', 't'])
stalk_root = st.selectbox('Корень стебля', ['c', 'e', 'r'])
ring_type = st.selectbox('Кольцевой тип', ['f', 'l', 'n', 'p'])
spore_print_color = st.selectbox('споровый принт цветной',['h', 'k', 'n', 'o', 'r', 'u', 'w', 'y'])
population = st.selectbox('популяция', ['c', 'n', 's', 'v', 'y'])
habitat = st.selectbox('Среда обитания', ['g', 'l', 'm', 'p', 'u', 'w'])

mushroom_data = {
    'cap_shape': cap_shape,
    'cap_surface': cap_surface,
    'cap_color': cap_color,
    'bruises': bruises,
    'odor': odor,
    'gill_attachment': gill_attachment,
    'gill_spacing': gill_spacing,
    'gill_size': gill_size,
    'gill_color': gill_color,
    'stalk_shape': stalk_shape,
    'stalk_root': stalk_root,
    'ring_type': ring_type,
    'spore_print_color': spore_print_color,
    'population': population,
    'habitat': habitat
}

if st.button('tap this'):
    try:
        answer = requests.post(api_url, json=mushroom_data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(
                f"result: {result.get('poisonous')}, {result.get('probability')}")
        else:
            st.error(f'Ошибка: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error('Не удалось соединится к API')