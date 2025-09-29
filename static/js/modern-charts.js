// Modern SVG-based charts using Plotly.js
// Engineering-focused, sharp, scalable charts

class ModernChartRenderer {
  constructor() {
    this.engineeringTheme = {
      // Semantic engineering color palette
      colors: {
        // Semantic color mapping for engineering contexts
        flowrate: '#1e40af',     // Deep blue - Flowrate/Capacity/Volume
        chemical: '#059669',     // Process green - Chemicals/Quality/Efficiency  
        energy: '#ea580c',       // Energy orange - Power/Temperature/Energy
        temperature: '#dc2626',  // Temperature red - Heat/Critical parameters
        neutral: '#64748b',      // Technical gray - Supporting elements
        // Legacy aliases for compatibility
        primary: '#1e40af',
        secondary: '#059669', 
        tertiary: '#dc2626',
        accent: '#ea580c'
      },
      
      // Modern layout configuration
      layout: {
        font: {
          family: '"Inter", "IBM Plex Sans", "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          size: 14,
          color: '#111827',
          weight: 500
        },
        paper_bgcolor: 'rgba(248, 250, 252, 0.8)',
        plot_bgcolor: 'rgba(255, 255, 255, 0.9)',
        margin: { t: 40, r: 30, b: 60, l: 70 },
        showlegend: false,
        hovermode: 'closest',
        
        // Professional grid styling
        xaxis: {
          gridcolor: 'rgba(226, 232, 240, 0.6)',
          gridwidth: 1,
          zeroline: false,
          showspikes: true,
          spikethickness: 1,
          spikecolor: '#64748b',
          tickfont: { size: 13, color: '#374151', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 },
          titlefont: { size: 15, color: '#111827', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 700, standoff: 25 }
        },
        yaxis: {
          gridcolor: 'rgba(226, 232, 240, 0.6)',
          gridwidth: 1,
          zeroline: false,
          showspikes: true,
          spikethickness: 1,
          spikecolor: '#64748b',
          tickfont: { size: 13, color: '#374151', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 },
          titlefont: { size: 15, color: '#111827', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 700, standoff: 25 }
        }
      },
      
      // Modern configuration
      config: {
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        toImageButtonOptions: {
          format: 'svg',
          filename: 'process_chart',
          height: 600,
          width: 800,
          scale: 1
        },
        responsive: true,
        useResizeHandler: true,
        style: { width: "100%", height: "100%" }
      }
    };
  }

