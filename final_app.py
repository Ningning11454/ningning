# 第10章/final_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

def get_dataframe_from_excel():
    # pd.read_excel()函数用于读取Excel文件的数据
    # 'supermarket_sales.xlsx'表示Excel文件的路径及名称
    # sheet_name='销售数据'表示读取名为"销售数据"的工作表的数据
    # skiprows=1表示跳过Excel中的第1行，因为第1行是标题
    # index_col='订单号'表示将"订单号"这一列作为返回的数据框的索引
    df = pd.read_excel('supermarket_sales.xlsx',
                       sheet_name='销售数据',
                       skiprows=1,
                       index_col='订单号'
                       )
    
    # 从时间列提取小时数作为新列
    df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
    return df

def add_sidebar_func(df):
    # 创建侧边栏
    with st.sidebar:
        # 添加侧边栏标题
        st.header("请筛选数据：")
        
        # 城市筛选多选框
        city_unique = df["城市"].unique()
        city = st.multiselect(
            "请选择城市：",
            options=city_unique,
            default=city_unique
        )
        
        # 顾客类型筛选多选框
        customer_type_unique = df["顾客类型"].unique()
        customer_type = st.multiselect(
            "请选择顾客类型：",
            options=customer_type_unique,
            default=customer_type_unique
        )
        
        # 性别筛选多选框
        gender_unique = df["性别"].unique()
        gender = st.multiselect(
            "请选择性别：",
            options=gender_unique,
            default=gender_unique
        )
    
    # 根据筛选条件过滤数据
    df_selection = df.query(
        "城市 == @city & 顾客类型 == @customer_type & 性别 == @gender"
    )
    return df_selection

def product_line_chart(df):
    # 按产品类型分组计算总销售额并排序（修复：Series排序移除by参数）
    sales_by_product_line = (
        df.groupby(by=["产品类型"])["总价"].sum().sort_values()
    )
    
    # 生成横向条形图
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
    )
    return fig_product_sales

def hour_chart(df):
    # 按小时数分组计算总销售额
    sales_by_hour = (
        df.groupby(by=["小时数"])["总价"].sum()
    )
    
    # 生成纵向条形图
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>",
    )
    return fig_hour_sales

def main_page_demo(df):
    """主界面函数"""
    # 设置标题
    st.title(':bar_chart: 销售仪表板')
    # 创建3列容器用于展示关键指标
    left_key_col, middle_key_col, right_key_col = st.columns(3)
    
    # 计算关键指标
    total_sales = int(df["总价"].sum())  # 总销售额（取整）
    average_rating = round(df["评分"].mean(), 1)  # 顾客评分平均值（保留1位小数）
    star_rating_string = ":star:" * int(round(average_rating, 0))  # 评分星级
    average_sale_by_transaction = round(df["总价"].mean(), 2)  # 每单平均销售额（保留2位小数）
    
    # 左侧列：总销售额
    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ¥ {total_sales:,}")
    
    # 中间列：顾客评分平均值
    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating_string}")
    
    # 右侧列：每单平均销售额
    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")
    
    # 水平分割线
    st.divider()
    
    # 创建2列容器用于展示图表
    left_chart_col, right_chart_col = st.columns(2)
    
    # 左侧图表列：按小时数的纵向条形图
    with left_chart_col:
        hour_fig = hour_chart(df)
        st.plotly_chart(hour_fig, use_container_width=True)
    
    # 右侧图表列：按产品类型的横向条形图
    with right_chart_col:
        product_fig = product_line_chart(df)
        st.plotly_chart(product_fig, use_container_width=True)

def run_app():
    """启动应用"""
    # 页面配置：标题、图标、宽布局
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide"
    )
    
    # 读取Excel数据
    sale_df = get_dataframe_from_excel()
    # 生成筛选后的数据
    df_selection = add_sidebar_func(sale_df)
    # 渲染主界面
    main_page_demo(df_selection)

# 程序入口
if __name__ == "__main__":
    run_app()
