import React from 'react' 
import { api } from './api'

import Nav from 'react-bootstrap/lib/Nav'
import NavItem from 'react-bootstrap/lib/NavItem'
import Form from 'react-bootstrap/lib/Form'
import FormGroup from 'react-bootstrap/lib/FormGroup'
import InputGroup from 'react-bootstrap/lib/InputGroup'
import FormControl from 'react-bootstrap/lib/FormControl'
import Button from 'react-bootstrap/lib/Button'
import LinkContainer from 'react-router-bootstrap/lib/LinkContainer'



class SessionPage extends React.Component {
    constructor(props) {
        super(props);
        this.sessionName = props.match.params.sessionName;
        this.state = { sequence_groups: [], newSequenceGroupName: '' }
        this.reload = this.reload.bind(this);
        this.setNewSequenceGroupName = this.setNewSequenceGroupName.bind(this);
        this.createSequenceGroup = this.createSequenceGroup.bind(this);
        this.sequenceGroups = this.sequenceGroups.bind(this);
    }

    componentDidMount() {
        this.reload()
    }

    render() {
        return (<div>
                <h3>{this.sessionName}</h3>
                <Form inline>
                    <FormGroup>
                        <InputGroup>
                            <FormControl type="text" value={this.state.newSequenceGroupName} onChange={this.setNewSequenceGroupName} />
                            <InputGroup.Button>
                                <Button onClick={this.createSequenceGroup}>New</Button>
                            </InputGroup.Button>
                        </InputGroup>
                    </FormGroup>
                </Form>
                <Nav bsStyle="pills" stacked >
                    { this.sequenceGroups() }
                </Nav>
            </div>
        );

    }

    sequenceGroups() {
        console.log(this.state.sequence_groups);
        return this.state.sequence_groups.map((sequenceGroup) => (
            <LinkContainer to={'/sessions/' + this.sessionName + '/' + sequenceGroup.name} key={sequenceGroup.name}>
                <NavItem>
                    <Button bsStyle='link' bsSize='sm' >&times;</Button> 
                    {sequenceGroup.name}
                </NavItem>
            </LinkContainer>
        ));
    }

    reload() {
        api.session(this.sessionName, (s) => { this.setState({sequence_groups: s.sequence_groups})  });
    }

    setNewSequenceGroupName(e) {
        console.log(e.target);
        this.setState({newSequenceGroupName: e.target.value});
    }

    createSequenceGroup() {
        api.createSequenceGroup(this.sessionName, this.state.newSequenceGroupName, this.reload);
    }
}

export default SessionPage;