  // Chart 1: Crude Flowrate vs Washwater Flowrate (PRIORITY CHART - FULL WIDTH)
  drawProcessChart1() {
    // Real process data from desalter operations
    const processData = [
      {washwater: 3.601, crudeFlow: 51850, salt: 0.939, bsw: 0.1441},
      {washwater: 0.773, crudeFlow: 54044, salt: 4.03, bsw: 0.1526},
      {washwater: 3.929, crudeFlow: 35897, salt: 0.637, bsw: 0.1314},
      {washwater: 1.367, crudeFlow: 57832, salt: 3.332, bsw: 0.1492},
      {washwater: 3.135, crudeFlow: 42736, salt: 1.359, bsw: 0.1348},
      {washwater: 2.343, crudeFlow: 45175, salt: 2.557, bsw: 0.1308},
      {washwater: 3.676, crudeFlow: 37162, salt: 1.051, bsw: 0.1328},
      {washwater: 3.594, crudeFlow: 31517, salt: 1.339, bsw: 0.1283},
      {washwater: 0.812, crudeFlow: 35311, salt: 3.577, bsw: 0.1361},
      {washwater: 2.311, crudeFlow: 48463, salt: 1.976, bsw: 0.1333},
      {washwater: 1.703, crudeFlow: 58906, salt: 3.385, bsw: 0.1542},
      {washwater: 1.243, crudeFlow: 33390, salt: 3.25, bsw: 0.1315},
      {washwater: 1.762, crudeFlow: 48701, salt: 2.743, bsw: 0.1374},
      {washwater: 1.448, crudeFlow: 53630, salt: 3.143, bsw: 0.1487},
      {washwater: 3.166, crudeFlow: 55371, salt: 1.86, bsw: 0.1503},
      {washwater: 2.173, crudeFlow: 42043, salt: 2.459, bsw: 0.1262},
      {washwater: 0.846, crudeFlow: 55985, salt: 3.92, bsw: 0.1684},
      {washwater: 1.464, crudeFlow: 51114, salt: 3.379, bsw: 0.1503},
      {washwater: 3.28, crudeFlow: 47507, salt: 2.044, bsw: 0.1391},
      {washwater: 2.299, crudeFlow: 33806, salt: 1.885, bsw: 0.1186}
    ];

    const flowRates = processData.map(d => d.crudeFlow);
    const washWater = processData.map(d => d.washwater);
    const saltPTB = processData.map(d => d.salt);
    const bswPercent = processData.map(d => d.bsw);

    // Add trend line for clarity
    const trendX = Array.from({length: 50}, (_, i) => 20000 + i * (60000 - 20000) / 49);
    const trendY = trendX.map(x => 0.5 + (x - 20000) / 40000 * 3.5);

    const data = [
      // Data points with Salt_PTB color coding and BSW sizing
      {
        x: flowRates,
        y: washWater,
        mode: 'markers',
        type: 'scatter',
        name: 'Process Data',
        marker: {
          size: saltPTB.map(salt => 8 + (salt - 0.5) * 4), // Size based on Salt (8-24 range)
          color: bswPercent,
          colorscale: [
            [0, '#10b981'], // Green for low BSW
            [0.5, '#f59e0b'], // Yellow for medium BSW
            [1, '#ef4444'] // Red for high BSW
          ],
          colorbar: {
            title: 'BSW (%)',
            titlefont: { size: 12, color: '#374151' },
            tickfont: { size: 10, color: '#6b7280' },
            thickness: 15,
            len: 0.7
          },
          opacity: 0.8,
          line: { width: 1, color: 'white' }
        },
        customdata: processData.map(d => [d.salt, d.bsw]),
        hovertemplate:
          '<b>Crude Flow:</b> %{x:,.0f} BPD<br>' +
          '<b>Washwater:</b> %{y:.3f}%<br>' +
          '<b>Salt (PTB):</b> %{customdata[0]:.3f}<br>' +
          '<b>BSW:</b> %{customdata[1]:.4f}%<br>' +
          '<extra></extra>'
      }
    ];

    const layout = {
      ...this.engineeringTheme.layout,
      margin: { t: 20, r: 30, b: 80, l: 80 },
      paper_bgcolor: 'rgba(248, 250, 252, 0.8)',
      plot_bgcolor: 'rgba(248, 250, 252, 0.9)',
      autosize: true,
      xaxis: {
        ...this.engineeringTheme.layout.xaxis,
        title: {
          text: 'Crude Flowrate (BPD)',
          font: { size: 15, color: '#111827', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 600 }
        },
        tickformat: ',.0f',
        tickfont: { size: 13, color: '#374151', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 }
      },
      yaxis: {
        ...this.engineeringTheme.layout.yaxis,
        title: {
          text: 'Washwater (% Vol.)',
          font: { size: 15, color: '#111827', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 600 }
        },
        tickformat: '.1f',
        tickfont: { size: 13, color: '#374151', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 }
      },
      showlegend: false,
      annotations: [
        {
          x: 0.02,
          y: 0.98,
          xref: 'paper',
          yref: 'paper',
          text: '<b>Visualization Key:</b><br>• Color: BSW Percentage<br>• Size: Salt Content (PTB)',
          showarrow: false,
          align: 'left',
          bgcolor: 'rgba(255, 255, 255, 0.9)',
          bordercolor: 'rgba(0, 0, 0, 0.1)',
          borderwidth: 1,
          font: { size: 11, color: '#374151', family: '"Inter", sans-serif' }
        }
      ]
    };

    Plotly.newPlot('processChart1', data, layout, this.engineeringTheme.config).then(() => {
      // Force resize to fit container width
      Plotly.Plots.resize('processChart1');
    });
  }

