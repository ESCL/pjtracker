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
 *   - dataFields: name of the instance fields that contains the values (y1, y2...)
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
        var graphData = [];
        var currentData;

        // Generate data
        var labelFieldParts, dataFieldValueParts;
        options.dataFields.forEach(function (dataField) {
            currentData = data.objects.map(function (obj) {
                labelFieldParts = options.labelField.split('.');
                dataFieldValueParts = dataField.value.split('.');
                var i;

                var label = obj[labelFieldParts[0]];
                for (i = 1; i < labelFieldParts.length; i++) {
                    label = label[labelFieldParts[i]];
                }

                var y = obj[dataFieldValueParts[0]];
                for (i = 1; i < dataFieldValueParts.length; i++) {
                    y = y[dataFieldValueParts[i]];
                }
                return {label: label, y: parseFloat(y)};
            });

            // Reverse if required
            if (options.order == -1 || options.order == 'desc') {
                currentData = currentData.reverse();
            }

            // Attach data setting name (and legend if enabled)
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
                    // Display shared tooltip if we have several fields
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
    });
}
