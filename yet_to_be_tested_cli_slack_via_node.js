const { execSync } = require('child_process');

function postReviewToSlack(webhookUrl, text, reviewText, linkUrl, hotelName, rating, imageUrl, imageAlt) {
    const payload = JSON.stringify({
        text: text,
        blocks: [
            {
                type: "section",
                text: {
                    type: "mrkdwn",
                    text: "Danny Torrence left the following review for your property:"
                }
            },
            {
                type: "section",
                block_id: "section567",
                text: {
                    type: "mrkdwn",
                    text: <${linkUrl}|${hotelName}> \n :star: \n ${reviewText}
                },
                accessory: {
                    type: "image",
                    image_url: imageUrl,
                    alt_text: imageAlt
                }
            },
            {
                type: "section",
                block_id: "section789",
                fields: [
                    {
                        type: "mrkdwn",
                        text: *Average Rating*\n${rating}
                    }
                ]
            }
        ]
    });

    const command = curl -X POST ${webhookUrl} -H 'Content-type: application/json' --data '${payload.replace(/'/g, "\\'")}';
    execSync(command, { stdio: 'inherit' });
}

// Example usage
const webhookUrl = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX';
const text = 'Danny Torrence left a 1 star review for your property.';
const reviewText = 'Doors had too many axe holes, guest in room 237 was far too rowdy, whole place felt stuck in the 1920s.';
const linkUrl = 'https://example.com';
const hotelName = 'Overlook Hotel';
const rating = '1.0';
const imageUrl = 'https://is5-ssl.mzstatic.com/image/thumb/Purple3/v4/d3/72/5c/d3725c8f-c642-5d69-1904-aa36e4297885/source/256x256bb.jpg';
const imageAlt = 'Haunted hotel image';

postReviewToSlack(webhookUrl, text, reviewText, linkUrl, hotelName, rating, imageUrl, imageAlt);