  // Chart 2: Temperature vs Demulsifier (Inverse Relationship)
  drawProcessChart2() {
    // Real process data from desalter operations
    const processData = [
      {demulsifier: 39.96, temperature: 121.05, salt: 9.9, bsw: 0.1394},
      {demulsifier: 86.06, temperature: 107.1, salt: 7.512, bsw: 0.1447},
      {demulsifier: 68.56, temperature: 109.04, salt: 9.9, bsw: 0.1709},
      {demulsifier: 57.89, temperature: 127.46, salt: 6.69, bsw: 0.0978},
      {demulsifier: 22.48, temperature: 120.16, salt: 9.9, bsw: 0.19},
      {demulsifier: 22.48, temperature: 105.23, salt: 9.9, bsw: 0.19},
      {demulsifier: 14.65, temperature: 107.54, salt: 9.9, bsw: 0.19},
      {demulsifier: 79.29, temperature: 121.59, salt: 9.073, bsw: 0.1349},
      {demulsifier: 58.09, temperature: 105.13, salt: 9.9, bsw: 0.19},
      {demulsifier: 66.65, temperature: 109.02, salt: 9.9, bsw: 0.1784},
      {demulsifier: 11.65, temperature: 118.72, salt: 9.9, bsw: 0.19},
      {demulsifier: 87.59, temperature: 122.3, salt: 9.9, bsw: 0.1625},
      {demulsifier: 76.6, temperature: 121.3, salt: 8.287, bsw: 0.1174},
      {demulsifier: 26.99, temperature: 110.61, salt: 9.9, bsw: 0.19},
      {demulsifier: 24.55, temperature: 122.8, salt: 9.9, bsw: 0.1875},
      {demulsifier: 24.67, temperature: 110.93, salt: 9.9, bsw: 0.19},
      {demulsifier: 34.34, temperature: 113.13, salt: 9.9, bsw: 0.19},
      {demulsifier: 51.98, temperature: 123.66, salt: 5.739, bsw: 0.0931},
      {demulsifier: 44.56, temperature: 121.24, salt: 8.214, bsw: 0.1257},
      {demulsifier: 33.3, temperature: 126.23, salt: 7.541, bsw: 0.1083}
    ];

    const temperatures = processData.map(d => d.temperature);
    const demulsifier = processData.map(d => d.demulsifier);
    const saltPTB = processData.map(d => d.salt);
    const bswPercent = processData.map(d => d.bsw);

    // Add inverse relationship trend line
    const trendTemp = Array.from({length: 30}, (_, i) => 105 + i * 25 / 29);
    const trendPPM = trendTemp.map(t => 90 - (t - 105) / 25 * 70);

    const data = [
      // Data points with BSW color coding and Salt sizing
      {
        x: temperatures,
        y: demulsifier,
        mode: 'markers',
        type: 'scatter',
        name: 'Process Data',
        marker: {
          size: saltPTB.map(salt => 8 + (salt - 5.5) * 3), // Size based on Salt (8-21 range)
          color: bswPercent,
          colorscale: [
            [0, '#10b981'], // Green for low BSW
            [0.5, '#f59e0b'], // Yellow for medium BSW
            [1, '#ef4444'] // Red for high BSW
          ],
          colorbar: {
            title: 'BSW (%)',
            titlefont: { size: 12, color: '#374151' },
            tickfont: { size: 10, color: '#6b7280' },
            thickness: 15,
            len: 0.7,
            x: 1.02
          },
          opacity: 0.8,
          line: { width: 1, color: 'white' }
        },
        customdata: processData.map(d => [d.salt, d.bsw]),
        hovertemplate:
          '<b>Temperature:</b> %{x:.2f}°C<br>' +
          '<b>Demulsifier:</b> %{y:.2f} ppm<br>' +
          '<b>Salt (PTB):</b> %{customdata[0]:.3f}<br>' +
          '<b>BSW:</b> %{customdata[1]:.4f}%<br>' +
          '<extra></extra>'
      }
    ];

    const layout = {
      ...this.engineeringTheme.layout,
      margin: { t: 20, r: 80, b: 60, l: 70 },
      paper_bgcolor: 'rgba(248, 250, 252, 0.8)',
      plot_bgcolor: 'rgba(248, 250, 252, 0.9)',
      xaxis: {
        ...this.engineeringTheme.layout.xaxis,
        title: {
          text: 'Temperature (°C)',
          font: { size: 12, color: '#475569', family: 'Inter' }
        }
      },
      yaxis: {
        ...this.engineeringTheme.layout.yaxis,
        title: {
          text: 'Demulsifier (ppm)',
          font: { size: 12, color: '#475569', family: 'Inter' }
        }
      },
      showlegend: false,
      annotations: [
        {
          x: 0.02,
          y: 0.98,
          xref: 'paper',
          yref: 'paper',
          text: '<b>Visualization Key:</b><br>• Color: BSW Percentage<br>• Size: Salt Content (PTB)',
          showarrow: false,
          align: 'left',
          bgcolor: 'rgba(255, 255, 255, 0.9)',
          bordercolor: 'rgba(0, 0, 0, 0.1)',
          borderwidth: 1,
          font: { size: 11, color: '#374151', family: '"Inter", sans-serif' }
        }
      ]
    };

    Plotly.newPlot('processChart2', data, layout, this.engineeringTheme.config);
  }

