import React, { useState } from 'react';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Form from './Form';
import Link from 'next/link';
import queryString from 'query-string';

const FestivalList = ({fes}) => {
    const [word, setWord] = useState('');
    return (
        <>
            <Form searchHandler={setWord} />
            <Divider />
            <p className="fest-list-p">찾는 축제 목록</p>
            <List>
                {fes.map((fes) => (
                    (fes.name.indexOf(word) != -1)
                    &&
                    <ListItem button key={fes.id}>
                        <Link href="/p/[id]" as={`/p/${
                            queryString.stringify({
                                id: fes.id,
                                name: fes.name,
                                x: fes.x,
                                y: fes.y,
                                cluster: fes.cluster,
                                man: fes.man,
                                exp: fes.explanation.replace(/(\\(n|t))/g, ''),
                                region: fes.region.replace(/(\\(n|t))/g, ''),
                                place: fes.place.replace(/(\\(n|t))/g, '')
                            })}`}>
                            <a className="fest-list-a">
                                <ListItemIcon>
                                    <img src={`/img/${fes.id}.jpg`} className="fest-list-img"></img>
                                </ListItemIcon>
                                <ListItemText primary={fes.name} />
                                <span>{fes.period}</span>
                            </a>
                        </Link>
                    </ListItem>
                ))}
            </List>
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
            `}</style>
        </>
    )
};

export default FestivalList;