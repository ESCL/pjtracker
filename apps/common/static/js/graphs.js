/**
 * @summary     pjtracker
 * @description Functionalities for graphs
 * @version     1.0.0
 * @file        graphs.js
 * @author      Omar Melendrez (www.escng.com)
 * @contact     omar.melendrez@escng.com
 *
 * @copyright Copyright 2015 Omar Melendrez, all rights reserved.
 *
 */

/**
 * Global variables
 */

var currentDiv = 0;

/**
 * Graphic chart generator
 *
 * api: "/resources/api/v0/employees/?format=json"
 * title: "Hours per activity"
 * type: "column" [valid types: column, pie, area, bar, doughnut]
 */

generateGraph = function(api, title, type) {
    var divId = "div" + currentDiv;
    var graphs = document.createElement('div');
    graphs.id = divId;
    graphs.setAttribute('class', 'graph-div six columns');
    document.querySelector('#graphs').appendChild(graphs);
    currentDiv++;

    get(api).then(function(data) {
        data = JSON.parse(data);
        var graphData = [];
        var l = data.meta.total_count;
        var record = data.objects;

        for (var i = 0; i < l; i++) {
            $this = record[i];
            var value = $this.id,
                label = $this.first_name;
            graphData.push({
                y : value,
                label : label
            });
        }

        var chart = new CanvasJS.Chart(divId, {
            theme: "theme1",
            title: {
                text: title
            },
            animationEnabled: true, // change to true
            exportEnabled: false, // If true a button will allow to export

            // graph to JPG file
            exportFileName: title,
            data: [{
                type : type,
                dataPoints : graphData
            }]
        });

        chart.render();

    }).catch(function(error) {
        console.log(error)
    });

};
