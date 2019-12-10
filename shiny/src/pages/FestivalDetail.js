import React, { useState } from 'react';
import fes from '../2019.json';
import FullWidthTabs from '../components/FullWidthTabs';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';


const FestivalDetail = ({ match }) => {
    const [res, setRes] = useState([]);
    
    const fe = JSON.parse(match.params.festival);
    
    Shiny.addCustomMessageHandler("1", res => {
        setRes(res);
    });
    
    Shiny.onInputChange("fesid", fe.id);

    const theme = createMuiTheme({
        palette: {
            primary: {
                main: '#8ebdd8',
                contrastText: 'white'
            }
        },
    });

    return (
        (res)
        &&
        <ThemeProvider theme={theme}>
            <FullWidthTabs fe={fe} res={res} fes={fes}></FullWidthTabs>
        </ThemeProvider>
    )
}

export default FestivalDetail;