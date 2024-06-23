
/*global $, browser*/
import { assert } from "chai";

async function clickElementByTextOrXpathOrObjectKey({text = '', xpath = '', objectKey = null}){
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
      await element.moveTo();
      await element.click();
      await element.waitForExist(1000);
      await element.waitForDisplayed(1000);
      

      await browser.keys('Enter');
      console.log("Enter key was pressed");
    } else {
      console.log('* "NO SCRIPT" tag was NOT detected *');
      element.waitForDisplayed();
      await element.waitForExist(1000);
      await element.waitForDisplayed(1000);
      

      element.click()
      console.log("Enter key was NOT pressed");
    }
  } else {
    assert.fail(`Element with text '${text}' not found`);
  }

  
}


export default clickElementByTextOrXpathOrObjectKey