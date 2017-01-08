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

    $('#script_sequences_refresh').click(this.reload_script_sequences.bind(this));
    $('#script_sequence_continue').click(this.continue_script_sequence.bind(this));
    $('#run-command-btn').click(this.run_command.bind(this));
    $('#run-command').val(localsettings.get(MiscPage.SETTING_RUN_COMMAND), '');
    this.reload_script_sequences();
};