  // Chart 3: Temperature vs Crude Flowrate
  drawProcessChart3() {
    // Real process data from desalter operations
    const processData = [
      {temperature: 111.22, crudeFlow: 59980, salt: 4.9, bsw: 0.1496},
      {temperature: 109.08, crudeFlow: 33508, salt: 4.463, bsw: 0.1342},
      {temperature: 124.59, crudeFlow: 30706, salt: 3.424, bsw: 0.0916},
      {temperature: 125.21, crudeFlow: 39139, salt: 3.683, bsw: 0.0988},
      {temperature: 120.64, crudeFlow: 28054, salt: 3.437, bsw: 0.0957},
      {temperature: 120.1, crudeFlow: 49477, salt: 3.725, bsw: 0.1187},
      {temperature: 127.14, crudeFlow: 27083, salt: 3.186, bsw: 0.0819},
      {temperature: 123.98, crudeFlow: 26082, salt: 3.41, bsw: 0.0928},
      {temperature: 109.53, crudeFlow: 34127, salt: 4.308, bsw: 0.1297},
      {temperature: 108.75, crudeFlow: 35960, salt: 4.61, bsw: 0.1326},
      {temperature: 115.89, crudeFlow: 57270, salt: 4.306, bsw: 0.1437},
      {temperature: 114.63, crudeFlow: 41727, salt: 4.645, bsw: 0.1281},
      {temperature: 119.39, crudeFlow: 38165, salt: 3.614, bsw: 0.1166},
      {temperature: 108.65, crudeFlow: 40557, salt: 4.664, bsw: 0.1389},
      {temperature: 122.16, crudeFlow: 57264, salt: 4.159, bsw: 0.1265},
      {temperature: 116.72, crudeFlow: 21997, salt: 3.702, bsw: 0.1061},
      {temperature: 119.25, crudeFlow: 54833, salt: 4.149, bsw: 0.1272},
      {temperature: 121.14, crudeFlow: 32104, salt: 4.174, bsw: 0.1025},
      {temperature: 123.08, crudeFlow: 42548, salt: 3.875, bsw: 0.1072},
      {temperature: 122.02, crudeFlow: 44511, salt: 3.288, bsw: 0.1073}
    ];

    const temperatures = processData.map(d => d.temperature);
    const flowRates = processData.map(d => d.crudeFlow);
    const saltPTB = processData.map(d => d.salt);
    const bswPercent = processData.map(d => d.bsw);

    const data = [
      // Data points with Salt color coding and BSW sizing
      {
        x: temperatures, // Temperature on X-axis as requested
        y: flowRates,   // Crude Flow on Y-axis
        mode: 'markers',
        type: 'scatter',
        name: 'Process Data',
        marker: {
          size: saltPTB.map(salt => 8 + (salt - 3.0) * 6), // Size based on Salt (8-20 range)
          color: bswPercent,
          colorscale: [
            [0, '#10b981'], // Green for low BSW
            [0.5, '#f59e0b'], // Yellow for medium BSW
            [1, '#ef4444'] // Red for high BSW
          ],
          colorbar: {
            title: 'BSW (%)',
            titlefont: { size: 12, color: '#374151' },
            tickfont: { size: 10, color: '#6b7280' },
            thickness: 15,
            len: 0.7,
            x: 1.02
          },
          opacity: 0.8,
          line: { width: 1, color: 'white' }
        },
        customdata: processData.map(d => [d.salt, d.bsw]),
        hovertemplate:
          '<b>Temperature:</b> %{x:.2f}°C<br>' +
          '<b>Crude Flow:</b> %{y:,.0f} BPD<br>' +
          '<b>Salt (PTB):</b> %{customdata[0]:.3f}<br>' +
          '<b>BSW:</b> %{customdata[1]:.4f}%<br>' +
          '<extra></extra>'
      }
    ];

    const layout = {
      ...this.engineeringTheme.layout,
      margin: { t: 20, r: 80, b: 60, l: 70 },
      paper_bgcolor: 'rgba(248, 250, 252, 0.8)',
      plot_bgcolor: 'rgba(248, 250, 252, 0.9)',
      xaxis: {
        ...this.engineeringTheme.layout.xaxis,
        title: {
          text: 'Temperature (°C)',
          font: { size: 12, color: '#475569', family: 'Inter' }
        },
        tickformat: '.1f'
      },
      yaxis: {
        ...this.engineeringTheme.layout.yaxis,
        title: {
          text: 'Crude Flowrate (BPD)',
          font: { size: 12, color: '#475569', family: 'Inter' }
        },
        tickformat: ',.0f'
      },
      showlegend: false,
      annotations: [
        {
          x: 0.02,
          y: 0.98,
          xref: 'paper',
          yref: 'paper',
          text: '<b>Visualization Key:</b><br>• Color: BSW Percentage<br>• Size: Salt Content (PTB)',
          showarrow: false,
          align: 'left',
          bgcolor: 'rgba(255, 255, 255, 0.9)',
          bordercolor: 'rgba(0, 0, 0, 0.1)',
          borderwidth: 1,
          font: { size: 11, color: '#374151', family: '"Inter", sans-serif' }
        }
      ]
    };

    Plotly.newPlot('processChart3', data, layout, this.engineeringTheme.config);
  }

