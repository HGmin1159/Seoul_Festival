import React from 'react';
import fes from '../2019.json';
import TemporaryDrawer from '../components/TemporaryDrawer.js';
import LeafMap from '../components/LeafMap';


const Home = () => {
  return (
    <>
      <TemporaryDrawer fes={fes}></TemporaryDrawer>
      
      <LeafMap fes={fes} full={true}></LeafMap>

      <style jsx>{`
        body {
          padding: 0;
          margin: 0;
        }
        html, body {
            height: 100vh;
            width: 100vw;
        }
      `}</style>
    </>
  )
};

export default Home;