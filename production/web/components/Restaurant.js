const Restaurant = ({ res }) => {
    return (
        <>
            <div className="name">
                {res.place_name}
            </div>
            <div className="category">
                {res.category_name.slice(res.category_name.indexOf('>') + 2)}
            </div>
            <style jsx>{`
                .name {
                    font-size: 0.9rem;
                }
                .category {
                    font-size: 0.7rem;
                }
            `}</style>
        </>
    )
}

export default Restaurant;