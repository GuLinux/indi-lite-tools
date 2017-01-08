var HistogramPage = function(localsettings, indi) {
    HistogramPage.SETTING_HISTOGRAM_BINS='setting_histogram_bins';
    HistogramPage.SETTING_HISTOGRAM_LOG='setting_histogram_log';
    HistogramPage.SETTING_HISTOGRAM_MODE='setting_histogram_mode';

    this.localsettings = localsettings;
    this.indi = indi;

    this.updateHistogramSettings = function() {
        var bins = parseInt($('#histogram-bins').val());
        var logarithmic = $('#histogram-logarithmic').prop('checked')
        var mode = $('#histogram-mode').val();
        this.localsettings.set(HistogramPage.SETTING_HISTOGRAM_BINS, bins);
        this.localsettings.set(HistogramPage.SETTING_HISTOGRAM_LOG, logarithmic);
        this.localsettings.set(HistogramPage.SETTING_HISTOGRAM_MODE, mode);
        json_request('/histogram/settings', {bins: bins, logarithmic: logarithmic, absolute: (mode == 'absolute')});
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
        if(this.chart !== undefined) {
            this.chart.destroy();
        }
        this.chart = new Chart(ctx, {
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
    };

    this.onDisplay = function() {
        if(this.localsettings.getJSON('histogram_page_first_run', true) == true ) {
            var firstRunCompleted = function(){
                this.localsettings.setJSON('histogram_page_first_run', false);
            };
            notification('info', 'Welcome', 'This is the Histogram page.<br>When an image is taken in the "Preview" page, an histogram will be plotted here, according to the configured settings.<br>' +
            'Current settings are: ' +
            '<ul><li><strong>Bins</strong>: how many bins to use when plotting the histogram</li>' +
            '<li><strong>Mode</strong>: histogram calculation mode. <i>Relative</i> will use the minimum and maximum pixel value, while <i>Absolute</i> will use the bit depth reported by the camera.</li>' +
            '<li><strong>Logarithmic</strong>: plot histogram using logarithmic scale for the y axis.</li></ul>' +
            'Settings will be used after the next image is shot.'
            , {on_closed: firstRunCompleted.bind(this) } );
        };
    };


    $('#histogram-update-settings').click(this.updateHistogramSettings.bind(this));
    /*
    $('#histogram-image').click(function() {
        $('#histogram-image').toggleClass('img-responsive');
    });
    */
    $('#histogram-bins').val(this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_BINS, 256));
    $('#histogram-mode').val(this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_MODE, 'relative'));
    $('#histogram-logarithmic').prop('checked', this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_LOG, 'true') == 'true');

    this.updateHistogramSettings();

};
