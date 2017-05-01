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

class SessionsPage extends React.Component {
    constructor(props) {
        super(props)
        this.state = { sessions: [], newSessionName: ''};
        this.setNewSessionName = this.setNewSessionName.bind(this);
        this.createSession = this.createSession.bind(this);
        this.removeSession = this.removeSession.bind(this);
    }

    render() {
        return (<div>
                <Form inline>
                    <FormGroup>
                        <InputGroup>
                            <FormControl type="text" value={this.state.newSessionName} onChange={this.setNewSessionName} />
                            <InputGroup.Button>
                                <Button onClick={this.createSession}>New</Button>
                            </InputGroup.Button>
                        </InputGroup>
                    </FormGroup>
                </Form>
                <Nav bsStyle="pills" stacked >
                    { this.sessions() }
                </Nav>
            </div>
        );
    }

    componentDidMount() {
        this.loadSessions();
    }

    sessions() {
        return this.state.sessions.map((session) => (
            <LinkContainer to={'sessions/' + session} key={session}>
                <NavItem>
                    <Button bsStyle='link' bsSize='sm' onClick={this.removeSession.bind(this, session)}>&times;</Button> 
                    {session}
                </NavItem>
            </LinkContainer>
        ));
    }

    loadSessions() {
        console.log('x2: reloading sessions');
        api.sessions((r) => {
            console.log('sessions reloaded: ');
            console.log(r);
            this.setState( { sessions: r.sessions } );
        });
    }

    createSession() {
        api.addSession(this.state.newSessionName, () => { this.loadSessions() } );
    }

    removeSession(name) {
        api.removeSession(name, () => this.loadSessions() );
    }

    setNewSessionName(e) {
        this.setState( { newSessionName: e.target.value } );
    }
}

export default SessionsPage;
