const { remote } = require('webdriverio');
require('dotenv').config();

// Define a custom command outside of the configuration object
function setupBrowser(browser) {
    browser.addCommand('getEnvVar', (key) => {
        return process.env[key];
    });
}

const config = {
    capabilities: {
        browserName: 'chrome',
    },
};

async function runInteractive() {
    const browser = await remote(config);

    // Call the setup function to add the custom command
    setupBrowser(browser);

    // Start the REPL session
    const repl = require('repl').start({
        prompt: 'WebdriverIO > ',
    });

    // Expose the browser object to the REPL session
    repl.context.browser = browser;

    // Close the browser when the REPL session is exited
    repl.on('exit', async () => {
        await browser.deleteSession();
    });
}

runInteractive();
/**
run this with:

node ./interactive.js

*/
