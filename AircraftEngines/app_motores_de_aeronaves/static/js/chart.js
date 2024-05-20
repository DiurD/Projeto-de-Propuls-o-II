(async function () {
  const { datum } = window;
  console.log(datum);

  const labels = datum.Section;
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Pressão [Pa]",
        data: datum.P,
        borderColor: "red",
        backgroundColor: "red",
        yAxisID: "y1",
      },
      {
        label: "Temperatura [K]",
        data: datum.T,
        hidden: true,
        borderColor: "blue",
        backgroundColor: "blue",
        yAxisID: "y2",
      },
      {
        label: "Mach",
        hidden: true,
        data: datum.Mach,
        borderColor: "purple",
        backgroundColor: "purple",
        yAxisID: "y3",
      },
      {
        label: "Diâmetro [m]",
        hidden: true,
        data: datum.D,
        borderColor: "green",
        backgroundColor: "green",
        yAxisID: "y4",
      },
      {
        label: "Área [m²]",
        hidden: true,
        data: datum.A,
        borderColor: "orange",
        backgroundColor: "orange",
        yAxisID: "y5",
      },
      {
        label: "Área ótima [m²]",
        hidden: true,
        data: datum.Aot,
        borderColor: "pink",
        backgroundColor: "pink",
        yAxisID: "y6",
      },
      {
        label: "Área/Área ótima [m²/m²]",
        hidden: true,
        data: datum.A_Aot,
        borderColor: "gray",
        backgroundColor: "gray",
        yAxisID: "y7",
      },
      {
        label: "Pressão total [Pa]",
        hidden: true,
        data: datum.Pt,
        borderColor: "black",
        backgroundColor: "black",
        yAxisID: "y8",
      },
      {
        label: "Temperatura total [K]",
        hidden: true,
        data: datum.Tt,
        borderColor: "#a98600",
        backgroundColor: "#a98600",
        yAxisID: "y9",
      },
    ],
  };

  const plugin = {
    id: "customCanvasBackgroundColor",
    beforeDraw: (chart, args, options) => {
      const { ctx } = chart;
      ctx.save();
      ctx.globalCompositeOperation = "destination-over";
      ctx.fillStyle = options.color || "#99ffff";
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();
    },
  };

  new Chart(document.getElementById("canvas"), {
    type: "line",
    data: data,
    options: {
      responsive: true,
      interaction: {
        mode: "index",
        intersect: false,
      },
      stacked: false,
      plugins: {
        customCanvasBackgroundColor: {
          color: "white",
        },
        title: {
          display: true,
          text: "Resultados por seção - " + datum.Nome,
          font: {
            size: 30,
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Seções do motor",
            font: {
              size: 15,
            },
          },
        },
        y1: {
          type: "linear",
          display: 'auto',
          position: "left",
          ticks: {
            display: 'auto',
            color: "red",
          },
        },
        y2: {
          type: "linear",
          display: 'auto',
          position: "right",
          ticks: {
            display: 'auto',
            color: "blue",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y3: {
          type: "linear",
          display: 'auto',
          position: "left",
          ticks: {
            display: 'auto',
            color: "purple",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y4: {
          type: "linear",
          display: 'auto',
          position: "right",
          ticks: {
            display: 'auto',
            color: "green",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y5: {
          type: "linear",
          display: 'auto',
          position: "left",
          ticks: {
            display: 'auto',
            color: "orange",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y6: {
          type: "linear",
          display: 'auto',
          position: "right",
          ticks: {
            display: 'auto',
            color: "pink",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y7: {
          type: "linear",
          display: 'auto',
          position: "left",
          ticks: {
            display: 'auto',
            color: "gray",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y8: {
          type: "linear",
          display: 'auto',
          position: "right",
          ticks: {
            display: 'auto',
            color: "black",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y9: {
          type: "linear",
          display: 'auto',
          position: "left",
          ticks: {
            display: 'auto',
            color: "#a98600",
          },

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
      },
    },
    plugins: [plugin],
  });
})();

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("download-chart").addEventListener("click", download);
});

var download = function () {
  var link = document.createElement("a");
  link.download = "grafico.png";
  link.href = document.getElementById("canvas").toDataURL("image/png");
  link.click();
};
