import React from 'react';
import CommitPendingValuesButton from './CommitPendingValuesButton'
import INDILight from './INDILight'
import PRINTJ from 'printj'

const sex2string = (format, value) => {
    // %010.6m
    // 0.0008388807046051948 => 0:00:03
    // 22.2061 => 22:12:22


    let formatSpecifiers = format.substring(1, format.indexOf('m')).split('.').map(x => parseInt(x));
    let width = formatSpecifiers[0];
    let fracSpecifier = formatSpecifiers[1];
    let fracBase;

    switch(fracSpecifier) {
        case 9:
            fracBase = 360000;
            break;
        case 8:
            fracBase = 36000;
            break;
        case 6:
            fracBase = 3600;
            break;
        case 5:
            fracBase = 600;
            break;
        default:
            fracBase = 60;
            break;
    }

    let isNegative = parseInt(value) < 0;
    console.log(`value: ${value}, format: ${format}, isNegative=${isNegative}, width=${width}, fracSpecifier=${fracSpecifier}, fracBase=${fracBase}`)

    return value;

//    value = Math.abs(value)
//
//
//    let intPartRound = Math.round(value * fracBase);
//    let remainder = intPartRound % fracBase
//    let intPart = Math.trunc(intPartRound / fracBase);
//    console.log(`intPartRound: ${intPartRound}, intPart: ${intPart}, remainder: ${remainder}`);
//    
//    return formatSpecifiers;
}

const formatValue = (value, displayValue) => {
    if(value.format.endsWith('m')) {
        return sex2string(value.format, displayValue);
    }
    let formatted = PRINTJ.sprintf(value.format, displayValue)
    return formatted;
}

const INDINumberProperty = ({device, property, isWriteable, pendingValues, displayValues, addPendingValues, commitPendingValues }) => (
    <div className="row">
        <div className="col-xs-1"><INDILight state={property.state} /></div> 
        <div className="col-xs-2">{property.label}</div> 
        <div className="col-xs-8">
            {property.values.map(value => (
                <div className="row" key={value.name} >
                    <div className="col-xs-2"><p>{value.label}</p></div>
                    <input
                        className="col-xs-10"
                        type="number"
                        min={value.min}
                        max={value.max}
                        step={value.step}
                        name={value.name}
                        value={formatValue(value, displayValues[value.name])}
                        onChange={e => addPendingValues(device, property, { [value.name]: parseFloat(e.target.value) })}
                        readOnly={!isWriteable}
                        />
                </div> 
            ))}
        </div>
        <div className="col-xs-1"><CommitPendingValuesButton bsStyle="primary" size="xsmall" device={device} isWriteable={isWriteable} pendingValues={pendingValues} commitPendingValues={commitPendingValues} property={property} /></div>
    </div>
)
 
export default INDINumberProperty
