/**
 * Created by kako on 05/11/15.
 */


var FilterMultiSelect = function(field) {
    this.field = field;

    this.createElements = function() {
        // Create all the elements required to make this work
        this.filters = {
            available: document.createElement('input'),
            selected: document.createElement('input')
        };
        this.selects = {
            available: document.createElement('select'),
            selected: document.createElement('select')
        };
        this.button = document.createElement('button');

        // Create main container to hold all the elements
        this.container = document.createElement('div');
        this.container.setAttribute('class', 'row');

        // Create and append containers for the elements
        this.container.appendChild(this.createSelectContainer(this.filters.available, this.selects.available, 'Available'));
        this.container.appendChild(this.createButtonContainer(this.button));
        this.container.appendChild(this.createSelectContainer(this.filters.selected, this.selects.selected, 'Selected'));
    };

    this.createButtonContainer = function(button) {
        // Crete a container with an action button
        var container = document.createElement('div');
        container.setAttribute('class', 'two columns');
        button.setAttribute('class', 'u-full-width multiselect-button');
        button.setAttribute('title', 'Swap the selected elements in either list');
        button.type = 'button';
        button.innerHTML = 'Update';
        container.appendChild(button);
        return container;
    };

    this.createSelectContainer = function(filter, select, title) {
        // Create a container with the given select element and a filter for it
        var container = document.createElement('div');
        container.setAttribute('class', 'five columns');
        var label = document.createElement('span');
        label.setAttribute('class', 'multiselect-title');
        label.innerHTML = title;
        container.appendChild(label);
        filter.type = 'text';
        filter.setAttribute('class', 'u-full-width');
        container.appendChild(filter);
        select.setAttribute('class', 'u-full-width');
        select.setAttribute('multiple', '');
        container.appendChild(select);
        return container;
    };

    this.createOption = function(option) {
        // Create an option element to use in selects
        var opt = document.createElement('option');
        opt.value = option.value;
        opt.text = option.text;
        opt.dataset.selected = option.selected;
        return opt;
    };

    this.refreshWidgets = function() {
        // Update the values in all selects with the current values (also reset filters)
        this.selects.available.innerHTML = '';
        this.selects.selected.innerHTML = '';
        this.filters.available.value = '';
        this.filters.selected.value = '';
        var opt;
        var opts = this.field.querySelectorAll('option');
        for (var i = 0; i < opts.length; i++) {
            opt = opts[i];
            var newOpt = this.createOption(opt);
            if (opt.selected) {
                this.selects.selected.appendChild(newOpt);
            } else {
                this.selects.available.appendChild(newOpt);
            }
        }
    };

    this.filterOptions = function(ev, select) {
        // Filter the options in a select
        var text = ev.currentTarget.value.toLowerCase();
        var opts = select.querySelectorAll('option');
        var opt;
        for (var i = 0; i < opts.length; i++) {
            opt = opts[i];
            if (opt.text.toLowerCase().indexOf(text) === -1) {
                opt.setAttribute('style', 'display: none;');
            } else {
                opt.setAttribute('style', 'display: block;');
            }
        }
    };

    this.updateSelected = function() {
        // Update the selected values in the real field
        var options, option, i;

        // First add all the ones that are selected in the available options
        options  = this.selects.available.querySelectorAll('option');
        for (i = 0; i < options.length; i++) {
            option = options[i];
            if (option.selected) {
                this.field.querySelector('option[value="' + option.value + '"]').selected = true;
            }
        }

        // Now remove all the ones that are selected in the selected options
        // Note: that sounds weird, but that selection implies the user want those
        // to move to the available ones, aka "unselect them"
        options  = this.selects.selected.querySelectorAll('option');
        for (i = 0; i < options.length; i++) {
            option = options[i];
            if (option.selected) {
                this.field.querySelector('option[value="' + option.value + '"]').selected = false;
            }
        }

        // Refresh both select widgets using the real field data
        this.refreshWidgets();
    };

    this.start = function() {
        var this_ = this;

        if (this.field.disabled || this.field.getAttribute('readonly')) {
            // Field is disabled, don't even bother
            return;
        }

        // Create all elements and populate magic multi-selects
        this.createElements();
        this.refreshWidgets();

        // Hide real multi-select field and append magic ones
        this.field.parentNode.insertBefore(this.container, this.field.nextSibling);
        this.field.setAttribute('style', 'display: none;');

        // Add event listener for button (update selected values)
        this.button.addEventListener('click', this_.updateSelected.bind(this));

        // Add event listener for filters (filter the selects) as user types
        this.filters.available.addEventListener(
            'keyup',
            function(ev) {this_.filterOptions(ev, this_.selects.available);}
        );
        this.filters.selected.addEventListener(
            'keyup',
            function(ev) {this_.filterOptions(ev, this_.selects.selected);}
        );
    };

    return this;
};
