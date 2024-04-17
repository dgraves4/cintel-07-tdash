import seaborn as sns  # Import Seaborn for data visualization
from faicons import icon_svg  # Import for embedding FontAwesome icons in the UI
from shiny import reactive  # Import reactive for creating reactive expressions
from shiny.express import input, render, ui  # Import UI elements, input handling, and rendering functions
from shinywidgets import render_bokeh   # Import Bokeh for interactive plots
import palmerpenguins  # Import palmerpenguins for data

# Load the dataset once at app start
df = palmerpenguins.load_penguins()

# Set global page options such as the title and layout configurations
ui.page_opts(title="Dgraves4 Module 7 Penguins Dashboard", fillable=True)

# Define a sidebar for interactive controls
with ui.sidebar(title="Filter controls"):
    # Create a slider input to filter penguins by body mass
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Create checkbox group for users to select which species to display
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()  # Horizontal rule for better visual separation
    ui.h6("Links")  # Subheading for links

    # Links to external resources and further reading
    ui.a(
        "Dgraves4 GitHub Source",
        href="https://github.com/dgravesr4/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "Dgraves4 GitHub App",
        href="https://dgravesr4.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "Dgraves4 GitHub Issues",
        href="https://github.com/dgravesr4/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Layout for value boxes displaying calculated statistics
with ui.layout_column_wrap(fill=False):
    # Value box to show total number of penguins after filtering
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"
        
        # Render a text output showing the count of penguins after filtering
        @render.text
        def count():
            return filtered_df().shape[0]

    # Value box for average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"
        
        # Render a text output showing the average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box for average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"
        
        # Render a text output showing the average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout for plots and data tables
with ui.layout_columns():
    # Card layout for bokeh plot
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth: Bokeh Plot")
        
        ui.input_selectize(
            "var", "Select variable",
            choices=["bill_length_mm", "body_mass_g"]
        )

        @render_bokeh
        def hist():
            from bokeh.plotting import figure
            from palmerpenguins import load_penguins

            p = figure(x_axis_label=input.var(), y_axis_label="count")
            bins = load_penguins()[input.var()].value_counts().sort_index()
            p.quad(
                top=bins.values,
                bottom=0,
                left=bins.index - 0.5,
                right=bins.index + 0.5,
            )
            return p

    # Card layout for displaying a data table of penguin stats
    with ui.card(full_screen=True):
        ui.card_header("Data Table: Penguin Data")
        
        # Render a data frame showing selected columns from filtered data
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Define a reactive expression to filter the dataframe based on user inputs
@reactive.calc
def filtered_df():
    # Filter the dataframe based on species selection and mass threshold
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

