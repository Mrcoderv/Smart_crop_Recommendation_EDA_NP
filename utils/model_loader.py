"""
Model Loader Module
Streamlit-specific utilities for loading and caching ML models
"""

import streamlit as st
from pathlib import Path
from utils.ml_predictor import MLCropPredictor, get_crop_info, get_suitability_message, get_confidence_color
from typing import Optional
import warnings
warnings.filterwarnings('ignore')


@st.cache_resource
def load_ml_model(model_dir: str = 'models') -> Optional[MLCropPredictor]:
    """
    Load ML model with Streamlit caching
    Models are cached and reused across reruns for efficiency
    """
    try:
        predictor = MLCropPredictor(model_dir=model_dir)
        if predictor.is_model_loaded():
            return predictor
        else:
            return None
    except Exception as e:
        st.error(f"Failed to load ML model: {str(e)}")
        return None


def check_model_availability() -> bool:
    """
    Check if model files exist
    """
    model_dir = Path('models')
    model_path = model_dir / 'crop_model.pkl'
    scaler_path = model_dir / 'scaler.pkl'
    label_encoder_path = model_dir / 'label_encoder.pkl'
    
    return all([model_path.exists(), scaler_path.exists(), label_encoder_path.exists()])


def display_model_info():
    """Display model information and status"""
    st.info("📊 **ML Model Information**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Type", "Random Forest")
    
    with col2:
        st.metric("Features", "6 inputs")
    
    with col3:
        st.metric("Output Classes", "10 crops")


def display_prediction_result(prediction_result: dict, show_details: bool = True):
    """
    Display prediction results in a beautiful card format
    
    Args:
        prediction_result: Dictionary with prediction details
        show_details: Whether to show additional details
    """
    if not prediction_result.get('success'):
        st.error(f"❌ Prediction Failed: {prediction_result.get('message', 'Unknown error')}")
        return
    
    predicted_crop = prediction_result['predicted_crop']
    confidence = prediction_result['confidence']
    crop_info = get_crop_info(predicted_crop)
    suitability_msg = get_suitability_message(confidence)
    confidence_color = get_confidence_color(confidence)
    
    # Main prediction card
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {confidence_color}20 0%, {confidence_color}10 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid {confidence_color};
            margin-bottom: 20px;
        ">
            <h3 style="margin: 0 0 10px 0; color: #2c3e50;">🎯 Predicted Crop</h3>
            <h1 style="margin: 0 0 10px 0; color: {confidence_color}; font-size: 36px;">
                {crop_info.get('emoji', '🌾')} {predicted_crop}
            </h1>
            <p style="margin: 0; color: #555; font-size: 14px;">{suitability_msg}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Confidence", f"{confidence:.1f}%")
        # Progress bar
        st.progress(min(confidence / 100, 1.0))
    
    # Crop information
    if show_details and crop_info:
        st.markdown("### 📋 Crop Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.write(f"**Optimal Temperature:** {crop_info.get('optimal_temp', 'N/A')}")
            st.write(f"**Optimal Rainfall:** {crop_info.get('optimal_rainfall', 'N/A')}")
        
        with info_col2:
            st.write(f"**Best Seasons:** {', '.join(crop_info.get('seasons', []))}")
        
        if crop_info.get('description'):
            st.write(f"**Description:** {crop_info['description']}")
    
    # Top 3 recommendations
    if 'top_3_recommendations' in prediction_result and show_details:
        st.markdown("### 🏆 Top 3 Recommendations")
        
        for idx, rec in enumerate(prediction_result['top_3_recommendations'], 1):
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                st.write(f"**#{idx}**")
            
            with col2:
                st.write(f"{rec['crop']}")
                st.progress(min(rec['confidence'] / 100, 1.0))
            
            with col3:
                st.write(f"{rec['confidence']:.1f}%")


def display_feature_importance(predictor: MLCropPredictor):
    """
    Display feature importance visualization
    """
    import plotly.graph_objects as go
    
    st.markdown("### 🔍 Feature Importance")
    
    importances = predictor.get_feature_importance()
    
    if not importances:
        st.warning("Unable to load feature importance data")
        return
    
    features = list(importances.keys())
    importance_values = list(importances.values())
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=importance_values,
            y=features,
            orientation='h',
            marker=dict(
                color=importance_values,
                colorscale='Viridis',
                showscale=False
            ),
            text=[f'{v:.3f}' for v in importance_values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Feature Importance in Crop Recommendation",
        xaxis_title="Importance Score",
        yaxis_title="Features",
        height=400,
        showlegend=False,
        hovermode='closest',
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_confidence_distribution(predictor: MLCropPredictor, prediction_result: dict):
    """
    Display confidence distribution across all crops
    """
    import plotly.graph_objects as go
    
    all_probs = prediction_result.get('all_probabilities', {})
    
    if not all_probs:
        return
    
    crops = list(all_probs.keys())
    confidences = list(all_probs.values())
    
    # Sort by confidence
    sorted_data = sorted(zip(crops, confidences), key=lambda x: x[1], reverse=True)
    crops_sorted = [x[0] for x in sorted_data]
    conf_sorted = [x[1] for x in sorted_data]
    
    # Color based on predicted crop
    colors = ['#27ae60' if c == prediction_result['predicted_crop'] else '#95a5a6' for c in crops_sorted]
    
    fig = go.Figure(data=[
        go.Bar(
            x=crops_sorted,
            y=conf_sorted,
            marker=dict(color=colors),
            text=[f'{c:.1f}%' for c in conf_sorted],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Confidence: %{y:.2f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Confidence Scores for All Crops",
        xaxis_title="Crop",
        yaxis_title="Confidence (%)",
        height=400,
        showlegend=False,
        hovermode='x',
        margin=dict(l=50, r=50, t=50, b=100),
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)


def get_model_status() -> dict:
    """Get current model status"""
    available = check_model_availability()
    
    status = {
        'available': available,
        'model_path': 'models/crop_model.pkl',
        'status': '✅ Ready' if available else '❌ Not trained',
        'message': 'Model is ready for predictions' if available else 'Please train the model first using: python models/train_model.py'
    }
    
    return status
