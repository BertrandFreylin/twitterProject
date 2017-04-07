google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(tweetRatio);

function tweetRatio() {

    $.ajax({
        url: "/get_tweet_ratio/",
        type: "post",
        data: 'get_tweet_ratio',
        success: function(json_dict) {
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Element');
            data.addColumn('number', 'Percentage');
            data.addRows([
            ['Nom/Description', json_dict['name_part']],
            ['Tweet', json_dict['text_part']]
            ]);
            var chart = new google.visualization.PieChart(document.getElementById('partchart'));
            var options = {
                legend: 'none',
                'width':400,
                 'height':300
            };
            chart.draw(data, options);
        }
    });

}

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(popHeroes);

function popHeroes() {

    $.ajax({
        url: "/get_popular_heroes/",
        type: "post",
        data: 'get_popular_heroes',
        success: function(json_dict) {
            var sortable = [];
            for (var hero in json_dict) {
                sortable.push([hero, json_dict[hero]]);
            }

            sortable.sort(function(a, b) {
                return b[1] - a[1];
            });

            array_hero = [['Héros', 'Nombre de tweets']];
            for(var i =0 in sortable) {
                array_hero.push([sortable[i][0], sortable[i][1]])
            }

            var data = google.visualization.arrayToDataTable(array_hero);

            var view = new google.visualization.DataView(data);

            var chart = new google.visualization.ColumnChart(document.getElementById("popchart"));
            var options = {
                legend: 'none',
                'width':650,
                'height':300
            };
            chart.draw(view, options);
        }
    });
}

google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(commovRatio);

function commovRatio() {
        $.ajax({
        url: "/get_support_heroes/",
        type: "post",
        data: 'get_support_heroes',
        success: function(json_dict) {
            var global_total = json_dict['movie']['TOTAL'] + json_dict['comic']['TOTAL'];
            var percentage_movie = json_dict['movie']['TOTAL'] * 100 / global_total;
            var percentage_comic = json_dict['comic']['TOTAL'] * 100 / global_total;

            var data = google.visualization.arrayToDataTable([
            ['Support', 'Pourcentage'],
            ['Films', percentage_movie],
            ['Comics', percentage_comic]
            ]);

            var options = {
            greenFrom: 50, greenTo: 100,
            yellowFrom:30, yellowTo: 50,
            redFrom:0, redTo: 30,
            minorTicks: 5,
            };

            var chart = new google.visualization.Gauge(document.getElementById('supportchart'));

            chart.draw(data, options);
        }
        });
}

google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(commovDetailRatio);

function commovDetailRatio() {
        $.ajax({
        url: "/get_support_heroes_by_hero/",
        type: "post",
        data: 'get_support_heroes_by_hero',
        success: function(json_dict) {
            var result_array = [['Héros', 'Films', 'Comics', 'Total']];

            for(var i =0 in json_dict) {
                result_array.push([i, json_dict[i]['movie'], json_dict[i]['comic'], json_dict[i]['TOTAL']])
            }

            var data = google.visualization.arrayToDataTable(result_array);

            var options = {
              chart: {
                legend: 'none',
                'width':650,
                'height':300
              }
            };

            var chart = new google.charts.Bar(document.getElementById('supportdetailchart'));

            chart.draw(data, options);
        }
        });
}

google.charts.load('current', {'packages':['geochart']});
google.charts.setOnLoadCallback(mapGlobal);


function mapGlobal() {
        $.ajax({
        url: "/get_countries_heroes/",
        type: "post",
        data: 'get_countries_heroes',
        success: function(json_dict) {
            var ordered_country = [['Pays', 'Popularité']]
            for(var i =0 in json_dict) {
                ordered_country.push([i, json_dict[i]])
            }
            var data = google.visualization.arrayToDataTable(ordered_country);

            var options = {
                height: 500,
            };

            var chart = new google.visualization.GeoChart(document.getElementById('mapchartbycountry'));

            chart.draw(data, options);
        }
        });
}

google.charts.load('current', {'packages':['geochart']});
google.charts.setOnLoadCallback(mapHeroesGlobal);

function mapHeroesGlobal() {
        $.ajax({
        url: "/get_fav_heroes_by_country/",
        type: "post",
        data: 'get_fav_heroes_by_country',
        success: function(json_dict) {
            var ordered_country = [['Pays', 'Top Héros', 'Popularité']];
            console.log(json_dict);
            for(country in json_dict) {
                ordered_country.push([country, json_dict[country]['top_hero'], json_dict[country]['value']])
            }
            var data = google.visualization.arrayToDataTable(ordered_country);

            var options = {
                height: 500,
            };

            var chart = new google.visualization.GeoChart(document.getElementById('mapchartbycountrybyheroes'));

            chart.draw(data, options);
        }
        });
}

google.charts.load('current', {packages: ['bar']});
google.charts.setOnLoadCallback(bartoto);

function bartoto() {

    $.ajax({
        url: "/get_fav_rt_hero/",
        type: "post",
        data: 'get_fav_rt_hero',
        success: function(json_dict) {
            var render = [['Héros', 'Favoris', 'Retweet']];

            for (hero in json_dict){
                render.push([hero, json_dict[hero]['totalfav'], json_dict[hero]['totalrt']])
            }
            var data = new google.visualization.arrayToDataTable(render);

            var options = {
              height: 500,
              chart: {
                title: 'Nearby galaxies',
                subtitle: 'distance on the left, brightness on the right'
              },
              bars: 'horizontal', // Required for Material Bar Charts.
              series: {
                0: { axis: 'distance' }, // Bind series 0 to an axis named 'distance'.
                1: { axis: 'brightness' } // Bind series 1 to an axis named 'brightness'.
              },
              axes: {
                x: {
                  distance: {label: 'Favoris'}, // Bottom x-axis.
                  brightness: {side: 'top', label: 'Retweet'} // Top x-axis.
                }
              }
            };

          var chart = new google.charts.Bar(document.getElementById('barchartfavrt'));
          chart.draw(data, options);
        }
    });

}