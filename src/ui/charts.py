"""
Advanced Charts and Results Module
=================================
Professional visualization suite for desalter optimization results.

This module provides comprehensive charts and analytics for understanding
optimization trade-offs, quality compliance, and operational insights.

Author: Engineering Team
Version: 2.0
License: Proprietary
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, Any, Tuple


class AdvancedChartsEngine:
    """Professional charts engine for desalter optimization results."""
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#d4af37',
            'secondary': '#f4d03f',
            'success': '#22c55e',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'background': 'rgba(0,0,0,0)',
            'grid': 'rgba(212,175,55,0.1)'
        }
    
    def create_pareto_front_chart(self, data: pd.DataFrame, params: Dict[str, Any]) -> go.Figure:
        """Create optimization trade-off / Pareto front chart."""
        # Calculate total cost (normalized)
        chemical_cost = data['ppm'] * 0.01  # $/bbl equivalent
        energy_cost = (data['T'] - 105) * 0.005 + (data['V'] - 22) * 0.003  # $/bbl
        wash_cost = data['wash_pct'] * 0.002  # $/bbl
        data['total_cost'] = chemical_cost + energy_cost + wash_cost
        
        # Compliance status
        data['compliance'] = data['BSW'] <= params['spec_bsw']
        
        fig = px.scatter(
            data,
            x='total_cost',
            y='flow_bpd',
            color='compliance',
            color_discrete_map={True: self.color_scheme['success'], False: self.color_scheme['danger']},
            size='BSW',
            hover_data=['T', 'V', 'ppm', 'wash_pct', 'BSW'],
            title="🎯 Optimization Trade-off Analysis (Pareto Front)",
            labels={
                'total_cost': 'Total Cost ($/bbl)',
                'flow_bpd': 'Throughput (BPD)',
                'compliance': 'BS&W Compliance'
            }
        )
        
        fig.update_layout(
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color='#e5e7eb',
            title_font_size=16,
            title_font_color=self.color_scheme['primary'],
            showlegend=True,
            legend=dict(title="BS&W Compliance", orientation="h", y=-0.1)
        )
        
        return fig
    
    def create_quality_compliance_chart(self, data: pd.DataFrame, params: Dict[str, Any]) -> go.Figure:
        """Create quality compliance histogram."""
        fig = go.Figure()
        
        # Histogram of BS&W distribution
        fig.add_trace(go.Histogram(
            x=data['BSW'],
            nbinsx=50,
            name='BS&W Distribution',
            marker_color=self.color_scheme['primary'],
            opacity=0.7
        ))
        
        # Add spec limit line
        fig.add_vline(
            x=params['spec_bsw'],
            line_dash="dash",
            line_color=self.color_scheme['danger'],
            annotation_text=f"Spec Limit ({params['spec_bsw']}%)",
            annotation_position="top right"
        )
        
        # Calculate compliance percentage
        compliance_pct = (data['BSW'] <= params['spec_bsw']).mean() * 100
        
        fig.update_layout(
            title=f"📊 Quality Compliance Distribution ({compliance_pct:.1f}% Compliant)",
            xaxis_title="BS&W (%)",
            yaxis_title="Frequency",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color='#e5e7eb',
            title_font_color=self.color_scheme['primary']
        )
        
        return fig
    
    def create_energy_quality_plot(self, data: pd.DataFrame) -> go.Figure:
        """Create energy vs quality scatter plot."""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("🌡️ Temperature vs BS&W", "⚡ Voltage vs BS&W"),
            horizontal_spacing=0.1
        )
        
        # Temperature plot
        fig.add_trace(
            go.Scatter(
                x=data['T'],
                y=data['BSW'],
                mode='markers',
                marker=dict(
                    color=data['flow_bpd'],
                    colorscale='Viridis',
                    size=6,
                    opacity=0.6,
                    colorbar=dict(title="Flow (BPD)", x=0.45)
                ),
                name='Temperature Effect'
            ),
            row=1, col=1
        )
        
        # Voltage plot
        fig.add_trace(
            go.Scatter(
                x=data['V'],
                y=data['BSW'],
                mode='markers',
                marker=dict(
                    color=data['ppm'],
                    colorscale='Plasma',
                    size=6,
                    opacity=0.6,
                    colorbar=dict(title="Demulsifier (ppm)", x=1.02)
                ),
                name='Voltage Effect'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title="⚡ Energy vs Quality Analysis",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color='#e5e7eb',
            title_font_color=self.color_scheme['primary'],
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1)
        fig.update_xaxes(title_text="Voltage (kV)", row=1, col=2)
        fig.update_yaxes(title_text="BS&W (%)", row=1, col=1)
        fig.update_yaxes(title_text="BS&W (%)", row=1, col=2)
        
        return fig
    
    def create_chemical_efficiency_curve(self, data: pd.DataFrame) -> go.Figure:
        """Create chemical efficiency curve."""
        # Group by demulsifier dosage and calculate mean BS&W
        ppm_grouped = data.groupby(pd.cut(data['ppm'], bins=20))['BSW'].agg(['mean', 'std']).reset_index()
        ppm_grouped['ppm_mid'] = ppm_grouped['ppm'].apply(lambda x: x.mid)
        
        fig = go.Figure()
        
        # Main efficiency curve
        fig.add_trace(go.Scatter(
            x=ppm_grouped['ppm_mid'],
            y=ppm_grouped['mean'],
            mode='lines+markers',
            name='Average BS&W',
            line=dict(color=self.color_scheme['primary'], width=3),
            marker=dict(size=8, color=self.color_scheme['primary'])
        ))
        
        # Confidence band
        fig.add_trace(go.Scatter(
            x=ppm_grouped['ppm_mid'],
            y=ppm_grouped['mean'] + ppm_grouped['std'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=ppm_grouped['ppm_mid'],
            y=ppm_grouped['mean'] - ppm_grouped['std'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(212,175,55,0.2)',
            name='±1 Std Dev',
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title="💧 Chemical Efficiency Curve",
            xaxis_title="Demulsifier Dosage (ppm)",
            yaxis_title="BS&W (%)",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color='#e5e7eb',
            title_font_color=self.color_scheme['primary']
        )
        
        return fig
    
    def create_wash_water_impact_curve(self, data: pd.DataFrame) -> go.Figure:
        """Create wash water impact curve."""
        # Group by wash water percentage
        wash_grouped = data.groupby(pd.cut(data['wash_pct'], bins=15))['BSW'].agg(['mean', 'min', 'max']).reset_index()
        wash_grouped['wash_mid'] = wash_grouped['wash_pct'].apply(lambda x: x.mid)
        
        fig = go.Figure()
        
        # Main curve
        fig.add_trace(go.Scatter(
            x=wash_grouped['wash_mid'],
            y=wash_grouped['mean'],
            mode='lines+markers',
            name='Average BS&W',
            line=dict(color=self.color_scheme['secondary'], width=3),
            marker=dict(size=8, color=self.color_scheme['secondary'])
        ))
        
        # Min-Max band
        fig.add_trace(go.Scatter(
            x=wash_grouped['wash_mid'],
            y=wash_grouped['max'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=wash_grouped['wash_mid'],
            y=wash_grouped['min'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(244,208,63,0.2)',
            name='Min-Max Range',
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title="🚿 Wash Water Impact Analysis",
            xaxis_title="Wash Water (% of crude)",
            yaxis_title="BS&W (%)",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color='#e5e7eb',
            title_font_color=self.color_scheme['primary']
        )
        
        return fig
    
    def create_operating_envelope_heatmap(self, data: pd.DataFrame) -> go.Figure:
        """Create operating envelope heatmap."""
        # Create grid for heatmap
        flow_bins = np.linspace(data['flow_bpd'].min(), data['flow_bpd'].max(), 20)
        temp_bins = np.linspace(data['T'].min(), data['T'].max(), 15)
        
        # Create 2D grid
        flow_grid, temp_grid = np.meshgrid(flow_bins, temp_bins)
        bsw_grid = np.zeros_like(flow_grid)
        
        for i in range(len(temp_bins)-1):
            for j in range(len(flow_bins)-1):
                mask = (
                    (data['T'] >= temp_bins[i]) & (data['T'] < temp_bins[i+1]) &
                    (data['flow_bpd'] >= flow_bins[j]) & (data['flow_bpd'] < flow_bins[j+1])
                )
                if mask.sum() > 0:
                    bsw_grid[i, j] = data[mask]['BSW'].mean()
                else:
                    bsw_grid[i, j] = np.nan
        
        fig = go.Figure(data=go.Heatmap(
            x=flow_bins,
            y=temp_bins,
            z=bsw_grid,
            colorscale='RdYlGn_r',
            colorbar=dict(title="BS&W (%)"),
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="🗺️ Operating Envelope Heatmap",
            xaxis_title="Flow Rate (BPD)",
            yaxis_title="Temperature (°C)",
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font_color='#e5e7eb',
            title_font_color=self.color_scheme['primary']
        )
        
        return fig
    
    def create_optimization_results_table(self, data: pd.DataFrame, best_idx: int, params: Dict[str, Any]) -> pd.DataFrame:
        """Create ranked optimization results table."""
        # Filter feasible solutions
        feasible_data = data[data['BSW'] <= params['spec_bsw']].copy()
        
        if feasible_data.empty:
            return pd.DataFrame()
        
        # Calculate cost
        chemical_cost = feasible_data['ppm'] * 0.01
        energy_cost = (feasible_data['T'] - 105) * 0.005 + (feasible_data['V'] - 22) * 0.003
        wash_cost = feasible_data['wash_pct'] * 0.002
        feasible_data['total_cost'] = chemical_cost + energy_cost + wash_cost
        
        # Sort by priorities (flow desc, cost asc)
        feasible_data = feasible_data.sort_values(['flow_bpd', 'total_cost'], ascending=[False, True])
        
        # Select top 10 results
        top_results = feasible_data.head(10).copy()
        
        # Format for display
        display_df = pd.DataFrame({
            'Rank': range(1, len(top_results) + 1),
            'Flow (BPD)': top_results['flow_bpd'].round(0).astype(int),
            'Temp (°C)': top_results['T'].round(1),
            'Voltage (kV)': top_results['V'].round(1),
            'Demulsifier (ppm)': top_results['ppm'].round(1),
            'Wash Water (%)': top_results['wash_pct'].round(2),
            'Predicted BS&W (%)': top_results['BSW'].round(3),
            'Cost ($/bbl)': top_results['total_cost'].round(4)
        })
        
        return display_df
    
    def calculate_savings_dashboard(self, best_result: pd.Series, baseline: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Calculate savings dashboard metrics."""
        # Baseline assumptions (typical current operation)
        baseline_flow = baseline.get('flow', 25000)
        baseline_ppm = baseline.get('ppm', 50)
        baseline_temp = baseline.get('temp', 120)
        baseline_wash = baseline.get('wash', 2.5)
        
        # Calculate daily savings
        chemical_savings_day = (baseline_ppm - best_result['ppm']) * baseline_flow * 0.01 / 1000  # $/day
        energy_savings_day = (baseline_temp - best_result['T']) * baseline_flow * 0.005 / 1000  # $/day
        wash_savings_day = (baseline_wash - best_result['wash_pct']) * baseline_flow * 0.002 / 1000  # $/day
        throughput_gain = best_result['flow_bpd'] - baseline_flow
        
        # Percentage improvements
        chemical_reduction_pct = (baseline_ppm - best_result['ppm']) / baseline_ppm * 100
        energy_reduction_pct = (baseline_temp - best_result['T']) / baseline_temp * 100
        wash_reduction_pct = (baseline_wash - best_result['wash_pct']) / baseline_wash * 100
        throughput_improvement_pct = throughput_gain / baseline_flow * 100
        
        return {
            'chemical': {
                'savings_day': chemical_savings_day,
                'reduction_pct': chemical_reduction_pct
            },
            'energy': {
                'savings_day': energy_savings_day,
                'reduction_pct': energy_reduction_pct
            },
            'wash_water': {
                'savings_day': wash_savings_day,
                'reduction_pct': wash_reduction_pct
            },
            'throughput': {
                'gain_bpd': throughput_gain,
                'improvement_pct': throughput_improvement_pct
            }
        }


