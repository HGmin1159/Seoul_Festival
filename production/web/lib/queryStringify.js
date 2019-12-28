import queryString from 'query-string';

const queryStringify = (festival) => (
    queryString.stringify({
        id: festival.id,
        name: festival.name,
        x: festival.x,
        y: festival.y,
        cluster: festival.cluster,
        man: festival.man,
        exp: festival.explanation.replace(/(\\(n|t))/g, ''),
        region: festival.region.replace(/(\\(n|t))/g, ''),
        place: festival.place.replace(/(\\(n|t))/g, ''),
        link: /(^http)|(^www)/.test(festival.link)? festival.link: null
    })
);

export default queryStringify;