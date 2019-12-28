import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Restaurant from './Restaurant';
import dynamic from 'next/dynamic';
import TemporaryDrawer from './TemporaryDrawer';
import BarChart from './BarChart';
import clt from '../clt_labels.json';
import Pie from './Pie';
import FestivalList from './FestivalList';

const LeafMap = dynamic(
    () => import('./LeafMap'),
    {
        ssr: false
    }
)

function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <Typography
            component="div"
            role="tabpanel"
            hidden={value !== index}
            id={`full-width-tabpanel-${index}`}
            aria-labelledby={`full-width-tab-${index}`}
            {...other}
        >
            {children}
        </Typography>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
};

function a11yProps(index) {
    return {
        id: `full-width-tab-${index}`,
        'aria-controls': `full-width-tabpanel-${index}`,
    };
}

export default function FullWidthTabs({ fe, res, fes }) {
    const [orientation, setOrientation] = useState(1);
    const [disabled, setDisabled] = useState(false);
    const [isWide, setIsWide] = useState(false);
    const [open, setOpen] = useState(null);

    const [height, setHeight] = useState(null)
    const [width, setWidth] = useState(null)
    if (process.browser) {
        useEffect(() => setHeight(window.innerHeight), [
            window.innerHeight
        ])
        useEffect(() => setWidth(window.innerWidth), [
            window.innerWidth
        ])
    }

    const resizeHandler = () => {
        setOrientation(window.innerWidth < window.innerHeight);
        setIsWide(window.innerWidth > 1024);
    }

    useEffect(() => {
        window.addEventListener('resize', resizeHandler);
        resizeHandler();
        return function cleanup() {
            window.removeEventListener('resize', resizeHandler);
        };
    }, [])

    useEffect(()=>{
        setOpen(null)
    }, [fe])

    const useStyles = makeStyles(() => ({
        root: {
            backgroundColor: 'primary',
            width: '100vw',
        },
        root2: {
            flexDirection: 'row',
            position: 'sticky',
            top: 0
        },
        tabs: {
            flexGrow: 0.9
        },
        panel: {
            overflowY: 'auto',
            height: height-58,
            width: '100%'
        }
    }));

    const classes = useStyles();
    const theme = useTheme();
    const [value, setValue] = useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const handleChangeIndex = index => {
        setValue(index);
    };

    return (
        <div className={classes.root}>
            <AppBar position="static" color="default" className={classes.root2}>
                <TemporaryDrawer fes={fes} isWide={isWide} height={height}></TemporaryDrawer>
                <Tabs
                    value={value}
                    onChange={handleChange}
                    indicatorColor="primary"
                    variant="fullWidth"
                    aria-label="full width tabs"
                    className={classes.tabs}
                >
                    <Tab label="축제정보" {...a11yProps(0)} />
                    <Tab label="지도" {...a11yProps(1)} />
                </Tabs>
            </AppBar>
            <div className="view-container">
                <div className="fest-list">
                    <FestivalList fes={fes}/>
                </div>
                <SwipeableViews
                    axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
                    index={value}
                    onChangeIndex={handleChangeIndex}
                    className={classes.panel}
                    disabled={disabled}
                >
                    <TabPanel value={value} index={0} dir={theme.direction} >
                        <div className="gridContainer1">
                            <img className="info-img" src={`/img/${fe.id}.jpg`}></img>
                            <div className="info">
                                <p className="info-text info-title">{fe.name}</p>
                                <p className="info-text text1">개최지역: {fe.region}</p>
                                <p className="info-text text2">축제장소: {fe.place}</p>
                                <p className="info-text link">누리집: <a href={fe.link}>{fe.link}</a></p>
                                <p className="info-text text3">{fe.exp}</p>
                            </div>
                            <div className="bar">
                                <BarChart data={clt[fe.cluster.toString()]} />
                            </div>
                            <div className="pie">
                                <Pie man={fe.man} />
                            </div>
                        </div>
                    </TabPanel>
                    <TabPanel value={value} index={1} dir={theme.direction}>
                        <div className="gridContainer">
                            <LeafMap fes={fe} res={res} key={value === 1} invalidate={value === 1} preventSwipe={(b)=>setDisabled(b)} open={open} />
                            <div className="scroll">
                                <ul className="ul">
                                    {res.map(res =>
                                        <li className="info-li" key={res.id} onClick={()=>setOpen(res.id)}>
                                            <Restaurant res={res}></Restaurant>
                                        </li>
                                    )}
                                </ul>
                                <footer>
                                    <div>
                                        Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from
                                    <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
                                    </div>
                                </footer>
                            </div>
                        </div>
                    </TabPanel>
                </SwipeableViews>
            </div>
            <style jsx global>{`
                body {
                    padding: 0;
                    margin: 0;
                }
                html, body {
                    height: 100vh;
                    width: 100vw;
                }
            `}</style>
            <style jsx>{`
                .gridContainer1 {
                    display: grid;
                    grid-template-rows: ${isWide || !orientation? 'auto minmax(256px,'+ Math.min((width-300*isWide)/2, height-58) +'px)':'auto auto minmax(256px,100vmin) minmax(256px,100vmin)'};
                    grid-template-columns: ${isWide || !orientation? '1fr 1fr':'100%'};
                }
                .info {
                    ${isWide || !orientation? 'grid-row: 1/2; grid-column: 2/3':''}
                }
                .bar {
                    position: relative;
                    width: 90%;
                    margin: 10px auto;
                }
                .pie {
                    position: relative;
                    width: 90%;
                    margin: 10px auto;
                    ${isWide || !orientation? 'grid-column: 2/3;':''}
                }
                .gridContainer {
                    display: grid;
                    grid-auto-columns: 100%;
                    width: 90%; margin: 10px auto;
                    ${orientation || height > 500 ? 'grid-template-rows: 1fr 1fr;':'grid-template-rows: minmax(256px, 1fr);'}
                    height: ${height - 78}px;
                }
                .ul {
                    padding-inline-start: 0;
                    padding-inline-end: 0;
                }
                .scroll {
                    overflow: auto;
                    height: 50vh;
                }
                .info-img {
                    ${isWide || !orientation? 'grid-row: 1/2; grid-column: 1/2;':''}
                    display: block;
                    width: 90%;
                    border: solid;
                    margin: 10px auto;
                }
                .info-text.info-title {
                    font-size: 1.5rem;
                    font-weight: 500;
                }
                .info-text {
                    display: block;
                    width: 86%;
                    margin: 10px auto;
                }
                .info-text.text1 {
                }
                .info-text.text2 {
                }
                .info-text.text3 {
                }
                .info-text.link {
                    text-overflow: ellipsis;
                    overflow: hidden;
                }
                .info-li {
                    list-style-type: none;
                    font-family: sans-serif;
                    color: rgba(0, 0, 0, 0.87);
                    margin: auto 0;
                    border-bottom: 1px solid #fbe4d4;
                }
                .info-li:hover {
                    background-color: rgba(245, 132, 84, 0.5);
                }
                ul {
                    display: ${orientation || height > 500 ? 'block' : 'none'};
                }
                footer {
                    font-size: 0.8rem;
                    margin: 1vw;
                }
                .fest-list {
                    max-width: 300px;
                    overflow-y: auto;
                    height: ${height-58}px;
                    ${isWide? '':'display: none;'}
                }
                .view-container {
                    display: ${isWide? 'grid':''};
                    justify-content: center;
                    justify-items: center;
                    grid-template-columns: auto 1fr;
                    grid-gap: 10px;
                }
            `}</style>
        </div>
    );
}
