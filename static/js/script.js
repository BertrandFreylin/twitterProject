google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

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
            chart.draw(data, null);
        }
    });

}

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

    $.ajax({
        url: "/get_popular_heroes/",
        type: "post",
        data: 'get_popular_heroes',
        success: function(json_dict) {
            console.log(json_dict);

            var sortable = [];
            for (var hero in json_dict) {
                sortable.push([hero, json_dict[hero]]);
            }

            sortable.sort(function(a, b) {
                return b[1] - a[1];
            });

            console.log(sortable);

            array_hero = [['Héros', 'Nombre de tweets']];
            for(var i =0 in sortable) {
                array_hero.push([sortable[i][0], sortable[i][1]])
            }

            var data = google.visualization.arrayToDataTable(array_hero);

            var view = new google.visualization.DataView(data);

            var chart = new google.visualization.ColumnChart(document.getElementById("popchart"));
            chart.draw(view);
        }
    });
}