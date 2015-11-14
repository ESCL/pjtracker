/**
 * Created by kako on 10/11/15.
 *
 * A few utility functions to use promises so we don't need
 * jQuery nor callbacks.
 *
 */

function getCsrfToken() {
    // Get CSRF token, used by Django forms
    return document.cookie.match(/csrftoken=(\w+)/)[1];
}

function wait() {
    // Placeholder call used as dummy AJAX call
    return new Promise(function(resolve) {
        setTimeout(function() {
            resolve('done');
        }, 5000);
    });
}

function get(url, querystring) {
    return new Promise(function(resolve, reject) {
        // Open xhr and set headers
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url + "?" + querystring, true);

        // Handle onload, resolve on status 201, reject on others
        xhr.onload = function() {
            if (xhr.status == 200) {
                resolve(xhr.response);
            } else {
                reject(Error(xhr.statusText));
            }
        };

        // Right, network errors are possible as well...
        xhr.onerror = function() {
            reject(Error("Connection Error"))
        };

        // Finally, send the stuff
        xhr.send(null);
    });
}

function post(url, data, format, safe) {
    return new Promise(function(resolve, reject) {
        // Open xhr and set headers
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);

        // Set headers and format data if needed
        if (format == 'json') {
            xhr.setRequestHeader("Content-Type", "application/json");
            data = JSON.stringify(data);
        } else {
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        }
        if (safe) {
            xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
        }

        // Handle onload, resolve on status 201, reject on others
        xhr.onload = function() {
            if (xhr.status == 201) {
                resolve(xhr.response);
            } else {
                reject(Error(xhr.statusText));
            }
        };

        // Right, network errors are possible as well...
        xhr.onerror = function() {
            reject(Error("Connection Error"))
        };

        // Finally, send the stuff
        xhr.send(data);
    });
}