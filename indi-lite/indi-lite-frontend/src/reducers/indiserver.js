const defaultState = {
    connected: false,
    host: '',
    port: '',
    devices: [],
    groups: [],
    properties: [],
    pendingProperties: [],
};

const receivedServerState = (state, action) => {
    let nextState = {...state, connected: action.state.connected, host: action.state.host, port: action.state.port.toString()};
    if(! nextState.connected) {
        nextState.devices = [];
        nextState.groups = [];
        nextState.properties = [];
        nextState.pendingProperties = [];
    }
    return nextState;
}

const remapProperties = (state, device, groups, properties) => {
    let nextStateProperties = state.properties.filter(property => property.device !== device);
    let nextStateGroups = state.groups.filter( group => group.device !== device);
    return {...state, groups: [...groups, ...nextStateGroups], properties: [...properties, ...nextStateProperties]};
}

const addPendingProperty = (state, pendingProperty) => {
    let isSamePendingProperty = (first, second) => {
        return first.device === second.device && first.group === second.group && first.name === second.name && first.valueName === second.valueName;
    }
    let pendingProperties = state.pendingProperties.filter(p => ! isSamePendingProperty(p, pendingProperty));
    if(pendingProperty.currentValue !== pendingProperty.newValue) {
        pendingProperties = [...pendingProperties, pendingProperty]
    }
    return {...state, pendingProperties};
}

const addPendingProperties = (state, pendingProperties) => {
    let newState = state;
    for(let p of pendingProperties) {
        newState = addPendingProperty(newState, p);
    }
    return newState;
}

const clearPendingProperties = state => ({...state, pendingProperties: []});

const indiserver = (state = defaultState, action) => {
    switch(action.type) {
        case 'RECEIVED_SERVER_STATE':
            return receivedServerState(state, action);
        case 'RECEIVED_INDI_DEVICES':
            return {...state, devices: action.devices};
        case 'RECEIVED_DEVICE_PROPERTIES':
            return remapProperties(state, action.device, action.groups, action.properties)
        case 'ADD_PENDING_PROPERTIES':
            return addPendingProperties(state, action.pendingProperties);
        case 'COMMITTED_PENDING_PROPERTIES':
            return clearPendingProperties(state);
        default:
            return state;
    }
}

export default indiserver;