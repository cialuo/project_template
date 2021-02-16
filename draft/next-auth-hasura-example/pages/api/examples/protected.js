// This is an example of to protect an API route
import { getSession } from 'next-auth/client'
import fetch from 'node-fetch'
async function safeParseJSON(response) {
    const body = await response.text();
    try {
        return JSON.parse(body);
    } catch (err) {
        console.error("Error:", err);
        console.error("Response body:", body);
        // throw err;
        return ReE(response, err.message, 500)
    }
}
export default async(req, res) => {
    const session = await getSession({ req })
    const re = await fetch('http://localhost:8069/hpu_api/partner/partner?name=administrator', {
        headers: {
            'api-key': 'admin'
        }
    })
    const d = await re.json()
    console.log('d', d)
    if (session) {
        res.send({ content: d.rows[0] })
    } else {
        res.send({ error: 'You must be sign in to view the protected content on this page.' })
    }
}