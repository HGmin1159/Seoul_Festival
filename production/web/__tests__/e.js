const { setDefaultOptions } = require('expect-puppeteer');
const devices = require( "puppeteer/DeviceDescriptors" );

jest.setTimeout(300000);
setDefaultOptions({ timeout: 3000 })


for (let device of devices) {
    describe(device.name, () => {
        beforeAll(async () => {
            console.log(new Date());
            console.log(device.name);
            await page.emulate(device);
            await page.goto('https://seoul-festival-git-dev.abcdefg.now.sh');
        });

        it('should', async () => {
            await expect(page).toClick('svg');
            await page.waitFor('.fest-list-a');
            let num = await page.$$eval('.fest-list-a', divs => divs.length);
            for (let i = 0; i < num; i++) {
                await page.evaluate((i) => {
                    document.querySelectorAll('.fest-list-a')[i].click();
                }, i);
                await page.waitFor('.info');
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
                await page.goBack();
                await expect(page).toClick('svg');
                await page.waitFor('.fest-list-a');
                await page.evaluate(() => {
                    document.querySelector('#prev').click();
                });
                await page.waitForFunction("document.querySelectorAll('.fest-list-a > div > span').length > 50");
            }
        })
    });
}
