import Ajax from './ajax'

class API {
    sessions(on_success, on_failure) {
        this._getResource('/api/sessions', on_success, on_failure);
    }

    addSession(name, on_success, on_failure) {
        this._editResource('/api/sessions/' + name, {}, 'POST', 201, on_success, on_failure);
    }


    removeSession(name, on_success, on_failure) {
        this._editResource('/api/sessions/' + name, {}, 'DELETE', 200, on_success, on_failure);
    }

    session(name, on_success) {
        this._getResource('/api/sessions/' + name, on_success);
    }

    createSequenceGroup(session, sequenceGroup, on_success, on_failure) {
        this._editResource('/api/sessions/' + session + '/' + sequenceGroup, {}, 'POST', 201, on_success, on_failure);
    }

    _getResource(url, on_success, on_failure) {
        Ajax.fetch( url ).then(Ajax.decode_json({
            is_success: (r) => r.status == 200,
            success: on_success,
            failure: on_failure
        }));
    }

    _editResource(url, payload, method, expected_state, on_success, on_failure) {
        Ajax.send_json(url, payload, method).then((r) => {
            if(r.status == expected_state) {
                on_success(r);
            } else {
                on_failure(r);
            }
        });
    }
}

export default API;
export let api = new API();
