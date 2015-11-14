/**
 * Created by kako on 14/11/15.
 */

(function() {
    function selectChildren(wbs) {
        // Select all the children rows using their parent WBS
        var rows = Array.prototype.slice.call(document.querySelectorAll('.project-wbs .body'));
        return rows.filter(function(row) {return row.dataset.wbsCode.indexOf(wbs) != -1});
    }

    function updateChildren(ev) {
        // Update the parent wbs on all children
        if (ev.target.value == '') {
            return;
        }

        // Get WBS versions
        var oldWbs = ev.target.parentNode.parentNode.dataset.wbsCode;
        var parentWbs = ev.target.parentNode.querySelector('.parent-wbs').innerHTML;
        var newCode = ev.target.value;
        var newWbs = [parentWbs, newCode].filter(function(part){return !!part}).join('.');

        // Update dataset and text on all children
        var children = selectChildren(oldWbs);
        children.forEach(function(row) {
            row.dataset.wbsCode = row.dataset.wbsCode.replace(oldWbs, newWbs);
            row.querySelector('.parent-wbs').innerHTML = row.querySelector('.parent-wbs').innerHTML.replace(oldWbs, newWbs);
        });
    }

    function updateAll() {
        // Handle reset to update all values to default
        var inputs = Array.prototype.slice.call(wbsInputs);
        inputs.forEach(function(input) {
            if ("createEvent" in document) {
                // Update value manually, reset DOES NOT update it
                input.value = input.defaultValue;
                var evt = document.createEvent("HTMLEvents");
                evt.initEvent("change", false, true);
                input.dispatchEvent(evt);
            }
            else
                input.fireEvent("onchange");
        })
    }

    // Attach form reset listener
    var form = document.querySelector('form');
    form.addEventListener('reset', updateAll);

    // Attach wbs code input change listeners
    var wbsInputs = document.querySelectorAll('.wbs-code input');
    var input;
    for (var i = 0; i < wbsInputs.length; i++) {
        input = wbsInputs[i];
        input.addEventListener('change', updateChildren);
    }
})();