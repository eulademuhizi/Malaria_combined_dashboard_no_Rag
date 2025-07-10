import streamlit as st
import base64
import os
from typing import Optional

class DashboardStyling:
    """Handle all dashboard styling, CSS, and visual appearance"""
    
    @staticmethod
    def setup_page_config():
        """Set up page configuration"""
        st.set_page_config(
            page_title="Rwanda Malaria Dashboard",
            page_icon="🦟",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    def apply_custom_css():
        """Apply comprehensive custom CSS for professional dark theme"""
        st.markdown("""
        <style>
            /* ===== DARK THEME BASE ===== */
            .stApp {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }
            
            .main .block-container {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            /* ===== SIDEBAR STYLING ===== */
            .css-1d391kg, .css-1lcbmhc, .css-17eq0hr {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
            }
            
            /* ===== HEADER AND TITLES ===== */
            .main-header {
                text-align: center;
                padding: 2rem 0;
                margin-bottom: 2rem;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
                color: white;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.6);
                border: 1px solid #333333;
            }
            
            .dashboard-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: #FFFFFF;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                letter-spacing: 1px;
                margin: 0;
            }
            
            .dashboard-subtitle {
                font-size: 1.1rem;
                color: #B0B0B0;
                margin-top: 0.5rem;
                font-weight: 300;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }
            
            /* ===== CARDS AND CONTAINERS ===== */
            .metric-card {
                background: linear-gradient(145deg, #2D2D2D, #3A3A3A) !important;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin-bottom: 1rem;
                border: 1px solid #404040;
                color: #FFFFFF !important;
                transition: transform 0.2s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.4);
            }
            
            /* Status indicators */
            .status-improved { border-left: 5px solid #4CAF50; }
            .status-concern { border-left: 5px solid #F44336; }
            .status-current { border-left: 5px solid #2196F3; }
            
            /* ===== FORM INPUTS ===== */
            .stSelectbox > div > div {
                background-color: #404040 !important;
                color: #FFFFFF !important;
                border: 2px solid #666666 !important;
                border-radius: 8px !important;
            }
            
            .stMultiSelect > div > div {
                background-color: #404040 !important;
                color: #FFFFFF !important;
                border: 2px solid #666666 !important;
                border-radius: 8px !important;
            }
            
            .stRadio > div {
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #444;
            }
            
            /* ===== BUTTONS ===== */
            .stButton > button {
                background: linear-gradient(145deg, #2196F3, #1976D2) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 2rem !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(145deg, #1976D2, #1565C0) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 16px rgba(33, 150, 243, 0.4) !important;
            }
            
            /* Sidebar buttons */
            .sidebar .stButton > button {
                width: 100% !important;
                text-align: left !important;
                background: linear-gradient(145deg, #404040, #4A4A4A) !important;
                border: 1px solid #666666 !important;
                margin-bottom: 0.5rem !important;
            }
            
            .sidebar .stButton > button:hover {
                background: linear-gradient(145deg, #FF6B6B, #FF5252) !important;
                border-color: #FF6B6B !important;
            }
            
            /* ===== METRICS DISPLAY ===== */
            [data-testid="metric-container"] {
                background: linear-gradient(145deg, #2D2D2D, #3A3A3A) !important;
                border: 1px solid #404040 !important;
                padding: 1rem !important;
                border-radius: 12px !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            }
            
            /* ===== TABS ===== */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2D2D2D !important;
                border-radius: 10px !important;
                padding: 0.5rem !important;
                gap: 0.5rem !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #404040 !important;
                color: #FFFFFF !important;
                border-radius: 8px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 500 !important;
                border: 1px solid #666666 !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(145deg, #2196F3, #1976D2) !important;
                color: white !important;
                border-color: #2196F3 !important;
                box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3) !important;
            }
            
            /* ===== PREDICTIONS SPECIFIC ===== */
            .prediction-card {
                background: linear-gradient(145deg, #1a237e, #283593) !important;
                border: 1px solid #3f51b5 !important;
                border-radius: 12px !important;
                padding: 1.5rem !important;
                margin-bottom: 1rem !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(26, 35, 126, 0.3) !important;
            }
            
            .risk-high {
                background: linear-gradient(145deg, #b71c1c, #d32f2f) !important;
                border-color: #f44336 !important;
            }
            
            .risk-medium {
                background: linear-gradient(145deg, #e65100, #f57c00) !important;
                border-color: #ff9800 !important;
            }
            
            .risk-low {
                background: linear-gradient(145deg, #1b5e20, #388e3c) !important;
                border-color: #4caf50 !important;
            }
            
            /* ===== TEXT AND GENERAL ===== */
            .stMarkdown, .stText, p, div, span {
                color: #FFFFFF !important;
            }
            
            /* ===== NOTIFICATIONS ===== */
            .stSuccess {
                background: linear-gradient(145deg, #e8f5e8, #c8e6c9) !important;
                border-left: 5px solid #4caf50 !important;
                color: #1b5e20 !important;
            }
            
            .stWarning {
                background: linear-gradient(145deg, #fff3e0, #ffe0b2) !important;
                border-left: 5px solid #ff9800 !important;
                color: #e65100 !important;
            }
            
            .stError {
                background: linear-gradient(145deg, #ffebee, #ffcdd2) !important;
                border-left: 5px solid #f44336 !important;
                color: #b71c1c !important;
            }
            
            .stInfo {
                background: linear-gradient(145deg, #e3f2fd, #bbdefb) !important;
                border-left: 5px solid #2196f3 !important;
                color: #0d47a1 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header_with_logo() -> str:
        """Render professional header with logo"""
        logo_base64 = DashboardStyling.get_logo_base64()
        
        if logo_base64:
            header_html = f"""
            <div class="main-header">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <img src="data:image/png;base64,{logo_base64}" 
                         alt="Health Intelligence Center" 
                         style="height: 120px; width: auto; margin-bottom: 1rem;">
                </div>
                <div class="dashboard-title">Rwanda Malaria Surveillance Dashboard</div>
                <div class="dashboard-subtitle">Advanced Analytics & Predictive Intelligence</div>
            </div>
            """
        else:
            header_html = """
            <div class="main-header">
                <div class="dashboard-title">🦟 Rwanda Malaria Surveillance Dashboard</div>
                <div class="dashboard-subtitle">Advanced Analytics & Predictive Intelligence</div>
            </div>
            """
        
        return header_html
    
    @staticmethod
    def get_logo_base64() -> str:
        """Get logo as base64 string"""
        logo_path = "assets/HIC_logo.png"
        
        try:
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_data = f.read()
                return base64.b64encode(logo_data).decode()
            else:
                return ""
        except Exception:
            return ""
    
    @staticmethod
    def create_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal") -> str:
        """Create a styled metric card"""
        delta_class = ""
        if delta:
            if delta_color == "inverse":
                delta_class = "status-concern" if delta.startswith("+") else "status-improved"
            else:
                delta_class = "status-improved" if delta.startswith("+") else "status-concern"
        else:
            delta_class = "status-current"
        
        delta_html = f'<div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>' if delta else ""
        
        return f"""
        <div class="metric-card {delta_class}">
            <div style="font-size: 0.9rem; color: #B0B0B0; font-weight: 500;">{title}</div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #FFFFFF; margin: 0.5rem 0;">{value}</div>
            {delta_html}
        </div>
        """
    
    @staticmethod
    def create_risk_badge(risk_level: str) -> str:
        """Create a risk level badge"""
        colors = {
            'High': '#d32f2f',
            'Medium': '#f57c00',
            'Low': '#388e3c'
        }
        
        color = colors.get(risk_level, '#666666')
        
        return f"""
        <span style="
            background-color: {color};
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        ">{risk_level} RISK</span>
        """
    
    @staticmethod
    def create_prediction_summary_card(district: str, predictions: list, risk_level: str, accuracy: str) -> str:
        """Create a prediction summary card"""
        risk_class = f"risk-{risk_level.lower()}"
        risk_badge = DashboardStyling.create_risk_badge(risk_level)
        
        pred_text = " → ".join([f"{int(p)}" for p in predictions])
        
        return f"""
        <div class="prediction-card {risk_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; font-size: 1.2rem;">{district}</h4>
                {risk_badge}
            </div>
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.9rem; color: #E0E0E0; margin-bottom: 0.5rem;">Next 3 Months:</div>
                <div style="font-size: 1.5rem; font-weight: 700; font-family: monospace;">{pred_text}</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #B0B0B0;">
                <span>Accuracy: {accuracy}</span>
                <span>Risk Assessment</span>
            </div>
        </div>
        """
    
    @staticmethod
    def render_navigation_tabs() -> dict:
        """Get navigation tab configuration"""
        return {
            'dashboard': {
                'label': '📊 Dashboard',
                'icon': '📊',
                'description': 'Overview & Geographic Analysis'
            },
            'trends': {
                'label': '📈 Trends',
                'icon': '📈',
                'description': 'Historical Trends & Insights'
            },
            'predictions': {
                'label': '🔮 Predictions',
                'icon': '🔮',
                'description': 'Forecasting & Moving Averages'
            },
            'assistant': {
                'label': '🤖 AI Assistant',
                'icon': '🤖',
                'description': 'Intelligent Analysis Support'
            }
        }
    
    @staticmethod
    def create_sidebar_metrics(metrics_data: dict) -> str:
        """Create sidebar summary metrics"""
        html = """
        <div style="margin-bottom: 2rem;">
            <h3 style="color: #2196F3; margin-bottom: 1rem; border-bottom: 2px solid #2196F3; padding-bottom: 0.5rem;">
                📊 Quick Summary
            </h3>
        """
        
        for key, value in metrics_data.items():
            html += f"""
            <div style="
                display: flex;
                justify-content: space-between;
                padding: 0.5rem 0;
                border-bottom: 1px solid #404040;
                color: #E0E0E0;
            ">
                <span>{key}:</span>
                <strong style="color: #2196F3;">{value}</strong>
            </div>
            """
        
        html += "</div>"
        return html