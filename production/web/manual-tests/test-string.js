const puppeteer = require('puppeteer');
const expect = require('expect-puppeteer');
const { setDefaultOptions } = require('expect-puppeteer');
let fixture = require('../2019.json');

setDefaultOptions({ timeout: 3000 })

fixture = fixture.map(festival => ({
    name: festival.name,
    region: '개최지역: ' + festival.region.replace(/(\\(n|t))/g, ''),
    place: '축제장소: ' + festival.place.replace(/(\\(n|t))/g, ''),
    link: '누리집: ' + festival.link,
    exp: festival.explanation.replace(/(\\(n|t))/g, '')
}));


(async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    await page.goto('https://seoul-festival-git-dev.abcdefg.now.sh');
    // await page.goto('http://localhost:3000');
        
    await expect(page).toClick('svg');
    await page.waitFor('.fest-list-a');
    let num = await page.$$eval('.fest-list-a', divs => divs.length);
    for (let i = 0; i < num; i++) {
        await page.evaluate((i) => {
            document.querySelectorAll('.fest-list-a')[i].click();
        }, i);
        await page.waitFor('.info');

        let name = await page.$eval('.info-title', el => el.textContent)
        let region = await page.$eval('.text1', el => el.textContent)
        let place = await page.$eval('.text2', el => el.textContent)
        let link = await page.$$('.link')
        if (link.length !== 0) {
            link = await page.$eval('.link', el => el.textContent)
        }
        let exp = await page.$eval('.text3', el => el.textContent)
        
        let flag = false;
        const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
        for (let festival of fixture) {
            flag = flag || eq(festival, {name, region, place, link, exp})
        }
        if (flag === false) {
            console.log({name, region, place, link, exp})
        }        

        await page.goBack();
        await expect(page).toClick('svg');
        await page.waitFor('.fest-list-a');
    }
    await page.evaluate(() => {
        document.querySelector('#prev').click();
    });
    await page.waitForFunction("document.querySelectorAll('.fest-list-a > div > span').length > 50");
    num = await page.$$eval('.fest-list-a', divs => divs.length);
    for (let i = 0; i < num; i++) {
        await page.evaluate((i) => {
            document.querySelectorAll('.fest-list-a')[i].click();
        }, i);
        await page.waitFor('.info');

        let name = await page.$eval('.info-title', el => el.textContent)
        let region = await page.$eval('.text1', el => el.textContent)
        let place = await page.$eval('.text2', el => el.textContent)
        let link = await page.$$('.link')
        if (link.length !== 0) {
            link = await page.$eval('.link', el => el.textContent)
        }
        let exp = await page.$eval('.text3', el => el.textContent)
        
        let flag = false;
        const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
        for (let festival of fixture) {
            flag = flag || eq(festival, {name, region, place, link, exp})
        }
        if (flag === false) {
            console.log({name, region, place, link, exp})
        }

        await page.goBack();
        await expect(page).toClick('svg');
        await page.waitFor('.fest-list-a');
        await page.evaluate(() => {
            document.querySelector('#prev').click();
        });
        await page.waitForFunction("document.querySelectorAll('.fest-list-a > div > span').length > 50");
    }
}
)();
