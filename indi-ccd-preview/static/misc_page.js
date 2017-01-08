var MiscPage = function(localsettings, indi) {
    this.localsettings = localsettings;
    this.indi = indi;
    MiscPage.SETTING_RUN_COMMAND='setting_run_command';

    this.run_command = function() {
        var command = $('#run-command').val();
        this.localsettings.set(MiscPage.SETTING_RUN_COMMAND, command);
        json_request('/run_command', {command: command}, {method: 'POST'});
    };

    this.reload_script_sequences = function() {
        $.ajax('/sequences', {success: function(d) {
            $('#script_sequences').empty().val(null);
            d['sequences'].forEach( function(seq) {
                $('#script_sequences').append($('<option />').val(seq['name']).text(seq['name']) );
            } );
        }});
    };

    this.continue_script_sequence = function() {
        sequence = $('#script_sequences').val();
        if(! sequence)
            return
        $.ajax('/sequence/' + sequence + '/continue', {method: 'POST'});
    };

    $('#shutdown-server').click(function() {
        $.ajax('/shutdown', {success: function(){
            notification('danger', 'Shutdown', 'Server is shutting down...');
        }});
    });

    $('#clean-cache').click(function() {
        $.ajax('/clean-cache', {success: function(data){
            level = data['files'] == 0 ? 'success' : 'warning';
            notification(level, 'Clean cache', 'Cache cleared, files remaining: ' + data['files'], {timeout: 5});
        }});
    });

    this.onDisplay = function() {
        if(this.localsettings.getJSON('misc_page_first_run', true) == true ) {
            var firstRunCompleted = function(){
                this.localsettings.setJSON('misc_page_first_run', false);
            };
            notification('info', 'Welcome', 'In this page you can find various utilities.' +
            '<ul><li><strong>Run command on server</strong>: executes any script or application on the server</li>' +
            '<li><strong>Script Sequences</strong>: this controls the INDI sequences bash script by writing the "confirmation" file needed to continue the shooting.</li>' +
            '<li><strong>Clean images cache</strong>: after each shot, images are still saved on server. Clicking this button will save all the space used for images cache.</li>' +
            '<li><strong>Shutdown INDI Previewer</strong>: shuts down this web server</li></ul>'
            , {on_closed: firstRunCompleted.bind(this) } );
        };
    };



    $('#script_sequences_refresh').click(this.reload_script_sequences.bind(this));
    $('#script_sequence_continue').click(this.continue_script_sequence.bind(this));
    $('#run-command-btn').click(this.run_command.bind(this));
    $('#run-command').val(localsettings.get(MiscPage.SETTING_RUN_COMMAND), '');
    this.reload_script_sequences();
};
