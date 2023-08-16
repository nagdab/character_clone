const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');


(async () => {
    const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' });
    const page = await browser.newPage();

    const targetDirectory = 'downloaded-site';
    if (!fs.existsSync(targetDirectory)) {
        fs.mkdirSync(targetDirectory);
    }

    // Intercept network requests
    await page.setRequestInterception(true);

    page.on('request', request => {
        request.continue();
    });

    page.on('response', async (response) => {
        const url = new URL(response.url());
        let filePath;
    
        if (url.protocol === 'data:') {
            // Handle data URLs: generate a unique filename using a hash of the content
            const hash = crypto.createHash('md5').update(url.href).digest('hex');
            filePath = path.join(__dirname, targetDirectory, 'data', `${hash}.svg`);
        } else {
            filePath = path.join(__dirname, targetDirectory, url.hostname, ...url.pathname.split('/').filter(p => p));
    
            if (response.url() === 'http://character.ai/') {
                filePath = path.join(__dirname, targetDirectory, 'index.html');
            } else if (url.pathname.endsWith('/')) {
                filePath = path.join(filePath, 'index.html');
            }
        }
    
        // Ensure the directory structure is preserved
        if (!fs.existsSync(path.dirname(filePath))) {
            fs.mkdirSync(path.dirname(filePath), { recursive: true });
        }
    
        // Handle the content by type
        if (response.status() !== 200) {
            return;
        }
    
        const buffer = await response.buffer();

        if (url.pathname.endsWith('/')) {
            console.warn(`NEW INDEX.HTML file: ${buffer}`)
        }

        if (fs.existsSync(filePath)) {
            console.warn(`Overwriting file: ${filePath}`);
        }
        fs.writeFileSync(filePath, buffer);
    });

    // Navigate to the desired URL.
    await page.goto('http://character.ai', { waitUntil: 'networkidle2' });

    // Optionally, wait for an additional set amount of time (e.g., 10 seconds).
    await page.waitForTimeout(10000);

    await browser.close();
})();