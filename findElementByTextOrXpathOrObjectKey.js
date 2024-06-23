/*global $, browser*/
import { assert } from "chai";

async function findElementByTextOrXpathOrObjectKey({text = '', xpath = '', objectKey = null}){
  let selector;
  let element;
  if (text.length > 0 && xpath.length === 0) {
      // Selects elements by exact text match
      selector = `//*[text()='${text}']`;
      element = await $(selector);
      await element.waitForExist(1000);
      await element.waitForDisplayed(1000);
  } else if (xpath.length > 0) {
      // Uses provided XPath
      selector = xpath;
      element = await $(selector);
      await element.waitForExist(1000);
      await element.waitForDisplayed(1000);

  } else if (objectKey !== null) {
      // Uses provided element
      element = objectKey;
  } else {
      // Handle case where neither text nor XPath is provided
      throw new Error(`Neither text nor XPath provided. \n\n text: "${text}" \n\n xpath: "${xpath}" \n\n objectKey: "${objectKey}" \n\n selector: "${selector}" \n\n element: "${element}" \n\n `);
  }

  if (element.isExisting()) {
    if (!(await element.isDisplayedInViewport())){
      await element.scrollIntoView({ block: 'center', inline: 'center' });
    }

    // now lets check pages with the noscript tag since mouse click works on them
    const isNoscriptPresent = await $('noscript').isExisting();
    if (isNoscriptPresent) {
        console.log('* NO SCRIPT tag DETECTED *');
        await element.waitForExist(1000);
        await element.waitForDisplayed(1000);
        
        await browser.setWindowSize(1280, 720);
        await browser.execute(() => {document.body.style.transform = 'scale(0.55)';});
        // sometimes clicks can throw "error not interactable" 
        // so, skip clicking since this is to only find the element and make sure it is displayed.
        // this is the difference between this function and the clickElementByTextOrXpathOrObjectKey:
        // list of the methods are: .moveTo(), .click(), .doubleClick(), .action('pointer')...
        try {
          await browser.pause(1000);
          await element.moveTo();
          await browser.action('pointer')
          .move({ duration: 0, origin: element })
          .down({ button: 0 }) // left button
          .pause(10)
          .up({ button: 0 })
          .perform();           

        } catch (error) {
          console.error('An error occurred:', error);
          // Regular expression to match either "move target out of bounds" or "element not interactable"
          const errorMessageRegex = /move target out of bounds|element not interactable/;
          if (errorMessageRegex.test(error.message)) {
            const currentElementText = await browser.execute(eval(() => document.activeElement.textContent))
            if (`${currentElementText}`.includes(await element.getText())) {
              console.log(`we are active on the target element, you can press enter if you want to`)
            } else {
              console.log(`this was the active element text:: ${currentElementText} \n\n and our target element text was :: ${await element.getText()}`);
            }
            console.error('Caught a specific error related to element interactivity:', error);
          } else {
              // If the error is not the one we're looking for, rethrow it
              throw error;
          }
        }
        
        await element.waitForExist(1000);
        await element.waitForDisplayed(1000);

    } else {
      console.log('* "NO SCRIPT" tag was NOT detected *');
      await element.waitForExist(1000);
      await element.waitForDisplayed(1000);
      await element.isDisplayed()
    }
  } else {
    assert.fail(`Element with text '${text}' not found`);
  }


}


export default findElementByTextOrXpathOrObjectKey