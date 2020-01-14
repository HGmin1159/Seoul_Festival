module.exports = {
    launch: {
      dumpio: true,
      headless: process.env.HEADLESS !== 'false',
    },
    browser: 'chromium',
    browserContext: 'default',
  }