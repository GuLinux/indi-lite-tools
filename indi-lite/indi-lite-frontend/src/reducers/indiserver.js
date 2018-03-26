const defaultState = {
        state: {
        connected: false,
        host: '',
        port: '',
    },
    deviceEntities: {},
    devices: [],
    groups: {},
    properties: {},
    pendingProperties: [],
    messages: [],
};

const groupID = (device, group) => device.id + '/' + group;
const createGroup = (device, group) => ({name: group, id: groupID(device, group) });

const receivedServerState = (state, action) => {
    let nextState = {...state, state: {connected: action.state.connected, host: action.state.host, port: action.state.port.toString()}};
    if(! nextState.state.connected) {
        nextState.devices = [];
        nextState.deviceEntities = {}
        nextState.groups = [];
        nextState.properties = [];
        nextState.pendingProperties = [];
    }
    return nextState;
}

const arrayToObjectById = array => array.reduce( (obj, element) => ({...obj, [element.id]: element}), {});

const remapProperty = (property, device) => ({...property, group: groupID(device, property.group)})

const receivedDeviceProperties = (state, device, properties) => {

    let allGroups = arrayToObjectById(Object.keys(state.groups).filter(id => state.groups[id].device !== device.id).map(id => state.groups[id]));
    let allProperties = arrayToObjectById(Object.keys(state.properties).filter(id => state.properties[id].device !== device.id).map(id => state.properties[id]));

    let deviceGroups = properties.map(p => p.group);
    deviceGroups = deviceGroups.filter( (name, index) => index === deviceGroups.indexOf(name)).map(name => createGroup(device, name));
    let deviceProperties = properties.map(p => remapProperty(p, device));

    let deviceUpdated = {...state.deviceEntities[device.id], groups: deviceGroups.map(g => g.id), properties: deviceProperties.map(p => p.id)};

    allGroups = {...allGroups, ...arrayToObjectById(deviceGroups)};
    allProperties = {...allProperties, ...arrayToObjectById(deviceProperties)};

    return {...state, deviceEntities: {...state.deviceEntities, [deviceUpdated.id]: deviceUpdated}, groups: allGroups, properties: allProperties };
}

const indiPropertyUpdated = (state, property) => {
    let device = state.deviceEntities[property.device];
    return {...state, properties: {...state.properties, [property.id]: remapProperty(property, device) } }
};

const indiPropertyAdded = (state, property) => {
    let groups = state.groups;
    if(state.properties.filter(p => p.device === property.device && p.group === property.group).length === 0) {
        groups = [...groups, {name: property.group, device: property.device}];
    }
    return {...state, properties: [...state.properties, property], groups};
};

const indiPropertyRemoved = (state, property) => {
    let properties = state.properties.filter(p => !(p.name ===property.name && p.device === property.device && p.group === property.group));
    let groups = state.groups
    if(properties.filter(p => p.device === property.device && p.group === property.group).length === 0) {
        groups = groups.filter(g => !(g.name === property.group && g.device === property.device));
    }
    return {...state, properties, groups};    
};



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

const commitPendingProperties = (state, pendingProperties) => {
    // TODO: set status as busy
    return {...state, pendingProperties: []};
}

const deviceEntity = (device, groups=[], properties=[]) => ({...device, properties, groups, })

const receivedINDIDevices = (state, devices) => ({
    ...state,
    deviceEntities: arrayToObjectById(devices.map(d => ({...d, properties: [], groups: []}) )),
    devices: devices.map(d => d.id),
})

const indiserver = (state = defaultState, action) => {
    switch(action.type) {
        case 'RECEIVED_SERVER_STATE':
            return receivedServerState(state, action);
        case 'RECEIVED_INDI_DEVICES':
            return receivedINDIDevices(state, action.devices);
        case 'RECEIVED_DEVICE_PROPERTIES':
            return receivedDeviceProperties(state, action.device, action.properties)
        case 'ADD_PENDING_PROPERTIES':
            return addPendingProperties(state, action.pendingProperties);
        case 'COMMIT_PENDING_PROPERTIES':
            return commitPendingProperties(state, action.pendingProperties);
        case 'INDI_DEVICE_MESSAGE':
            return {...state, messages: [...state.messages, { device: action.device.id, message: action.message}]}
        case 'INDI_PROPERTY_UPDATED':
            return indiPropertyUpdated(state, action.property);
        case 'INDI_PROPERTY_ADDED':
            return indiPropertyAdded(state, action.property);
        case 'INDI_PROPERTY_REMOVED':
            return indiPropertyRemoved(state, action.property);
        case 'INDI_DEVICE_ADDED':
            return {...state, devices: [...state.devices, action.device]}
        case 'INDI_DEVICE_REMOVED':
            return {
                ...state,
                devices: state.devices.filter(d => d.name === action.device),
                groups: state.groups.filter(g => g.device === action.device),
                properties: state.properties.filter(p => p.device === action.device)
            }
        default:
            return state;
    }
}

export default indiserver;
