function render_events(events_array, total_time, actual_time, actual_station) {
    let event_percentage;
    let events_div = "";
    let bootstrap_color = "warning";
    let icon = "bell";
    let countdown_found = false;

    let countdown = $(".chrono > .labels > .countdown");

    events_array = $.grep(events_array, function (obj) {
        return ($.inArray(actual_station, obj.stations) >= 0)
    });

    // Order events array by time (t)
    events_array.sort(function (obj1, obj2) {
        return obj1.t - obj2.t;
    });

    $.each(events_array, function (i, item) {
        event_percentage = (item.t / total_time) * 100;
        events_div += '<div id="event_' + i + '" class="event" style="left: ' + event_percentage + '%">' +
                        '<i class="fa fa-' + icon + ' text-' + bootstrap_color + '"></i>\n' +
                        '<p><span class="label label-warning">' + item.message + '</span></p>\n' +
                        '</div>\n';

        if (item.is_countdown && item.t >= actual_time && !countdown_found) {
            countdown_found = true;
            countdown.html(item.message + " " + moment((item.t - actual_time) * 1000).format("mm:ss"));
        }


    });

    countdown.toggleClass("hidden", !countdown_found);

    return events_div;
}