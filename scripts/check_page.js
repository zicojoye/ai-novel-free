const { chromium } = require('playwright');
(async () => {
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    const errors = [];
    const logs = [];
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push('[console.error] ' + msg.text());
      else if (msg.type() === 'warn') logs.push('[console.warn] ' + msg.text());
    });
    page.on('pageerror', err => errors.push('[pageerror] ' + err.message + '\n' + err.stack));
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle', timeout: 15000 });
    await page.waitForTimeout(3000);
    const rootHTML = await page.evaluate(() => document.getElementById('root') ? document.getElementById('root').innerHTML.substring(0, 500) : 'NO ROOT ELEMENT');
    const bodyText = await page.evaluate(() => document.body.innerText.substring(0, 200));
    console.log('=== ROOT innerHTML (first 500 chars) ===');
    console.log(rootHTML || '(EMPTY - 白屏确认)');
    console.log('=== body.innerText ===');
    console.log(bodyText || '(empty)');
    console.log('=== ERRORS ===');
    if (errors.length === 0) {
      console.log('(no errors)');
    } else {
      errors.forEach(e => console.log(e));
    }
    console.log('=== WARNINGS ===');
    logs.slice(0, 10).forEach(l => console.log(l));
  } catch (e) {
    console.log('Playwright error:', e.message);
  } finally {
    if (browser) await browser.close();
  }
})();
