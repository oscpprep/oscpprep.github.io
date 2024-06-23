/*global $, browser*/
import { sync as globSync } from 'glob';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const all_objects = {};

// Use glob to find all JS files in the pageobjects directory
const files = globSync(path.resolve(__dirname, '../pageobjects/**/*.js'));

// Dynamically import each file and add its exports to all_objects
for (const file of files) {
    const module = await import(file);
    Object.assign(all_objects, module.default || module);
}

async function globalObjectKeyFinder(objectName) {
    if (all_objects[objectName]) {
        return all_objects[objectName];
    }
    throw new Error(`Object with name ${objectName} not found`);
}

export default globalObjectKeyFinder;
