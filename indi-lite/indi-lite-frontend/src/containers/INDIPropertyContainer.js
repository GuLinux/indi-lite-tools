import { connect } from 'react-redux'
import INDISwitchProperty from '../components/INDISwitchProperty'
import INDILightProperty from '../components/INDILightProperty'
import INDITextProperty from '../components/INDITextProperty'
import INDINumberProperty from '../components/INDINumberProperty'
import Actions from '../actions'


const mapStateToProps = (state, ownProps) => {
    let device = ownProps.device;
    let group = ownProps.group;
    let property = ownProps.property;
    return {
        device, 
        group,
        property,
        pendingProperties: state.indiserver.pendingProperties
    }
}

const mapDispatchToProps = dispatch => ({
    addPendingProperties: (pendingProperties, autoApply) => dispatch(Actions.INDIServer.addPendingProperties(pendingProperties, autoApply)),
    commitPendingProperties: (pendingProperties) => dispatch(Actions.INDIServer.commitPendingProperties(pendingProperties)),
})

export const INDILightPropertyContainer = connect(mapStateToProps, mapDispatchToProps)(INDILightProperty)
export const INDISwitchPropertyContainer = connect(mapStateToProps, mapDispatchToProps)(INDISwitchProperty)
export const INDINumberPropertyContainer = connect(mapStateToProps, mapDispatchToProps)(INDINumberProperty)
export const INDITextPropertyContainer = connect(mapStateToProps, mapDispatchToProps)(INDITextProperty)


