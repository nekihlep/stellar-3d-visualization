# 🌌 Stellar 3D - Interactive Star Map

A web application for interactive 3D exploration of the night sky. Designed for astronomy enthusiasts and beginners to discover stars based on their properties and constellations in an intuitive visual interface.

[Live Demo](https://stellar-3d-visualization.streamlit.app/)

[Dataset](https://www.kaggle.com/datasets/zhukovaekaterina/simplified-hygdatabase?resource=download)

## 🚀 Features

### 🔭 **Smart Star Discovery**
- **3D Interactive Visualization** - Explore stars in three dimensions with distance, brightness, and spectral type axes
- **Real-time Filtering** - Adjust distance, brightness, and spectral class parameters
- **Dual View Modes** - Switch between "Naked Eye" (bright stars) and "Telescope" (fainter stars) views

### 🎨 **Intuitive Visual Design**
- **Spectral Color Coding** - Stars colored by temperature (O→M: blue→red)
- **Interactive Tooltips** - Hover for detailed star information (name, magnitude, distance, spectrum)

### 🌐 **User Experience**
- **Mobile-Optimized** - Responsive design works on phones, tablets, and desktops
- **Bilingual Interface** - Full Russian/English language support
- **One-Click Data Export** - Download constellation lists and filtered star data

## 🛠 Tech Stack

### **Frontend & Visualization**
- **Streamlit** - Web application framework
- **Plotly** - Interactive 3D visualizations
- **Pandas/NumPy** - Data processing and manipulation


## 📦 Installation & Local Setup

**Prerequisites**
- Python 3.8+
- pip package manager

**One-Command Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/stellar-3d.git
cd stellar-3d

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

pip install -r requirements.txt

Run the application

streamlit run app.py
