import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import MenuIcon from '@material-ui/icons/Menu';
import FestivalList from './FestivalList';

const useStyles = makeStyles({
    list: {
        width: "67vmin",
        maxWidth: "300px",
        minWidth: "256px"
    },
    btn: {
        zIndex: 2,
    },
    menu: {
        // color: 'rgba(0, 0, 0, 0.87)',
        // backgroundColor: '#f5f5f5',
        flexGrow: 0.1,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        cursor: 'pointer',
    }
});

export default function TemporaryDrawer({ fes, isWide }) {
    const classes = useStyles();
    const [state, setState] = React.useState({
        left: false
    });
    const [] = React.useState('');

    const toggleDrawer = (side, open) => event => {
        if (event.type === 'keydown' && event.key !== 'Escape') {
            return;
        }

        setState({ ...state, [side]: open });
    };

    const sideList = side => (
        <div
            className={classes.list}
            onKeyDown={toggleDrawer(side, false)}
        >
            <FestivalList fes={fes} />
        </div>
    );

    return (
        <div className={classes.menu}>
            <MenuIcon onClick={toggleDrawer('left', true)} className={classes.btn} visibility={isWide? 'hidden':'visible'}/>

            <Drawer open={state.left} onClose={toggleDrawer('left', false)}>
                {sideList('left')}
            </Drawer>
        </div>
    );
}
