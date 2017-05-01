import React from 'react' 
import SessionsPage from './sessions-page'
import SessionPage from './session-page'
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom'


class INDILiteApp extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route exact path='/' component={SessionsPage} />
                    <Route path='/sessions/:sessionName' component={SessionPage} />
                </div>
            </Router>
        )
    }
}

export default INDILiteApp;
