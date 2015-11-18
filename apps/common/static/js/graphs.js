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
 * Generate a simple graph, with one value per item
 *
 * options:
 *   - title: main title of the graph
 *   - type: type of graph [column, pie, area, bar, doughnut]
 *   - url: data endpoint, including querystring
 *   - labelField: name of the instance field that contains the label (x)
 *   - dataField: name of the instance field that contains the value (y)
 *   - theme (opt): theme to use (default to "theme1")
 *   - animate (opt): animate the graph? (default to false)
 *   - export (opt): allow exporting as file? (default to false)
 */

function generateGraph(options) {
    // Create graph container
    var divId = "div" + currentDiv;
    var graphs = document.createElement('div');
    graphs.id = divId;
    graphs.setAttribute('class', 'graph-div six columns');
    document.querySelector('#graphs').appendChild(graphs);
    currentDiv++;

    get(options.url).then(function(data) {
        // Parse response and setup order
        data = JSON.parse(data);
        var graphData = [], currentData;
        var order = options.order;

        // Generate data
        options.dataFields.forEach(function(dataField) {
            currentData = data.objects.map(function(obj) {
                return {
                    label: obj[options.labelField],
                    y: parseInt(obj[dataField.value])
                };
            });

            // Reverse if required
            if (order == -1 || order == 'desc') {
                currentData = currentData.reverse();
            }
            graphData.push({
                type: options.type,
                name: dataField.label,
                legendText: dataField.label,
                showInLegend: !!dataField.label,
                dataPoints: currentData
            });
        });


        // Create graph and attach to container
        var chart = new CanvasJS.Chart(
            divId,
            {
                title: {
                    text: options.title
                },
                toolTip: {
                    // Display shared tooltip if we have several several fields
                    shared: (options.dataFields.length > 1)
                },
                theme: options.theme || "theme1",
                animationEnabled: options.animate || false,
                exportEnabled: options.export || false,
                exportFileName: options.title,
                data: graphData
            }
        );

        // Render the graph
        chart.render();

    }).catch(function(error) {
        // Something failed, we don't care, just log it
        console.log(error)
    });
}