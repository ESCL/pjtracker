/**
 * Global setup for Ajax calls
 *
 */
$.ajaxSetup({
    type : 'GET',
    contentType : "application/json; charset=utf-8",
    dataType : "json",
    cache : true,
    timeout : 30000, // Timeout of 10 seconds
    error : function(xhr, errorThrown) {
        //log_ajax_error(xhr, errorThrown);
        return;
    }
});

generate_graph = function(div, api, title, type) {

    /** Graph types
     * column
     * area
     * bar
     * doughnut
     */

    $.ajax({
        url : api,
        data : "{}",
        success : function(data) {
            var graph_data = [];
            $this = data.meta;
            var value = parseInt($this.total_count);
            var label = "wbs"; //$this.label;
            graph_data.push({
                y : value,
                label : label 
            });

            var chart = new CanvasJS.Chart(div, {
                theme : "theme2", //theme1
                title : {
                    text : title
                },
                animationEnabled : true, // change to true
                exportEnabled : false, // If true a button will allow to export
                // graph to JPG file
                exportFileName : title,
                data : [{
                    type : type,
                    dataPoints : graph_data
                }]
            });
            chart.render();
        }
    });
};
