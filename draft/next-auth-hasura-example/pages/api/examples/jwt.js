// This is an example of how to read a JSON Web Token from an API route
import jwt from 'next-auth/jwt'
import { getSession } from 'next-auth/client'

export default async(req, res) => {
    const session = await getSession({ req })
    if (session && session.token) {
        res.send(JSON.stringify({ token: session.token }, null, 2))
    } else {
        res.status(404).send({ error: 'Not found' })
    }

}