(async function () {
  const { datum } = window;
  console.log(datum);

  const labels = datum.Pos;
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Pressão [Pa]",
        hidden: true,
        data: datum.P,
        borderColor: "red",
        backgroundColor: "red",
        yAxisID: "y1",
      },
      {
        label: "Temperatura [K]",
        data: datum.T,
        borderColor: "blue",
        backgroundColor: "blue",
        yAxisID: "y2",
      },
    ],
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
        title: {
          display: true,
          text: "Resultados por seção",
        },
      },
      scales: {
        y1: {
          type: "linear",
          display: true,
          position: "left",
        },
        y2: {
          type: "linear",
          display: true,
          position: "right",

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
      },
    },
  });
})();

// (async function () {
//   const DATA_COUNT = 7;
//   const NUMBER_CFG = { count: DATA_COUNT, min: -100, max: 100 };

//   const labels = Utils.months({ count: 7 });
//   const data = {
//     labels: labels,
//     datasets: [
//       {
//         label: "Dataset 1",
//         data: Utils.numbers(NUMBER_CFG),
//         borderColor: Utils.CHART_COLORS.red,
//         backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
//         yAxisID: "y",
//       },
//       {
//         label: "Dataset 2",
//         data: Utils.numbers(NUMBER_CFG),
//         borderColor: Utils.CHART_COLORS.blue,
//         backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
//         yAxisID: "y1",
//       },
//     ],
//   };

//   new Chart(document.getElementById("canvas"), {
//     type: "line",
//     data: data,
//     options: {
//       responsive: true,
//       interaction: {
//         mode: "index",
//         intersect: false,
//       },
//       stacked: false,
//       plugins: {
//         title: {
//           display: true,
//           text: "Chart.js Line Chart - Multi Axis",
//         },
//       },
//       scales: {
//         y: {
//           type: "linear",
//           display: true,
//           position: "left",
//         },
//         y1: {
//           type: "linear",
//           display: true,
//           position: "right",

//           // grid line settings
//           grid: {
//             drawOnChartArea: false, // only want the grid lines for one axis to show up
//           },
//         },
//       },
//     },
//   });
// })();
