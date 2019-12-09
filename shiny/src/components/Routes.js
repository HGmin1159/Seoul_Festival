import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import FestivalDetail from '../pages/FestivalDetail';
import Home from '../pages/Home';

export default () => (
    <Router>
        <Route path="/" component={Home} exact />
        <Route path="/shiny/" component={Home} exact />
        <Route path="/p/:festival" component={FestivalDetail} exact />
        <Route path="/shiny/p/:festival" component={FestivalDetail} exact />
    </Router>
)