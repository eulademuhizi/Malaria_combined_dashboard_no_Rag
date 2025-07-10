import streamlit as st
import geopandas as gpd
import pandas as pd
from typing import List, Tuple, Dict, Any

# Import custom modules
from data_loader import MalariaDataLoader, SectorDataLoader
from metrics_calculator import MetricsCalculator
from map_visualizations import MapVisualizations
from chart_visualizations import ChartVisualizations
from dashboard_styling import DashboardStyling

class SimplifiedDashboard:
    """Simplified main dashboard - clean and focused"""
    
    def __init__(self):
        # Initialize data loaders
        self.district_loader = MalariaDataLoader()
        self.sector_loader = SectorDataLoader()
        
        # Initialize session state
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'admin_level' not in st.session_state:
            st.session_state.admin_level = 'districts'
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'dashboard'
    
    def setup(self):
        """Setup page configuration and styling"""
        DashboardStyling.setup_page_config()
        DashboardStyling.apply_custom_css()
    
    def render_header(self):
        """Render dashboard header"""
        header_html = DashboardStyling.render_header_with_logo()
        st.markdown(header_html, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar navigation - CLEAN VERSION"""
        st.sidebar.markdown("## Administrative Level")
        
        # Admin level selection
        admin_level = st.sidebar.radio(
            "Select Level",
            ['districts', 'sectors'],
            format_func=lambda x: '📍 Districts' if x == 'districts' else '🏘️ Sectors',
            key='admin_level_radio'
        )
        st.session_state.admin_level = admin_level
        
        st.sidebar.markdown("---")
        
        # Navigation menu - Only Dashboard and Trends
        navigation_tabs = {
            'dashboard': {
                'label': '📊 Dashboard',
                'icon': '📊',
                'description': 'Overview & Geographic Analysis'
            },
            'trends': {
                'label': '📈 Trends',
                'icon': '📈',
                'description': 'Historical Trends & Insights'
            }
        }
        
        st.sidebar.markdown(f"## {admin_level.title()} Analysis")
        
        # Navigation buttons
        for page_key, page_info in navigation_tabs.items():
            if st.sidebar.button(
                page_info['label'], 
                key=f"{page_key}_{admin_level}",
                help=page_info['description']
            ):
                st.session_state.current_page = page_key
                st.rerun()
    
    def load_data(self) -> Tuple[gpd.GeoDataFrame, List[str], str]:
        """Load data based on selected admin level"""
        if st.session_state.admin_level == 'districts':
            data, entity_options = self.district_loader.load_data()
            display_type = "Districts"
        else:
            data, entity_options = self.sector_loader.load_data()
            display_type = "Sectors"
        
        if data is None:
            st.error("Failed to load data. Please check your data files.")
            st.stop()
        
        return data, entity_options, display_type
    
    def setup_components(self, data: gpd.GeoDataFrame) -> Dict[str, Any]:
        """Setup dashboard components"""
        display_type = "Districts" if st.session_state.admin_level == "districts" else "Sectors"
        
        components = {
            'metrics_calculator': MetricsCalculator(display_type),
            'map_viz': MapVisualizations(display_type, MetricsCalculator(display_type)),
            'chart_viz': ChartVisualizations(display_type, MetricsCalculator(display_type)),
            'display_type': display_type
        }
        
        return components
    
    def render_global_filters(self, data: gpd.GeoDataFrame) -> Tuple[int, int, str, Dict]:
        """Render global filters"""
        st.markdown("## Filters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            available_years = sorted(data['year'].unique(), reverse=True)
            selected_year = st.selectbox(
                "Year",
                available_years,
                key=f"year_{st.session_state.admin_level}_{st.session_state.current_page}"
            )
        
        with col2:
            available_months = sorted(data[data['year'] == selected_year]['month'].unique())
            month_names = {
                1: "January", 2: "February", 3: "March", 4: "April", 
                5: "May", 6: "June", 7: "July", 8: "August",
                9: "September", 10: "October", 11: "November", 12: "December"
            }
            
            selected_month = st.selectbox(
                "Month",
                available_months,
                format_func=lambda x: month_names.get(x, str(x)),
                index=len(available_months)-1 if available_months else 0,
                key=f"month_{st.session_state.admin_level}_{st.session_state.current_page}"
            )
        
        with col3:
            # Auto-detect available metrics for current admin level
            metric_options = self._get_available_metrics(data)
            
            # Check if previously selected metric exists for current admin level
            default_metric = list(metric_options.keys())[0]
            if (hasattr(st.session_state, 'dashboard_metric') and 
                st.session_state.dashboard_metric in metric_options):
                # Find the index of the previously selected metric
                try:
                    default_index = list(metric_options.keys()).index(st.session_state.dashboard_metric)
                except ValueError:
                    default_index = 0
            else:
                default_index = 0
            
            selected_metric = st.selectbox(
                "Primary Metric",
                list(metric_options.keys()),
                format_func=lambda x: metric_options[x],
                index=default_index,
                key=f"metric_{st.session_state.admin_level}_{st.session_state.current_page}"
            )
        
        # Store in session state for other pages - use admin level specific keys
        st.session_state[f'dashboard_year_{st.session_state.admin_level}'] = selected_year
        st.session_state[f'dashboard_month_{st.session_state.admin_level}'] = selected_month
        st.session_state[f'dashboard_metric_{st.session_state.admin_level}'] = selected_metric
        st.session_state[f'dashboard_metric_options_{st.session_state.admin_level}'] = metric_options
        
        # Also store general ones for backward compatibility
        st.session_state.dashboard_year = selected_year
        st.session_state.dashboard_month = selected_month
        st.session_state.dashboard_metric = selected_metric
        st.session_state.dashboard_metric_options = metric_options
        
        st.markdown("---")
        
        return selected_year, selected_month, selected_metric, metric_options
    
    def _get_available_metrics(self, data: gpd.GeoDataFrame) -> Dict[str, str]:
        """Get available metrics from data"""
        columns = data.columns.tolist()
        
        if 'all cases' in columns and 'Severe cases/Deaths' in columns:
            return {
                "all cases": "Total Cases",
                "Severe cases/Deaths": "Severe Cases/Deaths", 
                "all cases incidence": "Cases Incidence Rate"
            }
        elif 'Simple malaria cases' in columns:
            return {
                "Simple malaria cases": "Simple Malaria Cases",
                "incidence": "Incidence Rate"
            }
        else:
            return {"Population": "Population"}
    
    def render_page(self, data: gpd.GeoDataFrame, entity_options: List[str], components: Dict[str, Any]):
        """Render the selected page"""
        page = st.session_state.current_page
        
        if page == 'dashboard':
            self._render_dashboard_page(data, entity_options, components)
        elif page == 'trends':
            self._render_trends_page(data, entity_options, components)
    
    def _render_dashboard_page(self, data: gpd.GeoDataFrame, entity_options: List[str], components: Dict[str, Any]):
        """Render dashboard page"""
        st.markdown(f"# 📊 {st.session_state.admin_level.title()} Dashboard")
        st.markdown(f"Geographic analysis and overview across Rwanda's {st.session_state.admin_level}")
        
        # Global filters
        selected_year, selected_month, selected_metric, metric_options = self.render_global_filters(data)
        
        # Current data
        current_data = data[(data['year'] == selected_year) & (data['month'] == selected_month)]
        
        if current_data.empty:
            st.error("No data available for the selected period.")
            return
        
        # Overview cards
        self._render_overview_cards(current_data, data, selected_year, selected_month)
        
        st.markdown("---")
        
        # Main visualizations
        col1, col2 = st.columns([7, 3])
        
        with col1:
            st.markdown(f"### Geographic Distribution - {metric_options[selected_metric]}")
            map_fig = components['map_viz'].create_choropleth_map(data, selected_year, selected_month, selected_metric)
            st.plotly_chart(map_fig, use_container_width=True)
        
        with col2:
            st.markdown(f"### Top 10 {components['display_type']}")
            chart_fig = components['chart_viz'].create_top_entities_chart(data, selected_year, selected_month, selected_metric)
            st.plotly_chart(chart_fig, use_container_width=True)
    
    def _render_trends_page(self, data: gpd.GeoDataFrame, entity_options: List[str], components: Dict[str, Any]):
        """Render trends page"""
        st.markdown("# 📈 Trends & Insights")
        st.markdown(f"Historical analysis for {st.session_state.admin_level}")
        
        # Always get current available metrics for the current admin level
        available_metrics = self._get_available_metrics(data)
        
        # Use stored dashboard filters or defaults, but validate metric exists
        if (hasattr(st.session_state, f'dashboard_metric_{st.session_state.admin_level}') and 
            st.session_state[f'dashboard_metric_{st.session_state.admin_level}'] in available_metrics):
            selected_metric = st.session_state[f'dashboard_metric_{st.session_state.admin_level}']
            selected_year = st.session_state[f'dashboard_year_{st.session_state.admin_level}']
            selected_month = st.session_state[f'dashboard_month_{st.session_state.admin_level}']
        else:
            # Use defaults if stored metric doesn't exist for current admin level
            selected_year = data['year'].max()
            selected_month = data[data['year'] == selected_year]['month'].max()
            selected_metric = list(available_metrics.keys())[0]
        
        # Two-column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Historical Trends")
            
            # Entity selection
            default_entities = entity_options[:3] if entity_options else []
            selected_entities = st.multiselect(
                f"Select {components['display_type']} (max 5)",
                entity_options,
                default=default_entities,
                max_selections=5,
                key=f"trend_entities_{st.session_state.admin_level}"
            )
            
            if selected_entities:
                trend_fig = components['chart_viz'].create_trend_chart(data, selected_entities, selected_metric)
                if trend_fig:
                    st.plotly_chart(trend_fig, use_container_width=True)
            else:
                st.info(f"Please select {components['display_type'].lower()} to view trends")
        
        with col2:
            st.markdown("### Priority Analysis")
            
            current_data = data[(data['year'] == selected_year) & (data['month'] == selected_month)]
            
            if not current_data.empty:
                scatterplot_fig, _, _ = components['chart_viz'].create_scatterplot(data, selected_year, selected_month)
                if scatterplot_fig:
                    st.plotly_chart(scatterplot_fig, use_container_width=True)
    
    def _render_overview_cards(self, current_data: gpd.GeoDataFrame, all_data: gpd.GeoDataFrame, year: int, month: int):
        """Render overview metric cards with new 3-box design"""
        from utils import get_month_name
        
        # Get previous month for comparison
        if month == 1:
            prev_month, prev_year = 12, year - 1
        else:
            prev_month, prev_year = month - 1, year
        
        prev_data = all_data[(all_data['year'] == prev_year) & (all_data['month'] == prev_month)]
        
        # Get current selected metric from session state
        selected_metric = getattr(st.session_state, 'dashboard_metric', None)
        
        # Three columns layout
        col1, col2, col3 = st.columns([1, 1, 1])
        
        if st.session_state.admin_level == 'districts':
            self._render_district_overview_cards(col1, col2, col3, current_data, prev_data, selected_metric, year, month)
        else:
            self._render_sector_overview_cards(col1, col2, col3, current_data, prev_data, selected_metric, year, month)

    def _render_district_overview_cards(self, col1, col2, col3, current_data, prev_data, selected_metric, year, month):
        """Render district overview cards"""
        
        # Calculate current metrics
        current_total_cases = current_data['all cases'].sum()
        current_incidence = current_data['all cases incidence'].mean()
        
        # Calculate previous metrics
        prev_total_cases = prev_data['all cases'].sum() if not prev_data.empty else current_total_cases
        prev_incidence = prev_data['all cases incidence'].mean() if not prev_data.empty else current_incidence
        
        # Calculate changes
        cases_change = current_total_cases - prev_total_cases
        incidence_change = current_incidence - prev_incidence
        
        # Calculate district-level changes for ranking
        district_changes = []
        for district in current_data['District'].unique():
            current_district = current_data[current_data['District'] == district]
            prev_district = prev_data[prev_data['District'] == district] if not prev_data.empty else pd.DataFrame()
            
            if not current_district.empty:
                if selected_metric == 'all cases incidence':
                    current_val = current_district['all cases incidence'].iloc[0]
                    prev_val = prev_district['all cases incidence'].iloc[0] if not prev_district.empty else current_val
                    change = current_val - prev_val
                    change_pct = ((change / prev_val) * 100) if prev_val > 0 else 0
                    metric_name = "incidence"
                    current_display = f"{current_val:.1f}"
                else:  # Default to 'all cases'
                    current_val = current_district['all cases'].iloc[0]
                    prev_val = prev_district['all cases'].iloc[0] if not prev_district.empty else current_val
                    change = current_val - prev_val
                    change_pct = ((change / prev_val) * 100) if prev_val > 0 else 0
                    metric_name = "cases"
                    current_display = f"{int(current_val)}"
                
                district_changes.append({
                    'District': district,
                    'change': change,
                    'change_pct': change_pct,
                    'metric_name': metric_name,
                    'current_display': current_display
                })
        
        df_changes = pd.DataFrame(district_changes)
        
        # Column 1: Current Metrics
        with col1:
            st.markdown("###  CURRENT METRICS")
            
            st.metric(
                label="Total Cases",
                value=f"{int(current_total_cases):,}",
                delta=f"{cases_change:+,.0f}",
                delta_color="inverse"
            )
            
            st.metric(
                label="Average Incidence",
                value=f"{current_incidence:.1f}",
                delta=f"{incidence_change:+.1f}",
                delta_color="inverse"
            )
        
        # Column 2: Highest Increases
        with col2:
            st.markdown("###  HIGHEST INCREASES")
            
            if not df_changes.empty:
                top_increases = df_changes.nlargest(3, 'change')  # Sort by raw change, not percentage
                
                for _, row in top_increases.iterrows():
                    increase_pct = row['change_pct']
                    bg_color = 'rgba(40, 167, 69, 0.3)' if increase_pct <= 0 else 'rgba(220, 53, 69, 0.3)'
                    
                    st.markdown(f"""
                    <div style="
                        background: {bg_color};
                        padding: 1.2rem;
                        border-radius: 10px;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <strong style="flex: 1; color: white; font-size: 18px;">{row['District']}</strong>
                        <span style="color: white; text-align: right; font-size: 17px;">
                            {row['current_display']} {row['metric_name']} ({row['change']:+,.0f})
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Column 3: Biggest Decreases
        with col3:
            st.markdown("### BIGGEST DECREASES")
            
            if not df_changes.empty:
                top_decreases = df_changes.nsmallest(3, 'change')  # Sort by raw change, not percentage
                
                for _, row in top_decreases.iterrows():
                    decrease_pct = row['change_pct']
                    bg_color = 'rgba(40, 167, 69, 0.3)' if decrease_pct <= 0 else 'rgba(220, 53, 69, 0.3)'
                    
                    st.markdown(f"""
                    <div style="
                        background: {bg_color};
                        padding: 1.2rem;
                        border-radius: 10px;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <strong style="flex: 1; color: white; font-size: 18px;">{row['District']}</strong>
                        <span style="color: white; text-align: right; font-size: 17px;">
                            {row['current_display']} {row['metric_name']} ({row['change']:+,.0f})
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

    def _render_sector_overview_cards(self, col1, col2, col3, current_data, prev_data, selected_metric, year, month):
        """Render sector overview cards"""
        
        # Calculate current metrics
        current_simple_cases = current_data['Simple malaria cases'].sum()
        current_incidence = current_data['incidence'].mean()
        
        # Calculate previous metrics
        prev_simple_cases = prev_data['Simple malaria cases'].sum() if not prev_data.empty else current_simple_cases
        prev_incidence = prev_data['incidence'].mean() if not prev_data.empty else current_incidence
        
        # Calculate changes
        simple_cases_change = current_simple_cases - prev_simple_cases
        incidence_change = current_incidence - prev_incidence
        
        # Calculate sector-level changes for ranking
        sector_changes = []
        for _, sector_row in current_data.iterrows():
            sector_name = sector_row.get('sector_display', sector_row.get('Sector', 'Unknown'))
            sector_key = sector_row.get('sector_key', sector_name)
            
            # Find previous data for this sector
            prev_sector_data = prev_data[
                (prev_data['Sector'] == sector_row['Sector']) & 
                (prev_data['District'] == sector_row['District'])
            ] if not prev_data.empty else pd.DataFrame()
            
            if selected_metric == 'incidence':
                current_val = sector_row['incidence']
                prev_val = prev_sector_data['incidence'].iloc[0] if not prev_sector_data.empty else current_val
                change = current_val - prev_val
                change_pct = ((change / prev_val) * 100) if prev_val > 0 else 0
                metric_name = "incidence"
                current_display = f"{current_val:.1f}"
            else:  # Default to 'Simple malaria cases'
                current_val = sector_row['Simple malaria cases']
                prev_val = prev_sector_data['Simple malaria cases'].iloc[0] if not prev_sector_data.empty else current_val
                change = current_val - prev_val
                change_pct = ((change / prev_val) * 100) if prev_val > 0 else 0
                metric_name = "cases"
                current_display = f"{int(current_val)}"
            
            sector_changes.append({
                'Sector': sector_name,
                'change': change,
                'change_pct': change_pct,
                'metric_name': metric_name,
                'current_display': current_display
            })
        
        df_changes = pd.DataFrame(sector_changes)
        
        # Column 1: Current Metrics
        with col1:
            st.markdown("### CURRENT METRICS")
            
            st.metric(
                label="Simple Cases",
                value=f"{int(current_simple_cases):,}",
                delta=f"{simple_cases_change:+,.0f}",
                delta_color="inverse"
            )
            
            st.metric(
                label="Average Incidence",
                value=f"{current_incidence:.1f}",
                delta=f"{incidence_change:+.1f}",
                delta_color="inverse"
            )
        
        # Column 2: Highest Increases
        with col2:
            st.markdown("### HIGHEST INCREASES")
            
            if not df_changes.empty:
                top_increases = df_changes.nlargest(3, 'change')  # Sort by raw change, not percentage
                
                for _, row in top_increases.iterrows():
                    increase_pct = row['change_pct']
                    bg_color = 'rgba(40, 167, 69, 0.3)' if increase_pct <= 0 else 'rgba(220, 53, 69, 0.3)'
                    
                    st.markdown(f"""
                    <div style="
                        background: {bg_color};
                        padding: 1.2rem;
                        border-radius: 10px;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <strong style="flex: 1; color: white; font-size: 18px;">{row['Sector']}</strong>
                        <span style="color: white; text-align: right; font-size: 17px;">
                            {row['current_display']} {row['metric_name']} ({row['change']:+,.0f})
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Column 3: Biggest Decreases
        with col3:
            st.markdown("###  BIGGEST DECREASES")
            
            if not df_changes.empty:
                top_decreases = df_changes.nsmallest(3, 'change')  # Sort by raw change, not percentage
                
                for _, row in top_decreases.iterrows():
                    decrease_pct = row['change_pct']
                    bg_color = 'rgba(40, 167, 69, 0.3)' if decrease_pct <= 0 else 'rgba(220, 53, 69, 0.3)'
                    
                    st.markdown(f"""
                    <div style="
                        background: {bg_color};
                        padding: 1.2rem;
                        border-radius: 10px;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <strong style="flex: 1; color: white; font-size: 18px;">{row['Sector']}</strong>
                        <span style="color: white; text-align: right; font-size: 17px;">
                            {row['current_display']} {row['metric_name']} ({row['change']:+,.0f})
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
    
    def run(self):
        """Main execution function"""
        # Setup
        self.setup()
        
        # Render components
        self.render_header()
        self.render_sidebar()
        
        # Load data and setup components
        data, entity_options, display_type = self.load_data()
        components = self.setup_components(data)
        
        # Render selected page
        self.render_page(data, entity_options, components)

# Main execution
def main():
    """Main function to run the dashboard"""
    dashboard = SimplifiedDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()