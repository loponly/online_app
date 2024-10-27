import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import BusinessDashboard from './components/BusinessDashboard';
import ProjectManagement from './components/ProjectManagement';
import StudentTracking from './components/StudentTracking';

function App() {
    return (
        <Router>
            <Switch>
                <Route path="/business-dashboard" component={BusinessDashboard} />
                <Route path="/project-management" component={ProjectManagement} />
                <Route path="/student-tracking" component={StudentTracking} />
            </Switch>
        </Router>
    );
}

export default App;
