import streamlit as st
import pandas as pd
import numpy as np


restaurants = {
    "店铺名称": [
        "猪霸王", "中山路复记老友粉", "螺遇牛",
        "邕州老街南宁酸嘢", "三品王", "水街老牌糯米饭"
    ],
    "特色美食": [
        "老友粉", "老友粉", "老友粉",
        "南宁酸嘢", "螺蛳粉", "南宁糯米饭"
    ],
    "评分": [4.5, 4.7, 4.8, 4.6, 4.4, 4.9],
    "人均(元)": [18, 20, 19, 15, 17, 12],
    "经度": [108.3228, 108.3245, 108.3189, 108.3125, 108.3088, 108.3056],
    "纬度": [22.8156, 22.8178, 22.8211, 22.8235, 22.8198, 22.8256]
}
df_rest = pd.DataFrame(restaurants)


months = [f"{i}月" for i in range(1, 13)]
price_data = {
    "月份": months,
    "猪霸王": [16,20,27,30,16,18,12,15,13,18,17,20],
    "中山路复记老友粉": [18,19,20,15,17,25,25,27,20,14,12,22],
    "螺遇牛": [17,18,10,19,25,30,20,14,18,19,27,21],
    "三品王": [13,14,10,17,11,15,19,16,20,15,27,17],
    "水街老牌糯米饭": [15,17,26,17,37,17,18,28,17,16,21,19]
}
df_price = pd.DataFrame(price_data)


time_data = {
    "时段": ["11:00", "12:00", "13:00", "17:00", "18:00", "19:00", "20:00"],
    "猪霸王": [30, 50, 40, 25, 45, 55, 40],
    "中山路复记老友粉": [20, 15, 10, 35, 40, 30, 25],
    "螺遇牛":[30,25,16,45,34,78,54]
}
df_time = pd.DataFrame(time_data)



st.markdown('### <div class="section-title map-icon">📍美食店铺分布</div>', unsafe_allow_html=True)
with st.container():
    st.map(df_rest, latitude="纬度", longitude="经度", size="评分", color="#3B82F6", zoom=13)


st.markdown('### <div class="section-title rating-icon">⭐餐厅评分</div>', unsafe_allow_html=True)
with st.container():
    st.bar_chart(df_rest, x="店铺名称", y="评分", color="#3B82F6", height=400)


st.markdown('### <div class="section-title price-icon">💰不同类型餐厅价格（12个月）</div>', unsafe_allow_html=True)
with st.container():
    st.line_chart(df_price, x="月份", y=df_price.columns[1:], height=400, 
                  color=["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"])


st.markdown('### <div class="section-title time-icon">🕛用餐高峰时段</div>', unsafe_allow_html=True)
with st.container():
    st.area_chart(df_time, x="时段", y=df_time.columns[1:], height=400,
                  color=["#3B82F6", "#10B981", "#F59E0B"])
