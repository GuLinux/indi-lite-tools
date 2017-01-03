var HistogramPage = function(localsettings, indi) {
    HistogramPage.SETTING_HISTOGRAM_BINS='setting_histogram_bins';
    HistogramPage.SETTING_HISTOGRAM_LOG='setting_histogram_log';

    this.localsettings = localsettings;
    this.indi = indi;

    this.updateHistogramSettings = function() {
        var bins = parseInt($('#histogram-bins').val());
        var logarithmic = $('#histogram-logarithmic').prop('checked')
        this.localsettings.set(HistogramPage.SETTING_HISTOGRAM_BINS, bins);
        this.localsettings.set(HistogramPage.SETTING_HISTOGRAM_LOG, logarithmic);
        $.ajax('/histogram', {method: 'PUT', data: {bins: bins, logarithmic: logarithmic} });
    };

    this.setImage = function(url) {
        $('#histogram-image').attr('src', url);
    };

    this.setData = function(data, bins) {
        var is_logarithmic = this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_LOG, true) == 'true';
        var ctx = document.getElementById('histogram-plot').getContext('2d');
        var bins_labels = bins.filter( function(x) { return x > 0; }).map(function(x, i, a) {
            var prev = i == 0 ? 0 : a[i-1];
            return 'from ' + Number(prev).toFixed(1) + ' to ' + Number(x).toFixed(1);
        });
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: bins_labels,
                datasets: [{
                    label: "histogram",
                    data: data
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        type: is_logarithmic ? 'logarithmic' : 'linear'
                    }]
                }
            }
        });
/*
        var mapped = data.map(function(item, index){
            return { x: index, y: item};
        });

        var chart = new CanvasJS.Chart("histogram-plot", {
            title: { text: "Histogram Data" },
            axisY: {logarithmic: is_logarithmic},
            data: [ {
                type: "area",
                dataPoints: mapped
            }]
        });  
    chart.render();
*/
    };



    $('#histogram-update-settings').click(this.updateHistogramSettings.bind(this));
    /*
    $('#histogram-image').click(function() {
        $('#histogram-image').toggleClass('img-responsive');
    });
    */
    $('#histogram-bins').val(this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_BINS, 256));
    $('#histogram-logarithmic').prop('checked', this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_LOG, 'true') == 'true');

    this.updateHistogramSettings();

};
