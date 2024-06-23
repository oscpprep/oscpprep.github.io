/*global browser*/
import { assert } from "chai";

async function navigateWithKeys({
    set_pause_ml = 2000,
    search_mode_strict = true,
    stop_current_search_after = 41,
    inverse_search = false,

    beginning_set_of_keys_to_execute = [],
    ending_set_of_keys_to_execute = [], 

    any_number_of_repeatable_keys = 0,
    key_sets_for_any_number_of_repeatable_keys = [],

    first_repeatable_keys = [], 
    first_text_to_match = [], 
    first_active_element_text = '',
    
    second_repeatable_keys = [], 
    second_text_to_match = [], 
    second_active_element_text = '',
    
    third_repeatable_keys = [], 
    third_text_to_match = [], 
    third_active_element_text = '',
    
    fourth_repeatable_keys = [], 
    fourth_text_to_match = [], 
    fourth_active_element_text = '',
    
    fifth_repeatable_keys = [], 
    fifth_text_to_match = [], 
    fifth_active_element_text = '',
}) 

{
    let stop_searching_after = stop_current_search_after;
    if (any_number_of_repeatable_keys > 0 && key_sets_for_any_number_of_repeatable_keys.length > 0) {
        for (let i = 0; i < any_number_of_repeatable_keys; i++) {
            for (const key of key_sets_for_any_number_of_repeatable_keys) {
                await browser.pause(set_pause_ml);
                await browser.keys(key);
            }
        }
    }
    
    // Execute the first set of keys
    if (beginning_set_of_keys_to_execute.length > 0) {
        for (const key of beginning_set_of_keys_to_execute) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }

    // Continue executing keys until the text matches the desired condition
    if (first_repeatable_keys.length > 0) {stop_searching_after = stop_current_search_after;}
    while (first_repeatable_keys.length > 0) {
        let done = false;
        if (stop_searching_after === 0) {
            done = true;
            assert.fail('This item was never found after maximum tries ! ')
        } else {
            console.log(`stop current search after::: ${stop_searching_after}`)
            stop_searching_after -= 1;
        }
        
        // Update the condition after executing the repeatable keys
        await browser.pause(set_pause_ml);
        const conditionMatched = await browser.execute(eval(first_active_element_text));
        await browser.pause(set_pause_ml);
        if (conditionMatched === null) {
            console.log(`Your web app became unresponsive and the button's ariel-label bacame null. Retry your test with a smaller amount. This error was at the time of executing ${third_active_element_text} to search for ${third_text_to_match} after moving with keys: ${third_repeatable_keys}`);
        } else {
            console.log(`text to match::: "${first_text_to_match}", with the condition of the match::: "${conditionMatched}"`);
            for (const my_item of first_text_to_match ) { 
                // Break out of the loop when the condition is met
                console.log(`checking how condition comes true ::: ${my_item === conditionMatched} where my_item is ::: "${my_item}" and my condition is ::: "${conditionMatched}"`)
                if (inverse_search) {
                    if (search_mode_strict === true && my_item !== conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && !conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    }
                } else {
                    if (search_mode_strict === true && my_item === conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    } 
                }
                    
            };
        };
       
        if (done) {break;}
        for (const key of first_repeatable_keys) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }

    if (second_repeatable_keys.length > 0) {stop_searching_after = stop_current_search_after;}
    while (second_repeatable_keys.length > 0) {
        let done = false;
        if (stop_searching_after === 0) {
            done = true;
            assert.fail('This item was never found after maximum tries ! ')
        } else {
            console.log(`stop current search after::: ${stop_searching_after}`)
            stop_searching_after -= 1;
        }
    
        // Update the condition after executing the repeatable keys
        await browser.pause(set_pause_ml);
        const conditionMatched = await browser.execute(eval(second_active_element_text));
        await browser.pause(set_pause_ml);
        if (conditionMatched === null) {
            console.log(`Your web app became unresponsive and the button's ariel-label bacame null. Retry your test with a smaller amount. This error was at the time of executing ${third_active_element_text} to search for ${third_text_to_match} after moving with keys: ${third_repeatable_keys}`);
        } else {
            console.log(`text to match::: "${second_text_to_match}", with the condition of the match::: ${conditionMatched}`);
    
            for (const my_item of second_text_to_match ) { 
                // Break out of the loop when the condition is met
                console.log(`checking how condition comes true ::: ${my_item === conditionMatched} where my_item is ::: "${my_item}" and my condition is ::: "${conditionMatched}"`)

                if (inverse_search) {
                    if (search_mode_strict === true && my_item !== conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && !conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    }
                } else {
                    if (search_mode_strict === true && my_item === conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    } 
                }
            };
        };

        if (done) {break;}
        for (const key of second_repeatable_keys) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }

    if (third_repeatable_keys.length > 0) {stop_searching_after = stop_current_search_after;}
    while (third_repeatable_keys.length > 0) {
        let done = false;
        if (stop_searching_after === 0) {
            done = true;
            assert.fail('This item was never found after maximum tries ! ')
        } else {
            console.log(`stop current search after::: ${stop_searching_after}`)
            stop_searching_after -= 1;
        }
    
        // Update the condition after executing the repeatable keys
        await browser.pause(set_pause_ml);
        const conditionMatched = await browser.execute(eval(third_active_element_text));
        await browser.pause(set_pause_ml);

        if (conditionMatched === null) {
            console.log(`Your web app became unresponsive and the button's ariel-label bacame null. Retry your test with a smaller amount. This error was at the time of executing ${third_active_element_text} to search for ${third_text_to_match} after moving with keys: ${third_repeatable_keys}`);
        } else {
            console.log(`text to match::: "${third_text_to_match}", with the condition of the match::: ${conditionMatched}`);
    
            for (const my_item of third_text_to_match ) { 
                // Break out of the loop when the condition is met
                console.log(`checking how condition comes true ::: ${my_item === conditionMatched} where my_item is ::: "${my_item}" and my condition is ::: "${conditionMatched}"`)

                if (inverse_search) {
                    if (search_mode_strict === true && my_item !== conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && !conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    }
                } else {
                    if (search_mode_strict === true && my_item === conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    } 
                }
            };
        };

        
        if (done) {break;}
        for (const key of third_repeatable_keys) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }
    if (fourth_repeatable_keys.length > 0) {stop_searching_after = stop_current_search_after;}
    while (fourth_repeatable_keys.length > 0) {
        let done = false;
        if (stop_searching_after === 0) {
            done = true;
            assert.fail('This item was never found after maximum tries ! ')
        } else {
            console.log(`stop current search after::: ${stop_searching_after}`)
            stop_searching_after -= 1;
        }
    
        // Update the condition after executing the repeatable keys
        await browser.pause(set_pause_ml);
        const conditionMatched = await browser.execute(eval(fourth_active_element_text));
        await browser.pause(set_pause_ml);

        if (conditionMatched === null) {
            console.log(`Your web app became unresponsive and the button's ariel-label bacame null. Retry your test with a smaller amount. This error was at the time of executing ${third_active_element_text} to search for ${third_text_to_match} after moving with keys: ${third_repeatable_keys}`);
        } else {
            console.log(`text to match::: "${fourth_text_to_match}", with the condition of the match::: ${conditionMatched}`);
    
            for (const my_item of fourth_text_to_match ) { 
                // Break out of the loop when the condition is met
                console.log(`checking how condition comes true ::: ${my_item === conditionMatched} where my_item is ::: "${my_item}" and my condition is ::: "${conditionMatched}"`)

                if (inverse_search) {
                    if (search_mode_strict === true && my_item !== conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && !conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    }
                } else {
                    if (search_mode_strict === true && my_item === conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    } 
                }
            };
        };

        if (done) {break;}
        for (const key of fourth_repeatable_keys) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }
    if (fifth_repeatable_keys.length > 0) {stop_searching_after = stop_current_search_after;}
    while (fifth_repeatable_keys.length > 0) {
        let done = false;
        if (stop_searching_after === 0) {
            done = true;
            assert.fail('This item was never found after maximum tries ! ')
        } else {
            console.log(`stop current search after::: ${stop_searching_after}`)
            stop_searching_after -= 1;
        }
    
        // Update the condition after executing the repeatable keys
        await browser.pause(set_pause_ml);
        const conditionMatched = await browser.execute(eval(fifth_active_element_text));
        await browser.pause(set_pause_ml);

        if (conditionMatched === null) {
            console.log(`Your web app became unresponsive and the button's ariel-label bacame null. Retry your test with a smaller amount. This error was at the time of executing ${third_active_element_text} to search for ${third_text_to_match} after moving with keys: ${third_repeatable_keys}`);
        } else {
            console.log(`text to match::: "${fifth_text_to_match}", with the condition of the match::: ${conditionMatched}`);
        
            for (const my_item of fifth_text_to_match ) { 
                // Break out of the loop when the condition is met
                console.log(`checking how condition comes true ::: ${my_item === conditionMatched} where my_item is ::: "${my_item}" and my condition is ::: "${conditionMatched}"`)

                if (inverse_search) {
                    if (search_mode_strict === true && my_item !== conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && !conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    }
                } else {
                    if (search_mode_strict === true && my_item === conditionMatched) {
                        done = true;
                        break;
                    } else if (search_mode_strict === false && conditionMatched.includes(my_item)) {
                        done = true;
                        break;
                    } 
                }
            };
        };

        if (done) {break;}
        for (const key of fifth_repeatable_keys) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }

    if (ending_set_of_keys_to_execute.length > 0) {
        for (const key of ending_set_of_keys_to_execute) {
            await browser.pause(set_pause_ml);
            await browser.keys(key);
        }
    }
}


export default navigateWithKeys