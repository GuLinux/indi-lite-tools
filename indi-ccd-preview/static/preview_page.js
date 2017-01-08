this.PreviewPage = function(localsettings, indi) {
    this.localsettings = localsettings;
    this.indi = indi;
    PreviewPage.SETTING_EXPOSURE='setting_exposure';

    this.setImage = function(url) {
        $('#ccd-preview-image').attr('src', url);
    };

    this.preview = function() {
        this.set_exposure();
        current_indi_device().preview(this.exposure());
    };

    this.framing = function() {
        this.set_exposure();
        current_indi_device().framing(this.exposure());
        $('#framing').hide();
        $('#stop-framing').show();

    };

    this.stop_framing = function() {
        current_indi_device().stop_framing();
        $('#framing').show();
        $('#stop-framing').hide();
    }

    this.exposure = function() {
        return this.localsettings.get(PreviewPage.SETTING_EXPOSURE, 1);
    };

    this.set_exposure = function(value) {
        if(value === undefined)
            value = $('#exposure').val();
        this.localsettings.set(PreviewPage.SETTING_EXPOSURE, value);
        $('#exposure').val(this.exposure());
    };

    this.onDisplay = function() {
        if(this.localsettings.getJSON('preview_page_first_run', true) == true ) {
            var firstRunCompleted = function(){
                this.localsettings.setJSON('preview_page_first_run', false);
            };
            var showSecondMessage = function() {
                notification('info', 'Welcome', 'The page is responsive. By default image will be zoomed out to fit the page, if bigger. This will help visualization on mobile devices.<br>To view the image on its <strong>full size</strong>, simply click on it.', {on_closed: firstRunCompleted.bind(this) });
            };
            notification('info', 'Welcome', 'This is the INDI CCD Preview page.<br>Setting the exposure (in seconds) and clicking "Preview" will trigger an exposure that will be shown in this page.<br>The "Framing" button will continuously shoot, until you click the "Stop Framing" button.', {on_closed: showSecondMessage.bind(this) });
        };
    };


    $('#ccd-preview-image').click(function() {
        $('#ccd-preview-image').toggleClass('img-responsive');
    });

    this.set_exposure(this.exposure());
    $('#preview').click(this.preview.bind(this));
    $('#framing').click(this.framing.bind(this));
    $('#stop-framing').click(this.stop_framing.bind(this));
    $('#stop-framing').hide();

};