  // Chart 4: Temperature vs Power Consumption
  drawProcessChart4() {
    // Real process data from desalter operations
    const processData = [
      {power: 25.94, temperature: 117.85, salt: 3.344, bsw: 0.1197},
      {power: 23.76, temperature: 125.09, salt: 2.602, bsw: 0.1084},
      {power: 22.73, temperature: 106.19, salt: 3.831, bsw: 0.1467},
      {power: 23.92, temperature: 127.72, salt: 2.55, bsw: 0.106},
      {power: 26, temperature: 124.65, salt: 2.926, bsw: 0.1053},
      {power: 26.18, temperature: 126.83, salt: 2.652, bsw: 0.1034},
      {power: 29.63, temperature: 106.77, salt: 3.845, bsw: 0.1361},
      {power: 27.21, temperature: 109.04, salt: 3.725, bsw: 0.1359},
      {power: 26.11, temperature: 118.27, salt: 3.273, bsw: 0.1198},
      {power: 27.37, temperature: 113.01, salt: 3.338, bsw: 0.1289},
      {power: 24.71, temperature: 121.33, salt: 2.985, bsw: 0.1164},
      {power: 26.33, temperature: 109.05, salt: 3.731, bsw: 0.133},
      {power: 30.27, temperature: 111.51, salt: 3.177, bsw: 0.1284},
      {power: 24.72, temperature: 116.56, salt: 3.224, bsw: 0.1299},
      {power: 29.27, temperature: 113.79, salt: 3.511, bsw: 0.1277},
      {power: 23, temperature: 118.56, salt: 3.081, bsw: 0.118},
      {power: 26.98, temperature: 111.6, salt: 3.813, bsw: 0.1343},
      {power: 27.8, temperature: 129.39, salt: 2.643, bsw: 0.0935},
      {power: 27.77, temperature: 106.97, salt: 3.837, bsw: 0.139},
      {power: 24.07, temperature: 119.91, salt: 3.332, bsw: 0.1128}
    ];

    const temperatures = processData.map(d => d.temperature);
    const powerConsumption = processData.map(d => d.power);
    const saltPTB = processData.map(d => d.salt);
    const bswPercent = processData.map(d => d.bsw);

    const data = [
      // Data points with BSW color coding and Salt sizing
      {
        x: temperatures,
        y: powerConsumption,
        mode: 'markers',
        type: 'scatter',
        name: 'Process Data',
        marker: {
          size: saltPTB.map(salt => 8 + (salt - 2.5) * 8), // Size based on Salt (8-20 range)
          color: bswPercent,
          colorscale: [
            [0, '#10b981'], // Green for low BSW
            [0.5, '#f59e0b'], // Yellow for medium BSW
            [1, '#ef4444'] // Red for high BSW
          ],
          colorbar: {
            title: 'BSW (%)',
            titlefont: { size: 12, color: '#374151' },
            tickfont: { size: 10, color: '#6b7280' },
            thickness: 15,
            len: 0.7,
            x: 1.02
          },
          opacity: 0.8,
          line: { width: 1, color: 'white' }
        },
        customdata: processData.map(d => [d.salt, d.bsw]),
        hovertemplate:
          '<b>Temperature:</b> %{x:.2f}°C<br>' +
          '<b>Power:</b> %{y:.2f} kVA<br>' +
          '<b>Salt (PTB):</b> %{customdata[0]:.3f}<br>' +
          '<b>BSW:</b> %{customdata[1]:.4f}%<br>' +
          '<extra></extra>'
      }
    ];

    const layout = {
      ...this.engineeringTheme.layout,
      margin: { t: 20, r: 80, b: 60, l: 70 },
      paper_bgcolor: 'rgba(248, 250, 252, 0.8)',
      plot_bgcolor: 'rgba(248, 250, 252, 0.9)',
      xaxis: {
        ...this.engineeringTheme.layout.xaxis,
        title: {
          text: 'Temperature (°C)',
          font: { size: 12, color: '#475569', family: 'Inter' }
        },
        tickformat: '.1f'
      },
      yaxis: {
        ...this.engineeringTheme.layout.yaxis,
        title: {
          text: 'Power Consumption (kVA)',
          font: { size: 12, color: '#475569', family: 'Inter' }
        },
        tickformat: '.1f'
      },
      showlegend: false,
      annotations: [
        {
          x: 0.02,
          y: 0.98,
          xref: 'paper',
          yref: 'paper',
          text: '<b>Visualization Key:</b><br>• Color: BSW Percentage<br>• Size: Salt Content (PTB)',
          showarrow: false,
          align: 'left',
          bgcolor: 'rgba(255, 255, 255, 0.9)',
          bordercolor: 'rgba(0, 0, 0, 0.1)',
          borderwidth: 1,
          font: { size: 11, color: '#374151', family: '"Inter", sans-serif' }
        }
      ]
    };

    Plotly.newPlot('processChart4', data, layout, this.engineeringTheme.config);
  }

