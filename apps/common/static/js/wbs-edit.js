/**
 * Created by kako on 14/11/15.
 */

(function() {
    function addActivity(ev) {
        // Add a new activity form

        // First prevent event default and clone the first row
        ev.preventDefault();
        var prevSibling;
        var parentWbs;
        var oldNum;
        var newNum = allRows.length + 1;
        var row = allRows[0].cloneNode(true);

        // Update field names and reset their values
        var inputs = Array.prototype.slice.call(row.getElementsByTagName('input'));
        inputs = inputs.concat(Array.prototype.slice.call(row.getElementsByTagName('select')));
        inputs.forEach(function(input) {
            oldNum = input.name.split('-')[1];
            input.id = input.id.replace(oldNum, newNum);
            input.name = input.name.replace(oldNum, newNum);
            input.value = '';
        });

        // Determine wbs and location to append
        if (ev.target.dataset.action == 'add-sub-activity') {
            var parentRow = getRow(ev.target);
            var children = toggleChildren(null, parentRow, false);
            parentWbs = parentRow.dataset.wbs;
            if (children.length) {
                prevSibling = children[children.length - 1];
            } else {
                prevSibling = parentRow;
            }

        } else if (ev.target.dataset.action == 'add-activity') {
            parentWbs = '';
            prevSibling = ev.target.previousSibling;
        }

        // Set wbs attributes
        row.dataset.parentWbs = parentWbs;
        row.getElementsByTagName('span')[0].innerHTML = row.dataset.parentWbs;
        var code = row.getElementsByTagName('input')[0].value;
        row.dataset.wbs = [row.dataset.parentWbs, code].filter(function(part){return !!part}).join('.');
        row.dataset.new = true;

        // Init and append to its siblings
        initRow(row);
        prevSibling.parentNode.insertBefore(row, prevSibling.nextSibling);
    }

    function getRow(el) {
        // Get the parent "row" of the current element

        while (!el.classList.contains('row')) {
            el = el.parentNode;
        }
        return el;
    }

    function selectChildren(wbs, excludeRow) {
        // Select all the children rows using their parent WBS

        var qs ='div[data-parent-wbs="' + wbs + '"]';
        return Array.prototype.slice.call(document.querySelectorAll(qs));
    }

    function setAddSubAction(row) {
        // Enable "add subactivity" button if row has wbs code, disable otherwise

        var input = row.querySelector('.wbs-code input');
        var btn = row.querySelector('a[data-action="add-sub-activity"]');

        if (input.value == '') {
            btn.removeEventListener('click', addActivity);
            btn.classList.add('disabled');

        } else {
            btn.classList.remove('disabled');
            btn.addEventListener('click', addActivity);
        }
    }

    function setToggleAction(row) {
        // Enable toggle button if row has children, disable otherwise

        var btn = row.querySelector('a[data-action="toggle-children"]');
        var children = selectChildren(row.dataset.wbs, true);
        if (children.length == 0) {
            btn.removeEventListener('click', toggleChildren);
            btn.classList.add('disabled');
        } else {
            btn.addEventListener('click', toggleChildren);
            btn.classList.remove('disabled');
        }
    }

    function setRowVisibility(row) {
        // Hide by default if it's not main
        if (row.dataset.parentWbs != '') {
            row.classList.add('hidden');
        }
    }

    function toggleChildren(ev, row, hide) {
        // Toggle visibility of children rows, hiding them recursively
        // and displaying the first-level children

        if (ev) {
            // Base case, user clicked
            ev.preventDefault();
            row = getRow(ev.target);
        }

        // Get children and set "hide" if necessary
        var children = selectChildren(row.dataset.wbs);
        if (ev && children.length) {
            hide = !(children[0].classList.contains('hidden'));
        }

        // Loop and do whatever must be done
        if (hide) {
            // Hide, do it recursively
            children.forEach(function(subRow) {
                subRow.classList.add('hidden');
                toggleChildren(null, subRow, hide);
            })

        } else {
            // Display, only first-level children
            children.forEach(function(subRow) {
                subRow.classList.remove('hidden');
            })
        }
        return children;
    }

    function updateWbs(ev, row, newParentWbs) {
        // Update wbs info on all children, recursively

        if (ev) {
            // Base case, event, if it has a value get the row
            row = getRow(ev.target);
            setAddSubAction(row);
            if (ev.target.value == '') {
                return;
            }

        } else {
            // Recursion, update using parent data
            row.dataset.parentWbs = newParentWbs;
            row.getElementsByTagName('span')[0].innerHTML = row.dataset.parentWbs;
        }

        // Store old wbs and update it
        var code = row.getElementsByTagName('input')[0].value;
        var oldWbs = row.dataset.wbs;
        row.dataset.wbs = [row.dataset.parentWbs, code].filter(function(part){return !!part}).join('.');

        // Now update all children (fetch with old, update to new)
        // NOTE: new rows have  no children (their wbs is incomplete)
        if (oldWbs != row.dataset.parentWbs) {
            var children = selectChildren(oldWbs, row);
            children.forEach(function(subRow) {
                updateWbs(null, subRow, row.dataset.wbs);
            });
        }


    }

    function initRow(row) {
        // Add wbs change listener and set actions for buttons (enable/disable)

        var wbsInput = row.querySelector('.wbs-code input');
        wbsInput.addEventListener('change', updateWbs);
        setToggleAction(row);
        setAddSubAction(row);
    }

    // Get main elements to attach listeners
    var addButton = document.querySelector('button[data-action="add-activity"]');
    var allRows = document.querySelectorAll('.project-wbs .body.row');
    var row, i;

    // Attach form reset and submit listener
    addButton.addEventListener('click', addActivity);

    // Attach toggle children event listeners
    for (i = 0; i < allRows.length; i++) {
        row = allRows[i];
        initRow(row);
        setRowVisibility(row);
    }
})();