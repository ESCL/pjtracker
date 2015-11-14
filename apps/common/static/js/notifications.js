/**
 * Created by kako on 14/11/15.
 */
(function() {
    var dismissButtons = document.querySelectorAll('#notifications .notification a[data-action="dismiss"]');
    var btn;
    for (var i = 0; i < dismissButtons.length; i++) {

        btn = dismissButtons[i];
        btn.addEventListener('click', function (ev) {
            var id = ev.target.dataset.id;
            var url = "/notifications/api/v0/notifications/" + id + '/actions/';
            var posted = post(url, {'name': 'dismiss'}, 'json');
            posted.then(
                function () {
                    ev.target.parentNode.classList.add('disabled');
                }
            );
            posted.catch(
                function (error) {
                    console.log(error)
                }
            );
        })
    }
})();
