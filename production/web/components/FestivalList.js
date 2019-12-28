import React, { useState } from 'react';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Form from './Form';
import Link from 'next/link';
import queryStringify from '../lib/queryStringify';
import 'lazysizes';
import 'lazysizes/plugins/parent-fit/ls.parent-fit';


const getMaxFestDate = fes => {
    return(
    fes.date.map(d=>(
        new Date(d.year, d.month-1, d.day)
    )).reduce((prev, curr) => {
        // console.log((prev.getTime() < curr.getTime()? curr:prev).getMonth())
        return prev.getTime() < curr.getTime()? curr:prev
    }, new Date(0,0,0))
    )
}

const isCurrent = fes => (
    ((new Date()).getYear() < getMaxFestDate(fes).getYear())
    ||
    (
        ((new Date()).getYear() === getMaxFestDate(fes).getYear())
        &&
        ((new Date()).getMonth() <= getMaxFestDate(fes).getMonth())
    )
)

const FestivalList = ({fes}) => {
    const [word, setWord] = useState('');
    const [prev, setPrev] = useState(false);

    const getSorted = (fes, prev) => {
        const filtered = fes.filter(f=>(
            f.name.indexOf(word) != -1
            &&
            (isCurrent(f) ^ prev)
        ));
        filtered.sort(
            function (a, b) {
                return +(getMaxFestDate(a).getTime() > getMaxFestDate(b).getTime()) || +(getMaxFestDate(a).getTime() === getMaxFestDate(b).getTime()) - 1;
            }
        );
        return filtered;
    }

    return (
        <>
            <div className="fest-list-in">
                <div className="fest-list-in2">
                    <Form searchHandler={setWord} prevHandler={setPrev} />
                    <Divider />
                    <p className="fest-list-p">찾는 축제 목록</p>
                </div>
                <div className="fest-list-in3">
                    <List>
                        {getSorted(fes, prev).map((fes) => (
                            <ListItem button key={fes.id}>
                                <Link href="/p/[id]" as={`/p/${
                                    queryStringify(fes)
                                    }`}>
                                    <a className="fest-list-a">
                                        <ListItemIcon>
                                            <img data-src={`/img/${fes.id}.jpg`} className="fest-list-img lazyload"></img>
                                        </ListItemIcon>
                                        <ListItemText primary={fes.name} />
                                        <span>{fes.period}</span>
                                    </a>
                                </Link>
                            </ListItem>
                        ))}
                    </List>
                </div>
            </div>
            <style jsx>{`
                .fest-list-img {
                    width: 50vmin;
                    min-width: 200px;
                    max-width: 256px;
                    height: 50vmin;
                    max-height: 256px;
                }
                .fest-list-a {
                    text-decoration: none;
                    color: black;
                    cursor: pointer;
                    background-color: #f9f9f9;
                    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                    width: 50vmin;
                    min-width: 200px;
                    max-width: 256px;
                    padding: 4px 4px;
                }
                .fest-list-p {
                    margin: 4%;
                }
                .fest-list-in {
                    display: grid;
                    height: inherit;
                }
                .fest-list-in2 {
                    position: sticky;
                    top: 0;
                }
                .fest-list-in3 {
                    overflow: auto;
                }
            `}</style>
        </>
    )
};

export default FestivalList;