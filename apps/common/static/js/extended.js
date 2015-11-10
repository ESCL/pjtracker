/**
 * @summary     pjtracker
 * @description Functionalities for the user interface
 * @version     1.0.0
 * @file        extended.js
 * @author      Omar Melendrez (www.escng.com)
 * @contact     omar.melendrez@escng.com
 *
 * @copyright Copyright 2015 Omar Melendrez, all rights reserved.
 *
 */

/**
 * Global variables
 */
var current_div = 0;

/**
 * Global setup for Ajax calls
 *
 */

$.ajaxSetup({
    
    type : 'GET',
    
    contentType : "application/json; charset=utf-8",
    
    dataType : "json",
    
    cache : true,
    
    timeout : 60000, // Timeout of 60 seconds
    
    error : function(xhr, errorThrown) {
        
        //log_ajax_error(xhr, errorThrown);
        
        return;
    }
});

/**
 * Graphic chart generator
 *
 * api: "/resources/api/v0/employees/?format=json"
 * title: "Hours per activity"
 * type: "column" [valid types: column, pie, area, bar, doughnut]
 */
generate_graph = function(api, title, type) {

    var div = "div" + current_div;

    $(".row").append('<div id=' + div + ' class="graph_div four columns"></div>');

    current_div++;

    $.ajax({

        url : api,
        data : "{}",

        success : function(data) {

            var graph_data = [];
            
            var l = data.meta.total_count;

            var record = data.objects;

            for (var i = 0; i < l; i++) {
                $this = record[i];

                var value = $this.id,
                    label = $this.first_name;

                graph_data.push({

                    y : value,

                    label : label

                });

            };

            var chart = new CanvasJS.Chart(div, {

                theme : "theme1", //theme1

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
