# Capacitor Bank Energization Analysis App

This Streamlit application calculates the transient response of the energization current for capacitor banks. It can handle scenarios involving both isolated and back-to-back capacitor bank energizations. The app allows the user to input key electrical parameters and outputs various metrics, including inrush currents, oscillation frequencies, and visualizations.

## Features

- **Customizable Inputs**: Users can provide the voltage, frequency, short-circuit current, number of capacitor banks, and other important values to simulate real-world energization scenarios.
- **Isolated and Back-to-Back Capacitor Bank Calculations**: The app supports calculations for both isolated and multiple capacitor banks already in service.
- **Graphical Visualization**: The app generates interactive plots to visualize inrush currents and transient voltage behavior.
- **Language Support**: The app supports multiple languages, with translations for English, Portuguese, Spanish, Chinese, French, and German.
- **Downloadable Reports**: Users can download detailed PDF reports, including simulation results and graphs, in a ZIP file.

## Installation

To run this app locally, follow these steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run back_to_back_v8.py
    ```

2. Open the application in your browser at `http://localhost:8501`.

3. Input the desired parameters for the capacitor bank energization, such as:
   - 3-phase voltage [kV]
   - Frequency [Hz]
   - Short-circuit current at the bus [kA]
   - Number of banks

4. View the results, including inrush current peaks, oscillation frequencies, and transient voltage plots.

5. Download a report of the analysis in PDF format by clicking the "Latex Report" button.

## File Descriptions

- **`back_to_back_v8.py`**: Main application script handling user input, computations, and graphical output.
- **`config.py`**: Handles language and locale settings, allowing dynamic adjustments to the UI based on user-selected language.
- **`dicionarios.py`**: Contains translation dictionaries for multiple languages.
- **`funcoes_auxiliares.py`**: Contains helper functions for formatting inputs, calculations, and replacing values in LaTeX reports.
- **`inputs_layout.py`**: Responsible for rendering the input fields in the Streamlit UI.
- **`relatorio.py`**: Generates figures and processes LaTeX files to create downloadable reports.
- **`realtorio_pdf_inrush.py`**: Automates the generation of PDF reports using LaTeX templates.
- **`requirements.py`**: Contains a list of required Python packages.

## Dependencies

The application requires the following Python libraries, which are specified in the `requirements.txt` file:

- `matplotlib`
- `streamlit`
- `numpy`
- `pandas`
- `plotly`

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

Developed by Angelo Alfredo Hafner  
Email: [aah@dax.energy](mailto:aah@dax.energy)
