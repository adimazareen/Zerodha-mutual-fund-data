fetch('http://localhost:5000/get-data')
  .then(response => response.json())
  .then(data => {
    console.log(data);
    
    const chartOptions = {
      series: data.holdings.map(holding => ({
        name: holding.name,
        data: holding.data
      })),
      chart: {
        type: 'bar',
        height: 350,
        stacked: true,
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800
        }
      },
      xaxis: {
        categories: data.months,
        title: {
          text: "Month",
          style: {
            fontSize: '14px'
          }
        }
      },
      title: {
        text: "Top 10 Holdings and Other (Monthly)",
        align: 'center',
        style: {
          fontSize: '18px',
          color: '#555'
        }
      },
      yaxis: {
        title: {
          text: "Percentage (%)",
          style: {
            fontSize: '14px'
          }
        }
      },
      colors: [
        "#008FFB", "#00E396", "#FEB019", "#FF4560", "#775DD0",
        "#546E7A", "#26A69A", "#D10CE8", "#F46036", "#2F4F4F",
        "#A1A1A1", "#FEB019", "#FF4560", "#775DD0",
        "#546E7A", "#26A69A", "#D10CE8", "#F46036", "#2F4F4F",// Color for "Other"
      ],
      legend: {
        position: 'bottom',
        offsetY: 10
      },
      responsive: [{
        breakpoint: 600,
        options: {
          chart: {
            width: 300
          },
          legend: {
            position: 'bottom'
          }
        }
      }]
    };

    const chart = new ApexCharts(document.querySelector("#nav-chart"), chartOptions);
    chart.render();
  });

  function filterSuggestions() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const suggestions = document.getElementById('search-suggestions');
    const suggestionItems = suggestions.getElementsByTagName('li');

    let matchFound = false;
    for (let i = 0; i < suggestionItems.length; i++) {
      const text = suggestionItems[i].textContent.toLowerCase();
      if (text.includes(searchInput)) {
        suggestionItems[i].style.display = 'block';
        matchFound = true;
      } else {
        suggestionItems[i].style.display = 'none';
      }
    }

    // Show suggestions if any match is found
    suggestions.style.display = matchFound ? 'block' : 'none';
  }