import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

// Convert import.meta.url to a file path
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const pageObjects: { [key: string]: any } = {};

interface PageObject {
    [key: string]: any;
}

async function loadPageObjects(dir: string): Promise<void> {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            await loadPageObjects(fullPath);
        } else if (file.endsWith('.ts') && file !== 'page.ts') {
            const moduleName = path.basename(fullPath, '.ts');
            try {
                const module = await import(fullPath);
                pageObjects[moduleName] = module.default;
            } catch (error) {
                console.error(`Failed to import ${fullPath}:`, error);
            }
        }
    }
}

// Adjust the path according to your project structure
loadPageObjects(path.join(__dirname, '../pageobjects'));

export async function globalObjectKeyFinder(key: string) {
    for (const [pageObjectName, pageObject] of Object.entries(pageObjects)) {
        console.log(`currently working with this pageobject::: ${pageObjectName}`)
        if (key in pageObject) {
            return pageObject[key];
        }
    }
    throw new Error(`Key "${key}" not found in any page object.`);
  }
/**
 
Usage example
(async () => {
try {
    let accountMenu = await globalObjectKeyFinder('accountMenu');
    console.log(await accountMenu.waitForClickable());
    await accountMenu.click();
} catch (error) {
    console.error(error);
}
})();
   
*/
  
  