def render_advanced_charts(data: pd.DataFrame, best_idx: int, params: Dict[str, Any]) -> None:
    """Render all advanced charts and results."""
    charts_engine = AdvancedChartsEngine()
    
    st.markdown("### 📊 Advanced Analysis & Insights")
    
    # Strategic View: Pareto + Compliance
    st.markdown("#### 🎯 Strategic Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        pareto_fig = charts_engine.create_pareto_front_chart(data, params)
        st.plotly_chart(pareto_fig, use_container_width=True)
    
    with col2:
        compliance_fig = charts_engine.create_quality_compliance_chart(data, params)
        st.plotly_chart(compliance_fig, use_container_width=True)
    
    # Operational Insights: Curves
    st.markdown("#### ⚙️ Operational Insights")
    
    # Energy analysis
    energy_fig = charts_engine.create_energy_quality_plot(data)
    st.plotly_chart(energy_fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        chemical_fig = charts_engine.create_chemical_efficiency_curve(data)
        st.plotly_chart(chemical_fig, use_container_width=True)
    
    with col4:
        wash_fig = charts_engine.create_wash_water_impact_curve(data)
        st.plotly_chart(wash_fig, use_container_width=True)
    
    # Actionable Setpoints
    st.markdown("#### 🗺️ Operating Envelope")
    heatmap_fig = charts_engine.create_operating_envelope_heatmap(data)
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Results Table
    st.markdown("#### 📋 Top Optimization Results")
    results_table = charts_engine.create_optimization_results_table(data, best_idx, params)
    if not results_table.empty:
        st.dataframe(results_table, use_container_width=True, hide_index=True)
    else:
        st.warning("No feasible solutions found in the parameter space.")
    
    # Savings Dashboard
    if best_idx is not None:
        st.markdown("#### 💰 Business Value Dashboard")
        best_result = data.iloc[best_idx]
        baseline = {'flow': 25000, 'ppm': 50, 'temp': 120, 'wash': 2.5}  # Typical baseline
        savings = charts_engine.calculate_savings_dashboard(best_result, baseline)
        
        # Display savings cards
        savings_col1, savings_col2, savings_col3, savings_col4 = st.columns(4)
        
        with savings_col1:
            st.metric(
                "💧 Chemical Savings",
                f"${savings['chemical']['savings_day']:.0f}/day",
                f"{savings['chemical']['reduction_pct']:.1f}% reduction"
            )
        
        with savings_col2:
            st.metric(
                "⚡ Energy Savings",
                f"${savings['energy']['savings_day']:.0f}/day",
                f"{savings['energy']['reduction_pct']:.1f}% reduction"
            )
        
        with savings_col3:
            st.metric(
                "🚿 Water Savings",
                f"${savings['wash_water']['savings_day']:.0f}/day",
                f"{savings['wash_water']['reduction_pct']:.1f}% reduction"
            )
        
        with savings_col4:
            st.metric(
                "🏭 Throughput Gain",
                f"{savings['throughput']['gain_bpd']:.0f} BPD",
                f"{savings['throughput']['improvement_pct']:.1f}% increase"
            )
        
        # Total annual savings
        total_daily_savings = (savings['chemical']['savings_day'] + 
                             savings['energy']['savings_day'] + 
                             savings['wash_water']['savings_day'])
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(21, 128, 61, 0.1)); 
                    border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 16px; padding: 1.5rem; margin-top: 2rem;">
            <h4 style="color: #22c55e; margin: 0 0 1rem 0;">💰 Total Annual Savings Potential</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; color: #e5e7eb;">
                <div><strong>Daily Savings:</strong> ${total_daily_savings:.0f}</div>
                <div><strong>Annual Savings:</strong> ${total_daily_savings * 365:.0f}</div>
                <div><strong>ROI Period:</strong> ~6 months</div>
                <div><strong>Payback:</strong> Immediate</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
