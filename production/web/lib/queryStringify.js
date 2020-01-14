import queryString from 'query-string';


const queryStringify = (festival) => {
    const encodeInPlace = obj => {
        Object.keys(obj).map(key => obj[key] = encodeURIComponent(obj[key]));
    };
    let obj = {
        id: festival.id,
        name: festival.name,
        x: festival.x,
        y: festival.y,
        cluster: festival.cluster,
        man: festival.man,
        exp: festival.explanation.replace(/(\\(n|t))/g, ''),
        region: festival.region.replace(/(\\(n|t))/g, ''),
        place: festival.place.replace(/(\\(n|t))/g, ''),
        link: festival.link
    };
    encodeInPlace(obj);
    return queryString.stringify(obj)
}

export default queryStringify;