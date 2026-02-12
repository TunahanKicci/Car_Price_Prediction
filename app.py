import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Araba Fiyat Tahmin Sistemi",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <h1 style="
        text-align: center; 
        font-size: 75px; 
        font-weight: 900; 
        color: #1f77b4; 
        margin-bottom: 20px;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        line-height: 1.2;
    ">
        🚗 Araba Fiyat Tahmin Sistemi
    </h1>
""", unsafe_allow_html=True)

st.markdown("---")

# Load model and columns
@st.cache_resource
def load_model():
    try:
        model = joblib.load('car_price_prediction_model.pkl')
        model_columns = joblib.load('model_columns.pkl')
        return model, model_columns
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu: {str(e)}")
        return None, None

model, model_columns = load_model()

# Title
st.markdown('<p class="main-header">🚗 Araba Fiyat Tahmin Sistemi</p>', unsafe_allow_html=True)
st.markdown("---")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Fiyat Tahmini", "📈 Model Bilgisi", "ℹ️ Kullanım Kılavuzu"])

# TAB 1: Price Prediction
with tab1:
    st.markdown('<p class="sub-header">Araç Bilgilerini Girin</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏷️ Temel Bilgiler")
        
        # Model selection
        model_options = {
            'ford_ Focus': 'Ford Focus',
            'vw_ Golf': 'VW Golf',
            'ford_ Fiesta': 'Ford Fiesta',
            'vw_ Polo': 'VW Polo',
            'Audi_ A3': 'Audi A3',
            'bmw_ 3 Series': 'BMW 3 Series',
            'mercedes_ C Class': 'Mercedes C Class',
            'Audi_ A1': 'Audi A1',
            'Audi_ A4': 'Audi A4',
            'vw_ Tiguan': 'VW Tiguan',
            'z_Other': 'Diğer Modeller'
        }
        
        selected_model_display = st.selectbox(
            "Model",
            options=list(model_options.values()),
            help="Aracın modelini seçin"
        )
        
        # Get the key for selected model
        selected_model = [k for k, v in model_options.items() if v == selected_model_display][0]
        
        # Year
        year = st.slider(
            "Yıl",
            min_value=1980,
            max_value=2026,
            value=2020,
            help="Aracın üretim yılı"
        )
        
        # Transmission
        transmission = st.selectbox(
            "Vites Türü",
            options=['Manual', 'Automatic', 'Semi-Auto'],
            help="Aracın vites türü"
        )
        
        # Fuel Type
        fuel_type = st.selectbox(
            "Yakıt Tipi",
            options=['Petrol', 'Diesel', 'Hybrid', 'Other'],
            help="Aracın yakıt türü"
        )
    
    with col2:
        st.markdown("### ⚙️ Teknik Özellikler")
        
        # Mileage
        mileage = st.number_input(
            "Kilometre (km)",
            min_value=0,
            max_value=500000,
            value=30000,
            step=1000,
            help="Aracın toplam kilometresi"
        )
        
        # Tax
        tax = st.number_input(
            "Yıllık Vergi (£)",
            min_value=0,
            max_value=1000,
            value=150,
            step=10,
            help="Yıllık motorlu taşıt vergisi"
        )
        
        # MPG
        mpg = st.number_input(
            "Yakıt Tüketimi (MPG)",
            min_value=10.0,
            max_value=400.0,
            value=50.0,
            step=0.5,
            help="Galon başına mil (Miles Per Gallon)"
        )
        
        # Engine Size
        engine_size = st.selectbox(
            "Motor Hacmi (L)",
            options=[0.5, 1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.2, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0],
            index=5,
            help="Motor hacmi litre cinsinden"
        )
    
    with col3:
        st.markdown("### 📊 Hesaplanan Değerler")
        
        # Calculate age
        age = 2026 - year
        st.metric("Araç Yaşı", f"{age} yıl")
        
        # Calculate mileage per year
        mileage_per_year = mileage / max(age, 1)
        st.metric("Yıllık Ortalama KM", f"{mileage_per_year:,.0f} km")
        
        # Show engine size
        st.metric("Motor Hacmi", f"{engine_size} L")
        
        st.markdown("---")
        st.info("💡 Bu değerler otomatik olarak hesaplanmaktadır.")
    
    st.markdown("---")
    
    # Prediction button
    if st.button("🔮 Fiyat Tahmini Yap", type="primary"):
        if model is None:
            st.error("❌ Model yüklenemedi. Lütfen model dosyalarını kontrol edin.")
        else:
            try:
                # Create input dataframe with all required columns
                input_data = pd.DataFrame(0, index=[0], columns=model_columns)
                
                # Set numeric values (with log transformation as in training)
                input_data['year'] = year
                input_data['tax'] = tax
                
                # Apply log transformations (same as training)
                input_data['mileage'] = np.log(max(mileage, 1))
                input_data['mpg'] = np.log(max(mpg, 1))
                input_data['engineSize'] = np.log(max(engine_size, 0.1))
                input_data['age'] = np.log(max(age, 1))
                input_data['mileage_per_year'] = np.log(max(mileage_per_year, 1))
                
                # Set categorical variables (one-hot encoded)
                # Model
                if selected_model != 'z_Other':
                    model_col = f'model_{selected_model}'
                    if model_col in input_data.columns:
                        input_data[model_col] = 1
                
                # Transmission (drop_first=True, so first category is baseline)
                if transmission == 'Manual':
                    pass  # Manual is the baseline (all transmission columns = 0)
                else:
                    trans_col = f'transmission_{transmission}'
                    if trans_col in input_data.columns:
                        input_data[trans_col] = 1
                
                # Fuel Type (drop_first=True)
                if fuel_type != 'Diesel':  # Assuming Diesel is first alphabetically
                    fuel_col = f'fuelType_{fuel_type}'
                    if fuel_col in input_data.columns:
                        input_data[fuel_col] = 1
                
                # Make prediction
                prediction = model.predict(input_data)[0]
                
                # Display results
                st.markdown("---")
                st.markdown('<p class="sub-header">Tahmin Sonucu</p>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h2 style="text-align: center; color: #1f77b4;">Tahmini Fiyat</h2>
                        <h1 style="text-align: center; color: #2ca02c; font-size: 48px;">£{prediction:,.2f}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Show detailed breakdown
                st.markdown("### 📋 Tahmin Detayları")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Girilen Değerler:**")
                    details_df = pd.DataFrame({
                        'Özellik': ['Model', 'Yıl', 'Kilometre', 'Vites', 'Yakıt', 'Motor Hacmi', 'MPG', 'Vergi'],
                        'Değer': [
                            selected_model_display,
                            year,
                            f"{mileage:,} km",
                            transmission,
                            fuel_type,
                            f"{engine_size} L",
                            f"{mpg} MPG",
                            f"£{tax}"
                        ]
                    })
                    st.dataframe(details_df, hide_index=True, use_container_width=True)
                
                with col2:
                    st.markdown("**Fiyat Aralığı Tahmini:**")
                    
                    # Confidence interval (approximate)
                    rmse_val = 2564.18  # Sizin test hatanız
                    lower_bound = prediction - rmse_val
                    upper_bound = prediction + rmse_val
                    
                    # Eksiye düşmemesi için kontrol (opsiyonel ama iyi olur)
                    if lower_bound < 0: lower_bound = 0
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Indicator(
                        mode = "gauge+number+delta",
                        value = prediction,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Fiyat (£)"},
                        delta = {'reference': (lower_bound + upper_bound) / 2},
                        gauge = {
                            'axis': {'range': [None, upper_bound * 1.2]},
                            'bar': {'color': "#1f77b4"},
                            'steps': [
                                {'range': [0, lower_bound], 'color': "lightgray"},
                                {'range': [lower_bound, upper_bound], 'color': "lightblue"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': prediction
                            }
                        }
                    ))
                    
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info(f"📊 **Güven Aralığı:** £{lower_bound:,.2f} - £{upper_bound:,.2f}")
                
                # Feature importance visualization
                st.markdown("---")
                st.markdown("### 🎯 Fiyatı Etkileyen Faktörler")
                
                # --- BURADAN BAŞLAYARAK DEĞİŞTİRİN ---
                
                try:
                    # Modelden ham önem derecelerini al
                    importances = model.feature_importances_
                    feature_names = model_columns
                    
                    # Verileri bir DataFrame'de topla
                    feature_imp_df = pd.DataFrame({
                        'Feature': feature_names,
                        'Importance': importances
                    })
                    
                    # Kategorileri gruplandırmak için sözlük
                    # (One-Hot Encoding yapıldığı için parçalı sütunları birleştiriyoruz)
                    feature_groups = {
                        'model_': 'Model',
                        'transmission_': 'Vites',
                        'fuelType_': 'Yakıt Tipi',
                        'engineSize': 'Motor Hacmi',
                        'mileage': 'Kilometre',
                        'year': 'Yıl',
                        'tax': 'Vergi',
                        'mpg': 'MPG',
                        'age': 'Yaş',
                        'mileage_per_year': 'Yıllık KM'
                    }
                    
                    # Gruplandırılmış verileri saklayacak sözlük
                    grouped_importances = {}
                    
                    for index, row in feature_imp_df.iterrows():
                        feature_name = row['Feature']
                        importance_val = row['Importance']
                        
                        found_group = False
                        for prefix, group_name in feature_groups.items():
                            if prefix in feature_name:
                                grouped_importances[group_name] = grouped_importances.get(group_name, 0) + importance_val
                                found_group = True
                                break
                        
                        # Eğer hiçbir gruba uymuyorsa (örn: bilinmeyen bir sütun) olduğu gibi ekle
                        if not found_group:
                            grouped_importances[feature_name] = importance_val

                    # DataFrame'e dönüştür ve sırala
                    plot_data = pd.DataFrame({
                        'Özellik': list(grouped_importances.keys()),
                        'Etki': list(grouped_importances.values())
                    }).sort_values(by='Etki', ascending=True)

                    # Grafiği çiz
                    fig = px.bar(
                        plot_data,
                        x='Etki',
                        y='Özellik',
                        orientation='h',
                        title='Model Üzerindeki Özellik Önem Düzeyleri',
                        color='Etki',
                        color_continuous_scale='Blues'
                    )
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                     st.warning("Özellik önem düzeyleri yüklenemedi (Model özelliği desteklemiyor olabilir).")
                
                # --- DEĞİŞİKLİK SONU ---
                
            except Exception as e:
                st.error(f"❌ Tahmin yapılırken hata oluştu: {str(e)}")
                st.exception(e)

# TAB 2: Model Information
with tab2:
    st.markdown('<p class="sub-header">Model Performansı ve Bilgileri</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Model Metrikleri")
        
        metrics_df = pd.DataFrame({
            'Metrik': ['Train R² Skoru', 'Test R² Skoru', 'Train RMSE', 'Test RMSE', 'Model Tipi'],
            'Değer': ['%98.28', '%93.49', '1336.96', '2564.18', 'Random Forest Regressor']
        })
        
        st.dataframe(metrics_df, hide_index=True, use_container_width=True)
        
        st.success("✅ Model, test verisinde %93 doğruluk oranına ulaşmıştır.")
        
        st.markdown("### 🎯 Model Özellikleri")
        st.markdown("""
        - **Algoritma:** Random Forest Regressor
        - **Hiperparametreler:**
          - `n_estimators`: 500
          - `max_depth`: 20
          - `max_features`: 20
        - **Overfitting Durumu:** Kontrol altında ✅
        """)
    
    with col2:
        st.markdown("### 📈 Model Karşılaştırması")
        
        comparison_data = {
            'Model': ['Random Forest', 'Linear Regression'],
            'R² Skoru': [0.93, 0.75],
            'RMSE': [2564, 4200]
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='R² Skoru',
            x=comparison_data['Model'],
            y=comparison_data['R² Skoru'],
            marker_color='#1f77b4'
        ))
        
        fig.update_layout(
            title='Model Karşılaştırması - R² Skoru',
            yaxis_title='R² Skoru',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 Random Forest modeli, Linear Regression'a göre %21 daha iyi performans göstermiştir.")
    
    st.markdown("---")
    
    st.markdown("### 🔬 Veri Bilimi Süreci")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1️⃣ Veri Toplama**")
        st.markdown("""
        - 8 farklı marka
        - 100,000+ araç verisi
        - Birleştirme ve temizleme
        """)
    
    with col2:
        st.markdown("**2️⃣ Feature Engineering**")
        st.markdown("""
        - Araç yaşı hesaplama
        - Yıllık km hesaplama
        - Log transformasyonlar
        - One-hot encoding
        """)
    
    with col3:
        st.markdown("**3️⃣ Model Eğitimi**")
        st.markdown("""
        - GridSearchCV optimizasyon
        - Cross-validation
        - İstatistiksel testler
        - SHAP analizi
        """)

# TAB 3: User Guide
with tab3:
    st.markdown('<p class="sub-header">Kullanım Kılavuzu</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🚀 Nasıl Kullanılır?
    
    ### 1. Araç Bilgilerini Girin
    **Fiyat Tahmini** sekmesinde aşağıdaki bilgileri doldurun:
    - **Model:** Aracın markasını ve modelini seçin
    - **Yıl:** Üretim yılını girin (1980-2026 arası)
    - **Kilometre:** Toplam kilometreyi girin
    - **Vites Türü:** Manuel, Otomatik veya Yarı-Otomatik
    - **Yakıt Tipi:** Benzin, Dizel, Hibrit veya Diğer
    - **Motor Hacmi:** Motor hacmini litre cinsinden seçin
    - **MPG:** Yakıt tüketimini girin
    - **Vergi:** Yıllık motorlu taşıt vergisini girin
    
    ### 2. Tahmin Yapın
    Tüm bilgileri girdikten sonra **"Fiyat Tahmini Yap"** butonuna tıklayın.
    
    ### 3. Sonuçları İnceleyin
    - **Tahmini Fiyat:** Ana fiyat tahmini
    - **Güven Aralığı:** Fiyatın olası aralığı
    - **Etki Faktörleri:** Fiyatı etkileyen özelliklerin analizi
    
    ---
    
    ## 💡 İpuçları
    
    - **Kilometre:** Düşük kilometre daha yüksek fiyat demektir
    - **Yaş:** Yeni araçlar genellikle daha değerlidir
    - **Motor Hacmi:** Büyük motorlar genelde daha pahalıdır
    - **MPG:** Yüksek yakıt verimliliği fiyatı artırır
    - **Marka ve Model:** Premium markalar (Audi, BMW, Mercedes) daha yüksek fiyatlıdır
    
    ---
    
    ## ⚠️ Önemli Notlar
    
    - Bu sistem **İngiltere** piyasası için eğitilmiştir
    - Fiyatlar **Pound Sterling (£)** cinsindendir
    - Tahminler **%93-107** güven aralığındadır
    - Elektrikli araçlar veri setinde yeterli olmadığı için kapsam dışıdır
    - Çok eski (1980 öncesi) veya çok yeni (2026 sonrası) araçlar için tahmin doğruluğu düşebilir
    
    ---
    
    ## 📞 Destek
    
    Sorunuz veya geri bildiriminiz için lütfen iletişime geçin.
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🚗 Araba Fiyat Tahmin Sistemi v1.0</p>
        <p>Powered by Random Forest Machine Learning | Made with Streamlit ❤️</p>
    </div>
""", unsafe_allow_html=True)
