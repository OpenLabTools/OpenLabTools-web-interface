function plot_time_serise(name, id) {
    var options = {
        lines:  { show: true },
        points: { show: true },
        xaxis:  { mode: "time" },
        series: { shadowSize: 0 } // Drawing is faster without shadows
    };

    // Initiate a recurring data update
    function start_updating() {
        var data = [];
        var plot = $.plot("#" + name, data, options);
        var iteration = 0;
        function fetchData() {
            ++iteration;
            function onDataReceived(series) {
                data.push( [series.time*1000, series.data] );
                if (iteration > 20) { data.shift() }
                //console.log(data)
                plot.setData([data]);
                plot.setupGrid()
                plot.draw();
            }
            $.ajax({
                url: "/get_new_point",
                type: "GET",
                dataType: "json",
                data: {
                    name: name,
                    id : id
                },
                success: onDataReceived
            });
            setTimeout(fetchData, 1000);
        }
        fetchData();
    };
    start_updating();
};

function button_ajax(id, status_indicator) {
    var btn = $('#'+id);
    btn.button('loading');
    $.getJSON( "../button_click", { id: id } )
    .done( function (json) {
        console.log("State: " + json.state);
        if (status_indicator) {
            $("#"+ id + "-Status").text("Status: " + json.state);
        }
    })
    .fail( function () {
        alert("Request failed!")
    })
    .always( function () {
        btn.button('reset');
    });
}