# 🚗 Araba Fiyat Tahmin Sistemi - Streamlit Uygulaması

Bu proje, makine öğrenimi kullanarak araç fiyatlarını tahmin eden bir web uygulamasıdır.

## 📋 Özellikler

- **Gerçek zamanlı fiyat tahmini**: Araç özelliklerine göre anlık fiyat tahmini
- **İnteraktif arayüz**: Kullanıcı dostu, modern tasarım
- **Model performans metrikleri**: Detaylı model bilgileri ve karşılaştırmalar
- **Görselleştirmeler**: Plotly ile interaktif grafikler
- **Güven aralığı**: Tahmin güvenilirlik aralığı
- **Özellik önem analizi**: Fiyatı etkileyen faktörlerin görselleştirilmesi

## 🚀 Kurulum

### 1. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Model Dosyalarını Hazırlayın

Aşağıdaki dosyaların aynı dizinde olduğundan emin olun:
- `app.py` (Streamlit uygulaması)
- `car_price_prediction_model.pkl` (Eğitilmiş model)
- `model_columns.pkl` (Model kolonları)

### 3. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Uygulama otomatik olarak tarayıcınızda açılacaktır (genellikle http://localhost:8501).

## 📊 Kullanım

### Fiyat Tahmini Yapmak İçin:

1. **Model Seçimi**: Dropdown menüden aracın modelini seçin
2. **Yıl**: Slider ile üretim yılını belirleyin (1980-2026)
3. **Kilometre**: Aracın toplam kilometresini girin
4. **Vites Türü**: Manuel, Otomatik veya Yarı-Otomatik seçin
5. **Yakıt Tipi**: Benzin, Dizel, Hibrit veya Diğer seçin
6. **Motor Hacmi**: Dropdown'dan motor hacmini seçin
7. **MPG**: Yakıt tüketimini girin
8. **Vergi**: Yıllık motorlu taşıt vergisini girin
9. **"Fiyat Tahmini Yap"** butonuna tıklayın

### Sekme Yapısı:

- **📊 Fiyat Tahmini**: Ana tahmin ekranı
- **📈 Model Bilgisi**: Model performans metrikleri ve karşılaştırmalar
- **ℹ️ Kullanım Kılavuzu**: Detaylı kullanım talimatları

## 🎯 Model Detayları

- **Algoritma**: Random Forest Regressor
- **R² Skoru**: ~0.93 (Test verisi)
- **RMSE**: ~£2,500
- **Veri Seti**: 8 farklı marka, 100,000+ araç
- **Özellikler**: 30+ feature (one-hot encoded)

### Hiperparametreler:
- `n_estimators`: 500
- `max_depth`: 20
- `max_features`: 20

## 📁 Dosya Yapısı

```
.
├── app.py                              # Ana Streamlit uygulaması
├── requirements.txt                    # Python bağımlılıkları
├── car_price_prediction_model.pkl     # Eğitilmiş model
├── model_columns.pkl                   # Model kolonları
└── README.md                          # Bu dosya
```

## 🔧 Teknik Detaylar

### Feature Engineering:
- **age**: Araç yaşı (2026 - year)
- **mileage_per_year**: Yıllık ortalama kilometre
- **Log transformasyonlar**: mileage, mpg, engineSize, age, mileage_per_year

### Kategorik Değişkenler (One-Hot Encoding):
- **model**: 10 en popüler model + "Other"
- **transmission**: Manual, Automatic, Semi-Auto
- **fuelType**: Petrol, Diesel, Hybrid, Other

## 💡 Önemli Notlar

- Fiyatlar **Pound Sterling (£)** cinsindendir
- İngiltere piyasası için optimize edilmiştir
- Elektrikli araçlar veri setinde yetersiz olduğu için kapsam dışıdır
- Tahminler %93-107 güven aralığındadır

