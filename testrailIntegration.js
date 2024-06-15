
// testrailIntegration.js
import { execSync } from 'child_process';
import { secrets } from './secrets.js';

const username = secrets.testRail_Username;
const password = secrets.testRail_ApiKey;
const projectId = secrets.testRail_ProjectID; 
const sectionId = secrets.testRail_SuiteID; 
const testrailDomain = secrets.testRail_Domain;

export function sanitizeInput(input) {
    // Escape characters for CLI
    let sanitized = input.replace(/(["'$`\\])/g, '\\$1');
    
    // Escape characters for JSON
    sanitized = sanitized.replace(/\\/g, '\\\\')    // Double backslashes
                         .replace(/"/g, '\\"')     // Escape double quotes
                         .replace(/\n/g, '\\n')    // Newline to \n
                         .replace(/\r/g, '\\r')    // Carriage return to \r
                         .replace(/\t/g, '\\t');   // Tab to \t

    // Encode characters for URL/Web API
    sanitized = encodeURIComponent(sanitized);

    return sanitized;
}

export function alphanumeric(str) {
    // Replace any character that is not a-z, A-Z, 0-9, or space with an empty string
    return str.replace(/[^a-zA-Z0-9 ]/g, ' ');
}

export function firstLineOfError(str) {
    return alphanumeric(str.split('\n')[0]);
}

export function createTestSuite() {
    try {
        const createSuiteCmd = `curl -u "${username}:${password}" -H "Content-Type: application/json" -d '{"name": "Automated Test Suite", "description": "Suite created for automated tests"}' -X POST "https://${testrailDomain}/index.php?/api/v2/add_suite/${projectId}"`;
        console.log(`\n\n Creating test suite via curl::: \n\n ${createSuiteCmd}`)
        const result = execSync(createSuiteCmd, { encoding: 'utf-8' });
        console.log(result);
        const suite = JSON.parse(result);
        return suite.id;
    } catch (error) {
        console.error('Error creating test suite:', error);
        throw error;
    }
}

export function createTestRun(suiteId) {
    try {
        const createRunCmd = `curl -u "${username}:${password}" -H "Content-Type: application/json" -d '{"suite_id": ${suiteId}, "name": "Automated Test Run", "include_all": true}' -X POST "https://${testrailDomain}/index.php?/api/v2/add_run/${projectId}"`;
        console.log(`\n\n Creating test run via curl::: \n\n ${createRunCmd}`)
        const result = execSync(createRunCmd, { encoding: 'utf-8' });
        console.log(result);
        const run = JSON.parse(result);
        return run.id;
    } catch (error) {
        console.error('Error creating test run:', error);
        throw error;
    }
}

export function createTestCase(scenarioName) {
    try {
        const createCaseCmd = `curl -u "${username}:${password}" -H "Content-Type: application/json" -d '{"title": "${scenarioName}", "section_id": ${sectionId}, "type_id": 1, "priority_id": 2}' -X POST "https://${testrailDomain}/index.php?/api/v2/add_case/${sectionId}"`;
        console.log(`\n\n Creating test case via curl::: \n\n ${createCaseCmd}`)
        const result = execSync(createCaseCmd, { encoding: 'utf-8' });
        console.log(result);
        const testCase = JSON.parse(result);
        return testCase.id;
    } catch (error) {
        console.error('Error creating test case:', error);
        throw error;
    }
}

export function addTestResult(runId, caseId, statusId, comment) {
    try {
        const addResultCmd = `curl -u "${username}:${password}" -H "Content-Type: application/json" -d '{"status_id": ${statusId}, "comment": "${comment}"}' -X POST "https://${testrailDomain}/index.php?/api/v2/add_result_for_case/${runId}/${caseId}"`;
        console.log(`\n\n Adding result via curl::: \n\n ${addResultCmd}`)
        const result = execSync(addResultCmd, { encoding: 'utf-8' });
        console.log(result);
    } catch (error) {
        console.error('Error adding test result:', error);
        throw error;
    }
}

// usage::
import { secrets } from './secrets.js';
import { createTestSuite, createTestRun, createTestCase, addTestResult, sanitizeInput, alphanumeric, firstLineOfError} from './testrailIntegration.js';

let suiteId = secrets.testRail_SuiteID;
let runId = secrets.testRail_RunID;

afterScenario: function (world, result, context) {
        console.log(`Scenario tags: ${world.pickle.tags.map(tag => tag.name).join(', ')}`);
        console.log(`Finished scenario: ${world.pickle.name}`);
        console.log('Error: ', result.error);
        console.log('Passed?: ', result.passed);

        console.log('---------------- >>>>> beginning curls <<<<<< ---------------------------------------------------------------------------------------')
        if (process.env.testRailUsername || process.env.testRailApiKey) {
            
            if (!suiteId) {
                suiteId = createTestSuite();
            }

            if (!runId) {
                runId = createTestRun(suiteId);
            }

            const extractCaseIDfromScenarioTags = () => {
                const allTagsOfThisScenario = world.pickle.tags.map(tag => tag.name).join(', '); 
                const regex = /@C(\d+)/g;

                let match;
                const numbers = [];

                while ((match = regex.exec(allTagsOfThisScenario)) !== null) {
                    numbers.push(parseInt(match[1], 10));
                }
                return numbers;
            };

            const statusId = result.passed === false ? 5 : 1;
            const comment = result.passed === false ? firstLineOfError(result.error) : 'Test passed';
            let caseIds = extractCaseIDfromScenarioTags();
            console.log(caseIds);

            if (caseIds.length === 0) {
                console.log(`Case ID not found for scenario: ${world.pickle.name}. Creating a new test case.`);
                const newCaseId = createTestCase(world.pickle.name);
                caseIds.push(newCaseId);
            }

            caseIds.forEach(caseId => {
                addTestResult(runId, caseId, statusId, comment);
            });

            if (result.status === 'failed') {
                console.log(`Error: ${result.exception}`);
            }
        } else {
            console.log(`testRailUsername and testRailApiKey was not provided, therefore no records sent to TestRail`)
        }
        console.log('---------------- >>>>> ending curls <<<<<< ---------------------------------------------------------------------------------------')

    },


