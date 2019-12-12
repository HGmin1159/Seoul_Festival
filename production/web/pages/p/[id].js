import fetch from 'isomorphic-unfetch';
import Head from 'next/head';
import fes from '../../2019.json';
import FullWidthTabs from '../../components/FullWidthTabs';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
// import https from "https";

// const agent = new https.Agent({
//   rejectUnauthorized: false
// });

const Info = ({ fe, res }) => {


  const theme = createMuiTheme({
    palette: {
      primary: {
        main: '#8ebdd8',
        contrastText: 'white'
      }
    },
  });

  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"
          integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
          crossorigin="" />

        <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
          integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
          crossorigin=""></script>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
      </Head>
      <ThemeProvider theme={theme}>
        <FullWidthTabs fe={fe} res={res} fes={fes}></FullWidthTabs>
      </ThemeProvider>

    </>
  )
}

Info.getInitialProps = async function (context) {
  const fe = JSON.parse(decodeURI(context.query.id));
  fe.exp = fe.exp.replace(/escapeSlash/g, "/");
  const res = await fetch(`https://a.seoulfestival.shop/restaurants?id=${fe.id}`);
  const dataRes = await res.json();

  return {
    fe: fe,
    res: dataRes
  };
}

export default Info;
