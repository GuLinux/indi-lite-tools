import { Button } from 'react-bootstrap'
import React from 'react';

export const CommitPendingValuesButton = ({property, pendingProperties, canUpdate, commitPendingValues, bsStyle, size}) => {
    if(!canUpdate)
        return null;
    return (
        <Button
            bsStyle={bsStyle}
            bsSize={size}
            disabled={Object.keys(pendingProperties).length === 0}
            onClick={e => commitPendingValues(property, pendingProperties)}
            >set</Button>
    )
}
