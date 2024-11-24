import { expect, $, browser } from '@wdio/globals'
import { assert } from "chai";
import readline from 'readline';


/**
 * Switches to a new tab, performs actions, and switches back to the original tab.
 *
 * @param {WebdriverIO.Element} anchor - The anchor element to click and open a new tab.
 * @param {string[]} initialHandles - The original set of tab handles.
 * @param {Function} validateFn - A function to perform validations in the new tab.
 */
export async function switchToNewTabAndValidate(anchor, initialHandles, validateFn) {
    const errors = [];
    const browser = global.browser;

    try {
        // Click the anchor to open a new tab
        await anchor.click();

        // Wait for the new tab to open
        await browser.waitUntil(async () => {
            const updatedHandles = await browser.getWindowHandles();
            return updatedHandles.length > initialHandles.length;
        }, {
            timeout: 5000,
            timeoutMsg: `New tab did not open for anchor: ${await anchor.getText()}`,
        });

        // Identify the new tab
        const updatedHandles = await browser.getWindowHandles();
        const newTabHandle = updatedHandles.find(handle => !initialHandles.includes(handle));
        if (!newTabHandle) {
            throw new Error("Failed to identify the new tab.");
        }

        // Switch to the new tab
        await browser.switchToWindow(newTabHandle);

        // Execute validation logic in the new tab
        await validateFn();

        // Close the new tab
        await browser.closeWindow();

    } catch (error) {
        errors.push(`Error during tab validation: ${error.message}`);
    } finally {
        // Switch back to the original tab
        const remainingHandles = await browser.getWindowHandles();
        const originalHandle = initialHandles[0];
        if (!remainingHandles.includes(originalHandle)) {
            throw new Error("Original tab handle not found. Cannot switch back.");
        }
        await browser.switchToWindow(originalHandle);
    }

    if (errors.length > 0) {
        throw new Error(errors.join("\n"));
    }
}


/**
 * Verifies that a video element on the page is playing.
 * This function locates the first video element on the page (excluding those inside <script> tags),
 * checks if it is displayed, verifies it is not paused, and ensures the `currentTime` progresses over time.
 * 
 * Steps:
 * 1. Locate the video element on the page.
 * 2. Confirm the video element is visible.
 * 3. Retrieve the initial playback time of the video.
 * 4. Pause for 2 seconds to allow the video to play.
 * 5. Retrieve the updated playback time.
 * 6. Verify that the video is not paused and its playback time has progressed.
 * 
 * @throws {Error} If the video is not displayed, paused, or its `currentTime` does not advance.
 */
export async function verify_video_is_playing() {
    // Locate the video element
    const videoElement = await $('//video[not(ancestor::script)]');

    // Ensure the video is displayed
    await expect(videoElement).toBeDisplayed();

    // Get the initial currentTime
    const initialTime = await browser.execute((video) => video.currentTime, videoElement);

    // Wait for a moment to see if the video is playing
    await browser.pause(2000); // Pause for 2 seconds

    // Get the updated currentTime
    const updatedTime = await browser.execute((video) => video.currentTime, videoElement);

    // Get the paused state
    const isPaused = await browser.execute((video) => video.paused, videoElement);

    // Assertions
    expect(isPaused).toBe(false); // Video should not be paused
    expect(updatedTime).toBeGreaterThan(initialTime); // Video should have progressed
};


/**
 * Simulates scrolling the entire webpage to load dynamic content.
 * This function scrolls down the page incrementally in steps of 100px until reaching the bottom
 * and then scrolls back up in the same manner. It ensures that dynamically loaded content gets a chance
 * to render as the user would interact with the page.
 * 
 * Steps:
 * 1. Retrieve the total height of the webpage.
 * 2. Scroll down incrementally by 100px steps with pauses in between.
 * 3. Scroll back up incrementally by 100px steps with pauses in between.
 * 
 * @throws {Error} If the scrolling encounters issues due to unexpected page behavior or JavaScript execution.
 */
export async function scroll_load() {
    // Load the total page height
    const pageHeight = await browser.execute(() => document.body.scrollHeight);

    // Scroll down incrementally
    for (let i = 0; i < Math.ceil(pageHeight / 100); i++) {
        await new Promise(resolve => setTimeout(resolve, 10))
            .then(() => browser.scroll(0, i * 100));
        await browser.pause(100); // Small pause to allow content to load
    }

    // Scroll back up incrementally
    for (let i = 0; i < Math.ceil(pageHeight / 100); i++) {
        await new Promise(resolve => setTimeout(resolve, 10))
            .then(() => browser.scroll(0, i * -100));
        await browser.pause(100); // Small pause to mimic user behavior
    }
};


export async function getSimplifiedXPath (element) {
    return await browser.execute(
        function (el) {
            function getXPath(el) {
                if (el.id === 'html') {
                    return '/html';
                }
                if (el === document.body) {
                    return '/html/body';
                }

                const siblings = Array.from(el.parentNode.children).filter(
                    sibling => sibling.tagName === el.tagName
                );

                const index = siblings.length > 1
                    ? Array.from(siblings).indexOf(el) + 1
                    : null;

                const tagWithIndex = index
                    ? `${el.tagName.toLowerCase()}[${index}]`
                    : el.tagName.toLowerCase();

                return `${getXPath(el.parentNode)}/${tagWithIndex}`;
            }

            return getXPath(el);
        },
        element 
    );
};
