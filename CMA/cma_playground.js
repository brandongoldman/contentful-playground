const contentful = require('contentful-management')

// define environment and space details
const ACCESS_TOKEN = 'CFPAT-ocPMQqaIehFr-MU3QsER0viME4w0IVcnR9pQ6An0VBY';
const SPACE = 'tam1qruk5se1';
const ENVIRONMENT = 'master';
const TEST_CONTENT_TYPE_ID = 'creditcard'; // swap with content type desired

/*--------------------------------------------------------------------
|  Create Content Entry
|
|  Purpose:     This code block creates a new content entry based
|               on an existing content type.
*-------------------------------------------------------------------- */
function createContentEntry() {
    const client = contentful.createClient({
        accessToken: ACCESS_TOKEN
    });
    client.getSpace(SPACE)
        .then((space) => space.getEnvironment(ENVIRONMENT))
        .then((environment) => environment.createEntryWithId(TEST_CONTENT_TYPE_ID, 'Test_Entry_ID', {
            fields: {
                name: { // desired field(s)
                    'en-US': 'Test Name' // add content by locale if desired
                }
            }
        }))
        .then((entry) => console.log(entry))
        .catch(console.error)
}

// Driver Functions
createContentEntry();
