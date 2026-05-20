import requests
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from ipyleaflet import Map, TileLayer, basemaps, basemap_to_tiles

# Minimal UI layout with just a map card
app_ui = ui.page_fluid(
    ui.card(
        ui.card_header("Local TiTiler Map Test (Alaska ALFL 2020)"),
        output_widget("map_widget"),
        style="height: 85vh; margin-top: 20px;"
    )
)

def server(input, output, session):
    @render_widget
    def map_widget():
        cog_url = "http://206.12.92.143/data/dashboard/ALFL/Alaska/ALFL_Alaska_2020.tif"
        
        # 2. URL-encode the path parameters so it passes safely through the tiler
        encoded_cog = requests.utils.quote(cog_url, safe="")
        
        # 3. Point directly to your local intercepted ASGI tiler path
        local_tiler_base = "http://127.0.0.1:8000"
        
        tile_string = f"{local_tiler_base}/cog/tiles/{{z}}/{{x}}/{{y}}.png?url={encoded_cog}&colormap_name=ylgn"
        
        mean_density_layer = TileLayer(
            url=tile_string, 
            name="Mean Density Distribution",
            opacity=0.8
        )
        
        esri = basemap_to_tiles(basemaps.Esri.WorldImagery)
        esri.base = True
        
        # Initialize map centered on Alaska
        m = Map(layers=[esri, mean_density_layer], center=[64.2, -149.5], zoom=4)
        return m

app = App(app_ui, server)