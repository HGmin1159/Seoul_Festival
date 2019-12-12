import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Form from './Form';
import Link from 'next/link';
import MenuIcon from '@material-ui/icons/Menu';


const useStyles = makeStyles({
    list: {
        width: "67vmin",
        maxWidth: "300px"
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
            <Form></Form>
            <Divider />
            <p>찾는 축제 목록</p>
            <List>
                {fes.map((fes) => (

                    <ListItem button key={fes.id}>
                        <Link href="/p/[id]" as={`/p/${encodeURI(
                            JSON.stringify({
                                id: fes.id,
                                name: fes.name,
                                x: fes.x,
                                y: fes.y,
                                cluster: fes.cluster,
                                man: fes.man,
                                exp: fes.explanation.replace(/(\\(n|t))/g, '').replace(/\/{1}/g, 'escapeSlash'),
                                region: fes.개최지역,
                                place: fes.축제장소
                        }))}`}>
                            <a>
                                <ListItemIcon>
                                    <img src={`/img/${fes.id}.jpg`}></img>
                                </ListItemIcon>
                                <ListItemText primary={fes.name} />
                                <span>{fes.period}</span>
                            </a>
                        </Link>
                    </ListItem>

                ))}
            </List>
            <style jsx>{`
                img {
                    width: 50vmin;
                    max-width: 256px;
                    height: 50vmin;
                    max-height: 256px;
                }
                a {
                    text-decoration: none;
                    color: black;
                    cursor: pointer;
                    background-color: #f9f9f9;
                    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                    width: 50vmin;
                    padding: 4px 4px;
                }
                p {
                    margin: 4%;
                }
            `}</style>

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
