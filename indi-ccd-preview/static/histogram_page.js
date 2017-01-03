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



    $('#histogram-update-settings').click(this.updateHistogramSettings.bind(this));
    $('#histogram-image').click(function() {
        $('#histogram-image').toggleClass('img-responsive');
    });

    $('#histogram-bins').val(this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_BINS, 256));
    $('#histogram-logarithmic').prop('checked', this.localsettings.get(HistogramPage.SETTING_HISTOGRAM_LOG, 'true') == 'true');

    this.updateHistogramSettings();

};
