function lineChart(ctxL, labels, data, label, color, bcolor){
    //var ctxL = document.getElementById("lineChart").getContext('2d');
    var myLineChart = new Chart(ctxL, {
    type: 'line',
    data: {
    labels: labels,
    datasets: [{
    label: label,
    data: data,
    backgroundColor: color,
    borderColor: bcolor,
    borderWidth: 1
    },
    ]
    },
    options: {
        // scales: {
        //     xAxes: [{
        //         gridLines: {
        //             drawOnChartArea: false
        //         }
        //     }],
        //     yAxes: [{
        //         gridLines: {
        //             drawOnChartArea: false
        //         }
        //     }]
        // },
    responsive: true
    }
    });
}





// function playerStatsPerYear(player_id, season) {
//     let pointsAr = [];
//     let assistsAr = [];
//     let gamesNumbers = [];
//     let threePointsPer = [];
//     let freeThrowsPer = [];
//     return fetch("https://api-nba-v1.p.rapidapi.com/players/statistics?id=" + player_id.toString() + "&season=" + season.toString(), {
//             "method": "GET",
//             "headers": {
//                 "x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
//                 "x-rapidapi-key": "71df5c7d97msh81656ed06f59badp159b26jsna1076804ff4f"
//             }
//         })
//         .then(res => {
//             return res.json();
//         })
//         .then(data => {
//             var game = 0;
//             // console.log(data);
//             for (var row of data.response) {
//                 game = game + 1;
//                 pointsAr.push(row.points);
//                 assistsAr.push(row.assists);
//                 gamesNumbers.push(game);
//                 threePointsPer.push(row.tpp); 
//                 freeThrowsPer.push(row.ftp);  
//             }
//             // console.log(pointsAr)
//             // console.log(assistsAr)
//             // console.log(gamesNumbers)
//             return [pointsAr, assistsAr, gamesNumbers, threePointsPer, freeThrowsPer]
//         })
//         .catch(error => {
//             console.log(error)
//         });
// };
// (async() => {
//     var id = document.getElementById("id_player").content;
//     const x = await playerStatsPerYear(id, 2021).then(data => {return data;});
//     console.log(x[0])
//     console.log(x[1])
//     console.log(x[2])
//     ///////////////////////////////////////////////////////////////////////////////
//     var finalThreeP = 0;
//     var count = 0;
//     x[3].forEach(element => {
//         if(element != null){
//             finalThreeP = finalThreeP + Number(element);
//             count++;
//         }
//     });
//     var tppFinal = Math.round( finalThreeP/count * 10 ) / 10;
//     console.log('aaaaaaaaaaaaaaaaa', tppFinal);
//     ///////////////////////////////////////////////////////////////////////////////
//     var freeThrowP = 0;
//     var count = 0;
//     x[4].forEach(element => {
//         if(element != null){
//             freeThrowP = freeThrowP + Number(element);
//             count++;
//         }
//     });
//     var ftpFinal = Math.round( freeThrowP/count * 10 ) / 10;
//     console.log('aaaaaaaaaaaaaaaaa', ftpFinal);

//     ///////////////////////////////////////////////////////////////////////////////

//     // lineChart for Points
//     var ctx1 = document.getElementById("linePoints").getContext('2d');
//     lineChart(ctx1, x[2], x[0])
//     // DoughnutChart for 3P
//     var ctx2 = document.getElementById("tp-percentages").getContext('2d');
//     var labels = ['3P Percentage'];
//     DoughnutChart(ctx2, labels, tppFinal)
//     // DoughnutChart for FT
//     var ctx3 = document.getElementById("ft-percentages").getContext('2d');
//     var labels = ['FT Percentage'];
//     DoughnutChart(ctx3, labels, ftpFinal)
// })();