  // Chart 5: Parameter vs Quality Metrics (Dual Y-axis: BS&W + Salt)
  drawProcessChart5() {
    const parameters = ['Crude Flowrate (BPD)', 'Temperature (°C)', 'Washwater Flowrate (% Vol.)', 'Power (kVA)', 'Demulsifier (ppm)'];
    
    // Quality metrics data based on exact parameter values from metric cards
    // Flow Rate: 30,000 | Demulsifier: 42 | Temperature: 113 | Power: 29 | Wash Water: 1.9
    const bswValues = [0.85, 1.15, 0.65, 0.95, 0.75]; // BS&W (% vol.) - left Y-axis
    const saltValues = [18, 22, 14, 16, 12]; // Salt (PTB) - right Y-axis

    const data = [
      // BS&W trace (left Y-axis)
      {
        x: parameters,
        y: bswValues,
        mode: 'markers+lines',
        type: 'scatter',
        name: 'BS&W (% vol.)',
        yaxis: 'y1',
        line: {
          color: this.engineeringTheme.colors.flowrate,
          width: 3
        },
        marker: {
          size: 8,
          color: this.engineeringTheme.colors.flowrate,
          opacity: 0.8,
          line: { width: 2, color: 'white' }
        },
        hovertemplate:
          '<b>Parameter:</b> %{x}<br>' +
          '<b>BS&W:</b> %{y:.2f}% vol.<br>' +
          '<extra></extra>'
      },
      // Salt trace (right Y-axis)
      {
        x: parameters,
        y: saltValues,
        mode: 'markers+lines',
        type: 'scatter',
        name: 'Salt (PTB)',
        yaxis: 'y2',
        line: {
          color: this.engineeringTheme.colors.chemical,
          width: 3
        },
        marker: {
          size: 8,
          color: this.engineeringTheme.colors.chemical,
          opacity: 0.8,
          line: { width: 2, color: 'white' }
        },
        hovertemplate:
          '<b>Parameter:</b> %{x}<br>' +
          '<b>Salt:</b> %{y:.1f} PTB<br>' +
          '<extra></extra>'
      }
    ];

    const layout = {
      ...this.engineeringTheme.layout,
      margin: { t: 40, r: 80, b: 120, l: 80 },
      paper_bgcolor: 'rgba(248, 250, 252, 0.8)',
      plot_bgcolor: 'rgba(248, 250, 252, 0.9)',
      autosize: true,
      
      // X-axis configuration
      xaxis: {
        ...this.engineeringTheme.layout.xaxis,
        title: {
          text: 'Process Parameters',
          font: { size: 15, color: '#111827', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 600 }
        },
        tickangle: -45,
        tickfont: { size: 12, color: '#374151', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 }
      },
      
      // Left Y-axis (BS&W)
      yaxis: {
        ...this.engineeringTheme.layout.yaxis,
        title: {
          text: 'BS&W (% vol.)',
          font: { size: 15, color: this.engineeringTheme.colors.flowrate, family: '"Inter", "IBM Plex Sans", sans-serif', weight: 600 }
        },
        tickfont: { size: 13, color: this.engineeringTheme.colors.flowrate, family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 },
        tickformat: '.1f',
        side: 'left'
      },
      
      // Right Y-axis (Salt)
      yaxis2: {
        ...this.engineeringTheme.layout.yaxis,
        title: {
          text: 'Salt (PTB)',
          font: { size: 15, color: this.engineeringTheme.colors.chemical, family: '"Inter", "IBM Plex Sans", sans-serif', weight: 600 }
        },
        tickfont: { size: 13, color: this.engineeringTheme.colors.chemical, family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 },
        tickformat: '.0f',
        overlaying: 'y',
        side: 'right',
        gridcolor: 'rgba(226, 232, 240, 0.3)',
        gridwidth: 1,
        zeroline: false,
        showspikes: true,
        spikethickness: 1,
        spikecolor: '#64748b'
      },
      
      showlegend: true,
      legend: {
        x: 0.02,
        y: 0.98,
        bgcolor: 'rgba(255, 255, 255, 0.95)',
        bordercolor: 'rgba(0, 0, 0, 0.1)',
        borderwidth: 1,
        font: { size: 13, color: '#1f2937', family: '"Inter", "IBM Plex Sans", sans-serif', weight: 500 }
      }
    };

    Plotly.newPlot('processChart5', data, layout, this.engineeringTheme.config).then(() => {
      // Force resize to fit container width
      Plotly.Plots.resize('processChart5');
    });
  }


  // Initialize all modern charts with proper timing
  initializeModernCharts() {
    // Wait for containers to be visible and properly sized
    const checkAndDraw = () => {
      const chart2Container = document.getElementById('processChart2');
      if (!chart2Container) {
        console.warn('Chart containers not found');
        return;
      }
      
      // Check if container has proper dimensions
      const containerWidth = chart2Container.offsetWidth;
      if (containerWidth === 0) {
        // Container not ready, wait a bit more
        setTimeout(checkAndDraw, 50);
        return;
      }
      
      // Containers are ready, draw charts (only existing ones)
      this.drawProcessChart2();
      this.drawProcessChart3();
      this.drawProcessChart4();
      this.drawProcessChart5();
    };
    
    checkAndDraw();
  }
}

// Global chart renderer instance
const modernChartRenderer = new ModernChartRenderer();

// Initialize charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  // Wait for Plotly to be available
  if (typeof Plotly !== 'undefined') {
    setTimeout(() => {
      modernChartRenderer.initializeModernCharts();
    }, 500);
  } else {
    console.error('Plotly.js not loaded');
  }
});

// Export for use in other scripts
window.modernChartRenderer = modernChartRenderer;