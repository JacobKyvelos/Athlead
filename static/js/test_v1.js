function appearStats(i) {
    fetch("/static/json/player_history_stats.json")
    .then(response => {
        console.log(response);
        if(!response.ok){
            throw Error('error')
        }
        return response.json();
    })
    .then(data => {
        for (const row of data){
            if(row.year == i){
                document.getElementById('points').innerHTML = row.points;
                document.getElementById('assists').innerHTML = row.assists;
                document.getElementById('rebounds').innerHTML = row.totReb;
            }
            
        }
    })
    .catch(error => {
        console.log(error)
    }); 
  };

function statCharts(i){
    (async() => {
        const result = await appearStats(i).then(data => {
            return data;
        });
    })();

    console.log('allakse')
    console.log(document.getElementById('points').innerHTML)

    // chart colors
    var colors = ['#007bff','#28a745','#333333','#c3e6cb','#dc3545','#6c757d'];

    /* 3 donut charts */
    var donutOptions = {
      cutoutPercentage: 85, 
      legend: {position:'bottom', padding:5, labels: {pointStyle:'circle', usePointStyle:true}}
    };

    var x = document.getElementById('points').innerHTML
    var y = parseFloat(x)

    // donut 1
    var chDonutData1 = {
        labels: ['Bootstrap', 'Popper'],
        datasets: [
          {
            backgroundColor: colors.slice(0,3),
            borderWidth: 0,
            data: [y, 100-y]
          }
        ],
        
    };

    var chDonut1 = document.getElementById("chDonut1");
    if (chDonut1) {
      new Chart(chDonut1, {
          type: 'pie',
          data: chDonutData1,
          options: donutOptions
      });
    }
  }


function changeFunc(player_id, year) {
    fetch("https://api-nba-v1.p.rapidapi.com/players/statistics?id=" + player_id.toString() + "&season=" + year.toString(), {
            "method": "GET",
            "headers": {
                "x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
                "x-rapidapi-key": "71df5c7d97msh81656ed06f59badp159b26jsna1076804ff4f"
            }
        })
        //fetch("./stats_per_season.JSON")
        .then(response => {
            console.log(response);
            if (!response.ok) {
                throw Error('error')
            }
            return response.json();
        })
        .then(data => {
            // console.log(data);
            table = document.getElementById("trapezi");

            const tableHead = table.querySelector('thead')
            const tableBody = table.querySelector('tbody')

            tableHead.innerHTML = "<tr></tr>";
            tableBody.innerHTML = "";

            // headers

            const cellGameId = document.createElement('th');
            cellGameId.textContent = 'GAME';
            tableHead.querySelector('tr').appendChild(cellGameId);

            const cellPoi = document.createElement('th');
            cellPoi.textContent = 'POINTS';
            tableHead.querySelector('tr').appendChild(cellPoi);

            const cellAss = document.createElement('th');
            cellAss.textContent = 'ASSISTS';
            tableHead.querySelector('tr').appendChild(cellAss);

            const cellReb = document.createElement('th');
            cellReb.textContent = 'REBOUNDS';
            tableHead.querySelector('tr').appendChild(cellReb);
            // rows
            (async() => {
                var count = 0;
                for (const row of data.response) {
                    if(count < 5){
                        var codes = ''
                            // console.log(row.assists)
                        const rowElement = document.createElement('tr');

                        const cellGameId = document.createElement('td');
                        // cellGameId.textContent = row.game.id;
                        console.log(row.game.id)
                        var codes = await findGameId(row.game.id, year).then(data => {
                            return data;
                        });
                        console.log('kodikoiiiiiiiiiiiiiiiiiii',codes)
                        cellGameId.innerHTML = "<img src='" + codes[2] + "' alt='hello' style = 'max-width : 8%; height:auto;' /> " + codes[0] + "<img src='" + codes[1] + "' alt='home' style = 'max-width : 8%; height:auto;' /> "
                        rowElement.appendChild(cellGameId);

                        const cellPoi = document.createElement('td');
                        if(row.points != null){
                            cellPoi.textContent = row.points;
                            rowElement.appendChild(cellPoi);
                        }
                        else{
                            cellPoi.textContent = '-';
                            rowElement.appendChild(cellPoi);
                        }
                        
                        const cellAss = document.createElement('td');
                        cellAss.textContent = row.assists;
                        rowElement.appendChild(cellAss);

                        const cellReb = document.createElement('td');
                        cellReb.textContent = row.totReb;
                        rowElement.appendChild(cellReb);

                        tableBody.appendChild(rowElement);
                        count++;
                    }
                }
            })();
        })
        .catch(error => {
            console.log(error)
        });
};


function findGameId(gameId, year) {
    var array = [];
    return fetch("/static/json/games_per_season_" + year.toString() + ".JSON")
    // return fetch("https://api-nba-v1.p.rapidapi.com/games?season=" + year.toString(), {
    //     "method": "GET",
    //     "headers": {
    //         "x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
    //         "x-rapidapi-key": "71df5c7d97msh81656ed06f59badp159b26jsna1076804ff4f"
    //     }
    // })
        .then(res => {
            return res.json();
        })
        .then(data => {
            // console.log(data);
            for (var row of data.response) {
                if (row.id === gameId) {
                    var x = row.teams.visitors.code + '-' + row.teams.home.code
                    var home_logo = row.teams.home.logo;
                    var away_logo = row.teams.visitors.logo;
                    array.push(x);
                    array.push(home_logo);
                    array.push(away_logo);
                }
            }
            return array;
        })
        .catch(error => {
            console.log(error)
        });
};

changeFunc(document.getElementById('id_player').content, 2021);