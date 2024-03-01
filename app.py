import pickle
import streamlit as st
import pandas as pd
import requests

def recommend(m, num_recommendations=10):
    pro_index = products[products['product_name'] == m].index[0]
    distances = similarity[pro_index]
    pro_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:num_recommendations+1]
    recommended_pro = []
    for i in pro_list:
        recommended_pro.append((products.iloc[i[0]].product_name, products.iloc[i[0]].brand_name, products.iloc[i[0]].price_usd))
    return recommended_pro

def popular_recommendations(num_recommendations=50):
    # Implement logic to retrieve popular recommendations (e.g., based on views, purchases, etc.)
    # For demonstration purposes, returning top products from the dataset
    return top_products.head(num_recommendations)

top_product_dict = pickle.load(open('top_products.pkl', 'rb')) # Assuming top_product.pkl contains your top products data
top_products = pd.DataFrame(top_product_dict)

pro_dict = pickle.load(open('pro.pkl','rb'))
products = pd.DataFrame(pro_dict)

# Set background image
st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://i.ibb.co/0X3qDY9/yellow.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title("Sephora SkinCare Recommender")

# Custom CSS for improved design
st.markdown(
    """
    <style>
        .card {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: 0.3s;
            background-color: rgba(160, 213, 216, 0.8);
            margin-bottom: 20px;
        }
        .card:hover {
            box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        }
        .card-title {
            margin-top: 0;
            margin-bottom: 10px;
            color: #333;
        }
        .card-brand {
            margin: 0;
            color: #666;
        }
        .card-price {
            margin: 0;
            color: #666;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add overlay
st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)

option = st.selectbox(
    'Search items here',
    products['product_name'].values
)

if st.button('Recommend˚☽˚｡⋆:'):
    recommendation = recommend(option, num_recommendations=8)
    for product_name, brand_name, price_usd in recommendation:
        st.markdown(
            f"""
            <div class="card">
                <h3 class="card-title">{product_name}</h3>
                <p class="card-brand">Brand: {brand_name}</p>
                <p class="card-price">Price (USD): {price_usd}</p>
            </div>
            """
            ,
            unsafe_allow_html=True
        )
# Display popular recommendations as small designed cards
popular_rec = popular_recommendations()
st.subheader(":orange[Top selling products on Sephora ]:wink:")
for index, row in popular_rec.iterrows():
    st.markdown(
        f"""
        <div class="popular-card">
            <h3>{row['product_name']}</h3>
            <p>Brand: {row['brand_name']}</p>
            <p>Price (USD): {row['price_usd']}</p>
        </div>
        """
        ,
        unsafe_allow_html=True
    )

# Clearfix to ensure proper alignment of cards
st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)

